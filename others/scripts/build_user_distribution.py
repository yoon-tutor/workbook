"""Build the self-contained local client package without reading any credential."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
NAME = "workbook-maker-stage9-final-20260926"
TARGET = ROOT / "distribution" / NAME
ARCHIVE = TARGET.with_suffix(".zip")
SERVER_URL = "https://workbook-runtime-stage9-972256519381.asia-northeast3.run.app/mcp"
FILES = {
    "scripts/run.py": ROOT / "scripts/run.py",
    "runtime.lock.json": ROOT / "runtime.lock.json",
    "requirements-local.txt": ROOT / "requirements-local.txt",
    "examples/chocolate/content.json": ROOT / "workbooks/chocolate/content.json",
    "examples/U-20260710-001.json": ROOT / "updates/U-20260710-001.json",
}
DIRECTORIES = ("inputs", "outputs", "workbooks", "updates", "reports")

README = """# 10단계 영어 워크북 — 사용자 배포판

이 폴더는 설치된 원격 Workbook MCP에서 검증된 스크립트를 받아 **이 PC에서** 워크북을 만드는 실행 공간입니다. 입력·생성 중간물·HTML/PDF는 이 폴더에 남습니다. 토큰은 배포본에 들어 있지 않습니다.

## 처음 한 번

1. Windows에 **Python 3.11**과 Chrome 또는 Edge를 설치합니다.
2. 이 폴더에서 PowerShell을 열고 `powershell -ExecutionPolicy Bypass -File .\\setup.ps1`을 실행합니다. 전용 `.venv`를 만들고 PDF 검사용 Python 패키지를 설치합니다.
3. 이 폴더의 `.env`에서 `WORKBOOK_MCP_API_TOKEN=` 뒤에 **관리자가 별도로 전달한 토큰**을 넣습니다. URL은 설정되어 있습니다. 다른 사람에게 폴더를 전달할 때는 이 값을 다시 비우세요.
4. `.\\run.ps1 guide`와 `.\\run.ps1 sync`로 서버 연결과 고정 버전을 확인합니다.

`.env`와 `.agents`는 숨김 이름을 가진 파일·폴더입니다. 압축 해제 뒤에도 둘 다 있어야 합니다. 네트워크 연결과 토큰이 없으면 원격 실행은 진행되지 않습니다.

## 예제로 실행 확인

예제 정본과 업데이트 정의는 `examples/`에 있습니다. 작업 디렉터리는 이 배포 폴더입니다.

```powershell
.\\run.ps1 validate examples/chocolate/content.json
.\\run.ps1 prepare examples/chocolate/content.json --update examples/U-20260710-001.json --output-base chocolate_example
.\\run.ps1 status examples/chocolate/content.json
```

`prepare`가 반환한 `.build/releases/...` 안에 학생용·해설용 HTML/PDF와 `qa/samples/`의 contact sheet가 생깁니다. contact sheet에서 빈칸, 답안 칸, 빨간 해설 답과 페이지 잘림을 눈으로 확인합니다. **검수한 빌드에만** 아래 명령을 실행합니다.

```powershell
.\\run.ps1 publish <prepare가 반환한 buildDir> --reviewer <검수자> --notes "실제 확인한 페이지와 결과"
```

최종 네 파일은 `outputs/<이름>/문제.html`, `문제.pdf`, `해설.html`, `해설.pdf`에 저장됩니다. 기존 이름이 있으면 새 버전 폴더를 사용합니다. 릴리스 보고서와 이력은 `reports/`에 남습니다.

## 새 지문 작업

