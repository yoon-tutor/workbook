"""Browser, PDF and representative-image quality gates for workbook releases."""

from __future__ import annotations

import os
import base64
import json
import math
import re
import shutil
import signal
import socket
import struct
import subprocess
import time
import urllib.request
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CHROME_CANDIDATES = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
)
FAILURE_TEXT = (
    "워크북 렌더링 오류",
    "워크북 데이터 검토 오류",
    "워크북 렌더링 검토 오류",
    "페이지 넘침 검토 오류",
)
STRUCTURAL_CLASSES = (
    "page",
    "practice-item",
    "meaning-row",
    "correction-row",
    "correction-target",
    "paragraph-block",
    "solution-slot",
    "answer-target",
)


class QualityGateError(RuntimeError):
    """Raised when a public artifact would be unsafe to publish."""


@dataclass(frozen=True)
class DomAudit:
    edition: str
    page_count: int
    solution_count: int
    class_counts: dict[str, int]
    target_ids: tuple[str, ...]
    structure_digest: str
    html_path: str
    response_box_heights: tuple[tuple[str, float], ...] = ()
    response_line_layouts: tuple[
        tuple[str, tuple[tuple[float, float, float, float], ...]], ...
    ] = ()
    solution_slot_layouts: tuple[
        tuple[str, tuple[float, float, float, float]], ...
    ] = ()


@dataclass(frozen=True)
class PdfAudit:
    page_count: int
    page_sizes: tuple[tuple[float, float], ...]
    text_lengths: tuple[int, ...]
    pdf_path: str


@dataclass
class ReleaseQA:
    student_dom: DomAudit
    answer_dom: DomAudit
    student_pdf: PdfAudit
    answer_pdf: PdfAudit
    images: list[str] = field(default_factory=list)
    contact_sheets: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "passed",
            "dom": {
                "student": {
                    "pages": self.student_dom.page_count,
                    "solutions": self.student_dom.solution_count,
                },
                "answer": {
                    "pages": self.answer_dom.page_count,
                    "solutions": self.answer_dom.solution_count,
                },
                "sharedTargetSlotCount": len(self.student_dom.target_ids),
                "matchedResponseBoxCount": len(self.student_dom.response_box_heights),
                "matchedResponseLineCount": sum(
                    len(lines) for _target_id, lines in self.student_dom.response_line_layouts
                ),
                "matchedSolutionSlotCount": len(self.student_dom.solution_slot_layouts),
            },
            "pdf": {
                "studentPages": self.student_pdf.page_count,
                "answerPages": self.answer_pdf.page_count,
            },
            "visualSamples": list(self.images),
            "contactSheets": list(self.contact_sheets),
        }


class _DomMetricsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.class_counts: Counter[str] = Counter()
        self.target_ids: list[str] = []
        self._inside_pages = False
        self._skip_depth = 0
        self.structure_tokens: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "main" and attributes.get("id") == "pages":
            self._inside_pages = True
        if not self._inside_pages:
            return
        classes = set((attributes.get("class") or "").split())
        self.class_counts.update(classes)
        if self._skip_depth:
            self._skip_depth += 1
            return
        if classes & {"solution-value", "correction-original"}:
            self._skip_depth = 1
            return
        signature_attributes = []
        for key in ("data-page-id", "data-target-id"):
            if attributes.get(key):
                signature_attributes.append(f"{key}={attributes[key]}")
        self.structure_tokens.append(
            "<" + tag + "|" + ".".join(sorted(classes)) + "|" + "|".join(signature_attributes) + ">"
        )
        if "solution-slot" in classes:
            self.target_ids.append(attributes.get("data-target-id") or "")

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth:
            self._skip_depth -= 1
            return
        if self._inside_pages:
            self.structure_tokens.append(f"</{tag}>")
        if tag == "main" and self._inside_pages:
            self._inside_pages = False

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if not self._inside_pages or self._skip_depth:
            return
        normalized = " ".join(data.split())
        if normalized:
            self.structure_tokens.append(f"#text:{normalized}")


