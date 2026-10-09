# Workbook MCP 공유 인증 개편 검증

2026-10-07 KST. 작업 범위는 `워크북 3/워크북/others`의 활성 서버·패키징·테스트·운영 문서다. 기존 정본, 생성 엔진, 템플릿, 공개 결과, 고정 runtime lock과 과거 배포 스냅샷을 변경하지 않았다. 작업 전부터 수정되어 있던 Cloud Run 이름/주소 전환 설정은 보존했다.

## 구현

- 토플 정본 `shared_mcp_runtime`의 DB 검증기를 사용하며 같은 `DATABASE_URL`, 같은 schema의 `users`, `api_keys`, `usage_events`를 참조한다. 기존 정적 서버 토큰으로는 MCP를 인증할 수 없다.
- `config.py`, `app.py`, `tools.py`, `server.py`로 설정·조립·도구·진입점을 분리했다. 기존 도구 11개의 이름과 입력 필드, directApiVersion 2, runtimeId와 엔진 출력 형식을 유지했다.
- 도구 annotations와 엄격한 입력 검증, stateless JSON HTTP, DB 연결 풀 lifespan, 서비스명별 사용량 이벤트, 인스턴스 burst 보호를 연결했다. 상태 점검은 `/health`를 사용하며 로컬 호환 경로 `/healthz`를 유지한다.
- API 키나 원문/도구 인자가 framework 경고·예외 로그에 기록되지 않도록 공유 로그 보호기를 설치했다. 사용량 DB에는 사용자·서비스·도구·상태·처리 시간·고유 이벤트 ID만 저장한다.
- MCP Host/Origin 검사를 강제한다. Origin 없는 인증된 네이티브 클라이언트와 허가한 Origin만 접속한다. Cloud Run 배포는 정확한 hostname/origin을 연결하며 DB secret을 세 서비스의 같은 숫자 버전으로 고정한다.
- 릴리스에 소유자를 고정하고 이미지 검수·publish·산출물 링크·PDF 조회에서 다른 사용자와 소유자 없는 기존 릴리스를 차단한다. 사용자별 워크북 이력, create-only 저장소 잠금, 작업별 임시 프로세스/디렉터리를 적용했다.
- prepare/publish가 서로 다른 작업공간을 쓰므로 복원 시 release-state의 위치 필드만 새 경로에 연결한다. inputDigests와 artifact hash를 바꾸지 않는다. timeout 때 worker와 Chromium 자식 프로세스를 정리한다.
- 다운로드는 기존 하루 유효 capability URL을 유지한다. 서명 secret을 사용자 API 키와 분리했다. 기존 static secret의 서명 호환 fallback은 유지하지만 `tm_` 고객 API 키를 서명 비밀로 쓰는 것은 거부한다.
- 관리자 전용 `adopt_legacy_release.py`는 공유 DB의 활성 사용자를 확인하고 검증한 기존 릴리스만 귀속한다. 다른 소유자로 재할당하지 않고 PDF/HTML 바이트를 보존한다.
- allowlist 배포 패키지에 공유 runtime과 새 서버 모듈을 포함하고 test 인증·정본·client `.env`·pyc를 제외했다. 기존 static token 생성기는 사용 중단 안내로 교체했다.

## 검증 결과

| 검증 | 결과 |
|---|---|
| `python -X utf8 scripts/test_runtime_legacy.py` | 41개: 40 통과, macOS 파일 플래그 전용 1개 제외. 실제 Chrome 학생/해설 레이아웃 및 22쪽 private prepare 통과 |
| `python -X utf8 -m unittest discover -s tests_remote -v` | 32개: 31 통과, 작업 전부터 없었던 선택적 `distribution/workbook-maker.zip` 검사 1개 제외 |
| 최종 `tests_remote.test_shared_identity` + `tests_remote.test_direct_release_api` | 16개 모두 통과. Host/Origin 변경 후 실제 로컬 HTTP 이미지·embedded PDF·서명 다운로드 회귀 포함 |
| Python AST / PowerShell Parser / `git diff --check` | 통과 |

인증·사용량 테스트에는 합성 사용자 저장소를 주입했고 실제 고객 키나 DB를 사용하지 않았다. 외부 Origin은 인증/집계 전에 403, 허가되지 않은 Host는 SDK 표준 421로 차단되는 것을 확인했다. 소유권 검사는 review/publish/get-artifacts/read-artifact 네 경로 모두에서 확인했다. 버전 이력과 저장소 잠금은 같은 워크북 ID를 쓰는 두 사용자 사이에서도 분리됐다. 기존 runtime bundle, IR, HTML byte parity 검사도 통과했다.

Windows 샌드박스가 asyncio socketpair 및 임시 파일 rename을 제한해 로컬 테스트는 승인된 sandbox escalation으로 실행했다. 원래 엔진의 직접 unittest 명령은 Windows Chrome 후보 경로를 인식하지 않아 브라우저 검사 하나가 실패했으므로 기존 Windows 어댑터 실행기로 검증했다. 엔진 자체를 수정하거나 검사를 약화하지 않았다.

## 배포 상태

2026-10-07 개편 검증 시점에는 코드와 배포 스크립트만 준비했고 운영 배포와 실제 DB migration은 수행하지 않았다. 이후 사용자 승인에 따라 2026-10-08에 공유 사용량 migration `002`를 적용하고 세 서비스의 공동 인증 검증을 마친 뒤 `workbook-maker-00004-muq`로 운영 트래픽 100%를 전환했다. 자세한 이미지 digest·공유 DB 참조·검증 결과는 [운영 전환 기록](deployment-20261008-production.md)에 남겼다. 후보 단계의 JSON 기록은 당시 트래픽과 검증 상태를 보여 주는 이력으로 보존했다.

운영은 세 서비스 모두 `toefl-maker-database-url:1`과 `public` schema를 참조한다. 워크북 다운로드 서명은 기존 `workbook-runtime-token:latest`가 가리키던 동일한 값의 숫자 버전 `1`로 고정했다. 운영 공동 검증에서 합성 사용자 두 명의 동일 키 사용, 사용량 이벤트 6개, 폐기된 키 차단, 기존 토플 DB 키의 두 주소 인증을 확인했다. 합성 데이터 정리 후 DB는 원래 사용자 2개·키 1개·계약 8개·사용량 231개로 복구됐다.

고객 `.env` 수정이나 영구 고객 키 발급·교체, 실제 릴리스 소유권 귀속, 공개 산출물 publish, Git commit/push는 수행하지 않았다. 기존 릴리스 소유자는 관리자가 원래 고객과 이력을 확인한 후 명시적으로 귀속해야 한다.

사용량 이벤트는 기존 토플 기준의 운영 통계이며 저장 실패에 대한 경고를 제공한다. 월별 한도나 과금 원장의 정확성을 강제하지 않는다. 비정상 종료로 저장소 잠금이 남으면 실제 작업 종료를 확인한 관리자가 해당 잠금 객체만 제거한다.
