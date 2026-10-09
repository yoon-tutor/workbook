# Workbook MCP 운영 전환 결과

2026-10-08 KST. 사용자 승인에 따라 공유 DB 인증·사용량 저장을 운영에 적용했다. 후보 배포와 경계 검사는 워크북 담당이 수행했고, 세 서비스 공동 인증 검증과 운영 트래픽 전환·합성 데이터 정리는 통합 담당이 수행했다. 이 기록의 운영 전환 결과는 통합 담당의 완료 확인을 반영한다.

| 항목 | 최종 상태 |
|---|---|
| 프로젝트 / 리전 / 서비스 | `yoontutor-507902` / `asia-northeast3` / `workbook-maker` |
| 운영 revision / 트래픽 | `workbook-maker-00004-muq` / 100% |
| 이미지 | `asia-northeast3-docker.pkg.dev/yoontutor-507902/cloud-run-source-deploy/workbook-maker@sha256:0b937bd92f72e39cb8c4276ed2003003413a8f7b6c30731762e5860bf6008fb7` |
| Cloud Build | `b920fe55-6e6b-4d2b-8cc8-ac289b3cb1f8` / SUCCESS |
| 공유 DB | `DATABASE_URL` → Secret Manager `toefl-maker-database-url:1`, schema `public` |
| 다운로드 서명 | `WORKBOOK_ARTIFACT_SIGNING_SECRET` → `workbook-runtime-token:1` |
| 외부 상태 점검 | `/health` |

기존 MCP 주소 두 개를 유지했다.

- `https://workbook-maker-972256519381.asia-northeast3.run.app/mcp`
- `https://workbook-maker-yzxn4wai2a-du.a.run.app/mcp`

기존 런타임 서비스 계정, CPU 2, 메모리 2Gi, concurrency 1, 요청 timeout 900초, startup probe, 최대 인스턴스 설정, 릴리스 버킷, public origin과 공개 invoker IAM을 보존했다. 다운로드 서명 secret의 기존 `latest`는 enabled version `1`을 가리키므로 새 숫자 버전 참조는 같은 서명 값이다. 원본 secret 값을 읽거나 기록하지 않았다. 이전 이미지·revision·산출물을 삭제하지 않았다.

공유 migration `002`는 `mcp-shared-usage-upgrade-kb8jf` 작업으로 완료되고 컬럼·인덱스가 검증된 뒤 후보 배포를 진행했다. 후보 `/health` 200, 미인증 MCP 401, 외부 Origin 403을 확인했다. 로컬 `/healthz` 호환 경로는 유지하지만 Cloud Run 외부 점검에는 플랫폼 예약 경로를 피하는 `/health`를 사용한다. 유효기간이 남은 기존 signed URL이 제공되지 않아 비공개 산출물을 조회하지 않았으며, 서명 값·방식 보존으로 호환 조건을 유지했다.

세 서비스의 운영 공동 검증에서 합성 사용자 두 명의 공유 키 인증과 사용자 구분, 사용량 이벤트 6개, 키 폐기 후 인증 차단을 확인했다. 기존 토플 DB 키도 세 서비스의 두 URL 별칭에서 모두 인증됐다. 합성 데이터 정리 후 사용자 2개·키 1개·계약 8개·사용량 231개로 원래 DB 상태가 확인됐다. 고객 `.env`나 키 값을 변경하지 않았고 영구 고객 키 발급·교체, 기존 릴리스 소유권 귀속, 새 산출물 publish는 수행하지 않았다.

`deployment-20261008-before.json`은 rollback 기준, `deployment-20261008-plan.json`과 `deployment-20261008-candidate.json`은 후보 단계의 트래픽 0% 기록, `deployment-20261008-smoke.json`은 후보 경계 검사 기록이다. 이 파일들의 당시 상태는 보존한다. 최종 운영 상태는 이 문서와 `deployment-20261008-production.json`에 기록했다.
