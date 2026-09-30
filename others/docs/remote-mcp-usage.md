# Workbook MCP 연결 방식

## Codex 직접 MCP 연결 (Mac·Windows)

[Mac·Windows 공용 직접 MCP 배포판](../distribution/workbook-maker/README.md)은 프로젝트 `.codex/config.toml`에 HTTPS MCP 주소와 `http_headers_helper`를 등록한다. helper는 MCP 연결 시 배포 폴더의 `.env`에서 토큰을 읽어 Authorization 헤더만 만든다. 토큰을 세션 환경변수·채팅·전역 Codex 설정에 복사하지 않는다. `python3`가 필요하며, 로컬 워크북 실행 스크립트는 없다. 프로젝트 폴더를 신뢰하고 새 작업에서 `workbook_get_guidance`를 직접 호출한 뒤 `runtimeId`를 배포판의 `runtime.lock.json`과 대조한다. `AGENTS.md`는 도구 사용 순서를 지정한다. `.env`가 든 ZIP은 비공개로 보관한다.

도구가 보이지 않으면 이전 배포 폴더·기존 채팅을 계속 사용 중인지 확인하고, 새 `workbook-maker` 폴더를 신뢰한 뒤 새 작업을 연다. 이 배포판은 `http_headers_helper`를 인식하는 Codex가 필요하다. 확인한 Codex CLI 0.144.3은 이 설정을 무시했고 MCP 인증이 실패했다. 해당 버전에서는 Codex를 업데이트해야 한다. 배포판은 MCP 연결을 `required = true`로 설정해 인증 실패가 조용히 지나가지 않도록 한다.

현재 stage9 운영 서버의 직접 도구는 지침·런타임 조회, 작성 packet 검증·확장, 정본 검증, 중간 컴파일이다. 2026-09-27에 `workbook_authoring_verify`와 `workbook_authoring_expand`를 포함한 revision `workbook-runtime-stage9-00003-jad`가 활성화되었다. 기존 Codex 작업은 MCP 도구 목록을 다시 읽지 않을 수 있으므로 새 작업에서 확인한다. 브라우저 QA와 PDF prepare/publish 도구는 아직 없으므로 직접 MCP 경로에서 릴리스 완료를 선언하지 않는다.

## 기존 로컬 실행 경로

원격 MCP는 스키마·규칙·컴파일러·템플릿·릴리스 스크립트를 제공한다. 로컬은 입력, 작업 상태, 브라우저, PDF, 검수 이미지, 공개 결과를 보관한다. 일반 실행에서 원문과 정본은 서버에 전송되지 않는다. 서버의 별도 validate/compile 도구를 직접 호출할 때만 명시한 canonical이 전송된다.

## 설정

`others/.env.example`을 `others/.env`로 복사하고 `WORKBOOK_MCP_URL`, `WORKBOOK_MCP_API_TOKEN`을 설정한다. 전역 Codex 설정이나 명령행에 토큰을 넣지 않는다. 클라이언트는 Python 3.11 이상 표준 라이브러리만 사용한다. HTML/PDF 릴리스에는 Chrome/Chromium과 `python -m pip install -r requirements-local.txt`가 필요하다. 다른 브라우저 위치는 로컬 환경변수 `CHROME_BIN`으로 지정한다.

아래 명령의 작업 디렉터리는 `others/`다.

```powershell
python -X utf8 scripts/run.py guide
python -X utf8 scripts/run.py sync
python -X utf8 scripts/run.py validate workbooks/chocolate/content.json
python -X utf8 scripts/run.py inspect workbooks/chocolate/content.json --sentence 1
python -X utf8 scripts/run.py prepare workbooks/chocolate/content.json --update updates/U-20260710-001.json
python -X utf8 scripts/run.py status workbooks/chocolate/content.json
python -X utf8 scripts/run.py publish <build-dir> --reviewer Codex --notes "실제 시각 검수 기록"
```

prepare는 `.build/releases/`에만 저장한다. contact sheet를 직접 확인한 뒤 publish하면 기존 엔진이 `../outputs/`에 새 폴더를 할당한다. `compile`과 `render`는 중간 IR/HTML 점검용이며 publish를 대체하지 않는다.

## 실행 구조

`AGENTS.md → .agents/skills/workbook-release/SKILL.md → scripts/run.py → HTTPS MCP → runtime.lock.json 검증 → .runtime/<SHA256>/ → 로컬 실행`

실행할 때마다 MCP에 접속하고 lock과 다운로드 파일의 SHA-256을 확인한다. 캐시도 매번 전수 검사한다. 서버가 임의 명령이나 경로를 지정하지 않으며 사용자가 선택한 기존 CLI 명령만 별도 Python 프로세스로 실행한다. 인증 실패·네트워크 장애·해시 불일치 시 실패하며 자동 대체 실행이나 자동 업데이트는 없다.

`workbook_engine/`, `workbook_authoring/`, `config/`, `schemas/`, `assets/`는 서버 배포 원본이다. 새 배포는 원본 변경 검토 → 회귀 검증 → 새 lock 제공 순서로 수행한다. 고정 버전 클라이언트가 사용하는 서버 revision을 유지한 후 새 버전으로 전환한다. prepare와 publish 사이에는 lock을 변경하지 않는다.

## 서버 배포

```powershell
python -X utf8 -m workbook_mcp.bundle --lock runtime.lock.json
python -X utf8 scripts/package_server.py --output server-dist/<새버전>
```

첫 명령은 개발자가 새 배포를 검토한 뒤에만 사용한다. 기존 lock을 자동 갱신하지 않는다. 배포 디렉터리는 allowlist 파일만 포함하며 정본, 기존 출력, .env를 포함하지 않는다. 이 디렉터리를 Docker 빌드/Cloud Run 소스로 사용한다. 서버에는 `WORKBOOK_MCP_API_TOKEN`을 secret으로 제공한다. HTTP 인증 없이는 시작하지 않는다. 서버에 로컬 작업 상태를 저장하지 않으므로 다중 인스턴스와 재시작에 독립적이다.

개발 테스트는 `python -m workbook_mcp.server`로 loopback에 띄우며 토큰은 프로세스 환경으로 전달한다. 프로덕션은 HTTPS 주소를 사용한다.

## 보존 검증

`python scripts/check_preservation.py verify`는 개편 전 기록한 기존 파일을 전수 검사한다. 원래 테스트는 `python -m unittest discover -s tests -v`, MCP 전용 테스트는 `python -m unittest discover -s tests_remote -v`다. 실제 검증 결과와 제한은 `reports/remote-mcp/`에 기록한다.
