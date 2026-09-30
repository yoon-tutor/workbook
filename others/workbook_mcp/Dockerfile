FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends chromium fonts-noto-cjk && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nexec /usr/bin/chromium --no-sandbox "$@"\n' > /usr/local/bin/workbook-chromium && chmod 0755 /usr/local/bin/workbook-chromium
COPY workbook_mcp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN useradd --create-home workbook
RUN chown -R workbook:workbook /app
USER workbook
ENV HOST=0.0.0.0 PORT=8080 PYTHONDONTWRITEBYTECODE=1 CHROME_BIN=/usr/local/bin/workbook-chromium
EXPOSE 8080
CMD ["python", "-m", "workbook_mcp.server"]