- 원본 PDF·이미지·텍스트는 `inputs/`에 보존합니다. 이 배포판은 파일을 넣는 것만으로 원문을 자동 추측하거나 OCR하지 않습니다.
- Codex에서는 이 폴더의 `AGENTS.md`와 `.agents/skills/workbook-release/SKILL.md`를 읽게 합니다. `run.ps1 guide`로 서버의 작성 기준을 먼저 확인합니다.
- 작성한 통합 authoring packet은 `.build/authoring/<이름>/authoring.json`에 저장합니다. `run.ps1 authoring verify <packet>`으로 확인한 뒤 `run.ps1 authoring expand <packet> --output workbooks/<이름>/content.json`으로 정본을 만듭니다.
- 9단계 문단 배열은 지문 전체 문장을 A·B·C 선택지에 배분합니다. 선택지는 위에서부터 A·B·C로 보이고, 해설 정답은 원문 복원 순서입니다. 여러 문항의 정답이 전부 A·B·C이거나 같은 순열로 반복되지 않게 합니다. 새 packet은 서버의 `authoring verify`가 이를 검사합니다.
- 정본에 명시된 업데이트 ID·범위와 일치하는 JSON을 `updates/`에 둡니다. `examples/U-20260710-001.json`은 예제 지문 전용이므로 새 지문에 그대로 적용하지 않습니다.
- `run.ps1 validate <정본>` → `prepare <정본> --update <업데이트>` → 학생용·해설용 시각 검수 → `publish <빌드폴더> --reviewer ... --notes ...` 순서로 진행합니다.

실행 중 서버가 바뀌어 `runtime.lock.json`과 달라지면 중단합니다. 관리자가 검증한 새 배포판을 받아야 합니다. 기존 정본이나 결과를 덮어쓰지 않습니다.
"""

SKILL = """---
name: workbook-release
description: 원격 MCP의 고정 버전 스크립트를 받아 로컬에서 영어 10단계 워크북을 작성, 검증, 생성, 시각 검수, 릴리스한다.
---

이 배포 폴더의 `README.md`를 읽고 `run.ps1 guide`로 현재 서버 규칙을 확인한다. 원본은 `inputs/`, 정본은 `workbooks/<이름>/content.json`, 결과는 `outputs/`에 둔다. `.env`의 토큰을 출력·전송 자료·문서에 복사하지 않는다.

새 지문은 원문 전체를 확인하고 서버의 authoring pipeline에 맞추어 의미 콘텐츠가 완전한 packet을 작성한다. `run.ps1 authoring verify` 뒤 `authoring expand`로 정본을 만든다. 기존에 검토한 정본을 다시 expand해서 덮어쓰지 않는다.

9단계 문단 배열은 매 문항 지문 전체를 선택지에 넣고 A·B·C를 위에서 아래로 표시한다. 블록 내용만 섞고 `answerOrder`는 원문 복원 순서로 작성한다. 묶음 문항의 정답 순열을 가능한 범위에서 분산한다.

`validate` → `prepare --update` → 학생용·해설용 contact sheet 직접 검수 → `publish --reviewer --notes`를 따른다. 2·3단계 빈칸과 4·8·10단계 작성형, 정답 노출 0개, 겹침·잘림·페이지 수를 확인한다. `prepare`만으로 완료라고 보고하지 않는다. 원문 또는 문항이 불명확하면 추측하지 않는다.

원격이 실패하거나 runtime lock이 다르면 중단한다. 로컬에 별도 엔진을 복제하거나 QA 검사를 건너뛰지 않는다. 예제 파일은 새 지문 내용의 근거가 아니다.
"""

AGENTS = """# 이 배포 폴더의 실행 지침

