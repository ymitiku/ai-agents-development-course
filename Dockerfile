# ------------------------------------------------------------
# Builder: export deps with Poetry and prefetch wheels
# ------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# System libs (minimal) — libgomp often needed by scientific wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and export requirements
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir "poetry>=2.0.0" "poetry-plugin-export>=1.7.1"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Prefetch wheels for faster/clean installs in runtime
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

# Bring in the source (we run from source in runtime; no packaging required)
COPY . .

# ------------------------------------------------------------
# Runtime: slim image with only needed wheels + source
# ------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# System libs (match builder)
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies from prebuilt wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy source
COPY . .

# (Optional) run as non-root for safety
RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000

# Healthcheck: ensure the server is running and healthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import sys,urllib.request; \
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3).status==200 else 1)"


# Default: HTTP demo server
CMD ["python", "-m", "tools.mcp_server.app"]

# --- To run the MCP STDIO server instead, use:
# CMD ["python", "-m", "tools.mcp_server.mcp_stdio"]
