# 새 워크북 엔진 릴리스 안전성 레드팀 보고서

- 감사일: 2026-07-10
- 대상: `workbook_engine/{compiler,validator,render,qa,release,__main__,schema_gate}.py`, 공유 HTML/CSS/JS 템플릿, canonical·update schema, 변경 보고서 흐름
- 제약: `publish` 미실행, `outputs/` 미변경
- 최종 판정: **미해결 P0/P1 릴리스 차단점 0건**

최신 코드는 공개 전 비공개 `prepare` 검증, 학생용 정답 0, 해설용 정답만 빨강, 학생용·해설용 동일 문제 DOM, 10단계 전체 커버리지, 충돌 시 새 폴더, workbook별 업데이트 보고서를 fail-closed로 강제한다. 현재 잔존 위험은 정상 프로세스가 아닌 강제 종료·디스크 장애·준비 폴더 수동 조작 경계에 한정된다.

## 최종 재현 결과

| 검사 | 결과 | 근거 |
|---|---|---|
| canonical JSON Schema + 구조 검증 | 통과 | `schemaIssues: 0`, 오류·경고 0 |
| 전체 test suite | 통과 | 27/27, 실제 Chrome CDP·PDF `prepare` 포함 |
| renderer JavaScript syntax | 통과 | `node --check` |
| 학생용 정답 노출 | 통과 | 렌더 DOM `solution-value` 0 |
| 해설용 정답 색 | 통과 | 정답 slot `#D71920`, 일반 작업 텍스트 point-red 금지 |
| 학생용·해설용 구조 동일성 | 통과 | 정답 값만 제거한 `#pages` 태그·클래스·target·text 순서 SHA-256 일치 |
| 7단계 교정 target | 통과 | 5개 모두 밑줄, 검정 프롬프트, 해설의 정답만 빨강 |
| PDF | 통과 | 학생용·해설용 각 22쪽, A4, 빈 페이지·오류 마커·넘침 없음 |
| 검증 전 비공개 | 통과 | 통합 test의 `prepare` 산출물은 임시 build에만 생성, `outputs/` 미생성 |
| stale build 게시 거부 | 통과 | canonical·schema·spec·rubric·template·logo·engine digest 초기/종료/게시 직전 재검사 |
| 다중 workbook 보고서 | 통과 | `reports/updates/<updateId>/<workbook>.md` + aggregate index |

추가 공격 테스트에서 해설 작업 영역의 일반 영문 169개를 point-red로 강제하자 렌더 gate가 거부했다. 또한 해설 2단계의 `en/ko` 필드 순서만 바꾸어도 정규화 DOM digest mismatch로 거부했다.

## 감사 중 발견·종결된 결함

| 우선순위 | 실제 결함 | 재현 | 적용된 해결 |
|---|---|---|---|
| P0 | `prepare` 후 canonical/spec/template가 바뀌어도 예전 4개 산출물과 새 manifest를 섞어 게시할 수 있음 | 준비 manifest의 canonical digest와 현재 canonical digest 불일치를 실제 확인 | 전체 입력 digest, 준비 snapshot, 게시 전 2회 재검사, stale 회귀 test |
| P0 | 7단계가 “밑줄 친 부분”을 요구하지만 sanitizer가 target class/`strong`을 제거 | 초기 private PDF p14에 밑줄 0개 | `correction-target` span, sanitizer allowlist, CSS underline, CDP computed-style gate |
| P0 | `_build_manifest()` 시그니처와 호출 keyword 불일치 | 실제 happy-path가 `unexpected keyword argument 'pages'`로 중단될 상태 | student/answer pages 별도 전달 + 실제 `prepare` 통합 test |
| P0 | 리팩터링 중 `release_status()` return 누락과 `_build_manifest()` 조기 return | test에서 `NoneType` 오류, required-field gate unreachable | return 위치 분리 복구, 27/27 재통과 |
| P1 | `outputBase` 절대경로·`../`로 `outputs/` 밖 게시 가능 | `/tmp/...`, `../../../...`가 그대로 resolve | 단일 safe folder name allowlist + 회귀 test |
| P1 | 공개 폴더 rename 후 보고서·manifest 쓰기 실패 시 산출물만 노출 | 코드 순서상 보고서 쓰기가 공개 뒤에 있었음 | metadata temp/backup + output/metadata 롤백 트랜잭션 |
| P1 | 교정·문단 활동이 여러 개여도 `[0]`만 컴파일, 빈 배열도 canonical/compiled 통과 | 각 2개를 선언해도 1개 page만 생성 | 전체 활동 반복, 빈 배열·ID 중복 금지, 활동 전수 회귀 test |
| P1 | dependency-free schema gate가 update schema의 `oneOf/allOf/if/then`을 무시 | `affectedStages: [{"not":"a stage"}]`가 schema/custom 검증을 모두 통과 | 해당 keyword 구현 + invalid-stage test |
| P1 | `applyTo` 범위가 보고서 라벨로만 존재 | 선택되지 않은 workbook, `manual-review`, 기존 workbook의 `new-only`도 자동 진행 가능 | selected/new-only/manual-review 실집행 + canonical scope 일치 검사 |
| P1 | 보고서 page record에 content digest가 없고 student page를 answer에도 복제 | 번역을 바꿔 compiled JSON이 달라져도 page records 동일 | edition별 실제 page digest |
| P1 | canonical 번역·원문을 exercise `baseText`에 반복 저장해 업데이트 불일치 가능 | translation만 바꾸고 기존 `koBlank.baseText`를 남겼을 때 초기 validator가 통과 | default baseText 파생, 명시적 `overrideReason` 있는 예외만 허용 |
| P1 | 해설 작업 영역의 일반 본문이 빨강이어도 QA 통과 | 일반 영문 169개를 point-red로 바꾸고 `state=ok` 확인 | `.work-area` visible computed color 전수 검사 |
| P1 | 학생용·해설용 구조 검사가 class 개수·target ID만 비교 | 해설 2단계 field 순서를 뒤집어도 통과 | 정규화 전체 DOM signature 비교 |
| P1 | 다중 workbook 업데이트가 동일 `<updateId>.md`를 덮어써 이전 보고서 소실 | `all/selected` 순차 게시 시 마지막 workbook만 존재 | aggregate index + workbook별 detail 보고서 |
| P1 | 구성 변경 시 version bump를 강제하지 않고 engine 소스 hash가 최종 bundle에 없음 | 같은 `contentVersion`으로 canonical 수정 가능 | canonical/spec/schema/rubric/template/engine transition gate + `engineInputs` manifest |

