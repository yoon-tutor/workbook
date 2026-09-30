# 10단계 영어 워크북 — Mac·Windows 공용 MCP 배포판

이 배포판은 macOS와 Windows에서 Codex가 원격 Workbook MCP 도구를 직접 호출하도록 구성되어 있습니다. 연결 인증에는 `python3`가 필요합니다. PowerShell이나 Chrome은 MCP 연결에 필요하지 않습니다. `AGENTS.md`는 작업 지침이고, 실제 연결 등록은 `.codex/config.toml`이 담당합니다. 이 ZIP에는 인증 토큰이 든 `.env`가 포함되어 있으므로 비공개로 보관하고 외부에 공유하지 마세요.

## 연결

1. 숨김 폴더 `.codex/`와 `.agents/`, 그리고 **이 배포 폴더의 `.env`**가 압축 해제 후 남아 있는지 확인합니다. 인증 토큰의 저장 위치는 이 `.env` 하나입니다. 토큰을 채팅에서 다시 받거나 로그·저장소에 복사하지 않습니다.
2. Mac 또는 Windows에서 `python3 --version`이 실행되는지 확인합니다. 이 명령은 `.env`에서 인증 헤더를 만드는 데만 사용하며 워크북 생성 스크립트를 실행하지 않습니다.
3. **압축을 푼 `workbook-maker` 폴더 자체를** Codex의 신뢰하는 프로젝트로 열고 새 작업을 시작합니다. 기존 `workbook-maker-stage9-final-...` 폴더나 그 채팅에서는 새 MCP 설정이 적용되지 않습니다. 원본 자료는 새 배포 폴더의 `inputs/`로 옮기세요. `.codex/config.toml`의 `http_headers_helper`가 MCP 연결 시 이 폴더의 `.env`를 읽습니다. 환경변수 설정이나 `run.ps1` 실행은 필요하지 않습니다.
4. `workbook_get_guidance`를 호출하고 반환된 `runtimeId`를 `runtime.lock.json`과 대조합니다. 도구가 보이지 않으면 먼저 현재 폴더·프로젝트 신뢰·`.codex/config.toml`·`.env`를 확인합니다. 터미널의 `codex mcp get workbook_runtime` 결과에 `http_headers_helper: <redacted>`가 있는지도 확인합니다. 이 항목이 없으면 오래된 Codex가 인증 헬퍼를 무시하는 것이므로 Codex를 업데이트한 뒤 새 프로젝트 작업을 시작합니다. 현재 확인한 Codex CLI 0.144.3에서는 이 항목이 없습니다. 도구 목록이 보이기 전에는 워크북 생성을 진행하지 마세요.

## 작업 범위

원본은 `inputs/`, 작성 packet은 `.build/authoring/`, 정본은 `workbooks/`, 업데이트는 `updates/`, 결과는 `outputs/`에 둡니다. 에이전트는 `AGENTS.md`와 스킬에 따라 MCP 도구를 직접 사용합니다. MCP에 명시해 전달한 packet과 정본은 원격 서버로 전송됩니다.

PDF 릴리스에는 `workbook_get_guidance`의 `directApiVersion: 2`와 `workbook_prepare_release`, `workbook_review_image`, `workbook_publish_release`, `workbook_get_artifacts`, `workbook_read_artifact` 도구가 필요합니다. prepare가 자동 브라우저·PDF QA를 수행하고, 에이전트가 반환된 검수 이미지 모두를 실제 확인한 뒤 publish합니다. 공개 후 네 HTML/PDF 파일을 다운로드해 확인하세요. 도구가 아직 보이지 않거나 서버가 이전 버전이면 릴리스를 완료했다고 보고하지 마세요.
