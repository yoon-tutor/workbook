# 새 지문 통합 작성 파이프라인

이 경로는 콘텐츠 품질을 줄이지 않고 Codex의 반복 파일 작업만 줄인다. 번역, 의미 단위, 서술어, 어휘, 빈칸, cue, 오답, 교정, 단락 배열, 영작 제시어는 모두 `docs/semantic-rubric.md`를 따라 Codex가 작성한다.

## 불변 경계

- 기존 `workbooks/*/content.json`을 packet으로 다시 펼쳐 덮어쓰지 않는다.
- canonical schema, 10단계 spec, compiler, 공유 템플릿, 릴리스 QA는 기존 경로를 그대로 쓴다.
- packet expander는 영한 텍스트, 번역, 답, 오답, 문제 선정을 작성하거나 고치지 않는다.
- 반복되는 target의 위치가 명시되지 않으면 확장을 중단한다.

## 작업 흐름

1. 선명한 원본에서 영어 지문을 확정한다.
2. Codex가 지문 전체를 한 번의 통합 묶음으로 판단해 `.build/authoring/<name>/authoring.json`을 작성한다. 이 packet은 private staging이며 정본은 아니다.
3. `verify`로 packet을 canonical로 펼쳐 schema와 validator를 통과하는지 확인한다.
4. 실패하면 오류 path에 해당하는 문장·필드만 재판단한다.
5. 통과한 packet을 새 canonical `content.json`으로 한 번 확장한다.
6. 기존 `validate → prepare → 시각 검수 → publish` 경로를 그대로 수행한다.

## Packet 형식

최상위 metadata, sourceStatus, updateState, passageActivities와 각 문장의 의미 콘텐츠는 canonical과 같다. 다음 기계 필드만 축약한다.

- `sentences[].id`, `sentences[].no`: 배열 순서에서 생성
- `meaningSegments[].id`: 의미 단위 순서에서 생성
- annotation `segmentId`: 1부터 시작하는 `segment` 번호로 작성
- target: 한 번만 나오면 문자열, 반복되면 `{"text": "...", "occurrence": 2}`
- `arrange.chunks`: ID 없는 문자열 배열
- `arrange.displayOrder`: 1부터 시작하는 chunk 번호 순열
- correction target ID: 대상 순서에서 생성
- paragraph blocks: 각 block의 1부터 시작하는 문장 번호 배열
- paragraph displayOrder/answerOrder: 1부터 시작하는 block 번호 순열

새 9단계 문항에서는 `blocks`를 학생에게 **보이는 A·B·C 순서**로 작성한다. 각 block에 해당 지문의 원문 문장을 빠짐없이, 중복 없이 배분하고, `displayOrder`는 `[1,2,3]`으로 둔다. `answerOrder`는 원문을 복원하는 선택지 번호 순서이며 `[1,2,3]`이 되어서는 안 된다. 다섯 문항을 한 packet으로 작성할 때는 가능한 다섯 비자명 순열을 중복 없이 사용한다. `verify`와 `expand`는 이 새 문항 정책에 어긋나는 packet을 거부한다. 기존 canonical의 `validate`·`prepare`·출력 계약에는 이 제한을 소급 적용하지 않는다.

예시:

```json
{
  "source": "Having a common currency means that transaction costs disappear.",
  "translation": "공통 통화를 사용한다는 것은 거래 비용이 사라진다는 것을 의미한다.",
  "meaningSegments": [
    {"en": "Having a common currency means", "ko": "공통 통화를 사용한다는 것은 의미한다"},
    {"en": "that transaction costs disappear.", "ko": "거래 비용이 사라진다는 것을."}
  ],
  "annotations": {
    "predicates": [
      {"segment": 1, "en": ["means"], "ko": ["의미한다"]},
      {"segment": 2, "en": ["disappear"], "ko": ["사라진다는"]}
    ],
    "vocabulary": []
  }
}
```

## 도구

| 단계 | MCP 도구 |
|---|---|
| packet 검증 | `workbook_authoring_verify(packet)` |
| canonical 확장 | `workbook_authoring_expand(packet)` → 산출물 `content.json`을 `workbooks/<name>/`에 저장 |
| 정본 검사 | `workbook_validate_canonical(canonical)` |
| PDF 준비·검수·공개 | `workbook_prepare_release` → `workbook_review_image`(모든 이미지) → `workbook_publish_release` |

실패 응답의 `violations[].field`는 packet 또는 canonical 안의 위치다. 해당 문장·필드만 다시 판단해 고친다.
