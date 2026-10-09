# stage9 직접 작성 도구 배포

- 서비스: `workbook-runtime-stage9`, 지역: `asia-northeast3`
- 활성 revision: `workbook-runtime-stage9-00003-jad`, 트래픽 100%
- 런타임 ID: `0ea07fa4c92ae2c9cc07be3030e97e2d60999fd9f9129c604efb4900baebd1df` (기존 lock과 일치)
- 배포 소스: `server-dist/20260927-direct-authoring/`; 직전 배포 소스와 달라진 파일은 `workbook_mcp/server.py` 하나

로컬 인증 HTTP MCP 통합 테스트 15개가 통과했다. 새 revision은 트래픽 없이 먼저 배포해 실제 `tools/list`에서 `workbook_authoring_verify`, `workbook_authoring_expand`를 확인하고, guidance의 `directApiVersion: 1` 및 런타임 ID 일치를 검증한 뒤 100%로 전환했다. 활성 URL에서도 두 도구 등록, 빈 합성 packet 거부, 잘못된 Bearer 토큰의 HTTP 401을 확인했다. 원본 PDF나 작성 packet은 이 배포 검증에 전송하지 않았다.

원격 MCP에는 PDF 생성·브라우저 QA·시각 검수·publish 도구가 없다. 따라서 작성 packet 검증·정본 확장은 가능하지만 PDF 릴리스 완료는 아직 불가능하다.
