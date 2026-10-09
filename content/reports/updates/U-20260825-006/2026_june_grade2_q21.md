# 업데이트 보고서 `U-20260825-006`: 2026학년도 6월 고2 20·21번 10단계 워크북 신규 등록

## 요약

제공된 2026학년도 6월 고2 전국연합학력평가 PDF의 20번과 21번 지문을 각각 단일 canonical 정본으로 전사하고 학생용·해설용 10단계 워크북을 생성합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260825-006` |
| 날짜 | 2026-08-25 |
| 분류 | `new-content` |
| 적용 범위 | `selected` — 선택 워크북: 2026-june-grade2-q20, 2026-june-grade2-q21 |

## 요청 내용

- 고2 6월 원본 PDF의 20~21번으로 작업을 시작합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | — | 1.0.0 | `44136fa355b3` | `6a5b2ee9a871` | 변경 |
| spec | — | 1.0.2 | `44136fa355b3` | `94237af0a7ed` | 변경 |
| template | — | 1.0.1 | `44136fa355b3` | `6456357b00c6` | 변경 |
| build | — | 1.0.0 | `44136fa355b3` | `24ababc53df7` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | added | — | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… |
| 파생 | build | `workbook_engine/__main__.py` | added | — | {"sha256":"4abb421f270f4e5fb739aaac7d68ba89c65c17df0099564abcd730d95ca777e8","s… |
| 파생 | build | `workbook_engine/change_report.py` | added | — | {"sha256":"b70b6885ba408923d66b6eabd9280081eb22aa0e00fd51b53b54b9c830ee9c89","s… |
| 파생 | build | `workbook_engine/compiler.py` | added | — | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… |
| 파생 | build | `workbook_engine/manifest.py` | added | — | {"sha256":"046fe32ef8bc39f1f11bac7b11ed368e5697e96d453fa3a425f89f58edcdfee6","s… |
| 파생 | build | `workbook_engine/migrate_legacy.py` | added | — | {"sha256":"724a9f9e08c22d48d8f884ebf0629f1699b7542303685bff96192d2326e4d714","s… |
| 파생 | build | `workbook_engine/paginator.py` | added | — | {"sha256":"21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00","s… |
| 파생 | build | `workbook_engine/qa.py` | added | — | {"sha256":"42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2","s… |
| 파생 | build | `workbook_engine/release.py` | added | — | {"sha256":"53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6","s… |
| 파생 | build | `workbook_engine/render.py` | added | — | {"sha256":"8f6e83f0709c29001c1ec07acdd0c3db2095844b71f42362503918f045765053","s… |
| 파생 | build | `workbook_engine/schema_gate.py` | added | — | {"sha256":"fe4b1014e6bcb1dfe0353d8e6b2dec82745aa7cb92dae78f619c6b371f3e966b","s… |
| 파생 | build | `workbook_engine/textops.py` | added | — | {"sha256":"8bf721d88f5901515b440edb3fee7fd77aee82a8d1858aeac1b8afeb0c77c0f3","s… |
| 파생 | build | `workbook_engine/validator.py` | added | — | {"sha256":"9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1","s… |
| 파생 | build | `문제.html` | added | — | {"sha256":"f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d","s… |
| 파생 | build | `문제.pdf` | added | — | {"sha256":"62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db","s… |
| 파생 | build | `해설.html` | added | — | {"sha256":"02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293","s… |
| 파생 | build | `해설.pdf` | added | — | {"sha256":"36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q21/content.json` | added | — | {"sha256":"bfe93c2e32a6c34f659eda70fa31debf795b5e9200a0766e4f8e228a99000323","s… |
| 직접 | declared | `tmp/build_chocolate_reading_json.py` | declared | — | — |
| 직접 | declared | `updates/U-20260825-006.json` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q20/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | added | — | {"sha256":"f97bc280305f46e0b199e68c322318570cbb4787cad785bdd0d70250f83d3f2e","s… |
| 직접 | spec | `config/workbook-spec.json` | added | — | {"sha256":"8bea1dedad1775ad890f36a07ca0f4e1cb2b031b94346edfe3593b6a04f83b7d","s… |
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
| canonical | `$.canonical` | added | — | {"$schema":"../../schemas/canonical-workbook.schema.json","contentVersion":"1.0.0","metadata":{"grade":"고등학교 2학년","kick… |
| canonical | `$.contentVersion` | added | — | "1.0.0" |
| canonical | `$.files` | added | — | [{"path":"workbooks/2026-june-grade2-q21/content.json","sha256":"bfe93c2e32a6c34f659eda70fa31debf795b5e9200a0766e4f8e22… |
| canonical | `$.workbookId` | added | — | "2026-june-grade2-q21" |
| spec | `$.files` | added | — | [{"path":"config/versions.json","sha256":"f97bc280305f46e0b199e68c322318570cbb4787cad785bdd0d70250f83d3f2e","size":1348… |
| spec | `$.schemaFiles` | added | — | [{"path":"schemas/canonical-workbook.schema.json","sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218… |
| spec | `$.semanticRubricFile` | added | — | {"path":"docs/semantic-rubric.md","sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","size":80… |
| spec | `$.semanticRubricVersion` | added | — | "1.0.0" |
| spec | `$.spec` | added | — | {"$id":"https://local.workbook/spec/workbook-spec-1.0.0.json","$schema":"https://json-schema.org/draft/2020-12/schema",… |
| spec | `$.specVersion` | added | — | "1.0.2" |
| template | `$.files` | added | — | [{"path":"assets/yonjogyo-logo-footer.png","sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1",… |
| template | `$.rendererContract` | added | — | "shared-dom-explicit-targets-fail-closed" |
| template | `$.templateVersion` | added | — | "1.0.1" |

## 파생 영향 (파생 변경)

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| build | `$.appliedUpdates` | added | — | ["U-20260825-006"] |
| build | `$.buildVersion` | added | — | "1.0.0" |
| build | `$.builtAt` | added | — | "2026-08-25T15:54:47+09:00" |
| build | `$.canonicalDigest` | added | — | "540168f50b779cdbe563fa84df71dae8abf7900b5e1319d91d06add07e58043c" |
| build | `$.compilerVersion` | added | — | "1.0.2" |
| build | `$.contentVersion` | added | — | "1.0.0" |
| build | `$.engineDigest` | added | — | "b51bb9b758b4a296e3e5fa03c8af783a3626209e4cb1ee0cd519a6394e903d40" |
| build | `$.engineInputs` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","siz… |
| build | `$.files` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","siz… |
| build | `$.outputs` | added | — | [{"path":"문제.html","sha256":"f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d","size":135532},{"path":"… |
| build | `$.pages` | added | — | [{"digest":"8bbbf03aca57d4beb0235abc5172eea361bb9324437444684c1f3dbe87beae67","edition":"student","id":"student:2026-ju… |
| build | `$.qa` | added | — | {"contactSheets":["qa/samples/student-contact-sheet.png","qa/samples/answer-contact-sheet.png"],"dom":{"answer":{"pages… |
| build | `$.reportFormatVersion` | added | — | "1.0.0" |
| build | `$.schemaVersion` | added | — | "1.0.0" |
| build | `$.semanticRubricVersion` | added | — | "1.0.0" |
| build | `$.sourceDigest` | added | — | "d6302a49d275b6d670e630fe7362e1ce0dacf9a8a6d983fef34ecaa437ed60bb" |
| build | `$.specVersion` | added | — | "1.0.2" |
| build | `$.templateVersion` | added | — | "1.0.1" |
| build | `$.validationStatus` | added | — | "passed" |
| build | `$.visualReview` | added | — | {"notes":"학생용·해설용 접촉 시트와 1·7·8·9·10단계, 8단계 1-4 및 5-8 연속 페이지를 확인함. 7단계 is 목표 위치가 representations is에 정확하며, 해설 정답만 빨강이고 모… |
| build | `$.workbookId` | added | — | "2026-june-grade2-q21" |

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:2026-june-grade2-q21-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p02 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p03 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p04 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p05 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p06 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p07 | added | 7 | — |
| answer:2026-june-grade2-q21-p08 | added | 8 | s001, s002, s003, s004 |
| answer:2026-june-grade2-q21-p09 | added | 8 | s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p10 | added | 9 | — |
| answer:2026-june-grade2-q21-p11 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p02 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p03 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p04 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p05 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p06 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p07 | added | 7 | — |
| student:2026-june-grade2-q21-p08 | added | 8 | s001, s002, s003, s004 |
| student:2026-june-grade2-q21-p09 | added | 8 | s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p10 | added | 9 | — |
| student:2026-june-grade2-q21-p11 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | added | — | {"path":"문제.html","sha256":"f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d","size":135532} |
| `문제.pdf` | added | — | {"path":"문제.pdf","sha256":"62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db","size":604376} |
| `해설.html` | added | — | {"path":"해설.html","sha256":"02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293","size":144674} |
| `해설.pdf` | added | — | {"path":"해설.pdf","sha256":"36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39","size":736196} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 없음
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| legacy-test-fixture-restoration | pass | 기존 테스트가 참조하던 누락 자료를 정본에 기록된 SHA-256 값과 일치하는 보관본으로 복원했습니다. 새 20·21번 정본 작성에는 사용하지 않았습니다. |
| release-validation | pass | 두 canonical의 스키마·구조 검증이 통과했고 전체 단위 테스트 31개가 통과했습니다. |
| source-question-cross-check | pass | 20번 주장 문항의 정답 ③과 21번 밑줄 의미 문항의 정답 ①을 지문 의미 검토에 교차 사용했습니다. |
| source-transcription | pass | 원본 PDF 2쪽의 20번과 3쪽의 21번을 렌더링해 본문 단어, 대소문자, 문장부호를 시각 확인했습니다. |

## 호환성

- 적용 범위: `selected` — 선택 워크북: 2026-june-grade2-q20, 2026-june-grade2-q21
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | — | 1.0.0 |
| spec | — | 1.0.2 |
| template | — | 1.0.1 |
| build | — | 1.0.0 |

## 변경 통계

- 직접 JSON 경로: 13
- 파생 JSON 경로: 21
- 변경·선언 파일: 30
- 영향 페이지: 22
- 변경 출력: 4
