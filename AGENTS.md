# 워크북 제작기 개발 지침

이 파일은 **개발자용**이다. Codex는 이 파일을, Claude Code는 `CLAUDE.md`를 통해 같은 내용을 읽는다. 사용자에게 배포되는 지침은 `client/AGENTS.md`이며 이 파일의 내용은 배포본에 들어가지 않는다. 공통 규칙은 `docs/STANDARD.md`를 따르고 여기서 반복하지 않는다.

## 구조

- `server/`: MCP 서버(`workbook_mcp/`), 엔진(`workbook_engine/`), packet 확장(`workbook_authoring/`), 공통 런타임 복사본(`shared_mcp_runtime/`), 규격(`config/`), 스키마(`schemas/`), 서버가 제공하는 작성·품질 기준(`docs/`), 로고(`assets/`), 테스트, 스크립트, `service.json`
- `content/`: 개발자 정본 콘텐츠. `workbooks/<이름>/content.json`, `updates/U-*.json`, `reports/updates/`(변경 보고서), `reports/manifests/`(워크북별 릴리스 이력)
- `client/`: 사용자 배포본 원본 (`AGENTS.md`, `.agents/skills/workbook-maker/`, `examples/`)
- `outputs/`: 지금까지 공개한 워크북 결과 (보존, 추적)
- `docs/`: 표준 복사본, 운영(`OPERATIONS.md`), 콘텐츠·릴리스 규칙(`RELEASE_RULES.md`), 콘텐츠 변경 이력, 보고서(`reports/`)
- `.build/`(git 제외): 작성 중인 authoring packet, 서명 자료, 릴리스 staging

## 지침 경계

- 제작 규칙·검증·렌더링·PDF는 서버가 담당한다. 사용자 에이전트는 `workbook_get_guidance`가 주는 `server/docs/`·`server/config/`·`server/schemas/` 내용만 본다.
- `client/` 안의 문서에는 서버 내부 구조, 개발 경로, 검증 임계값, DB·배포 정보, 키를 쓰지 않는다. 사용자 문서는 `client/`의 실제 파일을 직접 고친다.
- `server/shared_mcp_runtime/`, `server/scripts/`의 공통 스크립트(`deploy.py`, `build_release.py`, `sandbox_client.py`, `audit_client.py`, `standard_tools.py`), `server/tests/test_standard_conformance.py`, 배포본의 `mcp_client.py`, `docs/STANDARD.md`는 `_standard` 저장소의 복사본이다. 직접 고치지 않고 `_standard`에서 고친 뒤 `python ../../_standard/sync.py .`로 반영한다.

## 배포본 테스트

`client/` 안에서 Codex를 직접 열지 않는다. 이 파일이 함께 적용되어 사용자 환경과 달라진다. 저장소 밖 복사본에서 테스트한다.

```bash
python server/scripts/sandbox_client.py --force
python server/scripts/smoke_live.py
```

기본 위치는 `~/agent-sandbox/workbook-maker/`이다. 그 폴더를 Codex로 열어 사용자처럼 작업한다.

## 개발 검증

```bash
python -m pip install -r server/requirements.txt
python -X utf8 -m unittest discover -s server/tests -v
python server/scripts/audit_client.py
python ../../_standard/sync.py . --check
python -X utf8 server/scripts/local_engine.py engine validate workbooks/<이름>/content.json
```

실제 PDF 경로 테스트에는 Chrome/Chromium이 필요하다(없으면 해당 테스트만 건너뛴다). 테스트는 메모리 인증 저장소와 임시 로컬 릴리스 저장소만 쓰며 운영 키·DB·버킷을 쓰지 않는다. `local_engine.py`는 `content/`를 작업공간으로 엔진을 실행하는 개발용 도구이며 publish는 하지 않는다.

## 배포

```bash
python server/scripts/deploy.py build
python server/scripts/deploy.py deploy
python server/scripts/deploy.py smoke
python server/scripts/build_release.py --user <이름> --key-file <키 파일>
```

