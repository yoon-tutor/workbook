"""Build a script-free Workbook MCP client handoff for Codex on macOS or Windows."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "workbook-maker"
TARGET = ROOT / "distribution" / NAME
ARCHIVE = ROOT / "distribution" / f"{NAME}.zip"
URL = "https://workbook-runtime-stage9-972256519381.asia-northeast3.run.app/mcp"
HEADER_HELPER = (
    'python3 -c "import json,pathlib; '
    'cwd=pathlib.Path.cwd(); '
    'root=next((p for p in (cwd,*cwd.parents) if (p/\'.codex/config.toml\').is_file()),None); '
    'assert root is not None, \'Workbook project config not found\'; '
    'tokens=[line.partition(\'=\')[2].strip() for line in '
    '(root/\'.env\').read_text(encoding=\'utf-8\').splitlines() '
    'if line.startswith(\'WORKBOOK_MCP_API_TOKEN=\')]; '
    'assert len(tokens)==1 and tokens[0], \'Package .env token is missing\'; '
    'print(json.dumps({\'Authorization\':\'Bearer \'+tokens[0]}))"'
)

FILES = {
    "runtime.lock.json": ROOT / "runtime.lock.json",
    "examples/chocolate/content.json": ROOT / "workbooks/chocolate/content.json",
    "examples/U-20260710-001.json": ROOT / "updates/U-20260710-001.json",
}
TEXT = {
    ".codex/config.toml": f'''[mcp_servers.workbook_runtime]
url = "{URL}"
# Read the package-local .env at MCP connection time; no session environment is needed.
http_headers_helper = {json.dumps(HEADER_HELPER)}
enabled = true
required = true
tool_timeout_sec = 900
''',
    ".env.example": f"WORKBOOK_MCP_API_TOKEN=\n",
    ".gitignore": ".env\n.build/\noutputs/\n",
    "AGENTS.md": '''# Workbook MCP 작업 지침

워크북 작업은 [.agents/skills/workbook-release/SKILL.md](.agents/skills/workbook-release/SKILL.md)를 따른다.
인증 토큰의 원본은 **이 배포 폴더의 `.env`**에 있는 `WORKBOOK_MCP_API_TOKEN`이다. 사용자에게 토큰을 채팅으로 다시 요구하거나 대화 내용을 인증 값으로 사용하지 않는다. `.codex/config.toml`의 `http_headers_helper`가 MCP 연결 시 이 `.env`를 읽어 Authorization 헤더를 만든다. 토큰을 세션 환경변수나 전역 Codex 설정에 복사하지 않는다.

이 폴더의 `.codex/config.toml`은 원격 `workbook_runtime` MCP를 등록한다. 연결 후 `workbook_get_guidance`를 직접 호출하고 `runtimeId`를 `runtime.lock.json`과 비교한다. PDF 릴리스에는 `directApiVersion: 2`와 prepare·review·publish 도구가 필요하다. 도구가 없으면 MCP 등록·인증·배포 상태를 진단한다. 현재 Codex가 `http_headers_helper`를 지원하는지 확인하고, 지원하지 않으면 Codex 업데이트가 필요하다고 보고한다. `run.ps1`, `setup.ps1`, `scripts/run.py`를 실행하지 않는다.

원본은 `inputs/`, 작성 packet은 `.build/authoring/`, 정본은 `workbooks/`, 업데이트 정의는 `updates/`, 공개 결과는 `outputs/`에 둔다. 토큰과 원본 자료를 로그나 문서에 복사하지 않는다. MCP 호출에 넣은 packet/정본은 원격 서버로 전송된다.
''',
    ".agents/skills/workbook-release/SKILL.md": '''---
name: workbook-release
description: Codex가 원격 Workbook MCP 도구로 영어 10단계 워크북을 작성, PDF 검수, 공개한다.
---

1. 인증 토큰은 배포 폴더의 `.env`에서만 읽는다. 채팅에서 토큰을 요구하거나 세션에 저장된 값을 대신 사용하지 않는다. 프로젝트 MCP 설정의 `http_headers_helper`가 연결 시 `.env`를 읽는다. `workbook_runtime` MCP 연결을 확인하고 `workbook_get_guidance`를 호출한다. 반환된 `runtimeId`가 `runtime.lock.json`과 다르면 중단한다. 도구가 보이지 않으면 프로젝트가 신뢰되었는지, `.codex/config.toml`과 `.env`가 있는지, Codex가 `http_headers_helper`를 지원하는지, `python3`가 실행되는지 확인한다. MCP 등록·인증 오류를 구분해 보고하고 PDF 작업을 진행하지 않는다.
2. `inputs/`의 원본을 확인해 통합 authoring packet을 `.build/authoring/<이름>/authoring.json`에 작성한다. 원본 문장·선택지·정답이 불명확하면 추측하지 않는다.
3. `workbook_authoring_verify`와 `workbook_authoring_expand`로 packet을 검증·확장하고 반환 정본을 `workbooks/<이름>/content.json`에 저장한다. 기존 검토 정본을 덮어쓰지 않는다. `workbook_validate_canonical`로 정본을 다시 검증한다.
4. `directApiVersion: 2`와 `workbook_prepare_release`가 확인되면 검증된 canonical과 update JSON을 직접 전달한다. 반환 상태는 자동 QA 통과·시각 검수 대기다. `workbook_compile`의 중간 IR이나 prepare를 최종 릴리스로 취급하지 않는다.
5. `reviewImages`의 모든 이름에 `workbook_review_image`를 호출해 학생용·해설용 contact sheet와 대표 전체 페이지를 실제로 본다. 2·3단계 빈칸, 4·8·10단계 작성형, 학생 정답 노출, 해설 정답, 잘림·겹침을 직접 확인한다. 자동 검증과 시각 검수는 별개다.
6. 결함이 없으면 `workbook_publish_release`에 release ID, 검수자, 구체적인 검수 기록을 전달한다. 반환된 네 HTML/PDF의 크기·SHA-256·다운로드 주소를 확인하고 실제 산출물을 내려받아 `outputs/`에 저장한다. PDF는 `workbook_read_artifact`로 MCP 파일로도 받을 수 있다. 링크가 만료되면 `workbook_get_artifacts`로 갱신한다. 네 파일과 검수 기록이 확인되기 전 완료로 보고하지 않는다.

9단계는 지문 전체 문장을 A·B·C 선택지에 빠짐없이 배분하고 `answerOrder`는 원문 복원 순서로 쓴다. 서버가 실패하면 로컬 엔진이나 추측으로 대체하지 않는다.
''',
    "README.md": '''# 10단계 영어 워크북 — Mac·Windows 공용 MCP 배포판

이 배포판은 macOS와 Windows에서 Codex가 원격 Workbook MCP 도구를 직접 호출하도록 구성되어 있습니다. 연결 인증에는 `python3`가 필요합니다. PowerShell이나 Chrome은 MCP 연결에 필요하지 않습니다. `AGENTS.md`는 작업 지침이고, 실제 연결 등록은 `.codex/config.toml`이 담당합니다. 이 ZIP에는 인증 토큰이 든 `.env`가 포함되어 있으므로 비공개로 보관하고 외부에 공유하지 마세요.

## 연결

1. 숨김 폴더 `.codex/`와 `.agents/`, 그리고 **이 배포 폴더의 `.env`**가 압축 해제 후 남아 있는지 확인합니다. 인증 토큰의 저장 위치는 이 `.env` 하나입니다. 토큰을 채팅에서 다시 받거나 로그·저장소에 복사하지 않습니다.
2. Mac 또는 Windows에서 `python3 --version`이 실행되는지 확인합니다. 이 명령은 `.env`에서 인증 헤더를 만드는 데만 사용하며 워크북 생성 스크립트를 실행하지 않습니다.
3. **압축을 푼 `workbook-maker` 폴더 자체를** Codex의 신뢰하는 프로젝트로 열고 새 작업을 시작합니다. 기존 `workbook-maker-stage9-final-...` 폴더나 그 채팅에서는 새 MCP 설정이 적용되지 않습니다. 원본 자료는 새 배포 폴더의 `inputs/`로 옮기세요. `.codex/config.toml`의 `http_headers_helper`가 MCP 연결 시 이 폴더의 `.env`를 읽습니다. 환경변수 설정이나 `run.ps1` 실행은 필요하지 않습니다.
4. `workbook_get_guidance`를 호출하고 반환된 `runtimeId`를 `runtime.lock.json`과 대조합니다. 도구가 보이지 않으면 먼저 현재 폴더·프로젝트 신뢰·`.codex/config.toml`·`.env`를 확인합니다. 터미널의 `codex mcp get workbook_runtime` 결과에 `http_headers_helper: <redacted>`가 있는지도 확인합니다. 이 항목이 없으면 오래된 Codex가 인증 헬퍼를 무시하는 것이므로 Codex를 업데이트한 뒤 새 프로젝트 작업을 시작합니다. 현재 확인한 Codex CLI 0.144.3에서는 이 항목이 없습니다. 도구 목록이 보이기 전에는 워크북 생성을 진행하지 마세요.

## 작업 범위

원본은 `inputs/`, 작성 packet은 `.build/authoring/`, 정본은 `workbooks/`, 업데이트는 `updates/`, 결과는 `outputs/`에 둡니다. 에이전트는 `AGENTS.md`와 스킬에 따라 MCP 도구를 직접 사용합니다. MCP에 명시해 전달한 packet과 정본은 원격 서버로 전송됩니다.

PDF 릴리스에는 `workbook_get_guidance`의 `directApiVersion: 2`와 `workbook_prepare_release`, `workbook_review_image`, `workbook_publish_release`, `workbook_get_artifacts`, `workbook_read_artifact` 도구가 필요합니다. prepare가 자동 브라우저·PDF QA를 수행하고, 에이전트가 반환된 검수 이미지 모두를 실제 확인한 뒤 publish합니다. 공개 후 네 HTML/PDF 파일을 다운로드해 확인하세요. 도구가 아직 보이지 않거나 서버가 이전 버전이면 릴리스를 완료했다고 보고하지 마세요.
''',
    "inputs/README.md": "원본 PDF, 이미지, HTML, 텍스트 파일을 이곳에 보존하세요.\n",
    "workbooks/README.md": "검증된 정본을 `<이름>/content.json`에 저장하세요.\n",
    "updates/README.md": "정본의 updateState와 ID·범위가 맞는 업데이트 JSON을 저장하세요.\n",
}


def main() -> None:
    if TARGET.exists() or ARCHIVE.exists():
        raise SystemExit("Direct MCP distribution already exists; choose a new version")
    for name in ("inputs", "outputs", "workbooks", "updates"):
        (TARGET / name).mkdir(parents=True, exist_ok=True)
    for name, source in FILES.items():
        destination = TARGET / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    env_lines = (ROOT / ".env").read_text(encoding="utf-8").splitlines()
    env_values = {}
    for line in env_lines:
        if not line or line.lstrip().startswith("#"):
            continue
        if "=" not in line:
            raise SystemExit("Invalid project-local .env")
        key, value = line.split("=", 1)
        if key not in ("WORKBOOK_MCP_URL", "WORKBOOK_MCP_API_TOKEN") or key in env_values:
            raise SystemExit("Unexpected or duplicate project-local .env key")
        env_values[key] = value.strip()
    if env_values.get("WORKBOOK_MCP_URL") != URL or not env_values.get("WORKBOOK_MCP_API_TOKEN"):
        raise SystemExit("Project-local MCP URL or token is missing")
    env_path = TARGET / ".env"
    env_path.write_text(
        "WORKBOOK_MCP_URL=" + URL + "\nWORKBOOK_MCP_API_TOKEN="
        + env_values["WORKBOOK_MCP_API_TOKEN"] + "\n",
        encoding="utf-8", newline="\n",
    )
    env_path.chmod(0o600)
    for name, value in TEXT.items():
        destination = TARGET / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(value, encoding="utf-8", newline="\n")
    checksums = {
        path.relative_to(TARGET).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(TARGET.rglob("*")) if path.is_file() and path != env_path
    }
    (TARGET / "SHA256SUMS.json").write_text(
        json.dumps({"files": checksums}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    with zipfile.ZipFile(ARCHIVE, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(TARGET.rglob("*")):
            name = f"{NAME}/{path.relative_to(TARGET).as_posix()}"
            if path.is_dir():
                bundle.writestr(name + "/", b"")
            elif path == env_path:
                entry = zipfile.ZipInfo(name)
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o600) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(entry, path.read_bytes())
            else:
                bundle.write(path, name)
    print(json.dumps({"package": str(TARGET), "zip": str(ARCHIVE),
                      "sha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
