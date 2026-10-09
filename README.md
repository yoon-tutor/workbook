# 10단계 영어 워크북 제작기 (workbook-maker)

영어 지문 정본 하나에서 학생용·해설용 10단계 워크북(HTML·PDF)을 만드는 MCP 서비스와 Codex용 사용자 배포본. 구조와 규칙은 공통 표준 [docs/STANDARD.md](docs/STANDARD.md)를 따른다.

```text
server/                 MCP 서버 (Cloud Run, 도쿄 asia-northeast1)
  workbook_mcp/         도구(tools.py) → 로직(service.py) → 2단계 릴리스(direct_release.py, release_worker.py)
  workbook_engine/      정본 검증·컴파일·렌더·브라우저/PDF QA·릴리스 엔진
  workbook_authoring/   authoring packet 검증·확장
  shared_mcp_runtime/   공통 인증·사용량·envelope·산출물 묶음 (_standard 복사본)
  config/ schemas/ docs/ assets/   10단계 규격, JSON Schema, 작성·품질 기준, 로고
  tests/                단위·HTTP 통합·배포본 왕복·표준 준수 테스트
  scripts/              deploy, build_release, sandbox_client, audit_client, smoke_live, local_engine 등
  service.json          서비스 설정 (배포·감사)
content/                개발자 정본 콘텐츠·업데이트·변경 보고서·릴리스 이력
client/                 사용자 배포본 원본 (AGENTS.md, .agents/skills/workbook-maker/, examples/)
outputs/                공개한 워크북 결과
docs/                   표준, 운영, 릴리스 규칙, 보고서
```

## 도구

| 도구 | 성공 status | 역할 |
|---|---|---|
| `workbook_get_guidance` | `ok` | 작성 파이프라인·의미 기준·규격·스키마, 9단계 작성 규칙, 검수 정책 |
| `workbook_authoring_verify` | `ok` | 새 authoring packet 검증 |
| `workbook_authoring_expand` | `ok` | packet → 정본 `content.json` (산출물 묶음) |
| `workbook_validate_canonical` | `ok` | 저장 없는 정본 검사 |
| `workbook_compile` | `ok` | 점검용 중간 IR |
| `workbook_prepare_release` | `needs_review` | 브라우저·PDF 자동 QA 후 비공개 릴리스, 검수 이미지 목록 |
| `workbook_review_image` | `needs_review` | 검수 이미지 한 장(PNG 묶음) 전달·열람 기록 |
| `workbook_publish_release` | `done` | 모든 이미지 열람 확인 후 공개, 네 파일 묶음(서명 URL) |
| `workbook_get_artifacts` | `done` | 공개 네 파일의 새 링크 |
| `workbook_read_artifact` | `ok` | 공개 파일 하나를 본문으로 |

입력 오류는 `invalid_input`, 릴리스 관문(미열람 이미지, 작업 중복, 이력 충돌, QA 실패)은 `rejected`로 돌려준다. 모든 응답은 표준 envelope이고 파일은 `mcp-artifact-bundle-v1`으로 전달된다.

인증은 토플 DB의 `users`·`api_keys`를 공유한다(`tm_` 키). 사용자 배포 zip은 `server/scripts/build_release.py`로 만든다. 운영 정보는 [docs/OPERATIONS.md](docs/OPERATIONS.md), 콘텐츠·릴리스 규칙은 [docs/RELEASE_RULES.md](docs/RELEASE_RULES.md).
