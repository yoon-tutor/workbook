"""Shared PostgreSQL identities and redacted operational usage.

No schema or table is created here. Every deployed service must use the same
database and schema containing the existing TOEFL ``users``/``api_keys`` tables.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hmac
import re
from uuid import UUID

from psycopg import sql
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

from .config import validate_schema
from .models import ApiKeyIdentity, UsageEvent


_VERSIONED_KEY_HASH = re.compile(r"^sha256:v1:[0-9a-f]{64}$")


def _aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


class PostgresIdentityUsageStore:
    """One adapter reused by all services, with schema-qualified SQL.

    ``schema=None`` is retained only for the private TOEFL adapter's historical
    isolated-schema tests. Production runtime factories always specify a schema.
    """

    def __init__(self, pool: ConnectionPool, *, schema: str | None = "public") -> None:
        self.pool = pool
        self.schema = validate_schema(schema) if schema is not None else None

    def _table(self, name: str) -> sql.Identifier:
        return sql.Identifier(self.schema, name) if self.schema else sql.Identifier(name)

    def verify_schema(self) -> None:
        """Fail startup if shared tables or the explicit upgrade are absent."""
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "SELECT k.id, k.user_id, k.key_hash, k.scopes, k.enabled, k.expires_at, "
                "k.last_used_at, u.id, u.status FROM {} AS k JOIN {} AS u "
                "ON u.id = k.user_id LIMIT 0"
            ).format(self._table("api_keys"), self._table("users")))
            connection.execute(sql.SQL(
                "SELECT event_id, service_name, user_id, tool_name, contract_id, "
                "outcome, latency_ms, created_at FROM {} LIMIT 0"
            ).format(self._table("usage_events")))

    def create_user(self, user_id: str, email: str, name: str, status: str = "active") -> None:
        if status not in {"active", "disabled"}:
            raise ValueError("invalid user status")
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "INSERT INTO {} (id, email, name, status) VALUES (%s, %s, %s, %s)"
            ).format(self._table("users")), (user_id, email, name, status))

    def save_api_key(self, key_id: str, user_id: str, key_hash: str,
                     scopes: tuple[str, ...], expires_at: datetime | None) -> None:
        if not _VERSIONED_KEY_HASH.fullmatch(key_hash):
            raise ValueError("key_hash must be a versioned SHA-256 digest")
        if not scopes or not all(isinstance(scope, str) and scope for scope in scopes):
            raise ValueError("scopes must contain non-empty strings")
        expiry = _aware_utc(expires_at) if expires_at is not None else None
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "INSERT INTO {} (id, user_id, key_hash, scopes, enabled, expires_at) "
                "VALUES (%s, %s, %s, %s, TRUE, %s)"
            ).format(self._table("api_keys")),
                (key_id, user_id, key_hash, Jsonb(list(scopes)), expiry))

    def find_api_key(self, key_hash: str) -> ApiKeyIdentity | None:
        if not _VERSIONED_KEY_HASH.fullmatch(key_hash):
            return None
        with self.pool.connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(sql.SQL(
                    "SELECT k.id, k.user_id, k.key_hash, k.scopes, k.expires_at "
                    "FROM {} AS k JOIN {} AS u ON u.id = k.user_id "
                    "WHERE k.key_hash = %s AND k.enabled = TRUE AND u.status = 'active' "
                    "AND (k.expires_at IS NULL OR k.expires_at > CURRENT_TIMESTAMP)"
                ).format(self._table("api_keys"), self._table("users")), (key_hash,))
                row = cursor.fetchone()
        if row is None or not hmac.compare_digest(str(row["key_hash"]), key_hash):
            return None
        scopes = row["scopes"]
        if not isinstance(scopes, list) or not all(isinstance(scope, str) and scope for scope in scopes):
            return None
        return ApiKeyIdentity(str(row["id"]), str(row["user_id"]), tuple(scopes), row["expires_at"])

    def touch_api_key(self, key_id: str, used_at: datetime) -> None:
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "UPDATE {} SET last_used_at=%s WHERE id=%s"
            ).format(self._table("api_keys")), (_aware_utc(used_at), key_id))

    def set_api_key_enabled(self, key_id: str, enabled: bool) -> None:
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "UPDATE {} SET enabled=%s WHERE id=%s"
            ).format(self._table("api_keys")), (enabled, key_id))

    def record_usage(self, event: UsageEvent) -> None:
        if event.latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        created_at = _aware_utc(event.created_at)
        UUID(event.event_id)
        if not event.service_name or len(event.service_name) > 128:
            raise ValueError("service_name must have 1-128 characters")
        with self.pool.connection() as connection:
            connection.execute(sql.SQL(
                "INSERT INTO {} (event_id, service_name, user_id, tool_name, "
                "contract_id, outcome, latency_ms, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (event_id) DO NOTHING"
            ).format(self._table("usage_events")), (
                event.event_id, event.service_name, event.user_id, event.tool_name,
                event.contract_id, event.outcome, event.latency_ms, created_at,
            ))
