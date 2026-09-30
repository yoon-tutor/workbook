# 업데이트 보고서 `U-20260826-010`: 해설 답안 줄 전체 형상 복제

## 요약

해설용 작성 답안의 줄별 위치·가로 길이·높이를 브라우저에서 측정하고, 동일한 형상을 유지한 채 답 글자만 제거하여 학생용을 생성합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260826-010` |
| 날짜 | 2026-08-26 |
| 분류 | `layout-and-release` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 서술형 문제본은 해설용 답안에서 글자만 지운 것처럼, 답안의 세로 높이뿐 아니라 각 줄의 가로 길이까지 동일하게 만듭니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.1 | 1.0.2 | `095f8aa8aef9` | `c2aa8ebccd1e` | 변경 |
| spec | 1.0.3 | 1.0.4 | `5f1517bd2a24` | `a0f160946460` | 변경 |
| template | 1.0.1 | 1.0.2 | `6456357b00c6` | `6f15a4b662e3` | 변경 |
| build | 1.0.1 | 1.0.2 | `1baaeffadb65` | `36f4f3ea2eff` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3","s… | {"sha256":"c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39","s… | {"sha256":"645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e","s… | {"sha256":"196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17","s… | {"sha256":"8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776","s… | {"sha256":"b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c","s… | {"sha256":"7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555","s… | {"sha256":"0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c","s… | {"sha256":"592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q21/content.json` | modified | {"sha256":"f3a170d72db5816034242eb334241e1b3aa65321641ad32304a0d64f7570ef53","s… | {"sha256":"bb12cc1bcb43b449408a41f83710949848fb64d91ffbb5f739f4431310c09e8c","s… |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q20/content.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"9bee028606d971486bdf8afe8402a0c4e6c7dc297b8ce8233f0103ff55229c24","s… | {"sha256":"4c2ccfab59c3714191ec938c25f4858922faec98a21d3f768b62e99ca728079a","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"d3c7fd913de930ab12fd341273263793621fa06407e38d3b759881b34e19f655","s… | {"sha256":"2f7c885febbb8519c7ef40b2a9bfda796164fd9f058511d5928db4c5070671ac","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | modified | {"sha256":"b8d6cf61d980afcfa0160d91fe87b73d535cc2ab80bac66964f45a9e0ec2345e","s… | {"sha256":"17971b7d4035cc58beb6bcea518e42d89bb4a54ac411860560e61fe9c3298bcd","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | modified | {"sha256":"fbce767b88b805800c5f03a51bfbe5c61985a55131b8624e43ab87acd5de3761","s… | {"sha256":"593f7a5b59a910f15f20b0a399919931535b2b0b6468ee00d8863aa089534be8","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.1" | "1.0.2" |
| canonical | `$.canonical.specVersion` | modified | "1.0.3" | "1.0.4" |
| canonical | `$.canonical.updateState.appliedUpdates[2]` | added | — | {"appliedAt":"2026-08-26T22:42:19+09:00","fromContentVersion":"1.0.1","id":"U-20260826-010","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.1" | "1.0.2" |
| canonical | `$.files[0].sha256` | modified | "f3a170d72db5816034242eb334241e1b3aa65321641ad32304a0d64f7570ef53" | "bb12cc1bcb43b449408a41f83710949848fb64d91ffbb5f739f4431310c09e8c" |
| canonical | `$.files[0].size` | modified | 28777 | 29030 |
| spec | `$.files[0].sha256` | modified | "9bee028606d971486bdf8afe8402a0c4e6c7dc297b8ce8233f0103ff55229c24" | "4c2ccfab59c3714191ec938c25f4858922faec98a21d3f768b62e99ca728079a" |
| spec | `$.files[0].size` | modified | 1428 | 1495 |
| spec | `$.files[1].sha256` | modified | "d3c7fd913de930ab12fd341273263793621fa06407e38d3b759881b34e19f655" | "2f7c885febbb8519c7ef40b2a9bfda796164fd9f058511d5928db4c5070671ac" |
| spec | `$.files[1].size` | modified | 16330 | 16356 |
| spec | `$.spec.specVersion` | modified | "1.0.3" | "1.0.4" |
| spec | `$.spec.validationGates.compiled[4]` | modified | "student response-area heights are copied from the browser-measured answer edition before solutions are removed" | "student response-line positions, widths, and heights are copied from the browser-measured answer edition before soluti… |
| spec | `$.specVersion` | modified | "1.0.3" | "1.0.4" |
| template | `$.files[1].sha256` | modified | "b8d6cf61d980afcfa0160d91fe87b73d535cc2ab80bac66964f45a9e0ec2345e" | "17971b7d4035cc58beb6bcea518e42d89bb4a54ac411860560e61fe9c3298bcd" |
| template | `$.files[1].size` | modified | 40565 | 41474 |
| template | `$.files[3].sha256` | modified | "fbce767b88b805800c5f03a51bfbe5c61985a55131b8624e43ab87acd5de3761" | "593f7a5b59a910f15f20b0a399919931535b2b0b6468ee00d8863aa089534be8" |
| template | `$.files[3].size` | modified | 14590 | 14934 |
| template | `$.templateVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.appliedUpdates[2]` | added | — | "U-20260826-010" |
| build | `$.buildVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.builtAt` | modified | "2026-08-26T22:35:32+09:00" | "2026-08-26T22:44:40+09:00" |
| build | `$.canonicalDigest` | modified | "dc58970e62c04ba05b4f89d56fb136a28ecd7ec779c3dae3ccf117ea005e1903" | "621d1318b0a57a2895ece6d5126a6f98d18d10e75cedb647820d56902d786f29" |
| build | `$.compilerVersion` | modified | "1.0.4" | "1.0.5" |
| build | `$.contentVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.engineDigest` | modified | "9afe922368d2a5cf2dcbc897eceea7a662069ced1216d20eff3541d1845a318b" | "98844f0174897aa69861255def4b02aa8bd363195a4eb60bd2ac207a72dd6d47" |
| build | `$.engineInputs[0].sha256` | modified | "0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3" | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" |
| build | `$.engineInputs[3].sha256` | modified | "9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c" | "7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e" |
| build | `$.engineInputs[3].size` | modified | 16639 | 17976 |
| build | `$.engineInputs[7].sha256` | modified | "d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555" | "0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604" |
| build | `$.engineInputs[7].size` | modified | 34434 | 39612 |
| build | `$.engineInputs[8].sha256` | modified | "c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c" | "592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f" |
| build | `$.files[0].sha256` | modified | "0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3" | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" |
| build | `$.files[3].sha256` | modified | "9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c" | "7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e" |
| build | `$.files[3].size` | modified | 16639 | 17976 |
| build | `$.files[7].sha256` | modified | "d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555" | "0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604" |
| build | `$.files[7].size` | modified | 34434 | 39612 |
| build | `$.files[8].sha256` | modified | "c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c" | "592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f" |
| build | `$.files[13].sha256` | modified | "b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39" | "645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1" |
| build | `$.files[13].size` | modified | 136108 | 140652 |
| build | `$.files[14].sha256` | modified | "3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e" | "196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274" |
| build | `$.files[14].size` | modified | 604367 | 607515 |
| build | `$.files[15].sha256` | modified | "7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17" | "8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef" |
| build | `$.files[15].size` | modified | 145250 | 149794 |
| build | `$.files[16].sha256` | modified | "73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776" | "b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9" |
| build | `$.files[16].size` | modified | 736181 | 738231 |
| build | `$.outputs[0].sha256` | modified | "b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39" | "645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1" |
| build | `$.outputs[0].size` | modified | 136108 | 140652 |
| build | `$.outputs[1].sha256` | modified | "3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e" | "196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274" |
| build | `$.outputs[1].size` | modified | 604367 | 607515 |
| build | `$.outputs[2].sha256` | modified | "7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17" | "8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef" |
| build | `$.outputs[2].size` | modified | 145250 | 149794 |
| build | `$.outputs[3].sha256` | modified | "73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776" | "b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9" |
| build | `$.outputs[3].size` | modified | 736181 | 738231 |
| build | `$.pages[3].digest` | modified | "a6a23bb1d33673ca8d1495643ce5b483fd2954db04080fb0752291d1f46a0251" | "eff89666fa3992429cf3383c5c52a29d534bb154202800311a916388e44bbf02" |
| build | `$.pages[7].digest` | modified | "20733eb5e83e3d6a1f1bf094fcff0045d35f6576476dd2758a0f30f5ec47d0a7" | "7edce66aef1674914f16e2b4e267db67d24c272c1cc01a8d2333f157093f641f" |
| build | `$.pages[8].digest` | modified | "ed2378cac01ab5bd31fb2d6bb8e45245ea7600ff11e9fa74446cf466256fcda9" | "33faf8aaa767880665aff7fbe1c8831c8af7dfd007c8092f4580a1fcd36e8818" |
| build | `$.pages[10].digest` | modified | "71ae50b5fc1c2de839c173ab6db281a023d6b52364539bf0eccdef64cfcbc32a" | "b0ad22eb6dda0dd0982132aa75e360664a5b065c1ffc10fe02c0ba83da0c916e" |
| build | `$.pages[14].digest` | modified | "fd8456c3ff60e9b14643c159e5ecd5e75608947fd9af90ffa028d57a909e2db0" | "553ea049ac1f991abe6cc43e5f5eaae478a07b7a604e57fd1d45a87fbc098592" |
| build | `$.pages[18].digest` | modified | "cea550bf046a66670986df1f7f3fe62003de6cb20fb939e5b11b145162820946" | "3cb4a2ae6b95b02983f80835e879f2dc75c907198936d5813ded37afab02a0c7" |
| build | `$.pages[19].digest` | modified | "9b6722b79f47a08363168b79b3f7bd28cb4b984223e2f3d37cecd187b2df247f" | "e3080477919db5544e81a828d0654535346afc71bcca2f5b56d3dbf9e135848c" |
| build | `$.pages[21].digest` | modified | "c0e9f9f5afeb84b90504b5d23e7d6704e8dce759812a7ca33b7ea32f4f357e4c" | "495140773be7b7276d527979217f01d6c49dbb3301e48621ee1fe0c397704393" |
| build | `$.qa.dom.matchedResponseLineCount` | added | — | 35 |
| build | `$.specVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.templateVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 24칸의 높이가 일치하며, 잘림·겹침·정답 노출·비정상 빨강이 없습니다." | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 24칸, 답안 35줄의 위치·가로 길이·높이가 일치하며 잘림·겹침·정답 노출·비정상 빨강이 없습니다." |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-26T22:36:12+09:00" | "2026-08-26T22:45:27+09:00" |

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
| `문제.html` | modified | {"path":"문제.html","sha256":"b919a8234103bc0424cfbc31b07c06df61dc107d060626ef33974a2627bb9a39","size":136108} | {"path":"문제.html","sha256":"645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1","size":140652} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"3d32bd6ea2bc60b5625f8220b45523e179bbdd79a14a0fe58306ae2e7d3c505e","size":604367} | {"path":"문제.pdf","sha256":"196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274","size":607515} |
| `해설.html` | modified | {"path":"해설.html","sha256":"7befb13577a175d2a7686e2b1e14883235f9434c79ca4b62bd16ebf2821ccf17","size":145250} | {"path":"해설.html","sha256":"8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef","size":149794} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"73941b829eca17f14584fc478158fec0f2f0818ec2644e40c04625270e440776","size":736181} | {"path":"해설.pdf","sha256":"b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9","size":738231} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 1, 2, 3, 5, 6, 7, 9
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| answer-first-geometry-projection | pass | 학생용이 해설용의 측정된 줄별 위치·가로 길이·높이를 유지하고 정답 데이터만 제거하는 단위 검사를 통과했습니다. |
| regression-suite | pass | 정본 5개 검증과 전체 회귀 검사 33개가 통과했습니다. |
| student-answer-line-geometry-match | pass | 브라우저가 학생용 빈 작성선과 해설 답안의 각 줄에 대해 위치·가로 길이·높이를 비교하며, 0.75px를 넘는 차이를 릴리스 차단 조건으로 검증합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.1 | 1.0.2 |
| spec | 1.0.3 | 1.0.4 |
| template | 1.0.1 | 1.0.2 |
| build | 1.0.1 | 1.0.2 |

## 변경 통계

- 직접 JSON 경로: 66
- 파생 JSON 경로: 0
- 변경·선언 파일: 20
- 영향 페이지: 8
- 변경 출력: 4
