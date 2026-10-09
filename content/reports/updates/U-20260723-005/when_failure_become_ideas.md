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
| canonical | 1.0.1 | 1.0.2 | `ac15ce3442a8` | `72a894eb2dc9` | 변경 |
| spec | 1.0.1 | 1.0.2 | `729f1700e7c8` | `a28c254c251d` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.1 | 1.0.2 | `02c3585a3c19` | `b1c814e6c46d` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17","s… | {"sha256":"e3c5747aacbdbf15d6ee4deb28ad3274e6cb27dce9a658f3024fb095b88ab273","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861","s… | {"sha256":"69deb9513358e26541ddc62e2f6e7352b6fbe933a3423a1b40f0ecb8a5ca598e","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc","s… | {"sha256":"10ded181cd65064d7d60f155b9a9c7e024439fa05512ec3dd8245e9cc99b6ef3","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8","s… | {"sha256":"b76d86fc0ec1567b320ca59d18a2ee9819df156ea3489b323272c44a91860b91","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… |
| 직접 | build | `workbook_engine/paginator.py` | modified | {"sha256":"241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d","s… | {"sha256":"21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00","s… |
| 직접 | build | `workbook_engine/validator.py` | modified | {"sha256":"41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee","s… | {"sha256":"9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1","s… |
| 직접 | canonical | `workbooks/when-failure-become-ideas/content.json` | modified | {"sha256":"d5d55fe18a5989d480863288b392199b69a053c7d74db5c2d00acf34e530a1e6","s… | {"sha256":"de738e60b819aa103b69b97bf6d2119368f369d807b48535f568fcd5c31281a9","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_paginator.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-005.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
| 직접 | declared | `workbooks/soccer-jersey-swap/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "d5d55fe18a5989d480863288b392199b69a053c7d74db5c2d00acf34e530a1e6" | "de738e60b819aa103b69b97bf6d2119368f369d807b48535f568fcd5c31281a9" |
| canonical | `$.files[0].size` | modified | 38810 | 39063 |
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
| build | `$.builtAt` | modified | "2026-07-23T23:17:16+09:00" | "2026-07-23T23:25:47+09:00" |
| build | `$.canonicalDigest` | modified | "228227fa9bbf1b4b86a804ff38f57a62b5b2bbc3ab54cb6c40406ab67078d779" | "8591398902a244ca2f6519420aceefdb9247d0e9b290ea469c6164d99ed2a5bc" |
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
| build | `$.files[13].sha256` | modified | "37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17" | "e3c5747aacbdbf15d6ee4deb28ad3274e6cb27dce9a658f3024fb095b88ab273" |
| build | `$.files[13].size` | modified | 158301 | 158027 |
| build | `$.files[14].sha256` | modified | "2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861" | "69deb9513358e26541ddc62e2f6e7352b6fbe933a3423a1b40f0ecb8a5ca598e" |
| build | `$.files[14].size` | modified | 757943 | 755102 |
| build | `$.files[15].sha256` | modified | "8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc" | "10ded181cd65064d7d60f155b9a9c7e024439fa05512ec3dd8245e9cc99b6ef3" |
| build | `$.files[15].size` | modified | 170688 | 170414 |
| build | `$.files[16].sha256` | modified | "70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8" | "b76d86fc0ec1567b320ca59d18a2ee9819df156ea3489b323272c44a91860b91" |
| build | `$.files[16].size` | modified | 906987 | 903993 |
| build | `$.outputs[0].sha256` | modified | "37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17" | "e3c5747aacbdbf15d6ee4deb28ad3274e6cb27dce9a658f3024fb095b88ab273" |
| build | `$.outputs[0].size` | modified | 158301 | 158027 |
| build | `$.outputs[1].sha256` | modified | "2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861" | "69deb9513358e26541ddc62e2f6e7352b6fbe933a3423a1b40f0ecb8a5ca598e" |
| build | `$.outputs[1].size` | modified | 757943 | 755102 |
| build | `$.outputs[2].sha256` | modified | "8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc" | "10ded181cd65064d7d60f155b9a9c7e024439fa05512ec3dd8245e9cc99b6ef3" |
| build | `$.outputs[2].size` | modified | 170688 | 170414 |
| build | `$.outputs[3].sha256` | modified | "70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8" | "b76d86fc0ec1567b320ca59d18a2ee9819df156ea3489b323272c44a91860b91" |
| build | `$.outputs[3].size` | modified | 906987 | 903993 |
| build | `$.pages[0].digest` | modified | "06370d0da0bbc768bec65fda25749b37f81ac6052d08281bc19d1e974bff2989" | "f6654f7b244227b11a19e8c71ddfd6535d5a8e4ae96dd5cebf36e701165c048c" |
| build | `$.pages[0].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[0].part` | modified | "1-12" | "1-11" |
| build | `$.pages[1].digest` | modified | "7078245216ba4cce0ee5b83f12e3d6259d2e2350dbd6d4c048202f97a2399ecf" | "55ab92f28f5e43530d0af0f3475f73774aeed6cc5745b36a67af004418c4e614" |
| build | `$.pages[1].itemIds[0]` | modified | "s013" | "s012" |
| build | `$.pages[1].itemIds[1]` | modified | "s014" | "s013" |
| build | `$.pages[1].itemIds[2]` | modified | "s015" | "s014" |
| build | `$.pages[1].itemIds[3]` | modified | "s016" | "s015" |
| build | `$.pages[1].itemIds[4]` | modified | "s017" | "s016" |
| build | `$.pages[1].itemIds[5]` | modified | "s018" | "s017" |
| build | `$.pages[1].itemIds[6]` | modified | "s019" | "s018" |
| build | `$.pages[1].itemIds[7]` | modified | "s020" | "s019" |
| build | `$.pages[1].itemIds[8]` | modified | "s021" | "s020" |
| build | `$.pages[1].itemIds[9]` | added | — | "s021" |
| build | `$.pages[1].part` | modified | "13-21" | "12-21" |
| build | `$.pages[2].digest` | modified | "97e287703f88590ba1b90762a354705ba4f1e82e086db1755fafd1df47cc9231" | "9997a03da67776bb301c00b4ebe4abddaab7d80daca956fc2e2611bea5acaec5" |
| build | `$.pages[2].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[2].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[2].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[2].part` | modified | "1-14" | "1-11" |
| build | `$.pages[3].digest` | modified | "a847c60b37127ea3d0d9b4fd6b2ab8f0260d872d2d6f407752f4c7f7984b659d" | "651d6b9ac43b0e0210607bb8e913c21201148ffc355727aa0fbd432914997e56" |
| build | `$.pages[3].itemIds[0]` | modified | "s015" | "s012" |
| build | `$.pages[3].itemIds[1]` | modified | "s016" | "s013" |
| build | `$.pages[3].itemIds[2]` | modified | "s017" | "s014" |
| build | `$.pages[3].itemIds[3]` | modified | "s018" | "s015" |
| build | `$.pages[3].itemIds[4]` | modified | "s019" | "s016" |
| build | `$.pages[3].itemIds[5]` | modified | "s020" | "s017" |
| build | `$.pages[3].itemIds[6]` | modified | "s021" | "s018" |
| build | `$.pages[3].itemIds[7]` | added | — | "s019" |
| build | `$.pages[3].itemIds[8]` | added | — | "s020" |
| build | `$.pages[3].itemIds[9]` | added | — | "s021" |
| build | `$.pages[3].part` | modified | "15-21" | "12-21" |
| build | `$.pages[4].digest` | modified | "ef2adf748cdd320f016caf30fb7cdda93395241cc5dd6c25c359ce04f4f880e8" | "72ea8a5f801f65c8e779b2c9da4c4d395fa107a7d19483466c769f24e1d9dfd4" |
| build | `$.pages[4].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[4].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[4].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[4].part` | modified | "1-14" | "1-11" |
| build | `$.pages[5].digest` | modified | "445565e513f4af0cc0efb28c3398116d8cd5602081264e56d8fb0cefb6db36c3" | "e9f53aa58394eea98ee8ae2de1c802472670d4c2c08183a752e4173b45e18ed6" |
| build | `$.pages[5].itemIds[0]` | modified | "s015" | "s012" |
| build | `$.pages[5].itemIds[1]` | modified | "s016" | "s013" |
| build | `$.pages[5].itemIds[2]` | modified | "s017" | "s014" |
| build | `$.pages[5].itemIds[3]` | modified | "s018" | "s015" |
| build | `$.pages[5].itemIds[4]` | modified | "s019" | "s016" |
| build | `$.pages[5].itemIds[5]` | modified | "s020" | "s017" |
| build | `$.pages[5].itemIds[6]` | modified | "s021" | "s018" |
| build | `$.pages[5].itemIds[7]` | added | — | "s019" |
| build | `$.pages[5].itemIds[8]` | added | — | "s020" |
| build | `$.pages[5].itemIds[9]` | added | — | "s021" |
| build | `$.pages[5].part` | modified | "15-21" | "12-21" |
| build | `$.pages[6].digest` | modified | "c31a2532eb99ac003c696390186afd8cdac14f947633d0f2d4913105cc1aae74" | "c3e8aaf0bb063191acbf5f78f79ae251387c21b869460cb3d9c74912b739a529" |
| build | `$.pages[6].itemIds[10]` | added | — | "s011" |
| build | `$.pages[6].part` | modified | "1-10" | "1-11" |
| build | `$.pages[7].digest` | modified | "6b30600bca6b1fbcf2618d5bbb9f9ab1233270e28036846ac2d7b65e0a2e1323" | "cdcbb91b92f524773b1a6b9ddb22993653a030605d800dbdbe6cd40c6a5dd6e7" |
| build | `$.pages[7].itemIds[0]` | modified | "s011" | "s012" |
| build | `$.pages[7].itemIds[1]` | modified | "s012" | "s013" |
| build | `$.pages[7].itemIds[2]` | modified | "s013" | "s014" |
| build | `$.pages[7].itemIds[3]` | modified | "s014" | "s015" |
| build | `$.pages[7].itemIds[4]` | modified | "s015" | "s016" |
| build | `$.pages[7].itemIds[5]` | modified | "s016" | "s017" |
| build | `$.pages[7].itemIds[6]` | modified | "s017" | "s018" |
| build | `$.pages[7].itemIds[7]` | modified | "s018" | "s019" |
| build | `$.pages[7].itemIds[8]` | modified | "s019" | "s020" |
| build | `$.pages[7].itemIds[9]` | modified | "s020" | "s021" |
| build | `$.pages[7].part` | modified | "11-20" | "12-21" |
| build | `$.pages[8].digest` | modified | "1391c5f0195ffa03260c7707c105e48db272be45f089b424af2ccae4d8aef19f" | "07608bfb3e591a579082d5808e4d5e3484deaaabed89559644f982345afae5f8" |
| build | `$.pages[8].itemIds[0]` | modified | "s021" | "s001" |
| build | `$.pages[8].itemIds[1]` | added | — | "s002" |
| build | `$.pages[8].itemIds[2]` | added | — | "s003" |
| build | `$.pages[8].itemIds[3]` | added | — | "s004" |
| build | `$.pages[8].itemIds[4]` | added | — | "s005" |
| build | `$.pages[8].itemIds[5]` | added | — | "s006" |
| build | `$.pages[8].itemIds[6]` | added | — | "s007" |
| build | `$.pages[8].itemIds[7]` | added | — | "s008" |
| build | `$.pages[8].itemIds[8]` | added | — | "s009" |
| build | `$.pages[8].itemIds[9]` | added | — | "s010" |
| build | `$.pages[8].itemIds[10]` | added | — | "s011" |
| build | `$.pages[8].part` | modified | "21-21" | "1-11" |
| build | `$.pages[8].stageId` | modified | "4" | "5" |
| build | `$.pages[9].digest` | modified | "03701227b5dc63cb5db46d7799ef8fdfb0ca8b79c49bf20ff35275221a53f104" | "25f01cfd6070648c7d639183dded02cc3145e0351753aa71a771064c3d792dea" |
| build | `$.pages[9].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[9].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[9].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[9].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[9].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[9].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[9].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[9].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[9].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[9].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[9].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[9].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[9].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[9].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[9].part` | modified | "1-14" | "12-21" |
| build | `$.pages[10].digest` | modified | "a936efabc7bb9cc1a1a2a0eb271300fdc0ba0c6f452f23bf0531529e815aee67" | "67de0d4c6c560fe05eefdf19047d4d549e83e4b729333529642b940535dcfa80" |
| build | `$.pages[10].itemIds[0]` | modified | "s015" | "s001" |
| build | `$.pages[10].itemIds[1]` | modified | "s016" | "s002" |
| build | `$.pages[10].itemIds[2]` | modified | "s017" | "s003" |
| build | `$.pages[10].itemIds[3]` | modified | "s018" | "s004" |
| build | `$.pages[10].itemIds[4]` | modified | "s019" | "s005" |
| build | `$.pages[10].itemIds[5]` | modified | "s020" | "s006" |
| build | `$.pages[10].itemIds[6]` | modified | "s021" | "s007" |
| build | `$.pages[10].itemIds[7]` | added | — | "s008" |
| build | `$.pages[10].itemIds[8]` | added | — | "s009" |
| build | `$.pages[10].itemIds[9]` | added | — | "s010" |
| build | `$.pages[10].itemIds[10]` | added | — | "s011" |
| build | `$.pages[10].part` | modified | "15-21" | "1-11" |
| build | `$.pages[10].stageId` | modified | "5" | "6" |
| build | `$.pages[11].digest` | modified | "cccd878e90a77ede52867ef323a737f0851dc453c7f3866b3b707f70006f4a3a" | "3b1fb8da2dcfa93181b5a1c1aa55a0a720de8a230aa666ea8eef03e384932b99" |
| build | `$.pages[11].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[11].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[11].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[11].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[11].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[11].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[11].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[11].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[11].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[11].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[11].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[11].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[11].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[11].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[11].part` | modified | "1-14" | "12-21" |
| build | `$.pages[12].digest` | modified | "58a13cb4c84b7840265ac8238059e9fa553a82140f7f8081419e85e9931a2c53" | "4ffa8f28c98e5f5119a45f58aa327520ea33bd2b938dc6f803c1cbe52bb53b5f" |
| build | `$.pages[12].itemIds[0]` | removed | "s015" | — |
| build | `$.pages[12].itemIds[1]` | removed | "s016" | — |
| build | `$.pages[12].itemIds[2]` | removed | "s017" | — |
| build | `$.pages[12].itemIds[3]` | removed | "s018" | — |
| build | `$.pages[12].itemIds[4]` | removed | "s019" | — |
| build | `$.pages[12].itemIds[5]` | removed | "s020" | — |
| build | `$.pages[12].itemIds[6]` | removed | "s021" | — |
| build | `$.pages[12].part` | modified | "15-21" | null |
| build | `$.pages[12].stageId` | modified | "6" | "7" |
| build | `$.pages[13].digest` | modified | "84d82178110df8a9f5e38a3cb8b7f80aa73b3321209014b89bee39652d2f9180" | "30005ab32fbe258149f8e615551f3cfcede77ba742ce8ccbc54f3bdcbeebe1e1" |
| build | `$.pages[13].itemIds[0]` | added | — | "s001" |
| build | `$.pages[13].itemIds[1]` | added | — | "s002" |
| build | `$.pages[13].itemIds[2]` | added | — | "s003" |
| build | `$.pages[13].itemIds[3]` | added | — | "s004" |
| build | `$.pages[13].itemIds[4]` | added | — | "s005" |
| build | `$.pages[13].itemIds[5]` | added | — | "s006" |
| build | `$.pages[13].part` | modified | null | "1-6" |
| build | `$.pages[13].stageId` | modified | "7" | "8" |
| build | `$.pages[14].digest` | modified | "881341168d82b5eee408a84ae78c239c2c9eb8757a7d429dcc0a6ea19ea9bc85" | "29316aba812c9b1b8c762e4a1f4e2bc864394889d1479491daf2fd9e54d81481" |
| build | `$.pages[14].itemIds[0]` | modified | "s001" | "s007" |
| build | `$.pages[14].itemIds[1]` | modified | "s002" | "s008" |
| build | `$.pages[14].itemIds[2]` | modified | "s003" | "s009" |
| build | `$.pages[14].itemIds[3]` | modified | "s004" | "s010" |
| build | `$.pages[14].itemIds[4]` | modified | "s005" | "s011" |
| build | `$.pages[14].itemIds[5]` | removed | "s006" | — |
| build | `$.pages[14].part` | modified | "1-6" | "7-11" |
| build | `$.pages[15].digest` | modified | "61d19bdbd8baba5b411555e6d2872926c40316ab342cff16c1b32a1093e0529a" | "6f6a95969de154e09ef78f11fb3f5fe27c4dadbd89f1b8c6100b629c07e38da0" |
| build | `$.pages[15].itemIds[0]` | modified | "s007" | "s012" |
| build | `$.pages[15].itemIds[1]` | modified | "s008" | "s013" |
| build | `$.pages[15].itemIds[2]` | modified | "s009" | "s014" |
| build | `$.pages[15].itemIds[3]` | modified | "s010" | "s015" |
| build | `$.pages[15].itemIds[4]` | modified | "s011" | "s016" |
| build | `$.pages[15].itemIds[5]` | removed | "s012" | — |
| build | `$.pages[15].part` | modified | "7-12" | "12-16" |
| build | `$.pages[16].digest` | modified | "5ade2829f5676b5929d6f3d2ba2ed3bf27b2e6c0cb0a8e8f25dba11593e0a043" | "520e42bfaff2855a4a85ddf44aa69813a85ac4394320d59ef5ebd9edc6b02a5e" |
| build | `$.pages[16].itemIds[0]` | modified | "s013" | "s017" |
| build | `$.pages[16].itemIds[1]` | modified | "s014" | "s018" |
| build | `$.pages[16].itemIds[2]` | modified | "s015" | "s019" |
| build | `$.pages[16].itemIds[3]` | modified | "s016" | "s020" |
| build | `$.pages[16].itemIds[4]` | modified | "s017" | "s021" |
| build | `$.pages[16].itemIds[5]` | removed | "s018" | — |
| build | `$.pages[16].part` | modified | "13-18" | "17-21" |
| build | `$.pages[17].digest` | modified | "9613774259637c0a6f5d9776561e781f63a63c85e71d61f770162d592e6a5853" | "885887004859a1f71e0e7c4f4d660f62b3c37295e23cefcbda97d1da04c385bb" |
| build | `$.pages[17].itemIds[0]` | removed | "s019" | — |
| build | `$.pages[17].itemIds[1]` | removed | "s020" | — |
| build | `$.pages[17].itemIds[2]` | removed | "s021" | — |
| build | `$.pages[17].part` | modified | "19-21" | null |
| build | `$.pages[17].stageId` | modified | "8" | "9" |
| build | `$.pages[18].digest` | modified | "dbe07b374cac4c714b30901b847e910bd056bbedf32aef7143c0d350f3377236" | "a6e9bc81dc26a14c42d32a19c04bf45e3c5f6f85f08aab003855e87308462c61" |
| build | `$.pages[18].itemIds[0]` | added | — | "s001" |
| build | `$.pages[18].itemIds[1]` | added | — | "s002" |
| build | `$.pages[18].itemIds[2]` | added | — | "s003" |
| build | `$.pages[18].itemIds[3]` | added | — | "s004" |
| build | `$.pages[18].itemIds[4]` | added | — | "s005" |
| build | `$.pages[18].itemIds[5]` | added | — | "s006" |
| build | `$.pages[18].itemIds[6]` | added | — | "s007" |
| build | `$.pages[18].part` | modified | null | "1-7" |
| build | `$.pages[18].stageId` | modified | "9" | "10" |
| build | `$.pages[19].digest` | modified | "85ccb9663bb440f80792085b31f8e17e66e15801e4e36d75ced8481e3e73259f" | "ba7252bac19845cb8e2595a2757479645ab29351609f1b5549c211755b7d6a1d" |
| build | `$.pages[19].itemIds[0]` | modified | "s001" | "s008" |
| build | `$.pages[19].itemIds[1]` | modified | "s002" | "s009" |
| build | `$.pages[19].itemIds[2]` | modified | "s003" | "s010" |
| build | `$.pages[19].itemIds[3]` | modified | "s004" | "s011" |
| build | `$.pages[19].itemIds[4]` | modified | "s005" | "s012" |
| build | `$.pages[19].itemIds[5]` | modified | "s006" | "s013" |
| build | `$.pages[19].itemIds[6]` | modified | "s007" | "s014" |
| build | `$.pages[19].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[19].part` | modified | "1-8" | "8-14" |
| build | `$.pages[20].digest` | modified | "6a43538d32c2bb19e78c65a0e4d82dd2710c1f6ca73fa27680eb38bf82f30274" | "f532316931343209ecf50e315503b136275ee520e59c46ee9f91359a20ffd2b5" |
| build | `$.pages[20].itemIds[0]` | modified | "s009" | "s015" |
| build | `$.pages[20].itemIds[1]` | modified | "s010" | "s016" |
| build | `$.pages[20].itemIds[2]` | modified | "s011" | "s017" |
| build | `$.pages[20].itemIds[3]` | modified | "s012" | "s018" |
| build | `$.pages[20].itemIds[4]` | modified | "s013" | "s019" |
| build | `$.pages[20].itemIds[5]` | modified | "s014" | "s020" |
| build | `$.pages[20].itemIds[6]` | modified | "s015" | "s021" |
| build | `$.pages[20].itemIds[7]` | removed | "s016" | — |
| build | `$.pages[20].part` | modified | "9-16" | "15-21" |
| build | `$.pages[21].digest` | modified | "7ac818903b3901d184899ebf3f6c49cf39f36b3ee7ac1397ce8ebd84aa11ed5a" | "f6654f7b244227b11a19e8c71ddfd6535d5a8e4ae96dd5cebf36e701165c048c" |
| build | `$.pages[21].edition` | modified | "student" | "answer" |
| build | `$.pages[21].id` | modified | "student:when-failure-become-ideas-p22" | "answer:when-failure-become-ideas-p01" |
| build | `$.pages[21].itemIds[0]` | modified | "s017" | "s001" |
| build | `$.pages[21].itemIds[1]` | modified | "s018" | "s002" |
| build | `$.pages[21].itemIds[2]` | modified | "s019" | "s003" |
| build | `$.pages[21].itemIds[3]` | modified | "s020" | "s004" |
| build | `$.pages[21].itemIds[4]` | modified | "s021" | "s005" |
| build | `$.pages[21].itemIds[5]` | added | — | "s006" |
| build | `$.pages[21].itemIds[6]` | added | — | "s007" |
| build | `$.pages[21].itemIds[7]` | added | — | "s008" |
| build | `$.pages[21].itemIds[8]` | added | — | "s009" |
| build | `$.pages[21].itemIds[9]` | added | — | "s010" |
| build | `$.pages[21].itemIds[10]` | added | — | "s011" |
| build | `$.pages[21].page` | modified | 22 | 1 |
| build | `$.pages[21].pageId` | modified | "when-failure-become-ideas-p22" | "when-failure-become-ideas-p01" |
| build | `$.pages[21].part` | modified | "17-21" | "1-11" |
| build | `$.pages[21].stageId` | modified | "10" | "1" |
| build | `$.pages[22].digest` | modified | "06370d0da0bbc768bec65fda25749b37f81ac6052d08281bc19d1e974bff2989" | "55ab92f28f5e43530d0af0f3475f73774aeed6cc5745b36a67af004418c4e614" |
| build | `$.pages[22].id` | modified | "answer:when-failure-become-ideas-p01" | "answer:when-failure-become-ideas-p02" |
| build | `$.pages[22].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[22].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[22].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[22].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[22].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[22].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[22].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[22].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[22].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[22].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[22].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[22].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[22].page` | modified | 1 | 2 |
| build | `$.pages[22].pageId` | modified | "when-failure-become-ideas-p01" | "when-failure-become-ideas-p02" |
| build | `$.pages[22].part` | modified | "1-12" | "12-21" |
| build | `$.pages[23].digest` | modified | "7078245216ba4cce0ee5b83f12e3d6259d2e2350dbd6d4c048202f97a2399ecf" | "78002335c8bdc1a333a67f30933d0989955be2852b369523e8e1cf83e59dff76" |
| build | `$.pages[23].id` | modified | "answer:when-failure-become-ideas-p02" | "answer:when-failure-become-ideas-p03" |
| build | `$.pages[23].itemIds[0]` | modified | "s013" | "s001" |
| build | `$.pages[23].itemIds[1]` | modified | "s014" | "s002" |
| build | `$.pages[23].itemIds[2]` | modified | "s015" | "s003" |
| build | `$.pages[23].itemIds[3]` | modified | "s016" | "s004" |
| build | `$.pages[23].itemIds[4]` | modified | "s017" | "s005" |
| build | `$.pages[23].itemIds[5]` | modified | "s018" | "s006" |
| build | `$.pages[23].itemIds[6]` | modified | "s019" | "s007" |
| build | `$.pages[23].itemIds[7]` | modified | "s020" | "s008" |
| build | `$.pages[23].itemIds[8]` | modified | "s021" | "s009" |
| build | `$.pages[23].itemIds[9]` | added | — | "s010" |
| build | `$.pages[23].itemIds[10]` | added | — | "s011" |
| build | `$.pages[23].page` | modified | 2 | 3 |
| build | `$.pages[23].pageId` | modified | "when-failure-become-ideas-p02" | "when-failure-become-ideas-p03" |
| build | `$.pages[23].part` | modified | "13-21" | "1-11" |
| build | `$.pages[23].stageId` | modified | "1" | "2" |
| build | `$.pages[24].digest` | modified | "4c174e2a6abf2be5b932b1046d7c243ca0f9e7951318cd0b278beba51a91f38c" | "bbac91e1b58203ab26f33ac87744537aec9aa4c0b527daccaa209d4e9e8f6648" |
| build | `$.pages[24].id` | modified | "answer:when-failure-become-ideas-p03" | "answer:when-failure-become-ideas-p04" |
| build | `$.pages[24].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[24].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[24].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[24].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[24].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[24].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[24].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[24].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[24].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[24].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[24].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[24].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[24].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[24].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[24].page` | modified | 3 | 4 |
| build | `$.pages[24].pageId` | modified | "when-failure-become-ideas-p03" | "when-failure-become-ideas-p04" |
| build | `$.pages[24].part` | modified | "1-14" | "12-21" |
| build | `$.pages[25].digest` | modified | "8965aa65f245bf81ea6f352aeeb122ad3383f7a365490fc43dcafdc12b95ec1e" | "317a5b73dda721a8efc66c96148360402722e1546902fc319fa31fd0e76b54bc" |
| build | `$.pages[25].id` | modified | "answer:when-failure-become-ideas-p04" | "answer:when-failure-become-ideas-p05" |
| build | `$.pages[25].itemIds[0]` | modified | "s015" | "s001" |
| build | `$.pages[25].itemIds[1]` | modified | "s016" | "s002" |
| build | `$.pages[25].itemIds[2]` | modified | "s017" | "s003" |
| build | `$.pages[25].itemIds[3]` | modified | "s018" | "s004" |
| build | `$.pages[25].itemIds[4]` | modified | "s019" | "s005" |
| build | `$.pages[25].itemIds[5]` | modified | "s020" | "s006" |
| build | `$.pages[25].itemIds[6]` | modified | "s021" | "s007" |
| build | `$.pages[25].itemIds[7]` | added | — | "s008" |
| build | `$.pages[25].itemIds[8]` | added | — | "s009" |
| build | `$.pages[25].itemIds[9]` | added | — | "s010" |
| build | `$.pages[25].itemIds[10]` | added | — | "s011" |
| build | `$.pages[25].page` | modified | 4 | 5 |
| build | `$.pages[25].pageId` | modified | "when-failure-become-ideas-p04" | "when-failure-become-ideas-p05" |
| build | `$.pages[25].part` | modified | "15-21" | "1-11" |
| build | `$.pages[25].stageId` | modified | "2" | "3" |
| build | `$.pages[26].digest` | modified | "afe86177223a9d9d781f0bcea27737e1dd86f4151804648f6282aaafe7f8cf0b" | "32e7cbe4eec42c1c04a930dfcc4285daa72c8462128d28d8a1e6b10360e9d801" |
| build | `$.pages[26].id` | modified | "answer:when-failure-become-ideas-p05" | "answer:when-failure-become-ideas-p06" |
| build | `$.pages[26].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[26].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[26].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[26].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[26].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[26].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[26].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[26].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[26].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[26].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[26].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[26].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[26].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[26].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[26].page` | modified | 5 | 6 |
| build | `$.pages[26].pageId` | modified | "when-failure-become-ideas-p05" | "when-failure-become-ideas-p06" |
| build | `$.pages[26].part` | modified | "1-14" | "12-21" |
| build | `$.pages[27].digest` | modified | "8cedb6e61d2e1bb562950083ca50887d27b5f852cb3e2bf79f32395cc7ce4cf1" | "d44f92a03f2000e38045103caec06c827036982f11b7c694db85a795b3478068" |
| build | `$.pages[27].id` | modified | "answer:when-failure-become-ideas-p06" | "answer:when-failure-become-ideas-p07" |
| build | `$.pages[27].itemIds[0]` | modified | "s015" | "s001" |
| build | `$.pages[27].itemIds[1]` | modified | "s016" | "s002" |
| build | `$.pages[27].itemIds[2]` | modified | "s017" | "s003" |
| build | `$.pages[27].itemIds[3]` | modified | "s018" | "s004" |
| build | `$.pages[27].itemIds[4]` | modified | "s019" | "s005" |
| build | `$.pages[27].itemIds[5]` | modified | "s020" | "s006" |
| build | `$.pages[27].itemIds[6]` | modified | "s021" | "s007" |
| build | `$.pages[27].itemIds[7]` | added | — | "s008" |
| build | `$.pages[27].itemIds[8]` | added | — | "s009" |
| build | `$.pages[27].itemIds[9]` | added | — | "s010" |
| build | `$.pages[27].itemIds[10]` | added | — | "s011" |
| build | `$.pages[27].page` | modified | 6 | 7 |
| build | `$.pages[27].pageId` | modified | "when-failure-become-ideas-p06" | "when-failure-become-ideas-p07" |
| build | `$.pages[27].part` | modified | "15-21" | "1-11" |
| build | `$.pages[27].stageId` | modified | "3" | "4" |
| build | `$.pages[28].digest` | modified | "87a4a8fac720ff3263736bc6dbcdc3ab8821b198713576c4a3f5460f9ddd37a0" | "5278c878283e41342f46d754946f47749c7b88ec8bc77bc0d38eee96bd57db61" |
| build | `$.pages[28].id` | modified | "answer:when-failure-become-ideas-p07" | "answer:when-failure-become-ideas-p08" |
| build | `$.pages[28].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[28].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[28].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[28].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[28].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[28].itemIds[5]` | modified | "s006" | "s017" |
| build | `$.pages[28].itemIds[6]` | modified | "s007" | "s018" |
| build | `$.pages[28].itemIds[7]` | modified | "s008" | "s019" |
| build | `$.pages[28].itemIds[8]` | modified | "s009" | "s020" |
| build | `$.pages[28].itemIds[9]` | modified | "s010" | "s021" |
| build | `$.pages[28].page` | modified | 7 | 8 |
| build | `$.pages[28].pageId` | modified | "when-failure-become-ideas-p07" | "when-failure-become-ideas-p08" |
| build | `$.pages[28].part` | modified | "1-10" | "12-21" |
| build | `$.pages[29].digest` | modified | "4d404ac7f731a222e2fb37452f76b4a5e9208419c771760d79ec57cf8017fbc4" | "4f103d3a9d1d727339793ff9cc3d41f904a936345cfc839491bc180beca3d560" |
| build | `$.pages[29].id` | modified | "answer:when-failure-become-ideas-p08" | "answer:when-failure-become-ideas-p09" |
| build | `$.pages[29].itemIds[0]` | modified | "s011" | "s001" |
| build | `$.pages[29].itemIds[1]` | modified | "s012" | "s002" |
| build | `$.pages[29].itemIds[2]` | modified | "s013" | "s003" |
| build | `$.pages[29].itemIds[3]` | modified | "s014" | "s004" |
| build | `$.pages[29].itemIds[4]` | modified | "s015" | "s005" |
| build | `$.pages[29].itemIds[5]` | modified | "s016" | "s006" |
| build | `$.pages[29].itemIds[6]` | modified | "s017" | "s007" |
| build | `$.pages[29].itemIds[7]` | modified | "s018" | "s008" |
| build | `$.pages[29].itemIds[8]` | modified | "s019" | "s009" |
| build | `$.pages[29].itemIds[9]` | modified | "s020" | "s010" |
| build | `$.pages[29].itemIds[10]` | added | — | "s011" |
| build | `$.pages[29].page` | modified | 8 | 9 |
| build | `$.pages[29].pageId` | modified | "when-failure-become-ideas-p08" | "when-failure-become-ideas-p09" |
| build | `$.pages[29].part` | modified | "11-20" | "1-11" |
| build | `$.pages[29].stageId` | modified | "4" | "5" |
| build | `$.pages[30].digest` | modified | "520886b6967d727354ae5de4dae68b07c6a3d4771b3ccac6088b1fefdb841324" | "3b53947142865147c866fc0e6c6a4a0dfbe4e828649ac01cfa78163ed1a584de" |
| build | `$.pages[30].id` | modified | "answer:when-failure-become-ideas-p09" | "answer:when-failure-become-ideas-p10" |
| build | `$.pages[30].itemIds[0]` | modified | "s021" | "s012" |
| build | `$.pages[30].itemIds[1]` | added | — | "s013" |
| build | `$.pages[30].itemIds[2]` | added | — | "s014" |
| build | `$.pages[30].itemIds[3]` | added | — | "s015" |
| build | `$.pages[30].itemIds[4]` | added | — | "s016" |
| build | `$.pages[30].itemIds[5]` | added | — | "s017" |
| build | `$.pages[30].itemIds[6]` | added | — | "s018" |
| build | `$.pages[30].itemIds[7]` | added | — | "s019" |
| build | `$.pages[30].itemIds[8]` | added | — | "s020" |
| build | `$.pages[30].itemIds[9]` | added | — | "s021" |
| build | `$.pages[30].page` | modified | 9 | 10 |
| build | `$.pages[30].pageId` | modified | "when-failure-become-ideas-p09" | "when-failure-become-ideas-p10" |
| build | `$.pages[30].part` | modified | "21-21" | "12-21" |
| build | `$.pages[30].stageId` | modified | "4" | "5" |
| build | `$.pages[31].digest` | modified | "35da7c02035be6bc5a6b64d565cc5ad07b4c0fe6b295331496c479267e5b04dc" | "44b3605202869c7c53bee627f0daa0b025221da735304bc5feec97acb68a0518" |
| build | `$.pages[31].id` | modified | "answer:when-failure-become-ideas-p10" | "answer:when-failure-become-ideas-p11" |
| build | `$.pages[31].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[31].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[31].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[31].page` | modified | 10 | 11 |
| build | `$.pages[31].pageId` | modified | "when-failure-become-ideas-p10" | "when-failure-become-ideas-p11" |
| build | `$.pages[31].part` | modified | "1-14" | "1-11" |
| build | `$.pages[31].stageId` | modified | "5" | "6" |
| build | `$.pages[32].digest` | modified | "47500c0296e031096baaf811da52b04fd7ccb9fffa9396d8eab04cfbf24dd977" | "f847dd406c7e443e477d7f55145e5d50988db0946b171686531754083520991d" |
| build | `$.pages[32].id` | modified | "answer:when-failure-become-ideas-p11" | "answer:when-failure-become-ideas-p12" |
| build | `$.pages[32].itemIds[0]` | modified | "s015" | "s012" |
| build | `$.pages[32].itemIds[1]` | modified | "s016" | "s013" |
| build | `$.pages[32].itemIds[2]` | modified | "s017" | "s014" |
| build | `$.pages[32].itemIds[3]` | modified | "s018" | "s015" |
| build | `$.pages[32].itemIds[4]` | modified | "s019" | "s016" |
| build | `$.pages[32].itemIds[5]` | modified | "s020" | "s017" |
| build | `$.pages[32].itemIds[6]` | modified | "s021" | "s018" |
| build | `$.pages[32].itemIds[7]` | added | — | "s019" |
| build | `$.pages[32].itemIds[8]` | added | — | "s020" |
| build | `$.pages[32].itemIds[9]` | added | — | "s021" |
| build | `$.pages[32].page` | modified | 11 | 12 |
| build | `$.pages[32].pageId` | modified | "when-failure-become-ideas-p11" | "when-failure-become-ideas-p12" |
| build | `$.pages[32].part` | modified | "15-21" | "12-21" |
| build | `$.pages[32].stageId` | modified | "5" | "6" |
| build | `$.pages[33].digest` | modified | "946564835f8b1075fd5b42af0318ac85b07a8cdff33495963ca3c90e6367b9b4" | "9d539a475e4b11f31dca0d94ebaf0ed8ace09d43117bfc9181b3a20ea22ef5b4" |
| build | `$.pages[33].id` | modified | "answer:when-failure-become-ideas-p12" | "answer:when-failure-become-ideas-p13" |
| build | `$.pages[33].itemIds[0]` | removed | "s001" | — |
| build | `$.pages[33].itemIds[1]` | removed | "s002" | — |
| build | `$.pages[33].itemIds[2]` | removed | "s003" | — |
| build | `$.pages[33].itemIds[3]` | removed | "s004" | — |
| build | `$.pages[33].itemIds[4]` | removed | "s005" | — |
| build | `$.pages[33].itemIds[5]` | removed | "s006" | — |
| build | `$.pages[33].itemIds[6]` | removed | "s007" | — |
| build | `$.pages[33].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[33].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[33].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[33].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[33].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[33].itemIds[12]` | removed | "s013" | — |
| build | `$.pages[33].itemIds[13]` | removed | "s014" | — |
| build | `$.pages[33].page` | modified | 12 | 13 |
| build | `$.pages[33].pageId` | modified | "when-failure-become-ideas-p12" | "when-failure-become-ideas-p13" |
| build | `$.pages[33].part` | modified | "1-14" | null |
| build | `$.pages[33].stageId` | modified | "6" | "7" |
| build | `$.pages[34].digest` | modified | "fd9d52995ea656b5b40dee332a92f6b95633b01d00be451647fab69b8bd51555" | "1a364197d04edf760aff18f1e8c4e72334fdc473fab16616deb1bac79c58be7a" |
| build | `$.pages[34].id` | modified | "answer:when-failure-become-ideas-p13" | "answer:when-failure-become-ideas-p14" |
| build | `$.pages[34].itemIds[0]` | modified | "s015" | "s001" |
| build | `$.pages[34].itemIds[1]` | modified | "s016" | "s002" |
| build | `$.pages[34].itemIds[2]` | modified | "s017" | "s003" |
| build | `$.pages[34].itemIds[3]` | modified | "s018" | "s004" |
| build | `$.pages[34].itemIds[4]` | modified | "s019" | "s005" |
| build | `$.pages[34].itemIds[5]` | modified | "s020" | "s006" |
| build | `$.pages[34].itemIds[6]` | removed | "s021" | — |
| build | `$.pages[34].page` | modified | 13 | 14 |
| build | `$.pages[34].pageId` | modified | "when-failure-become-ideas-p13" | "when-failure-become-ideas-p14" |
| build | `$.pages[34].part` | modified | "15-21" | "1-6" |
| build | `$.pages[34].stageId` | modified | "6" | "8" |
| build | `$.pages[35].digest` | modified | "107b4f15d85487613705999cae3fd55f8ff586cc911f0d0603325297f2c51017" | "3385bc22aebe8196b373b9f120113750f7edfeee2226a08c6ae14390bea329ac" |
| build | `$.pages[35].id` | modified | "answer:when-failure-become-ideas-p14" | "answer:when-failure-become-ideas-p15" |
| build | `$.pages[35].itemIds[0]` | added | — | "s007" |
| build | `$.pages[35].itemIds[1]` | added | — | "s008" |
| build | `$.pages[35].itemIds[2]` | added | — | "s009" |
| build | `$.pages[35].itemIds[3]` | added | — | "s010" |
| build | `$.pages[35].itemIds[4]` | added | — | "s011" |
| build | `$.pages[35].page` | modified | 14 | 15 |
| build | `$.pages[35].pageId` | modified | "when-failure-become-ideas-p14" | "when-failure-become-ideas-p15" |
| build | `$.pages[35].part` | modified | null | "7-11" |
| build | `$.pages[35].stageId` | modified | "7" | "8" |
| build | `$.pages[36].digest` | modified | "75a5b0c3c64c6ce0d76954a3def3a73272045b47c9ce1af8f701f490d2e14e1e" | "42bf4f03ed886012f667976a3439bc5dae80b2128e1bacf061cfca09016eb7ee" |
| build | `$.pages[36].id` | modified | "answer:when-failure-become-ideas-p15" | "answer:when-failure-become-ideas-p16" |
| build | `$.pages[36].itemIds[0]` | modified | "s001" | "s012" |
| build | `$.pages[36].itemIds[1]` | modified | "s002" | "s013" |
| build | `$.pages[36].itemIds[2]` | modified | "s003" | "s014" |
| build | `$.pages[36].itemIds[3]` | modified | "s004" | "s015" |
| build | `$.pages[36].itemIds[4]` | modified | "s005" | "s016" |
| build | `$.pages[36].itemIds[5]` | removed | "s006" | — |
| build | `$.pages[36].page` | modified | 15 | 16 |
| build | `$.pages[36].pageId` | modified | "when-failure-become-ideas-p15" | "when-failure-become-ideas-p16" |
| build | `$.pages[36].part` | modified | "1-6" | "12-16" |
| build | `$.pages[37].digest` | modified | "c632e686cae48f355b523f6da6f4d365220f099e0e3a8c932556cbc050faa4f4" | "7f60ecdfd2c62b15b7e6e7e41fe907d79c466923552324d1a328ac7103302bd7" |
| build | `$.pages[37].id` | modified | "answer:when-failure-become-ideas-p16" | "answer:when-failure-become-ideas-p17" |
| build | `$.pages[37].itemIds[0]` | modified | "s007" | "s017" |
| build | `$.pages[37].itemIds[1]` | modified | "s008" | "s018" |
| build | `$.pages[37].itemIds[2]` | modified | "s009" | "s019" |
| build | `$.pages[37].itemIds[3]` | modified | "s010" | "s020" |
| build | `$.pages[37].itemIds[4]` | modified | "s011" | "s021" |
| build | `$.pages[37].itemIds[5]` | removed | "s012" | — |
| build | `$.pages[37].page` | modified | 16 | 17 |
| build | `$.pages[37].pageId` | modified | "when-failure-become-ideas-p16" | "when-failure-become-ideas-p17" |
| build | `$.pages[37].part` | modified | "7-12" | "17-21" |
| build | `$.pages[38].digest` | modified | "e36355fdfb89260501fe4bb23216d97435ee65eeb62e7fd029743099f6ac1af8" | "af59690eb0fe7cb7f224e4e1dfbea237d88ddbe36fdc87b29de5cce55b9edff9" |
| build | `$.pages[38].id` | modified | "answer:when-failure-become-ideas-p17" | "answer:when-failure-become-ideas-p18" |
| build | `$.pages[38].itemIds[0]` | removed | "s013" | — |
| build | `$.pages[38].itemIds[1]` | removed | "s014" | — |
| build | `$.pages[38].itemIds[2]` | removed | "s015" | — |
| build | `$.pages[38].itemIds[3]` | removed | "s016" | — |
| build | `$.pages[38].itemIds[4]` | removed | "s017" | — |
| build | `$.pages[38].itemIds[5]` | removed | "s018" | — |
| build | `$.pages[38].page` | modified | 17 | 18 |
| build | `$.pages[38].pageId` | modified | "when-failure-become-ideas-p17" | "when-failure-become-ideas-p18" |
| build | `$.pages[38].part` | modified | "13-18" | null |
| build | `$.pages[38].stageId` | modified | "8" | "9" |
| build | `$.pages[39].digest` | modified | "65fae8e2373e204d0619b5ad723cb84ec55536b7e653359f97c7aa8a6b8b6a77" | "b32b2449bb75896a0272ac6154f806dc3613249ebbad8ddcfc361100c05d140c" |
| build | `$.pages[39].id` | modified | "answer:when-failure-become-ideas-p18" | "answer:when-failure-become-ideas-p19" |
| build | `$.pages[39].itemIds[0]` | modified | "s019" | "s001" |
| build | `$.pages[39].itemIds[1]` | modified | "s020" | "s002" |
| build | `$.pages[39].itemIds[2]` | modified | "s021" | "s003" |
| build | `$.pages[39].itemIds[3]` | added | — | "s004" |
| build | `$.pages[39].itemIds[4]` | added | — | "s005" |
| build | `$.pages[39].itemIds[5]` | added | — | "s006" |
| build | `$.pages[39].itemIds[6]` | added | — | "s007" |
| build | `$.pages[39].page` | modified | 18 | 19 |
| build | `$.pages[39].pageId` | modified | "when-failure-become-ideas-p18" | "when-failure-become-ideas-p19" |
| build | `$.pages[39].part` | modified | "19-21" | "1-7" |
| build | `$.pages[39].stageId` | modified | "8" | "10" |
| build | `$.pages[40].digest` | modified | "b724bd7030f45a512cfb142c4310a1e22bf5f2ea14890b8910b10428d85209dd" | "37f54bf55dae03719e60761489b4b14ef34e680b635bbe9c8c19101a9041bd32" |
| build | `$.pages[40].id` | modified | "answer:when-failure-become-ideas-p19" | "answer:when-failure-become-ideas-p20" |
| build | `$.pages[40].itemIds[0]` | added | — | "s008" |
| build | `$.pages[40].itemIds[1]` | added | — | "s009" |
| build | `$.pages[40].itemIds[2]` | added | — | "s010" |
| build | `$.pages[40].itemIds[3]` | added | — | "s011" |
| build | `$.pages[40].itemIds[4]` | added | — | "s012" |
| build | `$.pages[40].itemIds[5]` | added | — | "s013" |
| build | `$.pages[40].itemIds[6]` | added | — | "s014" |
| build | `$.pages[40].page` | modified | 19 | 20 |
| build | `$.pages[40].pageId` | modified | "when-failure-become-ideas-p19" | "when-failure-become-ideas-p20" |
| build | `$.pages[40].part` | modified | null | "8-14" |
| build | `$.pages[40].stageId` | modified | "9" | "10" |
| build | `$.pages[41].digest` | modified | "2e0d2761d171da1cfbf074e56bdfdaf98ad055cf5845a98efaa34e0575814d9d" | "f46983ac8b277ee35b02fbd5102185e0c567e4c2e8df13d91306d3cbba43c7da" |
| build | `$.pages[41].id` | modified | "answer:when-failure-become-ideas-p20" | "answer:when-failure-become-ideas-p21" |
| build | `$.pages[41].itemIds[0]` | modified | "s001" | "s015" |
| build | `$.pages[41].itemIds[1]` | modified | "s002" | "s016" |
| build | `$.pages[41].itemIds[2]` | modified | "s003" | "s017" |
| build | `$.pages[41].itemIds[3]` | modified | "s004" | "s018" |
| build | `$.pages[41].itemIds[4]` | modified | "s005" | "s019" |
| build | `$.pages[41].itemIds[5]` | modified | "s006" | "s020" |
| build | `$.pages[41].itemIds[6]` | modified | "s007" | "s021" |
| build | `$.pages[41].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[41].page` | modified | 20 | 21 |
| build | `$.pages[41].pageId` | modified | "when-failure-become-ideas-p20" | "when-failure-become-ideas-p21" |
| build | `$.pages[41].part` | modified | "1-8" | "15-21" |
| build | `$.pages[42]` | removed | {"digest":"1a00f72702f4ff195224f2411c74c005c8d5c0f409bceba035de177471e9de67","edition":"answer","id":"answer:when-failu… | — |
| build | `$.pages[43]` | removed | {"digest":"2ccaaa04e066dd828b1d3a84cb7a082a0139709d56fe0b03bc56db8a2110c2f4","edition":"answer","id":"answer:when-failu… | — |
| build | `$.qa.dom.answer.pages` | modified | 22 | 21 |
| build | `$.qa.dom.student.pages` | modified | 22 | 21 |
| build | `$.qa.pdf.answerPages` | modified | 22 | 21 |
| build | `$.qa.pdf.studentPages` | modified | 22 | 21 |
| build | `$.qa.visualSamples[3]` | modified | "qa/samples/student-p12.png" | "qa/samples/student-p11.png" |
| build | `$.qa.visualSamples[4]` | modified | "qa/samples/student-p14.png" | "qa/samples/student-p13.png" |
| build | `$.qa.visualSamples[5]` | modified | "qa/samples/student-p15.png" | "qa/samples/student-p14.png" |
| build | `$.qa.visualSamples[6]` | modified | "qa/samples/student-p19.png" | "qa/samples/student-p18.png" |
| build | `$.qa.visualSamples[7]` | modified | "qa/samples/student-p20.png" | "qa/samples/student-p19.png" |
| build | `$.qa.visualSamples[8]` | modified | "qa/samples/student-p22.png" | "qa/samples/student-p21.png" |
| build | `$.qa.visualSamples[12]` | modified | "qa/samples/answer-p12.png" | "qa/samples/answer-p11.png" |
| build | `$.qa.visualSamples[13]` | modified | "qa/samples/answer-p14.png" | "qa/samples/answer-p13.png" |
| build | `$.qa.visualSamples[14]` | modified | "qa/samples/answer-p15.png" | "qa/samples/answer-p14.png" |
| build | `$.qa.visualSamples[15]` | modified | "qa/samples/answer-p19.png" | "qa/samples/answer-p18.png" |
| build | `$.qa.visualSamples[16]` | modified | "qa/samples/answer-p20.png" | "qa/samples/answer-p19.png" |
| build | `$.qa.visualSamples[17]` | modified | "qa/samples/answer-p22.png" | "qa/samples/answer-p21.png" |
| build | `$.specVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 전체 contact sheet와 8단계 15페이지 원본 PNG를 확인함. 요청된 조각형 정답 밑줄이 문제·해설 모두 제거되었고, 학생용은 우리말·제시어·긴 작성선만, 해설용은 동일 긴 답안 영역에 … | "학생용·해설용 contact sheet와 4단계 7·8페이지 원본을 확인함. 21문항이 1-11/12-21로 균등 배치되어 21번 단독 꼬리 페이지가 제거되고 총 21쪽으로 감소함. 8단계 조각 밑줄 제거 상태,… |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-23T23:18:57+09:00" | "2026-07-23T23:27:57+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:when-failure-become-ideas-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| answer:when-failure-become-ideas-p02 | modified | 1 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:when-failure-become-ideas-p04 | modified | 2 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p05 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:when-failure-become-ideas-p06 | modified | 3 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p07 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011 |
| answer:when-failure-become-ideas-p08 | modified | 4 | s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p09 | modified | 4, 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s021 |
| answer:when-failure-become-ideas-p10 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p11 | modified | 5, 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p12 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p13 | modified | 6, 7 | s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p14 | modified | 7, 8 | s001, s002, s003, s004, s005, s006 |
| answer:when-failure-become-ideas-p15 | modified | 8 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011 |
| answer:when-failure-become-ideas-p16 | modified | 8 | s007, s008, s009, s010, s011, s012, s013, s014, s015, s016 |
| answer:when-failure-become-ideas-p17 | modified | 8 | s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p18 | modified | 8, 9 | s019, s020, s021 |
| answer:when-failure-become-ideas-p19 | modified | 9, 10 | s001, s002, s003, s004, s005, s006, s007 |
| answer:when-failure-become-ideas-p20 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:when-failure-become-ideas-p21 | modified | 10 | s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| answer:when-failure-become-ideas-p22 | removed | 10 | s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| student:when-failure-become-ideas-p02 | modified | 1 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:when-failure-become-ideas-p04 | modified | 2 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p05 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:when-failure-become-ideas-p06 | modified | 3 | s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p07 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011 |
| student:when-failure-become-ideas-p08 | modified | 4 | s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p09 | modified | 4, 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s021 |
| student:when-failure-become-ideas-p10 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p11 | modified | 5, 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p12 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p13 | modified | 6, 7 | s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p14 | modified | 7, 8 | s001, s002, s003, s004, s005, s006 |
| student:when-failure-become-ideas-p15 | modified | 8 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011 |
| student:when-failure-become-ideas-p16 | modified | 8 | s007, s008, s009, s010, s011, s012, s013, s014, s015, s016 |
| student:when-failure-become-ideas-p17 | modified | 8 | s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p18 | modified | 8, 9 | s019, s020, s021 |
| student:when-failure-become-ideas-p19 | modified | 9, 10 | s001, s002, s003, s004, s005, s006, s007 |
| student:when-failure-become-ideas-p20 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:when-failure-become-ideas-p21 | modified | 10 | s009, s010, s011, s012, s013, s014, s015, s016, s017, s018, s019, s020, s021 |
| student:when-failure-become-ideas-p22 | removed | 10 | s017, s018, s019, s020, s021 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"37f89c7c8f7b24ac87971238fd888739ee284a80100a51f68909a6b067ab1f17","size":158301} | {"path":"문제.html","sha256":"e3c5747aacbdbf15d6ee4deb28ad3274e6cb27dce9a658f3024fb095b88ab273","size":158027} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"2bf580f00790889d83b2b1a73b3691af0d60f0374ab84b05dded592e489e3861","size":757943} | {"path":"문제.pdf","sha256":"69deb9513358e26541ddc62e2f6e7352b6fbe933a3423a1b40f0ecb8a5ca598e","size":755102} |
| `해설.html` | modified | {"path":"해설.html","sha256":"8e7a95e0cc69e764176dfd2caef1f2f045a11d42b70ddf8334a6b14099b2febc","size":170688} | {"path":"해설.html","sha256":"10ded181cd65064d7d60f155b9a9c7e024439fa05512ec3dd8245e9cc99b6ef3","size":170414} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"70e17c504736025a66d40300b5348cd03475db09429fb6acdd10aabfd1921dc8","size":906987} | {"path":"해설.pdf","sha256":"b76d86fc0ec1567b320ca59d18a2ee9819df156ea3489b323272c44a91860b91","size":903993} |

## 영향 없음

- 동일한 manifest 구성 요소: `template`
- 직접·파생 변경이 기록되지 않은 단계: 없음
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

- 직접 JSON 경로: 590
- 파생 JSON 경로: 0
- 변경·선언 파일: 17
- 영향 페이지: 44
- 변경 출력: 4
