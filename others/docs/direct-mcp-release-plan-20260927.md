# 직접 MCP PDF 릴리스 구현 계획

## 구조 비교

1. MCP 응답에 네 파일 전체를 넣기: 서버 상태는 단순하지만 PDF와 QA 이미지가 도구 응답 크기와 모델 컨텍스트를 압박한다.
2. Cloud Run 임시 디스크에 prepare 상태 보관: 기존 엔진을 그대로 호출할 수 있지만 다음 요청이 다른 인스턴스로 가거나 재시작되면 상태가 사라진다.
3. 비공개 Cloud Storage에 prepare 결과를 보존: 기존 엔진의 자동 QA를 그대로 실행하고, 시각 검수와 publish를 분리할 수 있다. 이 경로를 선택한다.

## 순차 실행 및 재개 지점

1. 기존 release 엔진의 입력·출력 계약과 Cloud Run 이미지 의존성을 확인한다. 기존 정본과 공개 결과의 해시는 변경하지 않는다.
2. 서버에 직접 MCP `prepare`, 검수 이미지 조회, `publish`, 산출물 조회 도구를 구현한다. 서버는 입력값을 임시 작업공간에 쓰고 기존 `prepare_release`/`publish_release`를 호출한다. 준비 결과는 비공개 버킷에 저장한다.
3. `gs://workbook-release-stage9-yoontutor-507902` 버킷을 서울 지역에 만들고 공개 접근을 금지한다. 서비스 계정 `workbook-runtime@yoontutor-507902.iam.gserviceaccount.com`에 이 버킷으로 한정한 `roles/storage.objectUser`를 부여한다. 준비 결과와 검수 기록은 30일 후 삭제하고 공개 산출물은 보존한다. 이 변경은 자동 승인 검토가 명시적 승인 부족을 이유로 거부했으므로 사용자 승인 후 진행한다.
4. 로컬 자동 QA 및 시각 검수용 샘플을 실행한다. Cloud Build 이미지와 트래픽 없는 후보 revision을 배포해 도구 목록·인증·오류 처리를 확인한다.
5. 후보에서 실제 PDF 생성과 이미지 조회를 확인한 뒤 활성 트래픽으로 전환한다. 공용 배포본의 `AGENTS.md`, 스킬, README를 갱신한다.

`prepare`는 자동 QA 통과만 의미한다. 학생용·해설용 이미지를 사람이 확인하고 기록을 남기기 전 `publish`하지 않는다. PDF와 HTML을 실제로 내려받아 검증하기 전 최종 산출물 완료로 표시하지 않는다.
