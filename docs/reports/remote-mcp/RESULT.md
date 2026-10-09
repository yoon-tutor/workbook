# 원격 MCP / 로컬 실행공간 개편 검증

상태: 실제 HTTPS MCP 배포, 생성, 자동·시각 검수 및 새 결과 저장까지 완료. [실배포 확인](DEPLOYED.md).

## 변경한 실행 구조

`others/AGENTS.md → .agents/skills/workbook-release/SKILL.md → scripts/run.py → 인증된 MCP → runtime.lock.json 검증 → 로컬 .runtime/<SHA256> 실행`

원격 서버가 고정 버전 엔진·템플릿·규칙·작성/릴리스 스크립트를 제공한다. 로컬은 원문, canonical, 브라우저, PDF, QA, 작업 상태, 보고서, 공개 결과를 보관한다. 일반 실행은 canonical을 원격에 전송하지 않는다. HTTPS 설정, 인증, lock 확인, 다운로드·캐시 전수 해시 검사, 경로 검증을 실패 시 중단하도록 구현했다. 원격 장애 시 개발 엔진으로 자동 대체하지 않는다.

기존 `workbook_engine`의 13개 Python 파일과 템플릿·정본·규칙은 수정하지 않았다. 별도 runtime 어댑터가 입출력 경로 및 Windows Chrome 검색·프로세스 종료만 연결한다. 기존 manifest 상대 경로와 입력 해시도 동일하게 유지한다.

## 기존 자료와 결과 보존

- 개편 전 파일 4,584개를 SHA-256으로 검사했다. 의도한 `others/AGENTS.md` 실행 안내와 개편 계획 문서 외에 기존 파일 변경이 없다.
- 기존 공개 HTML/PDF **64개 전부 바이트 동일**. 기존 출력 폴더를 덮어쓰거나 삭제하지 않았다.
- 기존 15개 canonical의 학생용·해설용 **30종 IR 및 30종 HTML 전부 바이트 동일**. 인증된 HTTP MCP에서 다운로드한 런타임으로 비교했다.
- 기존 입력 해시와 엔진·템플릿 manifest 경로가 원격 런타임에서도 동일함을 검사했다.

근거: `original-files.json`, `preservation.json`, `render-baseline.json`, `parity-results.json`.

## 테스트와 실제 생성

| 검사 | 결과 |
|---|---|
| 기존 엔진 테스트, 원래 Windows 실행 | 38개 중 브라우저 탐색 오류 1개, 제외 2개. 개편 전 환경 문제를 그대로 기록 |
| 실제 다운로드한 최종 런타임으로 기존 테스트 | 38개 중 37개 통과, macOS 파일 속성 검사 1개 제외 |
| HTTP MCP·인증·변조·캐시·경로·출력 비교 | 13개 통과 |
| 프로젝트 스킬 형식 검사 | 통과 |
| 실제 thin CLI: guide → sync → validate → prepare → status | 통과 |
| 검수한 사본의 격리 publish | 네 파일 바이트 동일, 상세 보고서·인덱스·manifest 생성 확인 |

`chocolate_reading` 실제 생성: 학생용 22쪽, 해설용 22쪽. 학생 DOM 정답 0개, 해설 정답 255개. 공통 target 260개, 작성 박스 72개, 작성 줄 90개, 비작성 정답 슬롯 188개 정렬 검사 통과. 기존 overflow·잘림·겹침·0.75px 허용치 및 PDF 쪽수 검사를 약화하지 않았다.

학생용·해설용 contact sheet를 직접 확인했다. 2·3단계 빈칸과 4·8·10단계 작성형을 포함한다. 최종 런타임의 contact sheet 두 장은 직접 본 이미지와 바이트 단위로 동일했다. 이번 검토는 대표 이미지의 레이아웃 확인이며 전체 지문의 새로운 의미 품질 감사는 아니다.

실제 생성 파일은 `others/.build/releases/chocolate_reading/20260922-003316-93e71bb4/`에 보관했다. 사용자 공개 outputs에는 새 시험 결과를 게시하지 않았다. publish 검증은 자동 삭제되는 별도 임시 작업공간에서만 수행했다.

근거: `legacy-tests.log`, `legacy-downloaded-tests.log`, `mcp-tests.log`, `local-smoke.json`, `visual-review.json`, `publish-integration.json`.

## 실제 원격 배포 완료

사용자 승인 후 실제 배포와 실행을 완료했다. 활성 revision은 workbook-runtime-00002-b2z이며, 새 결과는 outputs/mcp_chocolate_remote_20260922/에 있다. 배포 버전, 인증 확인, 시각 검수, 원본 보존의 최신 증거는 [실배포 확인](DEPLOYED.md)을 참조한다.
