{% if cookiecutter.frontend_framework in ["vue", "react", "nuxt", "next"] %}# syntax=docker/dockerfile:1
# Node frontend — dev-oriented image for Docker Compose (install + dev server).
# Build from repository root: docker compose build frontend

ARG NODE_VERSION={{ cookiecutter.node_version }}
FROM node:${NODE_VERSION}-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN corepack enable

WORKDIR /app/frontend/{{ cookiecutter.frontend_framework }}

LABEL org.opencontainers.image.title="{{ cookiecutter.project_name }} frontend" \
    org.opencontainers.image.description="Node {{ cookiecutter.node_version }} ({{ cookiecutter.frontend_framework }})"

{% if cookiecutter.frontend_framework in ["vue", "react"] %}
EXPOSE 5173
{% else %}
EXPOSE 3000
{% endif %}

{% if cookiecutter.node_package_manager == "npm" %}
CMD ["sh", "-c", "npm ci && npm run dev"]
{% elif cookiecutter.node_package_manager == "pnpm" %}
CMD ["sh", "-c", "corepack prepare pnpm@9 --activate && pnpm install --frozen-lockfile && pnpm run dev"]
{% else %}
CMD ["sh", "-c", "yarn install --frozen-lockfile && yarn run dev"]
{% endif %}
{% endif %}
