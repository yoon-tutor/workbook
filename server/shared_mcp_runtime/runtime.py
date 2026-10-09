"""Fail-closed, lifespan-managed composition shared by the three products."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass

from fastmcp import FastMCP
from fastmcp.server.lifespan import Lifespan, lifespan
from psycopg import Connection, sql
from psycopg_pool import ConnectionPool

from .auth import DatabaseApiKeyVerifier, current_user_id
from .config import RuntimeConfig
from .store import PostgresIdentityUsageStore
from .logging import install_safe_framework_logging


@dataclass(frozen=True, slots=True)
class PostgresRuntime:
    pool: ConnectionPool
    identity_store: PostgresIdentityUsageStore
    usage_store: PostgresIdentityUsageStore
    auth: DatabaseApiKeyVerifier
    owner_provider: Callable[[], str]
    lifespan: Lifespan


def create_postgres_runtime(database_url: str, service_name: str, *, schema: str = "public",
                            pool_min_size: int = 1, pool_max_size: int = 10,
                            pool_open_timeout: float = 30.0) -> PostgresRuntime:
    """Construct resources without connecting; FastMCP owns their lifecycle.

    Every service uses the same existing shared schema. This factory neither
    creates tables nor provisions a separate identity database. A configure
    callback avoids startup search_path parameters rejected by some poolers.
    """
    config = RuntimeConfig(database_url, service_name, schema)
    install_safe_framework_logging()
    if pool_min_size < 0 or pool_max_size < max(1, pool_min_size) or pool_open_timeout <= 0:
        raise ValueError("invalid PostgreSQL pool bounds or timeout")

    def configure(connection: Connection) -> None:
        connection.execute(sql.SQL("SET search_path TO {}, pg_catalog").format(sql.Identifier(config.schema)))
        connection.commit()

    pool = ConnectionPool(
        conninfo=config.database_url, min_size=pool_min_size, max_size=pool_max_size,
        open=False, check=ConnectionPool.check_connection, configure=configure,
        name=config.service_name, timeout=pool_open_timeout,
    )
    store = PostgresIdentityUsageStore(pool, schema=config.schema)

    @lifespan
    async def manage_pool(_server: FastMCP):
        try:
            await asyncio.to_thread(pool.open, wait=True, timeout=pool_open_timeout)
            await asyncio.to_thread(store.verify_schema)
            yield {"postgres_pool": pool, "identity_store": store, "usage_store": store}
        finally:
            await asyncio.to_thread(pool.close)

    return PostgresRuntime(pool, store, store, DatabaseApiKeyVerifier(store), current_user_id, manage_pool)
