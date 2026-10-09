# 업데이트 보고서 `U-20260903-016`: 2026학년도 6월 고2 30·31번 10단계 워크북 신규 등록

## 요약

제공된 2026학년도 6월 고2 전국연합학력평가 PDF의 30번과 31번 지문을 각각 단일 canonical 정본으로 전사하고 학생용·해설용 10단계 워크북을 생성합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260903-016` |
| 날짜 | 2026-09-03 |
| 분류 | `new-content` |
| 적용 범위 | `selected` — 선택 워크북: 2026-june-grade2-q30, 2026-june-grade2-q31 |

## 요청 내용

- 고2 6월 원본 PDF의 30, 31번으로 작업을 시작합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | — | 1.0.0 | `44136fa355b3` | `8efc92413d19` | 변경 |
| spec | — | 1.0.6 | `44136fa355b3` | `b931803338b2` | 변경 |
| template | — | 1.0.4 | `44136fa355b3` | `248f772c4818` | 변경 |
| build | — | 1.0.0 | `44136fa355b3` | `fed43119ad2b` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | added | — | {"sha256":"af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd","s… |
| 파생 | build | `workbook_engine/__main__.py` | added | — | {"sha256":"4abb421f270f4e5fb739aaac7d68ba89c65c17df0099564abcd730d95ca777e8","s… |
| 파생 | build | `workbook_engine/change_report.py` | added | — | {"sha256":"b70b6885ba408923d66b6eabd9280081eb22aa0e00fd51b53b54b9c830ee9c89","s… |
| 파생 | build | `workbook_engine/compiler.py` | added | — | {"sha256":"30f60ef9ddb93dd7a8d3462a0fccb652ada4ae2d5703d5c2928ed6f7a65785b8","s… |
| 파생 | build | `workbook_engine/manifest.py` | added | — | {"sha256":"046fe32ef8bc39f1f11bac7b11ed368e5697e96d453fa3a425f89f58edcdfee6","s… |
| 파생 | build | `workbook_engine/migrate_legacy.py` | added | — | {"sha256":"724a9f9e08c22d48d8f884ebf0629f1699b7542303685bff96192d2326e4d714","s… |
| 파생 | build | `workbook_engine/paginator.py` | added | — | {"sha256":"21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00","s… |
| 파생 | build | `workbook_engine/qa.py` | added | — | {"sha256":"24b628516d4feacd50a3bc7b18cafdd9d9c8d96246b33f69f9eeea8d327ba604","s… |
| 파생 | build | `workbook_engine/release.py` | added | — | {"sha256":"097925500dc84f6a4bc13efab144343fcd4d6dbe1f1685fe1db5e87a7c90501e","s… |
| 파생 | build | `workbook_engine/render.py` | added | — | {"sha256":"8f6e83f0709c29001c1ec07acdd0c3db2095844b71f42362503918f045765053","s… |
| 파생 | build | `workbook_engine/schema_gate.py` | added | — | {"sha256":"fe4b1014e6bcb1dfe0353d8e6b2dec82745aa7cb92dae78f619c6b371f3e966b","s… |
| 파생 | build | `workbook_engine/textops.py` | added | — | {"sha256":"8bf721d88f5901515b440edb3fee7fd77aee82a8d1858aeac1b8afeb0c77c0f3","s… |
| 파생 | build | `workbook_engine/validator.py` | added | — | {"sha256":"9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1","s… |
| 파생 | build | `문제.html` | added | — | {"sha256":"dbc9f9b66af2834a34ce3d9b66f8ec3ed4a318fbc52cba25d18ae720ca5d0390","s… |
| 파생 | build | `문제.pdf` | added | — | {"sha256":"275a3790fff676c887b7652aebc0f0f5c0582d57aa80f5bb15cdfbc836dc5852","s… |
| 파생 | build | `해설.html` | added | — | {"sha256":"06b5c12d54f4602a3683a21aeb1478e2bcc586de7eac6370e7e6342fe961bb5f","s… |
| 파생 | build | `해설.pdf` | added | — | {"sha256":"446b075e8d25f314d0a390679c4e2704a0f042a8d5fc4cb573e2e370c32d943d","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q30/content.json` | added | — | {"sha256":"4dffa6eabf880f2bf8514c1e2a77d6a0f1bd0a9649647af57e36658afc6b8d20","s… |
| 직접 | declared | `updates/U-20260903-016.json` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q31/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | added | — | {"sha256":"ca932853263987cc7d3cdbab03c49e6e931ff9ea8f0387ebb438c4a513a9f872","s… |
| 직접 | spec | `config/workbook-spec.json` | added | — | {"sha256":"aadb3fe161b100e3a68ecb42fab51775e9738153a04278a53b27e7172f8d8f69","s… |
| 직접 | spec | `docs/semantic-rubric.md` | added | — | {"sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","s… |
| 직접 | spec | `schemas/canonical-workbook.schema.json` | added | — | {"sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218e6997","s… |
| 직접 | spec | `schemas/update.schema.json` | added | — | {"sha256":"76758164ed8c5bb1349c7c0d338c2d97837647aa19688a50553ed872fbb3dd7f","s… |
| 직접 | template | `assets/yonjogyo-logo-footer.png` | added | — | {"sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | added | — | {"sha256":"25a21d18af7ee1100e7a4d0023af1175140e82dd2cce2a246d0fcd5ece2411ee","s… |
| 직접 | template | `workbook_engine/templates/shell.html` | added | — | {"sha256":"1a0d56b95811b303e3fa73650dfe1ad690e2531e0628885a16cac72d5476007c","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | added | — | {"sha256":"ceab51f4246462f507a1de7c6aea850fb577113c37e74b4d98a645f23744a330","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical` | added | — | {"$schema":"../../schemas/canonical-workbook.schema.json","contentVersion":"1.0.0","metadata":{"grade":"고등학교 2학년","kick… |
| canonical | `$.contentVersion` | added | — | "1.0.0" |
| canonical | `$.files` | added | — | [{"path":"workbooks/2026-june-grade2-q30/content.json","sha256":"4dffa6eabf880f2bf8514c1e2a77d6a0f1bd0a9649647af57e3665… |
| canonical | `$.workbookId` | added | — | "2026-june-grade2-q30" |
| spec | `$.files` | added | — | [{"path":"config/versions.json","sha256":"ca932853263987cc7d3cdbab03c49e6e931ff9ea8f0387ebb438c4a513a9f872","size":1687… |
| spec | `$.schemaFiles` | added | — | [{"path":"schemas/canonical-workbook.schema.json","sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218… |
| spec | `$.semanticRubricFile` | added | — | {"path":"docs/semantic-rubric.md","sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","size":80… |
| spec | `$.semanticRubricVersion` | added | — | "1.0.0" |
| spec | `$.spec` | added | — | {"$id":"https://local.workbook/spec/workbook-spec-1.0.0.json","$schema":"https://json-schema.org/draft/2020-12/schema",… |
| spec | `$.specVersion` | added | — | "1.0.6" |
| template | `$.files` | added | — | [{"path":"assets/yonjogyo-logo-footer.png","sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1",… |
| template | `$.rendererContract` | added | — | "shared-dom-explicit-targets-fail-closed" |
| template | `$.templateVersion` | added | — | "1.0.4" |

## 파생 영향 (파생 변경)

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| build | `$.appliedUpdates` | added | — | ["U-20260903-016"] |
| build | `$.buildVersion` | added | — | "1.0.0" |
| build | `$.builtAt` | added | — | "2026-09-03T15:13:50+09:00" |
| build | `$.canonicalDigest` | added | — | "f40952eba5c4018c5f459de64868c5c631993c698516885c4d8d89ae59d80909" |
| build | `$.compilerVersion` | added | — | "1.0.7" |
| build | `$.contentVersion` | added | — | "1.0.0" |
| build | `$.engineDigest` | added | — | "755fa39f2f38e0c481da489f7b37fc92110b71ae3cf018dda83004df187ac114" |
| build | `$.engineInputs` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd","siz… |
| build | `$.files` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd","siz… |
| build | `$.outputs` | added | — | [{"path":"문제.html","sha256":"dbc9f9b66af2834a34ce3d9b66f8ec3ed4a318fbc52cba25d18ae720ca5d0390","size":147369},{"path":"… |
| build | `$.pages` | added | — | [{"digest":"2a89b1c93f6af1df2b95cd9503af64ba3c002399fa8b31aceab45167b9d7d7b8","edition":"student","id":"student:2026-ju… |
| build | `$.qa` | added | — | {"contactSheets":["qa/samples/student-contact-sheet.png","qa/samples/answer-contact-sheet.png"],"dom":{"answer":{"pages… |
| build | `$.reportFormatVersion` | added | — | "1.0.0" |
| build | `$.schemaVersion` | added | — | "1.0.0" |
| build | `$.semanticRubricVersion` | added | — | "1.0.0" |
| build | `$.sourceDigest` | added | — | "5a61a286decb599adc7f50f7a4f206831de6236cbbf10868b3f6003217381481" |
| build | `$.specVersion` | added | — | "1.0.6" |
| build | `$.templateVersion` | added | — | "1.0.4" |
| build | `$.validationStatus` | added | — | "passed" |
| build | `$.visualReview` | added | — | {"notes":"학생용·해설용 11쪽 전체 contact sheet와 7단계 상세 페이지를 확인했습니다. 1단계 다음 part, 2·3단계 빈칸, 4·8·10단계 작성 영역, 7단계 교정 색상, 9단계 문단 순서… |
| build | `$.workbookId` | added | — | "2026-june-grade2-q30" |

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:2026-june-grade2-q30-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p02 | added | 2 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p03 | added | 3 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p04 | added | 4 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p05 | added | 5 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p06 | added | 6 | s001, s002, s003, s004, s005, s006, s007 |
| answer:2026-june-grade2-q30-p07 | added | 7 | — |
| answer:2026-june-grade2-q30-p08 | added | 8 | s001, s002, s003, s004 |
| answer:2026-june-grade2-q30-p09 | added | 8 | s005, s006, s007 |
| answer:2026-june-grade2-q30-p10 | added | 9 | — |
| answer:2026-june-grade2-q30-p11 | added | 10 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p02 | added | 2 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p03 | added | 3 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p04 | added | 4 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p05 | added | 5 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p06 | added | 6 | s001, s002, s003, s004, s005, s006, s007 |
| student:2026-june-grade2-q30-p07 | added | 7 | — |
| student:2026-june-grade2-q30-p08 | added | 8 | s001, s002, s003, s004 |
| student:2026-june-grade2-q30-p09 | added | 8 | s005, s006, s007 |
| student:2026-june-grade2-q30-p10 | added | 9 | — |
| student:2026-june-grade2-q30-p11 | added | 10 | s001, s002, s003, s004, s005, s006, s007 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | added | — | {"path":"문제.html","sha256":"dbc9f9b66af2834a34ce3d9b66f8ec3ed4a318fbc52cba25d18ae720ca5d0390","size":147369} |
| `문제.pdf` | added | — | {"path":"문제.pdf","sha256":"275a3790fff676c887b7652aebc0f0f5c0582d57aa80f5bb15cdfbc836dc5852","size":606135} |
| `해설.html` | added | — | {"path":"해설.html","sha256":"06b5c12d54f4602a3683a21aeb1478e2bcc586de7eac6370e7e6342fe961bb5f","size":158080} |
| `해설.pdf` | added | — | {"path":"해설.pdf","sha256":"446b075e8d25f314d0a390679c4e2704a0f042a8d5fc4cb573e2e370c32d943d","size":752108} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 없음
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| release-validation | pass | 두 canonical의 스키마·구조 검증, 전체 단위 테스트, 브라우저 QA, 학생용 정답 0개, 답지 공유 target 일치, PDF 쪽수 및 대표 페이지 시각 검수를 완료했습니다. |
| semantic-review | pass | 완성 번역, 직독직해 영한 1:1 대응, 서술어, 어휘, 동사 cue, 오답과 배열 복원을 문장별로 검토했습니다. |
| source-question-cross-check | pass | 30번의 문맥상 부적절한 ③ more sensitive는 정답형 less sensitive로 정규화했고, 31번 빈칸은 정답 ① evolving uses를 canonical 본문에 복원했습니다. |
| source-transcription | pass | 원본 PDF 5쪽의 30번과 31번을 고해상도로 렌더링해 본문 단어, 대소문자, 숫자, 문장부호, 밑줄, 빈칸 및 선택지를 시각 확인했습니다. |

## 호환성

- 적용 범위: `selected` — 선택 워크북: 2026-june-grade2-q30, 2026-june-grade2-q31
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | — | 1.0.0 |
| spec | — | 1.0.6 |
| template | — | 1.0.4 |
| build | — | 1.0.0 |

## 변경 통계

- 직접 JSON 경로: 13
- 파생 JSON 경로: 21
- 변경·선언 파일: 29
- 영향 페이지: 22
- 변경 출력: 4
