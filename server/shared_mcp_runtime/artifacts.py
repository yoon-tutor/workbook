"""Standard artifact bundle shared by every MCP service (STANDARD.md 7)."""

from __future__ import annotations

import base64
import hashlib
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit

FORMAT = "mcp-artifact-bundle-v1"
INLINE_LIMIT = 4 * 1024 * 1024
LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
TEXT_SUFFIXES = frozenset({".html", ".htm", ".css", ".js", ".json", ".md", ".txt", ".csv", ".svg", ".xml"})


def safe_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or ":" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        raise ValueError(f"Unsafe artifact path: {value!r}")
    return value


def file_entry(path: str, data: bytes | str) -> dict[str, Any]:
    """Inline entry: UTF-8 text for text suffixes, base64 otherwise."""
    path = safe_relative_path(path)
    raw = data.encode("utf-8") if isinstance(data, str) else bytes(data)
    if len(raw) > INLINE_LIMIT:
        raise ValueError(f"{path} exceeds the inline limit; publish it as a url entry")
    entry: dict[str, Any] = {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}
    if PurePosixPath(path).suffix.lower() in TEXT_SUFFIXES:
        try:
            entry.update(encoding="utf-8", content=raw.decode("utf-8"))
            return entry
        except UnicodeDecodeError:
            pass
    entry.update(encoding="base64", content=base64.b64encode(raw).decode("ascii"))
    return entry


def url_entry(path: str, *, url: str, sha256: str, size: int, expires_at: str | None = None) -> dict[str, Any]:
    """Entry the client downloads from a signed URL (large or server-stored files)."""
    parts = urlsplit(url)
    loopback = parts.scheme == "http" and parts.hostname in LOOPBACK
    if not (parts.scheme == "https" or loopback) or not parts.hostname:
        raise ValueError("Artifact URLs must use HTTPS (plain http only for loopback tests)")
    entry: dict[str, Any] = {"path": safe_relative_path(path), "sha256": sha256, "size": int(size),
                             "encoding": "url", "url": url}
    if expires_at:
        entry["expires_at"] = expires_at
    return entry


def bundle(job: str, files: Iterable[Mapping[str, Any]], manifest: str | None = None) -> dict[str, Any]:
    """Wrap entries; ``job`` is the folder name the client creates under outputs/."""
    if not job or any(char in job for char in '/\\:') or job in (".", ".."):
        raise ValueError(f"Unsafe job name: {job!r}")
    entries = [dict(entry) for entry in files]
    seen: set[str] = set()
    for entry in entries:
        key = entry["path"].casefold()
        if key in seen:
            raise ValueError(f"Duplicate artifact path: {entry['path']}")
        seen.add(key)
    if manifest is not None and manifest not in {entry["path"] for entry in entries}:
        raise ValueError("manifest must name one of the bundled files")
    return {"format": FORMAT, "job": job, "files": entries, "manifest": manifest}
