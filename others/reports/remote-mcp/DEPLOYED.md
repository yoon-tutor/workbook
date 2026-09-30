# 실제 원격 배포·실행 확인

- 배포 완료: GCP `yoontutor-507902`, `asia-northeast3`, `workbook-runtime`.
- 활성 revision: `workbook-runtime-00002-b2z`, 트래픽 100%.
- 사용 중인 MCP URL: https://workbook-runtime-972256519381.asia-northeast3.run.app/mcp
- 인증: 잘못된 Bearer 토큰은 HTTP 401로 차단. 전용 서비스 계정에는 해당 인증 secret 읽기 권한만 부여했다. 토큰은 프로젝트 `others/.env`와 Secret Manager에 저장하며 일회용 업로드 파일은 삭제했다.
- 실행 버전: `3c517285402fd434a00b0a39c3559c85e00ec179762de3bdf24c303f2d2bb822`. 기존 local lock을 변경하지 않았다.

## 실제 실행과 결과

배포된 HTTPS MCP를 통해 guide → sync → validate → prepare → status → 시각 검수 → 로컬 publish를 실행했다. 서버는 실행 패키지만 제공하며 이 실행에서 canonical 및 PDF를 서버로 전송하지 않았다.

결과 폴더: `outputs/mcp_chocolate_remote_20260922/`.

- `문제.html`, `문제.pdf`, `해설.html`, `해설.pdf` 생성 완료.
- 학생용·해설용 PDF 각각 22쪽.
- 학생 DOM 정답 0개, 해설 정답 255개.
- 공통 target 260개, 작성 박스 72개, 작성 줄 90개, 비작성 정답 슬롯 188개 정렬 검사 통과.
- 기존 0.75px 허용치, overflow·겹침·잘림 및 PDF 쪽수 검사를 그대로 적용했다.
- 실제 생성 학생용·해설용 contact sheet를 직접 검수했다. 2·3단계 빈칸, 4·8·10단계 작성형, 5·6단계 문제 단서와 빨간 해설 답을 확인했다. 대표 이미지에서 잘림·겹침·푸터 침범을 발견하지 못했다. 전체 의미 콘텐츠를 새로 감사한 것은 아니다.
- 두 HTML과 두 compiled JSON은 앞서 로컬에서 검증한 결과와 바이트 단위로 동일하다.
- 최종 저장한 네 파일은 실제 검수한 빌드 파일과 바이트 단위로 동일하다.

기존 보고서까지 보존하기 위해 이번 샘플의 로컬 릴리스 상태와 보고서는 `others/.build/deployed-publication-20260922/`에 따로 저장했다. 이 작업공간의 outputs는 기존 로컬 outputs 폴더를 가리킨다. 웹사이트 공개 게시가 아니다.

## 원본 보존

개편 전 4,584개 파일을 배포·실행 후 다시 검사했다. 허용된 AGENTS 실행 안내와 개편 계획 문서 외에 변경이 없다. 기존 공개 HTML/PDF 64개, 정본, 엔진, 템플릿 및 기존 보고서는 모두 보존했다. 새 결과 네 파일만 새 폴더에 추가했다.

## 실배포에서 수정한 문제

Windows의 경로 정렬과 Linux의 대소문자 정렬 차이 때문에 파일 내용은 같지만 패키지 manifest 순서와 해시가 달랐다. 서버 배포 코드에 명시적인 대소문자 무시 정렬을 적용하고 두 OS 경로 유형의 회귀검사를 추가했다. 실행 엔진 파일·템플릿·기존 runtime lock은 변경하지 않았다. 실제 운영 서버에서도 기존 runtime ID와의 일치를 확인했다.

최종 서버 배포 소스는 `others/server-dist/20260922-linux-order/`다.

## 증거 파일

- `deployment.json`: 활성 revision 및 트래픽.
- `production-checks.json`: 실제 HTTPS 버전·인증 검사.
- `deployed-smoke.json`: 실제 thin CLI 실행과 자동 QA 결과.
- `deployed-visual-review.json`: 직접 시각 검수 기록과 QA 요약.
- `deployed-byte-comparison.json`: HTML/IR 동일성.
- `deployed-publish.json`: 새 로컬 결과 경로와 네 파일 복사 검증.
- `preservation-after-deployment.json`: 기존 파일 전수 보존 확인.
