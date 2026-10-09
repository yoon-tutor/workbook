#!/usr/bin/env python3
"""배포본에 개발 자료·비밀값·개인 정보·작업 잔여물이 들어 있으면 실패한다.

  python server/scripts/audit_client.py            # 저장소의 client/ (git 기준 파일)
  python server/scripts/audit_client.py <DIR>      # 복사본·패키지 폴더 (모든 파일)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standard_tools import CLIENT_DIR, git_visible_files, load_service  # noqa: E402

FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache", "tmp", ".work", "legacy", ".playwright-cli",
                   ".codex", "node_modules", ".DS_Store", "Thumbs.db"}
FORBIDDEN_SUFFIXES = {".pyc", ".log", ".hwp", ".zip"}
LOCAL_WORK = {"inputs", "outputs"}
ALLOWED_ROOT_JSON = {"manifest.json"}
TEXT_SUFFIXES = {".md", ".py", ".js", ".json", ".yaml", ".yml", ".css", ".html", ".txt", ".toml", ".example"}
COMMON_PATTERNS = (
    re.compile(r"/Users/[^/\s]+|[A-Za-z]:\\Users\\"),
    re.compile(r"\btm_[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)postgres(?:ql)?://"),
    re.compile(r"\.\.[\\/]+(?:server|development|others)(?:[\\/]|$)"),
)


def required_files(skill: str) -> list[str]:
    return ["AGENTS.md", "README.md", ".env.example", ".gitignore",
            f".agents/skills/{skill}/SKILL.md", f".agents/skills/{skill}/scripts/mcp_client.py"]


def audit(root: Path, files: list[Path]) -> list[str]:
    config = load_service()
    patterns = list(COMMON_PATTERNS)
    patterns.append(re.compile(rf"(?:from|import)\s+{re.escape(config['svc'])}_mcp\b"))
    patterns += [re.compile(pattern) for pattern in config.get("audit", {}).get("private_patterns", [])]
    errors: list[str] = []
    names = {path.as_posix() for path in files}
    for required in required_files(config["skill"]):
        if required not in names:
            errors.append(f"필수 파일 없음: {required}")
    for relative in files:
        parts = relative.parts
        if relative.as_posix() == ".env" or (parts and parts[0] in LOCAL_WORK and relative.name not in {"README.md", ".gitkeep"}):
            continue
        if FORBIDDEN_PARTS.intersection(parts):
            errors.append(f"금지된 폴더·파일: {relative.as_posix()}")
        if relative.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"금지된 파일 형식: {relative.as_posix()}")
        if len(parts) == 1 and relative.suffix == ".json" and relative.name not in ALLOWED_ROOT_JSON:
            errors.append(f"루트 작업 파일 금지: {relative.as_posix()}")
        if relative.suffix.lower() in TEXT_SUFFIXES or relative.name.startswith(".env."):
            text = (root / relative).read_text(encoding="utf-8", errors="replace")
            for pattern in patterns:
                if pattern.search(text):
                    errors.append(f"비공개 패턴 {pattern.pattern!r}: {relative.as_posix()}")
    return errors


def main() -> int:
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
        files = sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())
    else:
        root = CLIENT_DIR
        files = git_visible_files(root)
    errors = audit(root, files)
    for error in errors:
        print(error)
    if errors:
        return 1
    print(f"배포본 감사 통과: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