## 잔존 P2 경계조건

### P2-01. 프로세스 강제 종료 중 트랜잭션 회복

- 조건: output rename 후 metadata commit 중 프로세스가 `SIGKILL`·전원 장애로 종료됨.
- 현재 보호: 일반 Python 예외은 metadata backup을 복구하고 새 output 폴더를 제거한다.
- 잔존 위험: 프로세스 자체가 죽으면 `finally`/rollback이 실행되지 않아 부분 commit이 남을 수 있다. 또한 공개 commit 후 private `release-state.json` 쓰기가 실패하면 실제 게시는 성공했지만 상태가 `awaiting-visual-review`로 남을 수 있다.
- 권장: `prepared -> committing -> published` 저널을 동일 filesystem에 fsync하고, `status/recover` 명령이 저널·output·metadata를 비교해 재실행 또는 rollback하게 한다.

### P2-02. 준비 폴더의 파생 증거 수동 변조

- 조건: QA 후 사용자가 private build의 `build-manifest.json`, `before-bundle.json`, `after-bundle.json`, `qa.json`, contact sheet를 직접 수정함.
- 현재 보호: 최종 4개 산출물과 모든 외부 입력은 digest로 잠겨 있다.
- 잔존 위험: 게시 코드가 private build manifest/bundle을 읽으므로, 신뢰할 수 있는 workspace라는 가정이 깨지면 보고서·manifest·시각 검수 증거가 산출물과 불일치할 수 있다.
- 권장: 준비 상태의 파생 파일도 hash 목록에 포함하고 publish 직전 검증하거나, 잠긴 compiled JSON·QA 결과에서 manifest/report를 재생성한다.

### P2-03. 교정 정답의 원문 복원 자동 증명 한계

- 조건: correction target의 `correct`를 원문과 관계없는 비어 있지 않은 문자열로 바꿈.
- 재현: `correct = "banana"`도 구조 validator는 통과한다.
- 완화: 현재 Chocolate 교정 정답은 별도 의미 감사에서 재검증되었고, 게시는 contact sheet 시각 승인을 요구한다.
- 권장: correction activity에 source sentence ID/range 또는 복원 기준 텍스트를 보존하고, incorrect target을 correct로 채운 결과가 확정 원문과 일치하는지 검증한다.

### P2-04. console event·print media 전용 레이아웃 감시

- 조건: renderer가 `data-render-validation=ok` 후 `console.error`를 기록하거나, 향후 `@media print`에서만 레이아웃을 바꾸는 CSS가 추가됨.
- 현재 완화: DOM overflow, PDF 쪽수·A4·빈 쪽, 대표 페이지 PNG가 있어 현재 CSS의 실제 결함은 검출된다.
- 잔존 위험: CDP console/exception event를 별도 수집하지 않고, overflow JS는 일반 screen media에서 실행된다.
- 권장: `Runtime.exceptionThrown`/`Log.entryAdded`/`console.error` 수집과 `Emulation.setEmulatedMedia("print")` 후 두 번째 overflow audit를 추가한다.

## 게시 직전 조건

최신 private build `20260710-211850-10562827`은 `inputsCurrent: true`, `artifactsIntact: true`, `canPublish: true`다. 22쪽 학생용·해설용 산출물과 contact sheet가 존재하며, 아직 `awaiting-visual-review`이고 `outputDir` 생성은 없다.

따라서 기술적 릴리스 차단점은 없으며, 최종 시각 검수 승인 후에만 별도 `publish`를 실행해야 한다. 본 레드팀은 `publish` 명령을 호출하지 않았고 `outputs/`를 변경하지 않았다.
