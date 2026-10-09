"""Cloud Run entry point. Runtime composition and tools are independently testable."""

from .app import create_http_app, create_server
from .config import ServerSettings
from shared_mcp_runtime import http_security_kwargs

__all__ = ["create_server", "create_http_app", "ServerSettings"]


def main() -> None:
    settings = ServerSettings.from_environment()
    create_server(settings=settings).run(
        transport="http", host=settings.host, port=settings.port, path="/mcp",
        stateless_http=True, json_response=True, show_banner=False,
        **http_security_kwargs(),
    )


if __name__ == "__main__":
    main()
