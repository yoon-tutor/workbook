"""Compile canonical workbook content into shared student/answer page IR."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path
from typing import Any, Callable

from .paginator import paginate_stage
from .textops import render_annotated_text, render_targets
from .validator import load_spec, require_valid, validate_canonical, validate_compiled


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "config" / "workbook-spec.json"


STAGE_DEFS: dict[str, dict[str, Any]] = {
    "1": {"title": "지문 연습하기", "mode": "meaning"},
    "2": {"title": "빈칸 완성하기 (우리말)", "mode": "parallel"},
    "3": {"title": "빈칸 완성하기 (영문)", "mode": "parallel"},
    "4": {"title": "해석 연습하기", "mode": "writing"},
    "5": {"title": "동사형 연습하기", "mode": "parallel"},
    "6": {"title": "어법·어휘 고르기", "mode": "parallel"},
    "7": {"title": "어색한 곳 찾기", "mode": "correction"},
    "8": {"title": "순서 배열하기", "mode": "writing"},
    "9": {"title": "문단 배열하기", "mode": "paragraph-order"},
    "10": {"title": "영작 연습하기", "mode": "writing"},
}


def _stage_definition(spec: dict[str, Any], stage_no: str) -> dict[str, Any]:
    result = dict(STAGE_DEFS[stage_no])
    result["no"] = stage_no
    stages = (spec.get("logicalStages") or spec.get("stages") or []) if isinstance(spec, dict) else []
    for stage in stages:
        if str(stage.get("number", stage.get("no"))) == stage_no:
            result.update({key: value for key, value in stage.items() if key not in {"items", "units"}})
            break
    result["title"] = str(result.get("title") or STAGE_DEFS[stage_no]["title"])
    result["mode"] = str(
        result.get("rendererMode") or result.get("mode") or STAGE_DEFS[stage_no]["mode"]
    )
    return result


def _stage(spec: dict[str, Any], stage_no: str, edition: str) -> dict[str, Any]:
    stage = _stage_definition(spec, stage_no)
    stage["instruction"] = str(stage.get("instruction", ""))
    return stage


def _literal(value: str) -> str:
    return html.escape(value)


def _blank_target(item: dict[str, Any]) -> str:
    target_id = html.escape(str(item["id"]), quote=True)
    return f'<span class="blank answer-target" data-target-id="{target_id}"></span>'


def _verb_target(item: dict[str, Any]) -> str:
    target_id = html.escape(str(item["id"]), quote=True)
    cue = html.escape(str(item.get("cue", item.get("lemma", ""))))
    return f'<span class="verb-target answer-target" data-target-id="{target_id}">({cue})</span>'


def _choice_target(item: dict[str, Any]) -> str:
    target_id = html.escape(str(item["id"]), quote=True)
    options = " / ".join(html.escape(str(option)) for option in item.get("options", []))
    return f'<span class="choice-target answer-target" data-target-id="{target_id}">[{options}]</span>'


def _solutions(targets: list[dict[str, Any]]) -> dict[str, str]:
    return {str(item["id"]): str(item["target"]["text"]) for item in targets}


def _exercise_base(sentence: dict[str, Any], name: str) -> str:
    exercise = sentence["exercises"][name]
    if exercise.get("baseText"):
        return str(exercise["baseText"])
    if name == "koBlank":
        return str(sentence["translation"])
    return str(sentence.get("display") or sentence["source"])


def _render_exercise(
    sentence: dict[str, Any],
    name: str,
    renderer: Callable[[dict[str, Any]], str],
) -> tuple[str, dict[str, str]]:
    exercise = sentence["exercises"][name]
    targets = list(exercise.get("targets", []))
    return render_targets(_exercise_base(sentence, name), targets, renderer), _solutions(targets)


def _meaning_item(sentence: dict[str, Any]) -> dict[str, Any]:
    predicates = sentence.get("annotations", {}).get("predicates", [])
    vocabulary = sentence.get("annotations", {}).get("vocabulary", [])
    en_parts: list[str] = []
    ko_parts: list[str] = []
    for segment in sentence.get("meaningSegments", []):
        segment_id = str(segment["id"])
        segment_predicates = [item for item in predicates if str(item.get("segmentId")) == segment_id]
        segment_vocabulary = [item for item in vocabulary if str(item.get("segmentId")) == segment_id]
        en_parts.append(render_annotated_text(segment["en"], segment_predicates, segment_vocabulary, "en"))
        ko_parts.append(render_annotated_text(segment["ko"], segment_predicates, segment_vocabulary, "ko"))
    return {"no": sentence["no"], "en": " / ".join(en_parts), "hint": " / ".join(ko_parts), "solutions": {}}


def _parallel_item(sentence: dict[str, Any], name: str, blank_language: str) -> dict[str, Any]:
    exercise = sentence["exercises"][name]
    rendered, solutions = _render_exercise(sentence, name, _blank_target)
    if blank_language == "ko":
        return {"no": sentence["no"], "en": _literal(sentence.get("display") or sentence["source"]), "ko": rendered, "solutions": solutions}
    return {"no": sentence["no"], "ko": _literal(sentence["translation"]), "en": rendered, "solutions": solutions}


def _verb_item(sentence: dict[str, Any]) -> dict[str, Any]:
    rendered, solutions = _render_exercise(sentence, "verb", _verb_target)
    return {"no": sentence["no"], "ko": _literal(sentence["translation"]), "en": rendered, "solutions": solutions}


def _choice_item(sentence: dict[str, Any]) -> dict[str, Any]:
    rendered, solutions = _render_exercise(sentence, "choice", _choice_target)
    return {"no": sentence["no"], "ko": _literal(sentence["translation"]), "en": rendered, "solutions": solutions}


def _translation_item(sentence: dict[str, Any]) -> dict[str, Any]:
    target_id = f"{sentence['id']}-translation"
    return {
        "no": sentence["no"],
        "en": _literal(sentence.get("display") or sentence["source"]),
        "lines": 2,
        "answerHeight": "14mm",
        "responseTargetId": target_id,
        "solutions": {target_id: sentence["translation"]},
        "solutionText": sentence["translation"],
    }


def _arrange_item(sentence: dict[str, Any]) -> dict[str, Any]:
    arrange = sentence["exercises"]["arrange"]
    chunks = {str(item["id"]): str(item["text"]) for item in arrange["chunks"]}
    display_chunks: list[str] = []
    for item_id in arrange.get("displayOrder", []):
        display_chunks.append(chunks[str(item_id)])
    target_id = f"{sentence['id']}-arrange-response"
    solution = sentence.get("display") or sentence["source"]
    return {
        "no": sentence["no"],
        "ko": _literal(sentence["translation"]),
        "bank": " / ".join(_literal(value) for value in display_chunks),
        "lines": 2,
        "answerHeight": "14mm",
        "responseTargetId": target_id,
        "solutions": {target_id: solution},
        "solutionText": solution,
    }


def _writing_item(sentence: dict[str, Any]) -> dict[str, Any]:
    target_id = f"{sentence['id']}-writing"
    return {
        "no": sentence["no"],
        "ko": _literal(sentence["translation"]),
        "bank": ", ".join(_literal(str(value)) for value in sentence["exercises"]["writing"]["bank"]),
        "lines": 2,
        "answerHeight": "14mm",
        "responseTargetId": target_id,
        "solutions": {target_id: sentence.get("display") or sentence["source"]},
        "solutionText": sentence.get("display") or sentence["source"],
    }


def _correction_stages(canonical: dict[str, Any], spec: dict[str, Any], edition: str) -> list[dict[str, Any]]:
    activities = canonical.get("passageActivities", {}).get("correction", [])
    stages: list[dict[str, Any]] = []
    for activity in activities:
        stage = _stage(spec, "7", edition)
        stage["activityId"] = str(activity.get("id", ""))
        text = str(activity.get("textOverride", ""))
        targets = list(activity.get("targets", []))
        rendered = render_targets(
            text,
            targets,
            lambda item: (
                f'<span class="correction-target" data-target-id="{html.escape(str(item["id"]), quote=True)}">'
                f'{html.escape(str(item["incorrect"]))}</span>'
            ),
        )
        stage["passage"] = rendered
        stage["rows"] = [{"no": index + 1} for index in range(len(targets))]
        stage["corrections"] = [
            {
                "no": index + 1,
                "wrong": str(item["incorrect"]),
                "correct": str(item["correct"]),
                "targetId": str(item["id"]),
            }
            for index, item in enumerate(targets)
        ]
        stages.append(stage)
    return stages


def _paragraph_stages(canonical: dict[str, Any], spec: dict[str, Any], edition: str) -> list[dict[str, Any]]:
    activities = canonical.get("passageActivities", {}).get("paragraphOrder", [])
    sentence_map = {str(sentence["id"]): sentence for sentence in canonical["sentences"]}
    stages: list[dict[str, Any]] = []
    for activity in activities:
        stage = _stage(spec, "9", edition)
        stage["activityId"] = str(activity.get("id", ""))
        block_map = {str(block["id"]): block for block in activity["blocks"]}
        blocks: list[dict[str, str]] = []
        for block_id in activity["displayOrder"]:
            sentence_ids = block_map[str(block_id)]["sentenceIds"]
            text = " ".join(sentence_map[str(sentence_id)]["source"] for sentence_id in sentence_ids)
            blocks.append({"label": f"({block_id})", "text": _literal(text)})
        stage["blocks"] = blocks
        stage["sequenceSlots"] = len(blocks)
        stage["sequenceAnswer"] = list(activity["answerOrder"])
        stages.append(stage)
    return stages


def _student_projection(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projected = json.loads(json.dumps(pages, ensure_ascii=False))
    for page in projected:
        for collection_key in ("items", "units"):
            for item in page.get(collection_key, []):
                item["solutions"] = {}
                item.pop("solutionText", None)
        page.pop("corrections", None)
        page.pop("sequenceAnswer", None)
    return projected


def project_student_workbook(
    answer_document: dict[str, Any],
    *,
    expected_sentences: int | None = None,
) -> dict[str, Any]:
    """Remove solutions from an answer document without changing its layout IR."""

    if answer_document.get("edition") != "answer":
        raise ValueError("student projection requires an answer edition document")
    projected = json.loads(json.dumps(answer_document, ensure_ascii=False))
    projected["edition"] = "student"
    projected["pages"] = _student_projection(list(projected.get("pages", [])))
    if expected_sentences is not None:
        require_valid(validate_compiled(projected, expected_sentences))
    return projected


def lock_response_layout(
    answer_document: dict[str, Any],
    response_layouts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Bake measured answer text geometry into the shared answer-first layout."""

    if answer_document.get("edition") != "answer":
        raise ValueError("response layout can only be locked from the answer edition")
    locked = json.loads(json.dumps(answer_document, ensure_ascii=False))
    expected: set[str] = set()
    for page in locked.get("pages", []):
        if page.get("mode") != "writing":
            continue
        for item in page.get("items", []):
            target_id = str(
                item.get("responseTargetId")
                or item.get("solutionTargetId")
                or item.get("answerTargetId")
                or ""
            )
            if not target_id:
                continue
            expected.add(target_id)
            measured = response_layouts.get(target_id)
            if not isinstance(measured, dict):
                raise ValueError(f"missing measured response height for {target_id}")
            box_height = measured.get("boxHeightPx")
            lines = measured.get("lines")
            if (
                box_height is None
                or not math.isfinite(float(box_height))
                or float(box_height) <= 0
                or not isinstance(lines, list)
                or not lines
            ):
                raise ValueError(f"invalid measured response layout for {target_id}")
            normalized_lines: list[dict[str, float]] = []
            for line in lines:
                if not isinstance(line, dict):
                    raise ValueError(f"invalid measured response line for {target_id}")
                normalized = {
                    key: round(float(line.get(key, 0)), 2)
                    for key in ("leftPx", "topPx", "widthPx", "heightPx")
                }
                if any(not math.isfinite(value) for value in normalized.values()):
                    raise ValueError(f"invalid measured response line for {target_id}")
                if normalized["widthPx"] <= 0 or normalized["heightPx"] <= 0:
                    raise ValueError(f"empty measured response line for {target_id}")
                normalized_lines.append(normalized)
            item["responseLayout"] = {
                "boxHeightPx": math.ceil(float(box_height)),
                "lines": normalized_lines,
            }
            item["answerHeight"] = f"{math.ceil(float(box_height))}px"
            item["keepAnswerHeight"] = True
    unexpected = sorted(set(response_layouts) - expected)
    if unexpected:
        raise ValueError(f"measured unknown response target(s): {', '.join(unexpected)}")
    return locked


