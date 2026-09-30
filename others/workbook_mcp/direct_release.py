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
from hashlib import sha256
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from uuid import uuid4

from fastmcp.utilities.types import File, Image
from starlette.requests import Request
from starlette.responses import Response


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ("문제.html", "문제.pdf", "해설.html", "해설.pdf")
RELEASE_ID = re.compile(r"[0-9a-f]{32}\Z")


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


class _CloudStore:
    def __init__(self, name: str):
        from google.cloud import storage

        self.bucket = storage.Client().bucket(name)

    def read(self, key: str) -> bytes:
        return self.bucket.blob(key).download_as_bytes()

    def put(self, key: str, data: bytes, *, create_only: bool = False) -> None:
        self.bucket.blob(key).upload_from_string(
            data, if_generation_match=0 if create_only else None,
        )

    def list(self, prefix: str) -> list[str]:
        return [blob.name for blob in self.bucket.list_blobs(prefix=prefix)]


def _store():
    bucket = os.environ.get("WORKBOOK_RELEASE_BUCKET", "").strip()
    if bucket:
        return _CloudStore(bucket)
    local = os.environ.get("WORKBOOK_RELEASE_LOCAL_STORE", "").strip()
    if local:
        return _LocalStore(Path(local))
    raise RuntimeError("WORKBOOK_RELEASE_BUCKET is required for PDF releases")


def _id(value: str) -> str:
    if not RELEASE_ID.fullmatch(value):
        raise ValueError("Invalid release ID")
    return value


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


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
    data = store.read(f"prepared/{release_id}.zip")
    archive = zipfile.ZipFile(io.BytesIO(data))
    metadata = json.loads(archive.read("direct-release.json"))
    if metadata.get("releaseId") != release_id:
        raise ValueError("Prepared release identity mismatch")
    return archive, metadata


def prepare(canonical: dict, update: dict, output_base: str | None = None) -> dict:
    from workbook_engine.release import prepare_release

    if not isinstance(canonical, dict) or not isinstance(update, dict):
        raise ValueError("canonical and update must be objects")
    store = _store()
    release_id = uuid4().hex
    input_dir = ROOT / ".build" / "direct-mcp-inputs" / release_id
    input_dir.mkdir(parents=True, exist_ok=False)
    canonical_path = input_dir / "canonical.json"
    update_path = input_dir / "update.json"
    canonical_path.write_bytes(_json_bytes(canonical))
    update_path.write_bytes(_json_bytes(update))
    previous_digest = _restore_history(store, str(canonical.get("workbookId", "")))
    result = prepare_release(canonical_path, update_path=update_path, output_base=output_base)
    image_names = sorted(path.name for path in (result.build_dir / "qa" / "samples").glob("*.png"))
    if not image_names or not {"student-contact-sheet.png", "answer-contact-sheet.png"} <= set(image_names):
        raise RuntimeError("Visual review images are missing")
    metadata = {
        "releaseId": release_id,
        "workbookId": canonical["workbookId"],
        "buildDir": result.build_dir.relative_to(ROOT).as_posix(),
        "inputDir": input_dir.relative_to(ROOT).as_posix(),
        "pageCount": result.page_count,
        "previousBundleSha256": previous_digest,
        "reviewImages": image_names,
    }
    store.put(f"prepared/{release_id}.zip", _archive([input_dir, result.build_dir], metadata), create_only=True)
    qa = json.loads((result.build_dir / "qa" / "qa.json").read_text(encoding="utf-8"))
    return {"status": "awaiting-visual-review", **metadata, "qa": qa}


def review_image(release_id: str, image_name: str) -> Image:
    store = _store()
    archive, metadata = _load_archive(store, release_id)
    if image_name not in metadata["reviewImages"]:
        raise ValueError("Unknown review image")
    data = archive.read(f"{metadata['buildDir']}/qa/samples/{image_name}")
    store.put(f"reviewed/{release_id}/{image_name}.json", _json_bytes({"viewedAt": int(time.time())}))
    return Image(data=data, format="png")


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
    return ROOT / metadata["buildDir"]


def _artifact_signature(release_id: str, name: str, expiry: int) -> str:
    token = os.environ.get("WORKBOOK_MCP_API_TOKEN", "")
    if not token:
        raise RuntimeError("MCP signing token is missing")
    message = f"{release_id}\n{name}\n{expiry}".encode("utf-8")
    return hmac.new(token.encode("utf-8"), message, sha256).hexdigest()


