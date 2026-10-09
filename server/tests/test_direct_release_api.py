"""Review images, publish gating and artifact delivery over real loopback MCP HTTP.

The server uses the in-memory identity fixture and a temporary local release
store; no real key, database or bucket is involved.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen
from zipfile import ZipFile

from support import load_client, start_server, stop_server

from shared_mcp_runtime.envelope import validate_envelope
from workbook_mcp import direct_release

client_module = load_client()
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
IMAGES = ["answer-contact-sheet.png", "student-contact-sheet.png"]
FILES = {"문제.html": b"<html>student</html>", "문제.pdf": b"%PDF-local-test",
         "해설.html": b"<html>answer</html>", "해설.pdf": b"%PDF-answer-test"}
SECRET = "fixture-signing-secret"
ORIGIN = "https://example.invalid"


def prepared(store: Path, release_id: str) -> None:
    metadata = {"releaseId": release_id, "ownerId": "fixture-user", "workbookId": "fixture-book",
                "buildDir": ".build/releases/test/test-build", "inputDir": ".build/direct-mcp-inputs/" + release_id,
                "reviewImages": IMAGES}
    path = store / "prepared" / (release_id + ".zip")
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as archive:
        archive.writestr("direct-release.json", json.dumps(metadata))
        for name in IMAGES:
            archive.writestr(metadata["buildDir"] + "/qa/samples/" + name, PNG)


class DirectReleaseApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store = Path(cls.temp.name) / "store"
        cls.published_id, cls.review_id, cls.gate_id = "a" * 32, "b" * 32, "c" * 32
        for release_id in (cls.published_id, cls.review_id, cls.gate_id):
            prepared(cls.store, release_id)
        files = cls.store / "published" / cls.published_id / "files"
        files.mkdir(parents=True)
        records = {}
        for name, data in FILES.items():
            (files / name).write_bytes(data)
            records[name] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        (files.parent / "metadata.json").write_text(json.dumps({
            "status": "published", "releaseId": cls.published_id, "ownerId": "fixture-user",
            "workbookId": "fixture-book", "outputDirName": "fixture_book", "pageCount": 1, "files": records,
        }), encoding="utf-8")
        cls.token = "tm_" + secrets.token_urlsafe(24)
        cls.process, cls.port = start_server(Path(cls.temp.name) / "server.log", TEST_USER_API_KEY=cls.token,
                                             WORKBOOK_ARTIFACT_SIGNING_SECRET=SECRET,
                                             WORKBOOK_RELEASE_LOCAL_STORE=str(cls.store),
                                             WORKBOOK_PUBLIC_ORIGIN=ORIGIN)
        cls.client = client_module.McpClient(f"http://127.0.0.1:{cls.port}/mcp", cls.token, 120)
        cls.client.initialize()

    @classmethod
    def tearDownClass(cls):
        stop_server(cls.process)
        cls.temp.cleanup()

    def call(self, tool, /, **arguments):
        value = self.client.call(tool, arguments)
        self.assertEqual([], validate_envelope(value), value)
        self.assertEqual("workbook-maker", value["service"]["name"])
        return value

    def local(self, url):
        parts = urlsplit(url)
        return urlunsplit(("http", f"127.0.0.1:{self.port}", parts.path, parts.query, ""))

    def test_tool_inventory(self):
        tools = {tool["name"] for tool in self.client.request("tools/list", {})["tools"]}
        self.assertEqual({"workbook_get_guidance", "workbook_validate_canonical", "workbook_authoring_verify",
                          "workbook_authoring_expand", "workbook_compile", "workbook_prepare_release",
                          "workbook_review_image", "workbook_publish_release", "workbook_get_artifacts",
                          "workbook_read_artifact"}, tools)

    def test_review_image_is_artifact_bundle_and_recorded(self):
        value = self.call("workbook_review_image", release_id=self.review_id, image_name="student-contact-sheet.png")
        self.assertEqual("needs_review", value["status"])
        self.assertEqual(["answer-contact-sheet.png"], value["data"]["remaining"])
        self.assertEqual("workbook_review_image", value["next_action"]["tool"])
        self.assertEqual("answer-contact-sheet.png", value["next_action"]["arguments"]["image_name"])
        bundle = value["artifacts"]
        self.assertEqual("mcp-artifact-bundle-v1", bundle["format"])
        self.assertEqual("base64", bundle["files"][0]["encoding"])
        with tempfile.TemporaryDirectory() as folder:
            saved = client_module.save_bundle(bundle, output_root=Path(folder), into=Path(folder), timeout=30)
            self.assertEqual(PNG, (saved / "student-contact-sheet.png").read_bytes())
        self.assertTrue((self.store / "reviewed" / self.review_id / "student-contact-sheet.png.json").is_file())
        unknown = self.call("workbook_review_image", release_id=self.review_id, image_name="other.png")
        self.assertEqual("invalid_input", unknown["status"])
        self.assertEqual("image_name", unknown["violations"][0]["field"])

    def test_publish_requires_every_review_image(self):
        blocked = self.call("workbook_publish_release", release_id=self.gate_id, reviewer="QA", notes="checked")
        self.assertEqual("rejected", blocked["status"])
        self.assertEqual({"not opened: " + name for name in IMAGES}, {v["message"] for v in blocked["violations"]})
        self.assertEqual("workbook_review_image", blocked["next_action"]["tool"])
        self.call("workbook_review_image", release_id=self.gate_id, image_name=IMAGES[0])
        blocked = self.call("workbook_publish_release", release_id=self.gate_id, reviewer="QA", notes="checked")
        self.assertEqual("rejected", blocked["status"])
        self.assertEqual(["reviewImages"], [v["field"] for v in blocked["violations"]])
        self.assertIn(IMAGES[1], blocked["violations"][0]["message"])
        self.assertFalse((self.store / "published" / self.gate_id).exists())

    def test_get_artifacts_returns_signed_url_entries_with_server_digests(self):
        value = self.call("workbook_get_artifacts", release_id=self.published_id)
        self.assertEqual("done", value["status"])
        bundle = value["artifacts"]
        self.assertEqual("fixture_book", bundle["job"])
        self.assertEqual(sorted(FILES), sorted(entry["path"] for entry in bundle["files"]))
        for entry in bundle["files"]:
            self.assertEqual("url", entry["encoding"])
            self.assertTrue(entry["url"].startswith(ORIGIN + "/artifact/"))
            self.assertIn("expires_at", entry)
            with urlopen(self.local(entry["url"]), timeout=10) as response:
                data = response.read()
                self.assertIn("attachment", response.headers["Content-Disposition"])
            self.assertEqual(FILES[entry["path"]], data)
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])
            self.assertEqual(len(data), entry["size"])
        with self.assertRaises(HTTPError) as failure:
            urlopen(self.local(bundle["files"][0]["url"].replace("signature=", "signature=bad")), timeout=10)
        self.assertEqual(403, failure.exception.code)

    def test_read_artifact_is_inline_and_verifiable(self):
        value = self.call("workbook_read_artifact", release_id=self.published_id, name="문제.pdf")
        self.assertEqual("ok", value["status"])
        with tempfile.TemporaryDirectory() as folder:
            saved = client_module.save_bundle(value["artifacts"], output_root=Path(folder), into=None, timeout=30)
            self.assertEqual("fixture_book", saved.name)
            self.assertEqual(FILES["문제.pdf"], (saved / "문제.pdf").read_bytes())

    def test_unknown_release_is_invalid_input_not_error(self):
        for name, arguments in (("workbook_get_artifacts", {"release_id": "d" * 32}),
                                ("workbook_review_image", {"release_id": "d" * 32, "image_name": IMAGES[0]}),
                                ("workbook_read_artifact", {"release_id": "d" * 32, "name": "문제.pdf"}),
                                ("workbook_publish_release", {"release_id": "d" * 32, "reviewer": "a", "notes": "b"})):
            with self.subTest(tool=name):
                value = self.call(name, **arguments)
                self.assertEqual("invalid_input", value["status"])
                self.assertEqual("release_id", value["violations"][0]["field"])

    def test_large_review_image_link_route(self):
        with patch.dict(os.environ, {"WORKBOOK_ARTIFACT_SIGNING_SECRET": SECRET, "WORKBOOK_PUBLIC_ORIGIN": ORIGIN}):
            url, expires_at = direct_release.review_image_link(self.review_id, IMAGES[0])
        self.assertTrue(expires_at)
        with urlopen(self.local(url), timeout=10) as response:
            self.assertEqual(PNG, response.read())
        with self.assertRaises(HTTPError) as failure:
            urlopen(self.local(url.replace("review-image/" + self.review_id, "review-image/" + self.gate_id)), timeout=10)
        self.assertEqual(403, failure.exception.code)


if __name__ == "__main__":
    unittest.main()