class _WebSocket:
    """Minimal RFC 6455 client sufficient for local Chrome DevTools Protocol."""

    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "ws" or not parsed.hostname:
            raise QualityGateError(f"unsupported DevTools websocket URL: {url}")
        port = parsed.port or 80
        self.socket = socket.create_connection((parsed.hostname, port), timeout=5)
        self.buffer = bytearray()
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Origin: http://localhost\r\n\r\n"
        )
        self.socket.sendall(request.encode("ascii"))
        response = self._read_until(b"\r\n\r\n")
        status_line = response.split(b"\r\n", 1)[0]
        if b" 101 " not in status_line:
            self.close()
            raise QualityGateError(
                f"DevTools websocket handshake failed: {status_line.decode(errors='replace')}"
            )

    def _read_until(self, marker: bytes) -> bytes:
        while marker not in self.buffer:
            block = self.socket.recv(4096)
            if not block:
                raise QualityGateError("DevTools websocket closed during handshake")
            self.buffer.extend(block)
        end = self.buffer.index(marker) + len(marker)
        value = bytes(self.buffer[:end])
        del self.buffer[:end]
        return value

    def _read_exact(self, count: int) -> bytes:
        while len(self.buffer) < count:
            block = self.socket.recv(max(4096, count - len(self.buffer)))
            if not block:
                raise QualityGateError("DevTools websocket closed unexpectedly")
            self.buffer.extend(block)
        value = bytes(self.buffer[:count])
        del self.buffer[:count]
        return value

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        first = 0x80 | opcode
        length = len(payload)
        if length < 126:
            header = bytes((first, 0x80 | length))
        elif length < 65536:
            header = bytes((first, 0x80 | 126)) + struct.pack("!H", length)
        else:
            header = bytes((first, 0x80 | 127)) + struct.pack("!Q", length)
        mask = os.urandom(4)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.socket.sendall(header + mask + masked)

    def send_text(self, value: str) -> None:
        self._send_frame(0x1, value.encode("utf-8"))

    def recv_text(self, timeout: float) -> str:
        self.socket.settimeout(timeout)
        fragments = bytearray()
        started = False
        while True:
            first, second = self._read_exact(2)
            final = bool(first & 0x80)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(8))[0]
            mask = self._read_exact(4) if masked else b""
            payload = self._read_exact(length)
            if masked:
                payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
            if opcode == 0x8:
                raise QualityGateError("DevTools websocket closed")
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            if opcode == 0x1:
                fragments = bytearray(payload)
                started = True
            elif opcode == 0x0 and started:
                fragments.extend(payload)
            else:
                continue
            if final:
                return fragments.decode("utf-8")

    def close(self) -> None:
        try:
            self._send_frame(0x8, b"")
        except (OSError, AttributeError):
            pass
        try:
            self.socket.close()
        except (OSError, AttributeError):
            pass


class _CDP:
    def __init__(self, websocket_url: str) -> None:
        self.websocket = _WebSocket(websocket_url)
        self.next_id = 1

    def command(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        timeout: float = 30,
    ) -> dict[str, Any]:
        message_id = self.next_id
        self.next_id += 1
        self.websocket.send_text(
            json.dumps(
                {"id": message_id, "method": method, "params": params or {}},
                separators=(",", ":"),
            )
        )
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            remaining = max(0.1, deadline - time.monotonic())
            try:
                message = json.loads(self.websocket.recv_text(remaining))
            except socket.timeout:
                break
            if message.get("id") != message_id:
                continue
            if "error" in message:
                raise QualityGateError(f"CDP {method} failed: {message['error']}")
            return dict(message.get("result") or {})
        raise QualityGateError(f"CDP {method} timed out")

    def evaluate(self, expression: str) -> Any:
        response = self.command(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
        )
        if response.get("exceptionDetails"):
            raise QualityGateError(f"browser evaluation failed: {response['exceptionDetails']}")
        return (response.get("result") or {}).get("value")

    def close(self) -> None:
        self.websocket.close()


def find_chrome() -> Path:
    override = os.environ.get("CHROME_BIN")
    if override and Path(override).is_file():
        return Path(override)
    for candidate in CHROME_CANDIDATES:
        if candidate.is_file():
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)
    raise QualityGateError("Chrome/Chromium executable was not found")


def _devtools_targets(port: int) -> list[dict[str, Any]]:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1) as response:
        value = json.loads(response.read().decode("utf-8"))
    return [item for item in value if isinstance(item, dict)]


