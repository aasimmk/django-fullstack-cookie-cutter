# Claude Code Workspace Notes

This directory is for Claude Code-specific project helpers.

## Recommended usage
- Keep shared project context in `AGENTS.md` at repository root.
- Store Claude-specific prompt snippets and command recipes in `.claude/commands/`.
- Keep secrets out of this directory.

## Current project profile
- Backend: Django in `backend/src`
{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
- Frontend: `frontend/{{ cookiecutter['__frontend_framework'] }}` (Vite + django-vite)
{% elif cookiecutter['__frontend_framework'] == "nuxt" %}
- Frontend: `frontend/nuxt` (Nuxt 3, port 3000)
{% elif cookiecutter['__frontend_framework'] == "next" %}
- Frontend: `frontend/next` (Next.js App Router, port 3000)
{% elif cookiecutter['__frontend_framework'] == "htmx" %}
- Frontend style: HTMX + server-rendered templates
{% else %}
- Frontend style: server-rendered templates
{% endif %}
{% if cookiecutter.api_project == "y" %}
- API-first mode: enabled (DRF + CORS)
{% endif %}
