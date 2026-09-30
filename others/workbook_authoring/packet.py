"""Compact, deterministic authoring packets for new workbook passages.

The packet removes only mechanical identifiers and target wrappers. Translation,
meaning segmentation, annotations, exercise choices, distractors, corrections,
paragraph grouping, and writing cues remain authored values. Expanding a packet
must therefore never invent or rewrite semantic content.
"""

from __future__ import annotations

import copy
import json
import math
import string
from pathlib import Path
from typing import Any

from workbook_engine.schema_gate import validate_schema
from workbook_engine.validator import load_spec, require_valid, validate_canonical


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SCHEMA = ROOT / "schemas" / "canonical-workbook.schema.json"


class AuthoringPacketError(ValueError):
    """Raised when a packet would require a semantic guess to expand."""


def verify_new_packet_policy(packet: dict[str, Any]) -> None:
    """Check editorial stage-9 rules for newly authored packets only.

    Legacy canonical validation and compact/expand parity remain unchanged.
    Block list order determines the printed A, B, C labels; answerOrder is the
    source-order solution, so it must be checked separately.
    """

    activities = packet.get("passageActivities", {}).get("paragraphOrder", [])
    answers_by_size: dict[int, list[tuple[int, ...]]] = {}
    for index, activity in enumerate(activities, start=1):
        path = f"passageActivities.paragraphOrder[{index - 1}]"
        blocks = activity.get("blocks", [])
        if not isinstance(blocks, list) or len(blocks) < 2:
            raise AuthoringPacketError(f"{path}.blocks: at least two blocks are required")
        expected = list(range(1, len(blocks) + 1))
        if activity.get("displayOrder") != expected:
            raise AuthoringPacketError(
                f"{path}.displayOrder: new questions must print labels in A, B, C order; "
                "put shuffled source blocks in blocks and use [1, 2, 3]"
            )
        answer = activity.get("answerOrder")
        if not isinstance(answer, list) or sorted(answer) != expected:
            raise AuthoringPacketError(f"{path}.answerOrder: expected a permutation of block numbers")
        if answer == expected:
            raise AuthoringPacketError(
                f"{path}.answerOrder: an already ordered A-B-C choice is not a meaningful arrangement"
            )
        if activity.get("fixedIntroSentenceIds") or activity.get("fixedOutroSentenceIds"):
            raise AuthoringPacketError(
                f"{path}: new stage-9 questions must put the entire passage in blocks"
            )
        answers_by_size.setdefault(len(blocks), []).append(tuple(answer))

    for block_count, answers in answers_by_size.items():
        # A set should use every available non-identity permutation before repeating one.
        required_distinct = min(len(answers), math.factorial(block_count) - 1)
        if len(set(answers)) < required_distinct:
            raise AuthoringPacketError(
                "passageActivities.paragraphOrder: vary answerOrder across the question set"
            )


def _sentence_id(index: int) -> str:
    return f"s{index:03d}"


def _meaning_id(sentence_id: str, index: int) -> str:
    return f"{sentence_id}-m{index:02d}"


def _letter(index: int, *, upper: bool = False) -> str:
    alphabet = string.ascii_uppercase if upper else string.ascii_lowercase
    if index < 1 or index > len(alphabet):
        raise AuthoringPacketError("authoring packets support at most 26 chunks or blocks")
    return alphabet[index - 1]


def _count_occurrences(text: str, needle: str) -> int:
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        found = text.find(needle, start)
        if found < 0:
            return count
        count += 1
        start = found + len(needle)


def _compact_target(target: dict[str, Any]) -> str | dict[str, Any]:
    text = str(target["text"])
    occurrence = int(target.get("occurrence", 1))
    if occurrence == 1:
        return text
    return {"text": text, "occurrence": occurrence}