설정은 `server/service.json`, 결과는 `server/deploy-state.json`, 버킷·서명 비밀·운영 이력은 `docs/OPERATIONS.md`에 둔다. 버전은 `VERSION`과 `CHANGELOG.md`로 관리한다.

## 비밀값

`.env` 파일, `.build/deployment/`, 키 파일의 값을 출력하거나 문서·커밋·명령 인수에 복사하지 않는다.

## 커밋·PR 규칙

**커밋 단위**
- 한 커밋에는 목적 하나(기능 추가, 버그 수정, 리팩터링, 문서, 배포 설정 중 하나)만 담는다.
- 테스트(`python -X utf8 -m unittest discover -s server/tests -v`), `server/scripts/audit_client.py`, `python ../_standard/sync.py . --check`(워크북은 `../../_standard`)가 통과한 상태로만 커밋한다.
- 공통 자산을 바꿀 때는 `_standard`를 먼저 커밋하고, 각 서비스 저장소에 `chore(standard): 표준 <버전> 동기화` 커밋을 따로 만든다.
- 커밋하지 않는 것: `.env`, 키 파일, `releases/`, `.build/`, `.work/`, 학생 원본 자료, 캐시·로그. 커밋 전에 `git status`와 staged 파일 목록을 확인한다.

**커밋 메시지**
```text
<type>(<scope>): <한국어 요약, 50자 이내>

<무엇을 왜 바꿨는지>

검증: <실행한 테스트·감사·운영 점검과 결과>
배포 영향: <서버 재배포 필요 여부, 사용자 배포본 교체 필요 여부>
```
- type: `feat` 기능, `fix` 수정, `refactor` 구조 변경, `docs` 문서, `test` 테스트, `chore` 설정·정리·동기화, `deploy` 배포 설정
- scope: `server`, `client`, `standard`, `docs`, `deploy`, `content` 중 하나 또는 생략
- 사용자 배포본과의 호환이 깨지면 꼬리말에 `BREAKING CHANGE: <내용>`을 쓰고, `VERSION`의 MAJOR를 올리고, `CHANGELOG.md`를 같은 커밋에서 갱신한다.
- AI가 만든 커밋은 꼬리말에 `Co-Authored-By:` 줄을 남긴다.

**커밋 제안**
- 에이전트는 목적 하나가 끝나고 검증이 통과해 한 커밋 단위가 되었다고 판단하면, 작업 보고 끝에 커밋을 제안한다. 제안에는 포함할 파일 목록과 위 형식의 메시지 초안을 넣는다.
- 사용자가 승인하거나 커밋을 요청했을 때만 커밋한다. 푸시는 따로 요청받았을 때만 한다.
- 여러 목적이 섞였으면 나눌 단위를 함께 제안한다.

**브랜치·PR**
- `main`에 직접 커밋·푸시하지 않는다. 브랜치 이름은 `<type>/<짧은-영문-설명>`이다(예: `fix/vocabulary-column-split`).
- PR 제목은 커밋 제목 형식을 따른다. PR 본문은 다음 순서로 쓴다: 요약, 이유, 변경 내용, 검증(테스트 수·감사·`sync --check`·운영 점검), 배포 영향(서버 재배포, 배포본 교체, `VERSION`), 체크리스트.
- 병합은 squash merge로 하고, 배포는 `main`에 병합된 커밋에서만 한다.

## 서비스 고유 규칙

콘텐츠 작업 위치, 수정 위치, 버전 올림 규칙, **릴리스 차단 조건**은 [docs/RELEASE_RULES.md](docs/RELEASE_RULES.md)를 따른다. 정본·엔진·템플릿·공개 결과를 바꾸는 작업 전에 반드시 읽는다. 특히 `server/workbook_engine/`, `server/config/`, `server/schemas/`, `server/docs/semantic-rubric.md`, 템플릿은 릴리스 이력에 경로와 해시가 기록되므로 옮기거나 고칠 때 해당 버전을 함께 올린다.
