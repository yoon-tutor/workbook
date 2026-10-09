"""API-key issuance, hashing, and FastMCP bearer-token verification."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import secrets
from typing import Callable
import uuid

from fastmcp.server.auth import AccessToken, TokenVerifier
from fastmcp.server.dependencies import get_access_token

from .config import (
    API_KEY_HASH_VERSION,
    API_KEY_PREFIX,
    API_KEY_RANDOM_BYTES,
    DEFAULT_API_KEY_SCOPES,
)
from .models import ApiKeyStore


LOCAL_OWNER_ID = "local"


def utc_now() -> datetime:
    """Return an aware UTC timestamp; kept as a seam for deterministic tests."""

    return datetime.now(timezone.utc)


def _aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


def generate_api_key() -> str:
    """Generate a cryptographically random opaque API key."""

    return f"{API_KEY_PREFIX}{secrets.token_urlsafe(API_KEY_RANDOM_BYTES)}"


def hash_api_key(api_key: str) -> str:
    """Return the versioned, indexable digest stored in the database."""

    if not isinstance(api_key, str) or not api_key:
        raise ValueError("api_key must be a non-empty string")
    digest = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
    return f"{API_KEY_HASH_VERSION}:{digest}"


@dataclass(frozen=True, slots=True)
class IssuedApiKey:
    """One-time issuance result. ``api_key`` must never be persisted or logged."""

    key_id: str
    user_id: str
    api_key: str
    scopes: tuple[str, ...]
    expires_at: datetime | None


def issue_api_key(
    store: ApiKeyStore,
    user_id: str,
    *,
    scopes: tuple[str, ...] = DEFAULT_API_KEY_SCOPES,
    expires_at: datetime | None = None,
    key_factory: Callable[[], str] = generate_api_key,
    key_id_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
) -> IssuedApiKey:
    """Issue an API key, persist only its digest, and return the raw value once."""

    if not user_id:
        raise ValueError("user_id must be non-empty")
    if not scopes or not all(isinstance(scope, str) and scope for scope in scopes):
        raise ValueError("scopes must contain non-empty strings")
    normalized_expiry = _aware_utc(expires_at) if expires_at is not None else None
    api_key = key_factory()
    if not api_key.startswith(API_KEY_PREFIX):
        raise ValueError(f"API keys must start with {API_KEY_PREFIX!r}")
    key_id = key_id_factory()
    store.save_api_key(
        key_id,
        user_id,
        hash_api_key(api_key),
        tuple(scopes),
        normalized_expiry,
    )
    return IssuedApiKey(
        key_id=key_id,
        user_id=user_id,
        api_key=api_key,
        scopes=tuple(scopes),
        expires_at=normalized_expiry,
    )


class DatabaseApiKeyVerifier(TokenVerifier):
    """Resolve bearer API keys through the configured persistence adapter."""

    def __init__(self, store: ApiKeyStore) -> None:
        super().__init__(required_scopes=list(DEFAULT_API_KEY_SCOPES))
        self._store = store

    async def verify_token(self, token: str) -> AccessToken | None:
        if not token or not token.startswith(API_KEY_PREFIX):
            return None
        identity = await asyncio.to_thread(
            self._store.find_api_key, hash_api_key(token)
        )
        if identity is None:
            return None
        used_at = utc_now()
        if not all(scope in identity.scopes for scope in DEFAULT_API_KEY_SCOPES):
            return None
        if identity.expires_at is not None and _aware_utc(identity.expires_at) <= used_at:
            return None
        await asyncio.to_thread(self._store.touch_api_key, identity.key_id, used_at)
        return AccessToken(
            token=token,
            client_id=identity.key_id,
            subject=identity.user_id,
            scopes=list(identity.scopes),
            expires_at=(
                int(_aware_utc(identity.expires_at).timestamp())
                if identity.expires_at is not None
                else None
            ),
            claims={"user_id": identity.user_id, "key_id": identity.key_id},
        )


def current_user_id(*, local_owner_id: str | None = None) -> str:
    """Read the authenticated user ID, with an explicit local-only fallback."""

    access_token = get_access_token()
    if access_token is None:
        if local_owner_id is not None:
            return local_owner_id
        raise RuntimeError("authenticated MCP user is required")
    user_id = access_token.claims.get("user_id") or access_token.subject
    if not isinstance(user_id, str) or not user_id:
        raise RuntimeError("authenticated MCP token has no user_id")
    return user_id
