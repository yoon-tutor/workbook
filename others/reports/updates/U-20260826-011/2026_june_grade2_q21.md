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
| canonical | 1.0.2 | 1.0.3 | `c2aa8ebccd1e` | `91edca503ed7` | 변경 |
| spec | 1.0.4 | 1.0.5 | `a0f160946460` | `5d51719ab734` | 변경 |
| template | 1.0.2 | 1.0.3 | `6f15a4b662e3` | `bf9fbd837d50` | 변경 |
| build | 1.0.2 | 1.0.3 | `36f4f3ea2eff` | `153cd4208dc6` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `workbook_engine/__init__.py` | modified | {"sha256":"c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405","s… | {"sha256":"c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1","s… |
| 파생 | build | `문제.html` | modified | {"sha256":"645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1","s… | {"sha256":"3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274","s… | {"sha256":"6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef","s… | {"sha256":"a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9","s… | {"sha256":"9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q21/content.json` | modified | {"sha256":"bb12cc1bcb43b449408a41f83710949848fb64d91ffbb5f739f4431310c09e8c","s… | {"sha256":"e53591a13c31eeec1be55b158eabc745ad7eb81c7809145a8c7d72245ae7dbdd","s… |
| 직접 | declared | `updates/U-20260826-011.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q20/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "bb12cc1bcb43b449408a41f83710949848fb64d91ffbb5f739f4431310c09e8c" | "e53591a13c31eeec1be55b158eabc745ad7eb81c7809145a8c7d72245ae7dbdd" |
| canonical | `$.files[0].size` | modified | 29030 | 29283 |
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
| build | `$.canonicalDigest` | modified | "621d1318b0a57a2895ece6d5126a6f98d18d10e75cedb647820d56902d786f29" | "946a4348548bb03f3a12b33db72e3181cf111b0f86a9e518afd626b869b9bfbf" |
| build | `$.compilerVersion` | modified | "1.0.5" | "1.0.6" |
| build | `$.contentVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.engineDigest` | modified | "98844f0174897aa69861255def4b02aa8bd363195a4eb60bd2ac207a72dd6d47" | "9e405f4b6885cca274f4632926005ce451daccfa60a9e384cc6f5685d86cb382" |
| build | `$.engineInputs[0].sha256` | modified | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" |
| build | `$.files[0].sha256` | modified | "c6f58dc1d8e18aebef2275ba8bbb90180b79515168b2cf042e4ca0b870f27405" | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" |
| build | `$.files[13].sha256` | modified | "645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1" | "3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723" |
| build | `$.files[13].size` | modified | 140652 | 140643 |
| build | `$.files[14].sha256` | modified | "196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274" | "6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e" |
| build | `$.files[14].size` | modified | 607515 | 607245 |
| build | `$.files[15].sha256` | modified | "8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef" | "a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630" |
| build | `$.files[15].size` | modified | 149794 | 149785 |
| build | `$.files[16].sha256` | modified | "b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9" | "9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f" |
| build | `$.outputs[0].sha256` | modified | "645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1" | "3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723" |
| build | `$.outputs[0].size` | modified | 140652 | 140643 |
| build | `$.outputs[1].sha256` | modified | "196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274" | "6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e" |
| build | `$.outputs[1].size` | modified | 607515 | 607245 |
| build | `$.outputs[2].sha256` | modified | "8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef" | "a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630" |
| build | `$.outputs[2].size` | modified | 149794 | 149785 |
| build | `$.outputs[3].sha256` | modified | "b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9" | "9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f" |
| build | `$.specVersion` | modified | "1.0.4" | "1.0.5" |
| build | `$.templateVersion` | modified | "1.0.2" | "1.0.3" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·10단계 작성 페이지를 확인했습니다. 작성형 24칸, 답안 35줄의 위치·가로 길이·높이가 일치하며 잘림·겹침·정답 노출·비정상 빨강이 없습니다." | "학생용·해설용 전체 contact sheet와 4·8·11단계를 확인했습니다. 해설 문항의 박스·여백·가로 폭과 줄바꿈 공간을 유지하고 답 글자만 제거했으며, 별도 작성선·잘림·겹침·정답 노출·비정상 빨강이 없습… |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-26T22:45:27+09:00" | "2026-08-26T23:10:26+09:00" |

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
| `문제.html` | modified | {"path":"문제.html","sha256":"645c430ea9c00e39a6ba837518bf513b172ca1f30bf6451ecc915979378224a1","size":140652} | {"path":"문제.html","sha256":"3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723","size":140643} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"196dece3e661165c8fe96f41f69e07e3f2b48fa171a6767b1ae2e08f71775274","size":607515} | {"path":"문제.pdf","sha256":"6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e","size":607245} |
| `해설.html` | modified | {"path":"해설.html","sha256":"8f7497c9bea5b3209200baece325f7714fd9712c11de153379e5dab059340eef","size":149794} | {"path":"해설.html","sha256":"a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630","size":149785} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"b8448cb140c47996e73e6cdb435dabcadecb82a498d34ac6ea380a897bbcaef9","size":738231} | {"path":"해설.pdf","sha256":"9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f","size":738231} |

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
