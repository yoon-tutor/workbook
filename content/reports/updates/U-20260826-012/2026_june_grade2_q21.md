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
| canonical | 1.0.3 | 1.0.4 | `91edca503ed7` | `97c11ea0561f` | 변경 |
| spec | 1.0.5 | 1.0.6 | `5d51719ab734` | `99c2f3e65fe1` | 변경 |
| template | 1.0.3 | 1.0.4 | `bf9fbd837d50` | `248f772c4818` | 변경 |
| build | 1.0.3 | 1.0.4 | `153cd4208dc6` | `558ac9ec7117` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723","s… | {"sha256":"0346a24588f2a4e59e74c19bc7d117421175a29fc823c3f7c6f647751eb182df","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e","s… | {"sha256":"6c74c994af3e70ae14d316b63b634caceb88be3e6ec4aec71a2f568336674680","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630","s… | {"sha256":"30f0a56dfabea28ef6ec9eae74f283f29bd7ea9b18f53c2ccae87033a324d45c","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f","s… | {"sha256":"71ad1fe6d3654c73fabb21ad731c48fe03831d8cdb20bc91c1523c76dada4360","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"c4bc0ec218daa7f0637118f679ace1780d082f073e2a60b3a04ed934d0fccda1","s… | {"sha256":"af1c6c8451bc16d5769b0dbe55225c9d66e68ed46b6cd64eea4ce5e2f7eb0edd","s… |
| 직접 | build | `workbook_engine/compiler.py` | modified | {"sha256":"7f89c515d46819a4d3f33d8a1de5c9ac598431c25d4c11c44482fe8f37d02f4e","s… | {"sha256":"30f60ef9ddb93dd7a8d3462a0fccb652ada4ae2d5703d5c2928ed6f7a65785b8","s… |
| 직접 | build | `workbook_engine/qa.py` | modified | {"sha256":"0f03ab7c8eaf635acf857e59919ef52a5e02f07bbf933f0f02f54a95b62fa604","s… | {"sha256":"24b628516d4feacd50a3bc7b18cafdd9d9c8d96246b33f69f9eeea8d327ba604","s… |
| 직접 | build | `workbook_engine/release.py` | modified | {"sha256":"592870a51ab14a45bfbab0063c7a704e9c9b853b80af014afbd777e8c2ee479f","s… | {"sha256":"097925500dc84f6a4bc13efab144343fcd4d6dbe1f1685fe1db5e87a7c90501e","s… |
| 직접 | canonical | `workbooks/2026-june-grade2-q21/content.json` | modified | {"sha256":"e53591a13c31eeec1be55b158eabc745ad7eb81c7809145a8c7d72245ae7dbdd","s… | {"sha256":"b655acff41939784374558be10ab3a2d9aa5a73b1d9ae7bfa9ab8eb46eb88af7","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `updates/U-20260826-012.json` | declared | — | — |
| 직접 | declared | `workbook_engine/templates/README.md` | declared | — | — |
| 직접 | declared | `workbooks/2026-june-grade2-q20/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "e53591a13c31eeec1be55b158eabc745ad7eb81c7809145a8c7d72245ae7dbdd" | "b655acff41939784374558be10ab3a2d9aa5a73b1d9ae7bfa9ab8eb46eb88af7" |
| canonical | `$.files[0].size` | modified | 29283 | 29536 |
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
| build | `$.builtAt` | modified | "2026-08-26T23:08:00+09:00" | "2026-08-26T23:22:06+09:00" |
| build | `$.canonicalDigest` | modified | "946a4348548bb03f3a12b33db72e3181cf111b0f86a9e518afd626b869b9bfbf" | "31e9db7e5c21b99607ab60d62a2a8cc1db8840a8802223f2dca772cee176ae68" |
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
| build | `$.files[13].sha256` | modified | "3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723" | "0346a24588f2a4e59e74c19bc7d117421175a29fc823c3f7c6f647751eb182df" |
| build | `$.files[13].size` | modified | 140643 | 145563 |
| build | `$.files[14].sha256` | modified | "6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e" | "6c74c994af3e70ae14d316b63b634caceb88be3e6ec4aec71a2f568336674680" |
| build | `$.files[14].size` | modified | 607245 | 607353 |
| build | `$.files[15].sha256` | modified | "a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630" | "30f0a56dfabea28ef6ec9eae74f283f29bd7ea9b18f53c2ccae87033a324d45c" |
| build | `$.files[15].size` | modified | 149785 | 154705 |
| build | `$.files[16].sha256` | modified | "9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f" | "71ad1fe6d3654c73fabb21ad731c48fe03831d8cdb20bc91c1523c76dada4360" |
| build | `$.files[16].size` | modified | 738231 | 743175 |
| build | `$.outputs[0].sha256` | modified | "3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723" | "0346a24588f2a4e59e74c19bc7d117421175a29fc823c3f7c6f647751eb182df" |
| build | `$.outputs[0].size` | modified | 140643 | 145563 |
| build | `$.outputs[1].sha256` | modified | "6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e" | "6c74c994af3e70ae14d316b63b634caceb88be3e6ec4aec71a2f568336674680" |
| build | `$.outputs[1].size` | modified | 607245 | 607353 |
| build | `$.outputs[2].sha256` | modified | "a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630" | "30f0a56dfabea28ef6ec9eae74f283f29bd7ea9b18f53c2ccae87033a324d45c" |
| build | `$.outputs[2].size` | modified | 149785 | 154705 |
| build | `$.outputs[3].sha256` | modified | "9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f" | "71ad1fe6d3654c73fabb21ad731c48fe03831d8cdb20bc91c1523c76dada4360" |
| build | `$.outputs[3].size` | modified | 738231 | 743175 |
| build | `$.qa.dom.matchedSolutionSlotCount` | added | — | 69 |
| build | `$.qa.visualSamples[2]` | modified | "qa/samples/student-p04.png" | "qa/samples/student-p03.png" |
| build | `$.qa.visualSamples[3]` | modified | "qa/samples/student-p06.png" | "qa/samples/student-p04.png" |
| build | `$.qa.visualSamples[4]` | modified | "qa/samples/student-p07.png" | "qa/samples/student-p05.png" |
| build | `$.qa.visualSamples[5]` | modified | "qa/samples/student-p08.png" | "qa/samples/student-p06.png" |
| build | `$.qa.visualSamples[6]` | modified | "qa/samples/student-p10.png" | "qa/samples/student-p07.png" |
| build | `$.qa.visualSamples[7]` | modified | "qa/samples/student-p11.png" | "qa/samples/student-p08.png" |
| build | `$.qa.visualSamples[8]` | modified | "qa/samples/answer-p01.png" | "qa/samples/student-p10.png" |
| build | `$.qa.visualSamples[9]` | modified | "qa/samples/answer-p02.png" | "qa/samples/student-p11.png" |
| build | `$.qa.visualSamples[10]` | modified | "qa/samples/answer-p04.png" | "qa/samples/answer-p01.png" |
| build | `$.qa.visualSamples[11]` | modified | "qa/samples/answer-p06.png" | "qa/samples/answer-p02.png" |
| build | `$.qa.visualSamples[12]` | modified | "qa/samples/answer-p07.png" | "qa/samples/answer-p03.png" |
| build | `$.qa.visualSamples[13]` | modified | "qa/samples/answer-p08.png" | "qa/samples/answer-p04.png" |
| build | `$.qa.visualSamples[14]` | modified | "qa/samples/answer-p10.png" | "qa/samples/answer-p05.png" |
| build | `$.qa.visualSamples[15]` | modified | "qa/samples/answer-p11.png" | "qa/samples/answer-p06.png" |
| build | `$.qa.visualSamples[16]` | added | — | "qa/samples/answer-p07.png" |
| build | `$.qa.visualSamples[17]` | added | — | "qa/samples/answer-p08.png" |
| build | `$.qa.visualSamples[18]` | added | — | "qa/samples/answer-p10.png" |
| build | `$.qa.visualSamples[19]` | added | — | "qa/samples/answer-p11.png" |
| build | `$.specVersion` | modified | "1.0.5" | "1.0.6" |
| build | `$.templateVersion` | modified | "1.0.3" | "1.0.4" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 4·8·11단계를 확인했습니다. 해설 문항의 박스·여백·가로 폭과 줄바꿈 공간을 유지하고 답 글자만 제거했으며, 별도 작성선·잘림·겹침·정답 노출·비정상 빨강이 없습… | "학생용·해설용 전체 10단계 contact sheet와 2·3·4·5·6·7·8·9·10단계를 확인했습니다. 문장 속 빈칸 69개와 작성형 24개의 위치·가로·세로가 일치하며, 해설의 검정 문제 단서와 빨간 답을… |
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
| `문제.html` | modified | {"path":"문제.html","sha256":"3e6699ffd8cb2c3eb9cf84997e2fa9c7b533d83710c40991bb38f80bed8a5723","size":140643} | {"path":"문제.html","sha256":"0346a24588f2a4e59e74c19bc7d117421175a29fc823c3f7c6f647751eb182df","size":145563} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"6ec963deb4a9c7497d7e5af7e443413cf92e5b9a56cc01f8eaa660757e52dd9e","size":607245} | {"path":"문제.pdf","sha256":"6c74c994af3e70ae14d316b63b634caceb88be3e6ec4aec71a2f568336674680","size":607353} |
| `해설.html` | modified | {"path":"해설.html","sha256":"a3f112cb9f62017713aeb5976540cb13f23a25c4fb65c38aa368283f42304630","size":149785} | {"path":"해설.html","sha256":"30f0a56dfabea28ef6ec9eae74f283f29bd7ea9b18f53c2ccae87033a324d45c","size":154705} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"9302418db0d4c3b884de8de9f884027279a01dc9e675b43150a0cfa0fd91c17f","size":738231} | {"path":"해설.pdf","sha256":"71ad1fe6d3654c73fabb21ad731c48fe03831d8cdb20bc91c1523c76dada4360","size":743175} |

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
