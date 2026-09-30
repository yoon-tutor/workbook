"""Unpack the handoff ZIP and run a complete private sample in isolation."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
NAME = "workbook-maker-stage9-final-20260926"
ARCHIVE = ROOT / "distribution" / f"{NAME}.zip"
REPORT = ROOT / "reports" / "distribution" / f"{NAME}-verification.json"


def load_configuration() -> tuple[str, str]:
    values = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    url = values["WORKBOOK_MCP_URL"]
    token = values["WORKBOOK_MCP_API_TOKEN"]
    if not url.startswith("https://") or not token:
        raise RuntimeError("A configured project-local MCP is required for smoke verification")
    return url, token


def run(command: list[str], *, cwd: Path, timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"Distribution command failed: {Path(command[0]).name}: "
                           + result.stderr[-1000:])
    return result.stdout


def parsed(output: str) -> dict:
    return json.loads(output[output.index("{"):])


def main() -> None:
    url, token = load_configuration()
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        if any(not name.startswith(NAME + "/") or ".." in PurePosixPath(name).parts
               for name in names):
            raise ValueError("Archive has a path outside its package root")
        if NAME + "/.env" not in names or NAME + "/.agents/skills/workbook-release/SKILL.md" not in names:
            raise ValueError("Required hidden files missing from ZIP")
        if any(token.encode("utf-8") in archive.read(name) for name in names if not name.endswith("/")):
            raise ValueError("Credential leaked into the ZIP")
        with tempfile.TemporaryDirectory(prefix="user-package-", dir=ROOT / ".build") as directory:
            archive.extractall(directory)
            package = Path(directory) / NAME
            manifest = json.loads((package / "SHA256SUMS.json").read_text(encoding="utf-8"))
            for name, expected in manifest["files"].items():
                if hashlib.sha256((package / name).read_bytes()).hexdigest() != expected:
                    raise ValueError("Handoff package checksum mismatch: " + name)
            setup = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                         "-File", str(package / "setup.ps1")], cwd=package, timeout=240)
            if "Setup complete" not in setup:
                raise ValueError("Package setup did not finish")
            # The credential exists only in this temporary extraction for the smoke run.
            (package / ".env").write_text(
                "WORKBOOK_MCP_URL=" + url + "\nWORKBOOK_MCP_API_TOKEN=" + token + "\n",
                encoding="utf-8")
            def client(*args: str, timeout: int = 180) -> dict:
                return parsed(run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                                   "-File", str(package / "run.ps1"), *args],
                                  cwd=package, timeout=timeout))
            guide = client("guide")
            synced = client("sync")
            if guide["runtimeId"] != manifest["runtimeId"] or synced["runtimeId"] != manifest["runtimeId"]:
                raise ValueError("Distributed runtime does not match server")
            validated = client("validate", "examples/chocolate/content.json")
            if validated["status"] != "passed":
                raise ValueError("Distribution sample validation failed")
            prepared = client("prepare", "examples/chocolate/content.json", "--update",
                              "examples/U-20260710-001.json", "--output-base",
                              "handoff_smoke_chocolate", timeout=300)
            build = Path(prepared["buildDir"])
            qa = json.loads((build / "qa" / "qa.json").read_text(encoding="utf-8"))
            if qa["status"] != "passed" or prepared["pageCount"] != 22:
                raise ValueError("Distribution PDF/DOM quality gate failed")
            if qa["dom"]["student"]["solutions"] != 0 or qa["pdf"]["answerPages"] != 22:
                raise ValueError("Student/answer output contract changed")
            status = client("status", "examples/chocolate/content.json", "--build-dir", str(build))
            if not status["inputsCurrent"] or not status["artifactsIntact"] or not status["canPublish"]:
                raise ValueError("Distribution status integrity check failed")
            reference = ROOT / ".build/releases/chocolate_reading/20260922-005459-771afbeb"
            byte_match = {name: (build / name).read_bytes() == (reference / name).read_bytes()
                          for name in ("문제.html", "해설.html")}
            if not all(byte_match.values()):
                raise ValueError("Distributed HTML differs from verified server-run HTML")
            if any((package / "outputs").iterdir()):
                raise ValueError("prepare unexpectedly published a public output")
            evidence = {
                "status": "passed", "zip": str(ARCHIVE),
                "zipSha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                "runtimeId": synced["runtimeId"], "hiddenFilesIncluded": True,
                "tokenInArchive": False, "packageSetup": "passed",
                "commands": ["guide", "sync", "validate", "prepare", "status"],
                "studentPages": qa["pdf"]["studentPages"],
                "answerPages": qa["pdf"]["answerPages"],
                "studentSolutions": qa["dom"]["student"]["solutions"],
                "htmlByteIdenticalToPreviousRun": byte_match,
                "publicOutputCreatedDuringPrepare": False,
            }
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            REPORT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
            print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
