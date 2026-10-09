# Build context is staged by server/scripts/deploy.py from service.json build.context.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends chromium fonts-noto-cjk && rm -rf /var/lib/apt/lists/*
# The QA engine starts Chromium itself; the container has no user namespace sandbox.
RUN printf '#!/bin/sh\nexec /usr/bin/chromium --no-sandbox "$@"\n' > /usr/local/bin/workbook-chromium && chmod 0755 /usr/local/bin/workbook-chromium
WORKDIR /app
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt
COPY server/workbook_mcp /app/server/workbook_mcp
COPY server/workbook_engine /app/server/workbook_engine
COPY server/workbook_authoring /app/server/workbook_authoring
COPY server/shared_mcp_runtime /app/server/shared_mcp_runtime
COPY server/config /app/server/config
COPY server/schemas /app/server/schemas
COPY server/assets /app/server/assets
COPY server/docs /app/server/docs
COPY VERSION /app/VERSION
RUN useradd --create-home workbook
USER workbook
ENV PYTHONPATH=/app/server PYTHONDONTWRITEBYTECODE=1 MCP_SHARED_SCHEMA=public HOST=0.0.0.0 PORT=8080 CHROME_BIN=/usr/local/bin/workbook-chromium
WORKDIR /app/server
EXPOSE 8080
CMD ["python", "-m", "workbook_mcp.server"]
