#!/usr/bin/env python3
"""Render workbook HTML/PDF strictly from the locked workbook templates."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STUDENT_TEMPLATE = ROOT / "index.html"
ANSWER_TEMPLATE = ROOT / "answer-template.html"
OUTPUT_ROOT = ROOT / "outputs"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def load_worksheets(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("worksheets"), list):
        data = data["worksheets"]
    elif isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise SystemExit(f"{path} must contain a worksheet object, a worksheet array, or {{\"worksheets\": [...]}}")
    return data


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = path.with_name(f"{path.name}_v{index}")
        if not candidate.exists():
            return candidate
        index += 1


def render_html(template_path: Path, worksheets: list[dict[str, Any]], document_title: str, screen_title: str) -> str:
    html = template_path.read_text(encoding="utf-8")
    rendered = (
        html.replace("__DOCUMENT_TITLE__", document_title)
        .replace("__SCREEN_TITLE__", screen_title)
        .replace("__WORKSHEETS__", json.dumps(worksheets, ensure_ascii=False, indent=8))
        .replace("assets/yonjogyo-logo-footer.png", "../../assets/yonjogyo-logo-footer.png")
    )
    rendered = re.sub(
        r"const previewWorksheets = \[.*?\];\n\n      const worksheets",
        "const previewWorksheets = [];\n\n      const worksheets",
        rendered,
        count=1,
        flags=re.S,
    )
    rendered = rendered.replace(
        f'if (document.title.includes("{document_title}"))',
        "if (false)",
    )
    rendered = rendered.replace(
        f'if (screenTitle && screenTitle.textContent.includes("{screen_title}"))',
        "if (false)",
    )
    leftovers = ["__DOCUMENT_TITLE__", "__SCREEN_TITLE__", "__WORKSHEETS__"]
    remaining = [token for token in leftovers if token in rendered]
    if remaining:
        raise SystemExit(f"Unreplaced template placeholders remain: {', '.join(remaining)}")
    return rendered


def validate_rendered_html(html_path: Path) -> None:
    if not CHROME.exists():
        return
    result = subprocess.run(
        [
            str(CHROME),
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--dump-dom",
            html_path.resolve().as_uri(),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    dom = result.stdout
    if 'data-render-validation="failed"' not in dom:
        return

    main_match = re.search(r'<main\b[^>]*\bid="pages"[^>]*>(.*?)</main>', dom, flags=re.S)
    validation_html = main_match.group(1) if main_match else dom
    errors = [
        html.unescape(re.sub(r"<[^>]+>", "", item)).strip()
        for item in re.findall(r"<li>(.*?)</li>", validation_html, flags=re.S)
    ]
    errors = [error for error in errors if error]
    detail = "\n".join(f"- {error}" for error in errors) if errors else "Rendered HTML reported validation failure."
    raise SystemExit(f"{html_path} rendered validation failed:\n{detail}")


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found: {CHROME}")
    subprocess.run(
        [
            str(CHROME),
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            f"--print-to-pdf={pdf_path}",
            html_path.resolve().as_uri(),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student-json", required=True, type=Path, help="Student workbook worksheet JSON")
    parser.add_argument("--answer-json", type=Path, help="Answer workbook worksheet JSON")
    parser.add_argument("--out-name", required=True, help="Output folder name under Outputs/")
    parser.add_argument("--student-title", default="10단계 워크북")
    parser.add_argument("--student-screen-title", default="10단계 워크북")
    parser.add_argument("--answer-title", default="10단계 워크북 답지")
    parser.add_argument("--answer-screen-title", default="10단계 워크북 답지")
    parser.add_argument("--pdf", action="store_true", help="Also save 문제.pdf and 해설.pdf")
    args = parser.parse_args()

    out_dir = unique_path(OUTPUT_ROOT / args.out_name)
    out_dir.mkdir(parents=True, exist_ok=False)

    student_worksheets = load_worksheets(args.student_json)
    student_html = render_html(STUDENT_TEMPLATE, student_worksheets, args.student_title, args.student_screen_title)
    student_path = out_dir / "문제.html"
    student_path.write_text(student_html, encoding="utf-8")
    validate_rendered_html(student_path)

    answer_path = None
    if args.answer_json:
        answer_worksheets = load_worksheets(args.answer_json)
        answer_html = render_html(ANSWER_TEMPLATE, answer_worksheets, args.answer_title, args.answer_screen_title)
        answer_path = out_dir / "해설.html"
        answer_path.write_text(answer_html, encoding="utf-8")
        validate_rendered_html(answer_path)

    if args.pdf:
        print_pdf(student_path, out_dir / "문제.pdf")
        if answer_path:
            print_pdf(answer_path, out_dir / "해설.pdf")

    print(out_dir)


if __name__ == "__main__":
    main()
