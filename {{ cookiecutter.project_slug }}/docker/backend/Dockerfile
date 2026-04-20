# syntax=docker/dockerfile:1
# Django backend — production-oriented image (uv + Gunicorn).
# Build from repository root: docker build -f docker/backend/Dockerfile .

FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/backend

LABEL org.opencontainers.image.title="{{ cookiecutter.project_name }} backend" \
    org.opencontainers.image.description="Django (uv, Gunicorn)"

COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

COPY backend/ .

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
