# 업데이트 보고서 `U-20260826-012`: 해설 전체 형상에서 답만 제거한 문제본

## 요약

모든 정답 자리를 해설 브라우저 렌더링에서 먼저 측정하고, 문제본은 그 위치·가로·세로를 유지한 채 정답 값만 제거하도록 생성·검수·정리 절차를 전면 통일합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260826-012` |
| 날짜 | 2026-08-26 |
| 분류 | `layout-and-release` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- AGENTS, Python 생성기, JavaScript 렌더러, CSS, 검수 기준과 테스트를 모두 해설 우선·정답만 제거 원칙으로 수정하고, 품질과 콘텐츠에 필요 없는 중간 파일을 제거합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.3 | 1.0.4 | `fbf0ea768806` | `cf391b2d1515` | 변경 |
| spec | 1.0.5 | 1.0.6 | `5d51719ab734` | `99c2f3e65fe1` | 변경 |
| template | 1.0.3 | 1.0.4 | `bf9fbd837d50` | `248f772c4818` | 변경 |
| build | 1.0.3 | 1.0.4 | `1b3eb2be3de6` | `f9adf24d07f3` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14","s… | {"sha256":"557f3559673678ba0b761ebc19a846b15e96e255f03280f66612ac91ce1ac0f5","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c","s… | {"sha256":"54077126ff095cbcc3abb28c77cb1c0f0cd74fcca3d970dec770c232a10a9f51","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da","s… | {"sha256":"40d77763be1abee9fb213c4dd6ea7c745c5d737f0114985dfcd2fd215bf884d9","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d","s… | {"sha256":"383b4a5de46fa277a6044f8858abf9c06b1ecb7bdd17c4638177ab87e63a97e4","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1","s… | {"sha256":"af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e","s… | {"sha256":"30f60ef9ddb93dd7a8d3462a0fccb652ada4ae2d5703d5c2928ed6f7a65785b8","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604","s… | {"sha256":"24b628516d4feacd50a3bc7b18cafdd9d9c8d96246b33f69f9eeea8d327ba604","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f","s… | {"sha256":"097925500dc84f6a4bc13efab144343fcd4d6dbe1f1685fe1db5e87a7c90501e","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q20/content.json` | modified | {"sha256":"4d8936d97b499059065a0793c1ae3fb72d3a0b9a6ca9cf4dfa81029d099b8d14","s… | {"sha256":"65c4ba2c9269ec3ca24a9de09bc6baa0f7fbe2de312eb3615e95ee77f1fc9485","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `updates/U-20260826-012.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q21/content.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"e03942932f3e622c671a31d4d6de7f54a83cb8c6cf58af4aaa27dccebc9e1181","s… | {"sha256":"acd7a6469e17719beb827893b39a6608e8f270f2851b97e5d66de816dbf89a8f","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"4fb72de1a415c5ebef5bc2b567259e25b8b75e83a532678276682f4f8977133b","s… | {"sha256":"aadb3fe161b100e3a68ecb42fab51775e9738153a04278a53b27e7172f8d8f69","s… |
| 직접 | template | `workbook_engine/templates/renderer.js` | modified | {"sha256":"17971b7d4035cc58beb6bcea518e42d89bb4a54ac411860560e61fe9c3298bcd","s… | {"sha256":"25a21d18af7ee1100e7a4d0023af1175140e82dd2cce2a246d0fcd5ece2411ee","s… |
| 직접 | template | `workbook_engine/templates/workbook.css` | modified | {"sha256":"129f5d60db487391989b19833d5fd79b28b526f7a0195dc770171127c6172c97","s… | {"sha256":"ceab51f4246462f507a1de7c6aea850fb577113c37e74b4d98a645f23744a330","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.3" | "1.0.4" |
| canonical | `$.canonical.specVersion` | modified | "1.0.5" | "1.0.6" |
| canonical | `$.canonical.updateState.appliedUpdates[4]` | added | — | {"appliedAt":"2026-08-26T23:20:00+09:00","fromContentVersion":"1.0.3","id":"U-20260826-012","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.3" | "1.0.4" |
| canonical | `$.files[0].sha256` | modified | "4d8936d97b499059065a0793c1ae3fb72d3a0b9a6ca9cf4dfa81029d099b8d14" | "65c4ba2c9269ec3ca24a9de09bc6baa0f7fbe2de312eb3615e95ee77f1fc9485" |
| canonical | `$.files[0].size` | modified | 26402 | 26655 |
| spec | `$.files[0].sha256` | modified | "e03942932f3e622c671a31d4d6de7f54a83cb8c6cf58af4aaa27dccebc9e1181" | "acd7a6469e17719beb827893b39a6608e8f270f2851b97e5d66de816dbf89a8f" |
| spec | `$.files[0].size` | modified | 1547 | 1599 |
| spec | `$.files[1].sha256` | modified | "4fb72de1a415c5ebef5bc2b567259e25b8b75e83a532678276682f4f8977133b" | "aadb3fe161b100e3a68ecb42fab51775e9738153a04278a53b27e7172f8d8f69" |
| spec | `$.files[1].size` | modified | 16456 | 17021 |
| spec | `$.spec.answerEditionContract.choicePromptVisibleInAnswer` | added | — | true |
| spec | `$.spec.answerEditionContract.studentDerivation` | added | — | "render answer first, lock every solution slot and writing response geometry, then remove solution values only" |
| spec | `$.spec.principles.studentProjectionSource` | modified | "answer-edition-after-browser-measured-response-layout" | "answer-edition-after-browser-measured-all-solution-layouts" |
| spec | `$.spec.specVersion` | modified | "1.0.5" | "1.0.6" |
| spec | `$.spec.validationGates.compiled[4]` | modified | "student response-line positions, widths, and heights are copied from the browser-measured answer edition before soluti… | "every non-writing solution-slot position, width, and height is copied from the browser-measured answer edition before … |
| spec | `$.spec.validationGates.compiled[5]` | modified | "student writing areas do not draw replacement guide lines after the answer text is removed" | "student response-line positions, widths, and heights are copied from the browser-measured answer edition before soluti… |
| spec | `$.spec.validationGates.compiled[6]` | modified | "student edition exposes no solution values" | "student writing areas do not draw replacement guide lines after the answer text is removed" |
| spec | `$.spec.validationGates.compiled[7]` | modified | "every bank, target and slot cardinality is internally consistent" | "student edition exposes no solution values" |
| spec | `$.spec.validationGates.compiled[8]` | modified | "stage 10 student edition contains no English skeleton" | "every bank, target and slot cardinality is internally consistent" |
| spec | `$.spec.validationGates.compiled[9]` | added | — | "stage 10 student edition contains no English skeleton" |
| spec | `$.spec.validationGates.rendered[7]` | modified | "representative and risk pages pass visual review" | "every student and answer non-writing solution-slot has matching page-relative left, top, width, and height within 0.75… |
| spec | `$.spec.validationGates.rendered[8]` | added | — | "every student and answer writing response box and answer-line trace matches within 0.75px" |
| spec | `$.spec.validationGates.rendered[9]` | added | — | "representative and risk pages pass visual review" |
| spec | `$.specVersion` | modified | "1.0.5" | "1.0.6" |
| template | `$.files[1].sha256` | modified | "17971b7d4035cc58beb6bcea518e42d89bb4a54ac411860560e61fe9c3298bcd" | "25a21d18af7ee1100e7a4d0023af1175140e82dd2cce2a246d0fcd5ece2411ee" |
| template | `$.files[1].size` | modified | 41474 | 42558 |
| template | `$.files[3].sha256` | modified | "129f5d60db487391989b19833d5fd79b28b526f7a0195dc770171127c6172c97" | "ceab51f4246462f507a1de7c6aea850fb577113c37e74b4d98a645f23744a330" |
| template | `$.files[3].size` | modified | 14925 | 15185 |
| template | `$.templateVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.appliedUpdates[4]` | added | — | "U-20260826-012" |
| build | `$.buildVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.builtAt` | modified | "2026-08-26T23:08:00+09:00" | "2026-08-26T23:22:22+09:00" |
| build | `$.canonicalDigest` | modified | "06659276d83e546b50de7cc473edf7969ae07a1542b45c8e1c1a7c01b58dd360" | "f28e5b74fe63489c7319af9232a43abb8c242c7fe7be1a2c05ad3f55e5e62a3f" |
| build | `$.compilerVersion` | modified | "1.0.6" | "1.0.7" |
| build | `$.contentVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.engineDigest` | modified | "9e405f4b6885cca274f4632926005ce451daccfa60a9e384cc6f5685d86cb382" | "755fa39f2f38e0c481da489f7b37fc92110b71ae3cf018dda83004df187ac114" |
| build | `$.engineInputs[0].sha256` | modified | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" | "af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd" |
| build | `$.engineInputs[3].sha256` | modified | "7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e" | "30f60ef9ddb93dd7a8d3462a0fccb652ada4ae2d5703d5c2928ed6f7a65785b8" |
| build | `$.engineInputs[3].size` | modified | 17976 | 19480 |
| build | `$.engineInputs[7].sha256` | modified | "0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604" | "24b628516d4feacd50a3bc7b18cafdd9d9c8d96246b33f69f9eeea8d327ba604" |
| build | `$.engineInputs[7].size` | modified | 39612 | 43563 |
| build | `$.engineInputs[8].sha256` | modified | "592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f" | "097925500dc84f6a4bc13efab144343fcd4d6dbe1f1685fe1db5e87a7c90501e" |
| build | `$.engineInputs[8].size` | modified | 30969 | 31383 |
| build | `$.files[0].sha256` | modified | "c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1" | "af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd" |
| build | `$.files[3].sha256` | modified | "7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e" | "30f60ef9ddb93dd7a8d3462a0fccb652ada4ae2d5703d5c2928ed6f7a65785b8" |
| build | `$.files[3].size` | modified | 17976 | 19480 |
| build | `$.files[7].sha256` | modified | "0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604" | "24b628516d4feacd50a3bc7b18cafdd9d9c8d96246b33f69f9eeea8d327ba604" |
| build | `$.files[7].size` | modified | 39612 | 43563 |
| build | `$.files[8].sha256` | modified | "592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f" | "097925500dc84f6a4bc13efab144343fcd4d6dbe1f1685fe1db5e87a7c90501e" |
| build | `$.files[8].size` | modified | 30969 | 31383 |
| build | `$.files[13].sha256` | modified | "6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14" | "557f3559673678ba0b761ebc19a846b15e96e255f03280f66612ac91ce1ac0f5" |
| build | `$.files[13].size` | modified | 136670 | 141063 |
| build | `$.files[14].sha256` | modified | "26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c" | "54077126ff095cbcc3abb28c77cb1c0f0cd74fcca3d970dec770c232a10a9f51" |
| build | `$.files[14].size` | modified | 567230 | 567269 |
| build | `$.files[15].sha256` | modified | "9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da" | "40d77763be1abee9fb213c4dd6ea7c745c5d737f0114985dfcd2fd215bf884d9" |
| build | `$.files[15].size` | modified | 145016 | 149409 |
| build | `$.files[16].sha256` | modified | "33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d" | "383b4a5de46fa277a6044f8858abf9c06b1ecb7bdd17c4638177ab87e63a97e4" |
| build | `$.files[16].size` | modified | 684752 | 689653 |
| build | `$.outputs[0].sha256` | modified | "6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14" | "557f3559673678ba0b761ebc19a846b15e96e255f03280f66612ac91ce1ac0f5" |
| build | `$.outputs[0].size` | modified | 136670 | 141063 |
| build | `$.outputs[1].sha256` | modified | "26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c" | "54077126ff095cbcc3abb28c77cb1c0f0cd74fcca3d970dec770c232a10a9f51" |
| build | `$.outputs[1].size` | modified | 567230 | 567269 |
| build | `$.outputs[2].sha256` | modified | "9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da" | "40d77763be1abee9fb213c4dd6ea7c745c5d737f0114985dfcd2fd215bf884d9" |
| build | `$.outputs[2].size` | modified | 145016 | 149409 |
| build | `$.outputs[3].sha256` | modified | "33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d" | "383b4a5de46fa277a6044f8858abf9c06b1ecb7bdd17c4638177ab87e63a97e4" |
| build | `$.outputs[3].size` | modified | 684752 | 689653 |
| build | `$.qa.dom.matchedSolutionSlotCount` | added | — | 60 |
| build | `$.qa.visualSamples[2]` | modified | "qa/samples/student-p04.png" | "qa/samples/student-p03.png" |
| build | `$.qa.visualSamples[3]` | modified | "qa/samples/student-p06.png" | "qa/samples/student-p04.png" |
| build | `$.qa.visualSamples[4]` | modified | "qa/samples/student-p07.png" | "qa/samples/student-p05.png" |
| build | `$.qa.visualSamples[5]` | modified | "qa/samples/student-p08.png" | "qa/samples/student-p06.png" |
| build | `$.qa.visualSamples[6]` | modified | "qa/samples/student-p09.png" | "qa/samples/student-p07.png" |
| build | `$.qa.visualSamples[7]` | modified | "qa/samples/student-p10.png" | "qa/samples/student-p08.png" |
| build | `$.qa.visualSamples[8]` | modified | "qa/samples/answer-p01.png" | "qa/samples/student-p09.png" |
| build | `$.qa.visualSamples[9]` | modified | "qa/samples/answer-p02.png" | "qa/samples/student-p10.png" |
| build | `$.qa.visualSamples[10]` | modified | "qa/samples/answer-p04.png" | "qa/samples/answer-p01.png" |
| build | `$.qa.visualSamples[11]` | modified | "qa/samples/answer-p06.png" | "qa/samples/answer-p02.png" |
| build | `$.qa.visualSamples[12]` | modified | "qa/samples/answer-p07.png" | "qa/samples/answer-p03.png" |
| build | `$.qa.visualSamples[13]` | modified | "qa/samples/answer-p08.png" | "qa/samples/answer-p04.png" |
| build | `$.qa.visualSamples[14]` | modified | "qa/samples/answer-p09.png" | "qa/samples/answer-p05.png" |
| build | `$.qa.visualSamples[15]` | modified | "qa/samples/answer-p10.png" | "qa/samples/answer-p06.png" |
| build | `$.qa.visualSamples[16]` | added | — | "qa/samples/answer-p07.png" |
| build | `$.qa.visualSamples[17]` | added | — | "qa/samples/answer-p08.png" |
| build | `$.qa.visualSamples[18]` | added | — | "qa/samples/answer-p09.png" |
| build | `$.qa.visualSamples[19]` | added | — | "qa/samples/answer-p10.png" |
| build | `$.specVersion` | modified | "1.0.5" | "1.0.6" |
| build | `$.templateVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·10단계를 확인했습니다. 해설 문항의 박스·여백·가로 폭과 줄바꿈 공간을 유지하고 답 글자만 제거했으며, 별도 작성선·잘림·겹침·정답 노출·비정상 빨강이 없습… | "학생용·해설용 전체 10단계 contact sheet와 2·3·4·5·6·7·8·9·10단계를 확인했습니다. 문장 속 빈칸 60개와 작성형 18개의 위치·가로·세로가 일치하며, 해설의 검정 문제 단서와 빨간 답을… |
| build | `$.visualReview.reviewedAt` | modified | "2026-08-26T23:10:26+09:00" | "2026-08-26T23:23:15+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | 없음 |

### 페이지

변경 없음

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"6be9db495bcaf1379dacf51bde6277390fe131f3a1a66915e7ff4f7981fd9f14","size":136670} | {"path":"문제.html","sha256":"557f3559673678ba0b761ebc19a846b15e96e255f03280f66612ac91ce1ac0f5","size":141063} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"26d6579ad8d758306af3d60a0b99343d0459588be30c979f3fb6755018bf1c3c","size":567230} | {"path":"문제.pdf","sha256":"54077126ff095cbcc3abb28c77cb1c0f0cd74fcca3d970dec770c232a10a9f51","size":567269} |
| `해설.html` | modified | {"path":"해설.html","sha256":"9ef7b0585995fcd237115ea48852b631c769113cec425c48fbeb25d6da5d74da","size":145016} | {"path":"해설.html","sha256":"40d77763be1abee9fb213c4dd6ea7c745c5d737f0114985dfcd2fd215bf884d9","size":149409} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"33817fbe6ba45908366a1372a17225fc1f7e2095ea435174cc0bfc7b8d4afe5d","size":684752} | {"path":"해설.pdf","sha256":"383b4a5de46fa277a6044f8858abf9c06b1ecb7bdd17c4638177ab87e63a97e4","size":689653} |

## 영향 없음

- 동일한 manifest 구성 요소: 없음
- 직접·파생 변경이 기록되지 않은 단계: 1
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| all-solution-slot-geometry | pass | 브라우저 QA가 모든 비작성형 정답 자리의 페이지 기준 left/top/width/height를 문제본·해설본 사이에서 0.75px 허용치로 비교합니다. |
| intermediate-cleanup | pass | 측정용 HTML과 브라우저 프로필은 prepare 중 제거하고 캐시·중복 미리보기 파일은 공개 산출물과 무관한 범위에서 정리합니다. |
| student-answer-removal | pass | 문제본 payload와 DOM의 정답 값은 0개이며, 해설에서 측정한 형상 정보만 유지합니다. |
| writing-response-geometry | pass | 작성형 답안 박스와 답 줄별 위치·가로·세로 비교를 유지합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.3 | 1.0.4 |
| spec | 1.0.5 | 1.0.6 |
| template | 1.0.3 | 1.0.4 |
| build | 1.0.3 | 1.0.4 |

## 변경 통계

- 직접 JSON 경로: 89
- 파생 JSON 경로: 0
- 변경·선언 파일: 22
- 영향 페이지: 0
- 변경 출력: 4
