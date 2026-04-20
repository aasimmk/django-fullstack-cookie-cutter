# AGENTS.md

This file guides AI coding assistants (and humans) working in this generated repository.

## Product Context (Fill This In)

### Business Problem
- Placeholder: What customer/user problem are we solving?
- Placeholder: Why does this problem matter now?

### Proposed Solution
- Placeholder: What is the intended solution strategy?
- Placeholder: What constraints (regulatory, budget, team, timeline) matter?

### Core Features
- Placeholder: List key features and expected outcomes.
- Placeholder: Define success metrics for each feature.

## Technical Snapshot

- **Repository layout**
  - [`.editorconfig`](.editorconfig) → shared indentation/encoding for Python, YAML, JSON, TOML, and frontend sources
  - [`LICENSE`](LICENSE) → **{{ cookiecutter.license }}** (also set under `[project]` in `backend/pyproject.toml`)
  - `backend/` → Django app (project package: `src/`){% if cookiecutter.use_tox == "y" %} + [`backend/tox.ini`](backend/tox.ini) (**tox** / **tox-uv**){% endif %}
  {% if cookiecutter.frontend_framework in ["vue", "react"] %}
  - `frontend/{{ cookiecutter.frontend_framework }}/` → **Vite {{ cookiecutter.vite_major_version }}** + **django-vite**{% if cookiecutter.frontend_framework == "vue" %} (**Vue {{ cookiecutter.vue_major_version }}**){% else %} (**React {{ cookiecutter.react_major_version }}**){% endif %} (Node {{ cookiecutter.node_version }}, `frontend/.nvmrc`, **{{ cookiecutter.node_package_manager }}**)
  {% elif cookiecutter.frontend_framework == "nuxt" %}
  - `frontend/nuxt/` → **Nuxt {{ cookiecutter.nuxt_major_version }}** SPA on port **3000** (no django-vite; CORS to Django when **`api_project`** is on)
  {% elif cookiecutter.frontend_framework == "next" %}
  - `frontend/next/` → **Next.js {{ cookiecutter.next_major_version }}** (App Router) on port **3000** (same integration pattern as Nuxt)
  {% elif cookiecutter.frontend_framework == "htmx" %}
  - No separate SPA app; server-rendered + **HTMX {{ cookiecutter.htmx_major_version }}.x** in Django templates
  {% else %}
  - No separate frontend app (server-rendered templates only)
  {% endif %}
  {% if cookiecutter.cloud_provider != "none" %}
  - `deploy/{{ cookiecutter.cloud_provider }}/` → deployment scaffold
  {% endif %}
  {% if cookiecutter.use_postgresql == "y" %}
  - `docker/postgres/` → custom Postgres **{{ cookiecutter.postgres_version }}** image for Compose; extend `Dockerfile` (apt plugins) and `docker-entrypoint-initdb.d/` (SQL/sh init)
  {% endif %}
  - `docker-compose.yml` → **`backend`** ([`docker/backend/Dockerfile`](docker/backend/Dockerfile), Django on **:8000**){% if cookiecutter.frontend_framework in ["vue", "react", "nuxt", "next"] %} + **`frontend`** ([`docker/frontend/Dockerfile`](docker/frontend/Dockerfile), Node **{{ cookiecutter.node_version }}**, dev server on **{% if cookiecutter.frontend_framework in ["vue", "react"] %}5173{% else %}3000{% endif %}**){% endif %}
  {% if cookiecutter.use_redis_cache == "y" or cookiecutter.use_celery == "y" %}
  - [`README.md`](README.md) → **Celery and cache** (env vars and production runbooks for Redis / Celery)
  {% endif %}
  {% if cookiecutter.documentation_provider != "none" %}
  - `docs/` → documentation host scaffold (**{{ cookiecutter.documentation_provider }}** — see repository `README.md` → Documentation)
  {% endif %}

