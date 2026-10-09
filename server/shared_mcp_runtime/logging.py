"""Redact framework warning/error logs before any logging handler sees them."""

from __future__ import annotations

import json
import logging
from threading import Lock


_INSTALL_LOCK = Lock()


def install_safe_framework_logging() -> None:
    """Chain the current record factory and sanitize only MCP framework errors.

    FastMCP's mask_error_details protects client responses, but its validation
    warnings and exception tracebacks can still contain raw customer input.
    A record factory covers propagated and newly created child loggers as well
    as handlers installed later by the stdio runner. Application/usage logs are
    unaffected. Repeated installation is idempotent.
    """
    with _INSTALL_LOCK:
        previous_factory = logging.getLogRecordFactory()
        if getattr(previous_factory, "_shared_mcp_safe_factory", False):
            return

        def safe_factory(*args, **kwargs):
            record = previous_factory(*args, **kwargs)
            framework = record.name in {"fastmcp", "mcp"} or record.name.startswith(("fastmcp.", "mcp."))
            if framework and record.levelno >= logging.WARNING:
                error_type = record.exc_info[0].__name__ if record.exc_info and record.exc_info[0] else "FrameworkWarning"
                record.msg = json.dumps({
                    "event": "mcp_framework_error", "logger": record.name,
                    "level": record.levelname, "error_type": error_type,
                }, separators=(",", ":"), sort_keys=True)
                record.args = ()
                record.exc_info = None
                record.exc_text = None
                record.stack_info = None
            return record

        safe_factory._shared_mcp_safe_factory = True
        logging.setLogRecordFactory(safe_factory)


# Readable alias retained for callers integrating MCP-specific logging.
install_safe_mcp_logging = install_safe_framework_logging
