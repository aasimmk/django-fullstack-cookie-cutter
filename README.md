# 🍪 django-cookie-cutter

**django-cookie-cutter** is a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template that scaffolds a production-minded Django monorepo: a **`backend/`** app (project package under **`src/`**, [uv](https://github.com/astral-sh/uv), **Ruff**, **pytest**), optional **Vue 3** or **React 18/19** (**Vite 5/6**, Tailwind, Vitest, Playwright, **django-vite**), optional **Nuxt 3/4** or **Next.js 14/15** (standalone on port 3000 with Vitest + Playwright), optional **HTMX** (CDN major 1 or 2), and optional **PostgreSQL**, **Redis** caching, and **Celery** (Redis or RabbitMQ broker) with matching **Docker Compose** services (**`docker/backend/`** + optional **`docker/frontend/`** images) and **GitHub Actions** CI.

[![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-D4AA00?logo=cookiecutter&logoColor=white&style=flat)](https://github.com/cookiecutter/cookiecutter)
[![Django](https://img.shields.io/static/v1?label=Django&message=4.2%20%7C%205.0%20%7C%205.1%20%7C%205.2&color=092E20&logo=django&logoColor=white&style=flat)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/static/v1?label=Python&message=3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13&color=3776AB&logo=python&logoColor=white&style=flat)](https://www.python.org/)
[![uv](https://img.shields.io/static/v1?label=uv&message=backend%20deps%20%26%20CI&color=DE5FE9&style=flat)](https://github.com/astral-sh/uv)
[![PostgreSQL](https://img.shields.io/static/v1?label=PostgreSQL&message=15%20%7C%2016%20%7C%2017%20%7C%2018&color=4169E1&logo=postgresql&logoColor=white&style=flat)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/static/v1?label=Redis%20%28Compose%29&message=7&color=DC382D&logo=redis&logoColor=white&style=flat)](https://redis.io/)
[![RabbitMQ](https://img.shields.io/static/v1?label=RabbitMQ%20%28Compose%29&message=3.x&color=FF6600&logo=rabbitmq&logoColor=white&style=flat)](https://www.rabbitmq.com/)
[![Docker](https://img.shields.io/static/v1?label=Docker&message=Compose%20%2B%20backend%2Ffrontend%20images&color=2496ED&logo=docker&logoColor=white&style=flat)](https://docs.docker.com/compose/)
[![Node.js](https://img.shields.io/static/v1?label=Node.js&message=20%20%7C%2022%20%7C%2024%20%7C%2025%20%7C%2026&color=339933&logo=nodedotjs&logoColor=white&style=flat)](https://nodejs.org/)
[![npm](https://img.shields.io/static/v1?label=npm%20%7C%20pnpm%20%7C%20yarn&message=SPA%20install&color=CB3837&logo=npm&logoColor=white&style=flat)](https://www.npmjs.com/)

[![Frontend: none](https://img.shields.io/static/v1?label=Frontend&message=none%20%28Django%20templates%29&color=0C4A6E&logo=django&logoColor=white&style=flat)](#prompts)
[![HTMX](https://img.shields.io/static/v1?label=HTMX&message=django%2Dhtmx%20%C2%B7%20CDN%201%20%7C%202&color=3D72D7&logo=htmx&logoColor=white&style=flat)](https://htmx.org/)
[![Vue](https://img.shields.io/static/v1?label=Vue&message=3%20%C2%B7%20Vite%205%20%7C%206&color=4FC08D&logo=vuedotjs&logoColor=white&style=flat)](https://vuejs.org/)
[![React](https://img.shields.io/static/v1?label=React&message=18%20%7C%2019%20%C2%B7%20Vite%205%20%7C%206&color=20232A&logo=react&logoColor=61DAFB&style=flat)](https://react.dev/)
[![Nuxt](https://img.shields.io/static/v1?label=Nuxt&message=3%20%7C%204&color=00DC82&logo=nuxt&logoColor=white&style=flat)](https://nuxt.com/)
[![Next.js](https://img.shields.io/static/v1?label=Next.js&message=14%20%7C%2015%20%C2%B7%20App%20Router&color=000000&logo=nextdotjs&logoColor=white&style=flat)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/static/v1?label=Tailwind%20CSS&message=CDN%20%7C%20Vite%20build&color=06B6D4&logo=tailwindcss&logoColor=white&style=flat)](https://tailwindcss.com/)

[![pytest](https://img.shields.io/static/v1?label=pytest&message=django%20%2B%20coverage&color=0A9EDC&logo=pytest&logoColor=white&style=flat)](https://pytest.org/)
[![Vitest](https://img.shields.io/static/v1?label=Vitest&message=SPA%20%28v2%20%7C%20v3%29&color=6E9F18&logo=vitest&logoColor=white&style=flat)](https://vitest.dev/)
[![Playwright](https://img.shields.io/static/v1?label=Playwright&message=e2e&color=45ba4b&logo=playwright&logoColor=white&style=flat)](https://playwright.dev/)
[![GitHub Actions](https://img.shields.io/static/v1?label=CI&message=generated%20repos&color=2088FF&logo=githubactions&logoColor=white&style=flat)](README.md#github-actions-in-generated-projects)

[![AWS](https://img.shields.io/static/v1?label=AWS&message=Terraform%20bundle&color=232F3E&logo=amazonaws&logoColor=white&style=flat)](https://aws.amazon.com/)
[![GCP](https://img.shields.io/static/v1?label=GCP&message=Terraform%20bundle&color=4285F4&logo=googlecloud&logoColor=white&style=flat)](https://cloud.google.com/)
[![Azure](https://img.shields.io/static/v1?label=Azure&message=Terraform%20bundle&color=0078D4&logo=microsoftazure&logoColor=white&style=flat)](https://azure.microsoft.com/)
[![Heroku](https://img.shields.io/static/v1?label=Heroku&message=Procfile%20%2F%20docker%2Fbackend&color=430098&logo=heroku&logoColor=white&style=flat)](https://www.heroku.com/)
[![DigitalOcean](https://img.shields.io/static/v1?label=DigitalOcean&message=App%20Platform&color=0080FF&logo=digitalocean&logoColor=white&style=flat)](https://www.digitalocean.com/)
[![Cloud: none](https://img.shields.io/static/v1?label=Cloud&message=none%20%28Compose%20only%29&color=2496ED&logo=docker&logoColor=white&style=flat)](https://docs.docker.com/compose/)

[![GitBook](https://img.shields.io/static/v1?label=GitBook&message=Git%20sync&color=3884FF&logo=gitbook&logoColor=white&style=flat)](https://www.gitbook.com/)
[![Read the Docs](https://img.shields.io/static/v1?label=Read%20the%20Docs&message=MkDocs&color=8CA1AF&logo=readthedocs&logoColor=white&style=flat)](https://readthedocs.org/)
[![MkDocs](https://img.shields.io/static/v1?label=MkDocs&message=Material%20%2B%20GitHub%20Pages&color=526C82&logo=markdown&logoColor=white&style=flat)](https://www.mkdocs.org/)
[![Notion](https://img.shields.io/static/v1?label=Notion&message=wiki%20guide&color=000000&logo=notion&logoColor=white&style=flat)](https://www.notion.so/)
[![Docs: none](https://img.shields.io/static/v1?label=Docs&message=none%20%28README%20only%29&color=6B7280&style=flat)](#prompts)

## ⚡ Quick start

```bash
pip install "cookiecutter>=2.0"
# or: uv tool install cookiecutter

cookiecutter gh:YOUR_ORG/django-cookie-cutter
# or from a local checkout of this repository:
cookiecutter /path/to/django-cookie-cutter
```

Cookiecutter writes a new directory named after **`project_slug`**. See [Usage](#usage) for the full variable list and what runs after generation.

## 📑 Index

- [Quick start](#quick-start)
- [Introduction](#introduction)
- [Generated project structure](#generated-project-structure)
- [Choosing your stack](#choosing-your-stack)
- [Features](#features)
- [GitHub Actions in generated projects](#github-actions-in-generated-projects)
- [Usage](#usage)
  - [Prompts](#prompts)
- [Template layout](#template-layout)
- [Demo recording](#demo-recording)
- [Customizing this template](#customizing-this-template)
- [FAQ](#faq)
- [Compared to other templates](#compared-to-other-templates)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Requirements](#requirements)
- [License](#license)

## 🧭 Introduction

This repository is the **template source**, not a runnable Django app. Running Cookiecutter against it renders a new directory (your `project_slug`) containing a complete project you can version-control and deploy.

**🎯 Design goals:** sensible defaults, minimal magic, and choices you make up front (Django/Python versions, frontend, database, cache, task queue, cloud bundle, **open-source or proprietary license**, optional DRF API) so generated trees stay small and match what you actually use. Post-generation hooks prune unused `frontend/` and `deploy/` subtrees, align SPA lockfiles with your package manager, and optionally run **`uv sync`** so the backend environment is ready quickly.

**🚀 Typical uses:** greenfield APIs or server-rendered apps, SPAs backed by Django, teams standardizing on uv + Ruff, and projects that want Terraform or platform YAML stubs plus Docker Compose for local parity with production-ish services (Postgres, Redis, RabbitMQ, Celery worker/beat). Optional **documentation host** scaffolding (**GitBook**, **Read the Docs** + MkDocs, **MkDocs** + GitHub Pages, or **Notion**) is trimmed post-generation to match your choice.

## 🌳 Generated project structure

After you run Cookiecutter, the output is a single repo folder (your `project_slug`) with a layout similar to the tree below. Optional paths depend on your answers at the prompts; post-generation hooks delete branches you did not select.

```text
<project_slug>/
├── README.md                 # quick start + stack-specific notes for the new repo
├── AGENTS.md                 # AI / human orientation for the generated tree
├── LICENSE
├── .editorconfig
├── docker/backend/Dockerfile   # Django + uv (Compose + Heroku/DO when used)
├── docker/frontend/Dockerfile   # removed with frontend/ when SPA not selected
├── docker-compose.yml
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .env.example
│   ├── manage.py
│   ├── tox.ini               # only when use_tox = y
│   ├── src/                  # Django project package (settings, apps, urls)
│   └── tests/
├── frontend/                 # vue/, react/, nuxt/, or next/ when that SPA is selected (else removed)
├── deploy/                   # only when cloud_provider is not none
├── docker/postgres/          # only when use_postgresql = y
├── docs/                     # trimmed to match documentation_provider
├── mkdocs.yml                # only for mkdocs / readthedocs paths
├── .readthedocs.yaml         # only when documentation_provider = readthedocs
└── .github/workflows/
    ├── ci.yml                # backend (+ optional frontend + tox)
    └── docs.yml              # only when documentation_provider = mkdocs (MkDocs → gh-pages)
```

## 🤔 Choosing your stack

Use this as a shortcut before you read the full feature tables.

| If you want… | Sensible defaults |
| --- | --- |
| JSON API only, no SPA | `frontend_framework` = `none`, `api_project` = `y`; optional `openapi_schema` = `drf-spectacular` (OpenAPI 3) or `drf-yasg` (OpenAPI 2) |
| Server-rendered HTML with progressive enhancement | `frontend_framework` = `htmx` |
| Separate SPA with Django as API or hybrid | `frontend_framework` = `vue`, `react`, `nuxt`, or `next`; set **`vue_major_version`**, **`vite_major_version`**, **`react_major_version`**, **`nuxt_major_version`**, or **`next_major_version`** as prompted; set `node_version` + `node_package_manager` (`vue`/`react` use **django-vite** + :5173; `nuxt`/`next` on **:3000** when **`api_project`** is `y`) |
| Local DB without Docker Postgres | `use_postgresql` = `n` (SQLite for dev; pytest still uses `src.settings.test`) |
| Production-like local stack | `use_postgresql` = `y`, tune `postgres_version`; add Redis / Celery if you need them in dev |
| Background jobs | `use_celery` = `y`, then `celery_broker` = `redis` or `rabbitmq` to match ops |
| Managed cloud stubs | `cloud_provider` for AWS / GCP / Azure (Terraform), Heroku, or DigitalOcean; `none` keeps Compose-only deploy story |
| Hosted docs | `documentation_provider` other than `none`; extras are removed in `post_gen` |
| One command to mirror CI locally | `use_tox` = `y` (adds `backend/tox.ini` and a Tox job in GitHub Actions) |
| gettext / translated templates | `use_i18n` = `y` (`LocaleMiddleware`, `backend/locale/`, `/i18n/setlang/`) |

Compatibility rules (unsupported combinations) are enforced in `hooks/pre_gen_project.py` before any files are written (for example Django/Python pairs, and **`openapi_schema` must be `none` when `api_project` is `n`**).

## ✨ Features

Use the tables as a map from **what you pick at the prompt** to **what lands in the generated repo**. Anything not controlled by a variable is marked **Always**.

### 🐍 Backend and API

| What you get | Tuned by | Notes |
| --- | --- | --- |
| Django + Python pairing | `django_version`, `python_version` | 4.2–5.2 and 3.10–3.13; compatibility checked in `hooks/pre_gen_project.py` |
| Project package under `backend/src/` | **Always** | Settings modules `local`, `development`, `staging`, `production`, plus `test` for pytest |
| Env loading + typed helpers | **Always** | `src/settings/_env.py`, `python-dotenv`, `backend/.env` via `backend/.env.example` |
| `DATABASES` (Postgres vs SQLite) | `use_postgresql` | `y`: **psycopg** + **`DATABASE_URL`** parsed with **django-environ** in `base.py`. `n`: SQLite file under `backend/` |
| Dependency & run tooling | **Always** | [uv](https://github.com/astral-sh/uv), `backend/pyproject.toml` / `uv.lock`, WhiteNoise, Gunicorn |
| REST API (DRF, CORS, sample routes) | `api_project` | **Django REST Framework**, **django-cors-headers**, `src.apps.api`, `/api/v1/…` |
| OpenAPI / Swagger docs for the API | `openapi_schema` (only when `api_project` = `y`) | `none`, **drf-spectacular** (OpenAPI 3), or **drf-yasg** (OpenAPI 2); adds deps, `INSTALLED_APPS`, schema URLs, and smoke tests |
| Lint, format, tests, typing | **Always** | Ruff; pytest + pytest-django + pytest-cov; mypy + django-stubs |
| Tox aggregate checks + CI step | `use_tox` | `backend/tox.ini` (tox-uv: `py`, `ruff`, `migrate`), dev deps, optional GitHub Actions Tox job |
| gettext / locale / `LocaleMiddleware` | `use_i18n` | **`y`:** `USE_I18N`, `LANGUAGES`, `LOCALE_PATHS`, `backend/locale/`, `/i18n/` includes `set_language`, template `i18n` context · **`n`:** `post_gen` drops `backend/locale/` |

### 🎨 Frontend and UI

| What you get | Tuned by | Notes |
| --- | --- | --- |
| Server templates + Tailwind CDN | `frontend_framework` = `none` | Default Django templates |
| HTMX | `frontend_framework` = `htmx` | **django-htmx** + CDN assets; **`htmx_major_version`** picks HTMX 1.x vs 2.x on the CDN |
| Vue or React SPA | `frontend_framework` = `vue` / `react` | **`vue_major_version`** / **`vite_major_version`** (Vue) or **`react_major_version`** / **`vite_major_version`** (React); Tailwind, **django-vite**, build to `backend/static/dist` |
| Nuxt or Next SPA | `frontend_framework` = `nuxt` / `next` | **`nuxt_major_version`** (3 or 4, SPA mode) or **`next_major_version`** (14 or 15, App Router); dev server on **:3000**; use **`api_project`** = `y` for browser CORS to Django |
| Node version + lockfile tool | `node_version`, `node_package_manager` | Used for Vue/React/Nuxt/Next and CI; `frontend/.nvmrc`; post_gen aligns lockfile when possible |
| SPA unit + e2e tests | `frontend_framework` = `vue` / `react` / `nuxt` / `next` | Vitest + Playwright |
| Safe copy for `{{ … }}` in SPA files | **Always** (template) | `cookiecutter.json` `_copy_without_render` for Vue `.vue` and React `.tsx`/`.css` that contain framework mustaches; extend globs if you add files with literal `{{` that must not pass through Jinja |

### 🗄️ Data, cache, and background jobs

| What you get | Tuned by | Notes |
| --- | --- | --- |
| PostgreSQL in Compose | `use_postgresql`, `postgres_version` | `db` service from `docker/postgres/Dockerfile` (15–18), `docker-entrypoint-initdb.d/` for extensions |
| Redis as Django cache | `use_redis_cache` | `django.core.cache.backends.redis.RedisCache`, `REDIS_CACHE_URL`, `redis` package |
| Celery worker + beat | `use_celery`, `celery_broker` | **django-celery-beat**; broker Redis or RabbitMQ; Compose services; production runbooks live in the generated **README** → *Celery and cache* when Redis or Celery is on |

### 📋 Project metadata, docs, license, editor

| What you get | Tuned by | Notes |
| --- | --- | --- |
| Name, slug, description, author, i18n | `project_name`, `project_slug`, `description`, `author_name`, `email`, `use_i18n` | `pyproject.toml` / README metadata; gettext + `locale/` when `use_i18n` is `y` |
| Documentation host scaffold | `documentation_provider` | `none`, GitBook, Read the Docs + MkDocs, MkDocs + GitHub Pages, or Notion; extras removed in post_gen |
| SPDX or proprietary license | `license` | Root `LICENSE` + `[project].license` in `backend/pyproject.toml`; year stamped in post_gen |
| Shared editor rules | **Always** | Root `.editorconfig` |
| AI / agent hints | **Always** | `AGENTS.md`, `.cursor/rules/project-guidelines.mdc`, `.claude/` snippets reflect your choices |

### ☁️ Cloud, CI, and containers

| What you get | Tuned by | Notes |
| --- | --- | --- |
| Deploy starter (Terraform / platform YAML) | `cloud_provider` | AWS, GCP, Azure (Terraform); Heroku (`Procfile`, `heroku.yml`); DigitalOcean App Platform (incl. Celery workers when Celery is on); `none` drops extra `deploy/` trees |
| GitHub Actions | **Always** (with options) | Backend: uv sync, Ruff, migrations check, pytest; SPA build/test when Vue/React/Nuxt/Next; optional Tox job |
| Production image + local stack | **Always** (with options) | `{{ cookiecutter.project_slug }}/docker/backend/Dockerfile` for `backend/`; optional `{{ cookiecutter.project_slug }}/docker/frontend/Dockerfile` when Vue/React/Nuxt/Next (`post_gen` removes it with `frontend/` otherwise); `docker-compose.yml` for **`backend`** (+ **`frontend`** when SPA), optional Postgres, Redis, RabbitMQ, Celery; env vars documented in `backend/.env.example` |

### 🪝 Hooks

| Script | Role |
| --- | --- |
| `hooks/pre_gen_project.py` | Validates slug, Django/Python matrix, Postgres major, Celery broker, documentation provider, license, `use_tox`, `use_i18n`, and `openapi_schema` vs `api_project` |
| `hooks/post_gen_project.py` | Prunes unused `frontend/` and `deploy/` trees, `docker/frontend/` when no SPA, `docker/postgres/` when Postgres off, docs scaffolds, `backend/tox.ini` when Tox off; SPA lockfile alignment; `LICENSE` year; `uv sync` + Ruff format in `backend/` when uv is available |

## 🔁 GitHub Actions in generated projects

The rendered repo includes `.github/workflows/ci.yml`, which runs on pushes and pull requests to **`main`**.

**Backend job** (always; working directory `backend/`):

1. Checkout and [setup-uv](https://github.com/astral-sh/setup-uv) with your chosen Python version.
2. **`uv sync`** (`--frozen` when the lockfile supports it).
3. **Ruff** — `ruff check` and `ruff format --check`.
4. **Migrations** — `makemigrations --check --dry-run`.
5. **Pytest** — `uv run pytest`.
6. **Tox** (only when `use_tox` = `y`) — `tox run -e py,ruff,migrate` via uv.

**Frontend job** (when `frontend_framework` is `vue`, `react`, `nuxt`, or `next`): checkout, Node setup with lockfile caching, install (`npm ci`, `pnpm install --frozen-lockfile`, or `yarn install --frozen-lockfile`), then `test` (if defined) and `build`.

When `documentation_provider` is **`mkdocs`**, `.github/workflows/docs.yml` also publishes MkDocs to the **`gh-pages`** branch on pushes that touch `docs/**` or `mkdocs.yml` (enable GitHub Pages on that branch in repo settings).

## 🚀 Usage

```bash
pip install "cookiecutter>=2.0"
# or: uv tool install cookiecutter

cookiecutter gh:YOUR_ORG/django-cookie-cutter
# or from a local checkout:
cookiecutter /path/to/django-cookie-cutter
```

### 💬 Prompts

Cookiecutter asks variables **in the order they appear in `cookiecutter.json`**: project metadata first, then Django/backend, database, cache and Celery, frontend, then cloud and docs.

| Variable                 | Description                                                                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Project** | |
| `project_name`           | Human-readable name                                                                                                                                                             |
| `project_slug`           | Python/import-safe slug for the output folder and package metadata (default derives from `project_name`)                                                                      |
| `description`            | Short project blurb (`pyproject.toml`, generated README)                                                                                                                       |
| `author_name`            | Author for package metadata                                                                                                                                                     |
| `email`                  | Contact email for package metadata                                                                                                                                              |
| `license`                | `MIT`, `Apache-2.0`, `BSD-3-Clause`, `GPL-3.0-or-later`, `AGPL-3.0-or-later`, or `Proprietary` — root `LICENSE` and `backend/pyproject.toml`                                     |
| `use_i18n`               | `y` / `n` — gettext / `LocaleMiddleware` / `backend/locale/` / `/i18n/`; **`n`** removes `backend/locale/` in `post_gen`                                                         |
| **Django / backend** | |
| `django_version`         | 5.2, 5.1, 5.0, or 4.2                                                                                                                                                           |
| `python_version`         | 3.13, 3.12, 3.11, or 3.10 (must match Django support; `pre_gen` checks)                                                                                                         |
| `api_project`            | `y` / `n` — **DRF**, **django-cors-headers**, `src/apps.api`, `/api/v1/…`                                                                                                                                        |
| `openapi_schema`         | `none`, **drf-spectacular** (OpenAPI 3), or **drf-yasg** (OpenAPI 2) — only with `api_project=y` (`pre_gen` enforces)                                                          |
| `use_tox`                | `y` / `n` — **`backend/tox.ini`** (tox-uv), dev deps, optional CI Tox job                                                                                                                                        |
| **Database** | |
| `use_postgresql`         | `y` / `n` — Postgres vs SQLite (pytest still uses SQLite via `src.settings.test`)                                                                                                |
| `postgres_version`       | `18`, `17`, `16`, or `15` — Compose `db` image; ignored when `use_postgresql` is `n`                                                                                            |
| **Cache & tasks** | |
| `use_redis_cache`        | `y` / `n` — Redis as Django cache (`REDIS_CACHE_URL`)                                                                                                                            |
| `use_celery`             | `y` / `n`                                                                                                                                                                       |
| `celery_broker`          | `redis` or `rabbitmq` — when `use_celery` is `y`                                                                                                                                 |
| **Frontend** | |
| `frontend_framework`     | `none`, `htmx`, `vue`, `react`, `nuxt`, `next`                                                                                                                                  |
| `vue_major_version`      | `3` — when `frontend_framework` is `vue`, dependencies use **caret major** ranges (e.g. `^3`) so installs pick the latest **3.x**                                                                                    |
| `vite_major_version`     | `6` or `5` — when `frontend_framework` is `vue` or `react` (`^6` / `^5` for Vite and matching Vitest major)                                                                                                               |
| `react_major_version`    | `18` or `19` — when `frontend_framework` is `react` (`^18` / `^19` for React and matching `@types/*`)                                                                                                                      |
| `nuxt_major_version`     | `3` or `4` — when `frontend_framework` is `nuxt` (`^3` / `^4` for Nuxt, `^3` for Vue, `^4` / `^5` for vue-router)                                                                                                                          |
| `next_major_version`     | `15` or `14` — when `frontend_framework` is `next` (`^14` / `^15` for Next; `^18` / `^19` for React to match)                                                                        |
| `htmx_major_version`     | `2` or `1` — used when `frontend_framework` is `htmx` (CDN URL + SRI in `backend/templates/base.html`)                                                                       |
| `node_version`           | `20`, `22`, `24`, `25`, or `26` — when `frontend_framework` is `vue`, `react`, `nuxt`, or `next`                                                                                |
| `node_package_manager`   | `npm`, `pnpm`, or `yarn` — same scope as `node_version`                                                                                                                          |
| **Cloud & docs** | |
| `cloud_provider`         | `none`, `aws`, `gcp`, `azure`, `heroku`, `digitalocean`                                                                                                                         |
| `documentation_provider` | `none`, `gitbook`, `readthedocs`, `mkdocs`, or `notion` — docs scaffold under `docs/`                                                                                           |

⚙️ After generation, `hooks/post_gen_project.py` removes unused `frontend/*` and `deploy/*` trees, drops `docker/frontend/` when the frontend is not a Node SPA, drops `docker/postgres/` when PostgreSQL is disabled, prunes unused documentation-provider files, removes `backend/tox.ini` when Tox is disabled, removes **`backend/locale/`** when **`use_i18n`** is **`n`**, refreshes the SPA lockfile for the chosen package manager when possible, and runs `uv sync` when `uv` is available.

## 🗂️ Template layout

- 📁 `{{ cookiecutter.project_slug }}/` — rendered repo with root **`LICENSE`**, **`.editorconfig`**, `docker/backend/Dockerfile`, optional `docker/frontend/` (Node SPA only), `backend/` (Django in `src/` + uv, optional **`backend/tox.ini`** when `use_tox` is `y`), optional `frontend/`, and `deploy/`
- 🔍 `hooks/pre_gen_project.py` — Django / Python version compatibility checks; validates frontend **major** version choices (`vue_major_version`, `vite_major_version`, `react_major_version`, `nuxt_major_version`, `next_major_version`, `htmx_major_version`)
- ✂️ `hooks/post_gen_project.py` — prune options, documentation scaffold, SPA lockfiles, optional Tox file, `backend/locale/` when `use_i18n` is `n`, `uv sync`
- ⚙️ `cookiecutter.json` — defaults and `_copy_without_render` for Vue/React sources that contain literal `{{` … `}}` mustaches

## 🎬 Demo recording

A short terminal recording ([asciinema](https://asciinema.org/) or a GIF) of running `cookiecutter` against this template and listing the resulting tree helps newcomers see the prompts and output in one glance. If you publish one, add an embed or link here.

## 🛠️ Customizing this template

- **Prompts and defaults** live in [`cookiecutter.json`](cookiecutter.json). Keep **key order** as users see it at the terminal: generic project fields → Django/backend → database → cache/Celery → `frontend_framework` → **frontend major versions** (`vue_major_version`, `vite_major_version`, `react_major_version`, `nuxt_major_version`, `next_major_version`, `htmx_major_version`) → `node_version` / `node_package_manager` → cloud/docs → `_copy_without_render` last. New keys should have sensible defaults and be read in `hooks/pre_gen_project.py` / `hooks/post_gen_project.py` when they affect validation or pruning (for example `openapi_schema` is validated against `api_project`, and frontend majors are validated in `pre_gen_project.py`).
- **Conditional files** use Jinja2 (`{% if cookiecutter… %}`) inside `{{ cookiecutter.project_slug }}/`. Keep branches in sync with what `post_gen_project.py` removes so generated trees stay minimal.
- **Do not process** Vue/React/Nuxt/Next sources that contain literal `{{` … `}}` as template syntax: extend `_copy_without_render` in `cookiecutter.json` when adding new globs.
- **Test locally** with `cookiecutter /absolute/path/to/django-cookie-cutter --no-input` (uses defaults from `cookiecutter.json`) or a [replay file](https://cookiecutter.readthedocs.io/en/latest/advanced/replay.html) (`--replay` / `--replay-file`), then inspect the output directory.

## ❓ FAQ

**Why is this repo not a runnable Django app?**  
It is the Cookiecutter *source*. Only the generated `<project_slug>/` tree is a project you `cd` into and run.

**Why did `pre_gen_project` exit with an error?**  
Unsupported pairs (for example Django and Python versions that do not match upstream support) and invalid combinations are rejected before files are created. Open `hooks/pre_gen_project.py` for the exact rules.

**Why did post-generation `uv sync` not run?**  
`post_gen_project.py` runs `uv sync` only when the `uv` executable is available on your `PATH` at generation time. You can always `cd <project_slug>/backend && uv sync` manually.

**Can I re-run Cookiecutter on top of an existing project?**  
Cookiecutter does not merge into an existing app safely. Generate a fresh directory or apply changes by hand / via patches.

**Why are some SPA files copied without Jinja rendering?**  
Cookiecutter’s `_copy_without_render` copies matching paths literally so Vue `{{` mustache syntax (and similar in React templates) is not eaten by Jinja.

**Where is environment variable documentation?**  
In the generated project, see `backend/.env.example` and the **Celery and cache** section of `README.md` when Redis cache or Celery is enabled.

## 🆚 Compared to other templates

| | **django-cookie-cutter** (this repo) | Typical “batteries included” Django cookiecutters |
| --- | --- | --- |
| **Layout** | Monorepo: `backend/` + optional `frontend/`, optional `deploy/` | Often single Django tree or older pip-centric layout |
| **Python tooling** | **uv**, Ruff, pytest (+ optional tox-uv) | Often pip/poetry + separate tool choices |
| **Frontend** | `none` / HTMX / Vue / React (django-vite) / Nuxt / Next | Often templates-only or one SPA choice |
| **Infra** | Optional Terraform or platform YAML per cloud; Compose for local parity | Varies widely; not always a first-class option |
| **Docs / AI** | Optional docs host scaffold; `AGENTS.md` and Cursor rules in the output | Varies |

Other community templates (for example [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)) optimize for different defaults and file layouts—pick the template whose opinions match your team.

## 🤝 Contributing

Issues and pull requests are welcome. When you change prompts or hooks, regenerate a sample project locally and smoke-test `backend` (migrate, pytest) and, when applicable, the SPA build. Keep hook logic and `cookiecutter.json` defaults aligned so first-time runs stay smooth.

## 📰 Changelog

Notable template changes are best tracked through **[GitHub Releases](https://github.com/YOUR_ORG/django-cookie-cutter/releases)** once you publish this repository under your org or fork—tag releases so downstream teams can pin a known-good revision.

## 📦 Requirements

- 🍪 **Cookiecutter** 2.x (to expand the template)
- 🐍 **For generated projects:** [uv](https://github.com/astral-sh/uv), a Python matching the chosen `python_version`, and—if you select Vue, React, Nuxt, or Next—a **Node.js** install matching the chosen `node_version` (for local dev and CI)

## 📄 License

This template repository is not tied to a single SPDX license. When you generate a project, pick **`license`** at the prompt; the rendered repo includes a matching root **`LICENSE`** and metadata in **`backend/pyproject.toml`**.