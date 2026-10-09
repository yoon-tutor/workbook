#!/usr/bin/env python3
"""사용자별 배포 zip을 만든다: client/의 git 기준 파일 + manifest.json + 사용자 .env.

  python server/scripts/build_release.py --user <이름> --key-file <키 파일> [--url <MCP URL>]

키 파일은 키 한 줄만 있거나 MCP_API_TOKEN=... 줄이 있는 파일이다. 키를 출력하지 않는다.
URL을 생략하면 server/deploy-state.json의 운영 URL을 쓴다. 결과: releases/<service>-<version>-<user>.zip
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_client import audit  # noqa: E402
from standard_tools import CLIENT_DIR, REPO_ROOT, SERVER, git_visible_files, load_service, read_env, version  # noqa: E402


def read_key(path: Path) -> str:
    """Accept a bare key, MCP_API_TOKEN=..., or an issued-key note such as ``api_key: tm_...``."""
    values = read_env(path)
    text = values.get("MCP_API_TOKEN") or path.read_text(encoding="utf-8-sig")
    keys = set(re.findall(r"\btm_[A-Za-z0-9_-]{16,}", text))
    if len(keys) != 1:
        raise SystemExit("키 파일에서 tm_ API 키를 정확히 하나 찾지 못했다.")
    return keys.pop()


def main() -> int:
    config = load_service()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--user", required=True)
    parser.add_argument("--key-file", type=Path, required=True)
    parser.add_argument("--url")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9가-힣_-]{1,40}", args.user):
        parser.error("--user는 영문·숫자·한글·_-만 쓴다")

    url = args.url
    if not url:
        state = json.loads((SERVER / "deploy-state.json").read_text(encoding="utf-8"))
        url = state["url"].rstrip("/") + "/mcp"
    if not url.startswith("https://"):
        parser.error("MCP URL은 HTTPS여야 한다")
    key = read_key(args.key_file)

    files = git_visible_files(CLIENT_DIR)
    errors = audit(CLIENT_DIR, files)
    if errors:
        print("\n".join(errors))
        return 1

    service, release = config["service"], version()
    manifest = {
        "service": service,
        "version": release,
        "files": {path.as_posix(): hashlib.sha256((CLIENT_DIR / path).read_bytes()).hexdigest() for path in files},
    }
    output = REPO_ROOT / "releases" / f"{service}-{release}-{args.user}.zip"
    if output.exists():
        print(f"중단: {output}가 이미 있다. VERSION을 올리거나 기존 파일을 옮긴다.")
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        partial = Path(directory) / output.name
        with zipfile.ZipFile(partial, "x", zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                bundle.write(CLIENT_DIR / path, f"{service}/{path.as_posix()}")
            bundle.writestr(f"{service}/manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
            bundle.writestr(f"{service}/.env", f"MCP_URL={url}\nMCP_API_TOKEN={key}\n")
            for folder in ("inputs/", "outputs/"):
                if not any(path.as_posix().startswith(folder) for path in files):
                    bundle.writestr(f"{service}/{folder}", b"")
        partial.replace(output)
    print(f"{output} 생성 ({len(files)}개 파일, 버전 {release}). .env에 키가 들어 있으니 해당 사용자에게만 전달한다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
