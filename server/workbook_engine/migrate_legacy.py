"""Migrate the current Chocolate builder into the canonical workbook model."""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

from .textops import (
    BLANK_RE,
    CHOICE_RE,
    PAREN_RE,
    normalize_space,
    parse_inline_markup,
    reconstruct_from_tokens,
    split_outside_tags,
    target_from_span,
    targets_from_spans,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEGACY = ROOT / "tmp" / "build_chocolate_reading_json.py"
DEFAULT_OUTPUT = ROOT / "workbooks" / "chocolate" / "content.json"


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("legacy_chocolate_builder", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load legacy builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _meaning_record(sentence_id: str, en_markup: str, ko_markup: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    en_parts = split_outside_tags(en_markup)
    ko_parts = split_outside_tags(ko_markup)
    if len(en_parts) != len(ko_parts):
        raise ValueError(f"{sentence_id}: meaning segment count mismatch")

    segments: list[dict[str, Any]] = []
    predicates: list[dict[str, Any]] = []
    vocabulary: list[dict[str, Any]] = []
    for index, (en_part, ko_part) in enumerate(zip(en_parts, ko_parts), start=1):
        segment_id = f"{sentence_id}-m{index:02d}"
        en_text, en_spans = parse_inline_markup(en_part)
        ko_text, ko_spans = parse_inline_markup(ko_part)
        segments.append({"id": segment_id, "en": en_text, "ko": ko_text})

        en_predicates = [span for span in en_spans if span.kind == "predicate"]
        ko_predicates = [span for span in ko_spans if span.kind == "predicate"]
        predicate_count = max(len(en_predicates), len(ko_predicates))
        for predicate_index in range(predicate_count):
            predicate: dict[str, Any] = {
                "id": f"{segment_id}-p{predicate_index + 1:02d}",
                "segmentId": segment_id,
            }
            if predicate_index < len(en_predicates):
                predicate["en"] = [target_from_span(en_text, en_predicates[predicate_index])]
            if predicate_index < len(ko_predicates):
                predicate["ko"] = [target_from_span(ko_text, ko_predicates[predicate_index])]
            predicates.append(predicate)

        en_vocab = {span.color_slot: span for span in en_spans if span.kind == "vocab"}
        ko_vocab = {span.color_slot: span for span in ko_spans if span.kind == "vocab"}
        if set(en_vocab) != set(ko_vocab):
            raise ValueError(f"{segment_id}: vocab color pairing mismatch {set(en_vocab)} != {set(ko_vocab)}")
        for color_slot in sorted(en_vocab):
            en_span = en_vocab[color_slot]
            ko_span = ko_vocab[color_slot]
            vocabulary.append(
                {
                    "id": f"{segment_id}-v{color_slot}",
                    "segmentId": segment_id,
                    "colorSlot": color_slot,
                    "en": target_from_span(en_text, en_span),
                    "ko": target_from_span(ko_text, ko_span),
                    "meaning": en_span.meaning or ko_span.text,
                }
            )
    return segments, {"predicates": predicates, "vocabulary": vocabulary}


def _blank_exercise(sentence_id: str, language: str, template: str, answers: list[str]) -> dict[str, Any]:
    base_text, spans = reconstruct_from_tokens(template, BLANK_RE, list(answers))
    return {
        "baseText": base_text,
        "targets": targets_from_spans(base_text, spans, f"{sentence_id}-{language}-blank"),
    }


def _verb_exercise(sentence_id: str, template: str, answers: list[str]) -> dict[str, Any]:
    base_text, spans = reconstruct_from_tokens(template, PAREN_RE, list(answers), lambda match: match.group(1))
    targets = targets_from_spans(base_text, spans, f"{sentence_id}-verb")
    for target in targets:
        target["lemma"] = target.get("cue", "")
    return {"baseText": base_text, "targets": targets}


def _choice_exercise(sentence_id: str, template: str, answers: list[str]) -> dict[str, Any]:
    matches = list(CHOICE_RE.finditer(template))
    if len(matches) != len(answers):
        raise ValueError(f"{sentence_id}: choice count mismatch")
    base_text, spans = reconstruct_from_tokens(template, CHOICE_RE, list(answers), lambda _match: "")
    targets = targets_from_spans(base_text, spans, f"{sentence_id}-choice")
    for target, match, answer in zip(targets, matches, answers):
        options = [html.unescape(option.strip()) for option in match.group(1).split("/") if option.strip()]
        if html.unescape(answer) not in options:
            raise ValueError(f"{sentence_id}: choice answer {answer!r} is not in {options!r}")
        target["options"] = options
    return {"baseText": base_text, "targets": targets}


def _writing_bank(value: str) -> list[str]:
    return [html.unescape(item.strip()) for item in value.split(",") if item.strip()]


def _correction_activity(module: ModuleType) -> list[dict[str, Any]]:
    step = module.make_step7(True)
    passage, spans = parse_inline_markup(step["passage"])
    wrong_spans = [span for span in spans if span.kind == "predicate"]
    corrections = step.get("corrections", [])
    if len(wrong_spans) != len(corrections):
        raise ValueError("Correction passage target count mismatch")
    targets: list[dict[str, Any]] = []
    for index, (span, correction) in enumerate(zip(wrong_spans, corrections), start=1):
        targets.append(
            {
                "id": f"correction-01-target-{index:02d}",
                "target": target_from_span(passage, span),
                "incorrect": correction["wrong"],
                "correct": correction["correct"],
            }
        )
    return [{"id": "correction-01", "textOverride": passage, "targets": targets}]


def _paragraph_activity() -> list[dict[str, Any]]:
    blocks = [
        {"id": "C", "sentenceIds": ["s001", "s002", "s003"]},
        {"id": "D", "sentenceIds": [f"s{index:03d}" for index in range(4, 9)]},
        {"id": "A", "sentenceIds": ["s009", "s010", "s011"]},
        {"id": "E", "sentenceIds": [f"s{index:03d}" for index in range(12, 21)]},
        {"id": "B", "sentenceIds": [f"s{index:03d}" for index in range(21, 25)]},
    ]
    return [
        {
            "id": "paragraph-order-01",
            "blocks": blocks,
            "displayOrder": ["A", "B", "C", "D", "E"],
            "answerOrder": ["C", "D", "A", "E", "B"],
        }
    ]


def migrate(legacy_path: Path) -> dict[str, Any]:
    module = _load_module(legacy_path)
    sentence_count = len(module.source_sentences)
    arrays = [
        module.display_sentences,
        module.translations,
        module.meaning_units,
        module.ko_blank_items,
        module.en_blank_items,
        module.verb_items,
        module.choice_items,
        module.arrange_chunks,
        module.composition_banks,
    ]
    if any(len(items) != sentence_count for items in arrays):
        raise ValueError("Legacy sentence arrays do not have equal lengths")

    sentences: list[dict[str, Any]] = []
    for index in range(sentence_count):
        sentence_id = f"s{index + 1:03d}"
        meaning_segments, annotations = _meaning_record(
            sentence_id, module.meaning_units[index][0], module.meaning_units[index][1]
        )
        arrange_chunks = [segment["en"] for segment in meaning_segments]
        record = {
            "id": sentence_id,
            "no": index + 1,
            "source": module.source_sentences[index],
            "display": html.unescape(module.display_sentences[index]),
            "translation": module.translations[index],
            "meaningSegments": meaning_segments,
            "annotations": annotations,
            "exercises": {
                "koBlank": _blank_exercise(
                    sentence_id, "ko", module.ko_blank_items[index][0], module.ko_blank_items[index][1]
                ),
                "enBlank": _blank_exercise(
                    sentence_id, "en", module.en_blank_items[index][0], module.en_blank_items[index][1]
                ),
                "verb": _verb_exercise(sentence_id, module.verb_items[index][0], module.verb_items[index][1]),
                "choice": _choice_exercise(
                    sentence_id, module.choice_items[index][0], module.choice_items[index][1]
                ),
                "arrange": {
                    "chunks": [
                        {"id": f"{sentence_id}-arrange-{chunk_index + 1:02d}", "text": chunk}
                        for chunk_index, chunk in enumerate(arrange_chunks)
                    ],
                    "displayOrder": [
                        f"{sentence_id}-arrange-{chunk_index + 1:02d}"
                        for chunk_index in reversed(range(len(arrange_chunks)))
                    ],
                },
                "writing": {"bank": _writing_bank(module.composition_banks[index])},
            },
        }
        for exercise_name, default_text in {
            "koBlank": record["translation"],
            "enBlank": record["display"] or record["source"],
            "verb": record["display"] or record["source"],
            "choice": record["display"] or record["source"],
        }.items():
            exercise = record["exercises"][exercise_name]
            if exercise.get("baseText") == default_text:
                exercise.pop("baseText", None)
            else:
                exercise["overrideReason"] = "legacy에서 승인된 재표현 문항을 이관함"
        sentences.append(record)

    return {
        "schemaVersion": "1.0.0",
        "specVersion": "1.0.0",
        "contentVersion": "1.0.0",
        "workbookId": "chocolate-reading",
        "metadata": {
            "title": "Chocolate Reading 10단계 워크북",
            "lessonLabel": "Chocolate",
            "kicker": "Middle Reading",
            "grade": "중등",
            "topic": "초콜릿의 기원과 역사, 그리고 현대 초콜릿 산업의 발달",
            "sourceLanguage": "en",
            "targetLanguage": "ko",
        },
        "sourceStatus": {
            "status": "confirmed",
            "sourceType": "text",
            "references": [str(legacy_path.relative_to(ROOT))],
            "sentenceCount": sentence_count,
            "verifiedAt": "2026-07-10T00:00:00+09:00",
            "notes": f"legacy migration SHA-256: {_sha256(legacy_path)}",
        },
        "updateState": {
            "defaultScope": "all",
            "appliedUpdates": [
                {
                    "id": "U-20260710-001",
                    "scope": "all",
                    "fromContentVersion": "0.0.0",
                    "toContentVersion": "1.0.0",
                    "appliedAt": "2026-07-10T00:00:00+09:00",
                    "report": "reports/updates/U-20260710-001.md",
                }
            ],
        },
        "sentences": sentences,
        "passageActivities": {
            "correction": _correction_activity(module),
            "paragraphOrder": _paragraph_activity(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy", type=Path, default=DEFAULT_LEGACY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    canonical = migrate(args.legacy.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(canonical, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
