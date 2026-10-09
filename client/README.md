# 10단계 영어 워크북 제작기

영어 지문으로 학생용·해설용 10단계 워크북(HTML·PDF)을 만드는 Codex용 패키지입니다. 작성 규칙 검사, PDF 생성, 자동 품질 검사는 서버가 하고, Codex는 지문 분석·작성과 시각 검수를 맡습니다.

## 준비

- Python 3.10 이상 (추가 설치 없음). 브라우저·Node 설치는 필요하지 않습니다.
- Codex에서 이 폴더를 프로젝트로 열고 신뢰할 수 있는 프로젝트로 설정합니다.
- `.env`에 연결 정보(`MCP_URL`, `MCP_API_TOKEN`)가 들어 있습니다. 이 폴더와 `.env`는 다른 사람과 공유하지 마세요.

연결 확인:

```bash
python .agents/skills/workbook-maker/scripts/mcp_client.py ping
```

## 사용

1. `inputs/`에 영어 지문(PDF·이미지·텍스트·HTML)을 넣습니다.
2. Codex에 "워크북 만들어 줘"처럼 요청합니다. Codex가 `$workbook-maker` 스킬로 작업합니다.
3. Codex가 서버 지침에 따라 작성 packet을 쓰고 정본(`workbooks/<이름>/content.json`)을 만든 뒤, PDF를 준비하고 검수 이미지를 모두 열어 확인한 다음 공개합니다.
4. 결과는 `outputs/<이름>/`에 `문제.html`, `문제.pdf`, `해설.html`, `해설.pdf` 네 파일로 저장됩니다. 파일은 서버가 알려 준 SHA-256으로 검증된 뒤에만 저장됩니다.

## 폴더

| 폴더 | 내용 |
|---|---|
| `inputs/` | 원본 지문 |
| `.build/authoring/` | 작성 packet (중간 자료) |
| `workbooks/` | 정본 `content.json` |
| `updates/` | 업데이트 정의 JSON |
| `examples/` | 연결 확인용 예시 정본과 업데이트 |
| `outputs/` | 공개된 워크북 |
| `.work/` | 서버 응답·검수 이미지 등 중간 파일 |

정본과 packet은 서버로 전송되어 검사·생성에 쓰입니다. 공개 결과 링크는 하루 동안 유효하며, 만료되면 Codex가 다시 받습니다.
