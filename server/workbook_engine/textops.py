"""Text targeting and legacy inline-markup conversion helpers."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Callable, Iterable


BLANK_RE = re.compile(r'<span\s+class=["\']blank["\']\s*></span>', re.I)
PAREN_RE = re.compile(r"\(([^()]*)\)")
CHOICE_RE = re.compile(r"\[([^\[\]]+)\]")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def split_outside_tags(value: str, delimiter: str = "/") -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_tag = False
    for char in value:
        if char == "<":
            in_tag = True
        if char == delimiter and not in_tag:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
        if char == ">":
            in_tag = False
    parts.append("".join(current).strip())
    return parts


@dataclass(frozen=True)
class InlineSpan:
    kind: str
    start: int
    end: int
    text: str
    color_slot: int | None = None
    meaning: str | None = None


class _InlineParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.position = 0
        self.strong_stack: list[int] = []
        self.vocab_stack: list[tuple[int, int, str]] = []
        self.spans: list[InlineSpan] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "strong":
            self.strong_stack.append(self.position)
            return
        if tag != "span":
            return
        attributes = {key: value or "" for key, value in attrs}
        classes = set(attributes.get("class", "").split())
        if "vocab" not in classes:
            return
        color_slot = 0
        for class_name in classes:
            match = re.fullmatch(r"vocab-(\d+)", class_name)
            if match:
                color_slot = int(match.group(1))
                break
        self.vocab_stack.append((self.position, color_slot, attributes.get("data-meaning", "")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "strong" and self.strong_stack:
            start = self.strong_stack.pop()
            text = self.text[start:self.position]
            self.spans.append(InlineSpan("predicate", start, self.position, text))
            return
        if tag == "span" and self.vocab_stack:
            start, color_slot, meaning = self.vocab_stack.pop()
            text = self.text[start:self.position]
            self.spans.append(
                InlineSpan("vocab", start, self.position, text, color_slot=color_slot, meaning=meaning)
            )

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)
        self.position += len(data)

    @property
    def text(self) -> str:
        return "".join(self.text_parts)


def parse_inline_markup(value: str) -> tuple[str, list[InlineSpan]]:
    parser = _InlineParser()
    parser.feed(value)
    parser.close()
    if parser.strong_stack or parser.vocab_stack:
        raise ValueError("Unclosed inline markup")
    return parser.text, sorted(parser.spans, key=lambda span: (span.start, span.end, span.kind))


def occurrence_at(text: str, target: str, start: int) -> int:
    if not target:
        raise ValueError("Target text cannot be empty")
    positions = [match.start() for match in re.finditer(re.escape(target), text)]
    try:
        return positions.index(start) + 1
    except ValueError as error:
        raise ValueError(f"Target {target!r} does not start at {start} in {text!r}") from error


def locate_target(text: str, target: dict[str, Any]) -> tuple[int, int]:
    needle = str(target.get("text", ""))
    occurrence = int(target.get("occurrence", 1))
    if not needle or occurrence < 1:
        raise ValueError(f"Invalid target: {target!r}")
    matches = list(re.finditer(re.escape(needle), text))
    if len(matches) < occurrence:
        raise ValueError(f"Cannot find occurrence {occurrence} of {needle!r} in {text!r}")
    match = matches[occurrence - 1]
    return match.start(), match.end()


def target_from_span(text: str, span: InlineSpan) -> dict[str, Any]:
    return {"text": span.text, "occurrence": occurrence_at(text, span.text, span.start)}


def _assert_non_overlapping(intervals: Iterable[tuple[int, int, str]]) -> None:
    ordered = sorted(intervals)
    for index, (start, end, label) in enumerate(ordered):
        if start >= end:
            raise ValueError(f"Empty target interval: {label}")
        for other_start, other_end, other_label in ordered[index + 1 :]:
            if other_start >= end:
                break
            nested = (start <= other_start and other_end <= end) or (
                other_start <= start and end <= other_end
            )
            if not nested:
                raise ValueError(f"Partially overlapping targets: {label}, {other_label}")


def render_annotated_text(
    text: str,
    predicates: Iterable[dict[str, Any]],
    vocabulary: Iterable[dict[str, Any]],
    language: str,
) -> str:
    intervals: list[dict[str, Any]] = []
    for predicate in predicates:
        targets = predicate.get(language)
        if isinstance(targets, dict):
            targets = [targets]
        for target in targets or []:
            start, end = locate_target(text, target)
            intervals.append({"kind": "predicate", "start": start, "end": end, "data": predicate})
    for vocab in vocabulary:
        target = vocab.get(language)
        if not isinstance(target, dict):
            continue
        start, end = locate_target(text, target)
        intervals.append({"kind": "vocab", "start": start, "end": end, "data": vocab})

    _assert_non_overlapping((item["start"], item["end"], item["kind"]) for item in intervals)
    opens: dict[int, list[dict[str, Any]]] = {}
    closes: dict[int, list[dict[str, Any]]] = {}
    for item in intervals:
        opens.setdefault(item["start"], []).append(item)
        closes.setdefault(item["end"], []).append(item)

    output: list[str] = []
    for position in range(len(text) + 1):
        closing = sorted(
            closes.get(position, []),
            key=lambda item: (item["start"], 0 if item["kind"] == "vocab" else 1),
            reverse=True,
        )
        for item in closing:
            output.append("</span>" if item["kind"] == "vocab" else "</strong>")
        opening = sorted(
            opens.get(position, []),
            key=lambda item: (-item["end"], 0 if item["kind"] == "predicate" else 1),
        )
        for item in opening:
            if item["kind"] == "predicate":
                output.append("<strong>")
            else:
                vocab = item["data"]
                color = int(vocab.get("colorSlot", 1))
                meaning = html.escape(str(vocab.get("meaning", "")), quote=True)
                classes = f"vocab vocab-{color}"
                if language == "en":
                    classes += " gloss"
                    output.append(f'<span class="{classes}" data-meaning="{meaning}">')
                else:
                    output.append(f'<span class="{classes}">')
        if position < len(text):
            output.append(html.escape(text[position]))
    return "".join(output)


def reconstruct_from_tokens(
    template: str,
    pattern: re.Pattern[str],
    answers: list[str],
    token_value: Callable[[re.Match[str]], str] | None = None,
) -> tuple[str, list[tuple[int, int, str, str]]]:
    matches = list(pattern.finditer(template))
    if len(matches) != len(answers):
        raise ValueError(f"Template target count {len(matches)} != answer count {len(answers)}")
    output: list[str] = []
    spans: list[tuple[int, int, str, str]] = []
    cursor = 0
    length = 0
    for index, match in enumerate(matches):
        prefix = html.unescape(template[cursor : match.start()])
        answer = html.unescape(str(answers[index]))
        cue = html.unescape(token_value(match) if token_value else "")
        output.append(prefix)
        length += len(prefix)
        start = length
        output.append(answer)
        length += len(answer)
        spans.append((start, length, answer, cue))
        cursor = match.end()
    suffix = html.unescape(template[cursor:])
    output.append(suffix)
    return "".join(output), spans


def targets_from_spans(base_text: str, spans: Iterable[tuple[int, int, str, str]], prefix: str) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for index, (start, _end, answer, cue) in enumerate(spans, start=1):
        item: dict[str, Any] = {
            "id": f"{prefix}-{index:02d}",
            "target": {"text": answer, "occurrence": occurrence_at(base_text, answer, start)},
        }
        if cue:
            item["cue"] = cue
        targets.append(item)
    return targets


def render_targets(
    base_text: str,
    targets: list[dict[str, Any]],
    render_target: Callable[[dict[str, Any]], str],
) -> str:
    located: list[tuple[int, int, dict[str, Any]]] = []
    for item in targets:
        start, end = locate_target(base_text, item["target"])
        located.append((start, end, item))
    _assert_non_overlapping((start, end, item.get("id", "target")) for start, end, item in located)
    output: list[str] = []
    cursor = 0
    for start, end, item in sorted(located):
        output.append(html.escape(base_text[cursor:start]))
        output.append(render_target(item))
        cursor = end
    output.append(html.escape(base_text[cursor:]))
    return "".join(output)


def fill_targets(base_text: str, targets: list[dict[str, Any]]) -> str:
    return render_targets(base_text, targets, lambda item: html.escape(str(item["target"]["text"])))

