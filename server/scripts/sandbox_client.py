#!/usr/bin/env python3
"""배포본을 git 저장소 밖에 복사해 사용자 환경과 같은 조건으로 테스트한다.

Codex는 git 루트부터 작업 폴더까지의 AGENTS.md를 모두 합쳐 읽는다. 저장소 안의
client/에서 Codex를 열면 개발용 AGENTS.md가 함께 적용되므로 이 복사본에서 테스트한다.
복사 대상은 git이 보는 파일(추적 + 무시되지 않은 새 파일)과 개발자의 client/.env다.

  python server/scripts/sandbox_client.py [--dest DIR] [--force]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standard_tools import CLIENT_DIR, git_visible_files, inside_git_repository, load_service  # noqa: E402

MARKER = ".sandbox-source"


def main() -> int:
    name = load_service()["service"]
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", type=Path, default=Path.home() / "agent-sandbox" / name)
    parser.add_argument("--force", action="store_true", help="이 스크립트가 만든 기존 복사본을 교체한다")
    args = parser.parse_args()

    dest = args.dest.expanduser().resolve()
    repository = inside_git_repository(dest)
    if repository is not None:
        print(f"중단: {dest}는 git 저장소({repository}) 안에 있어 상위 AGENTS.md가 함께 적용된다.", file=sys.stderr)
        return 1
    if dest.exists():
        if not (dest / MARKER).is_file():
            print(f"중단: {dest}가 이미 있고 이 스크립트가 만든 복사본이 아니다.", file=sys.stderr)
            return 1
        if not args.force:
            print(f"중단: {dest}가 이미 있다. 교체하려면 --force를 사용한다.", file=sys.stderr)
            return 1
        shutil.rmtree(dest)

    files = git_visible_files(CLIENT_DIR)
    if (CLIENT_DIR / ".env").is_file():
        files.append(Path(".env"))
    for relative in files:
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CLIENT_DIR / relative, target)
    for folder in ("inputs", "outputs"):
        (dest / folder).mkdir(parents=True, exist_ok=True)
    (dest / MARKER).write_text(f"{CLIENT_DIR}\n", encoding="utf-8")

    print(f"{len(files)}개 파일을 {dest}에 복사했다. 이 폴더에서 Codex를 열어 테스트한다.")
    if (CLIENT_DIR / ".env").is_file():
        print("주의: 복사본에 .env(인증 키)가 포함되어 있다. 외부에 공유하지 않는다.")
    else:
        print("주의: client/.env가 없어 복사본에서 서버에 연결할 수 없다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
