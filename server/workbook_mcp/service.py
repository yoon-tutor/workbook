"""Tool logic: every function returns the standard envelope (STANDARD.md 6.4).

``tools.py`` is a thin adapter. Expected input and release-gate failures become
``invalid_input``/``rejected`` envelopes; only unexpected failures raise.
"""

from __future__ import annotations

import json
import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from shared_mcp_runtime import artifacts as bundles
from shared_mcp_runtime.envelope import envelope, next_action, violation

from . import direct_release
from .bundle import ROOT as SERVER, engine_identity

REPO = SERVER.parent
PUBLIC_FILES = direct_release.PUBLIC_FILES
RULE_FILES = ("docs/authoring-pipeline.md", "docs/semantic-rubric.md", "config/workbook-spec.json",
              "schemas/canonical-workbook.schema.json", "schemas/update.schema.json")
WORKFLOW = ("workbook_get_guidance", "workbook_authoring_verify", "workbook_authoring_expand",
            "workbook_validate_canonical", "workbook_prepare_release", "workbook_review_image",
            "workbook_publish_release", "workbook_get_artifacts")


def _version() -> str:
    value = os.environ.get("SERVICE_VERSION", "").strip()
    if value:
        return value
    path = REPO / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else "0.0.0"


SERVICE = {"name": "workbook-maker", "version": _version()}


def _reply(status: str, stage: str, **kwargs: Any) -> dict[str, Any]:
    return envelope(status, service=SERVICE, stage=stage, **kwargs)


def _invalid(stage: str, violations: list[dict], instruction: str, tool: str | None = None) -> dict[str, Any]:
    return _reply("invalid_input", stage, violations=violations, next_action=next_action(instruction, tool))


def _review_action(release_id: str, remaining: list[str]) -> dict[str, Any]:
    if remaining:
        return next_action(
            f"남은 검수 이미지 {len(remaining)}개를 하나씩 받아 직접 연다: " + ", ".join(remaining)
            + ". 각 호출에 --into로 빈 .work/review/<release_id>/ 폴더를 지정한다.",
            "workbook_review_image", {"release_id": release_id, "image_name": remaining[0]})
    return next_action(
        "모든 검수 이미지를 열었다. 실제로 확인한 결함 여부를 notes에 적어 공개한다. "
        "결함이 있으면 공개하지 말고 정본을 고쳐 다시 prepare한다.",
        "workbook_publish_release", {"release_id": release_id})


