"""Validated server configuration; client API keys are never server credentials."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerSettings:
    database_url: str = ""
    schema: str = "public"
    host: str = "127.0.0.1"
    port: int = 8080

    @classmethod
    def from_environment(cls) -> "ServerSettings":
        settings = cls(
            database_url=os.environ.get("DATABASE_URL", "").strip(),
            schema=os.environ.get("MCP_SHARED_SCHEMA", "public").strip(),
            host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "8080")),
        )
        if not 1 <= settings.port <= 65535:
            raise ValueError("PORT must be between 1 and 65535")
        return settings

