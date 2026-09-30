# AGENTS.md

이 폴더는 영어 지문 정본 하나에서 학생용·해설용 10단계 워크북을 생성하는 작업공간이다. 긴 규칙을 이 파일에 복제하지 않고 실행 가능한 spec·validator·공유 템플릿에 둔다.

상위 `워크북` 폴더는 사용자가 보기 쉽게 `input/`, `outputs/`, `others/` 세 폴더만 유지한다. 실행·검증은 이 `others/` 폴더에서 하며, `workbooks/`는 `input/workbooks/`에서도 같은 정본을 보여 준다. `outputs/`는 상위 공개 결과 폴더를 가리킨다.

## 작업 라우터

- 워크북 생성·수정·HTML/PDF·검수·릴리스에는 프로젝트의 [.agents/skills/workbook-release/SKILL.md](.agents/skills/workbook-release/SKILL.md)를 사용한다.
- Codex에서 새 워크북을 작업할 때는 [Mac·Windows 공용 MCP 배포판](distribution/workbook-maker/AGENTS.md)의 `.codex/config.toml`과 `AGENTS.md`를 사용한다. 에이전트가 등록된 MCP 도구를 직접 호출한다. 연결 및 현재 서버 기능은 [docs/remote-mcp-usage.md](docs/remote-mcp-usage.md)를 따른다.
- 아래 `scripts/run.py` 명령은 기존 개발·회귀 검증용 로컬 경로다. Mac용 직접 MCP 배포판의 필수 명령이 아니다.
- 새 지문은 `docs/authoring-pipeline.md`의 통합 authoring packet으로 의미 콘텐츠를 한 번에 작성한 뒤 canonical을 파생한다. 기존 canonical을 packet으로 재생성해 덮어쓰지 않는다.
- 콘텐츠 정본: `workbooks/<이름>/content.json`
- 새 지문 작성 packet: `.build/authoring/<이름>/authoring.json` (임시 private staging, 정본 아님)
- 단계·페이지·출력 계약: `config/workbook-spec.json`
- 의미 품질 기준: `docs/semantic-rubric.md`
- 공통 디자인: `workbook_engine/templates/`
- 생성·검증 엔진: `workbook_engine/`
- 업데이트 정의: `updates/U-YYYYMMDD-NNN.json`
- 변경 보고서: `reports/updates/<update-id>.md`

`AGENTS(34).md`, 기존 `outputs/`의 HTML, `tmp/` legacy builder는 새 작업의 기준이 아니다. 검토된 canonical을 legacy migration으로 다시 덮어쓰지 않는다.

## 수정 위치

| 요청 | 수정할 곳 |
|---|---|
| 원문·해석·직독직해·문항 정답 | 해당 canonical의 관련 문장/활동만 |
| 10단계 규칙·페이지 목표 | `config/workbook-spec.json`과 validator |
| 공통 레이아웃·색상·렌더 동작 | 공유 CSS/renderer 한 벌 |
| 출력·검증·릴리스 동작 | compiler/QA/release 모듈 |
| 변경 적용 범위 | update JSON과 version registry |

학생용/해설용 별도 콘텐츠나 별도 CSS를 만들지 않는다. 페이지, part, 번호, 정답 슬롯, HTML/PDF는 파생 데이터이므로 canonical에 저장하지 않는다.

Authoring packet은 번역·직독직해·서술어·어휘·빈칸·동사 cue·선택지·교정·단락 배열·영작 제시어를 줄이거나 자동 추측하는 형식이 아니다. 문장·문항 ID, `no`, `segmentId`, `colorSlot`, target wrapper만 결정론적으로 추가한다. 반복 target은 packet에 `occurrence`를 명시해야 하며 소프트웨어가 추측하지 않는다.

## 릴리스 차단 조건

