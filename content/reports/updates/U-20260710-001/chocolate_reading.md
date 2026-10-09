# 업데이트 보고서 `U-20260710-001`: 저비용 단일 정본 워크북 엔진 전면 재구축

## 요약

기존 콘텐츠와 확정 디자인을 보존하면서 중복 HTML·반복 프롬프트·정규식 정답 추측을 제거하고, canonical 정본에서 학생용과 해설용을 함께 생성·검증·릴리스하는 구조로 전환합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260710-001` |
| 날짜 | 2026-07-10 |
| 분류 | `architecture` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 기존 콘텐츠는 유지하되 전체 작업 구조를 처음부터 다시 구성합니다.
- 최초 출력부터 제품 수준이어야 하며 검증 전 결과는 공개하지 않습니다.
- 업데이트를 쉽게 추가하고 변경 위치를 Markdown 보고서로 남깁니다.
- AGENTS.md·HTML·Python 반복 컨텍스트를 줄이면서 현재 품질을 유지합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | — | 1.0.0 | `44136fa355b3` | `9cf1d89aad66` | 변경 |
| spec | — | 1.0.0 | `44136fa355b3` | `a9a40c1f3f96` | 변경 |
| template | — | 1.0.0 | `44136fa355b3` | `aac2eb9fdf15` | 변경 |
| build | — | 1.0.0 | `44136fa355b3` | `e4f0a9c06327` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | added | — | {"sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","s… |
| 파생 | build | `문제.html` | added | — | {"sha256":"afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424","s… |
| 파생 | build | `문제.pdf` | added | — | {"sha256":"cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800","s… |
| 파생 | build | `해설.html` | added | — | {"sha256":"9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0","s… |
| 파생 | build | `해설.pdf` | added | — | {"sha256":"55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1","s… |
| 직접 | build | `workbook_engine/__main__.py` | added | — | {"sha256":"4abb421f270f4e5fb739aaac7d68ba89c65c17df0099564abcd730d95ca777e8","s… |
| 직접 | build | `workbook_engine/change_report.py` | added | — | {"sha256":"b70b6885ba408923d66b6eabd9280081eb22aa0e00fd51b53b54b9c830ee9c89","s… |
| 직접 | build | `workbook_engine/compiler.py` | added | — | {"sha256":"9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163","s… |
| 직접 | build | `workbook_engine/manifest.py` | added | — | {"sha256":"046fe32ef8bc39f1f11bac7b11ed368e5697e96d453fa3a425f89f58edcdfee6","s… |
| 직접 | build | `workbook_engine/migrate_legacy.py` | added | — | {"sha256":"724a9f9e08c22d48d8f884ebf0629f1699b7542303685bff96192d2326e4d714","s… |
| 직접 | build | `workbook_engine/paginator.py` | added | — | {"sha256":"241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d","s… |
| 직접 | build | `workbook_engine/qa.py` | added | — | {"sha256":"42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2","s… |
| 직접 | build | `workbook_engine/release.py` | added | — | {"sha256":"53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6","s… |
| 직접 | build | `workbook_engine/render.py` | added | — | {"sha256":"8f6e83f0709c29001c1ec07acdd0c3db2095844b71f42362503918f045765053","s… |
| 직접 | build | `workbook_engine/schema_gate.py` | added | — | {"sha256":"fe4b1014e6bcb1dfe0353d8e6b2dec82745aa7cb92dae78f619c6b371f3e966b","s… |
| 직접 | build | `workbook_engine/textops.py` | added | — | {"sha256":"8bf721d88f5901515b440edb3fee7fd77aee82a8d1858aeac1b8afeb0c77c0f3","s… |
| 직접 | build | `workbook_engine/validator.py` | added | — | {"sha256":"41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee","s… |
| 직접 | canonical | `workbooks/chocolate/content.json` | added | — | {"sha256":"e9d4ba330f82d26f3f265cc5c174098877d18c6827468ef392446c7f54962b7f","s… |
| 직접 | declared | `/Users/apple/.codex/skills/workbook-release/SKILL.md` | declared | — | — |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `answer-template.html` | declared | — | — |
| 직접 | declared | `index.html` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_release_safety.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/preview-data.js` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | spec | `config/versions.json` | added | — | {"sha256":"c70e3f5c60e2e863631a17c7066fcd5e12bdb1fa1f1503cf26b692b3f59d5d6f","s… |
| 직접 | spec | `config/workbook-spec.json` | added | — | {"sha256":"ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61","s… |
| 직접 | spec | `docs/semantic-rubric.md` | added | — | {"sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","s… |
| 직접 | spec | `schemas/canonical-workbook.schema.json` | added | — | {"sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218e6997","s… |
| 직접 | spec | `schemas/update.schema.json` | added | — | {"sha256":"76758164ed8c5bb1349c7c0d338c2d97837647aa19688a50553ed872fbb3dd7f","s… |
| 직접 | template | `assets/yonjogyo-logo-footer.png` | added | — | {"sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | added | — | {"sha256":"2fcebc4d28282d98bb0a56e744c962b55c71a1f128af2192974b69b79515cb35","s… |
| 직접 | template | `workbook_engine/templates/shell.html` | added | — | {"sha256":"1a0d56b95811b303e3fa73650dfe1ad690e2531e0628885a16cac72d5476007c","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | added | — | {"sha256":"eafb37ee02f60764c3ac5e8236c2c256cde35ebf7fdc3be73451e8983c1f5b7d","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical` | added | — | {"contentVersion":"1.0.0","metadata":{"grade":"중등","kicker":"Middle Reading","lessonLabel":"Chocolate","sourceLanguage"… |
| canonical | `$.contentVersion` | added | — | "1.0.0" |
| canonical | `$.files` | added | — | [{"path":"workbooks/chocolate/content.json","sha256":"e9d4ba330f82d26f3f265cc5c174098877d18c6827468ef392446c7f54962b7f"… |
| canonical | `$.workbookId` | added | — | "chocolate-reading" |
| spec | `$.files` | added | — | [{"path":"config/versions.json","sha256":"c70e3f5c60e2e863631a17c7066fcd5e12bdb1fa1f1503cf26b692b3f59d5d6f","size":1208… |
| spec | `$.schemaFiles` | added | — | [{"path":"schemas/canonical-workbook.schema.json","sha256":"a128297a50c8aecca1122e4d8fcb186937dcb070d5e8b998cae0abfb218… |
| spec | `$.semanticRubricFile` | added | — | {"path":"docs/semantic-rubric.md","sha256":"2b21b6f5ab1c47bd9109bf4172ed54f7bc4f6d6de87abf5588e820d743b895a2","size":80… |
| spec | `$.semanticRubricVersion` | added | — | "1.0.0" |
| spec | `$.spec` | added | — | {"$id":"https://local.workbook/spec/workbook-spec-1.0.0.json","$schema":"https://json-schema.org/draft/2020-12/schema",… |
| spec | `$.specVersion` | added | — | "1.0.0" |
| template | `$.files` | added | — | [{"path":"assets/yonjogyo-logo-footer.png","sha256":"e717b1b2e4adeb9bd80e3779d5963414d98cb0da493d15ad36629bc62f303bf1",… |
| template | `$.rendererContract` | added | — | "shared-dom-explicit-targets-fail-closed" |
| template | `$.templateVersion` | added | — | "1.0.0" |

## 파생 영향 (파생 변경)

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| build | `$.appliedUpdates` | added | — | ["U-20260710-001"] |
| build | `$.buildVersion` | added | — | "1.0.0" |
| build | `$.builtAt` | added | — | "2026-07-10T21:19:00+09:00" |
| build | `$.canonicalDigest` | added | — | "a2fc8f57cf3e10bd3870f75d87b1cd08e962df2c4d589955b11b8621a461fefc" |
| build | `$.compilerVersion` | added | — | "1.0.0" |
| build | `$.contentVersion` | added | — | "1.0.0" |
| build | `$.engineDigest` | added | — | "a199d39b59695c50cdba9ad84a535eaf363eaa1c8a1c325796f361d4ab10a47e" |
| build | `$.engineInputs` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","siz… |
| build | `$.files` | added | — | [{"path":"workbook_engine/__init__.py","sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","siz… |
| build | `$.outputs` | added | — | [{"path":"문제.html","sha256":"afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424","size":197249},{"path":"… |
| build | `$.pages` | added | — | [{"digest":"c60c6512a2318a3fbe7680443fddaeb02ebc4d9f6f593d9247fef8a5f749246a","edition":"student","id":"student:chocola… |
| build | `$.qa` | added | — | {"contactSheets":["qa/samples/student-contact-sheet.png","qa/samples/answer-contact-sheet.png"],"dom":{"answer":{"pages… |
| build | `$.reportFormatVersion` | added | — | "1.0.0" |
| build | `$.schemaVersion` | added | — | "1.0.0" |
| build | `$.semanticRubricVersion` | added | — | "1.0.0" |
| build | `$.sourceDigest` | added | — | "2e957e3b573145c8c25e1e992a330cb9ce7d7180b5c734c2ba575d261743172d" |
| build | `$.specVersion` | added | — | "1.0.0" |
| build | `$.templateVersion` | added | — | "1.0.0" |
| build | `$.validationStatus` | added | — | "passed" |
| build | `$.visualReview` | added | — | {"notes":"학생용·해설용 22쪽 contact sheet와 원본 PNG를 확인함: 1-2쪽 번호 연속, 4·6단계 밀집 페이지, 7단계 검정 오답·밑줄 및 빨강 교정답, 8단계 배열, 9단계 문단 순서, 1… |
| build | `$.workbookId` | added | — | "chocolate-reading" |

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:chocolate-reading-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| answer:chocolate-reading-p02 | added | 1 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p03 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p04 | added | 2 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p05 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p06 | added | 3 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p07 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| answer:chocolate-reading-p08 | added | 4 | s011, s012, s013, s014, s015, s016, s017, s018, s019, s020 |
| answer:chocolate-reading-p09 | added | 4 | s021, s022, s023, s024 |
| answer:chocolate-reading-p10 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p11 | added | 5 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p12 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p13 | added | 6 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p14 | added | 7 | — |
| answer:chocolate-reading-p15 | added | 8 | s001, s002, s003, s004, s005, s006 |
| answer:chocolate-reading-p16 | added | 8 | s007, s008, s009, s010, s011, s012 |
| answer:chocolate-reading-p17 | added | 8 | s013, s014, s015, s016, s017, s018 |
| answer:chocolate-reading-p18 | added | 8 | s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p19 | added | 9 | — |
| answer:chocolate-reading-p20 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:chocolate-reading-p21 | added | 10 | s009, s010, s011, s012, s013, s014, s015, s016 |
| answer:chocolate-reading-p22 | added | 10 | s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p01 | added | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| student:chocolate-reading-p02 | added | 1 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p03 | added | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p04 | added | 2 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p05 | added | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p06 | added | 3 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p07 | added | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| student:chocolate-reading-p08 | added | 4 | s011, s012, s013, s014, s015, s016, s017, s018, s019, s020 |
| student:chocolate-reading-p09 | added | 4 | s021, s022, s023, s024 |
| student:chocolate-reading-p10 | added | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p11 | added | 5 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p12 | added | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p13 | added | 6 | s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p14 | added | 7 | — |
| student:chocolate-reading-p15 | added | 8 | s001, s002, s003, s004, s005, s006 |
| student:chocolate-reading-p16 | added | 8 | s007, s008, s009, s010, s011, s012 |
| student:chocolate-reading-p17 | added | 8 | s013, s014, s015, s016, s017, s018 |
| student:chocolate-reading-p18 | added | 8 | s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p19 | added | 9 | — |
| student:chocolate-reading-p20 | added | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:chocolate-reading-p21 | added | 10 | s009, s010, s011, s012, s013, s014, s015, s016 |
| student:chocolate-reading-p22 | added | 10 | s017, s018, s019, s020, s021, s022, s023, s024 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | added | — | {"path":"문제.html","sha256":"afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424","size":197249} |
| `문제.pdf` | added | — | {"path":"문제.pdf","sha256":"cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800","size":924807} |
| `해설.html` | added | — | {"path":"해설.html","sha256":"9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0","size":220066} |
| `해설.pdf` | added | — | {"path":"해설.pdf","sha256":"55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1","size":1135657} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 없음
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| browser-and-pdf-validation | pass | CDP 완료 상태, 페이지 넘침, 학생·해설 공통 슬롯, A4 PDF 페이지 수를 검사합니다. |
| canonical-and-compiled-validation | pass | 원문 복원, 타깃 해석, 10단계 전체 문장 커버리지와 학생용 정답 비노출을 검사합니다. |
| representative-visual-review | pass | 첫쪽·part 전환·중간 위험 단계·7단계·9단계·마지막 쪽을 학생용과 해설용에서 확인합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | — | 1.0.0 |
| spec | — | 1.0.0 |
| template | — | 1.0.0 |
| build | — | 1.0.0 |

## 변경 통계

- 직접 JSON 경로: 13
- 파생 JSON 경로: 21
- 변경·선언 파일: 36
- 영향 페이지: 44
- 변경 출력: 4
