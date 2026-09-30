---
name: workbook-release
description: 원격 MCP의 고정 버전 실행 스크립트로 이 프로젝트의 영어 10단계 워크북을 로컬 생성, 검수, 릴리스한다. 기존 정본과 출력 계약을 보존한다.
---

작업공간의 `others/`를 기준으로 실행한다. 진입점은 `scripts/run.py`다. 프로젝트 `others/.env`의 원격 MCP에 연결하고 `runtime.lock.json`과 일치하는 스크립트만 실행한다. 엔진·규칙·템플릿 개발 원본은 일반 생성 작업에서 수정하지 않는다.

1. `python -X utf8 scripts/run.py guide`로 원격 작성 지침과 스키마를 확인한다.
2. 새 지문은 guide의 authoring pipeline에 맞추어 authoring packet을 작성한다. `authoring verify <packet>` 후 `authoring expand <packet> --output workbooks/<이름>/content.json`으로 정본을 만든다. 기존 정본을 packet으로 다시 만들어 덮어쓰지 않는다.
   9단계는 지문 전체를 블록으로 배열한다. 선택지 표시는 위에서부터 A·B·C, 정답은 원문 복원 순서로 작성하고 묶음 문항의 정답 순열을 분산한다. `displayOrder`를 뒤집어 선택지 글자 자체를 C·B·A로 인쇄하지 않는다.
3. `validate workbooks/<이름>/content.json`으로 검증한다.
4. `prepare workbooks/<이름>/content.json --update updates/<ID>.json`으로 private staging에 생성한다.
5. 반환된 학생용·해설용 contact sheet에서 2·3단계 빈칸 및 4·8·10단계 작성형을 포함해 직접 시각 검수한다. 자동 검증과 시각 검수는 별개다.
6. 검수 통과 시 `publish <build-dir> --reviewer Codex --notes "실제 검수 내용"`을 실행한다. 실패한 QA, 미실행 브라우저, 미검수 이미지는 통과로 표시하지 않는다.

위 명령은 모두 `python -X utf8 scripts/run.py` 뒤에 붙인다. `status <canonical> [--build-dir <dir>]`로 재개 상태를 확인한다. publish는 원래 엔진의 새 버전 폴더 할당과 네 파일 계약을 유지한다.

원격이 바뀌어 lock과 다르면 중단하고 배포 버전과 검증 결과를 확인한다. lock을 자동으로 새 값으로 덮어쓰지 않는다. 네트워크 실패를 로컬 개발 엔진으로 대체하지 않는다.

설정·운영 경로는 [MCP 사용법](../../../docs/remote-mcp-usage.md), 출력·검수 계약은 [AGENTS.md](../../../AGENTS.md)에 있다.
