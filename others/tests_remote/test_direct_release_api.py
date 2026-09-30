"""Exercise direct PDF review and artifact delivery over real local MCP HTTP."""

from __future__ import annotations

import base64
import io
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run import Client

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")


class DirectReleaseApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store = Path(cls.temp.name)
        cls.release_id = "a" * 32
        cls.token = secrets.token_urlsafe(24)
        metadata = {
            "releaseId": cls.release_id,
            "buildDir": ".build/releases/test/test-build",
            "inputDir": ".build/direct-mcp-inputs/" + cls.release_id,
            "reviewImages": ["student-contact-sheet.png", "answer-contact-sheet.png"],
        }
        prepared = cls.store / "prepared" / (cls.release_id + ".zip")
        prepared.parent.mkdir()
        with ZipFile(prepared, "w") as archive:
            archive.writestr("direct-release.json", json.dumps(metadata))
            for name in metadata["reviewImages"]:
                archive.writestr(metadata["buildDir"] + "/qa/samples/" + name, PNG)
        pdf = cls.store / "published" / cls.release_id / "files" / "문제.pdf"
        pdf.parent.mkdir(parents=True)
        pdf.write_bytes(b"%PDF-local-test")
        (pdf.parent.parent / "metadata.json").write_text(json.dumps({
            "status": "published", "releaseId": cls.release_id,
            "files": {"문제.pdf": {"size": pdf.stat().st_size}},
        }), encoding="utf-8")
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            cls.port = probe.getsockname()[1]
        cls.url = f"http://127.0.0.1:{cls.port}/mcp"
        env = dict(os.environ, WORKBOOK_MCP_API_TOKEN=cls.token,
                   WORKBOOK_RELEASE_LOCAL_STORE=str(cls.store),
                   WORKBOOK_PUBLIC_ORIGIN="https://example.invalid",
                   HOST="127.0.0.1", PORT=str(cls.port), PYTHONDONTWRITEBYTECODE="1")
        cls.log = (cls.store / "server.log").open("w", encoding="utf-8")
        cls.process = subprocess.Popen([sys.executable, "-X", "utf8", "-m", "workbook_mcp.server"],
                                       cwd=ROOT, env=env, stdout=cls.log, stderr=cls.log,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                cls.client = Client(cls.url, cls.token)
                break
            except (OSError, ValueError):
                if cls.process.poll() is not None:
                    raise RuntimeError("Direct release MCP server failed")
                time.sleep(0.2)
        else:
            cls.process.terminate()
            raise RuntimeError("Direct release MCP startup timed out")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=10)
        cls.log.close()
        cls.temp.cleanup()

    def test_review_image_is_mcp_image_content(self):
        tools = {tool["name"] for tool in self.client.rpc("tools/list", {}, 3)["tools"]}
        self.assertTrue({"workbook_prepare_release", "workbook_review_image",
                         "workbook_publish_release", "workbook_get_artifacts",
                         "workbook_read_artifact"} <= tools)
        result = self.client.rpc("tools/call", {"name": "workbook_review_image", "arguments": {
            "release_id": self.release_id, "image_name": "student-contact-sheet.png"}}, 4)
        images = [item for item in result["content"] if item.get("type") == "image"]
        self.assertEqual(1, len(images))
        self.assertEqual(PNG, base64.b64decode(images[0]["data"]))

    def test_signed_artifact_route(self):
        value = self.client.call("workbook_get_artifacts", {"release_id": self.release_id})
        url = value["downloadUrls"]["문제.pdf"].replace("https://example.invalid", f"http://127.0.0.1:{self.port}")
        with urlopen(url, timeout=10) as response:
            self.assertEqual(b"%PDF-local-test", response.read())
            self.assertIn("attachment", response.headers["Content-Disposition"])
        with self.assertRaises(HTTPError) as failure:
            urlopen(url.replace("signature=", "signature=bad"), timeout=10)
        self.assertEqual(403, failure.exception.code)

    def test_embedded_pdf_resource(self):
        result = self.client.rpc("tools/call", {"name": "workbook_read_artifact", "arguments": {
            "release_id": self.release_id, "name": "문제.pdf"}}, 5)
        resources = [item["resource"] for item in result["content"] if item.get("type") == "resource"]
        self.assertEqual(1, len(resources))
        self.assertEqual(b"%PDF-local-test", base64.b64decode(resources[0]["blob"]))


if __name__ == "__main__":
    unittest.main()