@contextmanager
def _cdp_page(html_path: Path, profile: Path) -> Iterable[_CDP]:
    chrome = find_chrome()
    command = _browser_args(chrome, profile) + [
        "--remote-debugging-port=0",
        "--remote-allow-origins=*",
        html_path.resolve().as_uri(),
    ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    client: _CDP | None = None
    try:
        active_port = profile / "DevToolsActivePort"
        deadline = time.monotonic() + 15
        port: int | None = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise QualityGateError("Chrome exited before DevTools became ready")
            if active_port.is_file():
                try:
                    lines = active_port.read_text(encoding="utf-8").splitlines()
                except OSError:
                    lines = []  # Chrome may still hold the file while writing its port.
                if lines and lines[0].isdigit():
                    port = int(lines[0])
                    break
            time.sleep(0.05)
        if port is None:
            raise QualityGateError("Chrome DevTools port did not become ready")

        targets: list[dict[str, Any]] = []
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            try:
                targets = _devtools_targets(port)
            except (OSError, ValueError):
                targets = []
            if any(item.get("type") == "page" and item.get("webSocketDebuggerUrl") for item in targets):
                break
            time.sleep(0.05)
        target = next(
            (
                item
                for item in targets
                if item.get("type") == "page" and item.get("webSocketDebuggerUrl")
            ),
            None,
        )
        if target is None:
            raise QualityGateError("Chrome did not expose a page DevTools target")
        client = _CDP(str(target["webSocketDebuggerUrl"]))
        client.command("Runtime.enable")
        client.command("Page.enable")
        client.command("Page.navigate", {"url": html_path.resolve().as_uri()})
        yield client
    finally:
        if client is not None:
            client.close()
        if process.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               check=False)
                process.wait(timeout=5)
            else:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=5)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=5)


def _wait_for_render(
    client: _CDP,
    *,
    edition: str,
    expected_pages: int,
    timeout: float = 45,
) -> dict[str, Any]:
    expression = """
      (() => {
        const root = document.documentElement;
        const pages = document.querySelectorAll('#pages > .page').length;
        const panel = document.querySelector('#pages .validation-panel');
        const values = Array.from(document.querySelectorAll('#pages .solution-value'));
        const wrong = Array.from(document.querySelectorAll('#pages .correction-original'));
        const correctionTargets = Array.from(document.querySelectorAll('#pages .correction-target'));
        const workNodes = Array.from(document.querySelectorAll('#pages .work-area, #pages .work-area *'));
        return {
          state: root ? (root.dataset.renderValidation || '') : '',
          pages,
          panel: panel ? panel.innerText : '',
          solutions: values.length,
          badSolutionColors: values.filter(
            node => getComputedStyle(node).color !== 'rgb(215, 25, 32)'
          ).length,
          badCorrectionColors: wrong.filter(
            node => getComputedStyle(node).color === 'rgb(215, 25, 32)'
          ).length,
          correctionTargets: correctionTargets.length,
          badCorrectionUnderlines: correctionTargets.filter(
            node => !getComputedStyle(node).textDecorationLine.includes('underline')
          ).length,
          badCorrectionTargetColors: correctionTargets.filter(
            node => getComputedStyle(node).color === 'rgb(215, 25, 32)'
          ).length,
          unauthorizedRed: workNodes.filter(node => {
            const style = getComputedStyle(node);
            return style.color === 'rgb(215, 25, 32)'
              && !node.closest('.solution-value')
              && node.textContent.trim().length > 0
              && style.display !== 'none'
              && style.visibility !== 'hidden';
          }).length
        };
      })()
    """
    deadline = time.monotonic() + timeout
    last: dict[str, Any] = {}
    while time.monotonic() < deadline:
        value = client.evaluate(expression)
        if isinstance(value, dict):
            last = value
        state = str(last.get("state", ""))
        if state == "failed":
            raise QualityGateError(
                f"{edition}: browser render failed: {last.get('panel') or 'no failure detail'}"
            )
        if state == "ok":
            if int(last.get("pages", -1)) != expected_pages:
                raise QualityGateError(
                    f"{edition}: expected {expected_pages} pages, found {last.get('pages')}"
                )
            solutions = int(last.get("solutions", 0))
            if edition == "student" and solutions:
                raise QualityGateError(f"student browser render leaked {solutions} answers")
            if edition == "answer" and solutions < 1:
                raise QualityGateError("answer browser render has no answer values")
            if int(last.get("badSolutionColors", 0)):
                raise QualityGateError(f"{edition}: a solution value is not point red")
            if int(last.get("badCorrectionColors", 0)):
                raise QualityGateError("answer correction source text is incorrectly red")
            if int(last.get("correctionTargets", 0)) < 1:
                raise QualityGateError(f"{edition}: correction targets are not visibly marked")
            if int(last.get("badCorrectionUnderlines", 0)):
                raise QualityGateError(f"{edition}: a correction target is not underlined")
            if int(last.get("badCorrectionTargetColors", 0)):
                raise QualityGateError(f"{edition}: a correction prompt is incorrectly red")
            if int(last.get("unauthorizedRed", 0)):
                raise QualityGateError(
                    f"{edition}: point red appears on non-solution work text"
                )
            return last
        time.sleep(0.1)
    raise QualityGateError(f"{edition}: browser render stayed pending for {timeout:.0f}s")