def _expand_target(value: Any, *, base_text: str, path: str) -> dict[str, Any]:
    if isinstance(value, str):
        count = _count_occurrences(base_text, value)
        if count != 1:
            raise AuthoringPacketError(
                f"{path}: shorthand target must occur exactly once; found {count}. "
                "Use {\"text\": ..., \"occurrence\": N} when the authored target repeats."
            )
        return {"text": value, "occurrence": 1}
    if not isinstance(value, dict):
        raise AuthoringPacketError(f"{path}: target must be a string or target object")
    unknown = sorted(set(value) - {"text", "occurrence"})
    if unknown:
        raise AuthoringPacketError(f"{path}: unknown target fields: {unknown}")
    text = str(value.get("text", ""))
    occurrence = value.get("occurrence")
    if not text or not isinstance(occurrence, int) or occurrence < 1:
        raise AuthoringPacketError(f"{path}: repeated target requires text and positive occurrence")
    if _count_occurrences(base_text, text) < occurrence:
        raise AuthoringPacketError(f"{path}: occurrence {occurrence} does not resolve")
    return {"text": text, "occurrence": occurrence}


def _compact_target_list(values: list[dict[str, Any]]) -> list[Any]:
    return [_compact_target(value) for value in values]


def _expand_target_list(values: Any, *, base_text: str, path: str) -> list[dict[str, Any]]:
    if not isinstance(values, list) or not values:
        raise AuthoringPacketError(f"{path}: at least one target is required")
    return [
        _expand_target(value, base_text=base_text, path=f"{path}[{index}]")
        for index, value in enumerate(values)
    ]


