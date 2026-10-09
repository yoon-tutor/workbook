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
| canonical | 1.0.0 | 1.0.1 | `e8d2ca810feb` | `ac15ce3442a8` | 변경 |
| spec | 1.0.0 | 1.0.1 | `76ff1ec6e14f` | `729f1700e7c8` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.0 | 1.0.1 | `11d7c8316d5b` | `02c3585a3c19` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"4a116a35fc83c8b88c861b259a8185089d19ce985c1b303370a9797cc7b1a8c4","s… | {"sha256":"37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"28c82383d5123981a51aa1692147be19930e56c1272d748d3cf12c0dee92c297","s… | {"sha256":"2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"2fbc121aec8f2bcb4cb741534d2688737e654d270f13605c451cb6d25a156e66","s… | {"sha256":"8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"d62dbf644d2953c75bef2bc74a718bb295192c8eaa7f2e49812df6c5719bf75d","s… | {"sha256":"70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","s… | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163","s… | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… |
| 직접 | canonical | `workbooks/when-failure-become-ideas/content.json` | modified | {"sha256":"2aa04f71a01dfe7baf75a981d78cf1089aeb214ffb6d4e8ff5319fc17699ba69","s… | {"sha256":"d5d55fe18a5989d480863288b392199b69a053c7d74db5c2d00acf34e530a1e6","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-004.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/preview-data.js` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"134ec1b28a398aef777da408d6dc4c2410e9769806bdf55282f80c017828d3c5","s… | {"sha256":"32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61","s… | {"sha256":"f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.specVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.updateState.appliedUpdates[1]` | added | — | {"appliedAt":"2026-07-23T23:15:00+09:00","fromContentVersion":"1.0.0","id":"U-20260723-004","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.files[0].sha256` | modified | "2aa04f71a01dfe7baf75a981d78cf1089aeb214ffb6d4e8ff5319fc17699ba69" | "d5d55fe18a5989d480863288b392199b69a053c7d74db5c2d00acf34e530a1e6" |
| canonical | `$.files[0].size` | modified | 38557 | 38810 |
| spec | `$.files[0].sha256` | modified | "134ec1b28a398aef777da408d6dc4c2410e9769806bdf55282f80c017828d3c5" | "32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64" |
| spec | `$.files[0].size` | modified | 1252 | 1289 |
| spec | `$.files[1].sha256` | modified | "ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61" | "f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172" |
| spec | `$.files[1].size` | modified | 15679 | 15784 |
| spec | `$.spec.logicalStages[7].layout.answerEditionSolution` | added | — | "complete sentence in the shared answer-lines response slot" |
| spec | `$.spec.logicalStages[7].layout.arrangementSlots` | added | — | "forbidden" |
| spec | `$.spec.logicalStages[7].layout.fieldOrder[2]` | modified | "arrangement-slots" | "answer-lines" |
| spec | `$.spec.logicalStages[7].layout.fieldOrder[3]` | removed | "answer-lines" | — |
| spec | `$.spec.specVersion` | modified | "1.0.0" | "1.0.1" |
| spec | `$.specVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.appliedUpdates[1]` | added | — | "U-20260723-004" |
| build | `$.buildVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.builtAt` | modified | "2026-07-23T23:07:37+09:00" | "2026-07-23T23:17:16+09:00" |
| build | `$.canonicalDigest` | modified | "ad0536510cb8f639831906779cc2b3e431aa652814a7e6baa0f46019c0717cc4" | "228227fa9bbf1b4b86a804ff38f57a62b5b2bbc3ab54cb6c40406ab67078d779" |
| build | `$.compilerVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.engineDigest` | modified | "a199d39b59695c50cdba9ad84a535eaf363eaa1c8a1c325796f361d4ab10a47e" | "0e9ef363eb9d5cfdf00794efcdedb7481cce218b5c043f069078a8d991ace578" |
| build | `$.engineInputs[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.engineInputs[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.engineInputs[3].size` | modified | 14990 | 14275 |
| build | `$.files[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.files[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.files[3].size` | modified | 14990 | 14275 |
| build | `$.files[13].sha256` | modified | "4a116a35fc83c8b88c861b259a8185089d19ce985c1b303370a9797cc7b1a8c4" | "37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17" |
| build | `$.files[13].size` | modified | 161737 | 158301 |
| build | `$.files[14].sha256` | modified | "28c82383d5123981a51aa1692147be19930e56c1272d748d3cf12c0dee92c297" | "2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861" |
| build | `$.files[14].size` | modified | 762436 | 757943 |
| build | `$.files[15].sha256` | modified | "2fbc121aec8f2bcb4cb741534d2688737e654d270f13605c451cb6d25a156e66" | "8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc" |
| build | `$.files[15].size` | modified | 174657 | 170688 |
| build | `$.files[16].sha256` | modified | "d62dbf644d2953c75bef2bc74a718bb295192c8eaa7f2e49812df6c5719bf75d" | "70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8" |
| build | `$.files[16].size` | modified | 925585 | 906987 |
| build | `$.outputs[0].sha256` | modified | "4a116a35fc83c8b88c861b259a8185089d19ce985c1b303370a9797cc7b1a8c4" | "37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17" |
| build | `$.outputs[0].size` | modified | 161737 | 158301 |
| build | `$.outputs[1].sha256` | modified | "28c82383d5123981a51aa1692147be19930e56c1272d748d3cf12c0dee92c297" | "2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861" |
| build | `$.outputs[1].size` | modified | 762436 | 757943 |
| build | `$.outputs[2].sha256` | modified | "2fbc121aec8f2bcb4cb741534d2688737e654d270f13605c451cb6d25a156e66" | "8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc" |
| build | `$.outputs[2].size` | modified | 174657 | 170688 |
| build | `$.outputs[3].sha256` | modified | "d62dbf644d2953c75bef2bc74a718bb295192c8eaa7f2e49812df6c5719bf75d" | "70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8" |
| build | `$.outputs[3].size` | modified | 925585 | 906987 |
| build | `$.pages[14].digest` | modified | "67aae67437670b634950d9e77ce7e75d8deb221ab1f5ec95ed037dbf7f03e9cf" | "881341168d82b5eee408a84ae78c239c2c9eb8757a7d429dcc0a6ea19ea9bc85" |
| build | `$.pages[15].digest` | modified | "a06da348201f72bacde176113d4df5ca6307552f99c798be085490e7c33073f9" | "61d19bdbd8baba5b411555e6d2872926c40316ab342cff16c1b32a1093e0529a" |
| build | `$.pages[16].digest` | modified | "d38a4b1cc82ef3f0e06b0af822cb574e5cab7d26ca89e1311eef6850ee3ce59c" | "5ade2829f5676b5929d6f3d2ba2ed3bf27b2e6c0cb0a8e8f25dba11593e0a043" |
| build | `$.pages[17].digest` | modified | "f5dc149cd011bea882da22e1ec8dbe0fe72b197258988e4961f6af05a372a8ac" | "9613774259637c0a6f5d9776561e781f63a63c85e71d61f770162d592e6a5853" |
| build | `$.pages[36].digest` | modified | "8cce56303c4c9eb76592bf53f1ceeae125e6597032bfb32ab7db8d90188eabfe" | "75a5b0c3c64c6ce0d76954a3def3a73272045b47c9ce1af8f701f490d2e14e1e" |
| build | `$.pages[37].digest` | modified | "0fac2a261bc7415f14d4c250421494bdf21ca123a6df1193ed2a0328d903d4b1" | "c632e686cae48f355b523f6da6f4d365220f099e0e3a8c932556cbc050faa4f4" |
| build | `$.pages[38].digest` | modified | "2a6d1a99ab2ee1237b96cfaa4affc48ba2ff83a6a89dde078efafb27b2ac9964" | "e36355fdfb89260501fe4bb23216d97435ee65eeb62e7fd029743099f6ac1af8" |
| build | `$.pages[39].digest` | modified | "5e1978386c1388fef35ef3447341b36465338c15d9354a131439c537278e518a" | "65fae8e2373e204d0619b5ad723cb84ec55536b7e653359f97c7aa8a6b8b6a77" |
| build | `$.qa.dom.answer.solutions` | modified | 184 | 161 |
| build | `$.qa.dom.sharedTargetSlotCount` | modified | 209 | 165 |
| build | `$.specVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 contact sheet에서 1·2페이지, 밀집 문장 7·12페이지, 7단계 교정 14페이지, 8단계 배열 15페이지, 9단계 문단 순서 19페이지, 10단계 쓰기 20·22페이지를 확인함. 잘림·… | "학생용·해설용 전체 contact sheet와 8단계 15페이지 원본 PNG를 확인함. 요청된 조각형 정답 밑줄이 문제·해설 모두 제거되었고, 학생용은 우리말·제시어·긴 작성선만, 해설용은 동일 긴 답안 영역에 … |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-23T23:08:11+09:00" | "2026-07-23T23:18:57+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 8 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:when-failure-become-ideas-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:when-failure-become-ideas-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| answer:when-failure-become-ideas-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| answer:when-failure-become-ideas-p18 | modified | 8 | s019, s020, s021 |
| student:when-failure-become-ideas-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:when-failure-become-ideas-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| student:when-failure-become-ideas-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| student:when-failure-become-ideas-p18 | modified | 8 | s019, s020, s021 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"4a116a35fc83c8b88c861b259a8185089d19ce985c1b303370a9797cc7b1a8c4","size":161737} | {"path":"문제.html","sha256":"37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17","size":158301} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"28c82383d5123981a51aa1692147be19930e56c1272d748d3cf12c0dee92c297","size":762436} | {"path":"문제.pdf","sha256":"2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861","size":757943} |
| `해설.html` | modified | {"path":"해설.html","sha256":"2fbc121aec8f2bcb4cb741534d2688737e654d270f13605c451cb6d25a156e66","size":174657} | {"path":"해설.html","sha256":"8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc","size":170688} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"d62dbf644d2953c75bef2bc74a718bb295192c8eaa7f2e49812df6c5719bf75d","size":925585} | {"path":"해설.pdf","sha256":"70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8","size":906987} |

## 영향 없음

- 동일한 manifest 구성 요소: `template`
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
| template | 1.0.1 | 1.0.1 |
| build | 1.0.0 | 1.0.1 |

## 변경 통계

- 직접 JSON 경로: 58
- 파생 JSON 경로: 0
- 변경·선언 파일: 16
- 영향 페이지: 8
- 변경 출력: 4
