/*
 * Shared workbook renderer
 *
 * Primary input contract:
 *   window.WORKBOOK_EDITION = "student" | "answer"
 *   window.WORKBOOK_DATA = {
 *     metadata: {
 *       documentTitle, screenTitle, no, kicker, grade, topic,
 *       footerLogo?, showAnswerSummary?, answer?
 *     },
 *     pages: [
 *       {
 *         id?, no, title, part, instruction,
 *         mode: "meaning" | "parallel" | "writing" |
 *               "correction" | "paragraph-order",
 *         items? | units? | rows? | blocks?
 *       }
 *     ]
 *   }
 *
 * Exercise text may contain explicit target elements:
 *   <span class="blank" data-target-id="s03-blank-1"></span>
 * Item answers are keyed by the same stable id:
 *   solutions: { "s03-blank-1": "answer" }
 *
 * The renderer never paginates. One input page always becomes one A4 page.
 * Student and answer editions use the same problem markup. Answer values are
 * added only as .solution-value children of existing .solution-slot elements.
 */
(() => {
  "use strict";

  const VERSION = "1.0.2";
  const VALID_EDITIONS = new Set(["student", "answer"]);
  const VALID_MODES = new Set([
    "meaning",
    "parallel",
    "writing",
    "correction",
    "paragraph-order"
  ]);
  const DEFAULT_FOOTER_LOGO = "../../assets/yonjogyo-logo-footer.png";
  const RESOURCE_TIMEOUT_MS = 15000;
  // A4 millimetres resolve to fractional CSS pixels; allow the resulting
  // three-pixel border/rounding delta, but fail any larger intrusion.
  const OVERFLOW_TOLERANCE_PX = 3;

  const documentRoot = document.documentElement;
  const pagesRoot = document.querySelector("#pages");
  const statusNode = document.querySelector(".render-status");
  const screenTitleNode = document.querySelector(".screen-title");
  const printButton = document.querySelector("[data-print-button]");
  const diagnostics = [];
  let activeEdition = "student";
  let activeSolutionSlotLayouts = {};

  function text(value) {
    return value === undefined || value === null ? "" : String(value);
  }

  function list(value) {
    return Array.isArray(value) ? value : [];
  }

  function isObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function hasOwn(object, key) {
    return Object.prototype.hasOwnProperty.call(object, key);
  }

  function escapeHtml(value) {
    return text(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function escapeAttribute(value) {
    return escapeHtml(value);
  }

  function safeCssLength(value, fallback) {
    const candidate = text(value).trim();
    return /^\d+(?:\.\d+)?(?:mm|cm|pt|px|rem|em)$/.test(candidate)
      ? candidate
      : fallback;
  }

  function safeClassNames(value) {
    return text(value)
      .split(/\s+/)
      .filter((name) => /^[a-z][a-z0-9_-]*$/i.test(name))
      .join(" ");
  }

  function plainText(value) {
    const template = document.createElement("template");
    template.innerHTML = text(value);
    return (template.content.textContent || "").trim();
  }

  function answerText(value) {
    if (isObject(value) && hasOwn(value, "text")) return plainText(value.text);
    return plainText(value);
  }

  function updateStatus(message) {
    if (statusNode) statusNode.textContent = message;
  }

  function formatError(error) {
    if (error instanceof Error) return error.message;
    return text(error) || "알 수 없는 렌더링 오류";
  }

  function renderFailure(errors, title = "워크북 렌더링 오류") {
    const uniqueErrors = [...new Set(list(errors).map(formatError).filter(Boolean))];
    documentRoot.dataset.renderValidation = "failed";
    documentRoot.dataset.renderErrorCount = String(uniqueErrors.length || 1);
    updateStatus("검증 실패");

    if (!pagesRoot) return;
    const items = uniqueErrors.length
      ? uniqueErrors
      : ["렌더링 실패 원인을 확인할 수 없습니다."];
    pagesRoot.innerHTML = `
      <article class="page">
        <section class="validation-panel">
          <h1>${escapeHtml(title)}</h1>
          <ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
      </article>
    `;
  }

  function pushDiagnostic(message) {
    diagnostics.push(message);
  }

  function normalizeEdition(data) {
    const requested = text(
      window.WORKBOOK_EDITION ||
      data.edition ||
      documentRoot.dataset.workbookEdition ||
      "student"
    ).toLowerCase();

    if (!VALID_EDITIONS.has(requested)) {
      throw new Error(`WORKBOOK_EDITION은 student 또는 answer여야 합니다: ${requested}`);
    }
    return requested;
  }

  function withoutSteps(sheet) {
    if (!isObject(sheet)) return {};
    const { steps, pages, ...metadata } = sheet;
    return metadata;
  }

  function normalizePages(data) {
    const topMetadata = isObject(data.metadata)
      ? data.metadata
      : (isObject(data.sheet) ? withoutSteps(data.sheet) : {});

    if (Array.isArray(data.pages)) {
      return data.pages.map((page, index) => {
        if (!isObject(page)) {
          return { index, page: {}, step: null, metadata: topMetadata };
        }
        const explicitStep = isObject(page.step) ? page.step : page;
        const pageMetadata = isObject(page.metadata)
          ? page.metadata
          : (isObject(page.sheet) ? withoutSteps(page.sheet) : {});
        return {
          index,
          page,
          step: explicitStep,
          metadata: { ...topMetadata, ...pageMetadata }
        };
      });
    }

    if (Array.isArray(data.steps)) {
      return data.steps.map((step, index) => ({
        index,
        page: step,
        step,
        metadata: topMetadata
      }));
    }

    if (Array.isArray(data.worksheets)) {
      return data.worksheets.flatMap((sheet, sheetIndex) => {
        const metadata = { ...topMetadata, ...withoutSteps(sheet) };
        return list(sheet.steps).map((step, stepIndex) => ({
          index: `${sheetIndex}-${stepIndex}`,
          page: step,
          step,
          metadata
        }));
      });
    }

    throw new Error("WORKBOOK_DATA.pages 또는 WORKBOOK_DATA.steps 배열이 필요합니다.");
  }

  function normalizeWorkbook(rawData) {
    if (!isObject(rawData)) {
      throw new Error("window.WORKBOOK_DATA에 워크북 객체가 없습니다.");
    }

    const edition = normalizeEdition(rawData);
    const pages = normalizePages(rawData);
    const metadata = isObject(rawData.metadata) ? rawData.metadata : {};

    if (!pages.length) {
      throw new Error("렌더링할 고정 페이지가 없습니다.");
    }

    return { rawData, edition, pages, metadata };
  }

  function collectStringValues(value, output = []) {
    if (typeof value === "string") {
      output.push(value);
      return output;
    }
    if (Array.isArray(value)) {
      value.forEach((item) => collectStringValues(item, output));
      return output;
    }
    if (isObject(value)) {
      Object.values(value).forEach((item) => collectStringValues(item, output));
    }
    return output;
  }

  function validateStructure(workbook) {
    const errors = [];
    const pageIds = new Set();

    workbook.pages.forEach((entry, pageIndex) => {
      const step = entry.step;
      if (!isObject(step)) {
        errors.push(`${pageIndex + 1}쪽: 페이지 객체가 아닙니다.`);
        return;
      }

      const mode = text(step.mode || "parallel");
      if (!VALID_MODES.has(mode)) {
        errors.push(`${pageIndex + 1}쪽: 지원하지 않는 mode입니다: ${mode}`);
      }

      const pageId = text(
        entry.page.pageId ||
        step.pageId ||
        entry.page.id ||
        step.id ||
        `page-${pageIndex + 1}`
      );
      if (pageIds.has(pageId)) {
        errors.push(`${pageIndex + 1}쪽: 중복 page id입니다: ${pageId}`);
      }
      pageIds.add(pageId);

      if (mode === "meaning" && !(list(step.units).length || list(step.items).length)) {
        errors.push(`${pageIndex + 1}쪽: meaning 페이지에 units가 없습니다.`);
      }
      if (["parallel", "writing"].includes(mode) && !list(step.items).length) {
        errors.push(`${pageIndex + 1}쪽: ${mode} 페이지에 items가 없습니다.`);
      }
      if (mode === "correction" && !(list(step.rows).length || list(step.corrections).length)) {
        errors.push(`${pageIndex + 1}쪽: correction 페이지에 rows가 없습니다.`);
      }
      if (mode === "paragraph-order" && !list(step.blocks).length) {
        errors.push(`${pageIndex + 1}쪽: paragraph-order 페이지에 blocks가 없습니다.`);
      }
    });

    const stringValues = collectStringValues(workbook.rawData);
    if (stringValues.some((value) => /class=(?:"|')[^"']*\bsolution-value\b/i.test(value))) {
      errors.push("입력 데이터가 예약 클래스 solution-value를 직접 포함합니다.");
    }
    if (stringValues.some((value) => (
      /style=(?:"|')[^"']*(?:#d71920|rgb\(\s*215\s*,\s*25\s*,\s*32\s*\))/i.test(value)
    ))) {
      errors.push("입력 데이터가 정답 전용 빨강을 인라인 스타일로 포함합니다.");
    }

    return errors;
  }

  function sanitizeFragment(source, { study = false } = {}) {
    const template = document.createElement("template");
    template.innerHTML = text(source);

    template.content
      .querySelectorAll("script, style, iframe, object, embed, link, meta, form, input, button, textarea, select")
      .forEach((node) => node.remove());

    const allowedTags = new Set(["STRONG", "SPAN", "EM", "SUP", "SUB", "BR"]);
    const allowedClasses = /^(?:blank|answer-fill|correction-target|vocab|gloss|vocab-[1-8])$/;

    Array.from(template.content.querySelectorAll("*")).forEach((node) => {
      Array.from(node.attributes).forEach((attribute) => {
        const name = attribute.name.toLowerCase();
        if (name.startsWith("on") || name === "style" || name === "id") {
          node.removeAttribute(attribute.name);
          return;
        }

        if (name === "class") {
          const kept = attribute.value
            .split(/\s+/)
            .filter((className) => allowedClasses.test(className));
          if (kept.length) node.setAttribute("class", kept.join(" "));
          else node.removeAttribute("class");
          return;
        }

        if (name === "data-target-id") return;
        if (name === "data-meaning" && study) return;
        node.removeAttribute(attribute.name);
      });

      if (!allowedTags.has(node.tagName)) {
        node.replaceWith(...Array.from(node.childNodes));
      }
    });

    if (!study) {
      template.content.querySelectorAll("strong, em").forEach((node) => {
        node.replaceWith(...Array.from(node.childNodes));
      });
      template.content.querySelectorAll(".vocab, .gloss, .answer-fill").forEach((node) => {
        const preserved = Array.from(node.classList).filter((className) => className === "blank");
        if (preserved.length) node.setAttribute("class", preserved.join(" "));
        else node.removeAttribute("class");
        node.removeAttribute("data-meaning");
      });
    }

    return template;
  }

  function createSolutionContext(solutions, scopeLabel) {
    const mapping = isObject(solutions) ? solutions : {};
    const used = new Set();
    const targets = new Set();

    return {
      has(targetId) {
        return hasOwn(mapping, text(targetId).trim());
      },

      target(targetId, fallbackValue) {
        const id = text(targetId).trim();
        if (!id) {
          pushDiagnostic(`${scopeLabel}: data-target-id가 비어 있습니다.`);
          return activeEdition === "answer" ? fallbackValue : undefined;
        }
        if (targets.has(id)) {
          pushDiagnostic(`${scopeLabel}: target id가 중복되었습니다: ${id}`);
        }
        targets.add(id);

        if (hasOwn(mapping, id)) {
          used.add(id);
          return activeEdition === "answer" ? mapping[id] : undefined;
        }
        if (activeEdition === "answer" && fallbackValue !== undefined && fallbackValue !== "") {
          return fallbackValue;
        }
        if (activeEdition === "answer") {
          pushDiagnostic(`${scopeLabel}: 정답이 없는 target입니다: ${id}`);
        }
        return undefined;
      },

      finish() {
        if (activeEdition !== "answer") return;
        Object.keys(mapping).forEach((targetId) => {
          if (!used.has(targetId) && !targets.has(targetId)) {
            pushDiagnostic(`${scopeLabel}: 사용되지 않은 solution target입니다: ${targetId}`);
          }
        });
      }
    };
  }

  function appendSolutionValue(slot, solution) {
    if (activeEdition !== "answer") return;
    const value = answerText(solution);
    if (!value) return;
    const answer = document.createElement("span");
    answer.className = "solution-value";
    answer.textContent = value;
    slot.append(answer);
  }

  function applySolutionSlotLayout(slot) {
    if (!slot || slot.classList.contains("block-solution")) return;
    const targetId = text(slot.dataset.targetId).trim();
    const layout = isObject(activeSolutionSlotLayouts[targetId])
      ? activeSolutionSlotLayouts[targetId]
      : null;
    if (!layout) return;
    const width = Number(layout.widthPx);
    const height = Number(layout.heightPx);
    if (!(Number.isFinite(width) && width > 0 && Number.isFinite(height) && height > 0)) {
      pushDiagnostic(`정답 자리 측정값이 올바르지 않습니다: ${targetId}`);
      return;
    }
    slot.classList.add("solution-layout-locked");
    slot.style.setProperty("--solution-slot-width", `${width}px`);
    slot.style.setProperty("--solution-slot-height", `${height}px`);
  }

  function prepareExplicitTargets(template, solutionContext) {
    template.content.querySelectorAll("[data-target-id]").forEach((target) => {
      const targetId = text(target.dataset.targetId).trim();
      const originalChildren = Array.from(target.childNodes);
      const isBlank = target.classList.contains("blank");

      target.classList.add("solution-slot");
      if (!isBlank) target.classList.add("choice-slot");
      target.replaceChildren();

      const prompt = document.createElement("span");
      prompt.className = "slot-prompt";
      prompt.append(...originalChildren);
      target.append(prompt);

      appendSolutionValue(target, solutionContext.target(targetId));
      applySolutionSlotLayout(target);
    });
  }

  function renderRichText(source, solutionContext, options = {}) {
    const template = sanitizeFragment(source, options);
    prepareExplicitTargets(template, solutionContext);
    return template.innerHTML;
  }

  function splitOutsideTags(source) {
    const parts = [];
    let current = "";
    let inTag = false;

    for (const character of text(source)) {
      if (character === "<") {
        inTag = true;
        current += character;
      } else if (character === ">") {
        inTag = false;
        current += character;
      } else if (character === "/" && !inTag) {
        parts.push(current);
        current = "";
      } else {
        current += character;
      }
    }
    parts.push(current);
    return parts;
  }

  function renderInlineGloss(en, hint, scopeLabel) {
    const enParts = splitOutsideTags(en);
    const hintParts = splitOutsideTags(hint);

    if (enParts.length !== hintParts.length) {
      pushDiagnostic(
        `${scopeLabel}: en 의미 단위 ${enParts.length}개와 hint 의미 단위 ${hintParts.length}개가 다릅니다.`
      );
    }

    return enParts.map((enPart, index) => {
      const english = sanitizeFragment(enPart, { study: true }).innerHTML.trim();
      const meaning = sanitizeFragment(hintParts[index] || "", { study: true }).innerHTML.trim();
      const slash = index < enParts.length - 1
        ? '<span class="slash" aria-hidden="true">/</span>'
        : "";
      return `
        <span class="unit-chunk">
          <span class="segment-gloss">
            ${english}
            <span class="segment-meaning">${meaning}</span>
          </span>
        </span>
        ${slash}
      `;
    }).join("");
  }

  function stepLabel(step) {
    return [step.no, step.title, step.part]
      .map((part) => text(part).trim())
      .filter(Boolean)
      .map(escapeHtml)
      .join(" ");
  }

  function pageIdentity(entry, pageIndex) {
    return text(
      entry.page.pageId ||
      entry.step.pageId ||
      entry.page.id ||
      entry.step.id ||
      `page-${pageIndex + 1}`
    );
  }

  function renderMasthead(metadata, step) {
    return `
      <header class="masthead">
        <div class="mast-meta">
          <span class="lesson-chip">${escapeHtml(metadata.no || metadata.lesson || "")}</span>
          <span class="kicker">${escapeHtml(metadata.kicker || "")}</span>
          ${metadata.grade ? `<span class="grade-chip">${escapeHtml(metadata.grade)}</span>` : ""}
        </div>
        <div class="step-title">${stepLabel(step)}</div>
      </header>
    `;
  }

  function renderInstruction(step) {
    return `
      <section class="instruction">
        <p class="instruction-text">${escapeHtml(step.instruction || "")}</p>
      </section>
    `;
  }

  function renderStandaloneSolutionSlot(targetId, solution, className = "") {
    const classes = ["solution-slot", safeClassNames(className)].filter(Boolean).join(" ");
    const slot = document.createElement("span");
    slot.className = classes;
    slot.dataset.targetId = text(targetId);

    const prompt = document.createElement("span");
    prompt.className = "slot-prompt";
    slot.append(prompt);
    appendSolutionValue(slot, solution);
    applySolutionSlotLayout(slot);
    return slot.outerHTML;
  }

  function renderStudySummary(metadata, step, pageId) {
    const showSummary = step.mode === "meaning" || step.showStudySummary;
    const answer = isObject(metadata.answer) ? metadata.answer : {};
    const showAnswer = Boolean(
      metadata.showAnswerSummary ||
      answer.label ||
      answer.prompt ||
      answer.solution ||
      answer.text
    );
    if (!showSummary || (!metadata.topic && !showAnswer)) return "";

    const summaryTargetId = text(answer.targetId || `${pageId}-summary-answer`);
    const summarySolution = activeEdition === "answer"
      ? (answer.solution !== undefined ? answer.solution : answer.text)
      : undefined;

    return `
      <section class="study-summary">
        ${metadata.topic ? `
          <section class="topic-line">
            <div class="topic-label">주제 한 문장</div>
            <div class="topic-write">${escapeHtml(metadata.topic)}</div>
          </section>
        ` : ""}
        ${showAnswer ? `
          <section class="answer-line">
            <div class="answer-label">${escapeHtml(answer.label || "정답 확인")}</div>
            <div class="answer-write">
              ${renderStandaloneSolutionSlot(summaryTargetId, summarySolution, "summary-solution")}
            </div>
            <div class="answer-check">${escapeHtml(answer.check || "검토 완료")}</div>
          </section>
        ` : ""}
      </section>
    `;
  }

  function fieldDefinitions(step) {
    return list(step.fields).length
      ? step.fields
      : [
          { key: "en", className: "english" },
          { key: "ko", className: "korean" }
        ];
  }

  function renderField(field, item, solutionContext) {
    const key = text(field.key);
    const source = item[key];
    if (source === undefined || source === null || source === "") return "";

    return `
      <div class="field-row">
        ${field.label ? `<div class="field-label">${escapeHtml(field.label)}</div>` : ""}
        <p class="${safeClassNames(field.className || "")}">
          ${renderRichText(source, solutionContext)}
        </p>
      </div>
    `;
  }

  function renderBank(item, solutionContext) {
    if (!item.bank) return "";
    return `
      <div class="word-bank">
        <span class="bank-label">${escapeHtml(item.bankLabel || "제시어")}</span>
        <span class="bank-text">${renderRichText(item.bank, solutionContext)}</span>
      </div>
    `;
  }

  function itemResponseTargetId(item, pageId, itemIndex) {
    return text(
      item.responseTargetId ||
      item.solutionTargetId ||
      item.answerTargetId ||
      `${pageId}-item-${item.no || itemIndex + 1}-response`
    );
  }

  function legacyBoxSolution(item) {
    const keys = ["solution", "answerText", "model", "answer", "enAnswer", "koAnswer"];
    const key = keys.find((candidate) => item[candidate] !== undefined && item[candidate] !== "");
    return key ? item[key] : undefined;
  }

  function responseTrace(item, targetId) {
    const layout = isObject(item.responseLayout) ? item.responseLayout : {};
    const lines = list(layout.lines);
    if (!lines.length) return "";
    const metric = (value) => {
      const number = Number(value);
      return Number.isFinite(number) && number >= 0 ? number : 0;
    };
    return `
      <div class="response-trace" data-target-id="${escapeAttribute(targetId)}" aria-hidden="true">
        ${lines.map((line, index) => `
          <span
            class="response-trace-line"
            data-line-index="${index}"
            style="left:${metric(line.leftPx)}px;top:${metric(line.topPx)}px;width:${metric(line.widthPx)}px;height:${metric(line.heightPx)}px"
          ></span>
        `).join("")}
      </div>
    `;
  }

  function renderAnswerBox(item, solutionContext, pageId, itemIndex, forcedLines) {
    const lines = Number(forcedLines || item.lines || 0);
    const targetId = itemResponseTargetId(item, pageId, itemIndex);
    const fallback = legacyBoxSolution(item);
    const hasResponseArea = Boolean(
      lines ||
      item.answerHeight ||
      fallback !== undefined ||
      item.responseTargetId ||
      item.solutionTargetId ||
      item.answerTargetId
    );
    if (!hasResponseArea) return "";

    const lineCount = Math.max(2, lines || 2);
    const calculatedHeight = `${lineCount * 6}mm`;
    const height = item.keepAnswerHeight
      ? safeCssLength(item.answerHeight, calculatedHeight)
      : calculatedHeight;
    const expectsSolution = Boolean(
      item.responseTargetId ||
      item.solutionTargetId ||
      item.answerTargetId ||
      fallback !== undefined ||
      solutionContext.has(targetId)
    );
    const solution = expectsSolution
      ? solutionContext.target(targetId, fallback)
      : undefined;
    const trace = responseTrace(item, targetId);

    return `
      <div class="write-box ${trace ? "response-layout-locked" : ""}" style="--answer-height: ${height}">
        ${item.writeLabel ? `<div class="write-label">${escapeHtml(item.writeLabel)}</div>` : ""}
        ${renderStandaloneSolutionSlot(targetId, solution, "block-solution")}
        ${trace}
        ${trace ? "" : Array.from({ length: lines || 2 }, () => '<div class="write-line"></div>').join("")}
      </div>
    `;
  }

  function itemScopeLabel(pageId, item, itemIndex) {
    return `${pageId} ${item.no || itemIndex + 1}번`;
  }

  function renderMeaning(step, pageId) {
    const units = list(step.units).length ? step.units : list(step.items);
    return `
      <section class="work-area meaning-work-area">
        <section class="meaning-board">
          <div class="meaning-board-head">
            <div>No.</div>
            <div>원문 의미 단위</div>
          </div>
          <div class="meaning-list">
            ${units.map((unit, unitIndex) => {
              const unitNo = unit.no || unitIndex + 1;
              return `
                <section class="meaning-row">
                  <div class="meaning-cell unit-no">${escapeHtml(String(unitNo).padStart(2, "0"))}</div>
                  <div class="meaning-cell text-cell">
                    <p class="english inline-gloss">
                      ${renderInlineGloss(unit.en, unit.hint, `${pageId} ${unitNo}번`)}
                    </p>
                    ${unit.lines
                      ? `<div class="lines">${Array.from(
                          { length: Number(unit.lines) },
                          () => '<div class="write-line"></div>'
                        ).join("")}</div>`
                      : ""}
                  </div>
                </section>
              `;
            }).join("")}
          </div>
        </section>
      </section>
    `;
  }

  function renderParallel(step, pageId) {
    const fields = fieldDefinitions(step);
    const isReading = step.layout === "reading";

    return `
      <section class="work-area item-work-area">
        <div class="item-list">
          ${list(step.items).map((item, itemIndex) => {
            const scopeLabel = itemScopeLabel(pageId, item, itemIndex);
            const solutionContext = createSolutionContext(item.solutions, scopeLabel);
            const markup = `
              <section class="practice-item">
                <div class="item-no">${escapeHtml(item.no || itemIndex + 1)}</div>
                <div class="item-main ${isReading ? "reading-grid" : ""}">
                  ${fields.map((field) => renderField(field, item, solutionContext)).join("")}
                  ${renderBank(item, solutionContext)}
                  ${renderAnswerBox(item, solutionContext, pageId, itemIndex)}
                </div>
              </section>
            `;
            solutionContext.finish();
            return markup;
          }).join("")}
        </div>
      </section>
    `;
  }

  function isCompositionStep(step) {
    return /영작/.test([step.title, step.instruction].map(text).join(" "));
  }

  function renderWriting(step, pageId) {
    const isComposition = isCompositionStep(step);

    return `
      <section class="work-area item-work-area">
        <div class="item-list">
          ${list(step.items).map((item, itemIndex) => {
            const scopeLabel = itemScopeLabel(pageId, item, itemIndex);
            const solutionContext = createSolutionContext(item.solutions, scopeLabel);
            const markup = `
              <section class="practice-item">
                <div class="item-no">${escapeHtml(item.no || itemIndex + 1)}</div>
                <div class="item-main">
                  ${item.ko
                    ? `<p class="korean">${renderRichText(item.ko, solutionContext)}</p>`
                    : ""}
                  ${!isComposition && item.en
                    ? `<p class="english">${renderRichText(item.en, solutionContext)}</p>`
                    : ""}
                  ${item.prompt
                    ? `<p class="prompt">${renderRichText(item.prompt, solutionContext)}</p>`
                    : ""}
                  ${renderBank(item, solutionContext)}
                  ${renderAnswerBox(item, solutionContext, pageId, itemIndex, item.lines || 3)}
                </div>
              </section>
            `;
            solutionContext.finish();
            return markup;
          }).join("")}
        </div>
      </section>
    `;
  }

  function rowSolutions(row) {
    return isObject(row.solutions) ? row.solutions : {};
  }

  function renderCorrectionOriginalSlot(targetId, original) {
    const slot = document.createElement("span");
    slot.className = "solution-slot correction-entry";
    slot.dataset.targetId = text(targetId);

    const prompt = document.createElement("span");
    prompt.className = "slot-prompt";
    slot.append(prompt);

    if (activeEdition === "answer") {
      const value = answerText(original);
      if (value) {
        const sourceValue = document.createElement("span");
        sourceValue.className = "correction-original";
        sourceValue.textContent = value;
        slot.append(sourceValue);
      }
    }
    applySolutionSlotLayout(slot);
    return slot.outerHTML;
  }

  function renderCorrection(step, pageId) {
    const rows = list(step.corrections).length ? step.corrections : list(step.rows);
    return `
      <section class="work-area">
        <div class="correction-passage">
          <p class="english">${sanitizeFragment(step.passage).innerHTML}</p>
        </div>
        <div class="correction-rows">
          ${rows.map((row, rowIndex) => {
            const scopeLabel = `${pageId} 교정 ${row.no || rowIndex + 1}번`;
            const solutions = rowSolutions(row);
            const solutionContext = createSolutionContext(solutions, scopeLabel);
            const beforeId = text(
              row.beforeTargetId ||
              row.wrongTargetId ||
              `${pageId}-correction-${row.no || rowIndex + 1}-before`
            );
            const afterId = text(
              row.afterTargetId ||
              row.correctTargetId ||
              `${pageId}-correction-${row.no || rowIndex + 1}-after`
            );
            const before = solutionContext.target(
              beforeId,
              row.wrong !== undefined ? row.wrong : (row.before !== undefined ? row.before : row.original)
            );
            const after = solutionContext.target(
              afterId,
              row.correct !== undefined ? row.correct : (row.after !== undefined ? row.after : row.answer)
            );
            const markup = `
              <div class="correction-row">
                <span class="correction-no">(${escapeHtml(row.no || rowIndex + 1)})</span>
                ${renderCorrectionOriginalSlot(beforeId, before)}
                <span class="arrow">&rarr;</span>
                ${renderStandaloneSolutionSlot(afterId, after, "correction-entry")}
              </div>
            `;
            solutionContext.finish();
            return markup;
          }).join("")}
        </div>
      </section>
    `;
  }

  function sequenceSolutions(step) {
    if (isObject(step.solutions)) return step.solutions;
    const legacy = list(step.sequenceAnswer || step.answer || step.solution);
    return Object.fromEntries(legacy.map((value, index) => [
      text(list(step.sequenceTargetIds)[index] || `sequence-${index + 1}`),
      value
    ]));
  }

  function renderParagraphOrder(step, pageId) {
    const idsFromData = list(step.sequenceTargetIds).map(text);
    const solutionMap = sequenceSolutions(step);
    const slotCount = Number(step.sequenceSlots) || idsFromData.length || Object.keys(solutionMap).length || 3;
    const targetIds = Array.from({ length: slotCount }, (_, index) => (
      idsFromData[index] || `${pageId}-sequence-${index + 1}`
    ));
    const normalizedSolutions = {};

    Object.entries(solutionMap).forEach(([key, value], index) => {
      const resolvedKey = key.startsWith("sequence-") && !idsFromData.length
        ? targetIds[index]
        : key;
      normalizedSolutions[resolvedKey] = value;
    });

    const solutionContext = createSolutionContext(normalizedSolutions, `${pageId} 문단 배열`);
    const sequenceMarkup = targetIds.map((targetId, index) => {
      const solution = solutionContext.target(targetId);
      return `
        ${index ? '<span class="sequence-arrow">&rarr;</span>' : ""}
        ${renderStandaloneSolutionSlot(targetId, solution, "sequence-slot")}
      `;
    }).join("");
    solutionContext.finish();

    return `
      <section class="work-area">
        <div class="paragraph-list">
          ${step.intro ? `<p class="english">${sanitizeFragment(step.intro).innerHTML}</p>` : ""}
          ${list(step.blocks).map((block) => `
            <div class="paragraph-block">
              <div class="paragraph-label">${escapeHtml(block.label)}</div>
              <p class="paragraph">${sanitizeFragment(block.text).innerHTML}</p>
            </div>
          `).join("")}
          ${step.outro ? `<p class="english">${sanitizeFragment(step.outro).innerHTML}</p>` : ""}
          <div class="sequence-row">${sequenceMarkup}</div>
        </div>
      </section>
    `;
  }

  function renderStepBody(step, pageId) {
    const mode = step.mode || "parallel";
    if (mode === "meaning") return renderMeaning(step, pageId);
    if (mode === "writing") return renderWriting(step, pageId);
    if (mode === "correction") return renderCorrection(step, pageId);
    if (mode === "paragraph-order") return renderParagraphOrder(step, pageId);
    return renderParallel(step, pageId);
  }

  function footerLogo(workbook, entry) {
    return text(
      entry.page.footerLogo ||
      entry.metadata.footerLogo ||
      workbook.metadata.footerLogo ||
      DEFAULT_FOOTER_LOGO
    );
  }

  function renderFooter(workbook, entry, pageNumber) {
    const logo = footerLogo(workbook, entry);
    return `
      <footer class="footer">
        <span></span>
        <span>- ${escapeHtml(pageNumber)} -</span>
        <span>
          ${logo
            ? `<img class="footer-logo-mark" src="${escapeAttribute(logo)}" alt="" />`
            : ""}
        </span>
      </footer>
    `;
  }

  function renderPage(workbook, entry, pageIndex) {
    const step = entry.step;
    const pageId = pageIdentity(entry, pageIndex);
    const pageNumber = entry.page.pageNo || entry.page.page || pageIndex + 1;
    const stageId = entry.page.stageId || step.stageId || step.no || "";

    return `
      <article
        class="page"
        data-page-id="${escapeAttribute(pageId)}"
        data-page-no="${escapeAttribute(pageNumber)}"
        data-stage-id="${escapeAttribute(stageId)}"
      >
        <div class="sheet">
          ${renderMasthead(entry.metadata, step)}
          ${renderInstruction(step)}
          ${renderStudySummary(entry.metadata, step, pageId)}
          ${renderStepBody(step, pageId)}
          ${renderFooter(workbook, entry, pageNumber)}
        </div>
      </article>
    `;
  }

  function renderWorkbook(workbook) {
    pagesRoot.innerHTML = workbook.pages
      .map((entry, pageIndex) => renderPage(workbook, entry, pageIndex))
      .join("");
  }

  function resourceTimeout(label) {
    return new Promise((_, reject) => {
      window.setTimeout(
        () => reject(new Error(`${label} 로드를 ${RESOURCE_TIMEOUT_MS / 1000}초 안에 완료하지 못했습니다.`)),
        RESOURCE_TIMEOUT_MS
      );
    });
  }

  async function waitForFonts() {
    if (!document.fonts || !document.fonts.ready) return;
    await Promise.race([document.fonts.ready, resourceTimeout("폰트")]);
  }

  async function waitForImage(image) {
    const source = image.currentSrc || image.src || "이미지";
    if (image.complete) {
      if (!image.naturalWidth) throw new Error(`이미지 로드 실패: ${source}`);
      if (typeof image.decode === "function") {
        await image.decode().catch(() => undefined);
      }
      return;
    }

    await Promise.race([
      new Promise((resolve, reject) => {
        image.addEventListener("load", resolve, { once: true });
        image.addEventListener(
          "error",
          () => reject(new Error(`이미지 로드 실패: ${source}`)),
          { once: true }
        );
      }),
      resourceTimeout(`이미지 ${source}`)
    ]);
  }

  function nextFrame() {
    return new Promise((resolve) => window.requestAnimationFrame(() => resolve()));
  }

  async function waitForLayoutResources() {
    await Promise.all([
      waitForFonts(),
      ...Array.from(document.images).map(waitForImage)
    ]);
    await nextFrame();
    await nextFrame();
  }

  function detectSolutionDomErrors() {
    const errors = [];
    const solutionValues = Array.from(document.querySelectorAll(".solution-value"));

    if (activeEdition === "student" && solutionValues.length) {
      errors.push("학생용 문서에 solution-value가 렌더링되었습니다.");
    }

    solutionValues.forEach((value, index) => {
      const parent = value.parentElement;
      if (!parent || !parent.classList.contains("solution-slot")) {
        errors.push(`${index + 1}번째 solution-value가 solution-slot 밖에 있습니다.`);
      }
    });

    const targetIds = new Set();
    document.querySelectorAll(".solution-slot[data-target-id]").forEach((slot) => {
      const targetId = text(slot.dataset.targetId).trim();
      if (!targetId) {
        errors.push("data-target-id가 비어 있는 solution-slot이 있습니다.");
      } else if (targetIds.has(targetId)) {
        errors.push(`문서 전체에서 target id가 중복되었습니다: ${targetId}`);
      }
      targetIds.add(targetId);
    });

    if (document.querySelector(".solution, .filled-answer, .solution-text, .solution-line")) {
      errors.push("구형 답지 전용 클래스가 렌더링되었습니다.");
    }

    return errors;
  }

  function detectPageOverflowErrors() {
    return Array.from(document.querySelectorAll(".page")).flatMap((page, index) => {
      const errors = [];
      const sheet = page.querySelector(".sheet") || page;
      const sheetRect = sheet.getBoundingClientRect();
      const pageRect = page.getBoundingClientRect();
      const scrollOverflow = Math.max(
        sheet.scrollHeight - sheet.clientHeight,
        sheet.scrollWidth - sheet.clientWidth,
        page.scrollHeight - page.clientHeight,
        page.scrollWidth - page.clientWidth
      );
      const childBottom = Array.from(sheet.children).reduce((bottom, child) => {
        const style = window.getComputedStyle(child);
        if (style.display === "none") return bottom;
        return Math.max(bottom, child.getBoundingClientRect().bottom);
      }, sheetRect.top);
      const visualOverflow = Math.max(
        childBottom - sheetRect.bottom,
        sheetRect.right - pageRect.right,
        pageRect.left - sheetRect.left
      );
      const overflowAmount = Math.ceil(Math.max(scrollOverflow, visualOverflow));

      if (overflowAmount > OVERFLOW_TOLERANCE_PX) {
        const title = page.querySelector(".step-title")?.textContent.trim() || "단계 정보 없음";
        errors.push(
          `${index + 1}쪽 ${title}: 내용이 페이지 경계를 ${overflowAmount}px 넘습니다.`
        );
      }

      page.querySelectorAll(".work-area").forEach((area) => {
        const hiddenOverflow = Math.ceil(Math.max(
          area.scrollHeight - area.clientHeight,
          area.scrollWidth - area.clientWidth
        ));
        if (hiddenOverflow > OVERFLOW_TOLERANCE_PX) {
          errors.push(`${index + 1}쪽: 작업 영역 안의 내용이 ${hiddenOverflow}px 잘립니다.`);
        }
      });

      const footer = sheet.querySelector(".footer");
      if (footer) {
        const footerTop = footer.getBoundingClientRect().top;
        const preceding = Array.from(footer.parentElement.children).filter((child) => child !== footer);
        const precedingBottom = preceding.reduce(
          (bottom, child) => Math.max(bottom, child.getBoundingClientRect().bottom),
          sheetRect.top
        );
        if (precedingBottom - footerTop > OVERFLOW_TOLERANCE_PX) {
          errors.push(`${index + 1}쪽: 본문이 푸터 영역과 겹칩니다.`);
        }
      }

      return errors;
    });
  }

  function validateRenderedWorkbook(expectedPageCount) {
    const errors = [
      ...diagnostics,
      ...detectSolutionDomErrors(),
      ...detectPageOverflowErrors()
    ];
    const actualPageCount = document.querySelectorAll(".page").length;

    if (actualPageCount !== expectedPageCount) {
      errors.push(`고정 페이지 ${expectedPageCount}개 중 ${actualPageCount}개만 렌더링되었습니다.`);
    }

    return errors;
  }

  async function bootstrap() {
    diagnostics.length = 0;
    documentRoot.dataset.renderValidation = "pending";
    updateStatus("검증 중");

    try {
      if (!pagesRoot) throw new Error("#pages 요소가 없습니다.");

      const workbook = normalizeWorkbook(window.WORKBOOK_DATA);
      activeEdition = workbook.edition;
      activeSolutionSlotLayouts = isObject(workbook.rawData.solutionSlotLayouts)
        ? workbook.rawData.solutionSlotLayouts
        : {};
      documentRoot.dataset.workbookEdition = activeEdition;
      document.body.classList.remove("edition-student", "edition-answer");
      document.body.classList.add(`edition-${activeEdition}`);

      const title = text(
        workbook.metadata.documentTitle ||
        workbook.rawData.documentTitle ||
        (activeEdition === "answer" ? "10단계 워크북 해설" : "10단계 워크북")
      );
      const screenTitle = text(
        workbook.metadata.screenTitle ||
        workbook.rawData.screenTitle ||
        title
      );
      document.title = title;
      if (screenTitleNode) screenTitleNode.textContent = screenTitle;

      const structureErrors = validateStructure(workbook);
      if (structureErrors.length) {
        renderFailure(structureErrors, "워크북 데이터 검토 오류");
        return { ok: false, errors: structureErrors };
      }

      renderWorkbook(workbook);
      if (diagnostics.length) {
        renderFailure(diagnostics, "워크북 데이터 검토 오류");
        return { ok: false, errors: [...diagnostics] };
      }

      await waitForLayoutResources();
      const renderedErrors = validateRenderedWorkbook(workbook.pages.length);
      if (renderedErrors.length) {
        renderFailure(renderedErrors, "워크북 렌더링 검토 오류");
        return { ok: false, errors: renderedErrors };
      }

      documentRoot.dataset.renderValidation = "ok";
      documentRoot.dataset.renderPageCount = String(workbook.pages.length);
      updateStatus("검증 완료");
      return {
        ok: true,
        edition: activeEdition,
        pageCount: workbook.pages.length,
        version: VERSION
      };
    } catch (error) {
      const errors = [formatError(error)];
      renderFailure(errors);
      return { ok: false, errors };
    }
  }

  if (printButton) {
    printButton.addEventListener("click", () => {
      if (documentRoot.dataset.renderValidation === "ok") window.print();
    });
  }

  window.addEventListener("error", (event) => {
    if (documentRoot.dataset.renderValidation !== "pending") return;
    renderFailure([event.error || event.message]);
  });

  window.addEventListener("unhandledrejection", (event) => {
    if (documentRoot.dataset.renderValidation !== "pending") return;
    renderFailure([event.reason]);
  });

  const ready = bootstrap();
  window.__WORKBOOK_RENDER_READY__ = ready;
  window.WorkbookRenderer = Object.freeze({
    version: VERSION,
    ready,
    render: bootstrap
  });
})();
