# 업데이트 보고서 `U-20260826-009`: 해설 기준 서술형 답안 칸 동기화

## 요약

해설용을 먼저 렌더링해 작성형 정답이 실제로 차지한 높이를 측정하고, 같은 높이를 유지한 채 정답만 제거하여 학생용을 생성합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260826-009` |
| 날짜 | 2026-08-26 |
| 분류 | `layout-and-release` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 서술형 문제의 답안 칸을 해설용 답안이 차지하는 실제 높이만큼 확보하고, 해설용에서 답만 지운 구조로 학생용을 생성합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.0 | 1.0.1 | `6a5b2ee9a871` | `095f8aa8aef9` | 변경 |
| spec | 1.0.2 | 1.0.3 | `94237af0a7ed` | `5f1517bd2a24` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.0 | 1.0.1 | `24ababc53df7` | `1baaeffadb65` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… | {"sha256":"0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d","s… | {"sha256":"b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db","s… | {"sha256":"3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293","s… | {"sha256":"7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39","s… | {"sha256":"73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… | {"sha256":"9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2","s… | {"sha256":"d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6","s… | {"sha256":"c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q21/content.json` | modified | {"sha256":"bfe93c2e32a6c34f659eda70fa31debf795b5e9200a0766e4f8e228a99000323","s… | {"sha256":"f3a170d72db5816034242eb334241e1b3aa65321641ad32304a0d64f7570ef53","s… |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q20/content.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"f97bc280305f46e0b199e68c322318570cbb4787cad785bdd0d70250f83d3f2e","s… | {"sha256":"9bee028606d971486bdf8afe8402a0c4e6c7dc297b8ce8233f0103ff55229c24","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"8bea1dedad1775ad890f36a07ca0f4e1cb2b031b94346edfe3593b6a04f83b7d","s… | {"sha256":"d3c7fd913de930ab12fd341273263793621fa06407e38d3b759881b34e19f655","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.canonical.specVersion` | modified | "1.0.2" | "1.0.3" |
| canonical | `$.canonical.updateState.appliedUpdates[1]` | added | — | {"appliedAt":"2026-08-26T22:30:14+09:00","fromContentVersion":"1.0.0","id":"U-20260826-009","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| canonical | `$.files[0].sha256` | modified | "bfe93c2e32a6c34f659eda70fa31debf795b5e9200a0766e4f8e228a99000323" | "f3a170d72db5816034242eb334241e1b3aa65321641ad32304a0d64f7570ef53" |
| canonical | `$.files[0].size` | modified | 28524 | 28777 |
| spec | `$.files[0].sha256` | modified | "f97bc280305f46e0b199e68c322318570cbb4787cad785bdd0d70250f83d3f2e" | "9bee028606d971486bdf8afe8402a0c4e6c7dc297b8ce8233f0103ff55229c24" |
| spec | `$.files[0].size` | modified | 1348 | 1428 |
| spec | `$.files[1].sha256` | modified | "8bea1dedad1775ad890f36a07ca0f4e1cb2b031b94346edfe3593b6a04f83b7d" | "d3c7fd913de930ab12fd341273263793621fa06407e38d3b759881b34e19f655" |
| spec | `$.files[1].size` | modified | 16122 | 16330 |
| spec | `$.spec.principles.studentProjectionSource` | added | — | "answer-edition-after-browser-measured-response-layout" |
| spec | `$.spec.specVersion` | modified | "1.0.2" | "1.0.3" |
| spec | `$.spec.validationGates.compiled[4]` | modified | "student edition exposes no solution values" | "student response-area heights are copied from the browser-measured answer edition before solutions are removed" |
| spec | `$.spec.validationGates.compiled[5]` | modified | "every bank, target and slot cardinality is internally consistent" | "student edition exposes no solution values" |
| spec | `$.spec.validationGates.compiled[6]` | modified | "stage 10 student edition contains no English skeleton" | "every bank, target and slot cardinality is internally consistent" |
| spec | `$.spec.validationGates.compiled[7]` | added | — | "stage 10 student edition contains no English skeleton" |
| spec | `$.specVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.appliedUpdates[1]` | added | — | "U-20260826-009" |
| build | `$.buildVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.builtAt` | modified | "2026-08-25T15:54:47+09:00" | "2026-08-26T22:35:32+09:00" |
| build | `$.canonicalDigest` | modified | "540168f50b779cdbe563fa84df71dae8abf7900b5e1319d91d06add07e58043c" | "dc58970e62c04ba05b4f89d56fb136a28ecd7ec779c3dae3ccf117ea005e1903" |
| build | `$.compilerVersion` | modified | "1.0.2" | "1.0.4" |
| build | `$.contentVersion` | modified | "1.0.0" | "1.0.1" |
| build | `$.engineDigest` | modified | "b51bb9b758b4a296e3e5fa03c8af783a3626209e4cb1ee0cd519a6394e903d40" | "9afe922368d2a5cf2dcbc897eceea7a662069ced1216d20eff3541d1845a318b" |
| build | `$.engineInputs[0].sha256` | modified | "51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c" | "0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3" |
| build | `$.engineInputs[3].sha256` | modified | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" | "9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c" |
| build | `$.engineInputs[3].size` | modified | 14275 | 16639 |
| build | `$.engineInputs[7].sha256` | modified | "42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2" | "d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555" |
| build | `$.engineInputs[7].size` | modified | 31543 | 34434 |
| build | `$.engineInputs[8].sha256` | modified | "53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6" | "c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c" |
| build | `$.engineInputs[8].size` | modified | 29907 | 30969 |
| build | `$.files[0].sha256` | modified | "51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c" | "0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3" |
| build | `$.files[3].sha256` | modified | "01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840" | "9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c" |
| build | `$.files[3].size` | modified | 14275 | 16639 |
| build | `$.files[7].sha256` | modified | "42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2" | "d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555" |
| build | `$.files[7].size` | modified | 31543 | 34434 |
| build | `$.files[8].sha256` | modified | "53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6" | "c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c" |
| build | `$.files[8].size` | modified | 29907 | 30969 |
| build | `$.files[13].sha256` | modified | "f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d" | "b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39" |
| build | `$.files[13].size` | modified | 135532 | 136108 |
| build | `$.files[14].sha256` | modified | "62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db" | "3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e" |
| build | `$.files[14].size` | modified | 604376 | 604367 |
| build | `$.files[15].sha256` | modified | "02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293" | "7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17" |
| build | `$.files[15].size` | modified | 144674 | 145250 |
| build | `$.files[16].sha256` | modified | "36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39" | "73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776" |
| build | `$.files[16].size` | modified | 736196 | 736181 |
| build | `$.outputs[0].sha256` | modified | "f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d" | "b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39" |
| build | `$.outputs[0].size` | modified | 135532 | 136108 |
| build | `$.outputs[1].sha256` | modified | "62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db" | "3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e" |
| build | `$.outputs[1].size` | modified | 604376 | 604367 |
| build | `$.outputs[2].sha256` | modified | "02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293" | "7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17" |
| build | `$.outputs[2].size` | modified | 144674 | 145250 |
| build | `$.outputs[3].sha256` | modified | "36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39" | "73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776" |
| build | `$.outputs[3].size` | modified | 736196 | 736181 |
| build | `$.pages[3].digest` | modified | "3e90732671f4a672f94ff1d57398bc083233cc4c9285b7d61673454f2f4cab6e" | "a6a23bb1d33673ca8d1495643ce5b483fd2954db04080fb0752291d1f46a0251" |
| build | `$.pages[7].digest` | modified | "6b545385eaf10c9ca39f43c33876967e0221244f91bcdbf66c2d58a9719e9a4b" | "20733eb5e83e3d6a1f1bf094fcff0045d35f6576476dd2758a0f30f5ec47d0a7" |
| build | `$.pages[8].digest` | modified | "109c37aa6b386b300e3fdb8c201a61c4b6fabbfb694de3453a2820612d862e56" | "ed2378cac01ab5bd31fb2d6bb8e45245ea7600ff11e9fa74446cf466256fcda9" |
| build | `$.pages[10].digest` | modified | "28124c8923072745178a83f863373248c3fa2c4d8516cc479f82b39fd1416c9c" | "71ae50b5fc1c2de839c173ab6db281a023d6b52364539bf0eccdef64cfcbc32a" |
| build | `$.pages[14].digest` | modified | "bed5ed94da92d531756775fb980f22de001d3bf10634df2c3e00749463b1adc1" | "fd8456c3ff60e9b14643c159e5ecd5e75608947fd9af90ffa028d57a909e2db0" |
| build | `$.pages[18].digest` | modified | "65b36333fe9d76f3b380a5e6d3be3a0a3923931adaf0853a4bb0ed2128d037b9" | "cea550bf046a66670986df1f7f3fe62003de6cb20fb939e5b11b145162820946" |
| build | `$.pages[19].digest` | modified | "4a367a58db8e4dc8e4a15b092574d1650de4238c4e22211854136c56fee355c9" | "9b6722b79f47a08363168b79b3f7bd28cb4b984223e2f3d37cecd187b2df247f" |
| build | `$.pages[21].digest` | modified | "a20f04be793ebf3914b9a361065649d48bc8a3c0b5313c3eb792202becb9ea71" | "c0e9f9f5afeb84b90504b5d23e7d6704e8dce759812a7ca33b7ea32f4f357e4c" |
| build | `$.qa.dom.matchedResponseBoxCount` | added | — | 24 |
| build | `$.specVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 접촉 시트와 1·7·8·9·10단계, 8단계 1-4 및 5-8 연속 페이지를 확인함. 7단계 is 목표 위치가 representations is에 정확하며, 해설 정답만 빨강이고 모든 페이지·푸터에… | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 24칸의 높이가 일치하며, 잘림·겹침·정답 노출·비정상 빨강이 없습니다." |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-25T15:56:08+09:00" | "2026-08-26T22:36:12+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 4, 8, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:2026-june-grade2-q21-p04 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p08 | modified | 8 | s001, s002, s003, s004 |
| answer:2026-june-grade2-q21-p09 | modified | 8 | s005, s006, s007, s008 |
| answer:2026-june-grade2-q21-p11 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p04 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p08 | modified | 8 | s001, s002, s003, s004 |
| student:2026-june-grade2-q21-p09 | modified | 8 | s005, s006, s007, s008 |
| student:2026-june-grade2-q21-p11 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"f2fd176a6ea9f94925e896ac6325232bb22a88662ac8824fd2e9ee68667bbd8d","size":135532} | {"path":"문제.html","sha256":"b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39","size":136108} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"62c062ddd36ad14030d7eeb3605bc8eeb4d5e9ee61d32639d9e6c33f04d487db","size":604376} | {"path":"문제.pdf","sha256":"3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e","size":604367} |
| `해설.html` | modified | {"path":"해설.html","sha256":"02c7bd8533d27a25044949288948cd49a02c53873e16e919d35200aaa096b293","size":144674} | {"path":"해설.html","sha256":"7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17","size":145250} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"36225fc5e45543649a4f5d9e9b37dae9591dbcee461be146993560d63dd05f39","size":736196} | {"path":"해설.pdf","sha256":"73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776","size":736181} |

## 영향 없음

- 동일한 manifest 구성 요소: `template`
- 직접·파생 변경이 기록되지 않은 단계: 1, 2, 3, 5, 6, 7, 9
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| answer-first-projection | pass | 학생용이 해설용 IR의 답안 높이를 유지한 채 정답 데이터만 제거하는 단위 검사를 통과했습니다. |
| regression-suite | pass | 정본 5개 검증과 전체 회귀 검사 33개가 통과했습니다. |
| student-answer-height-match | pass | 브라우저가 학생용과 해설용의 모든 작성형 target 높이를 비교하며, 0.75px를 넘는 차이를 릴리스 차단 조건으로 검증합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.0 | 1.0.1 |
| spec | 1.0.2 | 1.0.3 |
| template | 1.0.1 | 1.0.1 |
| build | 1.0.0 | 1.0.1 |

## 변경 통계

- 직접 JSON 경로: 66
- 파생 JSON 경로: 0
- 변경·선언 파일: 17
- 영향 페이지: 8
- 변경 출력: 4
