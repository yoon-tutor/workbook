"""Standard tool response envelope shared by every MCP service (STANDARD.md 6.4)."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

STATUSES = frozenset({"ok", "needs_input", "invalid_input", "rejected", "needs_review", "done", "error"})
FAILURE_STATUSES = frozenset({"invalid_input", "rejected", "error"})


def violation(field: str, message: str, expected: Any = None) -> dict[str, Any]:
    item: dict[str, Any] = {"field": field, "message": message}
    if expected is not None:
        item["expected"] = expected
    return item


def next_action(instruction: str, tool: str | None = None, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
    action: dict[str, Any] = {"instruction": instruction}
    if tool:
        action["tool"] = tool
    if arguments:
        action["arguments"] = dict(arguments)
    return action


def envelope(
    status: str,
    *,
    service: Mapping[str, str],
    stage: str | None = None,
    next_action: Mapping[str, Any] | None = None,
    data: Mapping[str, Any] | None = None,
    violations: Iterable[Mapping[str, Any]] = (),
    artifacts: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the one response shape every tool returns as structured content."""
    if status not in STATUSES:
        raise ValueError(f"Unknown envelope status: {status}")
    items = [dict(item) for item in violations]
    if status in {"invalid_input", "rejected"} and not items:
        raise ValueError(f"{status} responses must list violations")
    if not {"name", "version"} <= set(service):
        raise ValueError("service must contain name and version")
    return {
        "status": status,
        "stage": stage,
        "next_action": dict(next_action) if next_action else None,
        "data": dict(data or {}),
        "violations": items,
        "artifacts": dict(artifacts) if artifacts else None,
        "service": {"name": service["name"], "version": service["version"]},
    }


def validate_envelope(value: Any) -> list[str]:
    """Return problems with a response; used by every service's envelope tests."""
    if not isinstance(value, dict):
        return ["response is not an object"]
    problems = []
    expected = {"status", "stage", "next_action", "data", "violations", "artifacts", "service"}
    if set(value) != expected:
        problems.append(f"keys {sorted(value)} != {sorted(expected)}")
    if value.get("status") not in STATUSES:
        problems.append(f"unknown status {value.get('status')!r}")
    if not isinstance(value.get("data"), dict):
        problems.append("data is not an object")
    if not isinstance(value.get("violations"), list):
        problems.append("violations is not a list")
    elif value.get("status") in {"invalid_input", "rejected"} and not value["violations"]:
        problems.append("failure without violations")
    action = value.get("next_action")
    if action is not None and not (isinstance(action, dict) and isinstance(action.get("instruction"), str)):
        problems.append("next_action must be null or contain instruction")
    service = value.get("service")
    if not (isinstance(service, dict) and service.get("name") and service.get("version")):
        problems.append("service name/version missing")
    return problems
