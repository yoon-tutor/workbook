# 워크북 MCP 운영

배포·운영 절차와 현재 운영 상태를 기록한다. 공통 규칙은 [STANDARD.md](STANDARD.md) 9장을 따른다. 서비스 설정의 원본은 `server/service.json`, 마지막 빌드·배포 결과는 `server/deploy-state.json`(deploy.py가 기록)이다.

## 구성

| 항목 | 값 |
|---|---|
| 프로젝트 / 리전 | `yoontutor-507902` / `asia-northeast1`(도쿄) |
| Cloud Run 서비스 / Artifact Registry | `workbook-maker` / `workbook-maker` (이미지 `.../workbook-maker/server`) |
| 실행 서비스 계정 | `workbook-runtime@yoontutor-507902.iam.gserviceaccount.com` (기존 계정) |
| 자원 | CPU 2, 메모리 2Gi, 동시 요청 1, 최대 인스턴스 1, 최소 0, 요청 제한 900초, 요청 기반 과금 |
| 환경값 | `MCP_SHARED_SCHEMA=public`, `WORKBOOK_RELEASE_BUCKET=workbook-release-an1-yoontutor-507902`, `WORKBOOK_PUBLIC_ORIGIN={service_url}`, `MCP_ALLOWED_HOSTS`·`SERVICE_VERSION`(deploy.py 자동) |
| Secret | `DATABASE_URL=toefl-maker-database-url:1`, `WORKBOOK_ARTIFACT_SIGNING_SECRET=workbook-runtime-token:1` |
| 상태 점검 | `/health`(생존), `/ready`(공유 DB 연결, 실패 시 503). Cloud Run이 `z`로 끝나는 경로를 예약하므로 `/healthz`는 로컬 호환용만 |

PDF 생성(Chromium)은 인스턴스 안에서 요청마다 별도 worker 프로세스로 하나씩 실행한다. 동시 요청 1과 최대 인스턴스 1은 렌더링 직렬화와 메모리 2Gi 안의 Chromium 실행을 위한 값이다.

## 인증·사용량

HTTP 서버는 토플 서버와 같은 `DATABASE_URL`, 같은 `MCP_SHARED_SCHEMA`를 사용한다. 공유 `users`·`api_keys`·`usage_events`를 쓰고 워크북 전용 사용자·키 테이블을 만들지 않는다. 사용자 키는 `tm_` 접두사 키이며 배포본 `.env`의 `MCP_API_TOKEN`에 들어간다. 서버는 시작할 때 마이그레이션하지 않고 테이블 존재만 확인한다. 사용량 이벤트에는 사용자·서비스·도구·상태·처리 시간만 기록하고 원문·정본·키·산출물은 넣지 않는다.

Host/Origin 검사는 공통 런타임이 한다. `MCP_ALLOWED_HOSTS`는 deploy.py가 서비스 URL에서 넣는다. 브라우저 Origin이 필요할 때만 `service.json`의 `run.allowed_origins`에 정확한 HTTPS Origin을 둔다.

## 릴리스 저장소와 다운로드 서명

릴리스 버킷은 비공개다. 객체 구성:

| 접두사 | 내용 | 보존 |
|---|---|---|
| `prepared/<id>.zip` | prepare 결과(입력·빌드·QA·검수 이미지) | 30일 후 삭제 |
| `reviewed/<id>/<이미지>.json` | 검수 이미지 전달 기록 | 30일 후 삭제 |
| `published/<id>/files/`, `evidence/`, `metadata.json` | 공개 네 파일, 보고서·QA 근거, 소유자·해시 | 보존 |
| `tenants/<user_id SHA-256>/history/`, `published/`, `locks/` | 사용자별 버전 이력·공개 기록·작업 잠금 | 보존 (잠금은 작업 후 삭제) |

수명 주기 규칙은 `server/config/direct-release-bucket-lifecycle.json`이다. 서비스 계정에는 이 버킷에 한정한 `roles/storage.objectUser`를 준다.

