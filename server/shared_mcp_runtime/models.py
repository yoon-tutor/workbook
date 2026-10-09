"""Product-independent ports for the shared TOEFL identity and usage tables."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ApiKeyIdentity:
    key_id: str
    user_id: str
    scopes: tuple[str, ...]
    expires_at: datetime | None


@dataclass(frozen=True, slots=True)
class UsageEvent:
    """One tool attempt, without source text, tokens, or tool arguments.

    ``event_id`` deduplicates persistence retries for this attempt. A new MCP
    request is a new attempt, even if the caller reuses a JSON-RPC request ID.
    These operational events are not an exactly-once billing ledger.
    """

    user_id: str
    tool_name: str
    contract_id: str | None
    outcome: str
    latency_ms: int
    created_at: datetime
    service_name: str
    event_id: str = field(default_factory=lambda: str(uuid4()))


@runtime_checkable
class ApiKeyStore(Protocol):
    def create_user(self, user_id: str, email: str, name: str, status: str = "active") -> None: ...

    def save_api_key(self, key_id: str, user_id: str, key_hash: str,
                     scopes: tuple[str, ...], expires_at: datetime | None) -> None: ...

    def find_api_key(self, key_hash: str) -> ApiKeyIdentity | None: ...

    def touch_api_key(self, key_id: str, used_at: datetime) -> None: ...

    def set_api_key_enabled(self, key_id: str, enabled: bool) -> None: ...


@runtime_checkable
class UsageStore(Protocol):
    def record_usage(self, event: UsageEvent) -> None: ...