def compact_canonical(canonical: dict[str, Any]) -> dict[str, Any]:
    """Remove mechanical data while preserving every authored semantic choice."""

    packet = copy.deepcopy(canonical)
    sentence_id_to_no = {
        str(sentence["id"]): int(sentence["no"])
        for sentence in canonical.get("sentences", [])
    }
    for sentence_index, sentence in enumerate(packet.get("sentences", []), start=1):
        expected_sentence_id = _sentence_id(sentence_index)
        if sentence.get("id") != expected_sentence_id or sentence.get("no") != sentence_index:
            raise AuthoringPacketError("canonical sentence IDs and numbers are not deterministic")
        sentence.pop("id")
        sentence.pop("no")

        segment_ids: dict[str, int] = {}
        for segment_index, segment in enumerate(sentence.get("meaningSegments", []), start=1):
            expected_segment_id = _meaning_id(expected_sentence_id, segment_index)
            if segment.get("id") != expected_segment_id:
                raise AuthoringPacketError(f"{expected_sentence_id}: meaning segment IDs are not deterministic")
            segment_ids[expected_segment_id] = segment_index
            segment.pop("id")

        predicate_counts: dict[int, int] = {}
        for predicate in sentence.get("annotations", {}).get("predicates", []):
            segment_no = segment_ids.get(str(predicate.pop("segmentId", "")))
            if segment_no is None:
                raise AuthoringPacketError(f"{expected_sentence_id}: predicate segment does not resolve")
            predicate_counts[segment_no] = predicate_counts.get(segment_no, 0) + 1
            expected_id = f"{_meaning_id(expected_sentence_id, segment_no)}-p{predicate_counts[segment_no]:02d}"
            if predicate.pop("id", None) != expected_id:
                raise AuthoringPacketError(f"{expected_sentence_id}: predicate IDs are not deterministic")
            predicate["segment"] = segment_no
            for language in ("en", "ko"):
                if language in predicate:
                    predicate[language] = _compact_target_list(predicate[language])

        for vocabulary_index, vocabulary in enumerate(
            sentence.get("annotations", {}).get("vocabulary", []), start=1
        ):
            segment_no = segment_ids.get(str(vocabulary.pop("segmentId", "")))
            if segment_no is None:
                raise AuthoringPacketError(f"{expected_sentence_id}: vocabulary segment does not resolve")
            expected_id = f"{_meaning_id(expected_sentence_id, segment_no)}-v{vocabulary_index:02d}"
            if vocabulary.pop("id", None) != expected_id:
                raise AuthoringPacketError(f"{expected_sentence_id}: vocabulary IDs are not deterministic")
            if vocabulary.pop("colorSlot", None) != vocabulary_index:
                raise AuthoringPacketError(f"{expected_sentence_id}: vocabulary color slots are not deterministic")
            vocabulary["segment"] = segment_no
            vocabulary["en"] = _compact_target(vocabulary["en"])
            vocabulary["ko"] = _compact_target(vocabulary["ko"])

        exercises = sentence.get("exercises", {})
        for exercise_name, short_name in (("koBlank", "ko"), ("enBlank", "en")):
            targets = exercises[exercise_name]["targets"]
            compacted: list[Any] = []
            for target_index, target in enumerate(targets, start=1):
                expected_id = f"{expected_sentence_id}-{short_name}-{target_index:02d}"
                if target.pop("id", None) != expected_id:
                    raise AuthoringPacketError(f"{expected_sentence_id}: {exercise_name} IDs are not deterministic")
                compacted.append(_compact_target(target["target"]))
            exercises[exercise_name]["targets"] = compacted

        for exercise_name in ("verb", "choice"):
            compacted_targets: list[dict[str, Any]] = []
            for target_index, target in enumerate(exercises[exercise_name]["targets"], start=1):
                expected_id = f"{expected_sentence_id}-{exercise_name}-{target_index:02d}"
                if target.pop("id", None) != expected_id:
                    raise AuthoringPacketError(f"{expected_sentence_id}: {exercise_name} IDs are not deterministic")
                target["target"] = _compact_target(target["target"])
                compacted_targets.append(target)
            exercises[exercise_name]["targets"] = compacted_targets

        arrange = exercises["arrange"]
        chunk_id_to_no: dict[str, int] = {}
        compacted_chunks: list[str] = []
        for chunk_index, chunk in enumerate(arrange["chunks"], start=1):
            expected_id = f"{expected_sentence_id}-{_letter(chunk_index)}"
            if chunk.get("id") != expected_id:
                raise AuthoringPacketError(f"{expected_sentence_id}: arrange chunk IDs are not deterministic")
            chunk_id_to_no[expected_id] = chunk_index
            compacted_chunks.append(str(chunk["text"]))
        arrange["chunks"] = compacted_chunks
        try:
            arrange["displayOrder"] = [chunk_id_to_no[str(value)] for value in arrange["displayOrder"]]
        except KeyError as error:
            raise AuthoringPacketError(f"{expected_sentence_id}: arrange order does not resolve") from error

    activities = packet.get("passageActivities", {})
    for activity_index, activity in enumerate(activities.get("correction", []), start=1):
        expected_activity_id = f"correction-{activity_index:02d}"
        if activity.pop("id", None) != expected_activity_id:
            raise AuthoringPacketError("correction activity IDs are not deterministic")
        for target_index, target in enumerate(activity.get("targets", []), start=1):
            expected_target_id = f"{expected_activity_id}-{target_index:02d}"
            if target.pop("id", None) != expected_target_id:
                raise AuthoringPacketError("correction target IDs are not deterministic")
            target["target"] = _compact_target(target["target"])

    for activity_index, activity in enumerate(activities.get("paragraphOrder", []), start=1):
        expected_activity_id = f"paragraph-order-{activity_index:02d}"
        if activity.pop("id", None) != expected_activity_id:
            raise AuthoringPacketError("paragraph-order activity IDs are not deterministic")
        block_id_to_no: dict[str, int] = {}
        compacted_blocks: list[list[int]] = []
        for block_index, block in enumerate(activity.get("blocks", []), start=1):
            expected_block_id = _letter(block_index, upper=True)
            if block.get("id") != expected_block_id:
                raise AuthoringPacketError("paragraph block IDs are not deterministic")
            block_id_to_no[expected_block_id] = block_index
            try:
                compacted_blocks.append([sentence_id_to_no[str(value)] for value in block["sentenceIds"]])
            except KeyError as error:
                raise AuthoringPacketError("paragraph sentence reference does not resolve") from error
        activity["blocks"] = compacted_blocks
        for key in ("displayOrder", "answerOrder"):
            try:
                activity[key] = [block_id_to_no[str(value)] for value in activity[key]]
            except KeyError as error:
                raise AuthoringPacketError(f"paragraph {key} does not resolve") from error
    return packet


def _exercise_base(sentence: dict[str, Any], name: str) -> str:
    exercise = sentence["exercises"][name]
    if exercise.get("baseText"):
        return str(exercise["baseText"])
    if name == "koBlank":
        return str(sentence["translation"])
    return str(sentence.get("display") or sentence["source"])


def expand_packet(packet: dict[str, Any], *, validate: bool = True) -> dict[str, Any]:
    """Expand mechanical fields and optionally run the full canonical validators."""

    canonical = copy.deepcopy(packet)
    sentences = canonical.get("sentences")
    if not isinstance(sentences, list) or not sentences:
        raise AuthoringPacketError("sentences must be a non-empty array")
    canonical.setdefault("$schema", "../../schemas/canonical-workbook.schema.json")
    source_status = canonical.setdefault("sourceStatus", {})
    source_status["sentenceCount"] = len(sentences)

    for sentence_index, sentence in enumerate(sentences, start=1):
        sentence_id = _sentence_id(sentence_index)
        sentence["id"] = sentence_id
        sentence["no"] = sentence_index
        segments = sentence.get("meaningSegments")
        if not isinstance(segments, list) or not segments:
            raise AuthoringPacketError(f"{sentence_id}: meaningSegments must be non-empty")
        for segment_index, segment in enumerate(segments, start=1):
            segment["id"] = _meaning_id(sentence_id, segment_index)

        predicate_counts: dict[int, int] = {}
        for predicate_index, predicate in enumerate(
            sentence.get("annotations", {}).get("predicates", []), start=1
        ):
            segment_no = predicate.pop("segment", None)
            if not isinstance(segment_no, int) or not 1 <= segment_no <= len(segments):
                raise AuthoringPacketError(f"{sentence_id}.predicates[{predicate_index}]: invalid segment")
            predicate_counts[segment_no] = predicate_counts.get(segment_no, 0) + 1
            segment_id = _meaning_id(sentence_id, segment_no)
            predicate["id"] = f"{segment_id}-p{predicate_counts[segment_no]:02d}"
            predicate["segmentId"] = segment_id
            segment = segments[segment_no - 1]
            for language in ("en", "ko"):
                if language in predicate:
                    predicate[language] = _expand_target_list(
                        predicate[language],
                        base_text=str(segment[language]),
                        path=f"{sentence_id}.predicates[{predicate_index}].{language}",
                    )

        for vocabulary_index, vocabulary in enumerate(
            sentence.get("annotations", {}).get("vocabulary", []), start=1
        ):
            segment_no = vocabulary.pop("segment", None)
            if not isinstance(segment_no, int) or not 1 <= segment_no <= len(segments):
                raise AuthoringPacketError(f"{sentence_id}.vocabulary[{vocabulary_index}]: invalid segment")
            segment_id = _meaning_id(sentence_id, segment_no)
            vocabulary["id"] = f"{segment_id}-v{vocabulary_index:02d}"
            vocabulary["segmentId"] = segment_id
            vocabulary["colorSlot"] = vocabulary_index
            segment = segments[segment_no - 1]
            vocabulary["en"] = _expand_target(
                vocabulary["en"],
                base_text=str(segment["en"]),
                path=f"{sentence_id}.vocabulary[{vocabulary_index}].en",
            )
            vocabulary["ko"] = _expand_target(
                vocabulary["ko"],
                base_text=str(segment["ko"]),
                path=f"{sentence_id}.vocabulary[{vocabulary_index}].ko",
            )

        exercises = sentence.get("exercises", {})
        for name, short_name in (("koBlank", "ko"), ("enBlank", "en")):
            exercise = exercises.get(name, {})
            base_text = _exercise_base(sentence, name)
            exercise["targets"] = [
                {
                    "id": f"{sentence_id}-{short_name}-{target_index:02d}",
                    "target": _expand_target(
                        value,
                        base_text=base_text,
                        path=f"{sentence_id}.{name}[{target_index}]",
                    ),
                }
                for target_index, value in enumerate(exercise.get("targets", []), start=1)
            ]

        for name in ("verb", "choice"):
            exercise = exercises.get(name, {})
            base_text = _exercise_base(sentence, name)
            expanded_targets: list[dict[str, Any]] = []
            for target_index, authored in enumerate(exercise.get("targets", []), start=1):
                if not isinstance(authored, dict):
                    raise AuthoringPacketError(f"{sentence_id}.{name}[{target_index}]: object required")
                authored["id"] = f"{sentence_id}-{name}-{target_index:02d}"
                authored["target"] = _expand_target(
                    authored.get("target"),
                    base_text=base_text,
                    path=f"{sentence_id}.{name}[{target_index}].target",
                )
                expanded_targets.append(authored)
            exercise["targets"] = expanded_targets

        arrange = exercises.get("arrange", {})
        compacted_chunks = arrange.get("chunks", [])
        if not isinstance(compacted_chunks, list) or len(compacted_chunks) < 2:
            raise AuthoringPacketError(f"{sentence_id}.arrange: at least two chunks are required")
        arrange["chunks"] = [
            {"id": f"{sentence_id}-{_letter(index)}", "text": str(text)}
            for index, text in enumerate(compacted_chunks, start=1)
        ]
        chunk_count = len(compacted_chunks)
        display_order = arrange.get("displayOrder")
        if sorted(display_order or []) != list(range(1, chunk_count + 1)):
            raise AuthoringPacketError(f"{sentence_id}.arrange.displayOrder must be a 1-based permutation")
        arrange["displayOrder"] = [f"{sentence_id}-{_letter(int(value))}" for value in display_order]

    activities = canonical.get("passageActivities", {})
    for activity_index, activity in enumerate(activities.get("correction", []), start=1):
        activity_id = f"correction-{activity_index:02d}"
        activity["id"] = activity_id
        base_text = str(activity.get("textOverride", ""))
        for target_index, target in enumerate(activity.get("targets", []), start=1):
            if not isinstance(target, dict):
                raise AuthoringPacketError(f"{activity_id}.targets[{target_index}]: object required")
            target["id"] = f"{activity_id}-{target_index:02d}"
            target["target"] = _expand_target(
                target.get("target"),
                base_text=base_text,
                path=f"{activity_id}.targets[{target_index}].target",
            )

    for activity_index, activity in enumerate(activities.get("paragraphOrder", []), start=1):
        activity_id = f"paragraph-order-{activity_index:02d}"
        activity["id"] = activity_id
        blocks = activity.get("blocks", [])
        if not isinstance(blocks, list) or not blocks:
            raise AuthoringPacketError(f"{activity_id}: blocks must be non-empty")
        activity["blocks"] = [
            {
                "id": _letter(block_index, upper=True),
                "sentenceIds": [_sentence_id(int(value)) for value in sentence_numbers],
            }
            for block_index, sentence_numbers in enumerate(blocks, start=1)
        ]
        block_count = len(blocks)
        for key in ("displayOrder", "answerOrder"):
            order = activity.get(key)
            if sorted(order or []) != list(range(1, block_count + 1)):
                raise AuthoringPacketError(f"{activity_id}.{key} must be a 1-based permutation")
            activity[key] = [_letter(int(value), upper=True) for value in order]

    if validate:
        schema = json.loads(CANONICAL_SCHEMA.read_text(encoding="utf-8"))
        schema_issues = validate_schema(canonical, schema)
        if schema_issues:
            raise AuthoringPacketError("canonical schema failed:\n" + "\n".join(issue.format() for issue in schema_issues))
        require_valid(validate_canonical(canonical, load_spec()))
    return canonical
