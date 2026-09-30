# 업데이트 보고서 `U-20260723-004`: 8단계 조각형 정답 밑줄 제거

## 요약

8단계 순서 배열하기에서 제시어 개수에 맞춘 짧은 정답 밑줄을 제거하고, 우리말·제시어·긴 답안 작성선만 유지합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260723-004` |
| 날짜 | 2026-07-23 |
| 분류 | `shared-layout` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 첨부 화면에 표시된 8단계의 조각형 정답 밑줄을 제거하고 AGENTS.md, HTML 파생물, Python 생성 엔진을 모두 일치시킵니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.0 | 1.0.1 | `9cf1d89aad66` | `06497a994d84` | 변경 |
| spec | 1.0.0 | 1.0.1 | `a9a40c1f3f96` | `729f1700e7c8` | 변경 |
| template | 1.0.0 | 1.0.1 | `aac2eb9fdf15` | `6456357b00c6` | 변경 |
| build | 1.0.0 | 1.0.1 | `e4f0a9c06327` | `b6018803e60d` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424","s… | {"sha256":"4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800","s… | {"sha256":"9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0","s… | {"sha256":"77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1","s… | {"sha256":"8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","s… | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163","s… | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… |
| 직접 | canonical | `workbooks/chocolate/content.json` | modified | {"sha256":"e9d4ba330f82d26f3f265cc5c174098877d18c6827468ef392446c7f54962b7f","s… | {"sha256":"e9bf81a89dc2d26a34d71668ca8f104f3de75a3cc0e2fb8f7907568d14e7409b","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-004.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/preview-data.js` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"c70e3f5c60e2e863631a17c7066fcd5e12bdb1fa1f1503cf26b692b3f59d5d6f","s… | {"sha256":"32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61","s… | {"sha256":"f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | modified | {"sha256":"2fcebc4d28282d98bb0a56e744c962b55c71a1f128af2192974b69b79515cb35","s… | {"sha256":"b8d6cf61d980afcfa0160d91fe87b73d535cc2ab80bac66964f45a9e0ec2345e","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | modified | {"sha256":"eafb37ee02f60764c3ac5e8236c2c256cde35ebf7fdc3be73451e8983c1f5b7d","s… | {"sha256":"fbce767b88b805800c5f03a51bfbe5c61985a55131b8624e43ab87acd5de3761","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.specVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.updateState.appliedUpdates[1]` | added | — | {"appliedAt":"2026-07-23T23:15:00+09:00","fromContentVersion":"1.0.0","id":"U-20260723-004","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.files[0].sha256` | modified | "e9d4ba330f82d26f3f265cc5c174098877d18c6827468ef392446c7f54962b7f" | "e9bf81a89dc2d26a34d71668ca8f104f3de75a3cc0e2fb8f7907568d14e7409b" |
| canonical | `$.files[0].size` | modified | 124980 | 125233 |
| spec | `$.files[0].sha256` | modified | "c70e3f5c60e2e863631a17c7066fcd5e12bdb1fa1f1503cf26b692b3f59d5d6f" | "32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64" |
| spec | `$.files[0].size` | modified | 1208 | 1289 |
| spec | `$.files[1].sha256` | modified | "ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61" | "f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172" |
| spec | `$.files[1].size` | modified | 15679 | 15784 |
| spec | `$.spec.logicalStages[7].layout.answerEditionSolution` | added | — | "complete sentence in the shared answer-lines response slot" |
| spec | `$.spec.logicalStages[7].layout.arrangementSlots` | added | — | "forbidden" |
| spec | `$.spec.logicalStages[7].layout.fieldOrder[2]` | modified | "arrangement-slots" | "answer-lines" |
| spec | `$.spec.logicalStages[7].layout.fieldOrder[3]` | removed | "answer-lines" | — |
| spec | `$.spec.specVersion` | modified | "1.0.0" | "1.0.1" |
| spec | `$.specVersion` | modified | "1.0.0" | "1.0.1" |
| template | `$.files[1].sha256` | modified | "2fcebc4d28282d98bb0a56e744c962b55c71a1f128af2192974b69b79515cb35" | "b8d6cf61d980afcfa0160d91fe87b73d535cc2ab80bac66964f45a9e0ec2345e" |
| template | `$.files[3].sha256` | modified | "eafb37ee02f60764c3ac5e8236c2c256cde35ebf7fdc3be73451e8983c1f5b7d" | "fbce767b88b805800c5f03a51bfbe5c61985a55131b8624e43ab87acd5de3761" |
| template | `$.templateVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.appliedUpdates[1]` | added | — | "U-20260723-004" |
| build | `$.buildVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.builtAt` | modified | "2026-07-10T21:19:00+09:00" | "2026-07-23T23:18:05+09:00" |
| build | `$.canonicalDigest` | modified | "a2fc8f57cf3e10bd3870f75d87b1cd08e962df2c4d589955b11b8621a461fefc" | "d00b93b4982db9a43670c8be9ac6b53376d6f310c2321267291a0fb6efd03c82" |
| build | `$.compilerVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.engineDigest` | modified | "a199d39b59695c50cdba9ad84a535eaf363eaa1c8a1c325796f361d4ab10a47e" | "0e9ef363eb9d5cfdf00794efcdedb7481cce218b5c043f069078a8d991ace578" |
| build | `$.engineInputs[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.engineInputs[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.engineInputs[3].size` | modified | 14990 | 14275 |
| build | `$.files[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.files[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.files[3].size` | modified | 14990 | 14275 |
| build | `$.files[13].sha256` | modified | "afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424" | "4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c" |
| build | `$.files[13].size` | modified | 197249 | 190281 |
| build | `$.files[14].sha256` | modified | "cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800" | "9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba" |
| build | `$.files[14].size` | modified | 924807 | 919425 |
| build | `$.files[15].sha256` | modified | "9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0" | "77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840" |
| build | `$.files[15].size` | modified | 220066 | 211771 |
| build | `$.files[16].sha256` | modified | "55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1" | "8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98" |
| build | `$.files[16].size` | modified | 1135657 | 1112757 |
| build | `$.outputs[0].sha256` | modified | "afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424" | "4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c" |
| build | `$.outputs[0].size` | modified | 197249 | 190281 |
| build | `$.outputs[1].sha256` | modified | "cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800" | "9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba" |
| build | `$.outputs[1].size` | modified | 924807 | 919425 |
| build | `$.outputs[2].sha256` | modified | "9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0" | "77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840" |
| build | `$.outputs[2].size` | modified | 220066 | 211771 |
| build | `$.outputs[3].sha256` | modified | "55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1" | "8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98" |
| build | `$.outputs[3].size` | modified | 1135657 | 1112757 |
| build | `$.pages[14].digest` | modified | "a5bb0c5e69836615d52977edf1845f3822ae1782b15e547aa050b90e8aa19465" | "c28f729f0212e4e77fa5a9706ec76d3e1c4a179d2c1cda90821d766b70dcc95b" |
| build | `$.pages[15].digest` | modified | "f3c9dd75dcc32bd41a7f493a00ff95536d00deafe12b75d50079a53ee27218e6" | "a8b6edca6086fa674347397486db514e062089a856889d899edac7790566329f" |
| build | `$.pages[16].digest` | modified | "0ad1ef0ae3f9bbdeeb1865add1d4d2d44665215588cd348c98465100b928bfbd" | "41ef253aa7fdee1f2e880f217da366925d45e9e347245191059420e9ea5ed5b5" |
| build | `$.pages[17].digest` | modified | "a2a975b8ddd5d943131dd3dbad80613fd0ef3c793ee055577689e925a667863c" | "1bace8b1ef97dbd173a846bc2ed4be6cde06102c62b6a62cf7705fe1aeaaac9e" |
| build | `$.pages[36].digest` | modified | "7909f957fa2695c9d0cf69e65908542f5e0a3ac54acf4703527ae940adc9c88f" | "225c0793141c49943632bf5f182c0fd9f991a457808203ace13b12d2b1c382c5" |
| build | `$.pages[37].digest` | modified | "b9b2ca1b29b139f02b9427c7ff82372cd96d29825998c378f40128bdd1f07314" | "9dba0aac32339830a40578c6c52808a23fb714918a91673f749b1d3394b88384" |
| build | `$.pages[38].digest` | modified | "afc1b2358ce31a1fa1f9ffd40a3e790dd668d2b123dad01c1a8d112a7f0ca177" | "ea2659ac5d6a252d93a07e3568a03ed2d9a5aeac1938aff5a3e8b7f9dac4393c" |
| build | `$.pages[39].digest` | modified | "eb42085a99a667c743fa0802132651b7ead1855ed71dc0575cad77940eb74e6f" | "1256c647872170ec261f67fd6b1b8a6490d03b54dabae9591ecf20eaa2aea6ca" |
| build | `$.qa.dom.answer.solutions` | modified | 310 | 255 |
| build | `$.qa.dom.sharedTargetSlotCount` | modified | 339 | 260 |
| build | `$.specVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.templateVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 22쪽 contact sheet와 원본 PNG를 확인함: 1-2쪽 번호 연속, 4·6단계 밀집 페이지, 7단계 검정 오답·밑줄 및 빨강 교정답, 8단계 배열, 9단계 문단 순서, 10단계 마지막 페… | "학생용·해설용 22쪽 contact sheet에서 1·2·7·12·14·15·19·20·22페이지를 확인함. 8단계 조각형 정답 밑줄이 제거되고 긴 작성선·완성 문장 해설만 유지됨. 잘림·겹침·번호 오류·학생용 … |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-10T21:23:42+09:00" | "2026-07-23T23:19:04+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 8 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:chocolate-reading-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:chocolate-reading-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| answer:chocolate-reading-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| answer:chocolate-reading-p18 | modified | 8 | s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:chocolate-reading-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| student:chocolate-reading-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| student:chocolate-reading-p18 | modified | 8 | s019, s020, s021, s022, s023, s024 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"afac72915623b3863b4c60903345757cfcea84a9f4b805593ce7ff2f45d4d424","size":197249} | {"path":"문제.html","sha256":"4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c","size":190281} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"cfc52627e65bb6c06c6723ee2c73eb114eb5943186d5c73c889224c3aca99800","size":924807} | {"path":"문제.pdf","sha256":"9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba","size":919425} |
| `해설.html` | modified | {"path":"해설.html","sha256":"9ca35c9cb48b2c6b90c84a35dd478fe61b0ef72094e7891e311eaa55b3069ce0","size":220066} | {"path":"해설.html","sha256":"77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840","size":211771} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"55c052905bf1a717160c2f9262f681da34639e7f83b4b68dcbaffaf784a431c1","size":1135657} | {"path":"해설.pdf","sha256":"8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98","size":1112757} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 1, 2, 3, 4, 5, 6, 7, 9, 10
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| release-validation | skipped | 공유 엔진 테스트와 새 비공개 빌드에서 확인합니다. |
| stage8-arrangement-slots | pass | 8단계 compiled item에 조각형 en/arrange-slot을 생성하지 않고 완성 문장 responseTargetId 하나만 생성하도록 계약 테스트를 추가했습니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.0 | 1.0.1 |
| spec | 1.0.0 | 1.0.1 |
| template | 1.0.0 | 1.0.1 |
| build | 1.0.0 | 1.0.1 |

## 변경 통계

- 직접 JSON 경로: 62
- 파생 JSON 경로: 0
- 변경·선언 파일: 18
- 영향 페이지: 8
- 변경 출력: 4
