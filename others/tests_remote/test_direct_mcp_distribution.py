"""Check that the common Codex package authenticates from its own .env."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tomllib
import unittest
import zipfile


PACKAGE = Path(__file__).resolve().parents[1] / "distribution" / "workbook-maker"


class DirectMcpDistributionTests(unittest.TestCase):
    def test_header_helper_reads_package_env_from_nested_workspace(self):
        config = tomllib.loads((PACKAGE / ".codex/config.toml").read_text(encoding="utf-8"))
        server = config["mcp_servers"]["workbook_runtime"]
        self.assertNotIn("bearer_token_env_var", server)
        self.assertTrue(server["required"])
        command = server["http_headers_helper"]
        lines = (PACKAGE / ".env").read_text(encoding="utf-8").splitlines()
        values = [line.partition("=")[2] for line in lines
                  if line.startswith("WORKBOOK_MCP_API_TOKEN=")]
        self.assertEqual(1, len(values))
        self.assertTrue(values[0])

        for shell in (None, shutil.which("sh")):
            if shell is None:
                result = subprocess.run(command, cwd=PACKAGE / "inputs", shell=True,
                                        capture_output=True, text=True, timeout=15)
            else:
                result = subprocess.run([shell, "-c", command], cwd=PACKAGE / "inputs",
                                        capture_output=True, text=True, timeout=15)
            self.assertEqual(0, result.returncode, "MCP header helper failed")
            headers = json.loads(result.stdout)
            if headers != {"Authorization": "Bearer " + values[0]}:
                self.fail("MCP header helper did not use the package-local .env")

    def test_archive_contains_one_env_and_no_workbook_runner(self):
        with zipfile.ZipFile(PACKAGE.with_suffix(".zip")) as archive:
            names = archive.namelist()
            self.assertEqual(1, names.count("workbook-maker/.env"))
            self.assertEqual((PACKAGE / ".env").read_bytes(),
                             archive.read("workbook-maker/.env"))
            self.assertFalse(any(name.endswith(("run.ps1", "setup.ps1", "run.py"))
                                 for name in names))


if __name__ == "__main__":
    unittest.main()
