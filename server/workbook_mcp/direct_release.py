"""Persistent, private two-phase PDF releases for the direct MCP API."""

from __future__ import annotations

import hmac
import io
import json
import os
import re
import shutil
import time
import zipfile
import subprocess
import sys
import tempfile
import signal
import anyio
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import lru_cache
from hashlib import sha256
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from uuid import uuid4

from starlette.requests import Request
from starlette.responses import Response


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ("문제.html", "문제.pdf", "해설.html", "해설.pdf")
RELEASE_ID = re.compile(r"[0-9a-f]{32}\Z")
REVIEW_IMAGE = re.compile(r"[0-9A-Za-z._-]{1,120}\.png\Z")
LINK_LIFETIME = 24 * 60 * 60
_STORAGE_CLIENTS: list = []


class ExpectedReleaseError(ValueError):
    """Actionable input or gate failure that becomes an envelope, never a ToolError.

    ``status`` is ``invalid_input`` (wrong input) or ``rejected`` (well formed but
    blocked by a release gate). ``violations`` are ``{field, message}`` items.
    """

    def __init__(self, message: str, *, status: str = "invalid_input", field: str = "request",
                 violations: list[dict] | None = None, missing_images: list[str] | None = None):
        super().__init__(message)
        self.status = status
        self.violations = violations or [{"field": field, "message": message}]
        self.missing_images = list(missing_images or [])

    def to_dict(self) -> dict:
        return {"error": str(self), "status": self.status, "violations": self.violations,
                "missingImages": self.missing_images}

    @classmethod
    def from_dict(cls, value: dict) -> "ExpectedReleaseError":
        status = value.get("status") if value.get("status") in {"invalid_input", "rejected"} else "invalid_input"
        violations = [item for item in value.get("violations") or [] if isinstance(item, dict)]
        return cls(str(value.get("error") or "Release request failed"), status=status,
                   violations=violations or None, missing_images=value.get("missingImages"))


def unavailable() -> ExpectedReleaseError:
    return ExpectedReleaseError("Release is unavailable for this user; verify the release ID",
                                field="release_id")


