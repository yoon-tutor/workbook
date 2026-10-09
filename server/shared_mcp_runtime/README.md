# Shared MCP runtime

Canonical source lives in the `_standard` repository. Each service vendors an
identical copy under `server/shared_mcp_runtime/` via `python _standard/sync.py`.
Never edit a vendored copy; change `_standard` and sync. Besides auth/telemetry,
the package provides the standard response envelope (`envelope.py`) and the
standard artifact bundle (`artifacts.py`) described in STANDARD.md 6.4 and 7.

All three production services must receive `DATABASE_URL` for the **same existing
TOEFL database**, and `MCP_SHARED_SCHEMA` for the same schema (default `public`).
Different passwords/roles may be used if they grant access to these same tables.
Do not create service-specific users/API-key tables or use SQLite for remote auth.
Existing `tm_` keys, `sha256:v1` digests, required `mcp:tools` scope, disabled users,
revocations, and expirations keep the TOEFL semantics. Revocation applies to all
services on the next bearer verification.

```python
from shared_mcp_runtime import load_runtime_config, create_postgres_runtime
from shared_mcp_runtime.telemetry import (
    StructuredToolTelemetryMiddleware, BurstProtectionMiddleware, InstanceBurstLimiter,
)

config = load_runtime_config("vocabulary-maker")
runtime = create_postgres_runtime(config.database_url, config.service_name, schema=config.schema)
# FastMCP(auth=runtime.auth, lifespan=runtime.lifespan, mask_error_details=True,
#         strict_input_validation=True)
# register product tools with runtime.owner_provider() for customer ownership
# register telemetry first, then the burst middleware so denied calls are observed
```

Apply additive TOEFL `server/migrations/002_shared_usage.sql` to the existing shared
schema once, before deploying any of the new servers. From the TOEFL repository's
`server/` folder, with the DSN supplied privately in the environment:

```powershell
python -m toefl_mcp.migrate --step shared-runtime
```

Only a new empty database needs `--step initial` first. Neither server startup nor
package import applies migrations. Startup opens the pool, checks the shared
relations and usage columns, and closes the pool on failure or shutdown. Blocking
psycopg operations run in worker threads outside the async MCP event loop.

Usage events retain original columns and add `service_name` and UUID `event_id`.
Historical rows are attributed to TOEFL and preserved without generated event IDs.
Reinserting the same event is idempotent. Each new MCP tool attempt gets a new event
ID; a JSON-RPC request ID is not a billing idempotency key. The events measure tool
attempts and outcomes, including guide/read/validation calls, not completed product
generation units. Select the relevant tool/outcome when querying product usage.

Usage persistence is best-effort to preserve existing product response behavior.
A database write failure emits redacted `usage_record_failed` metadata and never
changes the tool output. This is operational analytics, not a lossless billing
ledger or a distributed quota service. Burst protection is instance-local.

Arguments, source passages, candidate content, bearer tokens, and exception
messages are omitted from telemetry. Recognized statuses are allowlisted;
arbitrary `status` output text never becomes a log label. HTTP events use stdout;
stdio integrations must select `emit_stdio_event` to keep stdout protocol-only.

`install_safe_framework_logging()` additionally sanitizes FastMCP/MCP warning and
error records before any handler can output validation inputs or tracebacks.
Client-side `mask_error_details` alone does not protect framework logs. Safe
logger name, severity, and exception type remain visible; product telemetry is
unaffected. The production runtime installs it automatically; local composition
roots also install it for consistent privacy behavior.

Pinned dependencies (FastMCP 4.0.2, mcp 2.1.1, psycopg) are listed in every
service's `server/requirements.txt`. No live DB or cloud mutation occurs when
constructing the runtime.

## HTTP request protection

All HTTP composition roots and HTTP CLI runners pass `http_security_kwargs()`
to FastMCP. It explicitly enables Host/Origin protection. Requests without an
Origin header continue to use bearer authentication. Foreign browser origins
are rejected with 403 unless their exact HTTP(S) origin is allowlisted. Same
origin and local loopback requests retain FastMCP's documented behavior.

`MCP_ALLOWED_HOSTS` and `MCP_ALLOWED_ORIGINS` are comma-separated exact allowlists;
they reject wildcard entries and origin URLs with paths. Cloud Run must include
its actual public hostname in `MCP_ALLOWED_HOSTS`. Deployment scripts discover
the current service hostname before updating an existing service. Initial
deployments and custom domains can provide an explicit host list. Origin rules
do not configure CORS response permissions automatically.
