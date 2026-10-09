"""Non-secret shared defaults and explicit production configuration."""

from __future__ import annotations

from dataclasses import dataclass
import os
import re


API_KEY_PREFIX = "tm_"
API_KEY_HASH_VERSION = "sha256:v1"
API_KEY_RANDOM_BYTES = 32
DEFAULT_API_KEY_SCOPES = ("mcp:tools",)
INSTANCE_BURST_WINDOW_SECONDS = 60.0
INSTANCE_BURST_MAX_CALLS = 120
POSTGRES_POOL_MIN_SIZE = 1
POSTGRES_POOL_MAX_SIZE = 10
POSTGRES_POOL_OPEN_TIMEOUT_SECONDS = 30.0
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,62}$")


def validate_schema(schema: str) -> str:
    if not isinstance(schema, str) or not _IDENTIFIER.fullmatch(schema):
        raise ValueError("MCP_SHARED_SCHEMA must be a PostgreSQL identifier (1-63 characters)")
    return schema


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeConfig:
    """DSN is deliberately omitted from repr to avoid credential leakage."""

    database_url: str
    service_name: str
    schema: str = "public"

    def __post_init__(self) -> None:
        if not self.database_url:
            raise ValueError("DATABASE_URL must be non-empty")
        if not self.service_name or len(self.service_name) > 128:
            raise ValueError("service_name must have 1-128 characters")
        validate_schema(self.schema)


def load_runtime_config(service_name: str) -> RuntimeConfig:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required for shared MCP authentication")
    return RuntimeConfig(database_url, service_name, os.environ.get("MCP_SHARED_SCHEMA", "public"))
