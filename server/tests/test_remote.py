"""Engine parity and MCP round trips: the server path must not change engine bytes.

Render parity runs the unchanged engine through ``runtime_entry`` with content/
as the workspace (the same adapter the release worker uses). HTTP checks use
the shipped client package against the in-memory identity fixture.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import unittest

from support import CONTENT, SERVER, authoring_packet, canonical, load_client, start_server, stop_server

from shared_mcp_runtime.envelope import validate_envelope

client_module = load_client()
BASELINE = SERVER / "tests/fixtures/render-baseline.json"


def crlf_digest(path: Path) -> str:
    """Baseline digests were recorded with CRLF text; compare independent of the host OS."""
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return hashlib.sha256(data).hexdigest()


def run_engine(*arguments: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONPATH=str(SERVER), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-X", "utf8", "-m", "workbook_mcp.runtime_entry", "--workspace",
                           str(CONTENT), *arguments], cwd=CONTENT, env=env, capture_output=True, text=True,
                          encoding="utf-8", timeout=120)


class EngineParityTests(unittest.TestCase):
    def test_all_reviewed_canonical_ir_and_html_bytes(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as folder:
            for index, record in enumerate(baseline["records"]):
                with self.subTest(canonical=record["canonical"], edition=record["edition"]):
                    ir, html = Path(folder) / f"{index}.json", Path(folder) / f"{index}.html"
                    arguments = [record["canonical"], "--edition", record["edition"]]
                    result = run_engine("engine", "compile", *arguments, "--output", str(ir))
                    self.assertEqual(0, result.returncode, result.stderr)
                    result = run_engine("render", *arguments, "--output", str(html))
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual(record["irSha256"], crlf_digest(ir))
                    self.assertEqual(record["htmlSha256"], crlf_digest(html))

    def _bound(self, code: str) -> dict:
        prelude = ("import sys, json; from pathlib import Path; sys.path.insert(0, sys.argv[1]); "
                   "from workbook_mcp.runtime_entry import bind_workspace; root = Path(sys.argv[2]); "
                   "bind_workspace(root)\n")
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", "-c", prelude + code, str(SERVER), str(CONTENT)],
                                capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def test_input_digest_keys_survive_the_new_layout(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        current = self._bound(
            "from workbook_engine.release import _input_digests; "
            "print(json.dumps(_input_digests(root / 'workbooks/chocolate/content.json', root / 'updates/U-20260710-001.json')))")
        # Paths recorded in published history must not change with the folder move.
        self.assertEqual(set(baseline["inputDigests"]), set(current))
        changed_sources = {"workbook_engine/validator.py", "workbook_engine/qa.py",
                           "config/versions.json", "docs/semantic-rubric.md"}
        self.assertEqual({key: value for key, value in baseline["inputDigests"].items() if key not in changed_sources},
                         {key: value for key, value in current.items() if key not in changed_sources})
        for key in changed_sources:
            self.assertEqual(hashlib.sha256((SERVER / key).read_bytes()).hexdigest(), current[key])

    def test_reviewed_history_passes_the_version_gate(self):
        value = self._bound(
            "import workbook_engine.release as r\n"
            "canonical = json.loads((root / 'workbooks/chocolate/content.json').read_text(encoding='utf-8'))\n"
            "previous = r._previous_bundle(canonical['workbookId'])\n"
            "r._enforce_version_transitions(previous=previous, canonical=canonical, spec=r.load_spec(), "
            "versions=r.load_json(r.VERSIONS_PATH))\n"
            "print(json.dumps({'root': str(r.ROOT), 'previous': bool(previous.build), "
            "'engine': r.file_manifest(r.ENGINE_INPUT_PATHS, root=r.ROOT)}))")
        self.assertEqual(str(CONTENT), value["root"])
        self.assertTrue(value["previous"], "content/reports/manifests history was not found")
        self.assertTrue(all(item["path"].startswith("workbook_engine/") for item in value["engine"]["files"]))


class HttpRoundTripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.token = "tm_" + secrets.token_urlsafe(32)
        cls.process, port = start_server(Path(cls.temp.name) / "server.log", TEST_USER_API_KEY=cls.token,
                                         WORKBOOK_RELEASE_LOCAL_STORE=str(Path(cls.temp.name) / "store"))
        cls.url = f"http://127.0.0.1:{port}/mcp"
        cls.client = client_module.McpClient(cls.url, cls.token, 120)
        cls.client.initialize()

    @classmethod
    def tearDownClass(cls):
        stop_server(cls.process)
        cls.temp.cleanup()

    def call(self, tool, /, **arguments):
        value = self.client.call(tool, arguments)
        self.assertEqual([], validate_envelope(value), value)
        return value

    def test_unauthorized_request_fails(self):
        with self.assertRaises(client_module.ConfigError):
            client_module.McpClient(self.url, "wrong-token", 30).initialize()

    def test_guidance_exposes_stage9_authoring_contract(self):
        guidance = self.call("workbook_get_guidance")
        self.assertEqual("ok", guidance["status"])
        stage9 = guidance["data"]["stage9Authoring"]
        self.assertIn("A, B, C", stage9["choiceLabels"])
        self.assertIn("전체 문장", stage9["coverage"])
        self.assertIn("answerOrder", stage9["answerKey"])
        self.assertIn("정답 순열", stage9["questionSet"])
        self.assertIn("새 packet", stage9["verification"])
        self.assertEqual("workbook_authoring_verify", guidance["next_action"]["tool"])

    def test_remote_validation_and_compilation_match_the_engine(self):
        from workbook_engine.compiler import compile_workbook
        value = canonical()
        self.assertEqual("ok", self.call("workbook_validate_canonical", canonical=value)["status"])
        compiled = self.call("workbook_compile", canonical=value, edition="answer")
        self.assertEqual(compile_workbook(value, "answer"), compiled["data"]["ir"])
        invalid = self.call("workbook_validate_canonical", canonical={})
        self.assertEqual("invalid_input", invalid["status"])
        self.assertTrue(all(item["field"].startswith("canonical") for item in invalid["violations"]))

    def test_authoring_verify_and_expand(self):
        for tool in ("workbook_authoring_verify", "workbook_authoring_expand"):
            with self.subTest(tool=tool):
                self.assertEqual("invalid_input", self.call(tool, packet={})["status"])
        # A permutation that passes packet checks but fails canonical validation must come back as
        # invalid_input with the engine rule, not as a masked tool error.
        unordered = authoring_packet()
        unordered["passageActivities"]["paragraphOrder"][0]["answerOrder"] = [2, 3, 1]
        for tool in ("workbook_authoring_verify", "workbook_authoring_expand"):
            with self.subTest(tool=tool, case="canonical rule"):
                rejected = self.call(tool, packet=unordered)
                self.assertEqual("invalid_input", rejected["status"])
                self.assertEqual([("packet.passageActivities.paragraphOrder[0]", "paragraph.answer")],
                                 [(item["field"], item["message"].split(":")[0]) for item in rejected["violations"]])
        verified = self.call("workbook_authoring_verify", packet=authoring_packet())
        self.assertEqual(("ok", "authoring-fixture", 6), (verified["status"], verified["data"]["workbookId"],
                                                          verified["data"]["sentences"]))
        expanded = self.call("workbook_authoring_expand", packet=authoring_packet())
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "authoring-fixture"
            target.mkdir()
            client_module.save_bundle(expanded["artifacts"], output_root=Path(folder), into=target, timeout=30)
            saved = json.loads((target / "content.json").read_text(encoding="utf-8"))
            self.assertEqual("ok", self.call("workbook_validate_canonical", canonical=saved)["status"])
            with self.assertRaises(client_module.ArtifactError):  # never overwrites a reviewed canonical
                client_module.save_bundle(expanded["artifacts"], output_root=Path(folder), into=target, timeout=30)


if __name__ == "__main__":
    unittest.main()