워크북 생성·수정·검수·릴리스에는 [.agents/skills/workbook-release/SKILL.md](.agents/skills/workbook-release/SKILL.md)를 사용한다. 시작 안내는 [README.md](README.md)다. 원본은 `inputs/`, 정본은 `workbooks/`, 업데이트 정의는 `updates/`, 결과는 `outputs/`에 둔다. 모든 실행은 이 폴더의 `run.ps1`을 사용한다.
"""

SETUP = r"""$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
Set-Location -LiteralPath $taskRoot
$taskPython = 'python'
$taskPythonArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.11 -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 11))' 2>$null
    if ($LASTEXITCODE -eq 0) { $taskPython = 'py'; $taskPythonArgs = @('-3.11') }
}
if ($taskPythonArgs.Count -eq 0) {
    & python -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 11))'
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 is required' }
}
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    & $taskPython @taskPythonArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Unable to create package-local Python environment' }
}
& .\.venv\Scripts\python.exe -m pip install --disable-pip-version-check -r requirements-local.txt
if ($LASTEXITCODE -ne 0) { throw 'Unable to install PDF dependencies' }
if (-not (Test-Path -LiteralPath '.env')) { Copy-Item -LiteralPath '.env.example' -Destination '.env' }
Write-Output 'Setup complete. Add the separately supplied token to .env, then run .\run.ps1 guide.'
"""

RUN = r"""$ErrorActionPreference = 'Stop'
$taskPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Run setup.ps1 first' }
Push-Location -LiteralPath $PSScriptRoot
try {
    & $taskPython -X utf8 (Join-Path $PSScriptRoot 'scripts/run.py') @args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
"""

TEXT_FILES = {
    "README.md": README,
    "AGENTS.md": AGENTS,
    ".agents/skills/workbook-release/SKILL.md": SKILL,
    ".env.example": "WORKBOOK_MCP_URL=" + SERVER_URL + "\nWORKBOOK_MCP_API_TOKEN=\n",
    ".env": "WORKBOOK_MCP_URL=" + SERVER_URL + "\nWORKBOOK_MCP_API_TOKEN=\n",
    ".gitignore": ".env\n.venv/\n.runtime/\n.build/\noutputs/\n__pycache__/\n*.pyc\n",
    "setup.ps1": SETUP,
    "run.ps1": RUN,
    "inputs/README.md": "원본 PDF, 이미지, HTML, 텍스트 파일을 이곳에 보관하세요. `README.md`는 입력 자료가 아닙니다. 원문을 확인해 authoring packet을 작성한 뒤 정본을 생성합니다.\n",
    "workbooks/README.md": "검증한 정본을 `<이름>/content.json` 경로에 저장하세요. 원본 자료는 `inputs/`에 남깁니다.\n",
    "updates/README.md": "정본의 `updateState.appliedUpdates`와 ID·범위가 일치하는 업데이트 JSON을 저장하세요. 예제 정의는 `examples/`에 있습니다.\n",
}


def main() -> None:
    if TARGET.exists() or ARCHIVE.exists():
        raise SystemExit("Distribution already exists; preserve it and choose a new version")
    lock = json.loads((ROOT / "runtime.lock.json").read_text(encoding="utf-8"))
    if len(lock["runtimeId"]) != 64:
        raise SystemExit("Invalid pinned runtime")
    for name in DIRECTORIES:
        (TARGET / name).mkdir(parents=True, exist_ok=True)
    for name, source in FILES.items():
        destination = TARGET / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    for name, value in TEXT_FILES.items():
        destination = TARGET / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(value, encoding="utf-8", newline="\n")
    archive_files = sorted(path for path in TARGET.rglob("*") if path.is_file())
    if any(path.name in ("server.py", "Dockerfile") for path in archive_files):
        raise SystemExit("Server code cannot enter distribution")
    if "WORKBOOK_MCP_API_TOKEN=\n" not in (TARGET / ".env").read_text(encoding="utf-8"):
        raise SystemExit("Distribution must not contain a token")
    # .env is intentionally editable after installation; hash only the fixed package files.
    checksums = {path.relative_to(TARGET).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in archive_files if path != TARGET / ".env"}
    (TARGET / "SHA256SUMS.json").write_text(
        json.dumps({"runtimeId": lock["runtimeId"], "files": checksums},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with zipfile.ZipFile(ARCHIVE, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(TARGET.rglob("*")):
            name = f"{NAME}/{path.relative_to(TARGET).as_posix()}"
            if path.is_dir():
                bundle.writestr(name + "/", b"")
            elif path.is_file():
                bundle.write(path, name)
    print(json.dumps({"folder": str(TARGET), "zip": str(ARCHIVE),
                      "runtimeId": lock["runtimeId"], "fileCount": len(archive_files) + 1,
                      "zipSha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
