---
name: workbook-maker
description: inputs의 영어 지문으로 원격 Workbook Maker MCP 지침에 따라 학생용·해설용 10단계 워크북을 작성하고, PDF를 검수한 뒤 공개해 outputs에 저장한다. 일반 영어 질문에는 사용하지 않는다.
---

# 10단계 워크북 제작

서버 호출은 모두 이 스킬의 공통 클라이언트로 한다. 배포 폴더 루트에서 실행한다.

```bash
python .agents/skills/workbook-maker/scripts/mcp_client.py <명령>
```

아래에서는 이 명령을 `mcp`라고 줄여 쓴다. 모든 응답은 `status`, `next_action`, `violations`, `data`를 가진다. 큰 응답은 `--out .work/...json`으로 저장하고 표준 출력의 요약만 읽는다. 다음 할 일은 `next_action`을 따른다.

## 순서

1. **원본 확인.** `inputs/`(하위 폴더 포함)의 지문을 확인한다. `inputs/README.md`는 원본이 아니다. 사용자가 다른 자료를 지정하면 그 자료를 쓴다. 원문 문장·문장부호·선택지·빈칸·번호가 흐리거나 불확실하면 추측하지 말고 선명한 자료를 요청한다. 대상이 여럿이고 범위가 불명확하면 확인한다.

2. **지침 받기.**
   `mcp call workbook_get_guidance --out .work/guide.json`
   `.work/guide.json`의 `data.rules`(작성 파이프라인, 의미 품질 기준, 단계 규격, 정본·업데이트 스키마), `data.stage9Authoring`, `data.review`를 읽는다. 규칙을 로컬에서 추측하지 않는다.

3. **작성 packet.** 지침의 authoring pipeline에 따라 의미 콘텐츠 전체를 `.build/authoring/<이름>/authoring.json`에 한 번에 작성한다. `<이름>`은 영문 소문자·숫자·하이픈으로 정한다. 번역·직독직해·어휘·빈칸·선택지·영작 제시어를 줄이거나 자동 추측하지 않는다. 9단계는 지문 전체 문장을 A·B·C 선택지에 빠짐없이 배분하고 `answerOrder`는 원문 복원 순서로 쓴다.

4. **packet 검증.**
   `mcp call workbook_authoring_verify --arg-file packet=.build/authoring/<이름>/authoring.json`
   `invalid_input`이면 `violations`의 `field`를 고쳐 다시 검증한다.

5. **정본 저장.** 빈 폴더 `workbooks/<이름>/`을 만든 뒤 확장 결과를 그 폴더에 저장한다.
   `mcp call workbook_authoring_expand --arg-file packet=.build/authoring/<이름>/authoring.json --into workbooks/<이름>`
   클라이언트가 해시를 검증해 `workbooks/<이름>/content.json`을 쓴다. 같은 이름의 정본이 이미 있으면 저장하지 않고 실패한다. 기존 검토 정본을 덮어쓰지 말고 사용자에게 확인한다.

6. **정본 검사.**
   `mcp call workbook_validate_canonical --arg-file canonical=workbooks/<이름>/content.json`
   `ok`가 아니면 `violations`가 가리키는 문장·활동만 고쳐 다시 검사한다.

7. **업데이트 정의.** 정본의 `updateState.appliedUpdates`와 `id`·`applyTo`가 맞는 `updates/<ID>.json`을 둔다. 형식은 `data.rules["schemas/update.schema.json"]`, 예시는 `examples/U-20260710-001.json`이다.

8. **PDF 준비.** 몇 분 걸릴 수 있다.
   `mcp call workbook_prepare_release --arg-file canonical=workbooks/<이름>/content.json --arg-file update=updates/<ID>.json --arg output_base=<이름> --out .work/<이름>/prepare.json`
   `needs_review`는 자동 브라우저·PDF 검사만 통과했다는 뜻이다. `data.releaseId`, `data.reviewImages`, `data.qa`를 확인한다. `invalid_input`·`rejected`이면 `violations`를 해결하고 다시 준비한다. 검사를 약화하거나 우회하지 않는다.

9. **시각 검수.** `.work/review/<releaseId>/` 빈 폴더를 만들고 `data.reviewImages`의 이미지를 하나씩 받는다.
   `mcp call workbook_review_image --arg release_id=<releaseId> --arg image_name=<이미지> --into .work/review/<releaseId>`
   저장된 PNG 파일을 직접 열어 본다. 학생용·해설용 모두에서 2·3단계 빈칸, 4·8·10단계 작성형, 학생용 정답 노출, 해설 정답, 잘림·겹침, 문제본과 해설본의 정답 자리 위치를 확인한다. 응답의 `data.remaining`이 빌 때까지 반복한다. 자동 검사와 시각 검수는 별개다. 결함이 있으면 공개하지 말고 정본을 고쳐 8단계부터 다시 한다.

10. **공개.** 모든 이미지를 실제로 확인했을 때만 공개한다.
    `mcp call workbook_publish_release --arg release_id=<releaseId> --arg reviewer=<검수자> --arg notes="<실제 확인한 내용>" --out .work/<이름>/publish.json`
    클라이언트가 네 파일(`문제.html`, `문제.pdf`, `해설.html`, `해설.pdf`)을 받아 SHA-256과 크기를 검증한 뒤 `outputs/<폴더>/`에 저장하고 `saved_to`로 알려 준다.

11. **보고.** `saved_to`의 네 파일, 페이지 수, 검수에서 실제로 확인한 내용과 남은 문제를 보고한다. 네 파일이 저장되기 전에는 완료로 보고하지 않는다.

## 다시 받기

- 링크는 하루 동안 유효하다. 같은 응답으로 다시 받으려면 `mcp download --from .work/<이름>/publish.json`을 쓴다.
- 만료됐거나 다른 폴더가 필요하면 `mcp call workbook_get_artifacts --arg release_id=<releaseId>`로 새 링크를 받는다. 파일 하나만 필요하면 `workbook_read_artifact`(`--arg name=문제.pdf`)를 쓴다.

## 오류

- 종료 코드 2(연결·인증·설정 실패): 원인을 보고하고 중단한다. 로컬에서 다른 방법으로 대신 만들지 않는다.
- 종료 코드 1(`invalid_input`·`rejected`·`error`): `violations`와 `next_action`을 따른다. `error`가 반복되면 보고한다.
- 종료 코드 3(산출물 검증 실패): 파일이 저장되지 않았다. `workbook_get_artifacts`로 다시 받는다. `--into` 폴더에 같은 이름의 파일이 있어도 3으로 실패하므로 빈 폴더를 쓴다.
- 서버가 만든 HTML·PDF를 임의로 고치지 않는다. 연결 확인이 필요하면 `examples/chocolate/content.json`으로 `workbook_validate_canonical`을 호출한다.
