# 9단계 문단 배열 작성 정책 배포

- 서비스: `workbook-runtime-stage9`, revision `workbook-runtime-stage9-00002-g8f`, 트래픽 100%
- URL: `https://workbook-runtime-stage9-972256519381.asia-northeast3.run.app/mcp`
- 고정 런타임 ID: `0ea07fa4c92ae2c9cc07be3030e97e2d60999fd9f9129c604efb4900baebd1df`
- 기존 `workbook-runtime-multipassage` 서비스와 기존 공개 PDF는 유지했다.

`guide`의 9단계 작성 규칙과 서버에서 배포되는 `semantic-rubric.md`·`authoring-pipeline.md`를 수정했다. 새 packet의 `authoring verify`와 `expand`는 선택지 표시 A→B→C, 지문 전체 블록 포함, 비자명한 정답, 묶음 문항의 가능한 최대 정답 순열 다양성을 검사한다. 과거 canonical의 `validate`·컴파일은 변경하지 않는다.

## 검증

- 엔진 테스트 41개 통과(1개 플랫폼별 skip), MCP HTTP 통합 테스트 15개 통과.
- 실제 서비스의 `guide`·`sync`, 올바른 다섯 문항 `authoring verify`, 33번 `validate` 통과.
- 실제 서비스에서 C→B→A로 인쇄되는 선택지, 이미 A→B→C인 정답, 반복 정답, 고정 앞문장으로 부분 배열하는 packet을 모두 거부했다.
- 새 사용자 ZIP을 임시 폴더에서 설치하고 `guide`·`sync`·`validate`·`prepare`·`status` 실행: 22쪽 예제, 학생 정답 노출 0, 이전 HTML과 바이트 동일.
- 개편 전 공개 파일 65개와 수정 전 고2 30~34번 공개 파일 20개의 SHA-256을 각각 기존 기록과 대조해 모두 일치했다.

최종 사용자 배포판은 `distribution/workbook-maker-stage9-final-20260926.zip`이다. 이 ZIP에는 토큰이 없으며, 현재 테스트용 `distribution/workbook-maker-20260926` 폴더의 `.env`에는 기존 토큰 값을 보존한 채 URL과 lock만 갱신했다.
