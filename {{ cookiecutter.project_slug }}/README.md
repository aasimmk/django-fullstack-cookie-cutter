# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

**Layout:** `backend/` (Django project package `src/` + uv){% if cookiecutter['__frontend_framework'] in ["vue", "react", "nuxt", "next"] %} and `frontend/{{ cookiecutter['__frontend_framework'] }}/` ({% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}Vite + django-vite{% elif cookiecutter['__frontend_framework'] == "nuxt" %}Nuxt {{ cookiecutter['__nuxt_major_version'] }}{% else %}Next.js {{ cookiecutter['__next_major_version'] }}{% endif %}){% endif %} are siblings at the repo root.

## Index

- [Tech stack](#tech-stack)
- [Quick start](#quick-start)
{% if cookiecutter.api_project == "y" %}
- [REST API](#rest-api)
{% if cookiecutter.openapi_schema != "none" %}
- [API documentation](#api-documentation)
{% endif %}
{% endif %}
- [Django settings](#django-settings)
- [uv commands](#uv-commands)
- [Frontend](#frontend)
- [Docker](#docker)
- [Infrastructure](#infrastructure)
- [Celery and cache](#celery-and-cache)
- [Documentation](#documentation)
- [License](#license)

## Tech stack

This project was scaffolded with **django-fullstack-cookie-cutter**. The sections below reflect **your Cookiecutter answers** (not optional add-ons you must install later).

### Backend runtime

- **Django {{ cookiecutter.django_version }}** on **Python {{ cookiecutter.python_version }}** (`requires-python` in `backend/pyproject.toml` matches this floor).
- **[uv](https://github.com/astral-sh/uv)** for installs and `uv run …`; dependencies live in **`backend/pyproject.toml`** with a checked-in **`uv.lock`**.
- **Gunicorn** for WSGI deployment and **WhiteNoise** for static file serving in production-oriented settings.
- **Settings modules:** `src.settings.local` (default), `development`, `staging`, `production`, and `test` (used by pytest).
{% if cookiecutter.use_i18n == "y" %}
- **Internationalization (gettext):** `USE_I18N`, **`django.middleware.locale.LocaleMiddleware`**, `LANGUAGES`, **`LOCALE_PATHS`** → `backend/locale/`, template context processor `i18n`, and **`/i18n/setlang/`** for `POST` language changes (`django.conf.urls.i18n`). Extend **`LANGUAGES`** in `src/settings/base.py` as you add locales.
{% endif %}

### Data & persistence

{% if cookiecutter.use_postgresql == "y" %}
- **PostgreSQL {{ cookiecutter.postgres_version }}** for the default database in non-test settings: **`DATABASE_URL`** via **django-environ** in `src/settings/base.py`, driver **psycopg** (v3).
- **Docker Compose** includes a **`db`** service built from `docker/postgres/` (custom image + optional `docker-entrypoint-initdb.d/` scripts).
{% else %}
- **SQLite** file under `backend/` for local development; **pytest** uses **`src.settings.test`** (in-memory SQLite) so you do not need Postgres running for CI or unit tests.
{% endif %}

### HTTP APIs

{% if cookiecutter.api_project == "y" %}
- **Django REST Framework** with **django-cors-headers** and a versioned layout under **`/api/v1/…`** (see `src/apps/api/`). Session + basic auth and browsable API apply in development; staging/production bias toward **JSON-only** responses.
{% if cookiecutter.openapi_schema == "drf-spectacular" %}
- **OpenAPI 3** via **drf-spectacular**: `GET /api/schema/`, Swagger UI at `/api/schema/swagger-ui/`, ReDoc at **`/api/redoc/`** (same UI at `/api/schema/redoc/`).
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
- **OpenAPI 2 (Swagger)** via **drf-yasg**: `GET /api/swagger.json` or `/api/swagger.yaml`, UI at `/api/swagger/` and `/api/redoc/`.
{% endif %}
{% else %}
- **No DRF bundle** — expose HTTP via Django views (and templates or HTMX) unless you add an API layer yourself.
{% endif %}

### Frontend & templates

{% if cookiecutter['__frontend_framework'] == "none" %}
- **Server-rendered Django templates** with **Tailwind CSS** via CDN in `backend/templates/base.html` (no separate Node app).
{% elif cookiecutter['__frontend_framework'] == "htmx" %}
- **django-htmx** plus **HTMX {{ cookiecutter['__htmx_major_version'] }}.x** (CDN in `backend/templates/base.html`) and **Tailwind CSS** from CDNs; partials and regular Django views drive the UI (no separate Node app).
{% elif cookiecutter['__frontend_framework'] == "vue" %}
- **Vue {{ cookiecutter['__vue_major_version'] }}** SPA with **Vite {{ cookiecutter['__vite_major_version'] }}**, **Tailwind CSS**, **Vitest** (unit), and **Playwright** (e2e). **django-vite** bridges dev HMR and production manifests; build output is collected into **`backend/static/dist`**. Use **Node.js {{ cookiecutter.node_version }}** and **{{ cookiecutter.node_package_manager }}** (see `frontend/.nvmrc`).
{% elif cookiecutter['__frontend_framework'] == "react" %}
- **React {{ cookiecutter['__react_major_version'] }}** SPA with **Vite {{ cookiecutter['__vite_major_version'] }}**, **Tailwind CSS**, **Vitest** (unit), and **Playwright** (e2e). **django-vite** bridges dev HMR and production manifests; build output is collected into **`backend/static/dist`**. Use **Node.js {{ cookiecutter.node_version }}** and **{{ cookiecutter.node_package_manager }}** (see `frontend/.nvmrc`).
{% elif cookiecutter['__frontend_framework'] == "nuxt" %}
- **Nuxt {{ cookiecutter['__nuxt_major_version'] }}** in **SPA mode** (`ssr: false`) with **Vitest** and **Playwright**. The app runs its own dev server on **port 3000** (not embedded via django-vite). Use **Node.js {{ cookiecutter.node_version }}** and **{{ cookiecutter.node_package_manager }}** (see `frontend/.nvmrc`). Call Django from the browser with **`api_project` = `y`** (CORS defaults include `http://127.0.0.1:3000`) or add your own CORS rules.
{% else %}
- **Next.js {{ cookiecutter['__next_major_version'] }}** (App Router) with **React {% if cookiecutter['__next_major_version'] == "14" %}18{% else %}19{% endif %}**, **Vitest**, and **Playwright**. Same **port 3000** / **no django-vite** integration pattern as Nuxt: Django stays on **8000**, CORS defaults include the dev UI when **`api_project`** is enabled.
{% endif %}

### Cache, tasks, and messaging

{% if cookiecutter.use_redis_cache == "y" %}
- **Redis** as Django’s default cache backend (`django.core.cache.backends.redis.RedisCache`, **`REDIS_CACHE_URL`**).
{% else %}
- **No Redis cache** — Django uses local-memory caching unless you change settings.
{% endif %}
{% if cookiecutter.use_celery == "y" %}
- **Celery** with **django-celery-beat** (database scheduler). Broker: **{{ cookiecutter.celery_broker }}** (`CELERY_BROKER_URL` / **`CELERY_RESULT_BACKEND`** in `.env.example`). Compose defines **`celery-worker`** and **`celery-beat`** when enabled.
{% else %}
- **Celery is off** — no worker/beat services or broker wiring in this generated tree.
{% endif %}

### Deployment & infrastructure

{% if cookiecutter.cloud_provider == "none" %}
- **Cloud bundle:** `none` — this repo ships **Docker Compose** for local parity (**`backend`**{% if cookiecutter['__frontend_framework'] in ["vue", "react", "nuxt", "next"] %} + **`frontend`**{% endif %}{% if cookiecutter.use_postgresql == "y" %} + Postgres{% endif %}{% if cookiecutter.use_redis_cache == "y" or cookiecutter.use_celery == "y" %} + Redis/RabbitMQ as selected{% endif %}). Add your own IaC when you pick a host.
{% elif cookiecutter.cloud_provider == "aws" %}
- **AWS** starter under **`deploy/aws/terraform/`** (minimal modules; extend with your VPC, RDS, ElastiCache, etc.).
{% elif cookiecutter.cloud_provider == "gcp" %}
- **GCP** starter under **`deploy/gcp/terraform/`** (wire `gcp_project_id` and extend with your services).
{% elif cookiecutter.cloud_provider == "azure" %}
- **Azure** starter under **`deploy/azure/terraform/`**.
{% elif cookiecutter.cloud_provider == "heroku" %}
- **Heroku** artifacts under **`deploy/heroku/`** (`Procfile`, `runtime.txt`, optional `heroku.yml`) — commands assume **uv** and `backend/` as the app root.
{% else %}
- **DigitalOcean App Platform** spec under **`deploy/digitalocean/.do/app.yaml`** ([`docker/backend/Dockerfile`](docker/backend/Dockerfile) builds the backend image){% if cookiecutter.use_celery == "y" %} including worker/beat layouts when Celery is on{% endif %}.
{% endif %}

### Quality gates & automation

- **Ruff** (lint + format), **pytest** + **pytest-django** + **pytest-cov**, and **mypy** with **django-stubs** in the backend dev dependency group.
- **GitHub Actions** (`.github/workflows/ci.yml`): `uv sync`, Ruff, migration check, pytest{% if cookiecutter.use_tox == "y" %}, then **Tox** (`py`, `ruff`, `migrate` envs){% endif %}{% if cookiecutter['__frontend_framework'] in ["vue", "react", "nuxt", "next"] %}; a separate job installs Node deps under `frontend/{{ cookiecutter['__frontend_framework'] }}/` and runs tests + production build{% endif %}.
{% if cookiecutter.documentation_provider == "mkdocs" %}
- **Docs CI:** `.github/workflows/docs.yml` builds **MkDocs** and publishes to **`gh-pages`** when `docs/` or `mkdocs.yml` changes.
{% endif %}
{% if cookiecutter.use_tox == "y" %}
- **Tox** + **tox-uv** via `backend/tox.ini` mirrors the same checks locally or in CI.
{% endif %}

### Documentation & knowledge

{% if cookiecutter.documentation_provider == "none" %}
- **Docs host:** `none` — this README (and your own docs you add) are the source of truth.
{% elif cookiecutter.documentation_provider == "gitbook" %}
- **GitBook**-oriented notes under `docs/` (see `docs/GITBOOK.md`).
{% elif cookiecutter.documentation_provider == "readthedocs" %}
- **Read the Docs** + **MkDocs** (`.readthedocs.yaml`, `mkdocs.yml`, `docs/`).
{% elif cookiecutter.documentation_provider == "mkdocs" %}
- **MkDocs** (Material) with a GitHub Action publishing to **GitHub Pages** (`gh-pages`).
{% else %}
- **Notion**-oriented setup notes in `docs/NOTION.md` (Notion stays narrative; keep canonical facts in-repo).
{% endif %}

### License, metadata, and assistants

- **License:** {{ cookiecutter.license }} (root `LICENSE` and `backend/pyproject.toml` metadata). **Author:** {{ cookiecutter.author_name }} — **Email:** {{ cookiecutter.email }}.
- **Editor:** root `.editorconfig`. **AI / agent hints:** `AGENTS.md`, `.cursor/rules/project-guidelines.mdc`, and `.claude/` snippets match this stack.

## Quick start

```bash
cd backend
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

{% if cookiecutter.api_project == "y" %}
## REST API

- **Base path:** `/api/` (see `src/apps/api/urls.py`).
- **Example:** `GET /api/v1/health/` → `{"status": "ok", "service": "<project_slug>"}` (no auth).
- **DRF defaults:** session + basic auth, `IsAuthenticatedOrReadOnly`, JSON + browsable HTML renderers in development; **JSON only** in `staging` and `production`.
- **CORS:** set `CORS_ALLOWED_ORIGINS` in `backend/.env` (comma-separated). Defaults include local Django plus **Vite (:5173)** when Vue/React is selected, or **Nuxt / Next (:3000)** when those frameworks are selected.

```bash
curl -s http://127.0.0.1:8000/api/v1/health/
```

{% if cookiecutter.openapi_schema != "none" %}
### API documentation

With `uv run python manage.py runserver`, open the URLs below on **http://127.0.0.1:8000** (adjust host/port if needed).

{% if cookiecutter.openapi_schema == "drf-spectacular" %}
**OpenAPI 3** (drf-spectacular)

| API Docs                             | Path                                                                      |
|--------------------------------------|---------------------------------------------------------------------------|
| OpenAPI schema (for tools / codegen) | [`/api/schema/`](http://127.0.0.1:8000/api/schema/)                       |
| Swagger UI                           | [`/api/schema/swagger-ui/`](http://127.0.0.1:8000/api/schema/swagger-ui/) |
| **ReDoc**                            | [`/api/redoc/`](http://127.0.0.1:8000/api/redoc/)                         |
| ReDoc (same document, nested URL)    | [`/api/schema/redoc/`](http://127.0.0.1:8000/api/schema/redoc/)           |
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
**OpenAPI 2 / Swagger** (drf-yasg)

| API Docs     | Path                                                          |
|--------------|---------------------------------------------------------------|
| OpenAPI JSON | [`/api/swagger.json`](http://127.0.0.1:8000/api/swagger.json) |
| OpenAPI YAML | [`/api/swagger.yaml`](http://127.0.0.1:8000/api/swagger.yaml) |
| Swagger UI   | [`/api/swagger/`](http://127.0.0.1:8000/api/swagger/)         |
| **ReDoc**    | [`/api/redoc/`](http://127.0.0.1:8000/api/redoc/)             |
{% endif %}

{% if cookiecutter.openapi_schema == "drf-spectacular" %}
```bash
curl -s http://127.0.0.1:8000/api/schema/
```
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
```bash
curl -s http://127.0.0.1:8000/api/swagger.json
```
{% endif %}

{% else %}
Bundled **OpenAPI / Swagger / ReDoc** routes are off when `openapi_schema` is `none` at generation time. Add schema tooling in `src/apps/api/urls.py` and settings if you need interactive API docs later.
{% endif %}

{% endif %}
## Django settings

| `DJANGO_SETTINGS_MODULE`   | When to use                                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------------------------|
| `src.settings.local`       | Default in `manage.py` — same as `development`                                                                |
| `src.settings.development` | Debug on, console email{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}; **django-vite** dev mode (Vite on :5173){% elif cookiecutter['__frontend_framework'] in ["nuxt", "next"] %} (run Nuxt/Next separately on :3000){% endif %} |
| `src.settings.staging`     | Pre-production: `SECRET_KEY` required, HTTPS-oriented cookies, optional HSTS via `DJANGO_SECURE_HSTS_SECONDS` |
| `src.settings.production`  | Live deployment                                                                                               |

Set `DJANGO_SETTINGS_MODULE` in `backend/.env` or your process manager (see `backend/.env.example`).

Environment variables are read from `os.environ` after `backend/.env` is loaded in [`src/settings/_env.py`](backend/src/settings/_env.py) (via **python-dotenv**). Use the `env` singleton (`get_str`, `get_bool`, `get_list`, etc.) in settings modules. `DATABASE_URL` still uses **django-environ**’s parser in `base.py` when PostgreSQL is enabled.

## uv commands

Run the following from the **`backend/`** directory (repository root is one level up).

| Command                      | Purpose                                                                                            |
|------------------------------|----------------------------------------------------------------------------------------------------|
| `uv sync`                    | Install deps from `uv.lock`                                                                        |
| `uv run python manage.py …`  | Django management                                                                                  |
| `uv run ruff check .`        | Lint                                                                                               |
| `uv run ruff format .`       | Format                                                                                             |
| `uv run pytest`              | Tests under `tests/unit`, `tests/integration`, `tests/e2e` (markers: `unit`, `integration`, `e2e`) |
| `uv run pytest -m "not e2e"` | Faster run: skip `e2e` (`live_server`) tests                                                       |
{% if cookiecutter.use_i18n == "y" %}
| `uv run django-admin makemessages -l <lang>` | Extract strings into `locale/<lang>/LC_MESSAGES/django.po` |
| `uv run django-admin compilemessages` | Compile `.po` files to `.mo` |
{% endif %}
{% if cookiecutter.use_tox == "y" %}
| `uv run tox run -e py` | Run pytest via Tox (same as `uv run pytest`, useful for env isolation) |
| `uv run tox run -e ruff` | Ruff via Tox |
| `uv run tox run -e migrate` | `makemigrations --check --dry-run` via Tox |
| `uv run tox run -e py,ruff,migrate` | All Tox envs in one go |
{% endif %}

## Frontend

**Mode:** `{{ cookiecutter['__frontend_framework'] }}`{% if cookiecutter['__frontend_framework'] in ["vue", "react", "nuxt", "next"] %} · **Node:** {{ cookiecutter.node_version }} · **Package manager:** {{ cookiecutter.node_package_manager }}{% endif %}.

{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
The SPA is embedded from Django templates via **django-vite**; Vite listens on **:5173** in development.

```bash
cd frontend/{{ cookiecutter['__frontend_framework'] }}
{% if cookiecutter.node_package_manager == "npm" %}npm ci
npm run dev   # Vite on :5173 — run Django from ../backend on :8000
npm run build # writes assets to backend/static/dist for django-vite
npm run test  # Vitest (`tests/unit`, `tests/integration`)
npm run test:e2e  # Playwright — `tests/e2e` (run Django from ../backend first)
{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm install --frozen-lockfile
pnpm run dev
pnpm run build
pnpm run test  # Vitest (`tests/unit`, `tests/integration`)
pnpm run test:e2e  # Playwright — `tests/e2e`
{% else %}yarn install --frozen-lockfile
yarn run dev
yarn run build
yarn run test  # Vitest (`tests/unit`, `tests/integration`)
yarn run test:e2e  # Playwright — `tests/e2e`
{% endif %}
```
{% elif cookiecutter['__frontend_framework'] in ["nuxt", "next"] %}
**Nuxt** and **Next.js** run as **separate Node servers on port 3000** (Django remains on **:8000**). There is no django-vite bridge: use session/API calls against Django with CORS (defaults include :3000 when **`api_project`** is `y`).

```bash
cd frontend/{{ cookiecutter['__frontend_framework'] }}
{% if cookiecutter.node_package_manager == "npm" %}npm ci
npm run dev   # Nuxt or Next on :3000
npm run build
npm run test
npm run test:e2e
{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm install --frozen-lockfile
pnpm run dev
pnpm run build
pnpm run test
pnpm run test:e2e
{% else %}yarn install --frozen-lockfile
yarn run dev
yarn run build
yarn run test
yarn run test:e2e
{% endif %}
```
{% elif cookiecutter['__frontend_framework'] == "htmx" %}
HTMX is loaded from the CDN in `backend/templates/base.html`. Use Django views and partials as usual.
{% else %}
Templates use Tailwind via CDN in `backend/templates/base.html`.
{% endif %}

## Docker

Compose mounts the repo at `/app`. The **`backend`** service is built from [`docker/backend/Dockerfile`](docker/backend/Dockerfile) (Python + uv), uses `working_dir: /app/backend`, and exposes **:8000**.
{% if cookiecutter['__frontend_framework'] in ["vue", "react", "nuxt", "next"] %}
The **`frontend`** service is built from [`docker/frontend/Dockerfile`](docker/frontend/Dockerfile) (**Node {{ cookiecutter.node_version }}**), uses `working_dir: /app/frontend/{{ cookiecutter['__frontend_framework'] }}`, runs **`{{ cookiecutter.node_package_manager }} install`** then **`dev`** via the image `CMD`, and maps **{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}:5173{% else %}:3000{% endif %}** to your host. It **`depends_on`** **`backend`** (`service_started`) so the stack comes up in a sensible order.
{% endif %}

```bash
docker compose up --build
```

Copy `backend/.env.example` to `backend/.env` before first run (Compose uses `env_file: backend/.env`).
{% if cookiecutter.use_postgresql == "y" %}

**PostgreSQL ({{ cookiecutter.postgres_version }}):** the `db` service image is built from [`docker/postgres/Dockerfile`](docker/postgres/Dockerfile). Add OS-level packages there and/or SQL and shell scripts under [`docker/postgres/docker-entrypoint-initdb.d/`](docker/postgres/docker-entrypoint-initdb.d/) for `CREATE EXTENSION` and other one-time init ([`docker/postgres/README.md`](docker/postgres/README.md)).
{% endif %}

## Infrastructure

**Cloud bundle:** `{{ cookiecutter.cloud_provider }}`.

{% if cookiecutter.cloud_provider == "aws" %}
See `deploy/aws/terraform/` — configure `terraform.tfvars` with `project_name`, `environment`, then:

```bash
cd deploy/aws/terraform
terraform init
terraform plan
```
{% elif cookiecutter.cloud_provider == "gcp" %}
See `deploy/gcp/terraform/` — set `gcp_project_id` and run `terraform init && terraform plan`.
{% elif cookiecutter.cloud_provider == "azure" %}
See `deploy/azure/terraform/` — `terraform init && terraform plan` in that directory.
{% elif cookiecutter.cloud_provider == "heroku" %}
Copy `deploy/heroku/Procfile`, `runtime.txt`, and optionally `heroku.yml` to the repo root (or merge into your Heroku app). Commands assume `uv` and run from `backend/`.
{% elif cookiecutter.cloud_provider == "digitalocean" %}
Use `deploy/digitalocean/.do/app.yaml` as a starting point for App Platform ([`docker/backend/Dockerfile`](docker/backend/Dockerfile) builds `backend/`).
{% else %}
No cloud bundle selected — use Docker Compose for local development.
{% endif %}

## Celery and cache

{% if cookiecutter.use_redis_cache == "y" %}
Django uses **Redis** for the default cache (`REDIS_CACHE_URL`). Tests use in-memory cache instead.

{% endif %}
{% if cookiecutter.use_celery == "y" %}
Celery broker: **{{ cookiecutter.celery_broker }}** (`CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` in `backend/.env.example`). With Docker Compose, use **`celery-worker`** and **`celery-beat`** (same image as **`backend`**). Run locally from `backend/`:

```bash
cd backend
uv run celery -A src worker -l info
uv run celery -A src beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
{% else %}
Celery is disabled for this project.
{% endif %}
{% if cookiecutter.use_redis_cache == "y" or cookiecutter.use_celery == "y" %}

### Options at a glance

| Option                                     | Your choice                                                                                     |
|--------------------------------------------|-------------------------------------------------------------------------------------------------|
| Redis for Django cache (`REDIS_CACHE_URL`) | {% if cookiecutter.use_redis_cache == "y" %}yes{% else %}no{% endif %}                          |
| Celery                                     | {% if cookiecutter.use_celery == "y" %}yes{% else %}no{% endif %}                               |
| Celery broker                              | {% if cookiecutter.use_celery == "y" %}{{ cookiecutter.celery_broker }}{% else %}n/a{% endif %} |

**Local Docker:** see root `docker-compose.yml` — `redis` appears when cache or a Redis Celery broker is enabled; `rabbitmq` appears when Celery uses RabbitMQ. Celery runs as **`celery-worker`** and **`celery-beat`** services.

### Environment variables

{% if cookiecutter.use_redis_cache == "y" %}
- **`REDIS_CACHE_URL`** — Django default cache (`django.core.cache.backends.redis.RedisCache`). With Compose + Celery on Redis, use a dedicated logical DB index (e.g. `/2`) so it does not collide with broker/result URLs.
{% endif %}
{% if cookiecutter.use_celery == "y" %}
- **`CELERY_BROKER_URL`** — `redis://…` or `amqp://…` for RabbitMQ.
- **`CELERY_RESULT_BACKEND`** — e.g. `redis://…/1` when using Redis for results, or `rpc://` with RabbitMQ (default in `.env.example` for AMQP).
{% endif %}

### Production: AWS

- **Redis (cache + Celery results):** [ElastiCache for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html) in the same VPC as your app (ECS/EKS/Elastic Beanstalk). Point `REDIS_CACHE_URL` / `CELERY_RESULT_BACKEND` at the replication group endpoint.
- **RabbitMQ (Celery broker):** [Amazon MQ for RabbitMQ](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html) or a self-managed cluster; set `CELERY_BROKER_URL` to the AMQP URL.
- **Celery processes:** run **worker** and **beat** as separate ECS services / EKS Deployments / EB worker environments using the same container image as the Django app (`docker-compose.yml` **`backend`** / **`celery-*`** pattern), with commands matching Compose (`celery … worker` / `celery … beat`).

### Production: Google Cloud

- **Redis:** [Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis) (VPC). Use the instance host/port in `REDIS_CACHE_URL` and optionally `CELERY_RESULT_BACKEND`.
- **RabbitMQ:** [CloudAMQP](https://www.cloudamqp.com/) or self-managed on GCE/GKE; set `CELERY_BROKER_URL`.
- **Celery:** second and third [Cloud Run services](https://cloud.google.com/run/docs) or GKE workloads with the worker/beat commands.

### Production: Azure

- **Redis:** [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/). TLS URLs are common — ensure your client settings match (Django’s Redis backend supports `rediss://` when configured).
- **RabbitMQ:** Azure does not offer a first-party RabbitMQ PaaS; use [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/) with a RabbitMQ container, a partner offering, or CloudAMQP.
- **Celery:** separate Container Apps / App Service **worker** instances or AKS pods for worker and beat.

### Production: Heroku

- Add [**Heroku Redis**](https://devcenter.heroku.com/articles/heroku-redis) when using Django cache or Redis as broker/result store; add [**CloudAMQP**](https://elements.heroku.com/addons/cloudamqp) (or similar) when `CELERY_BROKER_URL` uses RabbitMQ.
- Scale processes: `heroku ps:scale worker=1 beat=1` (see root `Procfile` / `deploy/heroku/heroku.yml`).

### Production: DigitalOcean App Platform

{% if cookiecutter.cloud_provider == "digitalocean" %}
- See `deploy/digitalocean/.do/app.yaml`: **workers** `celery-worker` and `celery-beat` mirror the web service image and env.
{% else %}
- When using App Platform, add **workers** for `celery-worker` and `celery-beat` (see the DigitalOcean bundle in this template’s `deploy/digitalocean/.do/app.yaml` for a starting layout).
{% endif %}
- Provision [Managed Redis](https://docs.digitalocean.com/products/databases/redis/) or Managed Postgres as needed and bind secrets (`REDIS_CACHE_URL`, `DATABASE_URL`, `CELERY_*`).
- RabbitMQ is not offered as a managed DO database; use a third-party AMQP URL or run RabbitMQ on a Droplet/Kubernetes.

### Terraform stubs

{% if cookiecutter.cloud_provider != "none" %}
The `deploy/{{ cookiecutter.cloud_provider }}/terraform/` folder in this repo stays minimal (registry, storage, etc.). Add your own modules for ElastiCache, Amazon MQ, Memorystore, Azure Redis, and wire connection strings into your runtime environment.
{% else %}
If you add a cloud `deploy/` bundle later, extend its Terraform with managed Redis/RabbitMQ resources as needed.
{% endif %}
{% endif %}

## Documentation

{% if cookiecutter.documentation_provider == "none" %}
No hosted-documentation scaffold was selected. Add your own (MkDocs, Sphinx, GitBook, Notion, etc.) or re-run Cookiecutter with **`documentation_provider`** set to `gitbook`, `readthedocs`, `mkdocs`, or `notion`.
{% elif cookiecutter.documentation_provider == "gitbook" %}
Use **[`docs/GITBOOK.md`](docs/GITBOOK.md)** to connect [GitBook](https://www.gitbook.com/) to this repository. A short index lives in [`docs/README.md`](docs/README.md).
{% elif cookiecutter.documentation_provider == "readthedocs" %}
**[Read the Docs](https://readthedocs.org/)** builds the **MkDocs** site in this repo. Import the project in RTD; configuration is in [`.readthedocs.yaml`](.readthedocs.yaml). Local preview: `pip install -r docs/requirements.txt && mkdocs serve`. See also [`docs/README.md`](docs/README.md).
{% elif cookiecutter.documentation_provider == "mkdocs" %}
**MkDocs** (Material theme) with **[GitHub Actions](.github/workflows/docs.yml)** publishing to the **`gh-pages`** branch. Enable **GitHub Pages** (Settings → Pages → source `gh-pages`). Local preview: `pip install -r docs/requirements.txt && mkdocs serve`. See [`docs/README.md`](docs/README.md).
{% else %}
**[Notion](https://www.notion.so/)** — see **[`docs/NOTION.md`](docs/NOTION.md)** for a lightweight setup guide and [`docs/README.md`](docs/README.md).
{% endif %}

## License

{% if cookiecutter.license == "Proprietary" %}
This software is **proprietary**. See [`LICENSE`](LICENSE) for terms. Contact **{{ cookiecutter.author_name }}** for permissions.
{% else %}
Licensed under **{{ cookiecutter.license }}**. See the [`LICENSE`](LICENSE) file for the full text.
{% endif %}
