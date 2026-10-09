# 업데이트 보고서 `U-20260711-002`: Soccer Jersey Swap 10단계 워크북 신규 등록

## 요약

제공된 시험 지문 이미지를 단일 canonical 정본으로 전사하고 학생용·해설용 10단계 워크북을 생성합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260711-002` |
| 날짜 | 2026-07-11 |
| 분류 | `new-content` |
| 적용 범위 | `new-only` — 신규 워크북만 |

## 요청 내용

- Soccer Jersey Swap 지문으로 10단계 워크북 제작을 시작합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | — | 1.0.0 | `44136fa355b3` | `7fab4f3db2cf` | 변경 |
| spec | — | 1.0.0 | `44136fa355b3` | `8203ec9e777c` | 변경 |
| template | — | 1.0.1 | `44136fa355b3` | `6456357b00c6` | 변경 |
| build | — | 1.0.0 | `44136fa355b3` | `d3a665c7c84c` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | added | — | {"sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","s… |
| 파생 | build | `workbook_engine/__main__.py` | added | — | {"sha256":"4abb421f270f4e5fb739aaac7d68ba89c65c17df0099564abcd730d95ca777e8","s… |
| 파생 | build | `workbook_engine/change_report.py` | added | — | {"sha256":"b70b6885ba408923d66b6eabd9280081eb22aa0e00fd51b53b54b9c830ee9c89","s… |
| 파생 | build | `workbook_engine/compiler.py` | added | — | {"sha256":"9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163","s… |
| 파생 | build | `workbook_engine/manifest.py` | added | — | {"sha256":"046fe32ef8bc39f1f11bac7b11ed368e5697e96d453fa3a425f89f58edcdfee6","s… |
| 파생 | build | `workbook_engine/migrate_legacy.py` | added | — | {"sha256":"724a9f9e08c22d48d8f884ebf0629f1699b7542303685bff96192d2326e4d714","s… |
| 파생 | build | `workbook_engine/paginator.py` | added | — | {"sha256":"241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d","s… |
| 파생 | build | `workbook_engine/qa.py` | added | — | {"sha256":"42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2","s… |
| 파생 | build | `workbook_engine/release.py` | added | — | {"sha256":"53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6","s… |
| 파생 | build | `workbook_engine/render.py` | added | — | {"sha256":"8f6e83f0709c29001c1ec07acdd0c3db2095844b71f42362503918f045765053","s… |
| 파생 | build | `workbook_engine/schema_gate.py` | added | — | {"sha256":"fe4b1014e6bcb1dfe0353d8e6b2dec82745aa7cb92dae78f619c6b371f3e966b","s… |
| 파생 | build | `workbook_engine/textops.py` | added | — | {"sha256":"8bf721d88f5901515b440edb3fee7fd77aee82a8d1858aeac1b8afeb0c77c0f3","s… |
| 파생 | build | `workbook_engine/validator.py` | added | — | {"sha256":"41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee","s… |
| 파생 | build | `문제.html` | added | — | {"sha256":"251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054","s… |
| 파생 | build | `문제.pdf` | added | — | {"sha256":"86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155","s… |
| 파생 | build | `해설.html` | added | — | {"sha256":"dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf","s… |
| 파생 | build | `해설.pdf` | added | — | {"sha256":"0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32","s… |
| 직접 | canonical | `workbooks/soccer-jersey-swap/content.json` | added | — | {"sha256":"2d7b93b3064b9adb74ab53162e451719c941fdd0db548c147c01a99c34c4f807","s… |
| 직접 | declared | `updates/U-20260711-002.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | added | — | {"sha256":"c0a93788f2ee81ac0f5106cc5220e86267b6ecb0a8d89c7a8b996f6b085741cb","s… |
| 직접 | spec | `config/workbook-spec.json` | added | — | {"sha256":"ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61","s… |
| 직접 | spec | `docs/semantic-rubric.md` | added | — | {"sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","s… |
| 직접 | spec | `schemas/canonical-workbook.schema.json` | added | — | {"sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218e6997","s… |
| 직접 | spec | `schemas/update.schema.json` | added | — | {"sha256":"76758164ed8c5bb1349c7c0d338c2d97837647aa19688a50553ed872fbb3dd7f","s… |
| 직접 | template | `assets/yonjogyo-logo-footer.png` | added | — | {"sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | added | — | {"sha256":"b8d6cf61d980afcfa0160d91fe87b73d535cc2ab80bac66964f45a9e0ec2345e","s… |
| 직접 | template | `workbook_engine/templates/shell.html` | added | — | {"sha256":"1a0d56b95811b303e3fa73650dfe1ad690e2531e0628885a16cac72d5476007c","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | added | — | {"sha256":"fbce767b88b805800c5f03a51bfbe5c61985a55131b8624e43ab87acd5de3761","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical` | added | — | {"contentVersion":"1.0.0","metadata":{"grade":"중학교 3학년","kicker":"Middle School Reading","lessonLabel":"Soccer Jersey S… |
| canonical | `$.contentVersion` | added | — | "1.0.0" |
| canonical | `$.files` | added | — | [{"path":"workbooks/soccer-jersey-swap/content.json","sha256":"2d7b93b3064b9adb74ab53162e451719c941fdd0db548c147c01a99c… |
| canonical | `$.workbookId` | added | — | "soccer-jersey-swap" |
| spec | `$.files` | added | — | [{"path":"config/versions.json","sha256":"c0a93788f2ee81ac0f5106cc5220e86267b6ecb0a8d89c7a8b996f6b085741cb","size":1230… |
| spec | `$.schemaFiles` | added | — | [{"path":"schemas/canonical-workbook.schema.json","sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218… |
| spec | `$.semanticRubricFile` | added | — | {"path":"docs/semantic-rubric.md","sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","size":80… |
| spec | `$.semanticRubricVersion` | added | — | "1.0.0" |
| spec | `$.spec` | added | — | {"$id":"https://local.workbook/spec/workbook-spec-1.0.0.json","$schema":"https://json-schema.org/draft/2020-12/schema",… |
| spec | `$.specVersion` | added | — | "1.0.0" |
| template | `$.files` | added | — | [{"path":"assets/yonjogyo-logo-footer.png","sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1",… |
| template | `$.rendererContract` | added | — | "shared-dom-explicit-targets-fail-closed" |
| template | `$.templateVersion` | added | — | "1.0.1" |

## 파생 영향 (파생 변경)

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| build | `$.appliedUpdates` | added | — | ["U-20260711-002"] |
| build | `$.buildVersion` | added | — | "1.0.0" |
| build | `$.builtAt` | added | — | "2026-07-11T14:00:16+09:00" |
| build | `$.canonicalDigest` | added | — | "618e755c1e90b3e0438f3e2f1703b2d795db1cd90474f87918a1606e3d4e7fab" |
| build | `$.compilerVersion` | added | — | "1.0.0" |
| build | `$.contentVersion` | added | — | "1.0.0" |
| build | `$.engineDigest` | added | — | "a199d39b59695c50cdba9ad84a535eaf363eaa1c8a1c325796f361d4ab10a47e" |
| build | `$.engineInputs` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","siz… |
| build | `$.files` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","siz… |
| build | `$.outputs` | added | — | [{"path":"문제.html","sha256":"251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054","size":154824},{"path":"… |
| build | `$.pages` | added | — | [{"digest":"f3241a2b9fd537ec7bb45004a5fa735670b2040cd794b0496c8abad5d9a57252","edition":"student","id":"student:soccer-… |
| build | `$.qa` | added | — | {"contactSheets":["qa/samples/student-contact-sheet.png","qa/samples/answer-contact-sheet.png"],"dom":{"answer":{"pages… |
| build | `$.reportFormatVersion` | added | — | "1.0.0" |
| build | `$.schemaVersion` | added | — | "1.0.0" |
| build | `$.semanticRubricVersion` | added | — | "1.0.0" |
| build | `$.sourceDigest` | added | — | "d819f7db0187d96502a29f51b1ec26bb4d86d38fe231e95217a491f93b896f05" |
| build | `$.specVersion` | added | — | "1.0.0" |
| build | `$.templateVersion` | added | — | "1.0.1" |
| build | `$.validationStatus` | added | — | "passed" |
| build | `$.visualReview` | added | — | {"notes":"학생용·해설용 contact sheet에서 1단계 첫·분할 페이지, 4단계 해석, 7단계 교정 색상, 9단계 문단 순서, 10단계 마지막 페이지를 확인했습니다. 텍스트 잘림·겹침·페이지 초과·학생… |
| build | `$.workbookId` | added | — | "soccer-jersey-swap" |

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:soccer-jersey-swap-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| answer:soccer-jersey-swap-p02 | added | 1 | s013, s014 |
| answer:soccer-jersey-swap-p03 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p04 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p05 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| answer:soccer-jersey-swap-p06 | added | 4 | s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p07 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p08 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p09 | added | 7 | — |
| answer:soccer-jersey-swap-p10 | added | 8 | s001, s002, s003, s004, s005, s006 |
| answer:soccer-jersey-swap-p11 | added | 8 | s007, s008, s009, s010, s011, s012 |
| answer:soccer-jersey-swap-p12 | added | 8 | s013, s014 |
| answer:soccer-jersey-swap-p13 | added | 9 | — |
| answer:soccer-jersey-swap-p14 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:soccer-jersey-swap-p15 | added | 10 | s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| student:soccer-jersey-swap-p02 | added | 1 | s013, s014 |
| student:soccer-jersey-swap-p03 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p04 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p05 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| student:soccer-jersey-swap-p06 | added | 4 | s011, s012, s013, s014 |
| student:soccer-jersey-swap-p07 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p08 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p09 | added | 7 | — |
| student:soccer-jersey-swap-p10 | added | 8 | s001, s002, s003, s004, s005, s006 |
| student:soccer-jersey-swap-p11 | added | 8 | s007, s008, s009, s010, s011, s012 |
| student:soccer-jersey-swap-p12 | added | 8 | s013, s014 |
| student:soccer-jersey-swap-p13 | added | 9 | — |
| student:soccer-jersey-swap-p14 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:soccer-jersey-swap-p15 | added | 10 | s009, s010, s011, s012, s013, s014 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | added | — | {"path":"문제.html","sha256":"251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054","size":154824} |
| `문제.pdf` | added | — | {"path":"문제.pdf","sha256":"86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155","size":697429} |
| `해설.html` | added | — | {"path":"해설.html","sha256":"dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf","size":168651} |
| `해설.pdf` | added | — | {"path":"해설.pdf","sha256":"0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32","size":856243} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 없음
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| release-validation | skipped | canonical 작성 후 실행합니다. |
| source-transcription | pass | 이미지의 14개 문장을 정본에 보존합니다. |

## 호환성

- 적용 범위: `new-only` — 신규 워크북만
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | — | 1.0.0 |
| spec | — | 1.0.0 |
| template | — | 1.0.1 |
| build | — | 1.0.0 |

## 변경 통계

- 직접 JSON 경로: 13
- 파생 JSON 경로: 21
- 변경·선언 파일: 28
- 영향 페이지: 30
- 변경 출력: 4
