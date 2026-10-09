"""Explicit administrator-only migration of a verified legacy release owner."""

from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workbook_mcp import direct_release


def _optional_read(store, key):
    try:
        return store.read(key)
    except Exception as error:
        if isinstance(error, FileNotFoundError) or type(error).__name__ == "NotFound":
            return None
        raise


def adopt(store, release_id: str, owner_id: str) -> None:
    """Assign only an unowned record; never reassign an existing owner's data."""
    release_id = direct_release._id(release_id)
    owner_id = direct_release._owner(owner_id)
    prepared_key = f"prepared/{release_id}.zip"
    published_key = f"published/{release_id}/metadata.json"
    prepared_data = _optional_read(store, prepared_key)
    published_data = _optional_read(store, published_key)
    if prepared_data is None and published_data is None:
        raise ValueError("Legacy release does not exist")
    metadata = []
    if prepared_data is not None:
        with ZipFile(io.BytesIO(prepared_data)) as archive:
            metadata.append(json.loads(archive.read("direct-release.json")))
    if published_data is not None:
        metadata.append(json.loads(published_data))
    for value in metadata:
        if value.get("releaseId") != release_id or value.get("ownerId") not in (None, owner_id):
            raise ValueError("Existing release identity or owner prevents reassignment")
    workbook_id = next((value.get("workbookId") for value in metadata if value.get("workbookId")), None)
    if not workbook_id:
        raise ValueError("Legacy workbook identity is missing; inspect the original record")
    with direct_release._release_lock(store, owner_id, workbook_id) as history:
        if prepared_data is not None:
            result = io.BytesIO()
            with ZipFile(io.BytesIO(prepared_data)) as source, ZipFile(result, "w") as target:
                for member in source.infolist():
                    data = source.read(member.filename)
                    if member.filename == "direct-release.json":
                        data = direct_release._json_bytes(json.loads(data) | {"ownerId": owner_id})
                    target.writestr(member, data)
            store.put(prepared_key, result.getvalue())
        if published_data is not None:
            value = json.loads(published_data) | {"ownerId": owner_id}
            store.put(published_key, direct_release._json_bytes(value))
            history.put(published_key, direct_release._json_bytes(value))
        # Transfer only the selected workbook's legacy version history. Other
        # legacy releases and workbooks remain unowned until verified separately.
        from workbook_engine.release import _slug
        history_key = f"history/{_slug(workbook_id)}/bundle.json"
        legacy = _optional_read(store, history_key)
        if legacy is not None and _optional_read(history, history_key) is None:
            history.put(history_key, legacy, create_only=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--owner-id", required=True)
    parser.add_argument("--confirm-owner-assignment", action="store_true", required=True,
                        help="Administrator verified ownership from the original client records.")
    args = parser.parse_args()
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise SystemExit("DATABASE_URL is required to verify the shared active user")
    from psycopg import connect, sql
    schema = os.environ.get("MCP_SHARED_SCHEMA", "public")
    with connect(url) as connection:
        user = connection.execute(sql.SQL("SELECT id FROM {}.users WHERE id=%s AND status='active'")
            .format(sql.Identifier(schema)), (args.owner_id,)).fetchone()
    if not user:
        raise SystemExit("Owner must be an existing active user in the shared identity table")
    try:
        adopt(direct_release._store(), args.release_id, args.owner_id)
    finally:
        direct_release.close_storage_clients()
    print("Verified legacy release owner assigned; source and artifact bytes were preserved.")


if __name__ == "__main__":
    main()
