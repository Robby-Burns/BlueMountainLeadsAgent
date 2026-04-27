# 1. Use a slim, secure base image
FROM python:3.11-slim-bookworm

# 2. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# 3. Install system dependencies (curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Use UV for lightning-fast installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 5. Set work directory
WORKDIR /app

# 6. Install dependencies
COPY pyproject.toml .
# Using standard pip here but utilizing uv for speed
RUN uv pip install --system -r pyproject.toml

# 7. Copy application code
COPY . .

# 8. Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 9. Default Command (Runs the orchestrator)
CMD ["python", "main.py"]
