# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## For developers

Application code lives under **`backend/`** (Django project package `src/`). See the repository root **`README.md`** for environment setup, Docker Compose, and deployment notes.

## Building these docs locally

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

Open the URL printed in the terminal (usually `http://127.0.0.1:8000`).
