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
ENGLISH_WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
DIRECT_READING_META_RE = re.compile(r"도입|전개|예시|대조|강조|결론|다시 말해|이 말은|여기서는|(?:^|[\s,.;:!?，、])즉(?:[\s,.;:!?，、]|$)")
TEXT_TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]")


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


def text_value(value: Any) -> str:
    return "" if value is None else str(value)


def plain_text(value: Any) -> str:
    text = re.sub(r"<[^>]+>", "", text_value(value))
    return html.unescape(text).strip()


def normalized_text(value: Any) -> str:
    return re.sub(r"\s+", " ", plain_text(value)).strip()


def split_outside_tags(value: Any) -> list[str]:
    parts: list[str] = []
    current = ""
    in_tag = False
    for char in text_value(value):
        if char == "<":
            in_tag = True
            current += char
        elif char == ">":
            in_tag = False
            current += char
        elif char == "/" and not in_tag:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts


def english_word_count(value: Any) -> int:
    return len(ENGLISH_WORD_RE.findall(normalized_text(value)))


def is_empty_or_punctuation_only(value: Any) -> bool:
    return not TEXT_TOKEN_RE.search(normalized_text(value))


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def step_label(step: dict[str, Any]) -> str:
    return " ".join(text_value(step.get(key)).strip() for key in ("no", "title", "part") if text_value(step.get(key)).strip())


def part_range(part: Any) -> tuple[int, int] | None:
    match = re.match(r"^(\d+)\s*-\s*(\d+)$", text_value(part).strip())
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2))
    return (start, end) if start <= end else None


def validate_part_numbering(errors: list[str], sheet: dict[str, Any], sheet_index: int, step: dict[str, Any]) -> None:
    parsed_range = part_range(step.get("part"))
    if not parsed_range:
        return
    start, end = parsed_range
    if step.get("mode") == "meaning":
        entries = list_value(step.get("units")) or list_value(step.get("items"))
    else:
        entries = list_value(step.get("items"))
    expected_count = end - start + 1
    label = f"{text_value(sheet.get('no') or sheet_index + 1)} {step_label(step)}"
    if len(entries) != expected_count:
        errors.append(f"{label}: part 범위는 {expected_count}문항인데 실제 문항은 {len(entries)}개입니다")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        expected_no = start + index
        try:
            actual_no = int(text_value(entry.get("no")))
        except ValueError:
            actual_no = None
        if actual_no != expected_no:
            errors.append(f"{label}: {index + 1}번째 문항 no는 {expected_no}이어야 합니다")


def validate_meaning_step(errors: list[str], sheet: dict[str, Any], sheet_index: int, step: dict[str, Any]) -> None:
    units = list_value(step.get("units")) or list_value(step.get("items"))
    sheet_no = text_value(sheet.get("no") or sheet_index + 1)
    if not units:
        errors.append(f"{sheet_no} {step_label(step)}: 직독직해 unit이 없습니다")
        return

    for unit_index, unit in enumerate(units):
        if not isinstance(unit, dict):
            errors.append(f"{sheet_no} {step_label(step)} {unit_index + 1}번: unit은 객체여야 합니다")
            continue
        unit_no = text_value(unit.get("no") or unit_index + 1)
        label = f"{sheet_no} {step_label(step)} {unit_no}번"
        en_text = normalized_text(unit.get("en"))
        hint_text = normalized_text(unit.get("hint"))
        if not en_text or not hint_text:
            errors.append(f"{label}: en과 hint를 모두 입력해야 합니다")
            continue

        en_parts = [normalized_text(part) for part in split_outside_tags(unit.get("en"))]
        hint_parts = [normalized_text(part) for part in split_outside_tags(unit.get("hint"))]
        if len(en_parts) != len(hint_parts):
            errors.append(f"{label}: en 의미 단위 {len(en_parts)}개, hint 의미 단위 {len(hint_parts)}개")

        for part_index, part in enumerate(en_parts, start=1):
            if is_empty_or_punctuation_only(part):
                errors.append(f"{label}: en {part_index}번째 의미 단위가 비어 있거나 문장부호만 있습니다")
            if english_word_count(part) > 16:
                errors.append(f"{label}: en {part_index}번째 의미 단위가 너무 깁니다. 주어/동사/목적어·보어/부사구 단위로 더 끊으세요")

        for part_index, part in enumerate(hint_parts, start=1):
            if is_empty_or_punctuation_only(part):
                errors.append(f"{label}: hint {part_index}번째 의미 단위가 비어 있거나 문장부호만 있습니다")

        if english_word_count(unit.get("en")) >= 8 and len(en_parts) < 2:
            errors.append(f"{label}: 긴 영어 문장을 1개 의미 단위로 두었습니다. 직독직해 단위로 나누세요")
        if re.search(r"[A-Za-z]", hint_text):
            errors.append(f"{label}: hint에 영어 알파벳이 남아 있습니다. 한국어 뜻이나 한글 음차로 바꾸세요")
        if DIRECT_READING_META_RE.search(hint_text):
            errors.append(f"{label}: hint에 해설용 메타 표현이 있습니다. 원문 의미 대응만 남기세요")


def validate_worksheets(worksheets: list[dict[str, Any]], label: str) -> None:
    errors: list[str] = []
    for sheet_index, sheet in enumerate(worksheets):
        if not isinstance(sheet, dict):
            errors.append(f"{label} {sheet_index + 1}: worksheet는 객체여야 합니다")
            continue
        for step in list_value(sheet.get("steps")):
            if not isinstance(step, dict):
                continue
            validate_part_numbering(errors, sheet, sheet_index, step)
            if step.get("mode") == "meaning":
                validate_meaning_step(errors, sheet, sheet_index, step)
    if errors:
        detail = "\n".join(f"- {error}" for error in errors)
        raise SystemExit(f"{label} 직독직해 데이터 검토 오류:\n{detail}")


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

    student_worksheets = load_worksheets(args.student_json)
    validate_worksheets(student_worksheets, "문제")
    answer_worksheets = None
    if args.answer_json:
        answer_worksheets = load_worksheets(args.answer_json)
        validate_worksheets(answer_worksheets, "해설")

    out_dir = unique_path(OUTPUT_ROOT / args.out_name)
    out_dir.mkdir(parents=True, exist_ok=False)

    student_html = render_html(STUDENT_TEMPLATE, student_worksheets, args.student_title, args.student_screen_title)
    student_path = out_dir / "문제.html"
    student_path.write_text(student_html, encoding="utf-8")
    validate_rendered_html(student_path)

    answer_path = None
    if answer_worksheets is not None:
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
