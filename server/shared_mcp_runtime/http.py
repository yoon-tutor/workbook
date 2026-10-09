"""Explicit FastMCP HTTP Host/Origin protection shared by all services."""

from __future__ import annotations

from collections.abc import Sequence
from ipaddress import ip_address
import os
import re
from typing import Literal, TypedDict
from urllib.parse import urlsplit


class HttpSecurityKwargs(TypedDict):
    host_origin_protection: Literal[True]
    allowed_hosts: list[str]
    allowed_origins: list[str]


_DNS_HOST = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?$")


def _hosts(values: Sequence[str]) -> list[str]:
    result = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("MCP_ALLOWED_HOSTS entries must be exact hostnames")
        value = value.strip().lower()
        if not value or any(char in value for char in "*/?@#\\"):
            raise ValueError("MCP_ALLOWED_HOSTS entries must be exact hostnames, without wildcards or URLs")
        # Bare/bracketed IPv6 is supported for explicit local integrations.
        try:
            ip_address(value.strip("[]"))
        except ValueError:
            try:
                parsed = urlsplit(f"//{value}")
                hostname = parsed.hostname
                port = parsed.port
            except ValueError as exc:
                raise ValueError("MCP_ALLOWED_HOSTS entry is invalid") from exc
            if not hostname or not _DNS_HOST.fullmatch(hostname) or parsed.path or (port is not None and port < 1):
                raise ValueError("MCP_ALLOWED_HOSTS entry is invalid")
        result.append(value)
    return list(dict.fromkeys(result))


def _origins(values: Sequence[str]) -> list[str]:
    result = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("MCP_ALLOWED_ORIGINS entries must be exact HTTP(S) origins")
        value = value.strip().rstrip("/")
        try:
            parsed = urlsplit(value)
            port = parsed.port
        except ValueError as exc:
            raise ValueError("MCP_ALLOWED_ORIGINS entry is invalid") from exc
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment
                or any(char in value for char in "*?\\") or (port is not None and port < 1)):
            raise ValueError("MCP_ALLOWED_ORIGINS entries must be exact HTTP(S) origins, without paths or wildcards")
        _hosts([parsed.hostname])
        result.append(value)
    return list(dict.fromkeys(result))


def _values(explicit: Sequence[str] | None, env_name: str) -> Sequence[str]:
    if isinstance(explicit, str):
        raise ValueError(f"{env_name} must be a list of entries when passed as an argument")
    if explicit is not None:
        return explicit
    return [value.strip() for value in os.environ.get(env_name, "").split(",") if value.strip()]


def http_security_kwargs(*, allowed_hosts: Sequence[str] | None = None,
                         allowed_origins: Sequence[str] | None = None) -> HttpSecurityKwargs:
    """Arguments accepted by FastMCP 4 ``http_app`` and ``run(http)``.

    Browser requests with foreign Origin headers are denied unless their exact
    origin is configured. Bearer clients omitting Origin continue to work.
    FastMCP additionally allows same-origin and local loopback requests. Cloud
    Run's external hostname must be in MCP_ALLOWED_HOSTS; defaults never grant
    wildcard host/origin access. CORS, when needed, is configured separately.
    """
    return {
        "host_origin_protection": True,
        "allowed_hosts": _hosts(_values(allowed_hosts, "MCP_ALLOWED_HOSTS")),
        "allowed_origins": _origins(_values(allowed_origins, "MCP_ALLOWED_ORIGINS")),
    }
