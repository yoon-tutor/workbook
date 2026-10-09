#!/usr/bin/env python3
"""운영 서버 실사용 점검: 샌드박스 배포본의 공통 클라이언트로 도구를 왕복한다.

  python server/scripts/sandbox_client.py --force
  python server/scripts/smoke_live.py [--package ~/agent-sandbox/workbook-maker] [--release]

기본 점검: 잘못된 키 거부, ping, guidance, 예시 정본 검사, 잘못된 정본 거부.
--release: 예시 정본으로 prepare → 모든 검수 이미지 수신 → publish → 네 파일 해시 확인까지 실행한다.
           운영 버킷에 해당 키 사용자의 공개 릴리스가 하나 생기므로 필요할 때만 쓴다.
결과는 docs/reports/<날짜>-cloud-run-smoke.json에 저장한다(키·서명 URL·원문 없음).
"""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path(".agents/skills/workbook-maker/scripts/mcp_client.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, default=Path.home() / "agent-sandbox" / "workbook-maker")
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    package = args.package.expanduser().resolve()
    work = Path(tempfile.mkdtemp(prefix="workbook-smoke-"))

    def mcp(*arguments: str, root: Path = package) -> tuple[int, dict]:
        command = [sys.executable, str(root / SKILL), *arguments]
        if arguments[0] == "call" and "--into" not in arguments:
            command += ["--output-root", str(work / "outputs")]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=1800)
        return result.returncode, (json.loads(result.stdout) if result.stdout.strip() else {})

    results: dict = {"date": date.today().isoformat()}
    try:
        bad = work / "bad-package"
        shutil.copytree(package, bad, ignore=shutil.ignore_patterns("outputs", ".work", ".build"))
        env = (bad / ".env").read_text(encoding="utf-8")
        (bad / ".env").write_text(re.sub(r"MCP_API_TOKEN=.*", "MCP_API_TOKEN=tm_invalid_smoke_token_000", env), encoding="utf-8")
        code, _ = mcp("ping", root=bad)
        assert code == 2, f"invalid key accepted (exit {code})"
        results["invalid_auth"] = "rejected"

        code, ping = mcp("ping")
        assert code == 0, ping
        results["server"] = ping["server"]
        results["tools"] = ping["tools"]
        code, brief = mcp("call", "workbook_get_guidance", "--out", str(work / "guide.json"))
        guide = json.loads((work / "guide.json").read_text(encoding="utf-8"))
        assert code == 0 and guide["status"] == "ok" and "docs/semantic-rubric.md" in guide["data"]["rules"], brief
        results["guidance"] = {"status": "ok", "version": guide["service"]["version"], "engineId": guide["data"]["engineId"]}

        canonical = package / "examples/chocolate/content.json"
        update = package / "examples/U-20260710-001.json"
        code, valid = mcp("call", "workbook_validate_canonical", "--arg-file", f"canonical={canonical}")
        assert code == 0 and valid["status"] == "ok", valid
        empty = work / "empty.json"
        empty.write_text("{}", encoding="utf-8")
        code, invalid = mcp("call", "workbook_validate_canonical", "--arg-file", f"canonical={empty}")
        assert code == 1 and invalid["status"] == "invalid_input", invalid
        results["validate"] = {"example": "ok", "empty": "invalid_input"}

        if args.release:
            code, prepared = mcp("call", "workbook_prepare_release", "--arg-file", f"canonical={canonical}",
                                 "--arg-file", f"update={update}", "--arg", "output_base=smoke_chocolate",
                                 "--out", str(work / "prepare.json"))
            full = json.loads((work / "prepare.json").read_text(encoding="utf-8"))
            assert code == 0 and prepared["status"] == "needs_review", prepared
            release_id = full["data"]["releaseId"]
            review = work / "review"
            review.mkdir()
            for name in full["data"]["reviewImages"]:
                code, image = mcp("call", "workbook_review_image", "--arg", f"release_id={release_id}",
                                  "--arg", f"image_name={name}", "--into", str(review))
                assert code == 0 and (review / name).is_file(), image
            code, published = mcp("call", "workbook_publish_release", "--arg", f"release_id={release_id}",
                                  "--arg", "reviewer=smoke", "--arg",
                                  "notes=운영 점검용 예시 릴리스. 모든 검수 이미지를 내려받아 열었다.",
                                  "--out", str(work / "publish.json"))
            full = json.loads((work / "publish.json").read_text(encoding="utf-8"))
            assert code == 0 and published["status"] == "done", published
            saved = Path(published["saved_to"])
            for name, record in full["data"]["files"].items():
                data = (saved / name).read_bytes()
                assert hashlib.sha256(data).hexdigest() == record["sha256"] and len(data) == record["size"], name
            results["release"] = {"releaseId": release_id, "pageCount": full["data"]["pageCount"],
                                  "reviewImages": len(list(review.iterdir())), "files": sorted(full["data"]["files"])}
    finally:
        shutil.rmtree(work, ignore_errors=True)
    report = ROOT / "docs/reports" / f"{date.today().isoformat()}-cloud-run-smoke.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "report": str(report)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
