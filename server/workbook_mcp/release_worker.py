"""One private release job per process; the rendering engine stays byte-identical."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import direct_release
from .runtime_entry import bind_workspace
from workbook_engine.release import ReleaseError

_SCHEMA_LINE = re.compile(r"^\[SCHEMA\] (?P<path>[^:]+): (?P<message>.+)$")
_ISSUE_LINE = re.compile(r"^\[(?:ERROR|WARNING)\] (?P<code>\S+) (?P<path>[^:]+): (?P<message>.+)$")


def _field(prefix: str, path: str) -> str:
    path = path.strip()
    if path.startswith("$"):
        return prefix + path[1:] if path != "$" else prefix
    return f"{prefix}.{path}" if path else prefix


def violations_from_message(message: str, prefix: str) -> list[dict]:
    """Turn engine issue lines into ``{field, message}`` violations."""
    items = []
    for line in message.splitlines():
        line = line.strip()
        match = _SCHEMA_LINE.match(line)
        if match:
            items.append({"field": _field(prefix, match["path"]), "message": match["message"]})
            continue
        match = _ISSUE_LINE.match(line)
        if match:
            items.append({"field": _field(prefix, match["path"]), "message": f"{match['code']}: {match['message']}"})
    return items or [{"field": prefix, "message": message.strip()[:2000] or "invalid"}]


def classify(error: Exception) -> direct_release.ExpectedReleaseError | None:
    """Map expected engine failures to envelope statuses; None means unexpected."""
    from workbook_engine.qa import QualityGateError
    from workbook_engine.render import RenderBuildError
    from workbook_engine.validator import ValidationFailure

    if isinstance(error, direct_release.ExpectedReleaseError):
        return error
    message = str(error)
    if isinstance(error, ValidationFailure):
        return direct_release.ExpectedReleaseError(message, violations=[
            {"field": _field("canonical", issue.path), "message": f"{issue.code}: {issue.message}"}
            for issue in error.issues] or None, field="canonical")
    if isinstance(error, ReleaseError):
        for prefix in ("update", "canonical"):
            if message.startswith(f"{prefix} JSON Schema failed"):
                return direct_release.ExpectedReleaseError(
                    message, violations=violations_from_message(message, prefix))
        return direct_release.ExpectedReleaseError(message, status="rejected", field="release")
    if isinstance(error, (QualityGateError, RenderBuildError)):
        return direct_release.ExpectedReleaseError(message, status="rejected", field="qa")
    if isinstance(error, ValueError):
        return direct_release.ExpectedReleaseError(message, field="update" if "update" in message else "canonical")
    return None


def main() -> None:
    job_path = Path(sys.argv[1]).resolve()
    job = json.loads(job_path.read_text(encoding="utf-8"))
    workspace = job_path.parent
    bind_workspace(workspace)
    direct_release.ROOT = workspace
    owner_id = direct_release._owner(job["owner_id"])
    try:
        if job["action"] == "prepare":
            workbook_id = str(job["canonical"].get("workbookId", ""))
        elif job["action"] == "publish":
            archive, metadata = direct_release._load_archive(direct_release._store(), job["release_id"])
            archive.close()
            direct_release._require_owner(metadata, owner_id)
            workbook_id = metadata["workbookId"]
        else:
            raise ValueError("Unknown release operation")
        with direct_release._release_lock(direct_release._store(), owner_id, workbook_id):
            if job["action"] == "prepare":
                result = direct_release._prepare(job["canonical"], job["update"], job.get("output_base"), owner_id=owner_id)
            else:
                result = direct_release._publish(job["release_id"], job["reviewer"], job["notes"], owner_id=owner_id)
        value = {"result": result}
    except Exception as error:
        # Validation, QA and review-gate messages remain actionable; anything else
        # fails the worker so FastMCP masks it. Payloads and credentials are never logged.
        expected = classify(error)
        if expected is None:
            raise
        value = expected.to_dict()
    finally:
        direct_release.close_storage_clients()
    (workspace / "result.json").write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
