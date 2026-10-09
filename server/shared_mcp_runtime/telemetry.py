"""Per-instance burst protection and redacted tool-call telemetry."""

from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from collections.abc import Callable
from datetime import datetime, timezone
import json
import re
import sys
from threading import Lock
import time
from typing import Any
from uuid import uuid4

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools import ToolResult

from .config import INSTANCE_BURST_MAX_CALLS, INSTANCE_BURST_WINDOW_SECONDS
from .models import UsageEvent, UsageStore


_PUBLIC_CONTRACT_ID = re.compile(r"^[A-Za-z0-9_-]{20,128}$")
_PUBLIC_TOOL_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,127}$")
_SAFE_OUTCOMES = frozenset({
    "success", "error", "rate_limited", "invalid_input", "rejected", "fail",
    "pass", "valid", "accepted", "ready", "ready_to_prepare", "ready_for_layout",
    "instructions", "candidate_required", "pending", "pending_layout", "prepared",
    "published", "needs_review", "not_found", "complete", "completed", "ok",
    "awaiting-visual-review", "needs_input", "done",
})
EventSink = Callable[[dict[str, Any]], None]
OwnerProvider = Callable[[], str]


def emit_structured_event(event: dict[str, Any]) -> None:
    """Write exactly one redacted JSON event to stdout."""

    print(
        json.dumps(event, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        file=sys.stdout,
        flush=True,
    )


def emit_stdio_event(event: dict[str, Any]) -> None:
    """Keep stdout exclusively for MCP protocol messages on stdio transports."""
    print(
        json.dumps(event, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        file=sys.stderr,
        flush=True,
    )


class InstanceBurstLimitExceeded(ToolError):
    """A process-local abuse-control limit, not a durable customer quota."""


class InstanceBurstLimiter:
    """Thread-safe sliding window used only for short per-process bursts."""

    def __init__(
        self,
        max_calls: int = INSTANCE_BURST_MAX_CALLS,
        window_seconds: float = INSTANCE_BURST_WINDOW_SECONDS,
    ) -> None:
        if max_calls < 1 or window_seconds <= 0:
            raise ValueError("burst limiter values must be positive")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, owner_id: str, *, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        with self._lock:
            events = self._events[owner_id]
            while events and current - events[0] >= self.window_seconds:
                events.popleft()
            if len(events) >= self.max_calls:
                return False
            events.append(current)
            return True


class BurstProtectionMiddleware(Middleware):
    """Apply the explicitly instance-local burst limit to tool calls only."""

    def __init__(
        self, owner_provider: OwnerProvider, limiter: InstanceBurstLimiter
    ) -> None:
        self._owner_provider = owner_provider
        self._limiter = limiter

    async def on_call_tool(
        self,
        context: MiddlewareContext,
        call_next: CallNext,
    ) -> ToolResult:
        if not self._limiter.allow(self._owner_provider()):
            raise InstanceBurstLimitExceeded("instance burst limit exceeded")
        return await call_next(context)


def _safe_contract_id(arguments: dict[str, Any] | None) -> str | None:
    value = arguments.get("contract_id") if isinstance(arguments, dict) else None
    if isinstance(value, str) and _PUBLIC_CONTRACT_ID.fullmatch(value):
        return value
    return None


def _outcome(result: ToolResult) -> str:
    if result.is_error:
        return "error"
    structured = result.structured_content
    if not isinstance(structured, dict):
        return "success"
    status = structured.get("status")
    if isinstance(status, str) and status in _SAFE_OUTCOMES:
        return status
    return "success"


class StructuredToolTelemetryMiddleware(Middleware):
    """Emit redacted metadata and persist usage without changing tool results."""

    def __init__(
        self,
        owner_provider: OwnerProvider,
        *,
        service_name: str,
        usage_store: UsageStore | None = None,
        event_sink: EventSink = emit_structured_event,
        wall_clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._owner_provider = owner_provider
        self._usage_store = usage_store
        if not service_name or len(service_name) > 128:
            raise ValueError("service_name must have 1-128 characters")
        self._service_name = service_name
        self._event_sink = event_sink
        self._wall_clock = wall_clock
        self._monotonic = monotonic

    def _emit_best_effort(self, event: dict[str, Any]) -> None:
        try:
            self._event_sink(event)
        except Exception:
            # Logging is an operational side effect. A closed stdout pipe or a
            # custom sink failure must never replace the product response.
            pass

    async def on_call_tool(
        self,
        context: MiddlewareContext,
        call_next: CallNext,
    ) -> ToolResult:
        started = self._monotonic()
        created_at = self._wall_clock().astimezone(timezone.utc)
        requested_name = getattr(context.message, "name", "unknown")
        tool_name = (
            requested_name
            if isinstance(requested_name, str) and _PUBLIC_TOOL_NAME.fullmatch(requested_name)
            and not requested_name.startswith("tm_")
            else "unknown"
        )
        arguments = getattr(context.message, "arguments", None)
        contract_id = _safe_contract_id(arguments)
        event_id = str(uuid4())
        try:
            user_id = self._owner_provider()
        except RuntimeError:
            user_id = "unknown"

        result: ToolResult | None = None
        caught: BaseException | None = None
        try:
            result = await call_next(context)
            return result
        except BaseException as exc:
            caught = exc
            raise
        finally:
            latency_ms = max(0, round((self._monotonic() - started) * 1000))
            if isinstance(caught, InstanceBurstLimitExceeded):
                outcome = "rate_limited"
            elif caught is not None:
                outcome = "error"
            elif result is not None:
                outcome = _outcome(result)
            else:
                outcome = "error"
            event = UsageEvent(
                user_id=user_id,
                tool_name=tool_name,
                contract_id=contract_id,
                outcome=outcome,
                latency_ms=latency_ms,
                created_at=created_at,
                service_name=self._service_name,
                event_id=event_id,
            )
            self._emit_best_effort(
                {
                    "event": "tool_call",
                    "event_id": event_id,
                    "service_name": self._service_name,
                    "timestamp": created_at.isoformat().replace("+00:00", "Z"),
                    "user_id": user_id,
                    "tool": tool_name,
                    "contract_id": contract_id,
                    "outcome": outcome,
                    "latency_ms": latency_ms,
                }
            )
            if self._usage_store is not None and user_id != "unknown":
                try:
                    await asyncio.to_thread(self._usage_store.record_usage, event)
                except Exception as exc:
                    # Analytics is best-effort.  Never alter a successful worksheet
                    # response and never include exception messages or call arguments.
                    self._emit_best_effort(
                        {
                            "event": "usage_record_failed",
                            "event_id": event_id,
                            "service_name": self._service_name,
                            "timestamp": created_at.isoformat().replace("+00:00", "Z"),
                            "user_id": user_id,
                            "tool": tool_name,
                            "error_type": type(exc).__name__,
                        }
                    )
