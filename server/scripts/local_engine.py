#!/usr/bin/env python3
"""개발용 로컬 엔진 실행: content/를 작업공간으로 엔진·authoring 명령을 실행한다.

  python -X utf8 server/scripts/local_engine.py engine validate workbooks/<이름>/content.json
  python -X utf8 server/scripts/local_engine.py engine inspect workbooks/<이름>/content.json --sentence 3
  python -X utf8 server/scripts/local_engine.py engine compile workbooks/<이름>/content.json --edition answer --output ../.build/ir.json
  python -X utf8 server/scripts/local_engine.py engine prepare workbooks/<이름>/content.json --update updates/<ID>.json
  python -X utf8 server/scripts/local_engine.py engine status workbooks/<이름>/content.json
  python -X utf8 server/scripts/local_engine.py authoring verify ../.build/authoring/<이름>/authoring.json
  python -X utf8 server/scripts/local_engine.py authoring expand ../.build/authoring/<이름>/authoring.json --output workbooks/<이름>/content.json

상대 경로는 content/ 기준이다. prepare 결과는 content/.build/releases/(git 제외)에 쓴다.
공개(publish)는 서버의 workbook_publish_release로만 한다. 이 스크립트는 publish를 거부한다.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "server"
CONTENT = ROOT / "content"


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in {"engine", "authoring", "render"}:
        print(__doc__)
        return 2
    if argv[0] == "engine" and len(argv) > 1 and argv[1] in {"publish", "migrate-legacy"}:
        print("로컬 publish는 지원하지 않는다. 배포본에서 workbook_publish_release로 공개한다.", file=sys.stderr)
        return 2
    env = dict(os.environ, PYTHONPATH=str(SERVER), PYTHONDONTWRITEBYTECODE="1")
    command = [sys.executable, "-X", "utf8", "-m", "workbook_mcp.runtime_entry", "--workspace", str(CONTENT), *argv]
    return subprocess.run(command, cwd=CONTENT, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
