"""Validate cookiecutter variables before project generation (rendered by Cookiecutter)."""

import re
import sys

django_version = "{{ cookiecutter.django_version }}"
python_version = "{{ cookiecutter.python_version }}"
project_slug = "{{ cookiecutter.project_slug }}"
postgres_version = "{{ cookiecutter.postgres_version }}"
celery_broker = "{{ cookiecutter.celery_broker }}"
documentation_provider = "{{ cookiecutter.documentation_provider }}"
license_choice = "{{ cookiecutter.license }}"
use_tox = "{{ cookiecutter.use_tox }}"
api_project = "{{ cookiecutter.api_project }}"
openapi_schema = "{{ cookiecutter.openapi_schema }}"
use_i18n = "{{ cookiecutter.use_i18n }}"
frontend_stack = "{{ cookiecutter.frontend_stack }}"

ALLOWED_POSTGRES_VERSIONS = frozenset({"15", "16", "17", "18"})
ALLOWED_CELERY_BROKERS = frozenset({"redis", "rabbitmq"})
ALLOWED_DOCS_PROVIDERS = frozenset(
    {"none", "gitbook", "readthedocs", "mkdocs", "notion"},
)
ALLOWED_TOX = frozenset({"n", "y"})
ALLOWED_USE_I18N = frozenset({"n", "y"})
ALLOWED_OPENAPI_SCHEMA = frozenset({"none", "drf-spectacular", "drf-yasg"})

ALLOWED_FRONTEND_STACK = frozenset(
    {
        "none",
        "htmx_2",
        "htmx_1",
        "vue_3_vite_6",
        "vue_3_vite_5",
        "react_18_vite_6",
        "react_18_vite_5",
        "react_19_vite_6",
        "react_19_vite_5",
        "nuxt_3",
        "nuxt_4",
        "next_15",
        "next_14",
    },
)

ALLOWED_LICENSES = frozenset(
    {
        "MIT",
        "Apache-2.0",
        "BSD-3-Clause",
        "GPL-3.0-or-later",
        "AGPL-3.0-or-later",
        "Proprietary",
    },
)


def _django_major_minor(version: str) -> tuple[int, int]:
    parts = version.split(".")
    return int(parts[0]), int(parts[1])


def _python_tuple(version: str) -> tuple[int, int]:
    parts = version.split(".")
    return int(parts[0]), int(parts[1])


COMPATIBILITY: dict[tuple[int, int], tuple[tuple[int, int], tuple[int, int] | None]] = {
    (4, 2): ((3, 8), (3, 12)),
    (5, 0): ((3, 10), (3, 12)),
    (5, 1): ((3, 10), (3, 13)),
    (5, 2): ((3, 10), (3, 13)),
}


def validate_django_python(dj_ver: str, py_ver: str) -> None:
    dj = _django_major_minor(dj_ver)
    py = _python_tuple(py_ver)
    bounds = COMPATIBILITY.get(dj)
    if not bounds:
        raise ValueError(f"Unsupported Django version: {dj_ver}")
    low, high = bounds
    if py < low:
        raise ValueError(
            f"Django {dj_ver} requires Python >= {low[0]}.{low[1]}, got {py_ver}"
        )
    if high is not None and py > high:
        raise ValueError(
            f"Django {dj_ver} supports Python up to {high[0]}.{high[1]}, got {py_ver}"
        )


def validate_use_tox(value: str) -> None:
    if value not in ALLOWED_TOX:
        raise ValueError(f"use_tox must be one of {sorted(ALLOWED_TOX)}, got {value!r}")


def validate_use_i18n(value: str) -> None:
    if value not in ALLOWED_USE_I18N:
        raise ValueError(f"use_i18n must be one of {sorted(ALLOWED_USE_I18N)}, got {value!r}")


def validate_openapi_schema(schema: str) -> None:
    if schema not in ALLOWED_OPENAPI_SCHEMA:
        raise ValueError(
            "openapi_schema must be one of "
            f"{sorted(ALLOWED_OPENAPI_SCHEMA)}, got {schema!r}"
        )


def validate_api_openapi(api: str, schema: str) -> None:
    if api != "y" and schema != "none":
        raise ValueError(
            "openapi_schema must be 'none' when api_project is 'n' "
            "(drf-spectacular and drf-yasg require Django REST Framework)."
        )


def validate_license(license_id: str) -> None:
    if license_id not in ALLOWED_LICENSES:
        raise ValueError(
            f"license must be one of {sorted(ALLOWED_LICENSES)}, got {license_id!r}"
        )


def validate_documentation_provider(provider: str) -> None:
    if provider not in ALLOWED_DOCS_PROVIDERS:
        raise ValueError(
            f"documentation_provider must be one of {sorted(ALLOWED_DOCS_PROVIDERS)}, got {provider!r}"
        )


def validate_celery_broker(broker: str) -> None:
    if broker not in ALLOWED_CELERY_BROKERS:
        raise ValueError(
            f"celery_broker must be one of {sorted(ALLOWED_CELERY_BROKERS)}, got {broker!r}"
        )


def validate_postgres_version(version: str) -> None:
    if version not in ALLOWED_POSTGRES_VERSIONS:
        raise ValueError(
            f"postgres_version must be one of {sorted(ALLOWED_POSTGRES_VERSIONS)}, got {version!r}"
        )


def validate_frontend_stack() -> None:
    """Ensure frontend_stack is a supported framework + version combination."""
    if frontend_stack not in ALLOWED_FRONTEND_STACK:
        raise ValueError(
            "frontend_stack must be one of "
            f"{sorted(ALLOWED_FRONTEND_STACK)}, got {frontend_stack!r}"
        )


def validate_project_slug(slug: str) -> None:
    if not re.match(r"^[a-z][a-z0-9_]*$", slug):
        raise ValueError(
            "project_slug must start with a letter and contain only lowercase letters, digits, and underscores."
        )


def main() -> None:
    validate_project_slug(project_slug)
    validate_django_python(django_version, python_version)
    validate_postgres_version(postgres_version)
    validate_celery_broker(celery_broker)
    validate_documentation_provider(documentation_provider)
    validate_license(license_choice)
    validate_use_tox(use_tox)
    validate_use_i18n(use_i18n)
    validate_openapi_schema(openapi_schema)
    validate_api_openapi(api_project, openapi_schema)
    validate_frontend_stack()


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