prepare·review·publish·산출물 조회는 소유자(`ownerId`)가 일치해야 한다. 작업이 비정상 종료되어 `tenants/.../locks/...json`이 남으면 실제 작업이 끝났는지 확인한 뒤 그 객체만 지운다. 자동 만료로 잠금을 풀지 않는다. 소유자 없는 기존 릴리스는 MCP에서 자동 귀속하지 않는다. 관리자가 원래 고객을 확인한 뒤 `python server/scripts/adopt_legacy_release.py --release-id <ID> --owner-id <공유 DB 사용자 ID> --confirm-owner-assignment`로 귀속한다(DATABASE_URL과 WORKBOOK_RELEASE_BUCKET 필요).

공개 파일은 산출물 묶음(`mcp-artifact-bundle-v1`)의 `url` 항목으로 전달된다. URL은 `WORKBOOK_PUBLIC_ORIGIN/artifact/<id>/<파일>?expires=..&signature=..` 형식의 하루짜리 capability URL이며, 항목에는 공개 시 기록한 SHA-256과 크기가 들어 있어 클라이언트가 검증 후 저장한다. 4MB를 넘는 검수 이미지는 같은 방식의 `/review-image/<id>/<이미지>` 링크로, 그 이하는 base64로 전달한다. `WORKBOOK_ARTIFACT_INLINE_MAX_BYTES`(기본 0)를 주면 그 크기 이하의 공개 파일은 링크 대신 본문에 넣는다. `workbook_read_artifact`는 4MB 이하 파일을 항상 본문으로 준다.

서명 키는 서버 전용 `WORKBOOK_ARTIFACT_SIGNING_SECRET`(Secret `workbook-runtime-token`)이며 사용자 API 키와 분리한다. 서명 메시지 형식은 이전과 같다. 2.0.0에서 `WORKBOOK_MCP_API_TOKEN` 대체 사용을 제거했다. 새 값을 만들 때는 `python server/scripts/create_artifact_signing_secret.py`(값은 `.build/deployment/`에만 쓰고 출력하지 않음)로 만든 뒤 Secret Manager에 새 숫자 버전으로 올리고 `service.json`의 참조를 바꾼다. 키를 바꾸면 이미 발급한 링크가 무효가 된다.

## 배포 절차

```bash
python -X utf8 -m unittest discover -s server/tests -v
python server/scripts/audit_client.py
python ../../_standard/sync.py . --check
python server/scripts/deploy.py setup     # Artifact Registry·정리 정책·서비스 계정·Secret 접근 권한
python server/scripts/deploy.py build     # build.context allowlist로 Cloud Build, digest 기록
python server/scripts/deploy.py deploy    # 기록된 digest로 배포, Host·SERVICE_VERSION·{service_url} 확정
python server/scripts/deploy.py smoke     # /health, /ready
python server/scripts/sandbox_client.py --force
python server/scripts/smoke_live.py [--release]
```

`deploy.py setup`은 버킷을 만들지 않는다. 도쿄 버킷과 버킷 권한은 처음 한 번 아래처럼 준비한다.

```bash
gcloud storage buckets create gs://workbook-release-an1-yoontutor-507902 --project=yoontutor-507902 \
  --location=asia-northeast1 --uniform-bucket-level-access --public-access-prevention
gcloud storage buckets update gs://workbook-release-an1-yoontutor-507902 \
  --lifecycle-file=server/config/direct-release-bucket-lifecycle.json
gcloud storage buckets add-iam-policy-binding gs://workbook-release-an1-yoontutor-507902 \
  --member=serviceAccount:workbook-runtime@yoontutor-507902.iam.gserviceaccount.com --role=roles/storage.objectUser
```