def lock_solution_slot_layouts(
    answer_document: dict[str, Any],
    solution_layouts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Lock every non-writing answer slot to its browser-measured box size.

    The student edition is projected from this locked answer document. Removing
    solution values therefore cannot collapse inline cloze blanks or reflow the
    text that follows them.
    """

    if answer_document.get("edition") != "answer":
        raise ValueError("solution-slot layout can only be locked from the answer edition")
    if not solution_layouts:
        raise ValueError("answer solution-slot layout is empty")

    normalized: dict[str, dict[str, float]] = {}
    for target_id, layout in solution_layouts.items():
        if not target_id or not isinstance(layout, dict):
            raise ValueError("invalid measured solution-slot target")
        values = {
            key: round(float(layout.get(key, 0)), 2)
            for key in ("widthPx", "heightPx")
        }
        if any(not math.isfinite(value) or value <= 0 for value in values.values()):
            raise ValueError(f"invalid measured solution-slot layout for {target_id}")
        normalized[str(target_id)] = {
            "widthPx": math.ceil(values["widthPx"]),
            "heightPx": math.ceil(values["heightPx"]),
        }

    locked = json.loads(json.dumps(answer_document, ensure_ascii=False))
    locked["solutionSlotLayouts"] = dict(sorted(normalized.items()))
    return locked


def _compile_answer_workbook(
    canonical: dict[str, Any],
    spec: dict[str, Any],
) -> dict[str, Any]:
    sentences = list(canonical["sentences"])
    logical: list[tuple[dict[str, Any], str | None]] = []

    stage1 = _stage(spec, "1", "answer")
    stage1["units"] = [_meaning_item(sentence) for sentence in sentences]
    logical.append((stage1, "units"))

    stage2 = _stage(spec, "2", "answer")
    stage2.update({"fields": [{"key": "en", "className": "english"}, {"key": "ko", "className": "korean"}], "items": [_parallel_item(sentence, "koBlank", "ko") for sentence in sentences]})
    logical.append((stage2, "items"))

    stage3 = _stage(spec, "3", "answer")
    stage3.update({"fields": [{"key": "ko", "className": "korean"}, {"key": "en", "className": "english"}], "items": [_parallel_item(sentence, "enBlank", "en") for sentence in sentences]})
    logical.append((stage3, "items"))

    stage4 = _stage(spec, "4", "answer")
    stage4["items"] = [_translation_item(sentence) for sentence in sentences]
    logical.append((stage4, "items"))

    stage5 = _stage(spec, "5", "answer")
    stage5.update({"fields": [{"key": "ko", "className": "korean"}, {"key": "en", "className": "english"}], "items": [_verb_item(sentence) for sentence in sentences]})
    logical.append((stage5, "items"))

    stage6 = _stage(spec, "6", "answer")
    stage6.update({"fields": [{"key": "ko", "className": "korean"}, {"key": "en", "className": "english"}], "items": [_choice_item(sentence) for sentence in sentences]})
    logical.append((stage6, "items"))

    logical.extend((stage, None) for stage in _correction_stages(canonical, spec, "answer"))

    stage8 = _stage(spec, "8", "answer")
    stage8["items"] = [_arrange_item(sentence) for sentence in sentences]
    logical.append((stage8, "items"))

    logical.extend((stage, None) for stage in _paragraph_stages(canonical, spec, "answer"))

    stage10 = _stage(spec, "10", "answer")
    stage10["items"] = [_writing_item(sentence) for sentence in sentences]
    logical.append((stage10, "items"))

    pages: list[dict[str, Any]] = []
    for stage, collection_key in logical:
        if collection_key:
            pages.extend(paginate_stage(stage, spec, collection_key))
        else:
            pages.append(stage)

    for page_index, page in enumerate(pages, start=1):
        page["stageId"] = str(page.get("id", f"stage-{page.get('no', '')}"))
        page["pageId"] = f"{canonical['workbookId']}-p{page_index:02d}"
        page["pageNo"] = page_index

    source_metadata = dict(canonical.get("metadata", {}))
    student_title = str(
        source_metadata.get("title")
        or source_metadata.get("studentTitle")
        or "10단계 워크북"
    )
    metadata = {
        **source_metadata,
        "no": source_metadata.get("lessonLabel") or source_metadata.get("no") or "",
        "studentTitle": student_title,
        "answerTitle": source_metadata.get("answerTitle") or f"{student_title} 답지",
    }
    document = {
        "workbookId": canonical["workbookId"],
        "edition": "answer",
        "schemaVersion": canonical["schemaVersion"],
        "specVersion": canonical["specVersion"],
        "contentVersion": canonical["contentVersion"],
        "metadata": metadata,
        "pages": pages,
    }
    require_valid(validate_compiled(document, len(sentences)))
    return document


def compile_workbook(canonical: dict[str, Any], edition: str, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    if edition not in {"student", "answer"}:
        raise ValueError("edition must be student or answer")
    spec = spec or load_spec(DEFAULT_SPEC)
    require_valid(validate_canonical(canonical, spec))
    answer = _compile_answer_workbook(canonical, spec)
    if edition == "answer":
        return answer
    return project_student_workbook(answer, expected_sentences=len(canonical["sentences"]))


def compile_file(canonical_path: Path, edition: str, output_path: Path, spec_path: Path | None = None) -> Path:
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    spec = load_spec(spec_path or DEFAULT_SPEC)
    compiled = compile_workbook(canonical, edition, spec)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(compiled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path