def _artifact_urls(release_id: str) -> dict[str, str]:
    origin = os.environ.get("WORKBOOK_PUBLIC_ORIGIN", "").rstrip("/")
    if not origin.startswith("https://"):
        raise RuntimeError("WORKBOOK_PUBLIC_ORIGIN must be HTTPS")
    expiry = int(time.time()) + 24 * 60 * 60
    return {
        name: f"{origin}/artifact/{release_id}/{quote(name)}?expires={expiry}&signature={_artifact_signature(release_id, name, expiry)}"
        for name in PUBLIC_FILES
    }


def publish(release_id: str, reviewer: str, notes: str) -> dict:
    from workbook_engine.release import _slug, publish_release

    store = _store()
    archive, metadata = _load_archive(store, release_id)
    missing = sorted(set(metadata["reviewImages"]) - {
        PurePosixPath(key).name.removesuffix(".json")
        for key in store.list(f"reviewed/{release_id}/")
    })
    if missing:
        raise ValueError("Review images have not all been opened: " + ", ".join(missing))
    if not reviewer.strip() or not notes.strip():
        raise ValueError("Reviewer and visual review notes are required")
    if f"published/{release_id}/metadata.json" in store.list(f"published/{release_id}/"):
        return artifacts(release_id)
    current_digest = _restore_history(store, metadata["workbookId"])
    if current_digest != metadata.get("previousBundleSha256"):
        raise ValueError("A newer workbook release exists; prepare again before publishing")
    build_dir = _restore_archive(archive, metadata)
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
    store.put(f"history/{slug}/bundle.json", result.bundle_path.read_bytes())
    update_id = json.loads((ROOT / metadata["inputDir"] / "update.json").read_text(encoding="utf-8"))["id"]
    store.put(f"history/updates/{update_id}/{slug}.md", result.report_path.read_bytes())
    published = {
        "status": "published", "releaseId": release_id, "workbookId": metadata["workbookId"],
        "updateId": update_id,
        "outputDirName": result.output_dir.name, "pageCount": metadata["pageCount"],
        "files": records, "evidence": evidence_records,
        "reviewer": reviewer.strip(), "reviewNotes": notes.strip(),
    }
    store.put(f"published/{release_id}/metadata.json", _json_bytes(published), create_only=True)
    return {**published, "downloadUrls": _artifact_urls(release_id)}


def artifacts(release_id: str) -> dict:
    store = _store()
    value = json.loads(store.read(f"published/{_id(release_id)}/metadata.json"))
    return {**value, "downloadUrls": _artifact_urls(release_id)}


def read_artifact(release_id: str, name: str) -> File:
    """Return a published PDF as MCP embedded file content."""
    if name not in ("문제.pdf", "해설.pdf"):
        raise ValueError("Only published PDFs are available as embedded files")
    data = _store().read(f"published/{_id(release_id)}/files/{name}")
    return File(data=data, format="pdf", name=name)


async def artifact_route(request: Request) -> Response:
    release_id = request.path_params.get("release_id", "")
    name = request.path_params.get("name", "")
    if not RELEASE_ID.fullmatch(release_id) or name not in PUBLIC_FILES:
        return Response(status_code=404)
    try:
        expiry = int(request.query_params.get("expires", "0"))
    except ValueError:
        return Response(status_code=403)
    signature = request.query_params.get("signature", "")
    if expiry < int(time.time()) or expiry > int(time.time()) + 24 * 60 * 60 + 60:
        return Response(status_code=403)
    if not hmac.compare_digest(signature, _artifact_signature(release_id, name, expiry)):
        return Response(status_code=403)
    try:
        data = _store().read(f"published/{release_id}/files/{name}")
    except Exception as error:
        if isinstance(error, FileNotFoundError) or type(error).__name__ == "NotFound":
            return Response(status_code=404)
        raise
    media_type = "application/pdf" if name.endswith(".pdf") else "text/html; charset=utf-8"
    return Response(data, media_type=media_type, headers={
        "Content-Disposition": f"attachment; filename*=UTF-8''{quote(name)}",
        "Cache-Control": "private, no-store",
        "X-Content-Type-Options": "nosniff",
    })
