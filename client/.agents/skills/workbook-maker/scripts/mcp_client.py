#!/usr/bin/env python3
"""공통 MCP 클라이언트: 배포 폴더의 .env로 서버 도구를 호출하고 산출물을 검증해 저장한다.

Python 3.10+ 표준 라이브러리만 사용한다. 모든 서비스가 같은 파일을 쓴다(수정 금지).

  python .agents/skills/<skill>/scripts/mcp_client.py ping
  python .agents/skills/<skill>/scripts/mcp_client.py call <tool> [--args a.json]
         [--arg key=value] [--arg-file key=file.json] [--out r.json]
         [--output-root outputs] [--into DIR]
  python .agents/skills/<skill>/scripts/mcp_client.py download --from r.json [--output-root outputs] [--into DIR]

종료 코드: 0 성공, 1 서버가 invalid_input/rejected/error 반환, 2 연결·인증·설정 오류, 3 산출물 검증 실패
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import re
import shutil
import socket
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPHandler, HTTPRedirectHandler, HTTPSHandler, Request, build_opener

CLIENT_VERSION = "1.0.0"
PROTOCOL_VERSION = "2025-06-18"
BUNDLE_FORMAT = "mcp-artifact-bundle-v1"
PACKAGE_ROOT = Path(__file__).resolve().parents[4]
FAILURE_STATUSES = {"invalid_input", "rejected", "error"}
LOOPBACK = {"127.0.0.1", "localhost", "::1"}


class ConfigError(RuntimeError):
    """Configuration, connection or authentication problem (exit 2)."""


class ArtifactError(RuntimeError):
    """Artifact verification problem (exit 3)."""


# ---------------------------------------------------------------- configuration

def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.strip().partition("=")
        if not separator or key.startswith("#"):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def check_url(url: str, *, purpose: str) -> str:
    parts = urlsplit(url)
    if parts.username or parts.password or parts.fragment:
        raise ConfigError(f"{purpose} URL must not contain credentials or a fragment")
    if purpose == "MCP" and parts.query:
        raise ConfigError("MCP URL must not contain a query")
    secure = parts.scheme == "https" or (parts.scheme == "http" and parts.hostname in LOOPBACK)
    if not parts.hostname or not secure:
        raise ConfigError(f"{purpose} URL must use HTTPS")
    return url


def configuration() -> tuple[str, str]:
    values = read_env(PACKAGE_ROOT / ".env")
    url = values.get("MCP_URL", "").strip()
    token = values.get("MCP_API_TOKEN", "").strip()
    if not url or not token:
        raise ConfigError("Set MCP_URL and MCP_API_TOKEN in the package .env")
    return check_url(url, purpose="MCP"), token


# ---------------------------------------------------------------- transport

def _ipv4_first(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    host, port = address
    infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    infos.sort(key=lambda info: info[0] != socket.AF_INET)
    last_error: OSError | None = None
    for family, socktype, proto, _, sockaddr in infos:
        sock = socket.socket(family, socktype, proto)
        try:
            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sockaddr)
            return sock
        except OSError as exc:
            last_error = exc
            sock.close()
    raise last_error or OSError("No usable address")


class _HTTPConnection(http.client.HTTPConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = _ipv4_first


class _HTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = _ipv4_first


class _HTTPHandler(HTTPHandler):
    def http_open(self, request):
        return self.do_open(_HTTPConnection, request)


class _HTTPSHandler(HTTPSHandler):
    def https_open(self, request):
        return self.do_open(_HTTPSConnection, request)


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ConfigError("Redirects are not allowed")


def _opener():
    return build_opener(_HTTPHandler(), _HTTPSHandler(), _NoRedirect())


class McpClient:
    def __init__(self, url: str, token: str, timeout: float) -> None:
        self.url = url
        self.timeout = timeout
        self.next_id = 1
        self.opener = _opener()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json; charset=utf-8",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        }

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            with self.opener.open(Request(self.url, data=data, headers=self.headers, method="POST"),
                                  timeout=self.timeout) as response:
                session = response.headers.get("Mcp-Session-Id")
                if session:
                    self.headers["Mcp-Session-Id"] = session
                body = response.read()
        except HTTPError as exc:
            if exc.code in (401, 403):
                raise ConfigError(f"Authentication rejected (HTTP {exc.code}); check MCP_API_TOKEN") from None
            raise ConfigError(f"MCP server returned HTTP {exc.code}") from None
        except (URLError, TimeoutError, OSError) as exc:
            raise ConfigError(f"Cannot reach MCP server: {exc}") from None
        if not body:
            return {}
        text = body.decode("utf-8")
        if text.lstrip().startswith(("event:", "data:")):
            lines = [line[5:].strip() for line in text.splitlines() if line.startswith("data:")]
            text = lines[-1] if lines else "{}"
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ConfigError("MCP server returned invalid JSON") from None

    def request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        identity = self.next_id
        self.next_id += 1
        response = self._post({"jsonrpc": "2.0", "id": identity, "method": method, "params": params})
        if "error" in response:
            message = response["error"].get("message", "unknown") if isinstance(response["error"], dict) else "unknown"
            raise ConfigError(f"MCP protocol error: {message}")
        return response.get("result") or {}

    def initialize(self) -> dict[str, Any]:
        result = self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "mcp-client", "version": CLIENT_VERSION},
        })
        if result.get("protocolVersion"):
            self.headers["MCP-Protocol-Version"] = result["protocolVersion"]
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result

    def call(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        result = self.request("tools/call", {"name": tool, "arguments": arguments})
        structured = result.get("structuredContent")
        if isinstance(structured, dict):
            value = structured
        else:
            texts = [item.get("text", "") for item in result.get("content", []) if item.get("type") == "text"]
            try:
                value = json.loads(texts[0]) if texts else {}
            except json.JSONDecodeError:
                value = {"status": "error", "data": {"message": texts[0][:2000]}}
        if result.get("isError") and value.get("status") not in FAILURE_STATUSES:
            value = {**value, "status": "error"}
        return value


# ---------------------------------------------------------------- artifacts

def _safe_path(value: Any) -> PurePosixPath:
    if (not isinstance(value, str) or not value or "\\" in value or ":" in value
            or value.startswith("/") or any(part in ("", ".", "..") for part in value.split("/"))):
        raise ArtifactError(f"Unsafe artifact path: {value!r}")
    return PurePosixPath(value)


def _download(url: str, timeout: float) -> bytes:
    check_url(url, purpose="Artifact")
    try:
        with _opener().open(Request(url, method="GET"), timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        raise ArtifactError(f"Artifact download failed (HTTP {exc.code}); request a fresh link") from None
    except (URLError, TimeoutError, OSError, ConfigError) as exc:
        raise ArtifactError(f"Artifact download failed: {exc}") from None


def _entry_bytes(entry: dict[str, Any], timeout: float) -> bytes:
    encoding = entry.get("encoding")
    if encoding == "utf-8" and isinstance(entry.get("content"), str):
        data = entry["content"].encode("utf-8")
    elif encoding == "base64" and isinstance(entry.get("content"), str):
        try:
            data = base64.b64decode(entry["content"], validate=True)
        except ValueError:
            raise ArtifactError(f"Invalid base64 for {entry.get('path')}") from None
    elif encoding == "url" and isinstance(entry.get("url"), str):
        data = _download(entry["url"], timeout)
    else:
        raise ArtifactError(f"Unsupported artifact encoding for {entry.get('path')}")
    if hashlib.sha256(data).hexdigest() != entry.get("sha256"):
        raise ArtifactError(f"Artifact hash mismatch: {entry.get('path')}")
    if "size" in entry and entry["size"] != len(data):
        raise ArtifactError(f"Artifact size mismatch: {entry.get('path')}")
    return data


def _job_name(value: Any) -> str:
    name = re.sub(r"[^\w가-힣.-]+", "_", str(value or ""), flags=re.UNICODE).strip("._ ")[:80]
    return name or "result"


def save_bundle(bundle: Any, *, output_root: Path, into: Path | None, timeout: float) -> Path:
    if not isinstance(bundle, dict) or bundle.get("format") != BUNDLE_FORMAT:
        raise ArtifactError("Unsupported artifact bundle format")
    entries = bundle.get("files")
    if not isinstance(entries, list) or not entries:
        raise ArtifactError("Artifact bundle is empty")
    seen: set[str] = set()
    for entry in entries:
        key = str(_safe_path(entry.get("path") if isinstance(entry, dict) else None)).casefold()
        if key in seen:
            raise ArtifactError(f"Duplicate artifact path: {entry['path']}")
        seen.add(key)

    if into is not None:
        target = into.resolve()
        if not target.is_dir():
            raise ArtifactError(f"--into directory does not exist: {target}")
        for entry in entries:
            if target.joinpath(*_safe_path(entry["path"]).parts).exists():
                raise ArtifactError(f"Refusing to overwrite {entry['path']}")
        parent = target
    else:
        parent = output_root.resolve()
        parent.mkdir(parents=True, exist_ok=True)
        base = _job_name(bundle.get("job"))
        target = parent / base
        suffix = 2
        while target.exists():
            target = parent / f"{base}_{suffix:02d}"
            suffix += 1

    staging = Path(tempfile.mkdtemp(prefix=".download-", dir=parent))
    try:
        for entry in entries:
            destination = staging.joinpath(*_safe_path(entry["path"]).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            # write_bytes keeps server bytes exact (no CRLF translation on Windows)
            destination.write_bytes(_entry_bytes(entry, timeout))
        if into is None:
            staging.rename(target)
        else:
            for file in sorted(path for path in staging.rglob("*") if path.is_file()):
                destination = target / file.relative_to(staging)
                destination.parent.mkdir(parents=True, exist_ok=True)
                file.replace(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
    return target


def strip_contents(bundle: dict[str, Any]) -> dict[str, Any]:
    files = [{key: value for key, value in entry.items() if key != "content"}
             for entry in bundle.get("files", []) if isinstance(entry, dict)]
    return {**bundle, "files": files}


# ---------------------------------------------------------------- commands

def parse_pairs(items: list[str], *, from_file: bool) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in items:
        key, separator, value = item.partition("=")
        if not separator or not key:
            raise ConfigError(f"Expected key=value, got {item!r}")
        if from_file:
            try:
                result[key] = json.loads(Path(value).read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ConfigError(f"Cannot read JSON file for {key}: {exc}") from None
        else:
            result[key] = value
    return result


def build_arguments(args: argparse.Namespace) -> dict[str, Any]:
    arguments: dict[str, Any] = {}
    if args.args:
        try:
            loaded = json.loads(Path(args.args).read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigError(f"Cannot read --args: {exc}") from None
        if not isinstance(loaded, dict):
            raise ConfigError("--args must contain a JSON object")
        arguments.update(loaded)
    arguments.update(parse_pairs(args.arg, from_file=False))
    arguments.update(parse_pairs(args.arg_file, from_file=True))
    return arguments


def finish(response: dict[str, Any], args: argparse.Namespace) -> int:
    saved = None
    bundle = response.get("artifacts")
    if isinstance(bundle, dict) and bundle.get("files"):
        saved = save_bundle(bundle, output_root=Path(args.output_root), into=args.into, timeout=args.timeout)
        response = {**response, "artifacts": strip_contents(bundle)}
    summary = dict(response)
    if saved is not None:
        summary["saved_to"] = str(saved)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        brief = {key: summary.get(key) for key in ("status", "stage", "next_action", "violations", "saved_to")}
        brief["full_response"] = str(out.resolve())
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if response.get("status") in FAILURE_STATUSES else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--timeout", type=float, default=900, help="seconds per HTTP request")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("ping", help="check connection and list tools")
    call = commands.add_parser("call", help="call a tool")
    call.add_argument("tool")
    call.add_argument("--args", help="JSON file with the arguments object")
    call.add_argument("--arg", action="append", default=[], metavar="KEY=VALUE", help="string argument")
    call.add_argument("--arg-file", action="append", default=[], metavar="KEY=FILE", help="argument loaded from a JSON file")
    download = commands.add_parser("download", help="save artifacts from a saved full response")
    download.add_argument("--from", dest="source", required=True)
    for sub in (call, download):
        sub.add_argument("--out", help="write the full response (without file contents) here")
        sub.add_argument("--output-root", default=str(PACKAGE_ROOT / "outputs"))
        sub.add_argument("--into", type=Path, help="save artifacts into this existing folder")
    args = parser.parse_args(argv)

    try:
        if args.command == "download":
            response = json.loads(Path(args.source).read_text(encoding="utf-8-sig"))
            bundle = response.get("artifacts") or {}
            if any(entry.get("encoding") != "url" for entry in bundle.get("files", [])):
                raise ArtifactError("Saved responses keep only url entries; call the tool again for inline files")
            return finish(response, args)
        url, token = configuration()
        client = McpClient(url, token, args.timeout)
        info = client.initialize()
        if args.command == "ping":
            tools = client.request("tools/list", {}).get("tools", [])
            print(json.dumps({"status": "ok", "server": info.get("serverInfo"),
                              "tools": sorted(tool.get("name") for tool in tools)}, ensure_ascii=False, indent=2))
            return 0
        return finish(client.call(args.tool, build_arguments(args)), args)
    except ConfigError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except ArtifactError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
