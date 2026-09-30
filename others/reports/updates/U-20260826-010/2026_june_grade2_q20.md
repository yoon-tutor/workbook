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
| canonical | 1.0.1 | 1.0.2 | `4c91d72f4467` | `4703cc902eed` | 변경 |
| spec | 1.0.3 | 1.0.4 | `5f1517bd2a24` | `a0f160946460` | 변경 |
| template | 1.0.1 | 1.0.2 | `6456357b00c6` | `6f15a4b662e3` | 변경 |
| build | 1.0.1 | 1.0.2 | `7e9d68d09f64` | `1e90e86dae9b` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"0837ba886ad3323de7f411eead932a4fc8ec242038ff446e15ff59972c8d61c3","s… | {"sha256":"c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40","s… | {"sha256":"6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8","s… | {"sha256":"554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c","s… | {"sha256":"c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310","s… | {"sha256":"ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"9b56ebf4c586a0e085f1ec45d4687ae94bfa425739a216a9edbfba617184be7c","s… | {"sha256":"7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"d14a4802e5fab9c9bef9a917c723961b499a674d386bc5dbcfd325549b760555","s… | {"sha256":"0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"c424a3d9d8f2ed758c5903da17d3e54603b06cbe9e6689e352023af7e8de561c","s… | {"sha256":"592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q20/content.json` | modified | {"sha256":"f5e543251994eaecec29802d2a142471832c877d536873e84d6d6a3421111dc6","s… | {"sha256":"aa0d3e4c6c4e7cb9907dda10bd2787855cb8a1fc511e2020a6eaf16067c6648d","s… |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q21/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "f5e543251994eaecec29802d2a142471832c877d536873e84d6d6a3421111dc6" | "aa0d3e4c6c4e7cb9907dda10bd2787855cb8a1fc511e2020a6eaf16067c6648d" |
| canonical | `$.files[0].size` | modified | 25896 | 26149 |
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
| build | `$.canonicalDigest` | modified | "01449f46052327ad2c89ce360291b98c7f4bbca8b9f083f442095556f1c74269" | "618dbfa8dcc94b4756963e5f16359fbdc8035d5de267c05f766ccb389a34d931" |
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
| build | `$.files[13].sha256` | modified | "d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40" | "6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765" |
| build | `$.files[13].size` | modified | 132596 | 136679 |
| build | `$.files[14].sha256` | modified | "941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8" | "554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f" |
| build | `$.files[14].size` | modified | 565067 | 567469 |
| build | `$.files[15].sha256` | modified | "99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c" | "c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a" |
| build | `$.files[15].size` | modified | 140942 | 145025 |
| build | `$.files[16].sha256` | modified | "cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310" | "ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f" |
| build | `$.files[16].size` | modified | 683484 | 684752 |
| build | `$.outputs[0].sha256` | modified | "d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40" | "6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765" |
| build | `$.outputs[0].size` | modified | 132596 | 136679 |
| build | `$.outputs[1].sha256` | modified | "941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8" | "554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f" |
| build | `$.outputs[1].size` | modified | 565067 | 567469 |
| build | `$.outputs[2].sha256` | modified | "99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c" | "c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a" |
| build | `$.outputs[2].size` | modified | 140942 | 145025 |
| build | `$.outputs[3].sha256` | modified | "cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310" | "ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f" |
| build | `$.outputs[3].size` | modified | 683484 | 684752 |
| build | `$.pages[3].digest` | modified | "a7b8f2c1c61e63c8106893ea25b190420b108b20d2ce478ab15befd34217ff48" | "b1593bc420f7410851bfd4ea0fdd0a843d8fb1ec29c599fa26ae30d9f85ce54f" |
| build | `$.pages[7].digest` | modified | "91afdf6bbf685e558adff79cbb29f2f133d97f4db8e3ff98257507450bed37a5" | "28fb8a721fbc5549cc468683d0e56badc404663406d03152d84ee6766c5df6bb" |
| build | `$.pages[9].digest` | modified | "72d677cf67e182ae32bf7c63f8c7414e64d3672e8cd1a3be7f40e59d00e2ed45" | "acfbacccfb38b0f55bdbe018c3e29b410792edd845fec2a8074f558dac404a70" |
| build | `$.pages[13].digest` | modified | "f08356a8310657a61715207ef58fd32d71d32ba2823f32b1924e5144e64b2d1d" | "e6a2ec2ec876b2ec5f1f30d612dada34cc1ec8a110d9e751cfd287ff8371c041" |
| build | `$.pages[17].digest` | modified | "34b78a7a41a753e3ebda7ddf7b076a766c54ffa5b9831143a2ea0889595c9a66" | "1aebd06f6b7c8dc5039a79b38795545d921a92e707c75f3db009b56443a9ca21" |
| build | `$.pages[19].digest` | modified | "2e82fe10c0765f9b277873a8e2ce839967666ec553d4afe9772db7bb04d7f646" | "6f7939700fe5e9a828415e1bc31c224e1111906ecf58a56d658c966fd71e05d3" |
| build | `$.qa.dom.matchedResponseLineCount` | added | — | 32 |
| build | `$.specVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.templateVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 18칸의 높이가 일치하며, 잘림·겹침·정답 노출·비정상 빨강이 없습니다." | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 18칸, 답안 32줄의 위치·가로 길이·높이가 일치하며 잘림·겹침·정답 노출·비정상 빨강이 없습니다." |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-26T22:35:59+09:00" | "2026-08-26T22:45:15+09:00" |

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
| `문제.html` | modified | {"path":"문제.html","sha256":"d08399db99cb13f6e2dc014a40dcf807f8c26e819c6ec3718929df98df74ce40","size":132596} | {"path":"문제.html","sha256":"6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765","size":136679} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"941f176657409668d768dcd8288b1497197d48d5b892cf715b1435cfb519a0a8","size":565067} | {"path":"문제.pdf","sha256":"554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f","size":567469} |
| `해설.html` | modified | {"path":"해설.html","sha256":"99a28d1dc3a7ebf663d7198aa834a9fd235d615fe09c36006470f9093267d23c","size":140942} | {"path":"해설.html","sha256":"c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a","size":145025} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"cb01f32b0bb7aea8f84ceda30ebce8486d901a204b87195ae21dafe1daac8310","size":683484} | {"path":"해설.pdf","sha256":"ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f","size":684752} |

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

- 직접 JSON 경로: 64
- 파생 JSON 경로: 0
- 변경·선언 파일: 20
- 영향 페이지: 6
- 변경 출력: 4
