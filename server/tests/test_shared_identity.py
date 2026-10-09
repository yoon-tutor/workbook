"""Auth, telemetry, strict schemas, and owner isolation with no external DB access."""

from __future__ import annotations

import base64
import hashlib
import io
import asyncio
import logging
import subprocess
import sys
import json
import os
import tempfile
import unittest
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

import httpx

from support import CONTENT, REPO, SERVER, authoring_packet, canonical

from shared_mcp_runtime.auth import DatabaseApiKeyVerifier, current_user_id, hash_api_key
from shared_mcp_runtime.models import ApiKeyIdentity
from shared_mcp_runtime.envelope import validate_envelope
from workbook_mcp import direct_release
from workbook_mcp.server import ServerSettings, create_http_app, create_server
from workbook_mcp.service import SERVICE


class MemoryStore:
    def __init__(self):
        self.identities = {
            hash_api_key("tm_alice"): ApiKeyIdentity("key-a", "alice", ("mcp:tools",), None),
            hash_api_key("tm_bob"): ApiKeyIdentity("key-b", "bob", ("mcp:tools",), None),
        }
        self.events = []
        self.touches = []

    def find_api_key(self, digest):
        return self.identities.get(digest)

    def touch_api_key(self, key_id, when):
        self.touches.append(key_id)

    def record_usage(self, event):
        self.events.append(event)


class SharedIdentityTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.environ = patch.dict(os.environ, {
            "WORKBOOK_RELEASE_LOCAL_STORE": str(self.root), "WORKBOOK_RELEASE_BUCKET": "",
            "WORKBOOK_ARTIFACT_SIGNING_SECRET": "test-signing-secret",
            "WORKBOOK_PUBLIC_ORIGIN": "https://example.invalid",
        })
        self.environ.start()
        self.store = MemoryStore()
        self.opened = False
        self.closed = False

        @asynccontextmanager
        async def lifespan(_server):
            self.opened = True
            try:
                yield {}
            finally:
                self.closed = True

        self.runtime = SimpleNamespace(
            auth=DatabaseApiKeyVerifier(self.store), owner_provider=current_user_id,
            usage_store=self.store, lifespan=lifespan,
        )
        self.app = create_http_app(self.runtime)
        self.life_ready = asyncio.Event()
        self.life_stop = asyncio.Event()

        async def manage_lifespan():
            async with self.app.router.lifespan_context(self.app):
                self.life_ready.set()
                await self.life_stop.wait()

        self.life_task = asyncio.create_task(manage_lifespan())
        await self.life_ready.wait()
        self.http = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://localhost")
        self.release_id = "f" * 32
        metadata = {"releaseId": self.release_id, "ownerId": "alice", "workbookId": "test",
                    "buildDir": ".build/releases/test/build", "inputDir": ".build/direct-mcp-inputs/test",
                    "reviewImages": ["student-contact-sheet.png"]}
        prepared = self.root / "prepared" / f"{self.release_id}.zip"
        prepared.parent.mkdir()
        with ZipFile(prepared, "w") as archive:
            archive.writestr("direct-release.json", json.dumps(metadata))
            archive.writestr(metadata["buildDir"] + "/qa/samples/student-contact-sheet.png", b"test-png")
        published = self.root / "published" / self.release_id
        (published / "files").mkdir(parents=True)
        self.files = {"문제.html": b"<p>s</p>", "문제.pdf": b"%PDF-private-test",
                      "해설.html": b"<p>a</p>", "해설.pdf": b"%PDF-answer-test"}
        for name, data in self.files.items():
            (published / "files" / name).write_bytes(data)
        records = {name: {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
                   for name, data in self.files.items()}
        (published / "metadata.json").write_text(json.dumps(
            metadata | {"status": "published", "outputDirName": "test", "files": records}))

    async def asyncTearDown(self):
        await self.http.aclose()
        self.life_stop.set()
        await self.life_task
        self.assertTrue(self.opened)
        self.assertTrue(self.closed)
        self.environ.stop()
        self.temp.cleanup()

    async def rpc(self, token, method, params):
        return await self.http.post("/mcp", headers={"Authorization": f"Bearer {token}",
            "Accept": "application/json, text/event-stream"}, json={"jsonrpc": "2.0", "id": 1,
            "method": method, "params": params})

    async def call(self, token, name, arguments):
        response = await self.rpc(token, "tools/call", {"name": name, "arguments": arguments})
        self.assertEqual(200, response.status_code)
        return response.json()["result"]

    async def test_authentication_and_scoped_usage(self):
        for token in ("bad", "tm_missing"):
            response = await self.rpc(token, "tools/list", {})
            self.assertIn(response.status_code, (401, 403))
        for token, owner in (("tm_alice", "alice"), ("tm_bob", "bob")):
            result = await self.call(token, "workbook_validate_canonical", {"canonical": {}})
            self.assertEqual("invalid_input", result["structuredContent"]["status"])
            self.assertEqual(owner, self.store.events[-1].user_id)
            self.assertEqual("workbook-maker", self.store.events[-1].service_name)
            self.assertEqual("invalid_input", self.store.events[-1].outcome)
        self.assertNotEqual(self.store.events[0].event_id, self.store.events[1].event_id)
        self.assertEqual(["key-a", "key-b"], self.store.touches)

    async def test_tool_inventory_annotations_and_strict_arguments(self):
        response = await self.rpc("tm_alice", "tools/list", {})
        tools = response.json()["result"]["tools"]
        self.assertEqual(10, len(tools))
        self.assertNotIn("workbook_get_runtime", {tool["name"] for tool in tools})
        self.assertTrue(all("annotations" in tool for tool in tools))
        for args in ({"canonical": {}, "edition": "bad"}, {"canonical": {}, "edition": "answer", "extra": True}):
            result = await self.call("tm_alice", "workbook_compile", args)
            self.assertTrue(result.get("isError"))
        self.assertEqual(2, len(self.store.events))

    async def test_release_cross_user_denied_for_every_mcp_operation(self):
        calls = [
            ("workbook_review_image", {"release_id": self.release_id, "image_name": "student-contact-sheet.png"}),
            ("workbook_publish_release", {"release_id": self.release_id, "reviewer": "Bob", "notes": "reviewed"}),
            ("workbook_get_artifacts", {"release_id": self.release_id}),
            ("workbook_read_artifact", {"release_id": self.release_id, "name": "문제.pdf"}),
        ]
        for name, arguments in calls:
            result = await self.call("tm_bob", name, arguments)
            value = result["structuredContent"]
            self.assertEqual([], validate_envelope(value), name)
            self.assertEqual("invalid_input", value["status"], name)
            self.assertEqual("release_id", value["violations"][0]["field"], name)
            self.assertIsNone(value["artifacts"], name)
            self.assertNotIn("%PDF-private-test", json.dumps(result))
            self.assertNotIn(base64.b64encode(b"%PDF-private-test").decode(), json.dumps(result))
        self.assertFalse((self.root / "reviewed").exists())
        result = await self.call("tm_alice", "workbook_get_artifacts", {"release_id": self.release_id})
        self.assertEqual("done", result["structuredContent"]["status"])
        self.assertEqual(4, len(result["structuredContent"]["artifacts"]["files"]))

    async def test_every_tool_returns_standard_envelope(self):
        """STANDARD 6.4: each tool answers with the envelope for success and expected failures."""
        cases = [
            ("workbook_get_guidance", {}, "ok"),
            ("workbook_validate_canonical", {"canonical": canonical()}, "ok"),
            ("workbook_validate_canonical", {"canonical": {}}, "invalid_input"),
            ("workbook_authoring_verify", {"packet": authoring_packet()}, "ok"),
            ("workbook_authoring_verify", {"packet": {}}, "invalid_input"),
            ("workbook_authoring_expand", {"packet": authoring_packet()}, "ok"),
            ("workbook_authoring_expand", {"packet": {"passageActivities": 5}}, "invalid_input"),
            ("workbook_compile", {"canonical": canonical(), "edition": "student"}, "ok"),
            ("workbook_compile", {"canonical": {}, "edition": "answer"}, "invalid_input"),
            ("workbook_prepare_release", {"canonical": canonical(), "update": {}}, "invalid_input"),
            ("workbook_publish_release", {"release_id": self.release_id, "reviewer": "A", "notes": "n"}, "rejected"),
            ("workbook_review_image", {"release_id": self.release_id, "image_name": "student-contact-sheet.png"}, "needs_review"),
            ("workbook_get_artifacts", {"release_id": self.release_id}, "done"),
            ("workbook_read_artifact", {"release_id": self.release_id, "name": "해설.html"}, "ok"),
            ("workbook_get_artifacts", {"release_id": "0" * 32}, "invalid_input"),
        ]
        seen = set()
        for name, arguments, status in cases:
            result = await self.call("tm_alice", name, arguments)
            value = result["structuredContent"]
            self.assertEqual([], validate_envelope(value), (name, value))
            self.assertEqual(status, value["status"], (name, value["violations"]))
            self.assertEqual({"name": "workbook-maker", "version": SERVICE["version"]}, value["service"])
            for item in value["violations"]:
                self.assertTrue(item.get("field") and item.get("message"), (name, item))
            seen.add(name)
        self.assertEqual(10, len(seen))
        expanded = (await self.call("tm_alice", "workbook_authoring_expand", {"packet": authoring_packet()}))["structuredContent"]
        entry = expanded["artifacts"]["files"][0]
        self.assertEqual(("content.json", "utf-8"), (entry["path"], entry["encoding"]))
        self.assertEqual("authoring-fixture", json.loads(entry["content"])["workbookId"])
        rejected = (await self.call("tm_alice", "workbook_prepare_release",
                                    {"canonical": canonical(), "update": {}}))["structuredContent"]
        self.assertTrue(all(item["field"].startswith("update") for item in rejected["violations"]))

    async def test_signed_download_capability_and_health(self):
        value = await self.call("tm_alice", "workbook_get_artifacts", {"release_id": self.release_id})
        entry = next(item for item in value["structuredContent"]["artifacts"]["files"] if item["path"] == "문제.pdf")
        self.assertEqual(hashlib.sha256(b"%PDF-private-test").hexdigest(), entry["sha256"])
        url = entry["url"].replace("https://example.invalid", "http://localhost")
        response = await self.http.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"%PDF-private-test", response.content)
        self.assertEqual(403, (await self.http.get(url.replace("signature=", "signature=bad"))).status_code)
        self.assertEqual(200, (await self.http.get("/healthz")).status_code)
        response = await self.http.get("/health")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok", "service": "workbook-maker", "version": SERVICE["version"]}, response.json())
        self.assertEqual(200, (await self.http.get("/ready")).status_code)

    async def test_no_static_token_production_fallback(self):
        with self.assertRaisesRegex(RuntimeError, "DATABASE_URL"):
            create_server(settings=ServerSettings())

    async def test_foreign_origin_is_rejected_before_auth_or_usage(self):
        response = await self.http.post("/mcp", headers={
            "Authorization": "Bearer tm_alice", "Accept": "application/json, text/event-stream",
            "Origin": "https://foreign.invalid",
        }, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        self.assertEqual(403, response.status_code)
        self.assertEqual([], self.store.touches)
        self.assertEqual([], self.store.events)
        allowed = await self.rpc("tm_alice", "tools/list", {})
        self.assertEqual(200, allowed.status_code)
        same_origin = await self.http.post("/mcp", headers={
            "Authorization": "Bearer tm_alice", "Accept": "application/json, text/event-stream",
            "Origin": "http://localhost",
        }, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        self.assertEqual(200, same_origin.status_code)

    async def test_exact_deployment_host_and_origin_allowlist(self):
        with patch.dict(os.environ, {"MCP_ALLOWED_HOSTS": "service.example",
                                    "MCP_ALLOWED_ORIGINS": "https://service.example"}):
            app = create_http_app(self.runtime)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost") as http:
                headers = {"Authorization": "Bearer tm_alice", "Accept": "application/json, text/event-stream",
                           "Host": "service.example", "Origin": "https://service.example"}
                payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
                self.assertEqual(200, (await http.post("/mcp", headers=headers, json=payload)).status_code)
                headers["Host"] = "foreign.example"
                self.assertIn((await http.post("/mcp", headers=headers, json=payload)).status_code, (403, 421))

    async def test_framework_warnings_do_not_log_input_values(self):
        capture = io.StringIO()
        handler = logging.StreamHandler(capture)
        logger = logging.getLogger("fastmcp")
        logger.addHandler(handler)
        try:
            result = await self.call("tm_alice", "workbook_compile", {
                "canonical": {}, "edition": "PRIVATE_SOURCE_SENTINEL",
            })
            self.assertTrue(result.get("isError"))
            self.assertNotIn("PRIVATE_SOURCE_SENTINEL", capture.getvalue())
        finally:
            logger.removeHandler(handler)


class ReleaseStorageTests(unittest.TestCase):
    def test_prepared_archive_rebinds_workspace_without_altering_integrity_records(self):
        metadata = {"buildDir": ".build/releases/test/build", "inputDir": ".build/direct-mcp-inputs/test"}
        state = {"canonicalPath": "/old/prepare/canonical.json", "updatePath": "/old/prepare/update.json",
                 "contactSheets": ["/old/prepare/qa/samples/student-contact-sheet.png"],
                 "inputDigests": {"canonical": "verified-input"}, "artifacts": {"문제.pdf": {"sha256": "verified-pdf"}}}
        data = io.BytesIO()
        with ZipFile(data, "w") as archive:
            archive.writestr("direct-release.json", "{}")
            archive.writestr(metadata["buildDir"] + "/release-state.json", json.dumps(state))
            archive.writestr(metadata["inputDir"] + "/canonical.json", "{}")
            archive.writestr(metadata["inputDir"] + "/update.json", "{}")
        with tempfile.TemporaryDirectory() as folder, patch.object(direct_release, "ROOT", Path(folder)):
            with ZipFile(io.BytesIO(data.getvalue())) as archive:
                build = direct_release._restore_archive(archive, metadata)
            rebound = json.loads((build / "release-state.json").read_text(encoding="utf-8"))
            self.assertTrue(Path(rebound["canonicalPath"]).is_file())
            self.assertTrue(Path(rebound["updatePath"]).is_file())
            self.assertEqual(state["inputDigests"], rebound["inputDigests"])
            self.assertEqual(state["artifacts"], rebound["artifacts"])
            self.assertTrue(Path(rebound["contactSheets"][0]).is_relative_to(Path(folder)))

    def test_build_context_contains_runtime_and_excludes_private_data(self):
        """Stage service.json build.context the way deploy.py does and run guidance from it."""
        import re
        import shutil
        sys.path.insert(0, str(SERVER / "scripts"))
        import deploy  # vendored standard script; only its ignore rules are used (no gcloud)
        config = json.loads((SERVER / "service.json").read_text(encoding="utf-8"))
        context = config["build"]["context"]
        dockerfile = (SERVER / "Dockerfile").read_text(encoding="utf-8")
        for source in re.findall(r"^COPY (\S+) ", dockerfile, re.M):
            if source != "VERSION":
                self.assertTrue(any(item == source or item.startswith(source + "/") for item in context), source)
        with tempfile.TemporaryDirectory() as folder:
            stage = Path(folder)
            for relative in context:
                source, target = REPO / relative, stage / relative
                if source.is_dir():
                    shutil.copytree(source, target, ignore=deploy.IGNORE)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)
            (stage / "VERSION").write_text("9.9.9" + chr(10), encoding="utf-8")
            names = {path.relative_to(stage).as_posix() for path in stage.rglob("*") if path.is_file()}
            self.assertFalse(any("/tests/" in name or name.endswith((".pyc", ".env")) for name in names))
            self.assertFalse(any(name.startswith(("content/", "client/", "legacy/", "docs/")) for name in names))
            for required in ("server/workbook_mcp/release_worker.py", "server/workbook_mcp/runtime_entry.py",
                             "server/shared_mcp_runtime/envelope.py", "server/docs/semantic-rubric.md",
                             "server/assets/yonjogyo-logo-footer.png", "server/config/workbook-spec.json"):
                self.assertIn(required, names)
            env = {key: value for key, value in os.environ.items() if key not in ("PYTHONPATH", "SERVICE_VERSION")}
            result = subprocess.run([sys.executable, "-X", "utf8", "-c",
                                     "import sys; sys.path.insert(0, 'server'); from workbook_mcp import service, app; "
                                     "g = service.guidance(); print(g['status'], g['service']['version'], len(g['data']['rules']))"],
                                    cwd=stage, env=env, capture_output=True, text=True, encoding="utf-8", timeout=60)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("ok 9.9.9 5", result.stdout.strip())

    def test_signing_secret_never_falls_back_to_legacy_token(self):
        with patch.dict(os.environ, {"WORKBOOK_ARTIFACT_SIGNING_SECRET": "", "WORKBOOK_MCP_API_TOKEN": "legacy-value",
                                    "WORKBOOK_PUBLIC_ORIGIN": "https://example.invalid"}):
            with self.assertRaisesRegex(RuntimeError, "WORKBOOK_ARTIFACT_SIGNING_SECRET"):
                direct_release.artifact_link("f" * 32, "문제.pdf")
        with patch.dict(os.environ, {"WORKBOOK_ARTIFACT_SIGNING_SECRET": "tm_client_key_value",
                                    "WORKBOOK_PUBLIC_ORIGIN": "https://example.invalid"}):
            with self.assertRaisesRegex(RuntimeError, "server-only"):
                direct_release.artifact_link("f" * 32, "문제.pdf")

    def test_legacy_owner_denied_and_tenant_history_isolated(self):
        with self.assertRaises(ValueError):
            direct_release._require_owner({"releaseId": "f" * 32}, "alice")
        with tempfile.TemporaryDirectory() as folder:
            store = direct_release._LocalStore(Path(folder))
            alice = direct_release._TenantHistoryStore(store, "alice")
            bob = direct_release._TenantHistoryStore(store, "bob")
            alice.put("history/same/bundle.json", b"alice-history")
            self.assertEqual([], bob.list("history/"))
            with self.assertRaises(FileNotFoundError):
                bob.read("history/same/bundle.json")
            with direct_release._release_lock(store, "alice", "same"):
                with self.assertRaisesRegex(ValueError, "Another release job"):
                    with direct_release._release_lock(store, "alice", "same"):
                        pass
                with direct_release._release_lock(store, "bob", "same"):
                    pass
            with direct_release._release_lock(store, "alice", "same"):
                pass

    def test_worker_validation_leaves_no_source_workspace_or_storage_lock(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {
            "WORKBOOK_RELEASE_LOCAL_STORE": folder, "WORKBOOK_RELEASE_BUCKET": "",
        }):
            with self.assertRaisesRegex(ValueError, "update JSON Schema"):
                direct_release.prepare({}, {}, owner_id="alice")
            store = direct_release._LocalStore(Path(folder))
            self.assertFalse(any("/locks/" in key for key in store.list("tenants/")))
            self.assertEqual([], store.list("prepared/"))

    def test_administrator_legacy_adoption_preserves_file_bytes_and_rejects_reassignment(self):
        from scripts.adopt_legacy_release import adopt
        with tempfile.TemporaryDirectory() as folder:
            store = direct_release._LocalStore(Path(folder))
            release_id = "e" * 32
            store.put(f"published/{release_id}/metadata.json", direct_release._json_bytes({
                "releaseId": release_id, "workbookId": "legacy", "status": "published",
            }))
            store.put(f"published/{release_id}/files/문제.pdf", b"%PDF-original")
            adopt(store, release_id, "alice")
            metadata = json.loads(store.read(f"published/{release_id}/metadata.json"))
            direct_release._require_owner(metadata, "alice")
            self.assertEqual(b"%PDF-original", store.read(f"published/{release_id}/files/문제.pdf"))
            with self.assertRaisesRegex(ValueError, "reassignment"):
                adopt(store, release_id, "bob")


if __name__ == "__main__":
    unittest.main()
