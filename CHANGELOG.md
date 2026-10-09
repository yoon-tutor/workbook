# Changelog

서비스 버전 기록. 워크북 콘텐츠 업데이트 기록은 [docs/content-changelog.md](docs/content-changelog.md)에 있다.

## 2.0.0-beta.1 (2026-10-10)

정식 출시 전 베타 버전이다. 베타 동안에는 호환이 깨지는 변경이 있을 수 있으며 그때마다 `beta.N`을 올리고 사용자 배포본을 교체한다.

공통 개발 표준(`docs/STANDARD.md` 0.1.0) 적용. 기존 배포본과 호환되지 않으므로 사용자 배포본을 모두 교체한다.

- 저장소 구조를 `server/`, `content/`, `client/`, `docs/`, `legacy/`로 정리했다. `input/`·`others/outputs` 링크를 없앴다.
- 모든 도구 응답을 표준 envelope로 바꿨다. 예상한 입력 오류와 릴리스 관문은 ToolError 대신 `invalid_input`·`rejected`로 돌려준다.
- 검수 이미지, 확장된 정본, 공개 네 파일을 `mcp-artifact-bundle-v1`으로 전달한다. 공개 파일은 SHA-256·크기가 든 서명 URL 항목이다.
- 이전 로컬 runtime 경로(`workbook_get_runtime`, `runtime.lock.json`, `scripts/run.py`)를 제거했다.
- 배포본을 Codex 내장 MCP(`.codex/config.toml`)에서 공통 CLI(`mcp_client.py`)로 바꾸고 `.env` 변수 이름을 `MCP_URL`, `MCP_API_TOKEN`으로 바꿨다. 스킬 이름을 `workbook-maker`로 바꿨다.
- 다운로드 서명에서 `WORKBOOK_MCP_API_TOKEN` 대체 사용을 제거했다. `/ready` 엔드포인트를 추가했다.
- 배포 리전을 도쿄(`asia-northeast1`)로 옮기고 공통 `deploy.py`로 배포한다. 이미지는 Python 3.12다.

## 1.x (2026-09-22 ~ 2026-10-08)

버전 파일 도입 전. 원격 runtime 배포(09-22), 서버 직접 PDF 릴리스 directApiVersion 2(09-27), `workbook-maker` 이름 변경(10-06), 공유 DB 인증·사용량(10-08, 서울 revision `workbook-maker-00004-muq`). 상세는 `docs/OPERATIONS.md`의 운영 이력.