def _expected(stage: str) -> Callable:
    """Turn expected release errors into envelopes for one release tool."""
    def decorate(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
            try:
                return function(*args, **kwargs)
            except FileNotFoundError:
                error = direct_release.unavailable()
            except direct_release.ExpectedReleaseError as caught:
                error = caught
            if error.missing_images and kwargs.get("release_id"):
                action = _review_action(kwargs["release_id"], error.missing_images)
            elif error.status == "rejected":
                action = next_action("violations의 원인을 해결한 뒤 같은 단계부터 다시 진행한다. "
                                     "정본이나 update를 고쳤다면 다시 prepare한다.", "workbook_prepare_release")
            else:
                action = next_action("violations의 field를 고친 뒤 다시 호출한다.")
            return _reply(error.status, stage, violations=error.violations, next_action=action)
        return wrapper
    return decorate


# ------------------------------------------------------------------ guidance & validation

def guidance() -> dict[str, Any]:
    data = {
        "engineId": engine_identity()["engineId"],
        "publicFiles": list(PUBLIC_FILES),
        "workflow": list(WORKFLOW),
        "rules": {name: (SERVER / name).read_text(encoding="utf-8") for name in RULE_FILES},
        "stage9Authoring": {
            "choiceLabels": "선택지 표시는 위에서부터 A, B, C 순서다. 섞을 내용은 blocks에 그 순서로 넣는다.",
            "coverage": "매 문항의 지문 전체 문장을 이동 가능한 blocks에 빠짐없이 한 번씩 넣는다.",
            "answerKey": "answerOrder는 원문을 복원하는 선택지 순서다. 이미 A-B-C로 놓인 무의미한 배열 문제를 만들지 않는다.",
            "questionSet": "여러 문항은 가능한 범위에서 정답 순열이 서로 다르게 되도록 설계한다.",
            "verification": "새 packet의 authoring verify와 expand에서 위반을 거부하며 기존 공개본은 변경하지 않는다.",
        },
        "review": ("prepare는 자동 브라우저·PDF QA만 통과한 상태다. reviewImages의 모든 이미지를 받아 직접 열고 "
                   "2·3단계 빈칸, 4·8·10단계 작성형, 학생용 정답 노출, 해설 정답, 잘림·겹침을 확인한 뒤 공개한다."),
    }
    return _reply("ok", "guidance", data=data, next_action=next_action(
        "rules에 따라 authoring packet을 작성한 뒤 검증한다.", "workbook_authoring_verify"))


def _schema_violations(canonical: Any) -> list[dict]:
    from workbook_engine.schema_gate import validate_schema
    schema = json.loads((SERVER / "schemas/canonical-workbook.schema.json").read_text(encoding="utf-8"))
    from .release_worker import _field
    return [violation(_field("canonical", issue.path), issue.message)
            for issue in validate_schema(canonical, schema)]


def validate_canonical(canonical: dict) -> dict[str, Any]:
    from workbook_engine.validator import load_spec, validate_canonical as check
    from .release_worker import _field
    problems = _schema_violations(canonical)
    if problems:
        return _invalid("validate", problems, "canonical을 스키마에 맞게 고친 뒤 다시 검사한다.",
                        "workbook_validate_canonical")
    issues = check(canonical, load_spec())
    errors = [violation(_field("canonical", issue.path), f"{issue.code}: {issue.message}")
              for issue in issues if issue.severity == "error"]
    if errors:
        return _invalid("validate", errors, "violations의 문장·활동만 고친 뒤 다시 검사한다.",
                        "workbook_validate_canonical")
    data = {"valid": True, "workbookId": canonical.get("workbookId"),
            "sentences": len(canonical.get("sentences", [])),
            "warnings": [issue.format() for issue in issues if issue.severity != "error"]}
    return _reply("ok", "validate", data=data, next_action=next_action(
        "같은 canonical과 update JSON으로 PDF 릴리스를 준비한다.", "workbook_prepare_release"))


# ------------------------------------------------------------------ authoring

def _authoring(packet: dict, stage: str) -> tuple[dict | None, dict | None]:
    from workbook_authoring import AuthoringPacketError, expand_packet, verify_new_packet_policy
    from workbook_engine.validator import ValidationFailure
    from .release_worker import _field
    try:
        verify_new_packet_policy(packet)
        return expand_packet(packet), None
    except ValidationFailure as error:
        # The expanded canonical broke an engine rule; report each issue instead of a masked tool error.
        problems = [violation(_field("packet", issue.path), f"{issue.code}: {issue.message}")
                    for issue in error.issues] or [violation("packet", str(error)[:2000])]
    except AuthoringPacketError as error:
        path, separator, message = str(error).partition(": ")
        field = "packet." + path if separator and " " not in path else "packet"
        problems = [violation(field, message if separator and field != "packet" else str(error))]
    except (ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        problems = [violation("packet", f"packet structure is invalid ({type(error).__name__}: {error})"[:2000])]
    return None, _invalid(stage, problems, "rules의 authoring pipeline에 맞게 packet을 고친 뒤 다시 검증한다.",
                          "workbook_authoring_verify")


def authoring_verify(packet: dict) -> dict[str, Any]:
    canonical, failure = _authoring(packet, "authoring_verify")
    if failure:
        return failure
    data = {"valid": True, "workbookId": canonical["workbookId"], "sentences": len(canonical["sentences"]),
            "engineId": engine_identity()["engineId"]}
    return _reply("ok", "authoring_verify", data=data, next_action=next_action(
        "같은 packet을 확장해 정본 content.json을 받는다. 미리 만든 빈 workbooks/<이름>/ 폴더를 --into로 지정한다.",
        "workbook_authoring_expand"))


def authoring_expand(packet: dict) -> dict[str, Any]:
    canonical, failure = _authoring(packet, "authoring_expand")
    if failure:
        return failure
    text = json.dumps(canonical, ensure_ascii=False, indent=2) + "\n"
    job = str(canonical.get("workbookId") or "workbook")
    data = {"workbookId": canonical["workbookId"], "sentences": len(canonical["sentences"]),
            "engineId": engine_identity()["engineId"]}
    return _reply("ok", "authoring_expand", data=data,
                  artifacts=bundles.bundle(job, [bundles.file_entry("content.json", text)]),
                  next_action=next_action(
                      "저장된 content.json을 workbook_validate_canonical로 다시 검사한다. 기존 검토 정본을 덮어쓰지 않는다.",
                      "workbook_validate_canonical"))


def compile_edition(canonical: dict, edition: str) -> dict[str, Any]:
    from workbook_engine.compiler import compile_workbook
    problems = _schema_violations(canonical)
    if problems:
        return _invalid("compile", problems, "canonical을 스키마에 맞게 고친 뒤 다시 호출한다.",
                        "workbook_validate_canonical")
    try:
        compiled = compile_workbook(canonical, edition)
    except (ValueError, KeyError, TypeError) as error:
        return _invalid("compile", [violation("canonical", f"{type(error).__name__}: {error}"[:2000])],
                        "workbook_validate_canonical로 정본을 먼저 검사한다.", "workbook_validate_canonical")
    return _reply("ok", "compile", data={"edition": edition, "pageCount": len(compiled.get("pages", [])),
                                         "ir": compiled},
                  next_action=next_action("중간 IR은 점검용이다. 공개용 결과는 prepare·검수·publish로만 만든다.",
                                          "workbook_prepare_release"))


# ------------------------------------------------------------------ releases

PREPARE_KEYS = ("releaseId", "workbookId", "pageCount", "reviewImages", "qa")


@_expected("prepare")
def prepare_release(canonical: dict, update: dict, output_base: str | None, *, owner_id: str) -> dict[str, Any]:
    result = direct_release.prepare(canonical, update, output_base, owner_id=owner_id)
    data = {key: result[key] for key in PREPARE_KEYS if key in result}
    data["releaseStatus"] = result.get("status", "awaiting-visual-review")
    return _reply("needs_review", "prepare", data=data,
                  next_action=_review_action(result["releaseId"], list(result["reviewImages"])))


def _image_entry(release_id: str, image_name: str, data: bytes) -> dict[str, Any]:
    if len(data) <= bundles.INLINE_LIMIT:
        return bundles.file_entry(image_name, data)
    url, expires_at = direct_release.review_image_link(release_id, image_name)
    from hashlib import sha256
    return bundles.url_entry(image_name, url=url, sha256=sha256(data).hexdigest(), size=len(data),
                             expires_at=expires_at)


@_expected("review")
def review_image(*, release_id: str, image_name: str, owner_id: str) -> dict[str, Any]:
    result = direct_release.review_image(release_id, image_name, owner_id=owner_id)
    data = {"releaseId": release_id, "imageName": image_name, "reviewImages": result["reviewImages"],
            "remaining": result["remaining"]}
    bundle = bundles.bundle(f"review-{release_id}", [_image_entry(release_id, image_name, result["data"])])
    return _reply("needs_review", "review", data=data, artifacts=bundle,
                  next_action=_review_action(release_id, result["remaining"]))


def _inline_max() -> int:
    try:
        return max(0, min(int(os.environ.get("WORKBOOK_ARTIFACT_INLINE_MAX_BYTES", "0")), bundles.INLINE_LIMIT))
    except ValueError:
        return 0


def _public_bundle(release_id: str, metadata: dict, names: tuple[str, ...], inline_max: int,
                   owner_id: str) -> dict[str, Any]:
    entries = []
    for name in names:
        record = metadata["files"][name]
        if record["size"] <= inline_max:
            entries.append(bundles.file_entry(name, direct_release.read_public_file(
                release_id, name, owner_id=owner_id)))
        else:
            url, expires_at = direct_release.artifact_link(release_id, name)
            entries.append(bundles.url_entry(name, url=url, sha256=record["sha256"], size=record["size"],
                                             expires_at=expires_at))
    job = str(metadata.get("outputDirName") or metadata.get("workbookId") or release_id)
    return bundles.bundle(job, entries)


PUBLIC_KEYS = ("releaseId", "workbookId", "updateId", "outputDirName", "pageCount", "files", "reviewer")


def _published_data(metadata: dict) -> dict[str, Any]:
    data = {key: metadata[key] for key in PUBLIC_KEYS if key in metadata}
    data["releaseStatus"] = metadata.get("status", "published")
    return data


@_expected("publish")
def publish_release(*, release_id: str, reviewer: str, notes: str, owner_id: str) -> dict[str, Any]:
    direct_release.publish(release_id, reviewer, notes, owner_id=owner_id)
    metadata = direct_release.published(release_id, owner_id=owner_id)
    return _reply("done", "publish", data=_published_data(metadata),
                  artifacts=_public_bundle(release_id, metadata, PUBLIC_FILES, _inline_max(), owner_id),
                  next_action=next_action(
                      "클라이언트가 검증해 저장한 네 파일(saved_to)을 확인한다. 링크가 만료되면 workbook_get_artifacts로 다시 받는다."))


@_expected("artifacts")
def get_artifacts(*, release_id: str, owner_id: str) -> dict[str, Any]:
    metadata = direct_release.published(release_id, owner_id=owner_id)
    return _reply("done", "artifacts", data=_published_data(metadata),
                  artifacts=_public_bundle(release_id, metadata, PUBLIC_FILES, _inline_max(), owner_id),
                  next_action=next_action("클라이언트가 검증해 저장한 네 파일(saved_to)을 확인한다."))


@_expected("artifacts")
def read_artifact(*, release_id: str, name: str, owner_id: str) -> dict[str, Any]:
    metadata = direct_release.published(release_id, owner_id=owner_id)
    return _reply("ok", "artifacts", data=_published_data(metadata),
                  artifacts=_public_bundle(release_id, metadata, (name,), bundles.INLINE_LIMIT, owner_id))
