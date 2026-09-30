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
| canonical | 1.0.0 | 1.0.1 | `7fab4f3db2cf` | `de361e27fff4` | 변경 |
| spec | 1.0.0 | 1.0.1 | `8203ec9e777c` | `729f1700e7c8` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.0 | 1.0.1 | `d3a665c7c84c` | `a9442a4f0704` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054","s… | {"sha256":"8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155","s… | {"sha256":"a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf","s… | {"sha256":"98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32","s… | {"sha256":"490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2","s… | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163","s… | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… |
| 직접 | canonical | `workbooks/soccer-jersey-swap/content.json` | modified | {"sha256":"2d7b93b3064b9adb74ab53162e451719c941fdd0db548c147c01a99c34c4f807","s… | {"sha256":"dd5dc17c3ae865e37e7597ee061e57c95ec053a23e6117d52a9e561adeebdd8b","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-004.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/preview-data.js` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"c0a93788f2ee81ac0f5106cc5220e86267b6ecb0a8d89c7a8b996f6b085741cb","s… | {"sha256":"32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"ddd31459b8fd791929f103d44bc67942ccb9f2d1a4d6c9687cef569e6933aa61","s… | {"sha256":"f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.specVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.updateState.appliedUpdates[1]` | added | — | {"appliedAt":"2026-07-23T23:15:00+09:00","fromContentVersion":"1.0.0","id":"U-20260723-004","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.files[0].sha256` | modified | "2d7b93b3064b9adb74ab53162e451719c941fdd0db548c147c01a99c34c4f807" | "dd5dc17c3ae865e37e7597ee061e57c95ec053a23e6117d52a9e561adeebdd8b" |
| canonical | `$.files[0].size` | modified | 29321 | 29518 |
| spec | `$.files[0].sha256` | modified | "c0a93788f2ee81ac0f5106cc5220e86267b6ecb0a8d89c7a8b996f6b085741cb" | "32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64" |
| spec | `$.files[0].size` | modified | 1230 | 1289 |
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
| build | `$.builtAt` | modified | "2026-07-11T14:00:16+09:00" | "2026-07-23T23:18:23+09:00" |
| build | `$.canonicalDigest` | modified | "618e755c1e90b3e0438f3e2f1703b2d795db1cd90474f87918a1606e3d4e7fab" | "d77138eaea6365f88f4fb98952f96a6ec70475e98f54a08bd1759ada7b107695" |
| build | `$.compilerVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.engineDigest` | modified | "a199d39b59695c50cdba9ad84a535eaf363eaa1c8a1c325796f361d4ab10a47e" | "0e9ef363eb9d5cfdf00794efcdedb7481cce218b5c043f069078a8d991ace578" |
| build | `$.engineInputs[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.engineInputs[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.engineInputs[3].size` | modified | 14990 | 14275 |
| build | `$.files[0].sha256` | modified | "1c143836defbac767d2cb79b574fbddb98803a45c6b0605ccf5b4e359ca958f2" | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" |
| build | `$.files[3].sha256` | modified | "9324831b0dda2c1e214c033bd34a25f0ed5c5ca31c3fb10d137a5d4fd37a1163" | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" |
| build | `$.files[3].size` | modified | 14990 | 14275 |
| build | `$.files[13].sha256` | modified | "251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054" | "8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c" |
| build | `$.files[13].size` | modified | 154824 | 151456 |
| build | `$.files[14].sha256` | modified | "86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155" | "a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04" |
| build | `$.files[14].size` | modified | 697429 | 695776 |
| build | `$.files[15].sha256` | modified | "dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf" | "98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48" |
| build | `$.files[15].size` | modified | 168651 | 164661 |
| build | `$.files[16].sha256` | modified | "0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32" | "490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b" |
| build | `$.files[16].size` | modified | 856243 | 842774 |
| build | `$.outputs[0].sha256` | modified | "251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054" | "8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c" |
| build | `$.outputs[0].size` | modified | 154824 | 151456 |
| build | `$.outputs[1].sha256` | modified | "86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155" | "a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04" |
| build | `$.outputs[1].size` | modified | 697429 | 695776 |
| build | `$.outputs[2].sha256` | modified | "dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf" | "98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48" |
| build | `$.outputs[2].size` | modified | 168651 | 164661 |
| build | `$.outputs[3].sha256` | modified | "0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32" | "490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b" |
| build | `$.outputs[3].size` | modified | 856243 | 842774 |
| build | `$.pages[9].digest` | modified | "dac020d35e3c07c1f90769c4911243014939bdad87f979f16bdd5cc81d4ca7df" | "7293c0b2c9e40e03112354e675f7f0fcf0c46b3aa96064b812efba76c2522e2b" |
| build | `$.pages[10].digest` | modified | "689498a0a201fb55b61aca88e47dc22315240f38ef44a42638092e49d23c9b8a" | "57d02031c0e78be627d84b15c252b83e7bcd767e46c7b75ecf194e342772798f" |
| build | `$.pages[11].digest` | modified | "7d7ff4dac10ea1a6a70ff038eb78b5ac4e45d84d31fb92981efdda6809501174" | "17d9cc873e987dd01ae0e88acffef1afaa70f5f15223c142cae68f0697dff64a" |
| build | `$.pages[24].digest` | modified | "678a7720d7d2b1091f1d221d42a5ae5dd643d960946b755adb640a2d7763015c" | "4de5ef796cb2072fce72ad90f5a8fba5203df44545e817527ac67393a8e0a598" |
| build | `$.pages[25].digest` | modified | "3235543a8bb0c4872630e45b48f4112df1aed1b1ce8a4c237a22522a9bef58a9" | "1a318f5f0610e0bce87ac7685f8151fa6953f0ab931d13913144e9480cec51e6" |
| build | `$.pages[26].digest` | modified | "39c00cfc052221e230d7327822a90c0d4f26154bc6be8d6b479ae20b6ed68a58" | "aaef11e669a752accaeb20378db02386b02eaf2e799c31d5d298edcfc78c8ab4" |
| build | `$.qa.dom.answer.solutions` | modified | 138 | 112 |
| build | `$.qa.dom.sharedTargetSlotCount` | modified | 156 | 116 |
| build | `$.specVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 contact sheet에서 1단계 첫·분할 페이지, 4단계 해석, 7단계 교정 색상, 9단계 문단 순서, 10단계 마지막 페이지를 확인했습니다. 텍스트 잘림·겹침·페이지 초과·학생용 정답 노출이 … | "학생용·해설용 15쪽 contact sheet에서 1·2·5·8·9·10·13·14·15페이지를 확인함. 8단계 조각형 정답 밑줄이 제거되고 학생용 긴 작성선과 해설용 완성 문장만 유지됨. 잘림·겹침·번호 오류·… |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-11T14:00:35+09:00" | "2026-07-23T23:19:10+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 8 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:soccer-jersey-swap-p10 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:soccer-jersey-swap-p11 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| answer:soccer-jersey-swap-p12 | modified | 8 | s013, s014 |
| student:soccer-jersey-swap-p10 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:soccer-jersey-swap-p11 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| student:soccer-jersey-swap-p12 | modified | 8 | s013, s014 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"251d1fad716dee0fa9d919c11bbe833cfca2370de03fc64d32556b8e600df054","size":154824} | {"path":"문제.html","sha256":"8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c","size":151456} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"86cfcc7d156f1fbce11ed769e2e48b4f190654301ff39d846a1fe35a2aae2155","size":697429} | {"path":"문제.pdf","sha256":"a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04","size":695776} |
| `해설.html` | modified | {"path":"해설.html","sha256":"dceca21af550ee04e4055d92255e6abb863afe054e5e9c4e884add7bab0fb2cf","size":168651} | {"path":"해설.html","sha256":"98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48","size":164661} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"0fbec5d81a9632512d8500dd4bb5f9e8c78a8f05d90f8578712922d851240d32","size":856243} | {"path":"해설.pdf","sha256":"490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b","size":842774} |

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

- 직접 JSON 경로: 56
- 파생 JSON 경로: 0
- 변경·선언 파일: 16
- 영향 페이지: 6
- 변경 출력: 4
