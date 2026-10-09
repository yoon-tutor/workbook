"""Shared test setup: import path, repository locations and local browser lookup."""

from __future__ import annotations

import os
import sys
from pathlib import Path

SERVER = Path(__file__).resolve().parents[1]
REPO = SERVER.parent
CONTENT = REPO / "content"
CLIENT = REPO / "client/.agents/skills/workbook-maker/scripts/mcp_client.py"
if str(SERVER) not in sys.path:
    sys.path.insert(0, str(SERVER))


def enable_local_browser() -> None:
    """Let engine QA find Chrome/Edge on Windows dev machines (same adapter as runtime_entry)."""
    import workbook_engine.qa as qa
    from workbook_mcp.runtime_entry import windows_browser_support

    if os.name == "nt" and not getattr(qa, "_windows_support", False):
        windows_browser_support(qa)
        qa._windows_support = True


def load_client():
    """Import the client's common CLI module exactly as shipped."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("distribution_mcp_client", CLIENT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(name: str = "chocolate") -> dict:
    import json

    return json.loads((CONTENT / "workbooks" / name / "content.json").read_text(encoding="utf-8"))


def authoring_packet() -> dict:
    """A policy-compliant new packet derived from a reviewed canonical (stage 9 relabelled A-B-C)."""
    from workbook_authoring import compact_canonical

    packet = compact_canonical(canonical("2026-june-grade2-q23"))
    packet["workbookId"] = "authoring-fixture"
    packet["passageActivities"]["paragraphOrder"] = [
        {"blocks": [[3, 4], [5, 6], [1, 2]], "displayOrder": [1, 2, 3], "answerOrder": [3, 1, 2]}]
    return packet


def free_port() -> int:
    import socket

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def start_server(log_path: Path, **environment: str):
    """Start serve_fake_runtime.py on a free loopback port; returns (process, port).

    Uses only the in-memory identity store and WORKBOOK_RELEASE_LOCAL_STORE;
    never a real key, database or bucket.
    """
    import subprocess
    import time

    port = free_port()
    env = dict(os.environ, PYTHONPATH=str(SERVER), PYTHONDONTWRITEBYTECODE="1", HOST="127.0.0.1",
               PORT=str(port), WORKBOOK_RELEASE_BUCKET="", DATABASE_URL="", **environment)
    log = open(log_path, "w", encoding="utf-8")
    process = subprocess.Popen([sys.executable, "-X", "utf8", str(SERVER / "tests/serve_fake_runtime.py")],
                               env=env, stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    process.log = log
    deadline = time.monotonic() + 60
    import socket

    while True:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return process, port
        except OSError:
            if process.poll() is not None or time.monotonic() > deadline:
                stop_server(process)
                raise RuntimeError("test MCP server did not start; see " + str(log_path))
            time.sleep(0.1)


def stop_server(process) -> None:
    process.terminate()
    try:
        process.wait(timeout=15)
    except Exception:
        process.kill()
    process.log.close()


enable_local_browser()
