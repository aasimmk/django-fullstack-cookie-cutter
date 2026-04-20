# Workflow Command Recipes

Use these as reference prompts/steps when working with Claude Code.

## 1) Understand a feature area
1. Read `AGENTS.md`.
2. Identify relevant app/module:
   - Backend: `backend/src/apps/...`
{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
   - Frontend: `frontend/{{ cookiecutter['__frontend_framework'] }}/src/...`
{% elif cookiecutter['__frontend_framework'] == "nuxt" %}
   - Frontend: `frontend/nuxt/` (`app.vue`, `nuxt.config.ts`, …)
{% elif cookiecutter['__frontend_framework'] == "next" %}
   - Frontend: `frontend/next/app/...`
{% endif %}
3. Locate existing tests first.

## 2) Implement a backend change
1. Update code in `backend/src/...`.
2. If you change models or schema-related code, generate migrations with Django (`cd backend && uv run python manage.py makemigrations`); prefer idempotent, data-safe migrations and ask when behavior is ambiguous.
3. Add/adjust tests in `backend/tests/unit`, `backend/tests/integration`, or `backend/tests/e2e` (or app-level tests).
4. Run:
   - `cd backend && uv run ruff check .`
   - `cd backend && uv run pytest`

## 3) Implement frontend change
{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
1. Edit `frontend/{{ cookiecutter['__frontend_framework'] }}/src/...`.
2. Update tests under `frontend/{{ cookiecutter['__frontend_framework'] }}/tests/unit`, `tests/integration`, or `tests/e2e` (Playwright).
3. Run:
   - `cd frontend/{{ cookiecutter['__frontend_framework'] }} && {% if cookiecutter.node_package_manager == "npm" %}npm run test{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm run test{% else %}yarn run test{% endif %}`
   - `cd frontend/{{ cookiecutter['__frontend_framework'] }} && {% if cookiecutter.node_package_manager == "npm" %}npm run build{% elif cookiecutter.node_package_manager == "pnpm" %}pnpm run build{% else %}yarn run build{% endif %}`
{% elif cookiecutter['__frontend_framework'] in ["nuxt", "next"] %}
1. Edit `frontend/{{ cookiecutter['__frontend_framework'] }}/` sources.
2. Update `tests/unit` and `tests/e2e` as needed.
3. Run the same `test` / `build` commands as in `AGENTS.md` (from `frontend/{{ cookiecutter['__frontend_framework'] }}/`).
{% else %}
1. Edit Django templates/views.
2. Verify behavior with Django tests and local runserver.
{% endif %}

## 4) API changes
{% if cookiecutter.api_project == "y" %}
1. Add routes under `backend/src/apps/api/urls.py`.
2. Add views/serializers in `backend/src/apps/api/`.
3. Keep API versioning under `/api/v1/...`.
{% if cookiecutter.openapi_schema == "drf-spectacular" %}
4. Keep OpenAPI 3 metadata accurate (drf-spectacular: `@extend_schema`, `extend_schema_view`, `Serializer` fields); verify `GET /api/schema/` after API changes.
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
4. Keep OpenAPI 2 / Swagger metadata accurate (drf-yasg `swagger_auto_schema` on views where needed); verify `GET /api/swagger.json` after API changes.
{% endif %}
{% else %}
1. If introducing APIs, start with `/api/v1/...` versioned routes.
2. Add tests for status codes and response shape.
{% endif %}
