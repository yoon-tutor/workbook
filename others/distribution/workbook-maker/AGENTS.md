# Workbook MCP 작업 지침

워크북 작업은 [.agents/skills/workbook-release/SKILL.md](.agents/skills/workbook-release/SKILL.md)를 따른다.
인증 토큰의 원본은 **이 배포 폴더의 `.env`**에 있는 `WORKBOOK_MCP_API_TOKEN`이다. 사용자에게 토큰을 채팅으로 다시 요구하거나 대화 내용을 인증 값으로 사용하지 않는다. `.codex/config.toml`의 `http_headers_helper`가 MCP 연결 시 이 `.env`를 읽어 Authorization 헤더를 만든다. 토큰을 세션 환경변수나 전역 Codex 설정에 복사하지 않는다.

이 폴더의 `.codex/config.toml`은 원격 `workbook_runtime` MCP를 등록한다. 연결 후 `workbook_get_guidance`를 직접 호출하고 `runtimeId`를 `runtime.lock.json`과 비교한다. PDF 릴리스에는 `directApiVersion: 2`와 prepare·review·publish 도구가 필요하다. 도구가 없으면 MCP 등록·인증·배포 상태를 진단한다. 현재 Codex가 `http_headers_helper`를 지원하는지 확인하고, 지원하지 않으면 Codex 업데이트가 필요하다고 보고한다. `run.ps1`, `setup.ps1`, `scripts/run.py`를 실행하지 않는다.

원본은 `inputs/`, 작성 packet은 `.build/authoring/`, 정본은 `workbooks/`, 업데이트 정의는 `updates/`, 공개 결과는 `outputs/`에 둔다. 토큰과 원본 자료를 로그나 문서에 복사하지 않는다. MCP 호출에 넣은 packet/정본은 원격 서버로 전송된다.
