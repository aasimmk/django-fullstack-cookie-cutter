"""Remove unused template paths and sync dependencies (rendered by Cookiecutter)."""

import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime

FRONTEND = "{{ cookiecutter.frontend_framework }}"
NODE_PM = "{{ cookiecutter.node_package_manager }}"
CLOUD = "{{ cookiecutter.cloud_provider }}"
CELERY = "{{ cookiecutter.use_celery }}"
API = "{{ cookiecutter.api_project }}"
USE_PG = "{{ cookiecutter.use_postgresql }}"
DOCS = "{{ cookiecutter.documentation_provider }}"
TOX = "{{ cookiecutter.use_tox }}"
USE_I18N = "{{ cookiecutter.use_i18n }}"

SPA_FRAMEWORKS = frozenset({"vue", "react", "nuxt", "next"})

LOCKFILES_BY_PM = {
    "npm": "package-lock.json",
    "pnpm": "pnpm-lock.yaml",
    "yarn": "yarn.lock",
}

ROOT = os.getcwd()
BACKEND = os.path.join(ROOT, "backend")
DEPLOY = os.path.join(ROOT, "deploy")
FRONTEND_DIR = os.path.join(ROOT, "frontend")
POSTGRES_DOCKER = os.path.join(ROOT, "docker", "postgres")

_DOCS_README = os.path.join("docs", "README.md")

DOCS_SCAFFOLD_FILES: frozenset[str] = frozenset(
    {
        "mkdocs.yml",
        ".readthedocs.yaml",
        os.path.join("docs", "index.md"),
        os.path.join("docs", "requirements.txt"),
        os.path.join("docs", "GITBOOK.md"),
        os.path.join("docs", "NOTION.md"),
        _DOCS_README,
        os.path.join(".github", "workflows", "docs.yml"),
    },
)

DOCS_KEEP: dict[str, frozenset[str]] = {
    "none": frozenset(),
    "gitbook": frozenset({os.path.join("docs", "GITBOOK.md"), _DOCS_README}),
    "readthedocs": frozenset(
        {
            "mkdocs.yml",
            ".readthedocs.yaml",
            os.path.join("docs", "index.md"),
            os.path.join("docs", "requirements.txt"),
            _DOCS_README,
        },
    ),
    "mkdocs": frozenset(
        {
            "mkdocs.yml",
            os.path.join("docs", "index.md"),
            os.path.join("docs", "requirements.txt"),
            _DOCS_README,
            os.path.join(".github", "workflows", "docs.yml"),
        },
    ),
    "notion": frozenset({os.path.join("docs", "NOTION.md"), _DOCS_README}),
}


def stamp_license_year() -> None:
    """Replace __GENERATION_YEAR__ in LICENSE with the current UTC year."""
    path = os.path.join(ROOT, "LICENSE")
    if not os.path.isfile(path):
        return
    try:
        year = str(datetime.now(UTC).year)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "__GENERATION_YEAR__" not in text:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace("__GENERATION_YEAR__", year))
    except OSError:
        pass


def rmtree(path: str) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def prune_documentation_scaffold() -> None:
    """Keep only files for the selected documentation_provider."""
    keep = DOCS_KEEP.get(DOCS, frozenset())
    for rel in DOCS_SCAFFOLD_FILES:
        if rel in keep:
            continue
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            os.remove(path)
    docs_dir = os.path.join(ROOT, "docs")
    if os.path.isdir(docs_dir) and not os.listdir(docs_dir):
        os.rmdir(docs_dir)


def sync_frontend_lockfile() -> None:
    """Align lockfiles with the selected package manager (SPA frontends only)."""
    if FRONTEND not in SPA_FRAMEWORKS:
        return
    app_dir = os.path.join(FRONTEND_DIR, FRONTEND)
    if not os.path.isdir(app_dir):
        return
    for pm, name in LOCKFILES_BY_PM.items():
        if pm == NODE_PM:
            continue
        path = os.path.join(app_dir, name)
        if os.path.isfile(path):
            os.remove(path)
    refresh_cmd: list[str]
    if NODE_PM == "npm":
        # --ignore-scripts: postinstall (e.g. nuxt prepare) must not run until deps
        # exist; lockfile-only installs do not populate node_modules reliably.
        refresh_cmd = ["npm", "install", "--package-lock-only", "--ignore-scripts"]
    elif NODE_PM == "pnpm":
        refresh_cmd = ["pnpm", "install"]
    elif NODE_PM == "yarn":
        refresh_cmd = ["yarn", "install"]
    else:
        return
    try:
        subprocess.run(
            refresh_cmd,
            cwd=app_dir,
            check=False,
            timeout=600,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(
            f"Skipping {NODE_PM} lockfile refresh (tool not found or timed out). "
            f"Run `{' '.join(refresh_cmd)}` in {app_dir} so CI can install dependencies.",
        )


def main() -> None:
    stamp_license_year()

    # --- Cloud deploy: keep only selected provider ---
    if CLOUD == "none":
        rmtree(DEPLOY)
    elif os.path.isdir(DEPLOY):
        for name in os.listdir(DEPLOY):
            if name == CLOUD:
                continue
            rmtree(os.path.join(DEPLOY, name))

    # --- Frontend: keep only selected SPA stack ---
    if FRONTEND in SPA_FRAMEWORKS:
        for name in SPA_FRAMEWORKS:
            if name != FRONTEND:
                rmtree(os.path.join(FRONTEND_DIR, name))
    else:
        rmtree(FRONTEND_DIR)
        rmtree(os.path.join(ROOT, "docker", "frontend"))

    sync_frontend_lockfile()

    prune_documentation_scaffold()

    # --- Tox: backend/tox.ini only when enabled ---
    if TOX != "y":
        tox_ini = os.path.join(BACKEND, "tox.ini")
        if os.path.isfile(tox_ini):
            os.remove(tox_ini)

    # --- PostgreSQL: custom image tree only when enabled ---
    if USE_PG != "y":
        rmtree(POSTGRES_DOCKER)
        docker_dir = os.path.join(ROOT, "docker")
        if os.path.isdir(docker_dir) and not os.listdir(docker_dir):
            os.rmdir(docker_dir)

    # --- REST API app ---
    if API != "y":
        rmtree(os.path.join(BACKEND, "src", "apps", "api"))

    # --- Celery: remove tasks app and celery module when disabled ---
    if CELERY != "y":
        rmtree(os.path.join(BACKEND, "src", "apps", "tasks"))
        celery_file = os.path.join(BACKEND, "src", "celery.py")
        if os.path.isfile(celery_file):
            os.remove(celery_file)

    # --- gettext locale tree only when internationalization is enabled ---
    if USE_I18N != "y":
        locale_dir = os.path.join(BACKEND, "locale")
        if os.path.isdir(locale_dir):
            shutil.rmtree(locale_dir, ignore_errors=True)

    # --- uv sync + format rendered Python ---
    try:
        subprocess.run(
            ["uv", "sync"],
            cwd=BACKEND,
            check=False,
            timeout=300,
        )
        subprocess.run(
            ["uv", "run", "ruff", "format", "."],
            cwd=BACKEND,
            check=False,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(
            "Skipping uv sync (uv not found or timed out). Run `uv sync` in the backend/ directory.",
        )


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        print(f"post_gen hook error: {exc}", file=sys.stderr)
        sys.exit(1)
