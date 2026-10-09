"""Composition root for the stateless, authenticated workbook MCP service."""

from __future__ import annotations

import asyncio
from typing import Any
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from shared_mcp_runtime import create_postgres_runtime, install_safe_framework_logging, http_security_kwargs
from shared_mcp_runtime.telemetry import (
    BurstProtectionMiddleware,
    InstanceBurstLimiter,
    StructuredToolTelemetryMiddleware,
)

from . import direct_release
from .config import ServerSettings
from .service import SERVICE
from .tools import register_tools

SERVICE_NAME = SERVICE["name"]


def create_server(runtime: Any = None, *, settings: ServerSettings | None = None) -> FastMCP:
    """Build a server with a production DB runtime or an explicitly injected test runtime."""
    install_safe_framework_logging()
    settings = settings or ServerSettings.from_environment()
    if runtime is None:
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL must point to the shared TOEFL identity database")
        runtime = create_postgres_runtime(
            settings.database_url, service_name=SERVICE_NAME, schema=settings.schema,
        )

    @asynccontextmanager
    async def app_lifespan(server):
        async with runtime.lifespan(server) as state:
            try:
                yield state
            finally:
                direct_release.close_storage_clients()

    mcp = FastMCP(
        SERVICE_NAME, version=SERVICE["version"], auth=runtime.auth, lifespan=app_lifespan,
        mask_error_details=True, strict_input_validation=True,
        instructions=("Call workbook_get_guidance first. Every tool returns the standard envelope; follow next_action. "
                      "Prepare, open every review image, then publish; artifacts arrive as mcp-artifact-bundle-v1."),
    )
    mcp.add_middleware(StructuredToolTelemetryMiddleware(
        runtime.owner_provider, usage_store=runtime.usage_store, service_name=SERVICE_NAME,
    ))
    mcp.add_middleware(BurstProtectionMiddleware(runtime.owner_provider, InstanceBurstLimiter()))
    register_tools(mcp, runtime.owner_provider)
    mcp.custom_route("/artifact/{release_id}/{name}", methods=["GET"])(direct_release.artifact_route)
    mcp.custom_route("/review-image/{release_id}/{name}", methods=["GET"])(direct_release.review_image_route)

    @mcp.custom_route("/health", methods=["GET"])
    @mcp.custom_route("/healthz", methods=["GET"])
    async def health(_request: Request) -> JSONResponse:
        """Liveness only; no DB credentials, user data, or deployment internals."""
        return JSONResponse({"status": "ok", "service": SERVICE_NAME, "version": SERVICE["version"]})

    @mcp.custom_route("/ready", methods=["GET"])
    async def ready(_request: Request) -> JSONResponse:
        """Readiness: the shared identity database answers (503 otherwise)."""
        pool = getattr(runtime, "pool", None)
        if pool is not None:
            def check_database() -> None:
                with pool.connection() as connection:
                    connection.execute("SELECT 1")
            try:
                await asyncio.to_thread(check_database)
            except Exception:
                return JSONResponse({"status": "unavailable", "service": SERVICE_NAME}, status_code=503)
        return JSONResponse({"status": "ready", "service": SERVICE_NAME})

    return mcp


def create_http_app(runtime: Any = None, *, settings: ServerSettings | None = None):
    """ASGI app with the same stateless JSON settings used by Cloud Run."""
    return create_server(runtime, settings=settings).http_app(
        path="/mcp", stateless_http=True, json_response=True, **http_security_kwargs(),
    )