- **Backend stack**
  - Django {{ cookiecutter.django_version }}
  - Python {{ cookiecutter.python_version }}
  - uv + `pyproject.toml`
  - Ruff + pytest
  - **django-guardian** for object-level permissions (`guardian.backends.ObjectPermissionBackend` + `guardian` migrations)
  {% if cookiecutter.use_i18n == "y" %}
  - **Internationalization:** `USE_I18N`, `LocaleMiddleware`, `LANGUAGES`, `LOCALE_PATHS` → `backend/locale/`, `/i18n/setlang/` for language selection
  {% endif %}
  {% if cookiecutter.api_project == "y" %}
  - DRF + **django-filter** + CORS headers enabled (`DEFAULT_FILTER_BACKENDS`: DjangoFilterBackend, SearchFilter, OrderingFilter)
  {% if cookiecutter.openapi_schema == "drf-spectacular" %}
  - **drf-spectacular** (OpenAPI 3 schema + UI)
  {% elif cookiecutter.openapi_schema == "drf-yasg" %}
  - **drf-yasg** (OpenAPI 2 / Swagger schema + UI)
  {% endif %}
  {% endif %}
  {% if cookiecutter.use_redis_cache == "y" %}
  - Redis-backed Django cache (`REDIS_CACHE_URL`, `django.core.cache.backends.redis.RedisCache`)
  {% endif %}
  {% if cookiecutter.use_celery == "y" %}
  - Celery enabled (`src.apps.tasks`, `src.celery`); broker: **{{ cookiecutter.celery_broker }}**; Compose services `celery-worker` + `celery-beat`
  {% endif %}
  {% if cookiecutter.use_postgresql == "y" %}
  - PostgreSQL {{ cookiecutter.postgres_version }} (Docker Compose `db`; local URL in `backend/.env.example`)
  {% endif %}

{% if cookiecutter.api_project == "y" %}
- **API shape**
  - Base route: `/api/`
  - Versioned routes under `src/apps/api/urls.py`
  - Health endpoint: `GET /api/v1/health/`
  {% if cookiecutter.openapi_schema == "drf-spectacular" %}
  - OpenAPI 3: **drf-spectacular** — schema `GET /api/schema/`, Swagger UI `/api/schema/swagger-ui/`, ReDoc `/api/redoc/` (alias: `/api/schema/redoc/`)
  {% elif cookiecutter.openapi_schema == "drf-yasg" %}
  - OpenAPI 2: **drf-yasg** — `GET /api/swagger.json` (or `.yaml`), Swagger UI `/api/swagger/`, ReDoc `/api/redoc/`
  {% endif %}
{% endif %}

## Settings and Environment

{% if cookiecutter.use_i18n == "y" %}
- **i18n:** extend **`LANGUAGES`** in `src/settings/base.py`, store catalogs under **`backend/locale/`**, run **`django-admin makemessages`** / **`compilemessages`** from `backend/`. Templates can use Django’s **`i18n`** tag library (`trans`, `blocktrans`, …). Switch locale with a **`POST`** to **`reverse("set_language")`** (`language` + `next` form fields; see Django’s translation docs).
{% endif %}
- `DJANGO_SETTINGS_MODULE` defaults to `src.settings.local`.
- Available settings modules:
  - `src.settings.local` (re-export of development)
  - `src.settings.development`
  - `src.settings.staging`
  - `src.settings.production`
  - `src.settings.test`
- Environment variables are loaded via `src/settings/_env.py` from `backend/.env`.

## Preferred Commands

Run from repository root unless stated otherwise.

- Backend bootstrap:
  - `cd backend`
  - `uv sync`
  - After model changes: `uv run python manage.py makemigrations`
  - `uv run python manage.py migrate`
  - `uv run python manage.py runserver`
