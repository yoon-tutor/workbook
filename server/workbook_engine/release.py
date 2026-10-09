"""Two-phase workbook release: prepare privately, visually approve, publish atomically."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import uuid4

from . import ENGINE_VERSION
from .change_report import (
    compare_bundles,
    load_update,
    render_markdown,
    update_changelog,
    write_report,
)
from .compiler import (
    compile_workbook,
    lock_response_layout,
    lock_solution_slot_layouts,
    project_student_workbook,
)
from .manifest import (
    ManifestBundle,
    canonical_json,
    file_manifest,
    file_record,
    json_digest,
    load_bundle,
    write_bundle,
    write_json,
)
from .qa import (
    ReleaseQA,
    measure_answer_layouts,
    run_release_qa,
)
from .render import write_html
from .schema_gate import validate_schema
from .validator import load_json, load_spec, require_valid, validate_canonical


ROOT = Path(__file__).resolve().parents[1]
VERSIONS_PATH = ROOT / "config" / "versions.json"
SPEC_PATH = ROOT / "config" / "workbook-spec.json"
SEMANTIC_RUBRIC_PATH = ROOT / "docs" / "semantic-rubric.md"
CANONICAL_SCHEMA_PATH = ROOT / "schemas" / "canonical-workbook.schema.json"
UPDATE_SCHEMA_PATH = ROOT / "schemas" / "update.schema.json"
FOOTER_LOGO_PATH = ROOT / "assets" / "yonjogyo-logo-footer.png"
TEMPLATE_PATHS = (
    ROOT / "workbook_engine" / "templates" / "shell.html",
    ROOT / "workbook_engine" / "templates" / "workbook.css",
    ROOT / "workbook_engine" / "templates" / "renderer.js",
    FOOTER_LOGO_PATH,
)
ENGINE_INPUT_PATHS = tuple(sorted((ROOT / "workbook_engine").glob("*.py")))
PUBLIC_FILENAMES = ("문제.html", "문제.pdf", "해설.html", "해설.pdf")


class ReleaseError(RuntimeError):
    """Raised when a release cannot safely advance to the next phase."""


@dataclass(frozen=True)
class PreparedRelease:
    build_dir: Path
    state_path: Path
    student_html: Path
    student_pdf: Path
    answer_html: Path
    answer_pdf: Path
    contact_sheets: tuple[Path, ...]
    page_count: int


@dataclass(frozen=True)
class PublishedRelease:
    output_dir: Path
    report_path: Path
    aggregate_report_path: Path
    build_manifest_path: Path
    bundle_path: Path


def release_status(canonical_path: Path, *, build_dir: Path | None = None) -> dict[str, Any]:
    canonical_path = canonical_path.resolve()
    canonical = load_json(canonical_path)
    workbook_id = str(canonical.get("workbookId", ""))
    if build_dir is None:
        root = ROOT / ".build" / "releases" / _slug(workbook_id)
        candidates = sorted(
            (path for path in root.iterdir() if (path / "release-state.json").is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        ) if root.is_dir() else []
        if not candidates:
            return {
                "status": "no-prepared-build",
                "workbookId": workbook_id,
                "canonicalPath": str(canonical_path),
                "canPublish": False,
            }
        build_dir = candidates[0]
    build_dir = build_dir.resolve()
    state_path = build_dir / "release-state.json"
    if not state_path.is_file():
        raise ReleaseError("release-state.json was not found")
    state = load_json(state_path)
    expected = state.get("inputDigests", {})
    try:
        current = _input_digests(Path(state["canonicalPath"]), Path(state["updatePath"]))
    except (KeyError, OSError) as error:
        current = {}
        input_error = str(error)
    else:
        input_error = ""
    changed = sorted(
        path
        for path in set(current) | set(expected)
        if current.get(path) != expected.get(path)
    )
    try:
        _verify_prepared_artifacts(build_dir, state)
    except ReleaseError as error:
        artifacts_ok = False
        artifact_error = str(error)
    else:
        artifacts_ok = True
        artifact_error = ""
    current_status = str(state.get("status", "unknown"))
    manifest = {
        "status": current_status,
        "workbookId": workbook_id,
        "buildDir": str(build_dir),
        "pageCount": state.get("pageCount"),
        "contactSheets": state.get("contactSheets", []),
        "inputsCurrent": not changed and not input_error,
        "changedInputs": changed,
        "inputError": input_error or None,
        "artifactsIntact": artifacts_ok,
        "artifactError": artifact_error or None,
        "canPublish": (
            current_status == "awaiting-visual-review"
            and not changed
            and not input_error
            and artifacts_ok
        ),
        "outputDir": state.get("outputDir"),
        "visualReview": state.get("visualReview"),
    }
    return manifest


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _copy_public_artifact(source: Path, destination: Path) -> None:
    """Copy release bytes without carrying private-build visibility metadata."""
    shutil.copyfile(source, destination)
    hidden_flag = getattr(stat, "UF_HIDDEN", 0)
    change_flags = getattr(os, "chflags", None)
    destination_flags = getattr(destination.stat(), "st_flags", 0)
    if hidden_flag and change_flags is not None and destination_flags & hidden_flag:
        change_flags(destination, destination_flags & ~hidden_flag)


def _input_digests(canonical_path: Path, update_path: Path) -> dict[str, str]:
    paths = (
        canonical_path.resolve(),
        update_path.resolve(),
        SPEC_PATH,
        VERSIONS_PATH,
        SEMANTIC_RUBRIC_PATH,
        CANONICAL_SCHEMA_PATH,
        UPDATE_SCHEMA_PATH,
        *TEMPLATE_PATHS,
        *ENGINE_INPUT_PATHS,
    )
    manifest = {
        (
            path.resolve().relative_to(ROOT.resolve()).as_posix()
            if path.resolve().is_relative_to(ROOT.resolve())
            else path.resolve().as_posix()
        ): _sha256_file(path)
        for path in paths
    }
    return manifest


def _slug(workbook_id: str) -> str:
    value = re.sub(r"[^0-9A-Za-z가-힣_-]+", "_", workbook_id).strip("_-")
    return value.replace("-", "_") or "workbook"


def _build_directory(workbook_id: str) -> Path:
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    destination = ROOT / ".build" / "releases" / _slug(workbook_id) / f"{timestamp}-{uuid4().hex[:8]}"
    destination.mkdir(parents=True, exist_ok=False)
    return destination


def allocate_output_dir(base_name: str) -> Path:
    if (
        not base_name
        or Path(base_name).name != base_name
        or base_name in {".", ".."}
        or re.fullmatch(r"[0-9A-Za-z가-힣_-]+", base_name) is None
    ):
        raise ReleaseError("output base must be one safe folder name")
    root = ROOT / "outputs"
    root.mkdir(parents=True, exist_ok=True)
    base = root / base_name
    versions = [1] if base.exists() else []
    pattern = re.compile(rf"^{re.escape(base_name)}_v(\d+)$")
    for child in root.iterdir():
        match = pattern.fullmatch(child.name)
        if match:
            versions.append(int(match.group(1)))
    if not versions:
        return base
    return root / f"{base_name}_v{max(versions) + 1}"


def _sentence_ids(page: dict[str, Any]) -> list[str]:
    values = page.get("units") if page.get("mode") == "meaning" else page.get("items")
    if not isinstance(values, list):
        return []
    return [f"s{int(item.get('no')):03d}" for item in values if item.get("no") is not None]


def _applied_update_ids(canonical: dict[str, Any]) -> list[str]:
    values = canonical.get("updateState", {}).get("appliedUpdates", [])
    return [
        str(value.get("id")) if isinstance(value, dict) else str(value)
        for value in values
        if (isinstance(value, dict) and value.get("id")) or isinstance(value, str)
    ]


def _page_records(
    student_pages: list[dict[str, Any]],
    answer_pages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for edition, pages in (("student", student_pages), ("answer", answer_pages)):
        for page in pages:
            records.append(
                {
                    "id": f"{edition}:{page['pageId']}",
                    "edition": edition,
                    "page": page["pageNo"],
                    "pageId": page["pageId"],
                    "stageId": str(page.get("no", "")),
                    "part": page.get("part"),
                    "itemIds": _sentence_ids(page),
                    "digest": json_digest(page),
                }
            )
    return records


def _component_bundle(
    *,
    canonical: dict[str, Any],
    spec: dict[str, Any],
    versions: dict[str, Any],
    build_manifest: dict[str, Any],
    canonical_path: Path,
) -> ManifestBundle:
    current = versions["current"]
    canonical_component = {
        "contentVersion": canonical["contentVersion"],
        "workbookId": canonical["workbookId"],
        "canonical": canonical,
        **file_manifest((canonical_path,), root=ROOT),
    }
    spec_component = {
        "specVersion": current["specVersion"],
        "semanticRubricVersion": current["semanticRubricVersion"],
        "spec": spec,
        "schemaFiles": file_manifest((CANONICAL_SCHEMA_PATH, UPDATE_SCHEMA_PATH), root=ROOT)["files"],
        "semanticRubricFile": file_record(SEMANTIC_RUBRIC_PATH, root=ROOT),
        **file_manifest(
            (SPEC_PATH, VERSIONS_PATH, SEMANTIC_RUBRIC_PATH, CANONICAL_SCHEMA_PATH, UPDATE_SCHEMA_PATH),
            root=ROOT,
        ),
    }
    template_component = {
        "templateVersion": current["templateVersion"],
        "rendererContract": "shared-dom-explicit-targets-fail-closed",
        **file_manifest(TEMPLATE_PATHS, root=ROOT),
    }
    return ManifestBundle(
        canonical=canonical_component,
        spec=spec_component,
        template=template_component,
        build=build_manifest,
    )


def _artifact_records(build_dir: Path) -> list[dict[str, Any]]:
    paths = [build_dir / name for name in PUBLIC_FILENAMES]
    return [file_record(path, root=build_dir) for path in paths]


def _build_manifest(
    *,
    canonical: dict[str, Any],
    versions: dict[str, Any],
    student_pages: list[dict[str, Any]],
    answer_pages: list[dict[str, Any]],
    build_dir: Path,
    qa: ReleaseQA,
    built_at: str,
    validation_status: str,
) -> dict[str, Any]:
    current = versions["current"]
    sources = "\n".join(str(sentence["source"]) for sentence in canonical["sentences"])
    qa_data = qa.to_dict()
    for key in ("visualSamples", "contactSheets"):
        qa_data[key] = [
            Path(value).resolve().relative_to(build_dir.resolve()).as_posix()
            for value in qa_data.get(key, [])
        ]
    engine_inputs = file_manifest(ENGINE_INPUT_PATHS, root=ROOT)["files"]
    all_files = sorted(
        _artifact_records(build_dir) + engine_inputs,
        key=lambda record: str(record["path"]),
    )
    manifest = {
        "buildVersion": canonical["contentVersion"],
        "workbookId": canonical["workbookId"],
        "contentVersion": canonical["contentVersion"],
        "schemaVersion": canonical["schemaVersion"],
        "specVersion": canonical["specVersion"],
        "semanticRubricVersion": current["semanticRubricVersion"],
        "templateVersion": current["templateVersion"],
        "compilerVersion": ENGINE_VERSION,
        "reportFormatVersion": current["reportFormatVersion"],
        "appliedUpdates": _applied_update_ids(canonical),
        "sourceDigest": _sha256_bytes(sources.encode("utf-8")),
        "canonicalDigest": json_digest(canonical),
        "builtAt": built_at,
        "validationStatus": validation_status,
        "outputs": _artifact_records(build_dir),
        "pages": _page_records(student_pages, answer_pages),
        "qa": qa_data,
        "engineInputs": engine_inputs,
        "engineDigest": json_digest(engine_inputs),
        "files": all_files,
    }
    required = versions.get("buildManifestRequiredFields", [])
    missing = [key for key in required if key not in manifest]
    if missing:
        raise ReleaseError(f"build manifest is missing required fields: {missing}")
    return manifest


def _previous_bundle(workbook_id: str) -> ManifestBundle:
    path = ROOT / "reports" / "manifests" / f"{_slug(workbook_id)}-bundle.json"
    return load_bundle(path) if path.is_file() else ManifestBundle.empty()


def _render_update_index(update: Any, *, current_workbook_id: str) -> str:
    update_directory = ROOT / "reports" / "updates" / update.update_id
    existing = {
        path.stem for path in update_directory.glob("*.md")
    } if update_directory.is_dir() else set()
    current_slug = _slug(current_workbook_id)
    workbook_slugs = sorted(existing | {current_slug})
    lines = [
        f"# 업데이트 인덱스 `{update.update_id}`: {update.title}",
        "",
        update.summary,
        "",
        f"- 날짜: {update.date}",
        f"- 적용 범위: `{update.apply_to}`",
        "",
        "## 워크북별 상세 보고서",
        "",
    ]
    for slug in workbook_slugs:
        label = current_workbook_id if slug == current_slug else slug
        lines.append(f"- [{label}]({update.update_id}/{slug}.md)")
    return "\n".join(lines) + "\n"


def _enforce_update_scope(
    *,
    update: Any,
    workbook_id: str,
    previous: ManifestBundle,
    allow_manual_review: bool,
) -> None:
    if update.apply_to == "selected" and workbook_id not in update.selected_workbooks:
        raise ReleaseError(f"update {update.update_id} does not select workbook {workbook_id}")
    has_previous = any(bool(previous.component(name)) for name in ("canonical", "spec", "template", "build"))
    if update.apply_to == "new-only" and has_previous:
        raise ReleaseError(f"update {update.update_id} is new-only but this workbook already has a manifest")
    if update.apply_to == "manual-review" and not allow_manual_review:
        raise ReleaseError("manual-review update requires --allow-manual-review after explicit user approval")


def _enforce_version_transitions(
    *,
    previous: ManifestBundle,
    canonical: dict[str, Any],
    spec: dict[str, Any],
    versions: dict[str, Any],
) -> None:
    if not previous.canonical and not previous.spec and not previous.template and not previous.build:
        return
    previous_canonical = previous.canonical.get("canonical")
    if previous_canonical is not None and json_digest(previous_canonical) != json_digest(canonical):
        if previous.canonical.get("contentVersion") == canonical.get("contentVersion"):
            raise ReleaseError("canonical content changed without a contentVersion bump")

    current_versions = versions.get("current", {})
    previous_spec = previous.spec.get("spec")
    current_schema_files = file_manifest((CANONICAL_SCHEMA_PATH, UPDATE_SCHEMA_PATH), root=ROOT)["files"]
    spec_contract_changed = (
        previous_spec is not None
        and (
            json_digest(previous_spec) != json_digest(spec)
            or json_digest(previous.spec.get("schemaFiles", [])) != json_digest(current_schema_files)
        )
    )
    if spec_contract_changed and previous.spec.get("specVersion") == current_versions.get("specVersion"):
        raise ReleaseError("spec or schema changed without a specVersion bump")

    current_rubric = file_record(SEMANTIC_RUBRIC_PATH, root=ROOT)
    previous_rubric = previous.spec.get("semanticRubricFile")
    if previous_rubric and previous_rubric != current_rubric:
        if previous.spec.get("semanticRubricVersion") == current_versions.get("semanticRubricVersion"):
            raise ReleaseError("semantic rubric changed without a semanticRubricVersion bump")

    current_template_files = file_manifest(TEMPLATE_PATHS, root=ROOT)["files"]
    previous_template_files = previous.template.get("files")
    if previous_template_files and json_digest(previous_template_files) != json_digest(current_template_files):
        if previous.template.get("templateVersion") == current_versions.get("templateVersion"):
            raise ReleaseError("shared template changed without a templateVersion bump")

    current_engine = file_manifest(ENGINE_INPUT_PATHS, root=ROOT)["files"]
    previous_engine = previous.build.get("engineInputs")
    if previous_engine and json_digest(previous_engine) != json_digest(current_engine):
        if previous.build.get("compilerVersion") == ENGINE_VERSION:
            raise ReleaseError("workbook engine changed without a compilerVersion bump")


def prepare_release(
    canonical_path: Path,
    *,
    update_path: Path,
    output_base: str | None = None,
    allow_manual_review: bool = False,
) -> PreparedRelease:
    canonical_path = canonical_path.resolve()
    update_path = update_path.resolve()
    initial_input_digests = _input_digests(canonical_path, update_path)
    canonical = load_json(canonical_path)
    spec = load_spec(SPEC_PATH)
    versions = load_json(VERSIONS_PATH)
    update_value = load_json(update_path)
    update_schema_issues = validate_schema(update_value, load_json(UPDATE_SCHEMA_PATH))
    if update_schema_issues:
        raise ReleaseError("update JSON Schema failed:\n" + "\n".join(issue.format() for issue in update_schema_issues))
    update = load_update(update_path)
    schema_issues = validate_schema(canonical, load_json(CANONICAL_SCHEMA_PATH))
    if schema_issues:
        raise ReleaseError("canonical JSON Schema failed:\n" + "\n".join(issue.format() for issue in schema_issues))
    require_valid(validate_canonical(canonical, spec))

    previous = _previous_bundle(str(canonical["workbookId"]))
    _enforce_update_scope(
        update=update,
        workbook_id=str(canonical["workbookId"]),
        previous=previous,
        allow_manual_review=allow_manual_review,
    )
    _enforce_version_transitions(
        previous=previous,
        canonical=canonical,
        spec=spec,
        versions=versions,
    )
    applied_records = canonical.get("updateState", {}).get("appliedUpdates", [])
    applied = _applied_update_ids(canonical)
    if update.update_id not in applied:
        raise ReleaseError(f"canonical updateState does not include {update.update_id}")
    canonical_update = next(
        (
            value
            for value in applied_records
            if isinstance(value, dict) and str(value.get("id")) == update.update_id
        ),
        None,
    )
    if canonical_update and canonical_update.get("scope") != update.apply_to:
        raise ReleaseError("canonical applied update scope does not match the update definition")
    current = versions.get("current", {})
    if canonical.get("schemaVersion") != current.get("schemaVersion"):
        raise ReleaseError("canonical schemaVersion is not the registered current version")
    if canonical.get("specVersion") != current.get("specVersion"):
        raise ReleaseError("canonical specVersion is not the registered current version")
    if current.get("compilerVersion") != ENGINE_VERSION:
        raise ReleaseError("registered compilerVersion does not match workbook_engine")

    answer = compile_workbook(canonical, "answer", spec)
    build_dir = _build_directory(str(canonical["workbookId"]))
    layout_dir = build_dir / "layout"
    layout_dir.mkdir(parents=True)
    draft_answer_html = write_html(answer, layout_dir / "answer-measure.html")
    measured_layouts = measure_answer_layouts(
        draft_answer_html,
        expected_pages=len(answer["pages"]),
        profile_root=layout_dir / "chrome-profiles",
    )
    answer = lock_response_layout(answer, measured_layouts["responses"])
    answer = lock_solution_slot_layouts(answer, measured_layouts["solutionSlots"])
    student = project_student_workbook(
        answer,
        expected_sentences=len(canonical["sentences"]),
    )
    if len(student["pages"]) != len(answer["pages"]):
        raise ReleaseError("student and answer compiled page counts differ")

    # The draft HTML and browser profiles are measurement-only intermediates.
    # Keep the final compiled artifacts and QA evidence, not disposable state.
    shutil.rmtree(layout_dir)

    inputs_dir = build_dir / "inputs"
    inputs_dir.mkdir(parents=True)
    write_json(inputs_dir / "canonical.json", canonical)
    write_json(inputs_dir / "update.json", update_value)
    write_json(inputs_dir / "workbook-spec.json", spec)
    write_json(inputs_dir / "versions.json", versions)
    compiled_dir = build_dir / "compiled"
    compiled_dir.mkdir(parents=True)
    (compiled_dir / "student.json").write_text(canonical_json(student, pretty=True), encoding="utf-8")
    (compiled_dir / "answer.json").write_text(canonical_json(answer, pretty=True), encoding="utf-8")

    student_html = write_html(student, build_dir / "문제.html")
    answer_html = write_html(answer, build_dir / "해설.html")
    student_pdf = build_dir / "문제.pdf"
    answer_pdf = build_dir / "해설.pdf"
    qa = run_release_qa(
        student_html=student_html,
        answer_html=answer_html,
        student_pdf=student_pdf,
        answer_pdf=answer_pdf,
        pages=student["pages"],
        qa_root=build_dir / "qa",
    )
    shutil.rmtree(build_dir / "qa" / "chrome-profiles", ignore_errors=True)
    write_json(build_dir / "qa" / "qa.json", qa.to_dict())
    final_input_digests = _input_digests(canonical_path, update_path)
    if final_input_digests != initial_input_digests:
        changed = sorted(
            path
            for path in set(final_input_digests) | set(initial_input_digests)
            if final_input_digests.get(path) != initial_input_digests.get(path)
        )
        raise ReleaseError(
            "release inputs changed during prepare; discard this build: " + ", ".join(changed)
        )

    built_at = _now()
    build_manifest = _build_manifest(
        canonical=canonical,
        versions=versions,
        student_pages=student["pages"],
        answer_pages=answer["pages"],
        build_dir=build_dir,
        qa=qa,
        built_at=built_at,
        validation_status="automated-passed-awaiting-visual-review",
    )
    bundle = _component_bundle(
        canonical=canonical,
        spec=spec,
        versions=versions,
        build_manifest=build_manifest,
        canonical_path=canonical_path,
    )
    before = previous
    report = compare_bundles(before, bundle, update)
    write_bundle(build_dir / "before-bundle.json", before)
    write_bundle(build_dir / "after-bundle.json", bundle)
    write_json(build_dir / "build-manifest.json", build_manifest)
    write_report(build_dir / f"{update.update_id}.md", report)

    state = {
        "stateVersion": 1,
        "status": "awaiting-visual-review",
        "workbookId": canonical["workbookId"],
        "canonicalPath": str(canonical_path),
        "updatePath": str(update_path.resolve()),
        "updateId": update.update_id,
        "outputBase": output_base or _slug(str(canonical["workbookId"])),
        "builtAt": built_at,
        "pageCount": len(student["pages"]),
        "artifacts": {
            name: {"sha256": _sha256_file(build_dir / name), "size": (build_dir / name).stat().st_size}
            for name in PUBLIC_FILENAMES
        },
        "contactSheets": qa.contact_sheets,
        "inputDigests": initial_input_digests,
    }
    state_path = build_dir / "release-state.json"
    write_json(state_path, state)
    return PreparedRelease(
        build_dir=build_dir,
        state_path=state_path,
        student_html=student_html,
        student_pdf=student_pdf,
        answer_html=answer_html,
        answer_pdf=answer_pdf,
        contact_sheets=tuple(Path(path) for path in qa.contact_sheets),
        page_count=len(student["pages"]),
    )


def _verify_prepared_artifacts(build_dir: Path, state: dict[str, Any]) -> None:
    records = state.get("artifacts", {})
    for name in PUBLIC_FILENAMES:
        path = build_dir / name
        record = records.get(name, {})
        if not path.is_file():
            raise ReleaseError(f"prepared artifact is missing: {name}")
        if _sha256_file(path) != record.get("sha256") or path.stat().st_size != record.get("size"):
            raise ReleaseError(f"prepared artifact changed after QA: {name}")


def publish_release(
    build_dir: Path,
    *,
    reviewer: str,
    notes: str,
) -> PublishedRelease:
    build_dir = build_dir.resolve()
    state_path = build_dir / "release-state.json"
    if not state_path.is_file():
        raise ReleaseError("release-state.json was not found")
    state = load_json(state_path)
    if state.get("status") != "awaiting-visual-review":
        raise ReleaseError(f"release is not publishable: {state.get('status')}")
    if not reviewer.strip() or not notes.strip():
        raise ReleaseError("visual reviewer and notes are required")
    _verify_prepared_artifacts(build_dir, state)
    current_inputs = _input_digests(Path(state["canonicalPath"]), Path(state["updatePath"]))
    if current_inputs != state.get("inputDigests"):
        changed = sorted(
            path
            for path in set(current_inputs) | set(state.get("inputDigests", {}))
            if current_inputs.get(path) != state.get("inputDigests", {}).get(path)
        )
        raise ReleaseError(
            "release inputs changed after prepare; prepare a new build: " + ", ".join(changed)
        )

    update = load_update(build_dir / "inputs" / "update.json")
    build_manifest = load_json(build_dir / "build-manifest.json")
    build_manifest["validationStatus"] = "passed"
    build_manifest["visualReview"] = {
        "status": "passed",
        "reviewer": reviewer.strip(),
        "notes": notes.strip(),
        "reviewedAt": _now(),
    }
    prepared_bundle = load_bundle(build_dir / "after-bundle.json")
    bundle = ManifestBundle(
        canonical=prepared_bundle.canonical,
        spec=prepared_bundle.spec,
        template=prepared_bundle.template,
        build=build_manifest,
    )
    before = load_bundle(build_dir / "before-bundle.json")
    report = compare_bundles(before, bundle, update)

    reports = ROOT / "reports"
    aggregate_report_path = reports / "updates" / f"{update.update_id}.md"
    report_path = reports / "updates" / update.update_id / f"{_slug(str(state['workbookId']))}.md"
    manifest_dir = reports / "manifests"
    build_manifest_path = manifest_dir / f"{_slug(str(state['workbookId']))}-build.json"
    bundle_path = manifest_dir / f"{_slug(str(state['workbookId']))}-bundle.json"
    changelog_path = ROOT / "CHANGELOG.md"
    transaction_id = uuid4().hex[:8]
    metadata_pairs: list[tuple[Path, Path]] = []
    for destination in (report_path, aggregate_report_path, build_manifest_path, bundle_path, changelog_path):
        destination.parent.mkdir(parents=True, exist_ok=True)
    report_temp = report_path.parent / f".{report_path.name}.tmp-{transaction_id}"
    aggregate_temp = aggregate_report_path.parent / f".{aggregate_report_path.name}.tmp-{transaction_id}"
    manifest_temp = build_manifest_path.parent / f".{build_manifest_path.name}.tmp-{transaction_id}"
    bundle_temp = bundle_path.parent / f".{bundle_path.name}.tmp-{transaction_id}"
    changelog_temp = changelog_path.parent / f".{changelog_path.name}.tmp-{transaction_id}"
    write_report(report_temp, report)
    aggregate_temp.write_text(
        _render_update_index(update, current_workbook_id=str(state["workbookId"])),
        encoding="utf-8",
    )
    write_json(manifest_temp, build_manifest)
    write_bundle(bundle_temp, bundle)
    if changelog_path.is_file():
        shutil.copy2(changelog_path, changelog_temp)
    update_changelog(changelog_temp, report, report_path=aggregate_report_path)
    metadata_pairs.extend(
        (
            (report_temp, report_path),
            (aggregate_temp, aggregate_report_path),
            (manifest_temp, build_manifest_path),
            (bundle_temp, bundle_path),
            (changelog_temp, changelog_path),
        )
    )

    output_dir = allocate_output_dir(str(state["outputBase"]))
    temporary = output_dir.parent / f".{output_dir.name}.tmp-{uuid4().hex[:8]}"
    temporary.mkdir(parents=False, exist_ok=False)
    output_committed = False
    metadata_committed: list[Path] = []
    backup_dir = build_dir / "publish-backups"
    backups: dict[Path, Path] = {}
    try:
        for name in PUBLIC_FILENAMES:
            _copy_public_artifact(build_dir / name, temporary / name)
        for name in PUBLIC_FILENAMES:
            source = build_dir / name
            copied = temporary / name
            if _sha256_file(source) != _sha256_file(copied):
                raise ReleaseError(f"atomic publish copy verification failed: {name}")
        second_inputs = _input_digests(Path(state["canonicalPath"]), Path(state["updatePath"]))
        if second_inputs != state.get("inputDigests"):
            raise ReleaseError("release inputs changed while publishing; prepare a new build")
        if output_dir.exists():
            raise ReleaseError(f"output destination appeared during release: {output_dir}")
        os.replace(temporary, output_dir)
        output_committed = True
        backup_dir.mkdir(exist_ok=True)
        for index, (source, destination) in enumerate(metadata_pairs):
            if destination.exists():
                backup = backup_dir / f"{index:02d}-{destination.name}"
                shutil.copy2(destination, backup)
                backups[destination] = backup
            os.replace(source, destination)
            metadata_committed.append(destination)
    except Exception:
        for destination in reversed(metadata_committed):
            backup = backups.get(destination)
            if backup and backup.exists():
                os.replace(backup, destination)
            elif destination.exists():
                destination.unlink()
        if output_committed and output_dir.exists():
            shutil.rmtree(output_dir)
        raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
        for source, _destination in metadata_pairs:
            if source.exists():
                source.unlink()
        if backup_dir.exists():
            shutil.rmtree(backup_dir)

    state.update(
        {
            "status": "published",
            "publishedAt": _now(),
            "outputDir": str(output_dir),
            "visualReview": build_manifest["visualReview"],
        }
    )
    write_json(state_path, state)
    write_json(build_dir / "build-manifest.json", build_manifest)
    write_bundle(build_dir / "after-bundle.json", bundle)
    write_report(build_dir / f"{update.update_id}.md", report)
    return PublishedRelease(
        output_dir=output_dir,
        report_path=report_path,
        aggregate_report_path=aggregate_report_path,
        build_manifest_path=build_manifest_path,
        bundle_path=bundle_path,
    )