class _LocalStore:
    """Test-only storage; production must set WORKBOOK_RELEASE_BUCKET."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    def _path(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Invalid storage key")
        return path

    def read(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def put(self, key: str, data: bytes, *, create_only: bool = False) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        if create_only:
            with path.open("xb") as stream:
                stream.write(data)
        else:
            temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
            temporary.write_bytes(data)
            os.replace(temporary, path)

    def list(self, prefix: str) -> list[str]:
        path = self._path(prefix)
        return [item.relative_to(self.root).as_posix() for item in path.rglob("*") if item.is_file()] if path.is_dir() else []

    def delete(self, key: str) -> None:
        self._path(key).unlink()


class _CloudStore:
    def __init__(self, name: str):
        from google.cloud import storage

        self.client = storage.Client()
        _STORAGE_CLIENTS.append(self.client)
        self.bucket = self.client.bucket(name)

    def read(self, key: str) -> bytes:
        try:
            return self.bucket.blob(key).download_as_bytes()
        except Exception as error:
            # Normalise a missing object so every caller can treat it as unavailable.
            if type(error).__name__ == "NotFound":
                raise FileNotFoundError(key) from None
            raise

    def put(self, key: str, data: bytes, *, create_only: bool = False) -> None:
        self.bucket.blob(key).upload_from_string(
            data, if_generation_match=0 if create_only else None,
        )

    def list(self, prefix: str) -> list[str]:
        return [blob.name for blob in self.bucket.list_blobs(prefix=prefix)]

    def delete(self, key: str) -> None:
        self.bucket.blob(key).delete()


@lru_cache(maxsize=4)
def _cloud_store(name: str):
    return _CloudStore(name)


def close_storage_clients() -> None:
    """Clear cached clients at process shutdown (HTTP pools otherwise live for the process)."""
    while _STORAGE_CLIENTS:
        _STORAGE_CLIENTS.pop().close()
    _cloud_store.cache_clear()


def _store():
    bucket = os.environ.get("WORKBOOK_RELEASE_BUCKET", "").strip()
    if bucket:
        return _cloud_store(bucket)
    local = os.environ.get("WORKBOOK_RELEASE_LOCAL_STORE", "").strip()
    if local:
        return _LocalStore(Path(local))
    raise RuntimeError("WORKBOOK_RELEASE_BUCKET is required for PDF releases")


def _id(value: str) -> str:
    if not isinstance(value, str) or not RELEASE_ID.fullmatch(value):
        raise ExpectedReleaseError("Invalid release ID", field="release_id")
    return value


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def _owner(value: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 512:
        raise ValueError("Authenticated user identity is required")
    return value


def _require_owner(metadata: dict, owner_id: str) -> None:
    if metadata.get("ownerId") != _owner(owner_id):
        # Legacy records have no owner. Administrators must explicitly assign a
        # verified owner; the first caller must never acquire ownership.
        raise ExpectedReleaseError(
            "Release is unavailable for this user; contact the administrator if ownership needs migration",
            field="release_id")


class _TenantHistoryStore:
    """History and release locks are separated even when workbook IDs are equal."""

    def __init__(self, store, owner_id: str):
        self.store = store
        self.prefix = "tenants/" + sha256(_owner(owner_id).encode("utf-8")).hexdigest() + "/"

    def read(self, key: str) -> bytes:
        return self.store.read(self.prefix + key)

    def put(self, key: str, data: bytes, *, create_only: bool = False) -> None:
        self.store.put(self.prefix + key, data, create_only=create_only)

    def list(self, prefix: str) -> list[str]:
        return [key.removeprefix(self.prefix) for key in self.store.list(self.prefix + prefix)]

    def delete(self, key: str) -> None:
        self.store.delete(self.prefix + key)


@contextmanager
def _release_lock(store, owner_id: str, workbook_id: str):
    """Create-only storage lock also serializes publication across Cloud Run instances.

    A crashed worker leaves a lock for explicit administrator recovery. Automatically
    expiring an active lock would allow two publishers to overwrite the same history.
    """
    history = _TenantHistoryStore(store, owner_id)
    key = "locks/" + sha256(workbook_id.encode("utf-8")).hexdigest() + ".json"
    lock = _json_bytes({"jobId": uuid4().hex, "createdAt": int(time.time())})
    try:
        history.put(key, lock, create_only=True)
    except Exception as error:
        if isinstance(error, FileExistsError) or type(error).__name__ in {"PreconditionFailed", "Conflict"}:
            raise ExpectedReleaseError(
                "Another release job is running for this workbook; retry after it completes",
                status="rejected", field="workbookId") from None
        raise
    try:
        yield history
    finally:
        if history.read(key) == lock:
            history.delete(key)


def _run_worker(action: str, payload: dict) -> dict:
    """Run the unchanged engine in a clean per-job workspace and reclaim all local files."""
    with tempfile.TemporaryDirectory(prefix="workbook-release-") as directory:
        workspace = Path(directory)
        job = workspace / "job.json"
        job.write_bytes(_json_bytes({"action": action, **payload}))
        process = subprocess.Popen(
                [sys.executable, "-X", "utf8", "-m", "workbook_mcp.release_worker", str(job)],
                cwd=Path(__file__).resolve().parents[1], stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                start_new_session=os.name != "nt",
                creationflags=(subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0,
            )
        try:
            process.communicate(timeout=1800)
        except subprocess.TimeoutExpired:
            # Reclaim Chromium descendants as well as the Python worker.
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.kill()
            process.communicate()
            raise RuntimeError("Release job timed out; ask the administrator to check its storage lock before retrying") from None
        response = workspace / "result.json"
        if process.returncode or not response.is_file():
            raise RuntimeError("Release worker failed; inspect server diagnostics and retry")
        value = json.loads(response.read_text(encoding="utf-8"))
        if value.get("error"):
            raise ExpectedReleaseError.from_dict(value)
        return value["result"]


def _restore_history(store, workbook_id: str) -> str | None:
    from workbook_engine.release import _slug

    slug = _slug(workbook_id)
    key = f"history/{slug}/bundle.json"
    if key in store.list(f"history/{slug}/"):
        data = store.read(key)
        target = ROOT / "reports" / "manifests" / f"{slug}-bundle.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        previous_digest = sha256(data).hexdigest()
    else:
        (ROOT / "reports" / "manifests" / f"{slug}-bundle.json").unlink(missing_ok=True)
        previous_digest = None
    for key in store.list("published/"):
        if not key.endswith("/metadata.json"):
            continue
        value = json.loads(store.read(key))
        name = value.get("outputDirName")
        if isinstance(name, str) and re.fullmatch(r"[0-9A-Za-z가-힣_-]+", name):
            (ROOT / "outputs" / name).mkdir(parents=True, exist_ok=True)
    for key in store.list("history/updates/"):
        parts = PurePosixPath(key).parts
        if (len(parts) != 4 or parts[:2] != ("history", "updates")
            or not re.fullmatch(r"U-[0-9]{8}-[0-9]{3}", parts[2])
            or not re.fullmatch(r"[0-9A-Za-z가-힣_-]+\.md", parts[3])):
            continue
        target = ROOT / "reports" / "updates" / parts[2] / parts[3]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(store.read(key))
    return previous_digest


def _archive(paths: list[Path], metadata: dict) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("direct-release.json", _json_bytes(metadata))
        for root in paths:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(ROOT).as_posix())
    return buffer.getvalue()


def _load_archive(store, release_id: str):
    release_id = _id(release_id)
    try:
        data = store.read(f"prepared/{release_id}.zip")
    except FileNotFoundError:
        raise unavailable() from None
    archive = zipfile.ZipFile(io.BytesIO(data))
    metadata = json.loads(archive.read("direct-release.json"))
    if metadata.get("releaseId") != release_id:
        raise ValueError("Prepared release identity mismatch")
    return archive, metadata


def _published_metadata(store, release_id: str, owner_id: str) -> dict:
    try:
        value = json.loads(store.read(f"published/{_id(release_id)}/metadata.json"))
    except FileNotFoundError:
        raise ExpectedReleaseError("Release is not published for this user; verify the release ID or publish it first",
                                   field="release_id") from None
    _require_owner(value, owner_id)
    return value


def prepare(canonical: dict, update: dict, output_base: str | None = None, *, owner_id: str) -> dict:
    return _run_worker("prepare", {"canonical": canonical, "update": update,
                                   "output_base": output_base, "owner_id": _owner(owner_id)})


def _prepare(canonical: dict, update: dict, output_base: str | None = None, *, owner_id: str) -> dict:
    from workbook_engine.release import prepare_release

    if not isinstance(canonical, dict) or not isinstance(update, dict):
        raise ExpectedReleaseError("canonical and update must be objects", field="canonical")
    store = _store()
    history = _TenantHistoryStore(store, owner_id)
    release_id = uuid4().hex
    input_dir = ROOT / ".build" / "direct-mcp-inputs" / release_id
    input_dir.mkdir(parents=True, exist_ok=False)
    canonical_path = input_dir / "canonical.json"
    update_path = input_dir / "update.json"
    canonical_path.write_bytes(_json_bytes(canonical))
    update_path.write_bytes(_json_bytes(update))
    previous_digest = _restore_history(history, str(canonical.get("workbookId", "")))
    result = prepare_release(canonical_path, update_path=update_path, output_base=output_base)
    image_names = sorted(path.name for path in (result.build_dir / "qa" / "samples").glob("*.png"))
    if not image_names or not {"student-contact-sheet.png", "answer-contact-sheet.png"} <= set(image_names):
        raise RuntimeError("Visual review images are missing")
    metadata = {
        "releaseId": release_id,
        "ownerId": _owner(owner_id),
        "workbookId": canonical["workbookId"],
        "buildDir": result.build_dir.relative_to(ROOT).as_posix(),
        "inputDir": input_dir.relative_to(ROOT).as_posix(),
        "pageCount": result.page_count,
        "previousBundleSha256": previous_digest,
        "reviewImages": image_names,
    }
    store.put(f"prepared/{release_id}.zip", _archive([input_dir, result.build_dir], metadata), create_only=True)
    qa = json.loads((result.build_dir / "qa" / "qa.json").read_text(encoding="utf-8"))
    # Workspace paths are server internals; the client only needs image names.
    for key in ("contactSheets", "visualSamples"):
        if isinstance(qa.get(key), list):
            qa[key] = [Path(str(value)).name for value in qa[key]]
    return {"status": "awaiting-visual-review", **metadata, "qa": qa}


def _viewed_images(store, release_id: str) -> set[str]:
    return {PurePosixPath(key).name.removesuffix(".json") for key in store.list(f"reviewed/{release_id}/")}


def review_state(release_id: str, *, owner_id: str) -> dict:
    """Images of an owned prepared release and which of them were opened."""
    store = _store()
    archive, metadata = _load_archive(store, release_id)
    archive.close()
    _require_owner(metadata, owner_id)
    images = list(metadata["reviewImages"])
    viewed = _viewed_images(store, release_id)
    return {"reviewImages": images, "viewed": [name for name in images if name in viewed],
            "remaining": [name for name in images if name not in viewed]}


def review_image(release_id: str, image_name: str, *, owner_id: str) -> dict:
    """Return one owned review PNG and record that it was delivered for inspection."""
    store = _store()
    archive, metadata = _load_archive(store, release_id)
    _require_owner(metadata, owner_id)
    if image_name not in metadata["reviewImages"]:
        archive.close()
        raise ExpectedReleaseError("Unknown review image; use a name from reviewImages", field="image_name")
    with archive:
        data = archive.read(f"{metadata['buildDir']}/qa/samples/{image_name}")
    store.put(f"reviewed/{release_id}/{image_name}.json", _json_bytes({"viewedAt": int(time.time())}))
    viewed = _viewed_images(store, release_id)
    images = list(metadata["reviewImages"])
    return {"data": data, "workbookId": metadata.get("workbookId"), "reviewImages": images,
            "remaining": [name for name in images if name not in viewed]}


def _read_review_image(release_id: str, image_name: str) -> bytes:
    archive, metadata = _load_archive(_store(), release_id)
    with archive:
        if image_name not in metadata["reviewImages"]:
            raise FileNotFoundError(image_name)
        return archive.read(f"{metadata['buildDir']}/qa/samples/{image_name}")


def _restore_archive(archive: zipfile.ZipFile, metadata: dict) -> Path:
    allowed = (metadata["buildDir"] + "/", metadata["inputDir"] + "/")
    for member in archive.infolist():
        if member.filename == "direct-release.json":
            continue
        parts = PurePosixPath(member.filename).parts
        if (member.is_dir() or member.filename.startswith("/") or ".." in parts
            or not member.filename.startswith(allowed)):
            raise ValueError("Invalid prepared archive path")
        destination = ROOT.joinpath(*parts)
        if not destination.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Prepared archive escaped workspace")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(member) as source, destination.open("wb") as output:
            shutil.copyfileobj(source, output)
    build_dir = ROOT / metadata["buildDir"]
    # Prepare and publish intentionally run in different temporary workspaces.
    # Rebind only location fields; artifact/input hashes and content are untouched.
    state_path = build_dir / "release-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["canonicalPath"] = str(ROOT / metadata["inputDir"] / "canonical.json")
    state["updatePath"] = str(ROOT / metadata["inputDir"] / "update.json")
    state["contactSheets"] = [str(build_dir / "qa" / "samples" / Path(path).name)
                              for path in state.get("contactSheets", [])]
    state_path.write_bytes(_json_bytes(state))
    return build_dir


def _signing_secret() -> str:
    secret = os.environ.get("WORKBOOK_ARTIFACT_SIGNING_SECRET", "")
    if not secret:
        raise RuntimeError("WORKBOOK_ARTIFACT_SIGNING_SECRET is required for download links")
    if secret.startswith("tm_"):
        raise RuntimeError("Use a server-only artifact signing secret, separate from client API keys")
    return secret


def _artifact_signature(release_id: str, name: str, expiry: int) -> str:
    # Message format is unchanged so links issued by earlier revisions stay valid.
    message = f"{release_id}\n{name}\n{expiry}".encode("utf-8")
    return hmac.new(_signing_secret().encode("utf-8"), message, sha256).hexdigest()


def _origin() -> str:
    origin = os.environ.get("WORKBOOK_PUBLIC_ORIGIN", "").rstrip("/")
    if not origin.startswith("https://"):
        raise RuntimeError("WORKBOOK_PUBLIC_ORIGIN must be HTTPS")
    return origin


def _expiry() -> tuple[int, str]:
    expiry = int(time.time()) + LINK_LIFETIME
    return expiry, datetime.fromtimestamp(expiry, timezone.utc).isoformat(timespec="seconds")


def artifact_link(release_id: str, name: str) -> tuple[str, str]:
    """One-day capability URL for a published public file and its expiry time."""
    expiry, expires_at = _expiry()
    signature = _artifact_signature(release_id, name, expiry)
    return f"{_origin()}/artifact/{release_id}/{quote(name)}?expires={expiry}&signature={signature}", expires_at


def review_image_link(release_id: str, image_name: str) -> tuple[str, str]:
    """Capability URL for a review image too large to inline; signed in its own namespace."""
    expiry, expires_at = _expiry()
    signature = _artifact_signature(release_id, "review/" + image_name, expiry)
    return (f"{_origin()}/review-image/{release_id}/{quote(image_name)}?expires={expiry}&signature={signature}",
            expires_at)


def publish(release_id: str, reviewer: str, notes: str, *, owner_id: str) -> dict:
    # Enforce ownership and the review gate before scheduling an expensive worker.
    state = review_state(release_id, owner_id=owner_id)
    if state["remaining"]:
        raise ExpectedReleaseError(
            "Review images have not all been opened: " + ", ".join(state["remaining"]),
            status="rejected", missing_images=state["remaining"],
            violations=[{"field": "reviewImages", "message": f"not opened: {name}"} for name in state["remaining"]])
    return _run_worker("publish", {"release_id": release_id, "reviewer": reviewer,
                                   "notes": notes, "owner_id": _owner(owner_id)})


def _publish(release_id: str, reviewer: str, notes: str, *, owner_id: str) -> dict:
    from workbook_engine.release import _slug, publish_release

    store = _store()
    history = _TenantHistoryStore(store, owner_id)
    archive, metadata = _load_archive(store, release_id)
    _require_owner(metadata, owner_id)
    missing = sorted(set(metadata["reviewImages"]) - _viewed_images(store, release_id))
    if missing:
        archive.close()
        raise ExpectedReleaseError(
            "Review images have not all been opened: " + ", ".join(missing),
            status="rejected", missing_images=missing,
            violations=[{"field": "reviewImages", "message": f"not opened: {name}"} for name in missing])
    if not reviewer.strip() or not notes.strip():
        archive.close()
        raise ExpectedReleaseError("Reviewer and visual review notes are required", field="notes")
    if f"published/{release_id}/metadata.json" in store.list(f"published/{release_id}/"):
        archive.close()
        return _published_metadata(store, release_id, owner_id)
    current_digest = _restore_history(history, metadata["workbookId"])
    if current_digest != metadata.get("previousBundleSha256"):
        archive.close()
        raise ExpectedReleaseError("A newer workbook release exists; prepare again before publishing",
                                   status="rejected", field="release_id")
    build_dir = _restore_archive(archive, metadata)
    archive.close()
    result = publish_release(build_dir, reviewer=reviewer, notes=notes)
    records = {}
    for name in PUBLIC_FILES:
        data = (result.output_dir / name).read_bytes()
        store.put(f"published/{release_id}/files/{name}", data)
        records[name] = {"sha256": sha256(data).hexdigest(), "size": len(data)}
    evidence = {
        "report.md": result.report_path,
        "update-index.md": result.aggregate_report_path,
        "build-manifest.json": result.build_manifest_path,
        "qa.json": build_dir / "qa" / "qa.json",
    }
    evidence_records = {}
    for name, path in evidence.items():
        data = path.read_bytes()
        store.put(f"published/{release_id}/evidence/{name}", data)
        evidence_records[name] = {"sha256": sha256(data).hexdigest(), "size": len(data)}
    slug = _slug(metadata["workbookId"])
    history.put(f"history/{slug}/bundle.json", result.bundle_path.read_bytes())
    update_id = json.loads((ROOT / metadata["inputDir"] / "update.json").read_text(encoding="utf-8"))["id"]
    history.put(f"history/updates/{update_id}/{slug}.md", result.report_path.read_bytes())
    published = {
        "status": "published", "releaseId": release_id, "workbookId": metadata["workbookId"],
        "ownerId": _owner(owner_id),
        "updateId": update_id,
        "outputDirName": result.output_dir.name, "pageCount": metadata["pageCount"],
        "files": records, "evidence": evidence_records,
        "reviewer": reviewer.strip(), "reviewNotes": notes.strip(),
    }
    store.put(f"published/{release_id}/metadata.json", _json_bytes(published), create_only=True)
    history.put(f"published/{release_id}/metadata.json", _json_bytes(published), create_only=True)
    return published


def published(release_id: str, *, owner_id: str) -> dict:
    """Owned published metadata with sha256/size for every public file."""
    store = _store()
    value = _published_metadata(store, release_id, owner_id)
    files = dict(value.get("files") or {})
    for name in PUBLIC_FILES:
        record = dict(files.get(name) or {})
        if not record.get("sha256") or "size" not in record:
            # Releases adopted from older revisions may lack digests; derive them from storage.
            data = store.read(f"published/{release_id}/files/{name}")
            record = {"sha256": sha256(data).hexdigest(), "size": len(data)}
        files[name] = record
    return {**value, "files": files}


def read_public_file(release_id: str, name: str, *, owner_id: str) -> bytes:
    """Bytes of one owned, published public file."""
    if name not in PUBLIC_FILES:
        raise ExpectedReleaseError("Unknown public file", field="name")
    store = _store()
    _published_metadata(store, release_id, owner_id)
    return store.read(f"published/{release_id}/files/{name}")


def _signed(request: Request, release_id: str, signed_name: str) -> bool:
    try:
        expiry = int(request.query_params.get("expires", "0"))
    except ValueError:
        return False
    now = int(time.time())
    if expiry < now or expiry > now + LINK_LIFETIME + 60:
        return False
    signature = request.query_params.get("signature", "")
    return hmac.compare_digest(signature, _artifact_signature(release_id, signed_name, expiry))


def _download_response(data: bytes, name: str, media_type: str) -> Response:
    return Response(data, media_type=media_type, headers={
        "Content-Disposition": f"attachment; filename*=UTF-8''{quote(name)}",
        "Cache-Control": "private, no-store",
        "X-Content-Type-Options": "nosniff",
    })


async def artifact_route(request: Request) -> Response:
    release_id = request.path_params.get("release_id", "")
    name = request.path_params.get("name", "")
    if not RELEASE_ID.fullmatch(release_id) or name not in PUBLIC_FILES:
        return Response(status_code=404)
    if not _signed(request, release_id, name):
        return Response(status_code=403)
    try:
        data = await anyio.to_thread.run_sync(_store().read, f"published/{release_id}/files/{name}")
    except Exception as error:
        if isinstance(error, FileNotFoundError) or type(error).__name__ == "NotFound":
            return Response(status_code=404)
        raise
    media_type = "application/pdf" if name.endswith(".pdf") else "text/html; charset=utf-8"
    return _download_response(data, name, media_type)


async def review_image_route(request: Request) -> Response:
    release_id = request.path_params.get("release_id", "")
    name = request.path_params.get("name", "")
    if not RELEASE_ID.fullmatch(release_id) or not REVIEW_IMAGE.fullmatch(name):
        return Response(status_code=404)
    if not _signed(request, release_id, "review/" + name):
        return Response(status_code=403)
    try:
        data = await anyio.to_thread.run_sync(_read_review_image, release_id, name)
    except Exception as error:
        if isinstance(error, (FileNotFoundError, ExpectedReleaseError)) or type(error).__name__ == "NotFound":
            return Response(status_code=404)
        raise
    return _download_response(data, name, "image/png")
