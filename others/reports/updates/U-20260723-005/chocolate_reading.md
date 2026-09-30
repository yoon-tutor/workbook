# 업데이트 보고서 `U-20260723-005`: 같은 단계 페이지 균등 압축 및 단독 꼬리 페이지 금지

## 요약

같은 단계의 문항을 안전 상한 안에서 최소 페이지 수로 균등 분배하고, 마지막 페이지에 한 문항만 남는 불필요한 단독 페이지를 차단합니다.

## 업데이트 정보

| 항목 | 값 |
|---|---|
| ID | `U-20260723-005` |
| 날짜 | 2026-07-23 |
| 분류 | `pagination` |
| 적용 범위 | `all` — 전체 워크북 |

## 요청 내용

- 같은 영역의 작업은 가능한 한 적은 페이지에 담고, 앞 페이지에 여백이 있는데 마지막 한 문항만 다음 페이지로 넘어가지 않게 수정합니다.

## manifest 비교

| 구성 요소 | 이전 버전 | 이후 버전 | 이전 digest | 이후 digest | 결과 |
|---|---:|---:|---|---|---|
| canonical | 1.0.1 | 1.0.2 | `06497a994d84` | `a5d9da78703b` | 변경 |
| spec | 1.0.1 | 1.0.2 | `729f1700e7c8` | `a28c254c251d` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.1 | 1.0.2 | `b6018803e60d` | `5815476d0491` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c","s… | {"sha256":"3ada1095d793e008258ade59bdf9ecc060cd1a52bc56206e8113d06b5c32fdfa","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba","s… | {"sha256":"72f2c6bdfe57c6f349c17db8a24d9fbbc72cd52c33b02c90b451d3735122ed9e","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840","s… | {"sha256":"3e95160ce4554b2d1036a9c4d4ae466b15fd077afeabce92190c0391417780f2","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98","s… | {"sha256":"9cf73ff750a1044d9bc90f5cdb6f692eaa2ce1251359612f83cecc362243ac10","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… |
| 직접 | build | `workbook_engine/paginator.py` | modified | {"sha256":"241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d","s… | {"sha256":"21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00","s… |
| 직접 | build | `workbook_engine/validator.py` | modified | {"sha256":"41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee","s… | {"sha256":"9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1","s… |
| 직접 | canonical | `workbooks/chocolate/content.json` | modified | {"sha256":"e9bf81a89dc2d26a34d71668ca8f104f3de75a3cc0e2fb8f7907568d14e7409b","s… | {"sha256":"a147ec241f586856efe14396e36d31ccf97079e04500a041d64169382a7ad1a6","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_paginator.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-005.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
| 직접 | declared | `workbooks/when-failure-become-ideas/content.json` | declared | — | — |
| 직접 | spec | `config/versions.json` | modified | {"sha256":"32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64","s… | {"sha256":"68c5be414e2274e8f909970294dec45572a47094871fc8b31a066b08710304c0","s… |
| 직접 | spec | `config/workbook-spec.json` | modified | {"sha256":"f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172","s… | {"sha256":"8bea1dedad1775ad890f36a07ca0f4e1cb2b031b94346edfe3593b6a04f83b7d","s… |

## 직접 변경

### JSON 경로

| manifest | JSON 경로 | 변경 | 이전 | 이후 |
|---|---|---|---|---|
| canonical | `$.canonical.contentVersion` | modified | "1.0.1" | "1.0.2" |
| canonical | `$.canonical.specVersion` | modified | "1.0.1" | "1.0.2" |
| canonical | `$.canonical.updateState.appliedUpdates[2]` | added | — | {"appliedAt":"2026-07-23T23:25:00+09:00","fromContentVersion":"1.0.1","id":"U-20260723-005","report":"reports/updates/U… |
| canonical | `$.contentVersion` | modified | "1.0.1" | "1.0.2" |
| canonical | `$.files[0].sha256` | modified | "e9bf81a89dc2d26a34d71668ca8f104f3de75a3cc0e2fb8f7907568d14e7409b" | "a147ec241f586856efe14396e36d31ccf97079e04500a041d64169382a7ad1a6" |
| canonical | `$.files[0].size` | modified | 125233 | 125486 |
| spec | `$.files[0].sha256` | modified | "32a9003aa543f3b26c3fb9b7673ddf15e537da9c00a5ebe4060142d2d415bf64" | "68c5be414e2274e8f909970294dec45572a47094871fc8b31a066b08710304c0" |
| spec | `$.files[0].size` | modified | 1289 | 1326 |
| spec | `$.files[1].sha256` | modified | "f73abcb9483482b27045737ce08ad1a84efa294f64f9fae9fef802fab207d172" | "8bea1dedad1775ad890f36a07ca0f4e1cb2b031b94346edfe3593b6a04f83b7d" |
| spec | `$.files[1].size` | modified | 15784 | 16122 |
| spec | `$.spec.logicalStages[3].pagination.hardMaximum` | modified | 10 | 11 |
| spec | `$.spec.paginationContract.continuationPageMinimumItems` | added | — | 2 |
| spec | `$.spec.paginationContract.forbidden[5]` | modified | "renumbering a new part from one" | "a singleton continuation page that can be avoided within the stage hard maximum" |
| spec | `$.spec.paginationContract.forbidden[6]` | added | — | "renumbering a new part from one" |
| spec | `$.spec.paginationContract.packingStrategy` | added | — | "fewest-pages-balanced-within-hard-maximum" |
| spec | `$.spec.paginationContract.singletonTailPage` | added | — | "forbidden-when-the-stage-has-multiple-items" |
| spec | `$.spec.paginationContract.underfilledTailAction` | added | — | "rebalance-all-pages-of-the-same-stage" |
| spec | `$.spec.specVersion` | modified | "1.0.1" | "1.0.2" |
| spec | `$.specVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.appliedUpdates[2]` | added | — | "U-20260723-005" |
| build | `$.buildVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.builtAt` | modified | "2026-07-23T23:18:05+09:00" | "2026-07-23T23:27:00+09:00" |
| build | `$.canonicalDigest` | modified | "d00b93b4982db9a43670c8be9ac6b53376d6f310c2321267291a0fb6efd03c82" | "556a6335e436d1031b8085efa363cc466771a2080642517e03ed4c4c018c84b9" |
| build | `$.compilerVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.contentVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.engineDigest` | modified | "0e9ef363eb9d5cfdf00794efcdedb7481cce218b5c043f069078a8d991ace578" | "b51bb9b758b4a296e3e5fa03c8af783a3626209e4cb1ee0cd519a6394e903d40" |
| build | `$.engineInputs[0].sha256` | modified | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" | "51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c" |
| build | `$.engineInputs[6].sha256` | modified | "241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d" | "21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00" |
| build | `$.engineInputs[6].size` | modified | 2122 | 3394 |
| build | `$.engineInputs[12].sha256` | modified | "41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee" | "9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1" |
| build | `$.engineInputs[12].size` | modified | 25980 | 26644 |
| build | `$.files[0].sha256` | modified | "1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155" | "51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c" |
| build | `$.files[6].sha256` | modified | "241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d" | "21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00" |
| build | `$.files[6].size` | modified | 2122 | 3394 |
| build | `$.files[12].sha256` | modified | "41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee" | "9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1" |
| build | `$.files[12].size` | modified | 25980 | 26644 |
| build | `$.files[13].sha256` | modified | "4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c" | "3ada1095d793e008258ade59bdf9ecc060cd1a52bc56206e8113d06b5c32fdfa" |
| build | `$.files[13].size` | modified | 190281 | 190692 |
| build | `$.files[14].sha256` | modified | "9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba" | "72f2c6bdfe57c6f349c17db8a24d9fbbc72cd52c33b02c90b451d3735122ed9e" |
| build | `$.files[14].size` | modified | 919425 | 919521 |
| build | `$.files[15].sha256` | modified | "77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840" | "3e95160ce4554b2d1036a9c4d4ae466b15fd077afeabce92190c0391417780f2" |
| build | `$.files[15].size` | modified | 211771 | 212182 |
| build | `$.files[16].sha256` | modified | "8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98" | "9cf73ff750a1044d9bc90f5cdb6f692eaa2ce1251359612f83cecc362243ac10" |
| build | `$.files[16].size` | modified | 1112757 | 1113005 |
| build | `$.outputs[0].sha256` | modified | "4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c" | "3ada1095d793e008258ade59bdf9ecc060cd1a52bc56206e8113d06b5c32fdfa" |
| build | `$.outputs[0].size` | modified | 190281 | 190692 |
| build | `$.outputs[1].sha256` | modified | "9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba" | "72f2c6bdfe57c6f349c17db8a24d9fbbc72cd52c33b02c90b451d3735122ed9e" |
| build | `$.outputs[1].size` | modified | 919425 | 919521 |
| build | `$.outputs[2].sha256` | modified | "77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840" | "3e95160ce4554b2d1036a9c4d4ae466b15fd077afeabce92190c0391417780f2" |
| build | `$.outputs[2].size` | modified | 211771 | 212182 |
| build | `$.outputs[3].sha256` | modified | "8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98" | "9cf73ff750a1044d9bc90f5cdb6f692eaa2ce1251359612f83cecc362243ac10" |
| build | `$.outputs[3].size` | modified | 1112757 | 1113005 |
| build | `$.pages[0].digest` | modified | "c60c6512a2318a3fbe7680443fddaeb02ebc4d9f6f593d9247fef8a5f749246a" | "04b9504fead80c9956745793ac8b470162606ab1cea040c36dd092932b9d8d49" |
| build | `$.pages[1].digest` | modified | "165c3f95712bbb26694065d6185184dad087821329b49bfae428a50b0a00b9d6" | "4835c94bec0bba5a75a0e6a1d9755aa1b4533f1d28082ebf1442aab29dfc97b0" |
| build | `$.pages[2].digest` | modified | "fd02c99ec586c4819a0979ecc07b49970bdc4a46d5732d15d500be68ae71ca66" | "92a6b5d0297cd991d1a5370e172a32b2fe3530ac3c67a38c4eacc4c5bca29be5" |
| build | `$.pages[2].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[2].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[2].part` | modified | "1-14" | "1-12" |
| build | `$.pages[3].digest` | modified | "92b7118f176007390727514f995a7357ad7f0cc8bc63a2e00d8ef27f075bc7b6" | "b3d798982572fa1319253dadf87641440aa8a671832296ad8cd37344ccd28c48" |
| build | `$.pages[3].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[3].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[3].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[3].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[3].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[3].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[3].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[3].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[3].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[3].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[3].itemIds[10]` | added | — | "s023" |
| build | `$.pages[3].itemIds[11]` | added | — | "s024" |
| build | `$.pages[3].part` | modified | "15-24" | "13-24" |
| build | `$.pages[4].digest` | modified | "a880901d7f982bcc080db91acf966d3840ff8993d3a5b39071bcb8d95c6d1fda" | "e7b4ad6872c9f6b64f1d0ea6f72e5f64da09638538f4546ba5c26c65d8302af0" |
| build | `$.pages[4].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[4].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[4].part` | modified | "1-14" | "1-12" |
| build | `$.pages[5].digest` | modified | "e9338527f478b96e9147e0c3262451ccc171b53400de58be8ad2d9b5e248cd93" | "806889155e1a249ea966e45d667cf6b0779840129f081e48a43ebd0eeeed9a8c" |
| build | `$.pages[5].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[5].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[5].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[5].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[5].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[5].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[5].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[5].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[5].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[5].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[5].itemIds[10]` | added | — | "s023" |
| build | `$.pages[5].itemIds[11]` | added | — | "s024" |
| build | `$.pages[5].part` | modified | "15-24" | "13-24" |
| build | `$.pages[6].digest` | modified | "4a28f0720c95fc0a1ac1a9ba814e1280eb6fbc338324053de0526e9297be8c5c" | "496e7719334180669cab5b81d0abb79001cb34c9b2a2d76c5759a885192102eb" |
| build | `$.pages[6].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[6].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[6].part` | modified | "1-10" | "1-8" |
| build | `$.pages[7].digest` | modified | "2a4ff2311ecc1ac6bfddb14c1c340c78088c1863efc980b9c0b8e35b987b5cd3" | "57a167cd0542342a00824c5926eb3f3d8f97db71cc2718f687da78c668fb98c3" |
| build | `$.pages[7].itemIds[0]` | modified | "s011" | "s009" |
| build | `$.pages[7].itemIds[1]` | modified | "s012" | "s010" |
| build | `$.pages[7].itemIds[2]` | modified | "s013" | "s011" |
| build | `$.pages[7].itemIds[3]` | modified | "s014" | "s012" |
| build | `$.pages[7].itemIds[4]` | modified | "s015" | "s013" |
| build | `$.pages[7].itemIds[5]` | modified | "s016" | "s014" |
| build | `$.pages[7].itemIds[6]` | modified | "s017" | "s015" |
| build | `$.pages[7].itemIds[7]` | modified | "s018" | "s016" |
| build | `$.pages[7].itemIds[8]` | removed | "s019" | — |
| build | `$.pages[7].itemIds[9]` | removed | "s020" | — |
| build | `$.pages[7].part` | modified | "11-20" | "9-16" |
| build | `$.pages[8].digest` | modified | "58fe3041a057ec3741967a09d421a9a86379ec60641aa7fef32751f1e7eed0da" | "d11894ad31f675e97549e722bffaba4d7206b0ac852a64a026b455072bf00e1f" |
| build | `$.pages[8].itemIds[0]` | modified | "s021" | "s017" |
| build | `$.pages[8].itemIds[1]` | modified | "s022" | "s018" |
| build | `$.pages[8].itemIds[2]` | modified | "s023" | "s019" |
| build | `$.pages[8].itemIds[3]` | modified | "s024" | "s020" |
| build | `$.pages[8].itemIds[4]` | added | — | "s021" |
| build | `$.pages[8].itemIds[5]` | added | — | "s022" |
| build | `$.pages[8].itemIds[6]` | added | — | "s023" |
| build | `$.pages[8].itemIds[7]` | added | — | "s024" |
| build | `$.pages[8].part` | modified | "21-24" | "17-24" |
| build | `$.pages[9].digest` | modified | "97d93b4ccfc6266250004d264fdea8ffee8743524a150ac853b6d9d1b88f0f6a" | "ae2e91b729fb2b5fdc60e83ba7694246036e0f97e29170d4809196b1923986f2" |
| build | `$.pages[9].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[9].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[9].part` | modified | "1-14" | "1-12" |
| build | `$.pages[10].digest` | modified | "a4e211086cf79dd6bf7c71898fb03407183bc5f6b7440d2c101a901387c0dac3" | "4df26658fca748c6dff4833b7bbd9992e3cdf8a7764af78342b3bd0c78d981c4" |
| build | `$.pages[10].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[10].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[10].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[10].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[10].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[10].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[10].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[10].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[10].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[10].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[10].itemIds[10]` | added | — | "s023" |
| build | `$.pages[10].itemIds[11]` | added | — | "s024" |
| build | `$.pages[10].part` | modified | "15-24" | "13-24" |
| build | `$.pages[11].digest` | modified | "4b2ed1476eb7e1dd96617226614b1121aa14e8f61bca9b06af3ca6cf76d4e1d0" | "4dceedfc1fcbbf02ece0f8c31873858e973e5d5eed2a685506781d585499c262" |
| build | `$.pages[11].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[11].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[11].part` | modified | "1-14" | "1-12" |
| build | `$.pages[12].digest` | modified | "767978d2a078653675c1313045a90533d9385cd67f0bfbe993ee01a9dfc8978e" | "9153fe1f2991ab74ef85fddaffd2833169a10448283fdd07699318c607c68839" |
| build | `$.pages[12].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[12].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[12].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[12].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[12].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[12].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[12].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[12].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[12].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[12].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[12].itemIds[10]` | added | — | "s023" |
| build | `$.pages[12].itemIds[11]` | added | — | "s024" |
| build | `$.pages[12].part` | modified | "15-24" | "13-24" |
| build | `$.pages[14].digest` | modified | "c28f729f0212e4e77fa5a9706ec76d3e1c4a179d2c1cda90821d766b70dcc95b" | "9490dca3c12d2fd26664245063c0d6d09b0143a1eb41722768c8b2b8b8a20e0c" |
| build | `$.pages[15].digest` | modified | "a8b6edca6086fa674347397486db514e062089a856889d899edac7790566329f" | "fe2e29d5b841be2f4090dfcf33a27d1e96bf2698294b080b7525b7fe4df7d557" |
| build | `$.pages[16].digest` | modified | "41ef253aa7fdee1f2e880f217da366925d45e9e347245191059420e9ea5ed5b5" | "978e1bcd586422597944a9bd7e27ad7f771f216105246bf32305c1a045edcc82" |
| build | `$.pages[17].digest` | modified | "1bace8b1ef97dbd173a846bc2ed4be6cde06102c62b6a62cf7705fe1aeaaac9e" | "85095e6c080a2dfda37e54a1e357d2472488bcc7875831687105e90e194bd499" |
| build | `$.pages[19].digest` | modified | "3cc8686d3e5d0ef3aa5a96d1c0485ba1bc8663366f53e358ffa662af156000cc" | "193a6869ba5db696e2e4bfe099639adac26a9506a47cd12b777508c0c4a11726" |
| build | `$.pages[20].digest` | modified | "502e88a4f87c1f028b822d97b9b08945c4bc1f0f176de7d78b94ff9a54087087" | "8c506f5386ec9044dad73837ec9504b3ff757ed83c034527e355c3adb9b1e01f" |
| build | `$.pages[21].digest` | modified | "2e7447e9292926148737e25a3fc0c475bebe4bd9ec4af1ef5ca201a6f9a27047" | "a2b25a7250de23d680bbd036b2f49eb9e4d5ff4cc4def0e0003aee3fd937c5cb" |
| build | `$.pages[22].digest` | modified | "c60c6512a2318a3fbe7680443fddaeb02ebc4d9f6f593d9247fef8a5f749246a" | "04b9504fead80c9956745793ac8b470162606ab1cea040c36dd092932b9d8d49" |
| build | `$.pages[23].digest` | modified | "165c3f95712bbb26694065d6185184dad087821329b49bfae428a50b0a00b9d6" | "4835c94bec0bba5a75a0e6a1d9755aa1b4533f1d28082ebf1442aab29dfc97b0" |
| build | `$.pages[24].digest` | modified | "1794f532a3ac42d62e66f2e53742d042c6c36384f91c494fb3de0b3ec56551f9" | "c9f0a6be8e4192b9cb2bd7670c0eec785676e02d1e85d2f3db7e5462457fb3eb" |
| build | `$.pages[24].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[24].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[24].part` | modified | "1-14" | "1-12" |
| build | `$.pages[25].digest` | modified | "df3e417c0327be8824e4c9759dcd6263b72d682596892de98b1dc938546c1549" | "3df67b78d5e55876d82cfbd35bc29592d7065c36e9b98ff13dd51b2d2afff49b" |
| build | `$.pages[25].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[25].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[25].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[25].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[25].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[25].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[25].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[25].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[25].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[25].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[25].itemIds[10]` | added | — | "s023" |
| build | `$.pages[25].itemIds[11]` | added | — | "s024" |
| build | `$.pages[25].part` | modified | "15-24" | "13-24" |
| build | `$.pages[26].digest` | modified | "3b4f520192effb0d9024fd1e49a48efdfb696cdd838007baca6a4a5d957516d5" | "bc8a268ff7c759ea28403d7cd9ea476897f010b7f9130c75c37f263e496eb672" |
| build | `$.pages[26].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[26].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[26].part` | modified | "1-14" | "1-12" |
| build | `$.pages[27].digest` | modified | "97794054bffcdfe11913f2db61470b74732fa8d4f3e74b6beda59ec85fb59b46" | "11de5682f910c2e5b8f3ee6489559d5924e97d969c5db398f5c219a168701ea0" |
| build | `$.pages[27].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[27].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[27].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[27].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[27].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[27].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[27].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[27].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[27].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[27].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[27].itemIds[10]` | added | — | "s023" |
| build | `$.pages[27].itemIds[11]` | added | — | "s024" |
| build | `$.pages[27].part` | modified | "15-24" | "13-24" |
| build | `$.pages[28].digest` | modified | "86e05b6f644115f28ad6145e25c77ce8b3d64ad6164e4c9066cf1e28f4f2a161" | "db6be0131592fe1fec179e31987bb8668e15d948441fffdafc0768168811857f" |
| build | `$.pages[28].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[28].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[28].part` | modified | "1-10" | "1-8" |
| build | `$.pages[29].digest` | modified | "947aab35c772e8bc6c50f95958278b5b09182dedcb374c5a7e4e16f72742fef2" | "7cc44cb1e4be3ca4f2c0f1b50aada7935a4af02471ecb95c42c78c8135c65e05" |
| build | `$.pages[29].itemIds[0]` | modified | "s011" | "s009" |
| build | `$.pages[29].itemIds[1]` | modified | "s012" | "s010" |
| build | `$.pages[29].itemIds[2]` | modified | "s013" | "s011" |
| build | `$.pages[29].itemIds[3]` | modified | "s014" | "s012" |
| build | `$.pages[29].itemIds[4]` | modified | "s015" | "s013" |
| build | `$.pages[29].itemIds[5]` | modified | "s016" | "s014" |
| build | `$.pages[29].itemIds[6]` | modified | "s017" | "s015" |
| build | `$.pages[29].itemIds[7]` | modified | "s018" | "s016" |
| build | `$.pages[29].itemIds[8]` | removed | "s019" | — |
| build | `$.pages[29].itemIds[9]` | removed | "s020" | — |
| build | `$.pages[29].part` | modified | "11-20" | "9-16" |
| build | `$.pages[30].digest` | modified | "6c68c225387765bb6323819a2585267e33e462865a9d05cdd260ec5cebbb607e" | "dd69434cb57a53e16fa5f453492ed8a085e8240d74a40ae2946268d3ee62b7cc" |
| build | `$.pages[30].itemIds[0]` | modified | "s021" | "s017" |
| build | `$.pages[30].itemIds[1]` | modified | "s022" | "s018" |
| build | `$.pages[30].itemIds[2]` | modified | "s023" | "s019" |
| build | `$.pages[30].itemIds[3]` | modified | "s024" | "s020" |
| build | `$.pages[30].itemIds[4]` | added | — | "s021" |
| build | `$.pages[30].itemIds[5]` | added | — | "s022" |
| build | `$.pages[30].itemIds[6]` | added | — | "s023" |
| build | `$.pages[30].itemIds[7]` | added | — | "s024" |
| build | `$.pages[30].part` | modified | "21-24" | "17-24" |
| build | `$.pages[31].digest` | modified | "f4a59bd99ce12a7474705ea5adb93f400e30e22b44876962201a3b58b4147b32" | "fbba05fb693413e381a1589222aac01977dc222dc839aae53e6b8347742b0f4c" |
| build | `$.pages[31].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[31].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[31].part` | modified | "1-14" | "1-12" |
| build | `$.pages[32].digest` | modified | "d0c2d1d4fb9d11ba4d23b6f52d08b9cb18c25851df905dedeef76c80810317a5" | "65c1b63d309d41b3e5538e90a0434e6fe02e85627d074eefc793c9093c97965b" |
| build | `$.pages[32].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[32].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[32].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[32].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[32].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[32].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[32].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[32].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[32].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[32].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[32].itemIds[10]` | added | — | "s023" |
| build | `$.pages[32].itemIds[11]` | added | — | "s024" |
| build | `$.pages[32].part` | modified | "15-24" | "13-24" |
| build | `$.pages[33].digest` | modified | "dc585f4ca31db8a5ae3f047dc56a60e00526be28364db984520695f479aaf5bf" | "54cc252687edd72894d82f7a0db4b9dc7cf9379111bc9c07fafced89b5d493d6" |
| build | `$.pages[33].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[33].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[33].part` | modified | "1-14" | "1-12" |
| build | `$.pages[34].digest` | modified | "0691e4090fc61c1d857036130aa870d0d5d47f2330c5ac50bec6ce213d76ef46" | "6e45b62a46f1b322917e65302715b8ffabb9025ab515889d5c04c1fdc79d0bcc" |
| build | `$.pages[34].itemIds[0]` | modified | "s015" | "s013" |
| build | `$.pages[34].itemIds[1]` | modified | "s016" | "s014" |
| build | `$.pages[34].itemIds[2]` | modified | "s017" | "s015" |
| build | `$.pages[34].itemIds[3]` | modified | "s018" | "s016" |
| build | `$.pages[34].itemIds[4]` | modified | "s019" | "s017" |
| build | `$.pages[34].itemIds[5]` | modified | "s020" | "s018" |
| build | `$.pages[34].itemIds[6]` | modified | "s021" | "s019" |
| build | `$.pages[34].itemIds[7]` | modified | "s022" | "s020" |
| build | `$.pages[34].itemIds[8]` | modified | "s023" | "s021" |
| build | `$.pages[34].itemIds[9]` | modified | "s024" | "s022" |
| build | `$.pages[34].itemIds[10]` | added | — | "s023" |
| build | `$.pages[34].itemIds[11]` | added | — | "s024" |
| build | `$.pages[34].part` | modified | "15-24" | "13-24" |
| build | `$.pages[36].digest` | modified | "225c0793141c49943632bf5f182c0fd9f991a457808203ace13b12d2b1c382c5" | "a489d50da76fa6056f7090b019846b837cd4a5feca0d147a63350ac7a69c6855" |
| build | `$.pages[37].digest` | modified | "9dba0aac32339830a40578c6c52808a23fb714918a91673f749b1d3394b88384" | "d77fade76ddbfb30f8c946a50a8f89f24e99e47ff5719e03b84886bf83899745" |
| build | `$.pages[38].digest` | modified | "ea2659ac5d6a252d93a07e3568a03ed2d9a5aeac1938aff5a3e8b7f9dac4393c" | "5ce2b7cd1d5bfa99a43c973fe940df4b7dde11163ffe60f1763845f3870c36d0" |
| build | `$.pages[39].digest` | modified | "1256c647872170ec261f67fd6b1b8a6490d03b54dabae9591ecf20eaa2aea6ca" | "17f696ef4728e18b87a3135eac9d1179684a566a75bc10b962d702935a478c8b" |
| build | `$.pages[41].digest` | modified | "dcce10ab9907f908ef9e505c274792bcf709c2f5bbcf89638efbbd749da89e78" | "20df61082c21804df27f2b2301a704f23840a120e7224c0889f80922e7bbf469" |
| build | `$.pages[42].digest` | modified | "e679a9ef1d482b675351971f8ecb958a9253eafaf8e72650351b2ad624493ee1" | "98be534b986bd80ff1952c1435081090b620883ffc388aaff9b5e4fd91381531" |
| build | `$.pages[43].digest` | modified | "90dd0bd8a6a4ab8911b285375c632df56975b232750e5986b4403a2fa7c1c72e" | "5c0403a92b3510eeaee502a5ff60838aa1baf5940bdd1d15875198cbafaaa9db" |
| build | `$.specVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 22쪽 contact sheet에서 1·2·7·12·14·15·19·20·22페이지를 확인함. 8단계 조각형 정답 밑줄이 제거되고 긴 작성선·완성 문장 해설만 유지됨. 잘림·겹침·번호 오류·학생용 … | "학생용·해설용 22쪽 contact sheet에서 4단계가 긴 문장 높이를 지키며 8/8/8로 균등 배치된 것을 확인함. 단독 꼬리 페이지, 잘림·겹침·번호 오류·학생용 정답 누출·교정 색상 오류 없음." |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-23T23:19:04+09:00" | "2026-07-23T23:28:04+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 8, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:chocolate-reading-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| answer:chocolate-reading-p02 | modified | 1 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p04 | modified | 2 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p05 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p06 | modified | 3 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p07 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| answer:chocolate-reading-p08 | modified | 4 | s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020 |
| answer:chocolate-reading-p09 | modified | 4 | s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p10 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p11 | modified | 5 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p12 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:chocolate-reading-p13 | modified | 6 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:chocolate-reading-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| answer:chocolate-reading-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| answer:chocolate-reading-p18 | modified | 8 | s019, s020, s021, s022, s023, s024 |
| answer:chocolate-reading-p20 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:chocolate-reading-p21 | modified | 10 | s009, s010, s011, s012, s013, s014, s015, s016 |
| answer:chocolate-reading-p22 | modified | 10 | s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| student:chocolate-reading-p02 | modified | 1 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p04 | modified | 2 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p05 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p06 | modified | 3 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p07 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| student:chocolate-reading-p08 | modified | 4 | s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020 |
| student:chocolate-reading-p09 | modified | 4 | s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p10 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p11 | modified | 5 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p12 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:chocolate-reading-p13 | modified | 6 | s013, s014, s015, s016, s017, s018, s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p15 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:chocolate-reading-p16 | modified | 8 | s007, s008, s009, s010, s011, s012 |
| student:chocolate-reading-p17 | modified | 8 | s013, s014, s015, s016, s017, s018 |
| student:chocolate-reading-p18 | modified | 8 | s019, s020, s021, s022, s023, s024 |
| student:chocolate-reading-p20 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:chocolate-reading-p21 | modified | 10 | s009, s010, s011, s012, s013, s014, s015, s016 |
| student:chocolate-reading-p22 | modified | 10 | s017, s018, s019, s020, s021, s022, s023, s024 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"4c6df18a7fc0654f3d6df598a3b076010c3d1ef964ff76e3acc24129041dbc6c","size":190281} | {"path":"문제.html","sha256":"3ada1095d793e008258ade59bdf9ecc060cd1a52bc56206e8113d06b5c32fdfa","size":190692} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"9181afb6958fc85c0fcecdce621dfa957bc8a6f6165ac7b15aad9bccfbb246ba","size":919425} | {"path":"문제.pdf","sha256":"72f2c6bdfe57c6f349c17db8a24d9fbbc72cd52c33b02c90b451d3735122ed9e","size":919521} |
| `해설.html` | modified | {"path":"해설.html","sha256":"77cd1f919e03aed23c7eb365858b4d0ffe0c85d9529323d76261d2545aefb840","size":211771} | {"path":"해설.html","sha256":"3e95160ce4554b2d1036a9c4d4ae466b15fd077afeabce92190c0391417780f2","size":212182} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"8cbcfe2ffa51878d92a94d2fc475dd3058ec5cb35eee48c593ccb0f5e8112d98","size":1112757} | {"path":"해설.pdf","sha256":"9cf73ff750a1044d9bc90f5cdb6f692eaa2ce1251359612f83cecc362243ac10","size":1113005} |

## 영향 없음

- 동일한 manifest 구성 요소: `template`
- 직접·파생 변경이 기록되지 않은 단계: 7, 9
- 원문 문장과 학생용·해설용 공통 문제 구조는 별도 검증 결과가 실패하지 않는 한 유지됩니다.

## 검증 결과

| 검사 | 결과 | 설명 |
|---|---|---|
| balanced-pagination | pass | 21개 문항과 안전 상한 11에서 11/10으로 나뉘며, 13개 문항도 7/6으로 분배되어 단독 꼬리 페이지가 생기지 않는 회귀 검사를 추가했습니다. |
| compiled-singleton-tail-gate | pass | 문장 단계의 마지막 페이지가 한 문항이거나 같은 단계 페이지 간 문항 수 차이가 1을 넘으면 validation을 실패시킵니다. |
| release-validation | skipped | 전체 테스트와 새 비공개 렌더에서 확인합니다. |

## 호환성

- 적용 범위: `all` — 전체 워크북
- 학생용과 해설용은 동일한 단계·문항·정답 슬롯 계약을 사용합니다.
- 이전 정본과의 차이는 위 직접 변경 및 파생 변경 표에 기록된 범위로 제한됩니다.

## 버전

| 구성 요소 | 이전 | 이후 |
|---|---:|---:|
| canonical | 1.0.1 | 1.0.2 |
| spec | 1.0.1 | 1.0.2 |
| template | 1.0.1 | 1.0.1 |
| build | 1.0.1 | 1.0.2 |

## 변경 통계

- 직접 JSON 경로: 269
- 파생 JSON 경로: 0
- 변경·선언 파일: 17
- 영향 페이지: 40
- 변경 출력: 4
