---
name: workbook-release
description: Codex가 원격 Workbook MCP 도구로 영어 10단계 워크북을 작성, PDF 검수, 공개한다.
---

1. 인증 토큰은 배포 폴더의 `.env`에서만 읽는다. 채팅에서 토큰을 요구하거나 세션에 저장된 값을 대신 사용하지 않는다. 프로젝트 MCP 설정의 `http_headers_helper`가 연결 시 `.env`를 읽는다. `workbook_runtime` MCP 연결을 확인하고 `workbook_get_guidance`를 호출한다. 반환된 `runtimeId`가 `runtime.lock.json`과 다르면 중단한다. 도구가 보이지 않으면 프로젝트가 신뢰되었는지, `.codex/config.toml`과 `.env`가 있는지, Codex가 `http_headers_helper`를 지원하는지, `python3`가 실행되는지 확인한다. MCP 등록·인증 오류를 구분해 보고하고 PDF 작업을 진행하지 않는다.
2. `inputs/`의 원본을 확인해 통합 authoring packet을 `.build/authoring/<이름>/authoring.json`에 작성한다. 원본 문장·선택지·정답이 불명확하면 추측하지 않는다.
3. `workbook_authoring_verify`와 `workbook_authoring_expand`로 packet을 검증·확장하고 반환 정본을 `workbooks/<이름>/content.json`에 저장한다. 기존 검토 정본을 덮어쓰지 않는다. `workbook_validate_canonical`로 정본을 다시 검증한다.
4. `directApiVersion: 2`와 `workbook_prepare_release`가 확인되면 검증된 canonical과 update JSON을 직접 전달한다. 반환 상태는 자동 QA 통과·시각 검수 대기다. `workbook_compile`의 중간 IR이나 prepare를 최종 릴리스로 취급하지 않는다.
5. `reviewImages`의 모든 이름에 `workbook_review_image`를 호출해 학생용·해설용 contact sheet와 대표 전체 페이지를 실제로 본다. 2·3단계 빈칸, 4·8·10단계 작성형, 학생 정답 노출, 해설 정답, 잘림·겹침을 직접 확인한다. 자동 검증과 시각 검수는 별개다.
6. 결함이 없으면 `workbook_publish_release`에 release ID, 검수자, 구체적인 검수 기록을 전달한다. 반환된 네 HTML/PDF의 크기·SHA-256·다운로드 주소를 확인하고 실제 산출물을 내려받아 `outputs/`에 저장한다. PDF는 `workbook_read_artifact`로 MCP 파일로도 받을 수 있다. 링크가 만료되면 `workbook_get_artifacts`로 갱신한다. 네 파일과 검수 기록이 확인되기 전 완료로 보고하지 않는다.

9단계는 지문 전체 문장을 A·B·C 선택지에 빠짐없이 배분하고 `answerOrder`는 원문 복원 순서로 쓴다. 서버가 실패하면 로컬 엔진이나 추측으로 대체하지 않는다.
