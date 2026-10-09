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
| canonical | 1.0.1 | 1.0.2 | `de361e27fff4` | `b53eb6d776d2` | 변경 |
| spec | 1.0.1 | 1.0.2 | `729f1700e7c8` | `a28c254c251d` | 변경 |
| template | 1.0.1 | 1.0.1 | `6456357b00c6` | `6456357b00c6` | 동일 |
| build | 1.0.1 | 1.0.2 | `a9442a4f0704` | `c6f8b75b7052` | 변경 |

## 파일 변경

| 구분 | manifest | 파일 | 변경 | 이전 | 이후 |
|---|---|---|---|---|---|
| 파생 | build | `문제.html` | modified | {"sha256":"8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c","s… | {"sha256":"7bb372e6454418366a3f698ee5ff1bb4cfaf25a8ae27af7acdb7bb03a3ca0fe5","s… |
| 파생 | build | `문제.pdf` | modified | {"sha256":"a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04","s… | {"sha256":"207d85611c983e3a5de164a921a7ab74f101819037f25404e39b33037f5ecb09","s… |
| 파생 | build | `해설.html` | modified | {"sha256":"98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48","s… | {"sha256":"b1bbd7a4fc6c1dfda6c1597a62ddf9c056b9ca59c2385d5ff18dd62039068523","s… |
| 파생 | build | `해설.pdf` | modified | {"sha256":"490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b","s… | {"sha256":"94d323830196ec113b8ef03818237d24b81170d444ee1f825443dc259d018d7d","s… |
| 직접 | build | `workbook_engine/__init__.py` | modified | {"sha256":"1aeec670d896b74efdebdc353c8447de60ba72712f3de30891c00d2382229155","s… | {"sha256":"51971fe944f53b6d6be26501c8730fc99ec76bd250e966ef1c9129a5b257363c","s… |
| 직접 | build | `workbook_engine/paginator.py` | modified | {"sha256":"241dad0e1debc9ac9e28419ba6e5e942feb116c03e199704760d00a8d7cb267d","s… | {"sha256":"21a86b05605d8782e22ccf7b9ef3760efc59928d278e952a5aeec98cc3e26c00","s… |
| 직접 | build | `workbook_engine/validator.py` | modified | {"sha256":"41b0c15c3e21f124de4a92a679c125abb8ab278f663bd09f91bf68fa39af2cee","s… | {"sha256":"9a276f045506d98337bd9effd1a97fe25a89c45e20716506665d4c7fd36909b1","s… |
| 직접 | canonical | `workbooks/soccer-jersey-swap/content.json` | modified | {"sha256":"dd5dc17c3ae865e37e7597ee061e57c95ec053a23e6117d52a9e561adeebdd8b","s… | {"sha256":"62b66c27623e5db03e5b235d8dc71f5eaf381c14fa36c8a5d696f2769a202cae","s… |
| 직접 | declared | `AGENTS.md` | declared | — | — |
| 직접 | declared | `tests/test_engine.py` | declared | — | — |
| 직접 | declared | `tests/test_paginator.py` | declared | — | — |
| 직접 | declared | `tests/test_render_contract.py` | declared | — | — |
| 직접 | declared | `updates/U-20260723-005.json` | declared | — | — |
| 직접 | declared | `workbooks/chocolate/content.json` | declared | — | — |
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
| canonical | `$.files[0].sha256` | modified | "dd5dc17c3ae865e37e7597ee061e57c95ec053a23e6117d52a9e561adeebdd8b" | "62b66c27623e5db03e5b235d8dc71f5eaf381c14fa36c8a5d696f2769a202cae" |
| canonical | `$.files[0].size` | modified | 29518 | 29715 |
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
| build | `$.builtAt` | modified | "2026-07-23T23:18:23+09:00" | "2026-07-23T23:27:22+09:00" |
| build | `$.canonicalDigest` | modified | "d77138eaea6365f88f4fb98952f96a6ec70475e98f54a08bd1759ada7b107695" | "d28cd342129fee458dee97c9337ae536100916e864f2122763f5405340e11e34" |
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
| build | `$.files[13].sha256` | modified | "8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c" | "7bb372e6454418366a3f698ee5ff1bb4cfaf25a8ae27af7acdb7bb03a3ca0fe5" |
| build | `$.files[13].size` | modified | 151456 | 151720 |
| build | `$.files[14].sha256` | modified | "a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04" | "207d85611c983e3a5de164a921a7ab74f101819037f25404e39b33037f5ecb09" |
| build | `$.files[14].size` | modified | 695776 | 696357 |
| build | `$.files[15].sha256` | modified | "98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48" | "b1bbd7a4fc6c1dfda6c1597a62ddf9c056b9ca59c2385d5ff18dd62039068523" |
| build | `$.files[15].size` | modified | 164661 | 164925 |
| build | `$.files[16].sha256` | modified | "490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b" | "94d323830196ec113b8ef03818237d24b81170d444ee1f825443dc259d018d7d" |
| build | `$.files[16].size` | modified | 842774 | 843318 |
| build | `$.outputs[0].sha256` | modified | "8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c" | "7bb372e6454418366a3f698ee5ff1bb4cfaf25a8ae27af7acdb7bb03a3ca0fe5" |
| build | `$.outputs[0].size` | modified | 151456 | 151720 |
| build | `$.outputs[1].sha256` | modified | "a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04" | "207d85611c983e3a5de164a921a7ab74f101819037f25404e39b33037f5ecb09" |
| build | `$.outputs[1].size` | modified | 695776 | 696357 |
| build | `$.outputs[2].sha256` | modified | "98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48" | "b1bbd7a4fc6c1dfda6c1597a62ddf9c056b9ca59c2385d5ff18dd62039068523" |
| build | `$.outputs[2].size` | modified | 164661 | 164925 |
| build | `$.outputs[3].sha256` | modified | "490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b" | "94d323830196ec113b8ef03818237d24b81170d444ee1f825443dc259d018d7d" |
| build | `$.outputs[3].size` | modified | 842774 | 843318 |
| build | `$.pages[0].digest` | modified | "f3241a2b9fd537ec7bb45004a5fa735670b2040cd794b0496c8abad5d9a57252" | "d518176b947f5a1251793c5e9e8e7f62eb0fba611277f7049a9b632ec12d6e17" |
| build | `$.pages[0].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[0].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[0].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[0].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[0].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[0].part` | modified | "1-12" | "1-7" |
| build | `$.pages[1].digest` | modified | "645b12c0e80dba046099a021f77d65fa19798ebf64141ba00c76985867704272" | "ba9eef483916ed9f054855bb1198802e9d5f6bb6f3011d46c294c0857fac3f0c" |
| build | `$.pages[1].itemIds[0]` | modified | "s013" | "s008" |
| build | `$.pages[1].itemIds[1]` | modified | "s014" | "s009" |
| build | `$.pages[1].itemIds[2]` | added | — | "s010" |
| build | `$.pages[1].itemIds[3]` | added | — | "s011" |
| build | `$.pages[1].itemIds[4]` | added | — | "s012" |
| build | `$.pages[1].itemIds[5]` | added | — | "s013" |
| build | `$.pages[1].itemIds[6]` | added | — | "s014" |
| build | `$.pages[1].part` | modified | "13-14" | "8-14" |
| build | `$.pages[2].digest` | modified | "64546a754350ffb18b1551c6bf72d1e7bef4a0b39246f00907644e7ddd6d058c" | "d112be01b488ce11305108fe6f7987a42fdbac94c5be5034f00b40e63dc90fca" |
| build | `$.pages[3].digest` | modified | "2393b173671f29ffaf0df52400ba29879449e354a57e94084eba61697b0f9e70" | "9a44df8993037df64b7ebef8bd3d3ef0ffceef6818453fac0b1937a324b26bc9" |
| build | `$.pages[4].digest` | modified | "9db5fc0143d2fa383614eb6a8b48e01710867441f59a2cc0fbba2741a34170e3" | "2b10143d98e91d024413fac2f9e0180a72ff073abb7ca5be208c4ae4cdf57949" |
| build | `$.pages[4].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[4].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[4].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[4].part` | modified | "1-10" | "1-7" |
| build | `$.pages[5].digest` | modified | "3cda6c135bd4515ba625ffc1a4b800e757f5b74284aefa9a571c7170ab15df66" | "8acba758354c6fa1a136645f065289cc57fecaf0e389cd04fef7a23c0bf4f4b0" |
| build | `$.pages[5].itemIds[0]` | modified | "s011" | "s008" |
| build | `$.pages[5].itemIds[1]` | modified | "s012" | "s009" |
| build | `$.pages[5].itemIds[2]` | modified | "s013" | "s010" |
| build | `$.pages[5].itemIds[3]` | modified | "s014" | "s011" |
| build | `$.pages[5].itemIds[4]` | added | — | "s012" |
| build | `$.pages[5].itemIds[5]` | added | — | "s013" |
| build | `$.pages[5].itemIds[6]` | added | — | "s014" |
| build | `$.pages[5].part` | modified | "11-14" | "8-14" |
| build | `$.pages[6].digest` | modified | "17655b82c1412759485e7fac1c557fc7f11a8cfa2d80b069633619afe94f9723" | "e38411cdd1a61d04e69aa0b9bf0cbe193c22fbf658f9e9f57ce2ebcf9c64704b" |
| build | `$.pages[7].digest` | modified | "51c2fec1813132d01f4533c637c8f52b8816a9e6b7afdb399cd398ce488e634a" | "d189ed3412a831c15d724000e7cd94f4d3764396fc3269b7d01284f43cad6054" |
| build | `$.pages[9].digest` | modified | "7293c0b2c9e40e03112354e675f7f0fcf0c46b3aa96064b812efba76c2522e2b" | "f167e1c31d9b9b2ced10e14a91795fee37008c2881e836dceffa00fad384ba89" |
| build | `$.pages[9].itemIds[5]` | removed | "s006" | — |
| build | `$.pages[9].part` | modified | "1-6" | "1-5" |
| build | `$.pages[10].digest` | modified | "57d02031c0e78be627d84b15c252b83e7bcd767e46c7b75ecf194e342772798f" | "562d52a6c87d8315e024b3e2806d33a9acc7678f0814280e323daff96235d24e" |
| build | `$.pages[10].itemIds[0]` | modified | "s007" | "s006" |
| build | `$.pages[10].itemIds[1]` | modified | "s008" | "s007" |
| build | `$.pages[10].itemIds[2]` | modified | "s009" | "s008" |
| build | `$.pages[10].itemIds[3]` | modified | "s010" | "s009" |
| build | `$.pages[10].itemIds[4]` | modified | "s011" | "s010" |
| build | `$.pages[10].itemIds[5]` | removed | "s012" | — |
| build | `$.pages[10].part` | modified | "7-12" | "6-10" |
| build | `$.pages[11].digest` | modified | "17d9cc873e987dd01ae0e88acffef1afaa70f5f15223c142cae68f0697dff64a" | "f8de3c8f38939ff2d126191f3a5fbedb818449d8823878ffc5e71d27cbc79d93" |
| build | `$.pages[11].itemIds[0]` | modified | "s013" | "s011" |
| build | `$.pages[11].itemIds[1]` | modified | "s014" | "s012" |
| build | `$.pages[11].itemIds[2]` | added | — | "s013" |
| build | `$.pages[11].itemIds[3]` | added | — | "s014" |
| build | `$.pages[11].part` | modified | "13-14" | "11-14" |
| build | `$.pages[13].digest` | modified | "42ddc812b5ad2412a2312883d63a7ee3935dc6df44736998aaf0e20819c199b3" | "c3ec53d187128f9238869d97dd3c2796d2b63e153d45eb901b22f4c20c74e070" |
| build | `$.pages[13].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[13].part` | modified | "1-8" | "1-7" |
| build | `$.pages[14].digest` | modified | "8ef596f8ef1ee40821decaa3c9f1eab8590a8154e9d518889a5a145f08e539dd" | "16d7594694603604f82e39f635f34da252877ab98f81cb5d2b6335b2a5616d55" |
| build | `$.pages[14].itemIds[0]` | modified | "s009" | "s008" |
| build | `$.pages[14].itemIds[1]` | modified | "s010" | "s009" |
| build | `$.pages[14].itemIds[2]` | modified | "s011" | "s010" |
| build | `$.pages[14].itemIds[3]` | modified | "s012" | "s011" |
| build | `$.pages[14].itemIds[4]` | modified | "s013" | "s012" |
| build | `$.pages[14].itemIds[5]` | modified | "s014" | "s013" |
| build | `$.pages[14].itemIds[6]` | added | — | "s014" |
| build | `$.pages[14].part` | modified | "9-14" | "8-14" |
| build | `$.pages[15].digest` | modified | "f3241a2b9fd537ec7bb45004a5fa735670b2040cd794b0496c8abad5d9a57252" | "d518176b947f5a1251793c5e9e8e7f62eb0fba611277f7049a9b632ec12d6e17" |
| build | `$.pages[15].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[15].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[15].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[15].itemIds[10]` | removed | "s011" | — |
| build | `$.pages[15].itemIds[11]` | removed | "s012" | — |
| build | `$.pages[15].part` | modified | "1-12" | "1-7" |
| build | `$.pages[16].digest` | modified | "645b12c0e80dba046099a021f77d65fa19798ebf64141ba00c76985867704272" | "ba9eef483916ed9f054855bb1198802e9d5f6bb6f3011d46c294c0857fac3f0c" |
| build | `$.pages[16].itemIds[0]` | modified | "s013" | "s008" |
| build | `$.pages[16].itemIds[1]` | modified | "s014" | "s009" |
| build | `$.pages[16].itemIds[2]` | added | — | "s010" |
| build | `$.pages[16].itemIds[3]` | added | — | "s011" |
| build | `$.pages[16].itemIds[4]` | added | — | "s012" |
| build | `$.pages[16].itemIds[5]` | added | — | "s013" |
| build | `$.pages[16].itemIds[6]` | added | — | "s014" |
| build | `$.pages[16].part` | modified | "13-14" | "8-14" |
| build | `$.pages[17].digest` | modified | "1b2da53733fade816c7414fe1885f24bc29697f583515a985f4258a7b2539e00" | "dd54eddf7aa13c3a7b65e11bd63bca46fe2240b77f2cd6614d98f17750788304" |
| build | `$.pages[18].digest` | modified | "c901c83f810adec5d3de8465cb3edf13353c3ef51d657a5673bd367d889a8e31" | "b4b3f271c380905e8f88f89a6ef3fd7e417b452d15d5425ee94777623d30cc22" |
| build | `$.pages[19].digest` | modified | "5f8f1a4747ea13bfb96b5b10620ce3e7f8aa59b78da1ec2512ad1dafb3d20e11" | "2b841568efd14230958758e1c190af35f35fee7424c12a82f0892ec574e99256" |
| build | `$.pages[19].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[19].itemIds[8]` | removed | "s009" | — |
| build | `$.pages[19].itemIds[9]` | removed | "s010" | — |
| build | `$.pages[19].part` | modified | "1-10" | "1-7" |
| build | `$.pages[20].digest` | modified | "c58e3a5036d3ff12b40073c34c944cca8898fc747bad28fd889bb4024b607898" | "0f2b26fa35001bc4ea9a6ab0d4f42f21ed8aefaa78e1921c1202e37f0c007de7" |
| build | `$.pages[20].itemIds[0]` | modified | "s011" | "s008" |
| build | `$.pages[20].itemIds[1]` | modified | "s012" | "s009" |
| build | `$.pages[20].itemIds[2]` | modified | "s013" | "s010" |
| build | `$.pages[20].itemIds[3]` | modified | "s014" | "s011" |
| build | `$.pages[20].itemIds[4]` | added | — | "s012" |
| build | `$.pages[20].itemIds[5]` | added | — | "s013" |
| build | `$.pages[20].itemIds[6]` | added | — | "s014" |
| build | `$.pages[20].part` | modified | "11-14" | "8-14" |
| build | `$.pages[21].digest` | modified | "3ee2f4f5ce49663aa10b85dbe7b1c7a532e4f8108ad7a5c00a57ad35fdb7970f" | "10fe0cc38e61c5ee7c250de97d9e4c055d52f84d0349b4d51e8e4fe9be2cb3a6" |
| build | `$.pages[22].digest` | modified | "2d0586f1f0d24173cc233f950baf7bd65c4d9dbfa40ef52508a4e11f2a151755" | "95ae5b4177bfafec5a21ce0beeae2c358de1b35435b3ec19e4df80091a4de7de" |
| build | `$.pages[24].digest` | modified | "4de5ef796cb2072fce72ad90f5a8fba5203df44545e817527ac67393a8e0a598" | "2f084095eebd016a3594644efe38d0e915fa3f5a231da642d7d676ad5267b340" |
| build | `$.pages[24].itemIds[5]` | removed | "s006" | — |
| build | `$.pages[24].part` | modified | "1-6" | "1-5" |
| build | `$.pages[25].digest` | modified | "1a318f5f0610e0bce87ac7685f8151fa6953f0ab931d13913144e9480cec51e6" | "bbd17d0243f00051fdfc83a918ca5715fd4370c75f00754731ef807bf1259376" |
| build | `$.pages[25].itemIds[0]` | modified | "s007" | "s006" |
| build | `$.pages[25].itemIds[1]` | modified | "s008" | "s007" |
| build | `$.pages[25].itemIds[2]` | modified | "s009" | "s008" |
| build | `$.pages[25].itemIds[3]` | modified | "s010" | "s009" |
| build | `$.pages[25].itemIds[4]` | modified | "s011" | "s010" |
| build | `$.pages[25].itemIds[5]` | removed | "s012" | — |
| build | `$.pages[25].part` | modified | "7-12" | "6-10" |
| build | `$.pages[26].digest` | modified | "aaef11e669a752accaeb20378db02386b02eaf2e799c31d5d298edcfc78c8ab4" | "4ea965c81ab9b404733327b40316574ecb4c0ac4966b33571323d2280a33fc06" |
| build | `$.pages[26].itemIds[0]` | modified | "s013" | "s011" |
| build | `$.pages[26].itemIds[1]` | modified | "s014" | "s012" |
| build | `$.pages[26].itemIds[2]` | added | — | "s013" |
| build | `$.pages[26].itemIds[3]` | added | — | "s014" |
| build | `$.pages[26].part` | modified | "13-14" | "11-14" |
| build | `$.pages[28].digest` | modified | "5fcea9a81a383283b9f857dc148606be7390bb3e1e0a8efd8bb31a93426759d6" | "f6c4a4ccb5d03c7a90f44b78e1f66a09c9b6927f4cfca34d3d78de17d543350a" |
| build | `$.pages[28].itemIds[7]` | removed | "s008" | — |
| build | `$.pages[28].part` | modified | "1-8" | "1-7" |
| build | `$.pages[29].digest` | modified | "082601e25661c478fb92f53ae7b6437b54c96030a1f1c810d5e9009b2c1d443d" | "95aedd570e1e1fc176cab604b80d50d4fe66188b7e810ac99e7e28bf798a8484" |
| build | `$.pages[29].itemIds[0]` | modified | "s009" | "s008" |
| build | `$.pages[29].itemIds[1]` | modified | "s010" | "s009" |
| build | `$.pages[29].itemIds[2]` | modified | "s011" | "s010" |
| build | `$.pages[29].itemIds[3]` | modified | "s012" | "s011" |
| build | `$.pages[29].itemIds[4]` | modified | "s013" | "s012" |
| build | `$.pages[29].itemIds[5]` | modified | "s014" | "s013" |
| build | `$.pages[29].itemIds[6]` | added | — | "s014" |
| build | `$.pages[29].part` | modified | "9-14" | "8-14" |
| build | `$.specVersion` | modified | "1.0.1" | "1.0.2" |
| build | `$.visualReview.notes` | modified | "학생용·해설용 15쪽 contact sheet에서 1·2·5·8·9·10·13·14·15페이지를 확인함. 8단계 조각형 정답 밑줄이 제거되고 학생용 긴 작성선과 해설용 완성 문장만 유지됨. 잘림·겹침·번호 오류·… | "학생용·해설용 15쪽 contact sheet에서 같은 단계 문항이 7/7 등 균등 배치된 것을 확인함. 단독 꼬리 페이지, 잘림·겹침·번호 오류·학생용 정답 누출·교정 색상 오류 없음." |
| build | `$.visualReview.reviewedAt` | modified | "2026-07-23T23:19:10+09:00" | "2026-07-23T23:28:11+09:00" |

## 파생 영향 (파생 변경)

### JSON 경로

변경 없음

### 단계·문항

| 항목 | 영향 ID |
|---|---|
| 단계 | 1, 2, 3, 4, 5, 6, 8, 10 |
| 문항 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |

### 페이지

| 페이지 | 변경 | 단계 | 문항 |
|---|---|---|---|
| answer:soccer-jersey-swap-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| answer:soccer-jersey-swap-p02 | modified | 1 | s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p04 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p05 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| answer:soccer-jersey-swap-p06 | modified | 4 | s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p07 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p08 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p10 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| answer:soccer-jersey-swap-p11 | modified | 8 | s006, s007, s008, s009, s010, s011, s012 |
| answer:soccer-jersey-swap-p12 | modified | 8 | s011, s012, s013, s014 |
| answer:soccer-jersey-swap-p14 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| answer:soccer-jersey-swap-p15 | modified | 10 | s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p01 | modified | 1 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012 |
| student:soccer-jersey-swap-p02 | modified | 1 | s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p03 | modified | 2 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p04 | modified | 3 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p05 | modified | 4 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010 |
| student:soccer-jersey-swap-p06 | modified | 4 | s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p07 | modified | 5 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p08 | modified | 6 | s001, s002, s003, s004, s005, s006, s007, s008, s009, s010, s011, s012, s013, s014 |
| student:soccer-jersey-swap-p10 | modified | 8 | s001, s002, s003, s004, s005, s006 |
| student:soccer-jersey-swap-p11 | modified | 8 | s006, s007, s008, s009, s010, s011, s012 |
| student:soccer-jersey-swap-p12 | modified | 8 | s011, s012, s013, s014 |
| student:soccer-jersey-swap-p14 | modified | 10 | s001, s002, s003, s004, s005, s006, s007, s008 |
| student:soccer-jersey-swap-p15 | modified | 10 | s008, s009, s010, s011, s012, s013, s014 |

## 출력 변화

| 출력 | 변경 | 이전 | 이후 |
|---|---|---|---|
| `문제.html` | modified | {"path":"문제.html","sha256":"8e00e649ed379517f658bba404484a96c659940a1b0a6d618977244e8a0e537c","size":151456} | {"path":"문제.html","sha256":"7bb372e6454418366a3f698ee5ff1bb4cfaf25a8ae27af7acdb7bb03a3ca0fe5","size":151720} |
| `문제.pdf` | modified | {"path":"문제.pdf","sha256":"a26f11496b3e2c398695d3c77b7431305d7c130a3ecfcb61912f3f5f05f37e04","size":695776} | {"path":"문제.pdf","sha256":"207d85611c983e3a5de164a921a7ab74f101819037f25404e39b33037f5ecb09","size":696357} |
| `해설.html` | modified | {"path":"해설.html","sha256":"98c0c682765043f85f7c6608022b0c1a9f319dd01857722767c63c06c6760c48","size":164661} | {"path":"해설.html","sha256":"b1bbd7a4fc6c1dfda6c1597a62ddf9c056b9ca59c2385d5ff18dd62039068523","size":164925} |
| `해설.pdf` | modified | {"path":"해설.pdf","sha256":"490d29c54672a32b80baeecebb142f45134f361b4a7e033e11124ceeb7b1437b","size":842774} | {"path":"해설.pdf","sha256":"94d323830196ec113b8ef03818237d24b81170d444ee1f825443dc259d018d7d","size":843318} |

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

- 직접 JSON 경로: 181
- 파생 JSON 경로: 0
- 변경·선언 파일: 17
- 영향 페이지: 26
- 변경 출력: 4
