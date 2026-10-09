"""The user distribution, copied outside the repository, works over real HTTP via the common CLI.

The server is the in-memory identity fixture with a temporary local release
store: no production key, database or bucket is used.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from support import REPO, authoring_packet, load_client, start_server, stop_server

client = load_client()
SKILL_CLIENT = Path(".agents/skills/workbook-maker/scripts/mcp_client.py")


def browser_available() -> bool:
    from workbook_engine.qa import find_chrome
    try:
        find_chrome()
        return True
    except Exception:
        return False


class PackageConfigurationTests(unittest.TestCase):
    def test_env_is_package_local(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(client, "PACKAGE_ROOT", Path(folder)):
            env = Path(folder) / ".env"
            env.write_text("MCP_URL=https://example.invalid/mcp\nMCP_API_TOKEN=package-value\n", encoding="utf-8")
            with patch.dict(os.environ, {"MCP_API_TOKEN": "global-value", "MCP_URL": "https://global.invalid/mcp"}):
                self.assertEqual(("https://example.invalid/mcp", "package-value"), client.configuration())
            env.write_text("MCP_URL=http://example.invalid/mcp\nMCP_API_TOKEN=x\n", encoding="utf-8")
            with self.assertRaises(client.ConfigError):
                client.configuration()
            env.write_text("WORKBOOK_MCP_URL=https://example.invalid/mcp\nWORKBOOK_MCP_API_TOKEN=x\n", encoding="utf-8")
            with self.assertRaises(client.ConfigError):
                client.configuration()

    def test_package_has_no_legacy_connection_files(self):
        for relative in (".codex", "runtime.lock.json", "SHA256SUMS.json", ".agents/skills/workbook-release"):
            self.assertFalse((REPO / "client" / relative).exists(), relative)


class IsolatedDistributionHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        cls.package = root / "workbook-maker"
        shutil.copytree(REPO / "client", cls.package,
                        ignore=shutil.ignore_patterns("__pycache__", ".env", ".work", ".build", "outputs"))
        cls.token = "tm_" + secrets.token_urlsafe(32)
        cls.process, cls.port = start_server(
            root / "server.log", TEST_USER_API_KEY=cls.token, WORKBOOK_RELEASE_LOCAL_STORE=str(root / "store"),
            WORKBOOK_ARTIFACT_SIGNING_SECRET="fixture-signing-secret", WORKBOOK_PUBLIC_ORIGIN="https://example.invalid",
            # Loopback tests cannot follow https links, so published files come back inline here.
            WORKBOOK_ARTIFACT_INLINE_MAX_BYTES=str(4 * 1024 * 1024))
        cls.configure(cls.token)

    @classmethod
    def tearDownClass(cls):
        stop_server(cls.process)
        cls.temp.cleanup()

    @classmethod
    def configure(cls, key):
        (cls.package / ".env").write_text(f"MCP_URL=http://127.0.0.1:{cls.port}/mcp\nMCP_API_TOKEN={key}\n",
                                          encoding="utf-8")

    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, "-S", str(self.package / SKILL_CLIENT), *arguments], cwd=self.package,
                              capture_output=True, text=True, encoding="utf-8", timeout=1800)

    def call(self, *arguments, code=0):
        result = self.run_cli("call", *arguments)
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_1_connection_guidance_and_validation(self):
        self.configure("tm_wrong_" + secrets.token_urlsafe(16))
        failed = self.run_cli("ping")
        self.assertEqual(2, failed.returncode)
        self.assertNotIn(self.token, failed.stdout + failed.stderr)
        self.configure(self.token)
        ping = self.run_cli("ping")
        self.assertEqual(0, ping.returncode, ping.stderr)
        tools = json.loads(ping.stdout)["tools"]
        self.assertIn("workbook_prepare_release", tools)
        self.assertNotIn("workbook_get_runtime", tools)

        brief = self.call("workbook_get_guidance", "--out", ".work/guide.json")
        self.assertEqual("ok", brief["status"])
        saved = json.loads((self.package / ".work/guide.json").read_text(encoding="utf-8"))
        self.assertIn("docs/authoring-pipeline.md", saved["data"]["rules"])
        self.assertEqual({"name": "workbook-maker", "version": (REPO / "VERSION").read_text().strip()}, saved["service"])
        self.assertNotIn("data", brief)  # large rules stay in the --out file

        valid = self.call("workbook_validate_canonical", "--arg-file", "canonical=examples/chocolate/content.json")
        self.assertEqual("ok", valid["status"])
        (self.package / ".work/empty.json").write_text("{}", encoding="utf-8")
        invalid = self.call("workbook_validate_canonical", "--arg-file", "canonical=.work/empty.json", code=1)
        self.assertEqual("invalid_input", invalid["status"])
        self.assertTrue(invalid["violations"][0]["field"].startswith("canonical"))
        self.assertFalse((self.package / "server").exists())

    def test_2_authoring_saves_canonical_into_workbooks(self):
        packet = self.package / ".build/authoring/authoring-fixture/authoring.json"
        packet.parent.mkdir(parents=True)
        packet.write_text(json.dumps(authoring_packet(), ensure_ascii=False), encoding="utf-8")
        arguments = ("--arg-file", f"packet={packet.relative_to(self.package).as_posix()}")
        self.assertEqual("ok", self.call("workbook_authoring_verify", *arguments)["status"])
        target = self.package / "workbooks/authoring-fixture"
        target.mkdir()
        expanded = self.call("workbook_authoring_expand", *arguments, "--into", "workbooks/authoring-fixture")
        self.assertEqual(str(target.resolve()), expanded["saved_to"])
        self.assertEqual("ok", self.call("workbook_validate_canonical", "--arg-file",
                                         "canonical=workbooks/authoring-fixture/content.json")["status"])
        again = self.run_cli("call", "workbook_authoring_expand", *arguments, "--into", "workbooks/authoring-fixture")
        self.assertEqual(3, again.returncode)  # an existing canonical is never overwritten

    @unittest.skipUnless(browser_available(), "Chrome/Chromium is required for the real PDF release path")
    def test_3_prepare_review_publish_and_save_outputs(self):
        prepared = self.call("workbook_prepare_release", "--arg-file", "canonical=examples/chocolate/content.json",
                             "--arg-file", "update=examples/U-20260710-001.json", "--arg", "output_base=chocolate_test",
                             "--out", ".work/chocolate/prepare.json")
        self.assertEqual("needs_review", prepared["status"])
        full = json.loads((self.package / ".work/chocolate/prepare.json").read_text(encoding="utf-8"))
        release_id, images = full["data"]["releaseId"], full["data"]["reviewImages"]
        self.assertEqual(22, full["data"]["pageCount"])
        self.assertIn("student-contact-sheet.png", images)
        self.assertFalse(any("\\" in name or "/" in name for name in full["data"]["qa"]["contactSheets"]))

        blocked = self.call("workbook_publish_release", "--arg", f"release_id={release_id}", "--arg", "reviewer=QA",
                            "--arg", "notes=not yet", code=1)
        self.assertEqual("rejected", blocked["status"])
        self.assertEqual("workbook_review_image", blocked["next_action"]["tool"])

        review = self.package / ".work/review" / release_id
        review.mkdir(parents=True)
        for name in images:
            result = self.call("workbook_review_image", "--arg", f"release_id={release_id}", "--arg",
                               f"image_name={name}", "--into", f".work/review/{release_id}")
            self.assertEqual("needs_review", result["status"])
            self.assertTrue((review / name).read_bytes().startswith(b"\x89PNG"))
        self.assertEqual("workbook_publish_release", result["next_action"]["tool"])

        published = self.call("workbook_publish_release", "--arg", f"release_id={release_id}", "--arg", "reviewer=QA",
                              "--arg", "notes=모든 검수 이미지를 열어 잘림·겹침·정답 노출이 없음을 확인함",
                              "--out", ".work/chocolate/publish.json")
        self.assertEqual("done", published["status"])
        saved = Path(published["saved_to"])
        self.assertEqual(self.package / "outputs" / "chocolate_test", saved)
        records = json.loads((self.package / ".work/chocolate/publish.json").read_text(encoding="utf-8"))["data"]["files"]
        self.assertEqual(["문제.html", "문제.pdf", "해설.html", "해설.pdf"], sorted(path.name for path in saved.iterdir()))
        for name, record in records.items():
            data = (saved / name).read_bytes()
            self.assertEqual((record["sha256"], record["size"]), (hashlib.sha256(data).hexdigest(), len(data)))

        again = self.call("workbook_get_artifacts", "--arg", f"release_id={release_id}")
        self.assertEqual("done", again["status"])
        self.assertTrue(again["saved_to"].endswith("chocolate_test_02"))


if __name__ == "__main__":
    unittest.main()
