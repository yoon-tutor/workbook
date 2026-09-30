# 직접 MCP PDF 릴리스 배포 검증 (2026-09-27)

- 운영 revision: `workbook-runtime-stage9-00010-jih`, 트래픽 100%.
- Cloud Build: `575bc36e-cffb-4059-89c4-7de9bc9c55da`, 성공. 로컬 Docker는 사용하지 않았다.
- 이미지 digest: `sha256:eb2cd951d518abdc9729cddafd3b3c8cf9d4ea6ad36698f27a1ccb6561687e46`.
- 런타임 ID: `8a526dec4e625aa46ecf89f5b6ebee7eca7473325d477b3029abd50e2fb5d761`; 운영 `workbook_get_guidance`와 공용 배포본 `runtime.lock.json`이 일치한다.
- 운영 API: `directApiVersion: 2`, 작성·검증·prepare·검수 이미지·publish·산출물 조회/다운로드 도구를 제공한다.
- 비공개 서울 버킷 `gs://workbook-release-stage9-yoontutor-507902`: uniform bucket access, public access prevention, 준비본·검수 기록 30일 삭제. 서비스 계정에는 이 버킷의 `roles/storage.objectUser`만 부여했다.

승인받은 `chocolate` 예제로 후보 MCP에 정본과 업데이트 JSON을 전송했다. 서버가 학생용·해설용 PDF 각 22쪽을 생성하고 자동 QA를 통과했다. 반환된 검수 이미지 26개를 받아 학생용·해설용 contact sheet와 대표 전체 페이지의 빈칸, 작성 영역, 정답 노출, 잘림·겹침을 시각 확인했다. `publish` 후 HTML/PDF 네 파일을 후보 주소에서 내려받아 서버 기록의 크기·SHA-256과 일치함을 확인했다. 운영 트래픽 전환 후 기본 주소에서 같은 네 서명 링크가 정상 다운로드되고 해시가 일치함을 재확인했다. 23번 원문은 이 시험에 사용하지 않았다.

회귀 검증: 릴리스 테스트 7개 통과·플랫폼 전용 1개 건너뜀, MCP 계약 15개 통과, 공용 배포본 `.env` 인증 헬퍼/ZIP 테스트 2개 통과. 공용 ZIP: `distribution/workbook-maker.zip`, SHA-256 `437f92c31dee462f5e36c8f9189eb8b374c9033bcf86c378905de7fffcd6e0e8`.

현재 Windows의 `codex-cli 0.144.3`은 `http_headers_helper`를 MCP 인증 방식으로 표시하지 않는다(`codex mcp list`: `workbook_runtime` Auth `Unsupported`). 따라서 이 CLI에서는 배포 ZIP의 도구 연결이 검증되지 않았다. 배포본 README는 해당 설정을 지원하는 Codex에서 새 프로젝트로 열도록 안내한다. Mac의 Codex 버전과 도구 노출은 이 Windows 환경에서 직접 확인할 수 없다.
