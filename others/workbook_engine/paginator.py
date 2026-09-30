"""Deterministic page splitting for logical workbook stages."""

from __future__ import annotations

from math import ceil
from typing import Any, Iterable


DEFAULT_PAGE_TARGETS = {
    "1": 12,
    "2": 14,
    "3": 14,
    "4": 10,
    "5": 14,
    "6": 14,
    "8": 6,
    "10": 8,
}

DEFAULT_PAGE_MAXIMUMS = {
    **DEFAULT_PAGE_TARGETS,
    "1": 13,
    "4": 11,
}


def chunks(items: list[Any], size: int) -> Iterable[tuple[int, list[Any]]]:
    if size < 1:
        raise ValueError("Page size must be positive")
    for start in range(0, len(items), size):
        yield start, items[start : start + size]


def balanced_chunks(items: list[Any], maximum: int) -> Iterable[tuple[int, list[Any]]]:
    if maximum < 1:
        raise ValueError("Page maximum must be positive")
    if not items:
        return
    page_count = ceil(len(items) / maximum)
    base_size, larger_pages = divmod(len(items), page_count)
    start = 0
    for page_index in range(page_count):
        size = base_size + (1 if page_index < larger_pages else 0)
        yield start, items[start : start + size]
        start += size


def part_label(start: int, count: int) -> str:
    return f"{start + 1}-{start + count}"


def stage_page_target(spec: dict[str, Any], stage_no: str) -> int:
    stages = []
    if isinstance(spec, dict):
        stages = spec.get("logicalStages") or spec.get("stages") or []
    for stage in stages:
        if str(stage.get("number", stage.get("no"))) != str(stage_no):
            continue
        for key in ("pageTarget", "targetItemsPerPage", "itemsPerPage"):
            value = stage.get(key)
            if isinstance(value, int) and value > 0:
                return value
        pagination = stage.get("pagination")
        if isinstance(pagination, dict):
            for key in ("targetPerPage", "target", "pageTarget", "itemsPerPage"):
                value = pagination.get(key)
                if isinstance(value, int) and value > 0:
                    return value
    return DEFAULT_PAGE_TARGETS.get(str(stage_no), 1)


def stage_page_maximum(spec: dict[str, Any], stage_no: str) -> int:
    stages = []
    if isinstance(spec, dict):
        stages = spec.get("logicalStages") or spec.get("stages") or []
    for stage in stages:
        if str(stage.get("number", stage.get("no"))) != str(stage_no):
            continue
        pagination = stage.get("pagination")
        if isinstance(pagination, dict):
            value = pagination.get("hardMaximum")
            if isinstance(value, int) and value > 0:
                return value
    return DEFAULT_PAGE_MAXIMUMS.get(str(stage_no), stage_page_target(spec, stage_no))


def paginate_stage(
    stage: dict[str, Any],
    spec: dict[str, Any],
    collection_key: str = "items",
) -> list[dict[str, Any]]:
    stage_no = str(stage["no"])
    items = list(stage.get(collection_key, []))
    if not items:
        return [dict(stage)]
    maximum = stage_page_maximum(spec, stage_no)
    pages: list[dict[str, Any]] = []
    for start, page_items in balanced_chunks(items, maximum):
        page = {key: value for key, value in stage.items() if key != collection_key}
        page["part"] = part_label(start, len(page_items))
        page[collection_key] = page_items
        page["logicalItemCount"] = len(items)
        page["pageItemMaximum"] = maximum
        pages.append(page)
    return pages