- Quality:
  - `cd backend && uv run ruff check .`
  - `cd backend && uv run ruff format .`
  - `cd backend && uv run pytest` (optional: `uv run pytest -m "not e2e"` for a faster slice)
{% if cookiecutter.use_i18n == "y" %}
  - Translations: `cd backend && uv run django-admin makemessages -l <lang>` then `uv run django-admin compilemessages`
{% endif %}
{% if cookiecutter.use_tox == "y" %}
- Tox (from `backend/`; see `backend/tox.ini` — uses **tox-uv** + dev dependency group):
  - `cd backend && uv run tox run -e py,ruff,migrate`
{% endif %}
{% if cookiecutter.frontend_framework in ["vue", "react", "nuxt", "next"] %}
- Frontend (`frontend/{{ cookiecutter.frontend_framework }}/`):
  - `cd frontend/{{ cookiecutter.frontend_framework }} && {% if cookiecutter.node_package_manager == "npm" %}npm ci{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm install --frozen-lockfile{% else %}yarn install --frozen-lockfile{% endif %}`
  - `cd frontend/{{ cookiecutter.frontend_framework }} && {% if cookiecutter.node_package_manager == "npm" %}npm run dev{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm run dev{% else %}yarn run dev{% endif %}`{% if cookiecutter.frontend_framework in ["vue", "react"] %} (Vite :5173 + Django :8000){% else %} (Node UI :3000 + Django :8000){% endif %}
  - `cd frontend/{{ cookiecutter.frontend_framework }} && {% if cookiecutter.node_package_manager == "npm" %}npm run test{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm run test{% else %}yarn run test{% endif %}`
  - `cd frontend/{{ cookiecutter.frontend_framework }} && {% if cookiecutter.node_package_manager == "npm" %}npm run build{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm run build{% else %}yarn run build{% endif %}`
{% endif %}
{% if cookiecutter.use_celery == "y" %}
- Celery worker:
  - `cd backend && uv run celery -A src worker -l info`
- Celery beat (django-celery-beat database scheduler):
  - `cd backend && uv run celery -A src beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
{% endif %}

## AI Assistant Working Rules

- Prefer minimal, focused changes over broad refactors.
- Keep changes consistent with existing project structure.
- Update tests when behavior changes.
- Run relevant checks before finishing a task.
- Never commit secrets (`.env`, API keys, credentials).

## Guardrails for Contributors and Agents

- Always generate Django schema migrations with Django’s native tooling (`makemigrations` / `migrate`), not by hand-editing migration files unless you are following an explicit, documented exception.
- Prioritize idempotency, data correctness, and retry-safe behavior over feature expansion.
- Prefer configuration flags and settings-driven behavior over hardcoding environment-specific logic in application code.
- Do not guess product or architecture intent: when a bugfix or feature decision is ambiguous, ask questions before implementing.

## Code Navigation Hints

- Django project package: `backend/src/`
- Django apps:
  - `backend/src/apps/users/`
  {% if cookiecutter.api_project == "y" %}
  - `backend/src/apps/api/`
  {% endif %}
  {% if cookiecutter.use_celery == "y" %}
  - `backend/src/apps/tasks/`
  {% endif %}
- Templates: `backend/templates/`
- Tests: `backend/tests/` — **`unit/`** (no DB), **`integration/`** (Django `client` + DB), **`e2e/`** (`live_server`); markers `unit`, `integration`, `e2e` (see `backend/tests/README.md`)
{% if cookiecutter.frontend_framework in ["vue", "react"] %}
- Frontend tests: `frontend/{{ cookiecutter.frontend_framework }}/tests/` — **`unit/`** (Vitest), **`integration/`** (Vitest), **`e2e/`** (Playwright); see `frontend/{{ cookiecutter.frontend_framework }}/tests/README.md`
{% elif cookiecutter.frontend_framework in ["nuxt", "next"] %}
- Frontend tests: `frontend/{{ cookiecutter.frontend_framework }}/tests/` — Vitest (`tests/unit/`), Playwright (`tests/e2e/`); see `frontend/{{ cookiecutter.frontend_framework }}/tests/README.md`
{% endif %}

## Team Notes (Fill This In)

- Coding standards exceptions:
- Architectural decisions:
- Known technical debt:
- Release checklist:
