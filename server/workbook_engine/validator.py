"""Fail-closed validation for canonical content and compiled workbook views."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .textops import locate_target


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "config" / "workbook-spec.json"
META_RE = re.compile(r"도입|전개|예시|대조|강조|결론|다시 말해|이 말은|여기서는|(?:^|[\s,.;:!?])즉(?:[\s,.;:!?]|$)")
EN_RE = re.compile(r"[A-Za-z]")
WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
UPDATE_ID_RE = re.compile(r"U-[0-9]{8}-[0-9]{3,}")
SEMVER_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?")
UPDATE_SCOPES = {"new-only", "all", "selected", "manual-review"}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    severity: str = "error"

    def format(self) -> str:
        return f"[{self.severity.upper()}] {self.code} {self.path}: {self.message}"


class ValidationFailure(RuntimeError):
    def __init__(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues = list(issues)
        super().__init__("\n".join(issue.format() for issue in self.issues))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_spec(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_SPEC
    if target.exists():
        data = load_json(target)
        if isinstance(data, dict):
            return data
    return {}


def _add(issues: list[ValidationIssue], code: str, path: str, message: str, severity: str = "error") -> None:
    issues.append(ValidationIssue(code, path, message, severity))


def _targets_overlap(base_text: str, targets: list[dict[str, Any]]) -> bool:
    spans: list[tuple[int, int]] = []
    for item in targets:
        start, end = locate_target(base_text, item["target"])
        spans.append((start, end))
    spans.sort()
    return any(next_start < end for (_start, end), (next_start, _next_end) in zip(spans, spans[1:]))


def _validate_target_group(
    issues: list[ValidationIssue], path: str, exercise: dict[str, Any], *, require_targets: bool = True
) -> None:
    base_text = exercise.get("baseText")
    targets = exercise.get("targets")
    if not isinstance(base_text, str) or not base_text:
        _add(issues, "exercise.base", path, "baseText is required")
        return
    if not isinstance(targets, list) or (require_targets and not targets):
        _add(issues, "exercise.targets", path, "at least one target is required")
        return
    target_ids: list[str] = []
    for index, item in enumerate(targets):
        item_path = f"{path}.targets[{index}]"
        if not isinstance(item, dict):
            _add(issues, "target.type", item_path, "target must be an object")
            continue
        target_ids.append(str(item.get("id", "")))
        try:
            locate_target(base_text, item.get("target", {}))
        except (TypeError, ValueError) as error:
            _add(issues, "target.resolve", item_path, str(error))
    duplicates = [value for value, count in Counter(target_ids).items() if not value or count > 1]
    if duplicates:
        _add(issues, "target.ids", path, f"target IDs must be non-empty and unique: {duplicates}")
    try:
        if _targets_overlap(base_text, targets):
            _add(issues, "target.overlap", path, "targets overlap")
    except (TypeError, ValueError):
        pass


def _spec_stage_order(spec: dict[str, Any]) -> list[str]:
    order = spec.get("stageOrder")
    if isinstance(order, list) and order:
        return [str(value) for value in order]
    stages = spec.get("stages")
    if not stages:
        stages = spec.get("logicalStages")
    if isinstance(stages, list) and stages:
        return [str(stage.get("number", stage.get("no"))) for stage in stages]
    return [str(index) for index in range(1, 11)]


def validate_canonical(data: dict[str, Any], spec: dict[str, Any] | None = None) -> list[ValidationIssue]:
    spec = spec or {}
    issues: list[ValidationIssue] = []
    for key in ("schemaVersion", "specVersion", "contentVersion", "workbookId", "metadata", "sentences"):
        if key not in data:
            _add(issues, "root.required", key, "required field is missing")
    allowed_root = {
        "$schema", "schemaVersion", "specVersion", "contentVersion", "workbookId",
        "metadata", "sourceStatus", "updateState", "sentences", "passageActivities",
    }
    unknown_root = sorted(set(data) - allowed_root)
    if unknown_root:
        _add(issues, "root.unknown", "$", f"unknown root fields: {unknown_root}")
    for key in ("schemaVersion", "specVersion", "contentVersion"):
        if not SEMVER_RE.fullmatch(str(data.get(key, ""))):
            _add(issues, "version.semver", key, "version must use semantic versioning")

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        _add(issues, "metadata.type", "metadata", "metadata must be an object")
    else:
        for key in ("title", "kicker", "grade", "topic", "sourceLanguage", "targetLanguage"):
            if not str(metadata.get(key, "")).strip():
                _add(issues, "metadata.required", f"metadata.{key}", "required metadata is missing")
        if metadata.get("sourceLanguage") != "en" or metadata.get("targetLanguage") != "ko":
            _add(issues, "metadata.languages", "metadata", "languages must be en -> ko")

    source_status = data.get("sourceStatus", {})
    if source_status.get("status") != "confirmed":
        _add(issues, "source.unconfirmed", "sourceStatus.status", "release requires confirmed source")
    if source_status.get("sourceType") not in {"image", "pdf", "scan", "text", "manual", "mixed"}:
        _add(issues, "source.type", "sourceStatus.sourceType", "a supported sourceType is required")
    references = source_status.get("references")
    if not isinstance(references, list) or not references or any(not str(value).strip() for value in references):
        _add(issues, "source.references", "sourceStatus.references", "at least one source reference is required")

    update_state = data.get("updateState", {})
    if update_state.get("defaultScope") not in UPDATE_SCOPES:
        _add(issues, "update.scope", "updateState.defaultScope", "a valid default update scope is required")
    applied_updates = update_state.get("appliedUpdates")
    if not isinstance(applied_updates, list) or not applied_updates:
        _add(issues, "update.applied", "updateState.appliedUpdates", "at least one applied update record is required")
    else:
        update_ids: list[str] = []
        for update_index, update in enumerate(applied_updates):
            path = f"updateState.appliedUpdates[{update_index}]"
            if not isinstance(update, dict):
                _add(issues, "update.record", path, "applied update must be an object")
                continue
            update_id = str(update.get("id", ""))
            update_ids.append(update_id)
            if not UPDATE_ID_RE.fullmatch(update_id):
                _add(issues, "update.id", f"{path}.id", "invalid update id")
            if update.get("scope") not in UPDATE_SCOPES:
                _add(issues, "update.scope", f"{path}.scope", "invalid update scope")
            for key in ("fromContentVersion", "toContentVersion"):
                if not SEMVER_RE.fullmatch(str(update.get(key, ""))):
                    _add(issues, "update.version", f"{path}.{key}", "semantic version is required")
            if not str(update.get("appliedAt", "")).strip():
                _add(issues, "update.applied-at", f"{path}.appliedAt", "appliedAt is required")
            report = str(update.get("report", ""))
            if report and report != f"reports/updates/{update_id}.md":
                _add(issues, "update.report", f"{path}.report", "report path must match the update id")
        if len(update_ids) != len(set(update_ids)):
            _add(issues, "update.ids", "updateState.appliedUpdates", "applied update ids must be unique")
        last_valid = next((item for item in reversed(applied_updates) if isinstance(item, dict)), None)
        if last_valid and last_valid.get("toContentVersion") != data.get("contentVersion"):
            _add(issues, "update.current-version", "updateState.appliedUpdates", "latest update must end at contentVersion")

    sentences = data.get("sentences")
    if not isinstance(sentences, list) or not sentences:
        _add(issues, "sentences.empty", "sentences", "at least one sentence is required")
        return issues
    expected_count = source_status.get("sentenceCount")
    if not isinstance(expected_count, int) or expected_count != len(sentences):
        _add(issues, "sentences.count", "sentences", f"expected {expected_count}, found {len(sentences)}")

    ids: list[str] = []
    numbers: list[int] = []
    segment_ids: set[str] = set()
    sentence_by_id: dict[str, dict[str, Any]] = {}
    for index, sentence in enumerate(sentences, start=1):
        path = f"sentences[{index - 1}]"
        if not isinstance(sentence, dict):
            _add(issues, "sentence.type", path, "sentence must be an object")
            continue
        sentence_id = str(sentence.get("id", ""))
        ids.append(sentence_id)
        sentence_by_id[sentence_id] = sentence
        try:
            number = int(sentence.get("no"))
        except (TypeError, ValueError):
            number = -1
        numbers.append(number)
        if number != index:
            _add(issues, "sentence.number", f"{path}.no", f"expected {index}, found {sentence.get('no')}")
        source = sentence.get("source")
        translation = sentence.get("translation")
        if not isinstance(source, str) or not source:
            _add(issues, "sentence.source", f"{path}.source", "source is required")
            continue
        if not isinstance(translation, str) or not translation:
            _add(issues, "sentence.translation", f"{path}.translation", "translation is required")

        segments = sentence.get("meaningSegments")
        if not isinstance(segments, list) or not segments:
            _add(issues, "meaning.empty", f"{path}.meaningSegments", "meaning segments are required")
            continue
        reconstructed = " ".join(str(segment.get("en", "")) for segment in segments)
        if reconstructed != source:
            _add(issues, "meaning.source-fidelity", f"{path}.meaningSegments", "English segments do not reconstruct source exactly")
        if len(WORD_RE.findall(source)) >= 8 and len(segments) < 2:
            _add(issues, "meaning.too-few", f"{path}.meaningSegments", "long source requires at least two segments")
        for segment_index, segment in enumerate(segments):
            segment_path = f"{path}.meaningSegments[{segment_index}]"
            segment_id = str(segment.get("id", ""))
            if not segment_id or segment_id in segment_ids:
                _add(issues, "meaning.segment-id", f"{segment_path}.id", "segment ID must be unique")
            segment_ids.add(segment_id)
            en = str(segment.get("en", ""))
            ko = str(segment.get("ko", ""))
            if not en or not ko:
                _add(issues, "meaning.segment-text", segment_path, "en and ko are required")
            if len(WORD_RE.findall(en)) > 16:
                _add(issues, "meaning.segment-long", segment_path, "English segment exceeds 16 words")
            if EN_RE.search(ko):
                _add(issues, "meaning.ko-alphabet", f"{segment_path}.ko", "Korean hint contains Latin alphabet")
            if META_RE.search(ko):
                _add(issues, "meaning.ko-meta", f"{segment_path}.ko", "Korean hint contains explanatory meta wording")

        annotations = sentence.get("annotations", {})
        segment_map = {str(segment.get("id")): segment for segment in segments}
        for kind in ("predicates", "vocabulary"):
            for annotation_index, annotation in enumerate(annotations.get(kind, [])):
                annotation_path = f"{path}.annotations.{kind}[{annotation_index}]"
                segment = segment_map.get(str(annotation.get("segmentId")))
                if not segment:
                    _add(issues, "annotation.segment", annotation_path, "segmentId does not resolve")
                    continue
                for language in ("en", "ko"):
                    targets = annotation.get(language)
                    if isinstance(targets, dict):
                        targets = [targets]
                    for target in targets or []:
                        try:
                            locate_target(str(segment.get(language, "")), target)
                        except (TypeError, ValueError) as error:
                            _add(issues, "annotation.target", f"{annotation_path}.{language}", str(error))
                if kind == "vocabulary":
                    if not isinstance(annotation.get("en"), dict) or not isinstance(annotation.get("ko"), dict):
                        _add(issues, "vocab.pair", annotation_path, "vocabulary requires paired en and ko targets")
                    if annotation.get("colorSlot") not in {1, 2, 3, 4, 5, 6, 7, 8}:
                        _add(issues, "vocab.color", annotation_path, "colorSlot must be 1-8")
                    if not str(annotation.get("meaning", "")):
                        _add(issues, "vocab.meaning", annotation_path, "meaning is required")

        exercises = sentence.get("exercises", {})
        for name in ("koBlank", "enBlank", "verb", "choice"):
            exercise = exercises.get(name)
            if not isinstance(exercise, dict):
                _add(issues, "exercise.missing", f"{path}.exercises.{name}", "exercise is required")
                continue
            default_base = translation if name == "koBlank" else (sentence.get("display") or source)
            authored_base = exercise.get("baseText")
            if authored_base is not None:
                if authored_base == default_base:
                    _add(
                        issues,
                        "exercise.redundant-base",
                        f"{path}.exercises.{name}.baseText",
                        "remove baseText when it is identical to the canonical default",
                    )
                if not str(exercise.get("overrideReason", "")).strip():
                    _add(
                        issues,
                        "exercise.override-reason",
                        f"{path}.exercises.{name}",
                        "a divergent baseText requires overrideReason",
                    )
            elif exercise.get("overrideReason"):
                _add(
                    issues,
                    "exercise.orphan-reason",
                    f"{path}.exercises.{name}.overrideReason",
                    "overrideReason requires baseText",
                )
            resolved_exercise = dict(exercise)
            resolved_exercise["baseText"] = authored_base if authored_base is not None else default_base
            _validate_target_group(issues, f"{path}.exercises.{name}", resolved_exercise)
            if name == "verb":
                for target_index, target in enumerate(exercise.get("targets", [])):
                    if not str(target.get("cue", "")):
                        _add(issues, "verb.cue", f"{path}.exercises.verb.targets[{target_index}]", "cue is required")
            if name == "choice":
                for target_index, target in enumerate(exercise.get("targets", [])):
                    options = target.get("options")
                    correct = target.get("target", {}).get("text")
                    if not isinstance(options, list) or len(set(options)) < 2 or correct not in options:
                        _add(issues, "choice.options", f"{path}.exercises.choice.targets[{target_index}]", "options must contain one correct target and at least one different option")

        arrange = exercises.get("arrange", {})
        arrange_chunks = arrange.get("chunks", []) if isinstance(arrange, dict) else []
        chunk_text = " ".join(str(chunk.get("text", "")) for chunk in arrange_chunks)
        if chunk_text != source:
            _add(issues, "arrange.source-fidelity", f"{path}.exercises.arrange.chunks", "arrange chunks do not reconstruct source exactly")
        chunk_ids = [str(chunk.get("id", "")) for chunk in arrange_chunks]
        display_order = [str(value) for value in arrange.get("displayOrder", [])] if isinstance(arrange, dict) else []
        if Counter(chunk_ids) != Counter(display_order):
            _add(issues, "arrange.order", f"{path}.exercises.arrange.displayOrder", "displayOrder must be a permutation of chunk IDs")
        writing = exercises.get("writing", {})
        if not isinstance(writing, dict) or not isinstance(writing.get("bank"), list) or not writing["bank"]:
            _add(issues, "writing.bank", f"{path}.exercises.writing.bank", "writing bank is required")

    if len(ids) != len(set(ids)) or any(not value for value in ids):
        _add(issues, "sentence.ids", "sentences", "sentence IDs must be non-empty and unique")
    if numbers != list(range(1, len(sentences) + 1)):
        _add(issues, "sentence.sequence", "sentences", "sentence numbers must be continuous")

    activities = data.get("passageActivities", {})
    correction_activities = activities.get("correction", []) if isinstance(activities, dict) else []
    paragraph_activities = activities.get("paragraphOrder", []) if isinstance(activities, dict) else []
    if not isinstance(correction_activities, list) or not correction_activities:
        _add(issues, "correction.empty", "passageActivities.correction", "at least one correction activity is required")
        correction_activities = []
    if not isinstance(paragraph_activities, list) or not paragraph_activities:
        _add(issues, "paragraph.empty", "passageActivities.paragraphOrder", "at least one paragraph activity is required")
        paragraph_activities = []
    correction_ids = [str(activity.get("id", "")) for activity in correction_activities if isinstance(activity, dict)]
    if len(correction_ids) != len(set(correction_ids)) or any(not value for value in correction_ids):
        _add(issues, "correction.ids", "passageActivities.correction", "activity ids must be non-empty and unique")
    paragraph_ids = [str(activity.get("id", "")) for activity in paragraph_activities if isinstance(activity, dict)]
    if len(paragraph_ids) != len(set(paragraph_ids)) or any(not value for value in paragraph_ids):
        _add(issues, "paragraph.ids", "passageActivities.paragraphOrder", "activity ids must be non-empty and unique")

    all_correction_target_ids: set[str] = set()
    for activity_index, activity in enumerate(correction_activities):
        path = f"passageActivities.correction[{activity_index}]"
        text = str(activity.get("textOverride", ""))
        if not text:
            _add(issues, "correction.text", path, "textOverride is required for migrated correction activity")
            continue
        correction_targets = activity.get("targets", [])
        target_ids = [str(target.get("id", "")) for target in correction_targets if isinstance(target, dict)]
        if not correction_targets or len(target_ids) != len(set(target_ids)) or any(not value for value in target_ids):
            _add(issues, "correction.target-ids", f"{path}.targets", "target ids must be non-empty and unique")
        repeated_global = sorted(set(target_ids) & all_correction_target_ids)
        if repeated_global:
            _add(issues, "correction.target-ids", f"{path}.targets", f"target ids repeat another activity: {repeated_global}")
        all_correction_target_ids.update(target_ids)
        for target_index, target in enumerate(correction_targets):
            try:
                locate_target(text, target.get("target", {}))
            except (TypeError, ValueError) as error:
                _add(issues, "correction.target", f"{path}.targets[{target_index}]", str(error))
            if target.get("incorrect") != target.get("target", {}).get("text"):
                _add(issues, "correction.incorrect", f"{path}.targets[{target_index}]", "incorrect must match target text")
            if not str(target.get("correct", "")):
                _add(issues, "correction.correct", f"{path}.targets[{target_index}]", "correct value is required")

    paragraph_coverages: list[list[str]] = []
    for activity_index, activity in enumerate(paragraph_activities):
        path = f"passageActivities.paragraphOrder[{activity_index}]"
        blocks = activity.get("blocks", [])
        block_ids = [str(block.get("id", "")) for block in blocks]
        display_order = [str(value) for value in activity.get("displayOrder", [])]
        answer_order = [str(value) for value in activity.get("answerOrder", [])]
        if Counter(block_ids) != Counter(display_order) or Counter(block_ids) != Counter(answer_order):
            _add(issues, "paragraph.order", path, "displayOrder and answerOrder must be permutations of block IDs")
        covered = [sentence_id for block in blocks for sentence_id in block.get("sentenceIds", [])]
        paragraph_coverages.append(covered)
        covered_numbers = [sentence_by_id.get(sentence_id, {}).get("no") for sentence_id in covered]
        if (not covered or len(covered) != len(set(covered))
                or any(not isinstance(value, int) for value in covered_numbers)
                or sorted(covered_numbers) != list(range(min(covered_numbers), max(covered_numbers) + 1))):
            _add(issues, "paragraph.coverage", path,
                 "paragraph blocks must cover one contiguous passage exactly once")
        ordered_numbers: list[int] = []
        block_map = {str(block.get("id")): block for block in blocks}
        for block_id in answer_order:
            for sentence_id in block_map.get(block_id, {}).get("sentenceIds", []):
                ordered_numbers.append(int(sentence_by_id.get(sentence_id, {}).get("no", -1)))
        if ordered_numbers != sorted(covered_numbers):
            _add(issues, "paragraph.answer", path, "answerOrder does not reconstruct source sentence order")

    if paragraph_coverages:
        all_full_passage = all(Counter(covered) == Counter(ids) for covered in paragraph_coverages)
        partitioned_passages = (
            len(paragraph_coverages) > 1
            and Counter(sentence_id for covered in paragraph_coverages for sentence_id in covered)
            == Counter(ids)
        )
        if not all_full_passage and not partitioned_passages:
            _add(issues, "paragraph.coverage", "passageActivities.paragraphOrder",
                 "activities must each cover the full passage or partition all passages without overlap")

    if _spec_stage_order(spec) != [str(index) for index in range(1, 11)]:
        _add(issues, "spec.stage-order", "spec.stages", "spec must define stages 1-10 in order")
    return issues


def validate_compiled(data: dict[str, Any], expected_sentences: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    pages = data.get("pages") or data.get("steps")
    if not isinstance(pages, list) or not pages:
        return [ValidationIssue("compiled.pages", "pages", "compiled workbook has no pages")]
    grouped: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    page_ids: list[str] = []
    page_numbers: list[int] = []
    edition = str(data.get("edition", ""))
    for page_index, page in enumerate(pages):
        page_ids.append(str(page.get("pageId", "")))
        try:
            page_numbers.append(int(page.get("pageNo")))
        except (TypeError, ValueError):
            page_numbers.append(-1)
        stage_no = str(page.get("no"))
        if not order or order[-1] != stage_no:
            order.append(stage_no)
        grouped.setdefault(stage_no, []).append(page)
        if page.get("mode") == "meaning":
            entries = page.get("units", [])
        else:
            entries = page.get("items", [])
        if page.get("part") and entries:
            match = re.fullmatch(r"(\d+)-(\d+)", str(page["part"]))
            if not match:
                _add(issues, "compiled.part", f"pages[{page_index}].part", "part must be start-end")
            else:
                start, end = map(int, match.groups())
                numbers = [int(entry.get("no", -1)) for entry in entries]
                if numbers != list(range(start, end + 1)):
                    _add(issues, "compiled.numbering", f"pages[{page_index}]", "item numbers do not match part range")
        for item_index, item in enumerate(entries):
            solutions = item.get("solutions", {})
            if not isinstance(solutions, dict):
                _add(issues, "compiled.solutions", f"pages[{page_index}].items[{item_index}]", "solutions must be an object")
            if edition == "student" and solutions:
                _add(issues, "compiled.answer-leak", f"pages[{page_index}].items[{item_index}]", "student item contains solutions")
            if edition == "student" and "solutionText" in item:
                _add(issues, "compiled.answer-leak", f"pages[{page_index}].items[{item_index}]", "student item contains solutionText")
        if edition == "student" and (page.get("corrections") or page.get("sequenceAnswer")):
            _add(issues, "compiled.answer-leak", f"pages[{page_index}]", "student page contains answer-only activity data")
    if any(not value for value in page_ids) or len(page_ids) != len(set(page_ids)):
        _add(issues, "compiled.page-ids", "pages", "pageId values must be non-empty and unique")
    if page_numbers != list(range(1, len(pages) + 1)):
        _add(issues, "compiled.page-numbers", "pages", "pageNo values must be continuous")
    if order != [str(index) for index in range(1, 11)]:
        _add(issues, "compiled.stage-order", "pages", f"logical stage order is {order}")
    for stage_no in ("1", "2", "3", "4", "5", "6", "8", "10"):
        total = 0
        numbers: list[int] = []
        page_item_counts: list[int] = []
        for page in grouped.get(stage_no, []):
            entries = page.get("units", []) if stage_no == "1" else page.get("items", [])
            total += len(entries)
            page_item_counts.append(len(entries))
            numbers.extend(int(entry.get("no", -1)) for entry in entries)
        if total != expected_sentences or numbers != list(range(1, expected_sentences + 1)):
            _add(issues, "compiled.coverage", f"stage[{stage_no}]", f"expected full 1-{expected_sentences} coverage")
        if len(page_item_counts) > 1 and page_item_counts[-1] == 1:
            _add(
                issues,
                "compiled.singleton-tail",
                f"stage[{stage_no}]",
                "a continuation page must not contain only one item",
            )
        if page_item_counts and max(page_item_counts) - min(page_item_counts) > 1:
            _add(
                issues,
                "compiled.page-balance",
                f"stage[{stage_no}]",
                f"same-stage page counts are not balanced: {page_item_counts}",
            )
    return issues


def require_valid(issues: Iterable[ValidationIssue]) -> None:
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        raise ValidationFailure(errors)
