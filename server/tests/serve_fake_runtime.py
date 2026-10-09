"""Test-only HTTP server with an in-memory identity store; never deployed.

Run with PYTHONPATH=server. The one accepted key is TEST_USER_API_KEY (owner
``fixture-user``); releases use WORKBOOK_RELEASE_LOCAL_STORE, never GCS or a DB.
"""

from __future__ import annotations

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared_mcp_runtime.auth import DatabaseApiKeyVerifier, current_user_id, hash_api_key  # noqa: E402
from shared_mcp_runtime.models import ApiKeyIdentity  # noqa: E402
from shared_mcp_runtime import http_security_kwargs  # noqa: E402
from workbook_mcp.server import ServerSettings, create_server  # noqa: E402


class FixtureIdentityStore:
    def find_api_key(self, key_hash):
        if key_hash == hash_api_key(os.environ["TEST_USER_API_KEY"]):
            return ApiKeyIdentity("fixture-key", "fixture-user", ("mcp:tools",), None)
        return None

    def touch_api_key(self, key_id, used_at):
        pass

    def record_usage(self, event):
        pass


@asynccontextmanager
async def lifespan(_server):
    yield {}


def fake_runtime():
    store = FixtureIdentityStore()
    return SimpleNamespace(auth=DatabaseApiKeyVerifier(store), owner_provider=current_user_id,
                           usage_store=store, lifespan=lifespan)


if __name__ == "__main__":
    settings = ServerSettings.from_environment()
    create_server(fake_runtime(), settings=settings).run(
        transport="http", host=settings.host, port=settings.port, path="/mcp",
        stateless_http=True, json_response=True, show_banner=False,
        **http_security_kwargs(),
    )
