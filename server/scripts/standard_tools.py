"""Helpers shared by the standard dev scripts (vendored into <repo>/server/scripts/)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER = REPO_ROOT / "server"
CLIENT_DIR = REPO_ROOT / "client"
SERVICE_FILE = SERVER / "service.json"


def load_service() -> dict[str, Any]:
    config = json.loads(SERVICE_FILE.read_text(encoding="utf-8"))
    for key in ("service", "svc", "skill", "gcp", "build", "run"):
        if key not in config:
            raise KeyError(f"server/service.json is missing {key!r}")
    return config


def version() -> str:
    return (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def git_visible_files(directory: Path) -> list[Path]:
    """Tracked plus untracked-but-not-ignored files, relative to ``directory``."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
        cwd=directory, check=True, capture_output=True,
    )
    names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
    return sorted(Path(name) for name in names if (directory / name).is_file())


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.strip().partition("=")
        if separator and not key.startswith("#"):
            values[key.strip()] = value.strip().strip("\"'")
    return values


def gcloud(*args: str, data: str | None = None, check: bool = True) -> str | None:
    executable = shutil.which("gcloud")
    if not executable:
        raise RuntimeError("gcloud CLI is not installed")
    # gcloud is a Python program; force UTF-8 so Korean Windows locales (cp949) decode safely.
    environment = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    result = subprocess.run([executable, *args, "--quiet"], input=data, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", env=environment)
    if result.returncode:
        if not check:
            return None
        raise RuntimeError((result.stderr or "").strip()[-2000:] or f"gcloud exited {result.returncode}")
    return (result.stdout or "").strip()


def inside_git_repository(path: Path) -> Path | None:
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            return parent
    return None
