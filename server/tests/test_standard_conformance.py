"""Vendored from _standard: the service still matches the shared standard (STANDARD.md 8)."""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "server"))

from shared_mcp_runtime.envelope import validate_envelope  # noqa: E402


class StandardConformanceTest(unittest.TestCase):
    def test_vendored_files_match_manifest(self):
        manifest = json.loads((REPO / "server" / "standard-manifest.json").read_text(encoding="utf-8"))
        for relative, expected in manifest["files"].items():
            with self.subTest(file=relative):
                self.assertEqual(hashlib.sha256((REPO / relative).read_bytes()).hexdigest(), expected,
                                 "vendored file edited locally; change _standard and run sync.py")

    def test_client_audit_passes(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(REPO / "server" / "scripts" / "audit_client.py")],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_service_layout(self):
        config = json.loads((REPO / "server" / "service.json").read_text(encoding="utf-8"))
        for relative in ("AGENTS.md", "CLAUDE.md", "README.md", "VERSION", "CHANGELOG.md",
                         "server/Dockerfile", "server/requirements.txt", f"server/{config['svc']}_mcp"):
            with self.subTest(path=relative):
                self.assertTrue((REPO / relative).exists(), relative)
        self.assertRegex((REPO / "VERSION").read_text(encoding="utf-8").strip(), r"^\d+\.\d+\.\d+(-(alpha|beta|rc)\.\d+)?$")

    def test_envelope_validator_rejects_legacy_shape(self):
        self.assertTrue(validate_envelope({"status": "prepared", "next_call": "x"}))


if __name__ == "__main__":
    unittest.main()
