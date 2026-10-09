"""Compare workbook snapshots and render deterministic update reports.

This module has no implicit filesystem side effects.  ``write_report`` writes only
the requested report; ``update_changelog`` must be called explicitly when a
CHANGELOG entry is wanted.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date as calendar_date
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence

from .manifest import COMPONENTS, ManifestBundle, json_digest, load_bundle, read_json


APPLY_TO_VALUES = ("new-only", "all", "selected", "manual-review")
CHANGE_KINDS = ("added", "removed", "modified")
_SAFE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
_NATURAL_PART = re.compile(r"(\d+)")
_FILE_FINGERPRINT_KEYS = (
    "sha256",
    "hash",
    "digest",
    "checksum",
    "contentHash",
    "size",
)


def _natural_key(value: Any) -> tuple[Any, ...]:
    return tuple(
        int(part) if part.isdigit() else part.casefold()
        for part in _NATURAL_PART.split(str(value))
    )


def _json_path(parent: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{parent}[{key}]"
    if _SAFE_KEY.fullmatch(key):
        return f"{parent}.{key}"
    escaped = key.replace("\\", "\\\\").replace("'", "\\'")
    return f"{parent}['{escaped}']"


def _summary(value: Any, *, limit: int = 120) -> str:
    if value is _MISSING:
        return "—"
    rendered = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    rendered = rendered.replace("\n", "\\n")
    if len(rendered) > limit:
        rendered = rendered[: limit - 1] + "…"
    return rendered


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


class _Missing:
    pass


_MISSING = _Missing()


@dataclass(frozen=True)
class UpdateDefinition:
    update_id: str
    title: str
    date: str
    summary: str
    category: str
    apply_to: str
    selected_workbooks: tuple[str, ...] = ()
    affected_stages: tuple[str, ...] = ()
    direct_files: tuple[str, ...] = ()
    direct_json_paths: tuple[tuple[str, str], ...] = ()
    request: tuple[str, ...] = ()
    verification: tuple[Mapping[str, Any], ...] = ()

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "UpdateDefinition":
        if not isinstance(value, Mapping):
            raise ValueError("update definition must be a JSON object")
        required = ("id", "title", "date", "summary", "category", "applyTo")
        missing = [name for name in required if not value.get(name)]
        if missing:
            raise ValueError(f"missing update field(s): {', '.join(missing)}")
        update_id = str(value["id"])
        if not re.fullmatch(r"U-\d{8}-\d{3,}", update_id):
            raise ValueError("update id must match U-YYYYMMDD-NNN")
        update_date = str(value["date"])
        try:
            calendar_date.fromisoformat(update_date)
        except ValueError as error:
            raise ValueError("update date must use YYYY-MM-DD") from error

        apply_to = str(value["applyTo"])
        if apply_to not in APPLY_TO_VALUES:
            allowed = ", ".join(APPLY_TO_VALUES)
            raise ValueError(f"applyTo must be one of: {allowed}")

        selected_value = value.get("selectedWorkbooks", ())
        if isinstance(selected_value, str) or not isinstance(selected_value, Sequence):
            raise ValueError("selectedWorkbooks must be an array")
        selected = tuple(str(item) for item in selected_value)
        if apply_to == "selected" and not selected:
            raise ValueError("selectedWorkbooks is required when applyTo is selected")

        direct = value.get("directChanges", {})
        if direct is None:
            direct = {}
        if not isinstance(direct, Mapping):
            raise ValueError("directChanges must be a JSON object")
        file_values = direct.get("files", ())
        if isinstance(file_values, str) or not isinstance(file_values, Sequence):
            raise ValueError("directChanges.files must be an array")
        direct_files = tuple(sorted({str(item) for item in file_values}))

        path_specs: list[tuple[str, str]] = []
        json_path_values = direct.get("jsonPaths", ())
        if isinstance(json_path_values, str) or not isinstance(json_path_values, Sequence):
            raise ValueError("directChanges.jsonPaths must be an array")
        for item in json_path_values:
            if not isinstance(item, Mapping):
                raise ValueError("directChanges.jsonPaths entries must be objects")
            manifest = str(item.get("manifest", ""))
            path = str(item.get("path", ""))
            if manifest not in COMPONENTS or not path.startswith("$"):
                raise ValueError(
                    "each direct JSON path needs a valid manifest and a path starting with $"
                )
            path_specs.append((manifest, path))

        stage_values = value.get("affectedStages", ())
        if isinstance(stage_values, str) or not isinstance(stage_values, Sequence):
            raise ValueError("affectedStages must be an array")
        stages = tuple(sorted({str(item) for item in stage_values}, key=_natural_key))
        request = value.get("request", ())
        if isinstance(request, str):
            request = (request,)
        elif not isinstance(request, Sequence):
            raise ValueError("request must be a string or an array")
        verification = value.get("verification", ())
        if not isinstance(verification, Sequence) or isinstance(verification, str):
            raise ValueError("verification must be an array")
        normalized_verification: list[Mapping[str, Any]] = []
        for item in verification:
            if not isinstance(item, Mapping):
                raise ValueError("verification entries must be objects")
            normalized_verification.append(dict(item))

        return cls(
            update_id=update_id,
            title=str(value["title"]),
            date=update_date,
            summary=str(value["summary"]),
            category=str(value["category"]),
            apply_to=apply_to,
            selected_workbooks=tuple(sorted(set(selected), key=_natural_key)),
            affected_stages=stages,
            direct_files=direct_files,
            direct_json_paths=tuple(sorted(set(path_specs))),
            request=tuple(str(item) for item in request),
            verification=tuple(normalized_verification),
        )


@dataclass(frozen=True)
class JsonChange:
    manifest: str
    path: str
    kind: str
    before: Any
    after: Any
    classification: str
    stage_ids: tuple[str, ...] = ()
    item_ids: tuple[str, ...] = ()
    page_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class FileChange:
    manifest: str
    path: str
    kind: str
    classification: str
    before: str = "—"
    after: str = "—"


@dataclass(frozen=True)
class OutputChange:
    output: str
    kind: str
    before: str
    after: str


@dataclass(frozen=True)
class PageChange:
    page: str
    kind: str
    stage_ids: tuple[str, ...] = ()
    item_ids: tuple[str, ...] = ()


@dataclass
class ChangeReport:
    update: UpdateDefinition
    component_rows: list[dict[str, str]] = field(default_factory=list)
    json_changes: list[JsonChange] = field(default_factory=list)
    file_changes: list[FileChange] = field(default_factory=list)
    output_changes: list[OutputChange] = field(default_factory=list)
    page_changes: list[PageChange] = field(default_factory=list)
    stage_ids: list[str] = field(default_factory=list)
    item_ids: list[str] = field(default_factory=list)

    @property
    def direct_changes(self) -> list[JsonChange]:
        return [change for change in self.json_changes if change.classification == "direct"]

    @property
    def derived_changes(self) -> list[JsonChange]:
        return [change for change in self.json_changes if change.classification == "derived"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "update": {
                "id": self.update.update_id,
                "title": self.update.title,
                "date": self.update.date,
                "category": self.update.category,
                "applyTo": self.update.apply_to,
            },
            "components": list(self.component_rows),
            "counts": {
                "directJsonPaths": len(self.direct_changes),
                "derivedJsonPaths": len(self.derived_changes),
                "files": len(self.file_changes),
                "outputs": len(self.output_changes),
                "pages": len(self.page_changes),
            },
            "stageIds": list(self.stage_ids),
            "itemIds": list(self.item_ids),
        }


def load_update(path: str | Path) -> UpdateDefinition:
    value = read_json(path)
    if not isinstance(value, Mapping):
        raise ValueError("update definition must be a JSON object")
    return UpdateDefinition.from_dict(value)


def _context_from_mapping(
    mapping: Mapping[str, Any], collection: str | None
) -> tuple[set[str], set[str], set[str]]:
    stages: set[str] = set()
    items: set[str] = set()
    pages: set[str] = set()

    for key in ("stageId", "stage_id", "stepId", "step_id", "stage", "step"):
        value = mapping.get(key)
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            stages.add(str(value))
    for key in ("itemId", "item_id", "sentenceId", "sentence_id", "unitId", "unit_id"):
        value = mapping.get(key)
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            items.add(str(value))
    for key in ("pageId", "page_id"):
        value = mapping.get(key)
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            pages.add(str(value))

    identifier = next(
        (
            mapping[key]
            for key in ("id", "no", "number")
            if isinstance(mapping.get(key), (str, int))
            and not isinstance(mapping.get(key), bool)
        ),
        None,
    )
    if identifier is not None:
        if collection in {"stages", "steps", "worksheets"}:
            stages.add(str(identifier))
        elif collection in {"items", "sentences", "units", "questions"}:
            items.add(str(identifier))
        elif collection == "pages":
            pages.add(str(identifier))

    if collection == "pages":
        page_number = mapping.get("page", mapping.get("pageNo", mapping.get("number")))
        edition = mapping.get("edition")
        if isinstance(page_number, (str, int)) and not isinstance(page_number, bool):
            pages.add(f"{edition}:{page_number}" if edition else str(page_number))
    return stages, items, pages


def _is_declared_direct(
    update: UpdateDefinition, manifest: str, path: str
) -> bool:
    if (manifest, path) in update.direct_json_paths:
        return True
    return any(
        manifest == direct_manifest
        and (path == direct_path or path.startswith(direct_path + ".") or path.startswith(direct_path + "["))
        for direct_manifest, direct_path in update.direct_json_paths
    )


def _diff_json(
    before: Any,
    after: Any,
    *,
    manifest: str,
    update: UpdateDefinition,
    path: str = "$",
    collection: str | None = None,
    stages: frozenset[str] = frozenset(),
    items: frozenset[str] = frozenset(),
    pages: frozenset[str] = frozenset(),
) -> list[JsonChange]:
    before_mapping = before if isinstance(before, Mapping) else {}
    after_mapping = after if isinstance(after, Mapping) else {}
    local_stages: set[str] = set(stages)
    local_items: set[str] = set(items)
    local_pages: set[str] = set(pages)
    for mapping in (before_mapping, after_mapping):
        found_stages, found_items, found_pages = _context_from_mapping(mapping, collection)
        local_stages.update(found_stages)
        local_items.update(found_items)
        local_pages.update(found_pages)

    if isinstance(before, Mapping) and isinstance(after, Mapping):
        changes: list[JsonChange] = []
        for key in sorted(set(before) | set(after)):
            next_before = before.get(key, _MISSING)
            next_after = after.get(key, _MISSING)
            changes.extend(
                _diff_json(
                    next_before,
                    next_after,
                    manifest=manifest,
                    update=update,
                    path=_json_path(path, key),
                    collection=key,
                    stages=frozenset(local_stages),
                    items=frozenset(local_items),
                    pages=frozenset(local_pages),
                )
            )
        return changes

    if isinstance(before, list) and isinstance(after, list):
        changes = []
        for index in range(max(len(before), len(after))):
            next_before = before[index] if index < len(before) else _MISSING
            next_after = after[index] if index < len(after) else _MISSING
            changes.extend(
                _diff_json(
                    next_before,
                    next_after,
                    manifest=manifest,
                    update=update,
                    path=_json_path(path, index),
                    collection=collection,
                    stages=frozenset(local_stages),
                    items=frozenset(local_items),
                    pages=frozenset(local_pages),
                )
            )
        return changes

    if before is not _MISSING and after is not _MISSING and before == after:
        return []

    if before is _MISSING:
        kind = "added"
    elif after is _MISSING:
        kind = "removed"
    else:
        kind = "modified"
    classification = (
        "direct"
        if manifest != "build" or _is_declared_direct(update, manifest, path)
        else "derived"
    )
    return [
        JsonChange(
            manifest=manifest,
            path=path,
            kind=kind,
            before=before,
            after=after,
            classification=classification,
            stage_ids=tuple(sorted(local_stages, key=_natural_key)),
            item_ids=tuple(sorted(local_items, key=_natural_key)),
            page_ids=tuple(sorted(local_pages, key=_natural_key)),
        )
    ]


def _file_records(component: Mapping[str, Any]) -> dict[str, Any]:
    files = component.get("files", ())
    records: dict[str, Any] = {}
    if isinstance(files, Mapping):
        for path, metadata in files.items():
            records[str(path)] = metadata
    elif isinstance(files, list):
        for item in files:
            if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
                continue
            records[item["path"]] = dict(item)
    return records


def _fingerprint(record: Any) -> str:
    if isinstance(record, Mapping):
        reduced = {
            key: record[key] for key in _FILE_FINGERPRINT_KEYS if key in record
        }
        if reduced:
            return _summary(reduced, limit=80)
    return _summary(record, limit=80)


def _compare_files(
    before: ManifestBundle, after: ManifestBundle, update: UpdateDefinition
) -> list[FileChange]:
    changes: list[FileChange] = []
    observed_direct: set[str] = set()
    for manifest in COMPONENTS:
        old = _file_records(before.component(manifest))
        new = _file_records(after.component(manifest))
        for path in sorted(set(old) | set(new), key=_natural_key):
            if path in old and path in new and old[path] == new[path]:
                continue
            if path not in old:
                kind = "added"
            elif path not in new:
                kind = "removed"
            else:
                kind = "modified"
            classification = (
                "direct"
                if manifest != "build" or path in update.direct_files
                else "derived"
            )
            if path in update.direct_files:
                observed_direct.add(path)
            changes.append(
                FileChange(
                    manifest=manifest,
                    path=path,
                    kind=kind,
                    classification=classification,
                    before=_fingerprint(old.get(path, _MISSING)),
                    after=_fingerprint(new.get(path, _MISSING)),
                )
            )
    for path in sorted(set(update.direct_files) - observed_direct, key=_natural_key):
        changes.append(
            FileChange(
                manifest="declared",
                path=path,
                kind="declared",
                classification="direct",
            )
        )
    return sorted(
        changes,
        key=lambda change: (
            change.classification,
            change.manifest,
            _natural_key(change.path),
        ),
    )


def _named_records(value: Any, key: str) -> dict[str, Any]:
    """Collect conventional ``outputs`` or ``pages`` records recursively."""

    records: dict[str, Any] = {}

    def visit(node: Any, prefix: str) -> None:
        if isinstance(node, Mapping):
            for child_key, child in node.items():
                child_prefix = f"{prefix}/{child_key}" if prefix else str(child_key)
                if child_key == key:
                    add_collection(child, child_prefix)
                else:
                    visit(child, child_prefix)
        elif isinstance(node, list):
            for index, child in enumerate(node):
                visit(child, f"{prefix}/{index}")

    def add_collection(collection: Any, prefix: str) -> None:
        if isinstance(collection, Mapping):
            for name, record in collection.items():
                records[str(name)] = record
            return
        if not isinstance(collection, list):
            return
        for index, record in enumerate(collection):
            if isinstance(record, Mapping):
                candidates = (
                    ("path", record.get("path")),
                    ("id", record.get("id")),
                    ("name", record.get("name")),
                    ("output", record.get("output")),
                )
                name = next(
                    (str(value) for _, value in candidates if value is not None),
                    None,
                )
                if name is None and key == "pages":
                    page = record.get("page", record.get("pageNo", record.get("number")))
                    edition = record.get("edition")
                    if page is not None:
                        name = f"{edition}:{page}" if edition else str(page)
                if name is None:
                    name = f"{prefix}/{index}"
            else:
                name = f"{prefix}/{index}"
            records[name] = record

    visit(value, "")
    return records


def _compare_outputs(before: ManifestBundle, after: ManifestBundle) -> list[OutputChange]:
    old = _named_records(before.build, "outputs")
    new = _named_records(after.build, "outputs")
    changes: list[OutputChange] = []
    for name in sorted(set(old) | set(new), key=_natural_key):
        if name in old and name in new and old[name] == new[name]:
            continue
        kind = "added" if name not in old else "removed" if name not in new else "modified"
        changes.append(
            OutputChange(
                output=name,
                kind=kind,
                before=_summary(old.get(name, _MISSING)),
                after=_summary(new.get(name, _MISSING)),
            )
        )
    return changes


def _record_context(record: Any, collection: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(record, Mapping):
        return (), ()
    stages, items, _ = _context_from_mapping(record, collection)
    for item in record.get("stageIds", ()) if isinstance(record.get("stageIds"), list) else ():
        stages.add(str(item))
    for item in record.get("itemIds", ()) if isinstance(record.get("itemIds"), list) else ():
        items.add(str(item))
    return (
        tuple(sorted(stages, key=_natural_key)),
        tuple(sorted(items, key=_natural_key)),
    )


def _compare_pages(before: ManifestBundle, after: ManifestBundle) -> list[PageChange]:
    old = _named_records(before.build, "pages")
    new = _named_records(after.build, "pages")
    changes: list[PageChange] = []
    for name in sorted(set(old) | set(new), key=_natural_key):
        if name in old and name in new and old[name] == new[name]:
            continue
        kind = "added" if name not in old else "removed" if name not in new else "modified"
        stages: set[str] = set()
        items: set[str] = set()
        for record in (old.get(name), new.get(name)):
            found_stages, found_items = _record_context(record, "pages")
            stages.update(found_stages)
            items.update(found_items)
        changes.append(
            PageChange(
                page=name,
                kind=kind,
                stage_ids=tuple(sorted(stages, key=_natural_key)),
                item_ids=tuple(sorted(items, key=_natural_key)),
            )
        )
    return changes


def compare_bundles(
    before: ManifestBundle,
    after: ManifestBundle,
    update: UpdateDefinition,
) -> ChangeReport:
    """Compare all four manifest components and return a report model."""

    component_rows: list[dict[str, str]] = []
    json_changes: list[JsonChange] = []
    before_versions = before.versions()
    after_versions = after.versions()
    for component in COMPONENTS:
        old = before.component(component)
        new = after.component(component)
        old_digest = json_digest(old)
        new_digest = json_digest(new)
        component_rows.append(
            {
                "component": component,
                "beforeVersion": before_versions[component] or "—",
                "afterVersion": after_versions[component] or "—",
                "beforeDigest": old_digest[:12],
                "afterDigest": new_digest[:12],
                "status": "changed" if old_digest != new_digest else "unchanged",
            }
        )
        json_changes.extend(
            _diff_json(old, new, manifest=component, update=update)
        )

    json_changes.sort(
        key=lambda change: (
            change.classification,
            COMPONENTS.index(change.manifest),
            _natural_key(change.path),
        )
    )
    file_changes = _compare_files(before, after, update)
    output_changes = _compare_outputs(before, after)
    page_changes = _compare_pages(before, after)

    stages: set[str] = set(update.affected_stages)
    items: set[str] = set()
    for change in json_changes:
        stages.update(change.stage_ids)
        items.update(change.item_ids)
    for page in page_changes:
        stages.update(page.stage_ids)
        items.update(page.item_ids)

    return ChangeReport(
        update=update,
        component_rows=component_rows,
        json_changes=json_changes,
        file_changes=file_changes,
        output_changes=output_changes,
        page_changes=page_changes,
        stage_ids=sorted(stages, key=_natural_key),
        item_ids=sorted(items, key=_natural_key),
    )


def _apply_scope(update: UpdateDefinition) -> str:
    labels = {
        "new-only": "신규 워크북만",
        "all": "전체 워크북",
        "selected": "선택 워크북",
        "manual-review": "자동 적용 없음 · 수동 검토",
    }
    value = labels[update.apply_to]
    if update.apply_to == "selected":
        value += ": " + ", ".join(update.selected_workbooks)
    return value


def _render_json_table(changes: Iterable[JsonChange]) -> list[str]:
    rows = list(changes)
    if not rows:
        return ["변경 없음"]
    lines = [
        "| manifest | JSON 경로 | 변경 | 이전 | 이후 |",
        "|---|---|---|---|---|",
    ]
    for change in rows:
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    change.manifest,
                    f"`{change.path}`",
                    change.kind,
                    _summary(change.before),
                    _summary(change.after),
                )
            )
            + " |"
        )
    return lines


def render_markdown(report: ChangeReport) -> str:
    """Render a byte-for-byte deterministic Korean Markdown report."""

    update = report.update
    lines = [
        f"# 업데이트 보고서 `{update.update_id}`: {update.title}",
        "",
        "## 요약",
        "",
        update.summary,
        "",
        "## 업데이트 정보",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| ID | `{_cell(update.update_id)}` |",
        f"| 날짜 | {_cell(update.date)} |",
        f"| 분류 | `{_cell(update.category)}` |",
        f"| 적용 범위 | `{_cell(update.apply_to)}` — {_cell(_apply_scope(update))} |",
        "",
    ]
    if update.request:
        lines.extend(["## 요청 내용", ""])
        lines.extend(f"- {item}" for item in update.request)
        lines.append("")

    lines.extend(
        [
            "## manifest 비교",
            "",
            "| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |",
            "|---|---:|---:|---|---|---|",
        ]
    )
    status_label = {"changed": "변경", "unchanged": "동일"}
    for row in report.component_rows:
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    row["component"],
                    row["beforeVersion"],
                    row["afterVersion"],
                    f"`{row['beforeDigest']}`",
                    f"`{row['afterDigest']}`",
                    status_label[row["status"]],
                )
            )
            + " |"
        )

    lines.extend(["", "## 파일 변경", ""])
    if not report.file_changes:
        lines.append("변경 없음")
    else:
        lines.extend(
            [
                "| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |",
                "|---|---|---|---|---|---|",
            ]
        )
        for change in report.file_changes:
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        "직접" if change.classification == "direct" else "파생",
                        change.manifest,
                        f"`{change.path}`",
                        change.kind,
                        change.before,
                        change.after,
                    )
                )
                + " |"
            )

    lines.extend(["", "## 직접 변경", "", "### JSON 경로", ""])
    lines.extend(_render_json_table(report.direct_changes))

    lines.extend(["", "## 파생 영향 (파생 변경)", "", "### JSON 경로", ""])
    lines.extend(_render_json_table(report.derived_changes))
    lines.extend(
        [
            "",
            "### 단계·문항",
            "",
            "| 항목 | 영향 ID |",
            "|---|---|",
            f"| 단계 | {_cell(', '.join(report.stage_ids) if report.stage_ids else '없음')} |",
            f"| 문항 | {_cell(', '.join(report.item_ids) if report.item_ids else '없음')} |",
            "",
            "### 페이지",
            "",
        ]
    )
    if not report.page_changes:
        lines.append("변경 없음")
    else:
        lines.extend(
            [
                "| 페이지 | 변경 | 단계 | 문항 |",
                "|---|---|---|---|",
            ]
        )
        for page in report.page_changes:
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        page.page,
                        page.kind,
                        ", ".join(page.stage_ids) or "—",
                        ", ".join(page.item_ids) or "—",
                    )
                )
                + " |"
            )

    lines.extend(["", "## 출력 변화", ""])
    if not report.output_changes:
        lines.append("변경 없음")
    else:
        lines.extend(
            [
                "| 출력 | 변경 | 이전 | 이후 |",
                "|---|---|---|---|",
            ]
        )
        for output in report.output_changes:
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        f"`{output.output}`",
                        output.kind,
                        output.before,
                        output.after,
                    )
                )
                + " |"
            )

    unchanged_components = [
        row["component"] for row in report.component_rows if row["status"] == "unchanged"
    ]
    all_stages = {str(index) for index in range(1, 11)}
    unaffected_stages = sorted(all_stages - set(report.stage_ids), key=_natural_key)
    lines.extend(["", "## 영향 없음", ""])
    lines.append(
        "- 동일한 manifest 구성 요소: "
        + (", ".join(f"`{value}`" for value in unchanged_components) if unchanged_components else "없음")
    )
    lines.append(
        "- 직접·파생 변경이 기록되지 않은 단계: "
        + (", ".join(unaffected_stages) if unaffected_stages else "없음")
    )
    lines.append("- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.")

    lines.extend(["", "## 검증 결과", ""])
    if not update.verification:
        lines.append("등록된 검증 결과 없음")
    else:
        lines.extend(["| 검사 | 결과 | 설명 |", "|---|---|---|"])
        for check in sorted(
            update.verification, key=lambda item: _natural_key(item.get("name", ""))
        ):
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        check.get("name", "—"),
                        check.get("status", "—"),
                        check.get("details", "—"),
                    )
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## 호환성",
            "",
            f"- 적용 범위: `{update.apply_to}` — {_apply_scope(update)}",
            "- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.",
            "- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.",
            "",
            "## 버전",
            "",
            "| 구성 요소 | 이전 | 이후 |",
            "|---|---:|---:|",
        ]
    )
    for row in report.component_rows:
        lines.append(
            f"| {row['component']} | {row['beforeVersion']} | {row['afterVersion']} |"
        )

    lines.extend(
        [
            "",
            "## 변경 통계",
            "",
            f"- 직접 JSON 경로: {len(report.direct_changes)}",
            f"- 파생 JSON 경로: {len(report.derived_changes)}",
            f"- 변경·선언 파일: {len(report.file_changes)}",
            f"- 영향 페이지: {len(report.page_changes)}",
            f"- 변경 출력: {len(report.output_changes)}",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(path: str | Path, report: ChangeReport) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown(report), encoding="utf-8")
    return destination


def _changelog_line(report: ChangeReport, report_link: str | None) -> str:
    title = report.update.title.replace("\n", " ").strip()
    summary = report.update.summary.replace("\n", " ").strip()
    if len(summary) > 100:
        summary = summary[:99] + "…"
    identifier = report.update.update_id
    label = f"[{identifier}]({report_link})" if report_link else f"`{identifier}`"
    return (
        f"- {report.update.date} — {label}: {title} — {summary} "
        f"(`{report.update.apply_to}`)"
    )


def update_changelog(
    path: str | Path,
    report: ChangeReport,
    *,
    report_path: str | Path | None = None,
) -> Path:
    """Explicitly upsert one concise entry; repeated calls never duplicate it."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if report_path is None:
        link = None
    else:
        report_destination = Path(report_path)
        try:
            link = report_destination.resolve().relative_to(destination.parent.resolve()).as_posix()
        except ValueError:
            link = report_destination.as_posix()
    entry = _changelog_line(report, link)

    if destination.exists():
        content = destination.read_text(encoding="utf-8")
    else:
        content = "# CHANGELOG\n"
    lines = content.rstrip("\n").splitlines()
    if not lines:
        lines = ["# CHANGELOG"]
    identifier_pattern = re.compile(
        rf"^- .*?(?:\[{re.escape(report.update.update_id)}\]\(|`{re.escape(report.update.update_id)}`)"
    )
    matching_indexes = [
        index for index, line in enumerate(lines) if identifier_pattern.search(line)
    ]
    replaced = bool(matching_indexes)
    if matching_indexes:
        lines[matching_indexes[0]] = entry
        for index in reversed(matching_indexes[1:]):
            del lines[index]
    if not replaced:
        if lines[-1] != "":
            lines.append("")
        lines.append(entry)
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return destination


def build_report(
    *,
    update_path: str | Path,
    before_path: str | Path,
    after_path: str | Path,
) -> ChangeReport:
    return compare_bundles(
        load_bundle(before_path),
        load_bundle(after_path),
        load_update(update_path),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare workbook manifest bundles and write an update report."
    )
    parser.add_argument("--update", required=True, help="update definition JSON")
    parser.add_argument("--before", required=True, help="before manifest bundle JSON")
    parser.add_argument("--after", required=True, help="after manifest bundle JSON")
    parser.add_argument("--report", required=True, help="Markdown report destination")
    parser.add_argument(
        "--changelog",
        help="optional CHANGELOG path; omitted means no CHANGELOG side effect",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = build_report(
        update_path=args.update,
        before_path=args.before,
        after_path=args.after,
    )
    report_path = write_report(args.report, report)
    if args.changelog:
        update_changelog(args.changelog, report, report_path=report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
