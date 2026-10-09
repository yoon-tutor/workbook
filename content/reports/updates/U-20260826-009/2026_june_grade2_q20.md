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
| canonical | 1.0.0 | 1.0.1 | `f0205981b992` | `4c91d72f4467` | 변경 |
| spec | 1.0.2 | 1.0.3 | `94237af0a7ed` | `5f1517bd2a24` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.0 | 1.0.1 | `bb68948adb18` | `7e9d68d09f64` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… | {"sha256":"0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"3eae2a4ca30fec441f6e16cf88b49f0c0f96a973bf4863f5e2708a0c922ca5cc","s… | {"sha256":"d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"c17cd88a9a462f59e33895abfe48b6398b461dfad238ed664a4a6d46983a796e","s… | {"sha256":"941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"412698d445f914dc9f018ce9c8ca9d428d3b2eb12a94f2e2e033e81ce7d8c228","s… | {"sha256":"99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"7e527c4c474be85725d6866fef2a18103b40e0c76dd48eec44fb59ad0f09a877","s… | {"sha256":"cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"01a494e0ac7cf8d607340e9d06fe9a910fa1cd1b1422c73dc7b1d76b44e8d840","s… | {"sha256":"9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"42d8b5216b70fa0eaba08421b78fdbf50f1021f41e2dc1a31805adbef9c0e4b2","s… | {"sha256":"d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"53f264feb5b216ac0a4daec4eb23213bb407ce29a70a014ea0c4d6916832eed6","s… | {"sha256":"c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q20/content.json` | modified | {"sha256":"65a25d699aa8d469f9937f75dfa602a109962837dcce117fe8e81c75806a44a2","s… | {"sha256":"f5e543251994eaecec29802d2a142471832c877d536873e84d6d6a3421111dc6","s… |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q21/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "65a25d699aa8d469f9937f75dfa602a109962837dcce117fe8e81c75806a44a2" | "f5e543251994eaecec29802d2a142471832c877d536873e84d6d6a3421111dc6" |
| canonical | `$.files[0].size` | modified | 25643 | 25896 |
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
| build | `$.builtAt` | modified | "2026-08-25T15:52:41+09:00" | "2026-08-26T22:35:32+09:00" |
| build | `$.canonicalDigest` | modified | "d4de9ee9646f8035fa7aa8f885859ac7e08f0739f671e26b4d290e179e8e8c88" | "01449f46052327ad2c89ce360291b98c7f4bbca8b9f083f442095556f1c74269" |
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
| build | `$.files[13].sha256` | modified | "3eae2a4ca30fec441f6e16cf88b49f0c0f96a973bf4863f5e2708a0c922ca5cc" | "d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40" |
| build | `$.files[13].size` | modified | 132164 | 132596 |
| build | `$.files[14].sha256` | modified | "c17cd88a9a462f59e33895abfe48b6398b461dfad238ed664a4a6d46983a796e" | "941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8" |
| build | `$.files[14].size` | modified | 565062 | 565067 |
| build | `$.files[15].sha256` | modified | "412698d445f914dc9f018ce9c8ca9d428d3b2eb12a94f2e2e033e81ce7d8c228" | "99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c" |
| build | `$.files[15].size` | modified | 140510 | 140942 |
| build | `$.files[16].sha256` | modified | "7e527c4c474be85725d6866fef2a18103b40e0c76dd48eec44fb59ad0f09a877" | "cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310" |
| build | `$.files[16].size` | modified | 683488 | 683484 |
| build | `$.outputs[0].sha256` | modified | "3eae2a4ca30fec441f6e16cf88b49f0c0f96a973bf4863f5e2708a0c922ca5cc" | "d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40" |
| build | `$.outputs[0].size` | modified | 132164 | 132596 |
| build | `$.outputs[1].sha256` | modified | "c17cd88a9a462f59e33895abfe48b6398b461dfad238ed664a4a6d46983a796e" | "941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8" |
| build | `$.outputs[1].size` | modified | 565062 | 565067 |
| build | `$.outputs[2].sha256` | modified | "412698d445f914dc9f018ce9c8ca9d428d3b2eb12a94f2e2e033e81ce7d8c228" | "99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c" |
| build | `$.outputs[2].size` | modified | 140510 | 140942 |
| build | `$.outputs[3].sha256` | modified | "7e527c4c474be85725d6866fef2a18103b40e0c76dd48eec44fb59ad0f09a877" | "cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310" |
| build | `$.outputs[3].size` | modified | 683488 | 683484 |
| build | `$.pages[3].digest` | modified | "0b7d0a1cd33e506caf05d6b78bc0a97a9538a81f2718ef8f6579f4f0d8bd0b91" | "a7b8f2c1c61e63c8106893ea25b190420b108b20d2ce478ab15befd34217ff48" |
| build | `$.pages[7].digest` | modified | "f1e9c49ce931ad84d909138b15619d5bda08229b4dfe8738da046e3ddc410fb1" | "91afdf6bbf685e558adff79cbb29f2f133d97f4db8e3ff98257507450bed37a5" |
| build | `$.pages[9].digest` | modified | "23bc6ee5c9d50b5db0abc9a6ac8ad094984cfc51f33f0038d4a659be0d8e45ef" | "72d677cf67e182ae32bf7c63f8c7414e64d3672e8cd1a3be7f40e59d00e2ed45" |
| build | `$.pages[13].digest` | modified | "1a965fe28afdbd473837349a6faed2c19f70fbe84d7d09501e096491d5fe89c7" | "f08356a8310657a61715207ef58fd32d71d32ba2823f32b1924e5144e64b2d1d" |
| build | `$.pages[17].digest` | modified | "99db770419f2ede7a09af657cb7c80c167e466a79775b7ef7a05e175509ebdae" | "34b78a7a41a753e3ebda7ddf7b076a766c54ffa5b9831143a2ea0889595c9a66" |
| build | `$.pages[19].digest` | modified | "4a2c73ae7b42d03fe80b4e0a3ce03bfc432fd2dd1aa95e3ba0aaa67be4141091" | "2e82fe10c0765f9b277873a8e2ce839967666ec553d4afe9772db7bb04d7f646" |
| build | `$.qa.dom.matchedResponseBoxCount` | added | — | 18 |
| build | `$.specVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 접촉 시트와 1·7·8·9·10단계를 확인함. 6개 문장 전체, 7단계 검정 오답과 해설 정답 빨강, 8단계 긴 답안 영역의 완성 문장, 문단 순서, 마지막 쪽과 푸터에 잘림·겹침·정답 노출이 없음… | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 18칸의 높이가 일치하며, 잘림·겹침·정답 노출·비정상 빨강이 없습니다." |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-25T15:56:00+09:00" | "2026-08-26T22:35:59+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 4, 8, 10 |
| 문항 | s001, s002, s003, s004, s005, s006 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:2026-june-grade2-q20-p04 | modified | 4 | s001, s002, s003, s004, s005, s006 |
| answer:2026-june-grade2-q20-p08 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:2026-june-grade2-q20-p10 | modified | 10 | s001, s002, s003, s004, s005, s006 |
| student:2026-june-grade2-q20-p04 | modified | 4 | s001, s002, s003, s004, s005, s006 |
| student:2026-june-grade2-q20-p08 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:2026-june-grade2-q20-p10 | modified | 10 | s001, s002, s003, s004, s005, s006 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"3eae2a4ca30fec441f6e16cf88b49f0c0f96a973bf4863f5e2708a0c922ca5cc","size":132164} | {"path":"문제.html","sha256":"d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40","size":132596} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"c17cd88a9a462f59e33895abfe48b6398b461dfad238ed664a4a6d46983a796e","size":565062} | {"path":"문제.pdf","sha256":"941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8","size":565067} |
| `해설.html` | modified | {"path":"해설.html","sha256":"412698d445f914dc9f018ce9c8ca9d428d3b2eb12a94f2e2e033e81ce7d8c228","size":140510} | {"path":"해설.html","sha256":"99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c","size":140942} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"7e527c4c474be85725d6866fef2a18103b40e0c76dd48eec44fb59ad0f09a877","size":683488} | {"path":"해설.pdf","sha256":"cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310","size":683484} |

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

- 직접 JSON 경로: 64
- 파생 JSON 경로: 0
- 변경·선언 파일: 17
- 영향 페이지: 6
- 변경 출력: 4
