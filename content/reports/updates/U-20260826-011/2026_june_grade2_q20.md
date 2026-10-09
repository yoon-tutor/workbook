# 업데이트 보고서 `U-20260826-011`: 해설 답안 글자만 제거한 문제본

## 요약

해설용 작성 문항의 박스와 답안 공간을 그대로 유지하고, 학생용에서는 답 글자만 제거해 별도의 작성선 없이 빈 공간으로 제공합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260826-011` |
| 날짜 | 2026-08-26 |
| 분류 | `layout-and-release` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 해설 문항을 그대로 복제한 뒤 빨간 답 글자만 지우고, 그 자리에 새 밑줄을 만들지 않은 문제본을 생성합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.2 | 1.0.3 | `4703cc902eed` | `fbf0ea768806` | 변경 |
| spec | 1.0.4 | 1.0.5 | `a0f160946460` | `5d51719ab734` | 변경 |
| template | 1.0.2 | 1.0.3 | `6f15a4b662e3` | `bf9fbd837d50` | 변경 |
| build | 1.0.2 | 1.0.3 | `1e90e86dae9b` | `1b3eb2be3de6` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405","s… | {"sha256":"c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765","s… | {"sha256":"6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f","s… | {"sha256":"26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a","s… | {"sha256":"9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f","s… | {"sha256":"33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q20/content.json` | modified | {"sha256":"aa0d3e4c6c4e7cb9907dda10bd2787855cb8a1fc511e2020a6eaf16067c6648d","s… | {"sha256":"4d8936d97b499059065a0793c1ae3fb72d3a0b9a6ca9cf4dfa81029d099b8d14","s… |
| 직접 | declared | `updates/U-20260826-011.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q21/content.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"4c2ccfab59c3714191ec938c25f4858922faec98a21d3f768b62e99ca728079a","s… | {"sha256":"e03942932f3e622c671a31d4d6de7f54a83cb8c6cf58af4aaa27dccebc9e1181","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"2f7c885febbb8519c7ef40b2a9bfda796164fd9f058511d5928db4c5070671ac","s… | {"sha256":"4fb72de1a415c5ebef5bc2b567259e25b8b75e83a532678276682f4f8977133b","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | modified | {"sha256":"593f7a5b59a910f15f20b0a399919931535b2b0b6468ee00d8863aa089534be8","s… | {"sha256":"129f5d60db487391989b19833d5fd79b28b526f7a0195dc770171127c6172c97","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.2" | "1.0.3" |
| canonical | `$.canonical.specVersion` | modified | "1.0.4" | "1.0.5" |
| canonical | `$.canonical.updateState.appliedUpdates[3]` | added | — | {"appliedAt":"2026-08-26T23:06:04+09:00","fromContentVersion":"1.0.2","id":"U-20260826-011","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.2" | "1.0.3" |
| canonical | `$.files[0].sha256` | modified | "aa0d3e4c6c4e7cb9907dda10bd2787855cb8a1fc511e2020a6eaf16067c6648d" | "4d8936d97b499059065a0793c1ae3fb72d3a0b9a6ca9cf4dfa81029d099b8d14" |
| canonical | `$.files[0].size` | modified | 26149 | 26402 |
| spec | `$.files[0].sha256` | modified | "4c2ccfab59c3714191ec938c25f4858922faec98a21d3f768b62e99ca728079a" | "e03942932f3e622c671a31d4d6de7f54a83cb8c6cf58af4aaa27dccebc9e1181" |
| spec | `$.files[0].size` | modified | 1495 | 1547 |
| spec | `$.files[1].sha256` | modified | "2f7c885febbb8519c7ef40b2a9bfda796164fd9f058511d5928db4c5070671ac" | "4fb72de1a415c5ebef5bc2b567259e25b8b75e83a532678276682f4f8977133b" |
| spec | `$.files[1].size` | modified | 16356 | 16456 |
| spec | `$.spec.specVersion` | modified | "1.0.4" | "1.0.5" |
| spec | `$.spec.validationGates.compiled[5]` | modified | "student edition exposes no solution values" | "student writing areas do not draw replacement guide lines after the answer text is removed" |
| spec | `$.spec.validationGates.compiled[6]` | modified | "every bank, target and slot cardinality is internally consistent" | "student edition exposes no solution values" |
| spec | `$.spec.validationGates.compiled[7]` | modified | "stage 10 student edition contains no English skeleton" | "every bank, target and slot cardinality is internally consistent" |
| spec | `$.spec.validationGates.compiled[8]` | added | — | "stage 10 student edition contains no English skeleton" |
| spec | `$.specVersion` | modified | "1.0.4" | "1.0.5" |
| template | `$.files[3].sha256` | modified | "593f7a5b59a910f15f20b0a399919931535b2b0b6468ee00d8863aa089534be8" | "129f5d60db487391989b19833d5fd79b28b526f7a0195dc770171127c6172c97" |
| template | `$.files[3].size` | modified | 14934 | 14925 |
| template | `$.templateVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.appliedUpdates[3]` | added | — | "U-20260826-011" |
| build | `$.buildVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.builtAt` | modified | "2026-08-26T22:44:40+09:00" | "2026-08-26T23:08:00+09:00" |
| build | `$.canonicalDigest` | modified | "618dbfa8dcc94b4756963e5f16359fbdc8035d5de267c05f766ccb389a34d931" | "06659276d83e546b50de7cc473edf7969ae07a1542b45c8e1c1a7c01b58dd360" |
| build | `$.compilerVersion` | modified | "1.0.5" | "1.0.6" |
| build | `$.contentVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.engineDigest` | modified | "98844f0174897aa69861255def4b02aa8bd363195a4eb60bd2ac207a72dd6d47" | "9e405f4b6885cca274f4632926005ce451daccfa60a9e384cc6f5685d86cb382" |
| build | `$.engineInputs[0].sha256` | modified | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" |
| build | `$.files[0].sha256` | modified | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" |
| build | `$.files[13].sha256` | modified | "6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765" | "6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14" |
| build | `$.files[13].size` | modified | 136679 | 136670 |
| build | `$.files[14].sha256` | modified | "554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f" | "26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c" |
| build | `$.files[14].size` | modified | 567469 | 567230 |
| build | `$.files[15].sha256` | modified | "c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a" | "9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da" |
| build | `$.files[15].size` | modified | 145025 | 145016 |
| build | `$.files[16].sha256` | modified | "ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f" | "33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d" |
| build | `$.outputs[0].sha256` | modified | "6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765" | "6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14" |
| build | `$.outputs[0].size` | modified | 136679 | 136670 |
| build | `$.outputs[1].sha256` | modified | "554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f" | "26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c" |
| build | `$.outputs[1].size` | modified | 567469 | 567230 |
| build | `$.outputs[2].sha256` | modified | "c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a" | "9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da" |
| build | `$.outputs[2].size` | modified | 145025 | 145016 |
| build | `$.outputs[3].sha256` | modified | "ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f" | "33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d" |
| build | `$.specVersion` | modified | "1.0.4" | "1.0.5" |
| build | `$.templateVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 18칸, 답안 32줄의 위치·가로 길이·높이가 일치하며 잘림·겹침·정답 노출·비정상 빨강이 없습니다." | "학생용·해설용 전체 contact sheet와 4·8·10단계를 확인했습니다. 해설 문항의 박스·여백·가로 폭과 줄바꿈 공간을 유지하고 답 글자만 제거했으며, 별도 작성선·잘림·겹침·정답 노출·비정상 빨강이 없습… |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-26T22:45:15+09:00" | "2026-08-26T23:10:26+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 4, 8, 10 |
| 문항 | 없음 |

### 페이지

변경 없음

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"6df4c8e0390899a3242b6095d7078d1d78c5460e99caeceb71bab123b1be2765","size":136679} | {"path":"문제.html","sha256":"6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14","size":136670} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"554bdb8a11cdf39795abe03efa10e1d945a7fd16bb3f5b147b1b77808a6afe7f","size":567469} | {"path":"문제.pdf","sha256":"26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c","size":567230} |
| `해설.html` | modified | {"path":"해설.html","sha256":"c42488a9da6712b6d7e1ee4f0ab605cd87b400120389e780de0efbd2f89a7c1a","size":145025} | {"path":"해설.html","sha256":"9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da","size":145016} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"ee2902d8224cf57f365bc3af46ab669c6f0ac31b601c91e81acec43c25f4799f","size":684752} | {"path":"해설.pdf","sha256":"33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d","size":684752} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 1, 2, 3, 5, 6, 7, 9
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| answer-only-text-removal | pass | 학생용은 해설 답안 줄의 측정 형상을 보존하되 답 글자와 대체 작성선을 모두 표시하지 않습니다. |
| regression-suite | pass | 정본 5개 검증과 전체 회귀 검사 33개가 통과했습니다. |
| student-answer-geometry-match | pass | 브라우저가 답 글자를 제거한 학생용 빈 공간과 해설 답안의 줄별 위치·가로 길이·높이를 비교합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.2 | 1.0.3 |
| spec | 1.0.4 | 1.0.5 |
| template | 1.0.2 | 1.0.3 |
| build | 1.0.2 | 1.0.3 |

## 변경 통계

- 직접 JSON 경로: 46
- 파생 JSON 경로: 0
- 변경·선언 파일: 15
- 영향 페이지: 0
- 변경 출력: 4