`smoke_live.py`는 샌드박스 배포본(`~/agent-sandbox/workbook-maker`, `client/.env` 사용)으로 잘못된 키 거부, ping, guidance, 정본 검사를 확인한다. `--release`는 예시 정본으로 prepare·검수 이미지 수신·publish·네 파일 해시 확인까지 실행하며, 그 키 사용자의 공개 릴리스가 하나 생긴다. 결과는 `docs/reports/<날짜>-cloud-run-smoke.json`에 남는다.

사용자 배포 zip은 `python server/scripts/build_release.py --user <이름> --key-file <키 파일>`로 만든다(`releases/`, git 제외). 2.0.0은 MAJOR 변경이므로 기존 사용자 배포본(`.codex/config.toml`·`runtime.lock.json` 방식)을 모두 새 zip으로 교체한다.

## 운영 이력

| 날짜 | 내용 |
|---|---|
| 2026-09-22 | 원격 MCP가 고정 runtime 패키지를 내려주고 로컬에서 엔진을 실행하는 구조로 배포(당시 문서는 git 기록의 `others/docs/remote-mcp-migration.md`). |
| 2026-09-27 | 서버 직접 PDF 릴리스(directApiVersion 2): prepare → 검수 이미지 → publish, 서울 버킷 `workbook-release-stage9-yoontutor-507902`(30일 수명 주기). |
| 2026-10-06 | 서비스 이름을 `workbook-runtime-stage9`에서 `workbook-maker`로 변경(`docs/reports/remote-mcp/workbook-maker-rename-20261006.md`). |
| 2026-10-08 | 공유 DB 인증·사용량 적용. 서울 `asia-northeast3` revision `workbook-maker-00004-muq` 트래픽 100%, 이미지 `asia-northeast3-docker.pkg.dev/yoontutor-507902/cloud-run-source-deploy/workbook-maker@sha256:0b937bd92f72e39cb8c4276ed2003003413a8f7b6c30731762e5860bf6008fb7`, URL `https://workbook-maker-972256519381.asia-northeast3.run.app/mcp`, `https://workbook-maker-yzxn4wai2a-du.a.run.app/mcp`. CPU 2, 2Gi, 동시 요청 1, 최대 인스턴스 1, timeout 900초(`docs/reports/remote-mcp/deployment-20261008-production.md`). |
| 2026-10-09 | 2.0.0-beta.1 저장소 표준화 후 도쿄 `asia-northeast1` 배포. revision `workbook-maker-00003-qqf`(2026-10-10 베타 버전 표기 재배포, 최초 `00002-mgx`), URL `https://workbook-maker-yzxn4wai2a-an.a.run.app/mcp`, digest `sha256:70921f39c03ddfe62643a88c2a7be3571dde99b2fe3e97afc66a2a1180c2bed5`, 버킷 `gs://workbook-release-an1-yoontutor-507902`(서울 버킷 객체 복사). 운영 점검 `smoke_live.py --release` 통과: 22쪽, 검수 이미지 26장, 네 파일 해시 확인 (`docs/reports/2026-10-09-cloud-run-smoke.json`). 서울 서비스·버킷은 배포본 교체 후 별도 승인으로 정리한다. |

### 서울 → 도쿄 전환 메모

- 서울 버킷에는 2026-10-09 기준 공개 릴리스 2개(`published/`), 전역 이력 2개 워크북(`history/`), 30일 수명의 `prepared/`·`reviewed/`만 있고 `tenants/`가 없다. 모두 소유자 없는 이전 기록이라 현재 서버에서도 어떤 사용자도 MCP로 조회할 수 없다. 새 서버 운영에 복사는 필요 없다. 관리자 귀속(adopt)이 필요해지면 그때 `published/<id>/`와 해당 `history/<slug>/`를 도쿄 버킷으로 복사한 뒤 귀속한다.
- 이전 서울 서버가 발급한 다운로드 링크는 서울 주소를 가리키므로 서울 서비스를 내리면 끊긴다(최대 하루짜리).
- 도쿄 검증(`smoke`, `smoke_live.py --release`)과 사용자 배포본 교체가 끝난 뒤 서울 서비스·이미지·버킷을 정리한다.
