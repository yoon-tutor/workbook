# Cloud Run 서비스 이름 전환 (2026-10-06)

사용자 요청에 따라 `workbook-runtime-stage9`를 `workbook-maker`로 전환했다. 새 이름으로 같은 운영 이미지를 배포하고 검증 후 기존 서비스와 모든 하위 revision을 삭제했다.

- 프로젝트: `yoontutor-507902`, 지역: `asia-northeast3`
- 서비스: `workbook-maker`, revision: `workbook-maker-00001-9vv`, Ready=True, 트래픽 100%
- MCP: `https://workbook-maker-972256519381.asia-northeast3.run.app/mcp`
- 이미지 digest: `sha256:eb2cd951d518abdc9729cddafd3b3c8cf9d4ea6ad36698f27a1ccb6561687e46`
- 런타임 ID: `8a526dec4e625aa46ecf89f5b6ebee7eca7473325d477b3029abd50e2fb5d761`, directApiVersion=2
- 기존 서비스 계정, Secret Manager 참조, 저장 버킷, CPU·메모리·동시성·시간 제한·시작 검사를 유지했다. 공개 산출물 origin만 새 서비스 주소로 변경했다.
- 기존 이미지 저장소와 저장 버킷은 새 서비스도 사용하므로 보존했다.

개발용 `others/.env`, 공용 배포판 `.env`와 `.codex/config.toml`, `.env.example`, 두 배포 생성 스크립트와 연결 안내를 갱신했다. 토큰 값과 runtime lock은 유지했다. 배포판 SHA256SUMS의 설정 파일 해시를 갱신하고 목록 전체를 검증했다.

기존 서비스 삭제 후 두 클라이언트의 MCP 인증 연결, 고정 runtime ID, 필수 작성·릴리스 도구를 확인했다. 기존 공개 릴리스 `8205cbf7b6ee414d9ecf2aa726a5b5b5`의 산출물 네 파일을 새 origin에서 실제 내려받고 서버 기록의 크기와 SHA-256이 일치함을 검증했다.

| 파일 | 크기(bytes) | SHA-256 |
|---|---:|---|
| 문제.html | 213255 | `32e1bb9349f2d0a9cceef5617e0ba8ba6ec3401bcf9b401873d3840f4d28b0bf` |
| 문제.pdf | 918770 | `a9b0ae5d44dfcd119c9e12d84d44c03fd78d8a7b9b3ce85e5411f92f08d16b79` |
| 해설.html | 234745 | `7482f065eef9f4bae90906159a7ec1a74368a433b7794e477478992bbf384200` |
| 해설.pdf | 1003719 | `3dd4bf472067baf42d651459a974fb958ffdd7218467a222181edd854467117a` |

최종 Cloud Run 서비스 목록은 `workbook-maker`, `vocabulary-maker`, `toefl-maker-private`다. 기존 주소로 연결하는 외부 배포본은 새 MCP 주소로 변경한 뒤 새 Codex 작업에서 연결해야 한다. 기존 공개 파일은 저장 버킷에 보존되어 `workbook_get_artifacts`로 새 다운로드 링크를 받을 수 있다.
