"""Build deterministic, self-contained workbook HTML documents.

The authored template never contains workbook content.  A release injects one
compiled edition, the shared stylesheet, the shared renderer and small binary
assets into a single HTML file so moving the four public outputs cannot break
their appearance.
"""

from __future__ import annotations

import base64
import json
import mimetypes
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = Path(__file__).resolve().parent / "templates"
DEFAULT_SHELL = TEMPLATE_ROOT / "shell.html"
DEFAULT_CSS = TEMPLATE_ROOT / "workbook.css"
DEFAULT_RENDERER = TEMPLATE_ROOT / "renderer.js"
DEFAULT_FOOTER_LOGO = ROOT / "assets" / "yonjogyo-logo-footer.png"


class RenderBuildError(RuntimeError):
    """Raised before browser rendering when the HTML bundle is incomplete."""


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _safe_script_json(value: Any) -> str:
    """Serialize JSON without allowing workbook text to terminate a script."""

    rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (
        rendered.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def prepare_document(
    compiled: dict[str, Any],
    *,
    footer_logo: Path | None = DEFAULT_FOOTER_LOGO,
) -> dict[str, Any]:
    """Return a release-ready copy without mutating the compiled IR."""

    document = deepcopy(compiled)
    edition = str(document.get("edition", ""))
    if edition not in {"student", "answer"}:
        raise RenderBuildError("compiled edition must be student or answer")

    metadata = document.setdefault("metadata", {})
    if footer_logo is not None:
        if not footer_logo.is_file():
            raise RenderBuildError(f"footer logo does not exist: {footer_logo}")
        metadata["footerLogo"] = data_uri(footer_logo)

    if edition == "answer":
        title = metadata.get("answerTitle") or "10단계 워크북 해설"
    else:
        title = metadata.get("studentTitle") or "10단계 워크북"
    metadata["documentTitle"] = str(title)
    metadata["screenTitle"] = str(title)
    return document


def build_html(
    compiled: dict[str, Any],
    *,
    shell_path: Path = DEFAULT_SHELL,
    css_path: Path = DEFAULT_CSS,
    renderer_path: Path = DEFAULT_RENDERER,
    footer_logo: Path | None = DEFAULT_FOOTER_LOGO,
) -> str:
    document = prepare_document(compiled, footer_logo=footer_logo)
    edition = str(document["edition"])
    shell = shell_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    renderer = renderer_path.read_text(encoding="utf-8")

    style_marker = '<link rel="stylesheet" href="./workbook.css" />'
    renderer_marker = '<script src="./renderer.js" defer></script>'
    if shell.count(style_marker) != 1 or shell.count(renderer_marker) != 1:
        raise RenderBuildError("template shell markers are missing or duplicated")

    payload = _safe_script_json(document)
    data_script = (
        '<script data-workbook-payload>\n'
        f'window.WORKBOOK_DATA={payload};\n'
        f'window.WORKBOOK_EDITION={json.dumps(edition)};\n'
        "</script>"
    )
    renderer_script = f'<script data-workbook-renderer>\n{renderer}\n</script>'
    html = shell.replace(style_marker, f'<style data-workbook-style>\n{css}\n</style>')
    html = html.replace(renderer_marker, f"{data_script}\n{renderer_script}")
    html = html.replace(
        'data-workbook-edition="student"',
        f'data-workbook-edition="{edition}"',
        1,
    )

    forbidden = (
        "__DOCUMENT_TITLE__",
        "__SCREEN_TITLE__",
        "__WORKSHEETS__",
        'href="./workbook.css"',
        'src="./renderer.js"',
    )
    leftovers = [value for value in forbidden if value in html]
    if leftovers:
        raise RenderBuildError(f"unresolved release marker(s): {', '.join(leftovers)}")
    return html


def write_html(compiled: dict[str, Any], destination: Path, **kwargs: Any) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_html(compiled, **kwargs), encoding="utf-8")
    return destination

