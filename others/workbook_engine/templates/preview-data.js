/* Ten-stage renderer fixture. Production builds must not include this file. */
const previewRequestedEdition =
  window.WORKBOOK_PREVIEW_EDITION ||
  new URLSearchParams(window.location.search).get("edition");
window.WORKBOOK_EDITION = previewRequestedEdition === "answer" ? "answer" : "student";
window.WORKBOOK_DATA = {
  metadata: {
    documentTitle: window.WORKBOOK_EDITION === "answer"
      ? "10단계 워크북 해설 템플릿"
      : "10단계 워크북 학생용 템플릿",
    screenTitle: "공유 10단계 워크북 템플릿",
    no: "Preview",
    kicker: "Middle Reading",
    grade: "중등",
    topic: "새 정보와 배경지식을 연결하는 독서 습관",
    footerLogo: window.WORKBOOK_PREVIEW_FOOTER || "../../assets/yonjogyo-logo-footer.png"
  },
  pages: [
    {
      pageId: "preview-p01", pageNo: 1, stageId: "passage-practice",
      no: "1", title: "지문 연습하기", part: "1-2", mode: "meaning",
      instruction: "영문과 해석을 읽고 문장의 의미를 이해해 보세요.",
      units: [
        { no: 1, en: "Good readers / <strong>connect</strong> new information / with what they already know.", hint: "훌륭한 독자들은 / <strong>연결한다</strong> 새로운 정보를 / 그들이 이미 아는 것과." },
        { no: 2, en: "This <span class=\"vocab vocab-1 gloss\" data-meaning=\"습관\">habit</span> / <strong>makes</strong> difficult passages / easier to understand.", hint: "이 <span class=\"vocab vocab-1\">습관은</span> / <strong>만든다</strong> 어려운 지문을 / 이해하기 더 쉽게." }
      ]
    },
    {
      pageId: "preview-p02", pageNo: 2, stageId: "korean-cloze",
      no: "2", title: "빈칸 완성하기 (우리말)", part: "1-2", mode: "parallel",
      instruction: "영문을 읽고 우리말 해석의 빈칸을 완성해 보세요.",
      items: [
        { no: 1, en: "Good readers connect new information with what they already know.", ko: "훌륭한 독자들은 새로운 정보를 <span class=\"blank\" data-target-id=\"preview-s2-1\"></span>.", solutions: { "preview-s2-1": "배경지식과 연결한다" } },
        { no: 2, en: "This habit makes difficult passages easier to understand.", ko: "이 습관은 어려운 지문을 <span class=\"blank\" data-target-id=\"preview-s2-2\"></span>.", solutions: { "preview-s2-2": "더 쉽게 이해하게 한다" } }
      ]
    },
    {
      pageId: "preview-p03", pageNo: 3, stageId: "english-cloze",
      no: "3", title: "빈칸 완성하기 (영문)", part: "1-2", mode: "parallel",
      instruction: "우리말 해석을 읽고 영문의 빈칸을 완성해 보세요.",
      items: [
        { no: 1, ko: "훌륭한 독자들은 새로운 정보를 배경지식과 연결한다.", en: "Good readers <span class=\"blank\" data-target-id=\"preview-s3-1\"></span> new information.", solutions: { "preview-s3-1": "connect" } },
        { no: 2, ko: "이 습관은 어려운 지문을 더 쉽게 이해하게 한다.", en: "This habit <span class=\"blank\" data-target-id=\"preview-s3-2\"></span> difficult passages easier.", solutions: { "preview-s3-2": "makes" } }
      ]
    },
    {
      pageId: "preview-p04", pageNo: 4, stageId: "translation-practice",
      no: "4", title: "해석 연습하기", part: "1-2", mode: "writing",
      instruction: "문장 전체의 자연스러운 해석을 써 보세요.",
      items: [
        { no: 1, en: "Good readers connect new information with what they already know.", lines: 2, responseTargetId: "preview-s4-1", solutions: { "preview-s4-1": "훌륭한 독자들은 새로운 정보를 자신이 이미 아는 것과 연결한다." } },
        { no: 2, en: "This habit makes difficult passages easier to understand.", lines: 2, responseTargetId: "preview-s4-2", solutions: { "preview-s4-2": "이 습관은 어려운 지문을 더 쉽게 이해하게 한다." } }
      ]
    },
    {
      pageId: "preview-p05", pageNo: 5, stageId: "verb-form",
      no: "5", title: "동사형 연습하기", part: "1-2", mode: "parallel",
      instruction: "괄호 안에 주어진 단어를 알맞게 고쳐 쓰세요.",
      items: [
        { no: 1, ko: "훌륭한 독자들은 새로운 정보를 연결한다.", en: "Good readers <span class=\"verb-target\" data-target-id=\"preview-s5-1\">(connect)</span> new information.", solutions: { "preview-s5-1": "connect" } },
        { no: 2, ko: "이 습관은 어려운 지문을 더 쉽게 만든다.", en: "This habit <span class=\"verb-target\" data-target-id=\"preview-s5-2\">(make)</span> difficult passages easier.", solutions: { "preview-s5-2": "makes" } }
      ]
    },
    {
      pageId: "preview-p06", pageNo: 6, stageId: "grammar-vocabulary-choice",
      no: "6", title: "어법·어휘 고르기", part: "1-2", mode: "parallel",
      instruction: "괄호 안에서 옳은 어법과 어휘를 골라 보세요.",
      items: [
        { no: 1, ko: "훌륭한 독자들은 새로운 정보를 연결한다.", en: "Good readers <span class=\"choice-target\" data-target-id=\"preview-s6-1\">[connect / connects]</span> new information.", solutions: { "preview-s6-1": "connect" } },
        { no: 2, ko: "이 습관은 지문을 더 쉽게 만든다.", en: "This habit makes passages <span class=\"choice-target\" data-target-id=\"preview-s6-2\">[easier / easiest]</span>.", solutions: { "preview-s6-2": "easier" } }
      ]
    },
    {
      pageId: "preview-p07", pageNo: 7, stageId: "correction",
      no: "7", title: "어색한 곳 찾기", mode: "correction",
      instruction: "밑줄 친 부분 중 어법상 어색한 곳을 찾아 알맞게 고쳐 쓰세요.",
      passage: "Good readers (1) <span class=\"correction-target\" data-target-id=\"preview-s7-find\">connects</span> new information with what they already know.",
      rows: [
        { no: 1, beforeTargetId: "preview-s7-before", afterTargetId: "preview-s7-after", solutions: { "preview-s7-before": "connects", "preview-s7-after": "connect" } }
      ]
    },
    {
      pageId: "preview-p08", pageNo: 8, stageId: "sentence-order",
      no: "8", title: "순서 배열하기", part: "1-1", mode: "writing",
      instruction: "우리말과 같은 뜻이 되도록 주어진 단어를 바르게 배열해 보세요.",
      items: [
        { no: 1, ko: "훌륭한 독자들은 새로운 정보를 배경지식과 연결한다.", bank: "new information / Good readers / with what they know / connect", lines: 2, responseTargetId: "preview-s8-response", solutions: { "preview-s8-response": "Good readers connect new information with what they know." } }
      ]
    },
    {
      pageId: "preview-p09", pageNo: 9, stageId: "paragraph-order",
      no: "9", title: "문단 배열하기", mode: "paragraph-order",
      instruction: "다음 문단을 알맞은 순서로 배열해 보세요.",
      blocks: [
        { label: "(B)", text: "Then, connect the new idea to that knowledge." },
        { label: "(C)", text: "Finally, check whether the passage makes sense." },
        { label: "(A)", text: "First, recall what you already know." }
      ],
      sequenceSlots: 3,
      sequenceTargetIds: ["preview-s9-1", "preview-s9-2", "preview-s9-3"],
      solutions: { "preview-s9-1": "A", "preview-s9-2": "B", "preview-s9-3": "C" }
    },
    {
      pageId: "preview-p10", pageNo: 10, stageId: "composition",
      no: "10", title: "영작 연습하기", part: "1-1", mode: "writing",
      instruction: "우리말과 제시어만 보고 원문과 같은 뜻의 영어 문장을 써 보세요.",
      items: [
        { no: 1, ko: "훌륭한 독자들은 새로운 정보를 자신이 이미 아는 것과 연결한다.", bank: "good readers, connect, new information, already know", lines: 2, responseTargetId: "preview-s10-1", solutions: { "preview-s10-1": "Good readers connect new information with what they already know." } }
      ]
    }
  ]
};

if (window.WORKBOOK_EDITION === "student") {
  const removeSolutions = (value) => {
    if (!value || typeof value !== "object") return;
    if (Array.isArray(value)) {
      value.forEach(removeSolutions);
      return;
    }
    delete value.solutions;
    Object.values(value).forEach(removeSolutions);
  };
  removeSolutions(window.WORKBOOK_DATA);
}
