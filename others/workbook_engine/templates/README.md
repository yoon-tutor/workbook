# 공유 워크북 템플릿 계약

이 디렉터리는 학생용과 답지가 함께 사용하는 단일 렌더 소스다. `shell.html`은 데이터가 없는 배포용 셸이고, `workbook.css`와 `renderer.js`가 현재 확정 디자인과 렌더 동작을 제공한다. `preview.html`과 `preview-data.js`는 작은 개발 fixture이며 최종 출력에 포함하지 않는다.

## 입력

렌더러 실행 전에 전역 두 개를 지정한다.

```js
window.WORKBOOK_EDITION = "student"; // 또는 "answer"
window.WORKBOOK_DATA = {
  metadata: {
    documentTitle: "문제",
    screenTitle: "10단계 워크북",
    no: "Chocolate",
    kicker: "Middle Reading",
    grade: "중등",
    topic: "초콜릿의 기원과 역사"
  },
  pages: [
    {
      pageId: "stage-03-page-01",
      pageNo: 1,
      stageId: "stage-03",
      no: "3",
      title: "빈칸 완성하기 (영문)",
      part: "1-14",
      instruction: "문맥에 맞는 말을 빈칸에 쓰세요.",
      mode: "parallel",
      items: []
    }
  ]
};
```

`pages`의 원소 하나가 A4 한 쪽이다. 렌더러는 페이지를 합치거나 나누지 않는다. 이전 형식과의 이전 작업을 위해 최상위 `steps` 및 `worksheets[].steps`도 읽지만, 새 compiler는 `pages`를 출력한다.

지원하는 `mode`는 다음과 같다.

- `meaning`: `units[]`
- `parallel`: `items[]`
- `writing`: `items[]`
- `correction`: `rows[]` 또는 `corrections[]`
- `paragraph-order`: `blocks[]`

## 명시적 정답 target

문제 문자열의 정답 위치는 정규식으로 추측하지 않는다. compiler가 모든 위치에 고유한 `data-target-id`를 넣고 같은 item의 `solutions`에서 답을 연결한다.

```json
{
  "en": "They <span class=\"blank\" data-target-id=\"s03-en-01\"></span> cacao.",
  "solutions": {
    "s03-en-01": "used"
  }
}
```

학생용과 답지는 같은 target 요소를 `.solution-slot`으로 렌더링한다. `answer` edition에서만 그 안에 아래 자식이 추가된다.

```html
<span class="solution-value">used</span>
```

릴리스는 해설용을 먼저 브라우저에 렌더링한다. 2·3·5·6·7·9단계의 모든 비작성형 `.solution-slot`은 실제 가로·세로를 `solutionSlotLayouts`에 잠그고, 4·8·10단계 작성형은 답의 각 줄 위치·가로·세로와 전체 `.write-box` 높이를 `responseLayout`에 잠근다. 그 해설용 IR에서 정답 값만 제거해 학생용을 만든다. 따라서 정답이 빠져도 뒤 문장이 당겨지거나 문항 높이가 줄지 않고, 시각적으로는 해설 문항에서 답 글자만 지운 형태가 된다. 학생용 payload와 DOM에는 정답이 남지 않는다.

5·6단계의 괄호형·선택형 문제 단서는 해설에서도 `.slot-prompt`로 그대로 보존하고, 빨간 `.solution-value`를 옆에 추가한다. 문제 단서를 해설에서 숨겼다가 학생용에서 되살리는 방식은 금지한다.

작성형 답안 영역은 `responseTargetId`를 표준으로 사용한다. 이전 중간 IR과의 호환을 위해 `solutionTargetId`와 `answerTargetId`도 허용한다.

```json
{
  "lines": 3,
  "responseTargetId": "s10-response-01",
  "solutions": {
    "s10-response-01": "Good readers connect new information."
  }
}
```

8단계 순서 배열하기도 이 작성형 답안 영역을 사용한다. 학생용과 해설용 모두 조각 수에 맞춘 짧은 빈칸을 별도로 렌더링하지 않고, 우리말·제시어·긴 답안 작성선만 같은 위치에 둔다. 해설용에서는 긴 답안 영역의 동일한 `responseTargetId`에 완성 문장 하나를 표시한다.

7단계 교정 행은 틀린 표현과 고친 표현의 target을 각각 둔다. 답지에서 틀린 표현은 `.correction-original`의 검정 본문으로, 고친 표현만 `.solution-value`의 포인트 빨강으로 표시된다.

교정 지문 안에서 학생이 찾아야 할 표현은 `<span class="correction-target" data-target-id="…">`로 명시하며, renderer는 이 클래스의 검정 밑줄이 실제 적용됐는지 CDP 품질 검사에 노출한다.

```json
{
  "beforeTargetId": "s07-before-01",
  "afterTargetId": "s07-after-01",
  "solutions": {
    "s07-before-01": "connects",
    "s07-after-01": "connect"
  }
}
```

9단계는 `sequenceTargetIds`, `sequenceSlots`, 단계 수준 `solutions`를 사용한다.

## 학생용 projection

렌더러는 `student` edition에서 정답 값을 DOM에 넣지 않는다. 그러나 최종 학생용 HTML의 소스에도 정답이 남지 않게 하려면 compiler가 학생용 payload를 만들 때 `solutions`와 구형 `answer`/`solution` 값 자체를 제거해야 한다. `data-target-id`, `responseTargetId`, `sequenceTargetIds`, `sequenceSlots`, `solutionSlotLayouts`, `responseLayout`은 유지해야 두 edition의 문제 구조와 답 자리 형상이 동일하다.

## 완료 및 실패 계약

렌더러는 DOM 생성 뒤 폰트와 모든 이미지를 기다리고 두 프레임 뒤 레이아웃을 검사한다.

- 성공: `<html data-render-validation="ok" data-render-page-count="…">`
- 실패: `<html data-render-validation="failed">`와 `.validation-panel`
- 진행 중: `<html data-render-validation="pending">`
- Promise: `window.__WORKBOOK_RENDER_READY__`

자동 생성기는 `ok`만 성공으로 인정해야 한다. `pending`, `failed`, renderer 미실행은 모두 실패다.

릴리스 QA는 모든 비작성형 정답 슬롯의 페이지 기준 `left/top/width/height`와 작성형 답안의 박스 및 줄별 형상을 문제본·해설본 사이에서 비교한다. 하나라도 0.75px을 넘게 다르면 공개를 차단한다.

## 정답 색상 계약

정답 포인트 빨강 `#D71920`은 `.solution-value`에만 부여한다. `.solution-slot`, 작성선, 틀린 표현, 문제 본문에는 정답 빨강을 부여하지 않는다. 기존 답지 전용 클래스인 `.solution`, `.filled-answer`, `.solution-text`, `.solution-line`이 DOM에 나오면 렌더 검증이 실패한다.