- 원문·문장부호·선택지·빈칸·번호가 불확실하면 추측하지 말고 선명한 자료를 요청한다.
- 원문 전체 문장을 모든 문장 단위 단계에서 빠짐없이 사용한다.
- 고정 10단계 순서와 세로 배치를 유지한다.
- 직독직해 영어 단위와 한국어 단위를 1:1로 맞추고 영어 어순을 유지한다.
- 학생용 payload와 DOM에는 정답이 0개여야 한다.
- 해설을 브라우저에 먼저 완성하고, 문제본은 그 해설 IR에서 `.solution-value` 정답 값만 제거해 만든다. 2·3단계 문장 속 빈칸, 5·6단계 선택 자리, 7단계 교정 칸, 9단계 순서 칸, 4·8·10단계 작성 영역까지 예외 없이 적용한다.
- 모든 비작성형 `.solution-slot`은 해설에서 측정한 페이지 내 위치·가로·세로가 문제본과 0.75px 이내로 같아야 한다. 작성형은 답안 박스와 답의 각 줄 위치·가로·세로가 같은 허용치 안에서 일치해야 한다.
- 문제본을 위해 임의의 고정 폭 빈칸이나 대체 밑줄을 다시 만들지 않는다. 해설의 답 글자만 사라진 빈 자리를 그대로 유지한다.
- 5·6단계의 괄호형·선택형 문제 단서는 해설에서도 숨기지 않는다. 검정 문제 단서와 빨간 정답을 함께 보여야 문제본이 해설본에서 정답만 제거한 구조가 된다.
- 8단계는 우리말·제시어·긴 답안 작성선만 표시한다. 제시어 개수에 맞춘 조각형 정답 밑줄은 문제·해설 모두 만들지 않으며, 해설 정답은 긴 답안 영역에 완성 문장으로 표시한다.
- 같은 단계의 연속 문항은 안전 상한 안에서 가장 적은 페이지에 균등하게 나눈다. 앞 페이지에 들어갈 수 있는 문항을 남겨 둔 채 마지막 페이지에 한 문항만 배치하는 단독 꼬리 페이지는 만들지 않는다.
- 브라우저 overflow, 잘림, 겹침, target 불일치, 모든 정답 자리의 위치·가로·세로 불일치, PDF 쪽수 불일치가 하나라도 있으면 공개하지 않는다. 검사를 약화하거나 예외 처리해 통과시키지 않는다.
- `prepare` 결과의 학생용·해설용 contact sheet에서 2·3단계 빈칸과 4·8·10단계 작성형을 반드시 포함해 눈으로 확인하기 전 `publish`하지 않는다.
- 측정용 임시 HTML·브라우저 프로필·캐시·중복 미리보기 파일은 최종 산출물이 아니다. 필요한 검증이 끝나면 제거하되 canonical, 네 공개 산출물, QA 이미지·JSON, 릴리스 상태·보고서는 보존한다.

## 기존 개발 경로의 명령

```bash
python -X utf8 scripts/run.py inspect workbooks/<이름>/content.json --sentence <번호>
python -X utf8 scripts/run.py validate workbooks/<이름>/content.json
python3 -m unittest discover -s tests -v
python -X utf8 scripts/run.py status workbooks/<이름>/content.json
python -X utf8 scripts/run.py prepare workbooks/<이름>/content.json --update updates/<ID>.json
python -X utf8 scripts/run.py publish <build-dir> --reviewer Codex --notes "실제 시각 검수 결과"
python -X utf8 scripts/run.py authoring verify .build/authoring/<이름>/authoring.json
python -X utf8 scripts/run.py authoring expand .build/authoring/<이름>/authoring.json --output workbooks/<이름>/content.json
```

`prepare`는 `.build/releases/`에만 쓴다. 모든 자동·시각 검사를 통과한 `publish`만 기존 폴더를 덮어쓰지 않는 새 `outputs/<이름>_vN/`을 만들고, 네 파일(`문제.html`, `문제.pdf`, `해설.html`, `해설.pdf`), 워크북별 상세 보고서, 업데이트 인덱스를 확정한다.
