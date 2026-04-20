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
vue_major_version = "{{ cookiecutter.vue_major_version }}"
vite_major_version = "{{ cookiecutter.vite_major_version }}"
react_major_version = "{{ cookiecutter.react_major_version }}"
nuxt_major_version = "{{ cookiecutter.nuxt_major_version }}"
next_major_version = "{{ cookiecutter.next_major_version }}"
htmx_major_version = "{{ cookiecutter.htmx_major_version }}"

ALLOWED_POSTGRES_VERSIONS = frozenset({"15", "16", "17", "18"})
ALLOWED_CELERY_BROKERS = frozenset({"redis", "rabbitmq"})
ALLOWED_DOCS_PROVIDERS = frozenset(
    {"none", "gitbook", "readthedocs", "mkdocs", "notion"},
)
ALLOWED_TOX = frozenset({"n", "y"})
ALLOWED_USE_I18N = frozenset({"n", "y"})
ALLOWED_OPENAPI_SCHEMA = frozenset({"none", "drf-spectacular", "drf-yasg"})

ALLOWED_VUE_MAJOR = frozenset({"3"})
ALLOWED_VITE_MAJOR = frozenset({"5", "6"})
ALLOWED_REACT_MAJOR = frozenset({"18", "19"})
ALLOWED_NUXT_MAJOR = frozenset({"3", "4"})
ALLOWED_NEXT_MAJOR = frozenset({"14", "15"})
ALLOWED_HTMX_MAJOR = frozenset({"1", "2"})

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


def validate_frontend_majors() -> None:
    """Ensure framework major-version choices are allowed and match frontend_framework."""
    if vue_major_version not in ALLOWED_VUE_MAJOR:
        raise ValueError(
            f"vue_major_version must be one of {sorted(ALLOWED_VUE_MAJOR)}, "
            f"got {vue_major_version!r}"
        )
    if vite_major_version not in ALLOWED_VITE_MAJOR:
        raise ValueError(
            f"vite_major_version must be one of {sorted(ALLOWED_VITE_MAJOR)}, "
            f"got {vite_major_version!r}"
        )
    if react_major_version not in ALLOWED_REACT_MAJOR:
        raise ValueError(
            f"react_major_version must be one of {sorted(ALLOWED_REACT_MAJOR)}, "
            f"got {react_major_version!r}"
        )
    if nuxt_major_version not in ALLOWED_NUXT_MAJOR:
        raise ValueError(
            f"nuxt_major_version must be one of {sorted(ALLOWED_NUXT_MAJOR)}, "
            f"got {nuxt_major_version!r}"
        )
    if next_major_version not in ALLOWED_NEXT_MAJOR:
        raise ValueError(
            f"next_major_version must be one of {sorted(ALLOWED_NEXT_MAJOR)}, "
            f"got {next_major_version!r}"
        )
    if htmx_major_version not in ALLOWED_HTMX_MAJOR:
        raise ValueError(
            f"htmx_major_version must be one of {sorted(ALLOWED_HTMX_MAJOR)}, "
            f"got {htmx_major_version!r}"
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
    validate_frontend_majors()


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