def _browser_args(chrome: Path, profile: Path) -> list[str]:
    shutil.rmtree(profile, ignore_errors=True)
    profile.mkdir(parents=True, exist_ok=True)
    return [
        str(chrome),
        "--headless=new",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-sync",
        "--metrics-recording-only",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        "--window-size=1280,1600",
        f"--user-data-dir={profile.resolve()}",
    ]


def _stream_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _run(
    command: list[str],
    *,
    timeout: int = 90,
    accept_chrome_hang: bool = False,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode
    except subprocess.TimeoutExpired as error:
        if not accept_chrome_hang:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
            raise QualityGateError(f"browser command timed out after {timeout}s") from error
        partial_stdout = _stream_text(error.stdout)
        partial_stderr = _stream_text(error.stderr)
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate(timeout=5)
        stdout = _stream_text(stdout) or partial_stdout
        stderr = _stream_text(stderr) or partial_stderr
        return_code = 0
    result = subprocess.CompletedProcess(command, return_code, stdout, stderr)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()[-4000:]
        raise QualityGateError(f"browser command failed ({result.returncode}): {detail}")
    return result


def snapshot_dom(
    html_path: Path,
    *,
    edition: str,
    expected_pages: int,
    profile_root: Path,
) -> tuple[str, DomAudit]:
    with _cdp_page(html_path, profile_root / f"dom-{edition}") as client:
        _wait_for_render(client, edition=edition, expected_pages=expected_pages)
        response_box_heights = _response_box_heights(client)
        response_line_layouts = _response_line_layouts(client, edition=edition)
        solution_slot_layouts = _solution_slot_layouts(client)
        dom = str(client.evaluate("document.documentElement.outerHTML") or "")
    if not dom.strip():
        raise QualityGateError(f"{edition}: browser returned an empty DOM")
    html_tag = re.search(r"<html\b[^>]*>", dom, flags=re.IGNORECASE)
    if not html_tag or not re.search(
        r'data-render-validation=["\']ok["\']', html_tag.group(0), flags=re.IGNORECASE
    ):
        details = " / ".join(value for value in FAILURE_TEXT if value in dom)
        raise QualityGateError(f"{edition}: rendered DOM did not reach validation=ok{': ' + details if details else ''}")
    page_match = re.search(
        r'data-render-page-count=["\'](\d+)["\']', html_tag.group(0), flags=re.IGNORECASE
    )
    if not page_match or int(page_match.group(1)) != expected_pages:
        raise QualityGateError(f"{edition}: expected {expected_pages} rendered pages")
    parser = _DomMetricsParser()
    parser.feed(dom)
    page_count = parser.class_counts["page"]
    solutions = parser.class_counts["solution-value"]
    if page_count != expected_pages:
        raise QualityGateError(f"{edition}: expected {expected_pages} .page nodes, found {page_count}")
    if edition == "student" and solutions:
        raise QualityGateError(f"student DOM leaked {solutions} solution values")
    if edition == "answer" and not solutions:
        raise QualityGateError("answer DOM contains no solution values")
    if any(not value for value in parser.target_ids):
        raise QualityGateError(f"{edition}: an empty solution target id was rendered")
    if len(parser.target_ids) != len(set(parser.target_ids)):
        raise QualityGateError(f"{edition}: duplicate solution target ids were rendered")

    audit = DomAudit(
        edition=edition,
        page_count=page_count,
        solution_count=solutions,
        class_counts={key: parser.class_counts[key] for key in STRUCTURAL_CLASSES},
        target_ids=tuple(parser.target_ids),
        structure_digest=sha256("\n".join(parser.structure_tokens).encode("utf-8")).hexdigest(),
        html_path=str(html_path),
        response_box_heights=tuple(sorted(response_box_heights.items())),
        response_line_layouts=tuple(sorted(response_line_layouts.items())),
        solution_slot_layouts=tuple(sorted(solution_slot_layouts.items())),
    )
    return dom, audit


def _response_box_heights(client: _CDP) -> dict[str, float]:
    expression = """
      (() => {
        const result = {};
        const duplicates = [];
        document.querySelectorAll('#pages .write-box').forEach(box => {
          const slot = box.querySelector('.block-solution.solution-slot[data-target-id]');
          if (!slot) return;
          const targetId = slot.dataset.targetId || '';
          if (!targetId || Object.prototype.hasOwnProperty.call(result, targetId)) {
            duplicates.push(targetId);
            return;
          }
          result[targetId] = box.getBoundingClientRect().height;
        });
        return { result, duplicates };
      })()
    """
    measured = client.evaluate(expression)
    if not isinstance(measured, dict) or not isinstance(measured.get("result"), dict):
        raise QualityGateError("response layout measurement returned invalid data")
    duplicates = [str(value) for value in measured.get("duplicates", []) if str(value)]
    if duplicates:
        raise QualityGateError(
            f"response layout contains duplicate target(s): {', '.join(duplicates)}"
        )
    heights = {str(key): float(value) for key, value in measured["result"].items()}
    invalid = [key for key, value in heights.items() if not math.isfinite(value) or value <= 0]
    if invalid:
        raise QualityGateError(
            f"response layout contains invalid height(s): {', '.join(invalid)}"
        )
    return heights


def _response_line_layouts(
    client: _CDP,
    *,
    edition: str,
) -> dict[str, tuple[tuple[float, float, float, float], ...]]:
    if edition not in {"student", "answer"}:
        raise QualityGateError(f"unsupported response layout edition: {edition}")
    expression = f"""
      (() => {{
        const edition = {json.dumps(edition)};
        const result = {{}};
        document.querySelectorAll('#pages .write-box').forEach(box => {{
          const slot = box.querySelector('.block-solution.solution-slot[data-target-id]');
          if (!slot) return;
          const targetId = slot.dataset.targetId || '';
          const boxRect = box.getBoundingClientRect();
          let rects = [];
          if (edition === 'answer') {{
            const value = slot.querySelector(':scope > .solution-value');
            if (!value) return;
            const range = document.createRange();
            range.selectNodeContents(value);
            rects = Array.from(range.getClientRects());
          }} else {{
            const trace = box.querySelector(`.response-trace[data-target-id="${{CSS.escape(targetId)}}"]`);
            if (!trace) return;
            rects = Array.from(trace.querySelectorAll('.response-trace-line'))
              .map(node => node.getBoundingClientRect());
          }}
          result[targetId] = rects
            .filter(rect => rect.width > 0 && rect.height > 0)
            .map(rect => [
              rect.left - boxRect.left,
              rect.top - boxRect.top,
              rect.width,
              rect.height
            ]);
        }});
        return result;
      }})()
    """
    measured = client.evaluate(expression)
    if not isinstance(measured, dict):
        raise QualityGateError(f"{edition}: response line layout measurement returned invalid data")
    result: dict[str, tuple[tuple[float, float, float, float], ...]] = {}
    for target_id, lines in measured.items():
        if not isinstance(lines, list) or not lines:
            raise QualityGateError(f"{edition}: response target {target_id} has no line geometry")
        normalized: list[tuple[float, float, float, float]] = []
        for line in lines:
            if not isinstance(line, list) or len(line) != 4:
                raise QualityGateError(f"{edition}: response target {target_id} has invalid line geometry")
            values = tuple(float(value) for value in line)
            if any(not math.isfinite(value) for value in values) or values[2] <= 0 or values[3] <= 0:
                raise QualityGateError(f"{edition}: response target {target_id} has invalid line geometry")
            normalized.append(values)
        result[str(target_id)] = tuple(normalized)
    return result


def _solution_slot_layouts(
    client: _CDP,
) -> dict[str, tuple[float, float, float, float]]:
    """Measure all visible, non-writing solution slots relative to their page."""

    expression = """
      (() => {
        const result = {};
        const duplicates = [];
        document.querySelectorAll(
          '#pages .solution-slot[data-target-id]:not(.block-solution)'
        ).forEach(slot => {
          const targetId = slot.dataset.targetId || '';
          const page = slot.closest('.page');
          const rect = slot.getBoundingClientRect();
          const pageRect = page ? page.getBoundingClientRect() : null;
          if (!targetId || !pageRect || Object.prototype.hasOwnProperty.call(result, targetId)) {
            duplicates.push(targetId);
            return;
          }
          if (rect.width <= 0 || rect.height <= 0) return;
          result[targetId] = [
            rect.left - pageRect.left,
            rect.top - pageRect.top,
            rect.width,
            rect.height
          ];
        });
        return { result, duplicates };
      })()
    """
    measured = client.evaluate(expression)
    if not isinstance(measured, dict) or not isinstance(measured.get("result"), dict):
        raise QualityGateError("solution-slot layout measurement returned invalid data")
    duplicates = [str(value) for value in measured.get("duplicates", []) if str(value)]
    if duplicates:
        raise QualityGateError(
            f"solution-slot layout contains duplicate target(s): {', '.join(duplicates)}"
        )
    result: dict[str, tuple[float, float, float, float]] = {}
    for target_id, layout in measured["result"].items():
        if not isinstance(layout, list) or len(layout) != 4:
            raise QualityGateError(f"solution-slot {target_id} has invalid geometry")
        values = tuple(float(value) for value in layout)
        if any(not math.isfinite(value) for value in values) or values[2] <= 0 or values[3] <= 0:
            raise QualityGateError(f"solution-slot {target_id} has invalid geometry")
        result[str(target_id)] = values
    return result


def measure_answer_layouts(
    html_path: Path,
    *,
    expected_pages: int,
    profile_root: Path,
) -> dict[str, dict[str, Any]]:
    """Measure writing responses and every other answer slot in one browser pass."""

    with _cdp_page(html_path, profile_root / "layout-answer") as client:
        _wait_for_render(client, edition="answer", expected_pages=expected_pages)
        heights = _response_box_heights(client)
        lines = _response_line_layouts(client, edition="answer")
        slots = _solution_slot_layouts(client)
    if not heights:
        raise QualityGateError("answer response layout contains no measurable writing boxes")
    if heights.keys() != lines.keys():
        raise QualityGateError("answer response box and line targets differ")
    if not slots:
        raise QualityGateError("answer contains no measurable non-writing solution slots")
    return {
        "responses": {
            target_id: {
                "boxHeightPx": height,
                "lines": [
                    {
                        "leftPx": left,
                        "topPx": top,
                        "widthPx": width,
                        "heightPx": line_height,
                    }
                    for left, top, width, line_height in lines[target_id]
                ],
            }
            for target_id, height in heights.items()
        },
        "solutionSlots": {
            target_id: {"widthPx": layout[2], "heightPx": layout[3]}
            for target_id, layout in slots.items()
        },
    }


def measure_response_box_layouts(
    html_path: Path,
    *,
    expected_pages: int,
    profile_root: Path,
) -> dict[str, dict[str, Any]]:
    """Measure each answer line's exact browser geometry before student projection."""

    return measure_answer_layouts(
        html_path,
        expected_pages=expected_pages,
        profile_root=profile_root,
    )["responses"]


def measure_response_box_heights(
    html_path: Path,
    *,
    expected_pages: int,
    profile_root: Path,
) -> dict[str, float]:
    """Compatibility view of answer-first layouts containing only box heights."""

    layouts = measure_response_box_layouts(
        html_path,
        expected_pages=expected_pages,
        profile_root=profile_root,
    )
    return {target_id: float(layout["boxHeightPx"]) for target_id, layout in layouts.items()}


def require_shared_structure(student: DomAudit, answer: DomAudit) -> None:
    if student.page_count != answer.page_count:
        raise QualityGateError("student and answer page counts differ")
    if student.class_counts != answer.class_counts:
        raise QualityGateError(
            f"student and answer structural counts differ: {student.class_counts} != {answer.class_counts}"
        )
    if student.target_ids != answer.target_ids:
        raise QualityGateError("student and answer solution-slot order differs")
    if student.structure_digest != answer.structure_digest:
        raise QualityGateError("student and answer normalized problem DOM differs")
    student_heights = dict(student.response_box_heights)
    answer_heights = dict(answer.response_box_heights)
    if student_heights.keys() != answer_heights.keys():
        raise QualityGateError("student and answer response-box targets differ")
    mismatched = [
        target_id
        for target_id in student_heights
        if abs(student_heights[target_id] - answer_heights[target_id]) > 0.75
    ]
    if mismatched:
        raise QualityGateError(
            "student and answer response-box heights differ: " + ", ".join(mismatched)
        )
    student_lines = dict(student.response_line_layouts)
    answer_lines = dict(answer.response_line_layouts)
    if student_lines.keys() != answer_lines.keys():
        raise QualityGateError("student and answer response-line targets differ")
    geometry_mismatches: list[str] = []
    for target_id in student_lines:
        if len(student_lines[target_id]) != len(answer_lines[target_id]):
            geometry_mismatches.append(target_id)
            continue
        if any(
            any(abs(student_value - answer_value) > 0.75 for student_value, answer_value in zip(student_line, answer_line))
            for student_line, answer_line in zip(student_lines[target_id], answer_lines[target_id])
        ):
            geometry_mismatches.append(target_id)
    if geometry_mismatches:
        raise QualityGateError(
            "student and answer response-line geometry differs: "
            + ", ".join(geometry_mismatches)
        )
    student_slots = dict(student.solution_slot_layouts)
    answer_slots = dict(answer.solution_slot_layouts)
    if student_slots.keys() != answer_slots.keys():
        raise QualityGateError("student and answer non-writing solution-slot targets differ")
    slot_mismatches = [
        target_id
        for target_id in student_slots
        if any(
            abs(student_value - answer_value) > 0.75
            for student_value, answer_value in zip(student_slots[target_id], answer_slots[target_id])
        )
    ]
    if slot_mismatches:
        raise QualityGateError(
            "student and answer solution-slot geometry differs: "
            + ", ".join(slot_mismatches)
        )


def print_pdf(
    html_path: Path, pdf_path: Path, *, profile_root: Path, edition: str, expected_pages: int
) -> Path:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        pdf_path.unlink()
    with _cdp_page(html_path, profile_root / f"pdf-{edition}") as client:
        _wait_for_render(client, edition=edition, expected_pages=expected_pages)
        state = client.evaluate(
            "Number((window.WORKBOOK_DATA && window.WORKBOOK_DATA.pages || []).length)"
        )
        if int(state or 0) != expected_pages:
            raise QualityGateError(f"{edition}: compiled page count differs from prepared pages")
        result = client.command(
            "Page.printToPDF",
            {
                "landscape": False,
                "displayHeaderFooter": False,
                "printBackground": True,
                "preferCSSPageSize": True,
                "marginTop": 0,
                "marginBottom": 0,
                "marginLeft": 0,
                "marginRight": 0,
            },
            timeout=90,
        )
        encoded = result.get("data")
        if not isinstance(encoded, str) or not encoded:
            raise QualityGateError(f"{edition}: CDP returned no PDF data")
        pdf_path.write_bytes(base64.b64decode(encoded))
    if not pdf_path.is_file() or pdf_path.stat().st_size < 10_000:
        raise QualityGateError(f"{edition}: Chrome did not create a usable PDF")
    return pdf_path


def inspect_pdf(pdf_path: Path, *, expected_pages: int) -> PdfAudit:
    try:
        import fitz  # type: ignore
    except ImportError as error:  # pragma: no cover - environment gate
        raise QualityGateError("PyMuPDF is required for PDF verification") from error

    document = fitz.open(pdf_path)
    try:
        if document.page_count != expected_pages:
            raise QualityGateError(
                f"{pdf_path.name}: expected {expected_pages} pages, found {document.page_count}"
            )
        sizes: list[tuple[float, float]] = []
        lengths: list[int] = []
        for index in range(document.page_count):
            page = document.load_page(index)
            width, height = float(page.rect.width), float(page.rect.height)
            sizes.append((round(width, 2), round(height, 2)))
            if not (590 <= width <= 600 and 837 <= height <= 847):
                raise QualityGateError(
                    f"{pdf_path.name} page {index + 1}: expected A4, found {width:.1f}×{height:.1f} pt"
                )
            extracted = page.get_text("text").strip()
            lengths.append(len(extracted))
            if len(extracted) < 40:
                raise QualityGateError(f"{pdf_path.name} page {index + 1}: page appears blank")
            for marker in FAILURE_TEXT:
                if marker in extracted:
                    raise QualityGateError(
                        f"{pdf_path.name} page {index + 1}: failure marker in PDF: {marker}"
                    )
        return PdfAudit(
            page_count=document.page_count,
            page_sizes=tuple(sizes),
            text_lengths=tuple(lengths),
            pdf_path=str(pdf_path),
        )
    finally:
        document.close()


def representative_indices(pages: list[dict[str, Any]]) -> list[int]:
    if not pages:
        return []
    stage_first: dict[str, int] = {}
    for index, page in enumerate(pages):
        stage_first.setdefault(str(page.get("no", "")), index)
    candidates = {
        0,
        min(1, len(pages) - 1),
        len(pages) // 2,
        len(pages) - 1,
    }
    for stage in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
        if stage in stage_first:
            candidates.add(stage_first[stage])
    return sorted(candidates)


def render_pdf_samples(
    pdf_path: Path,
    *,
    output_dir: Path,
    edition: str,
    page_indices: Iterable[int],
    scale: float = 1.25,
) -> tuple[list[Path], Path]:
    try:
        import fitz  # type: ignore
        from PIL import Image, ImageDraw  # type: ignore
    except ImportError as error:  # pragma: no cover - environment gate
        raise QualityGateError("PyMuPDF and Pillow are required for visual samples") from error

    output_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(pdf_path)
    images: list[Path] = []
    try:
        for page_index in page_indices:
            if page_index < 0 or page_index >= document.page_count:
                continue
            pixmap = document.load_page(page_index).get_pixmap(
                matrix=fitz.Matrix(scale, scale), alpha=False
            )
            destination = output_dir / f"{edition}-p{page_index + 1:02d}.png"
            pixmap.save(destination)
            images.append(destination)
    finally:
        document.close()
    if not images:
        raise QualityGateError(f"{edition}: no representative PDF pages were rendered")

    opened = [Image.open(path).convert("RGB") for path in images]
    try:
        thumb_width = 360
        label_height = 28
        thumbs: list[Any] = []
        for page_number, source in zip(page_indices, opened):
            height = round(source.height * thumb_width / source.width)
            thumb = source.resize((thumb_width, height))
            canvas = Image.new("RGB", (thumb_width, height + label_height), "white")
            canvas.paste(thumb, (0, label_height))
            ImageDraw.Draw(canvas).text((8, 7), f"{edition} · page {page_number + 1}", fill="black")
            thumbs.append(canvas)
        columns = 3
        rows = (len(thumbs) + columns - 1) // columns
        cell_width = max(image.width for image in thumbs)
        cell_height = max(image.height for image in thumbs)
        contact = Image.new("RGB", (cell_width * columns, cell_height * rows), "#dddddd")
        for index, thumb in enumerate(thumbs):
            x = (index % columns) * cell_width
            y = (index // columns) * cell_height
            contact.paste(thumb, (x, y))
        contact_path = output_dir / f"{edition}-contact-sheet.png"
        contact.save(contact_path, optimize=True)
    finally:
        for source in opened:
            source.close()
    return images, contact_path


def run_release_qa(
    *,
    student_html: Path,
    answer_html: Path,
    student_pdf: Path,
    answer_pdf: Path,
    pages: list[dict[str, Any]],
    qa_root: Path,
) -> ReleaseQA:
    expected_pages = len(pages)
    profiles = qa_root / "chrome-profiles"
    _student_dom_text, student_dom = snapshot_dom(
        student_html,
        edition="student",
        expected_pages=expected_pages,
        profile_root=profiles,
    )
    _answer_dom_text, answer_dom = snapshot_dom(
        answer_html,
        edition="answer",
        expected_pages=expected_pages,
        profile_root=profiles,
    )
    require_shared_structure(student_dom, answer_dom)

    print_pdf(student_html, student_pdf, profile_root=profiles, edition="student", expected_pages=expected_pages)
    print_pdf(answer_html, answer_pdf, profile_root=profiles, edition="answer", expected_pages=expected_pages)
    student_pdf_audit = inspect_pdf(student_pdf, expected_pages=expected_pages)
    answer_pdf_audit = inspect_pdf(answer_pdf, expected_pages=expected_pages)

    indices = representative_indices(pages)
    student_images, student_contact = render_pdf_samples(
        student_pdf,
        output_dir=qa_root / "samples",
        edition="student",
        page_indices=indices,
    )
    answer_images, answer_contact = render_pdf_samples(
        answer_pdf,
        output_dir=qa_root / "samples",
        edition="answer",
        page_indices=indices,
    )
    return ReleaseQA(
        student_dom=student_dom,
        answer_dom=answer_dom,
        student_pdf=student_pdf_audit,
        answer_pdf=answer_pdf_audit,
        images=[str(path) for path in student_images + answer_images],
        contact_sheets=[str(student_contact), str(answer_contact)],
    )
