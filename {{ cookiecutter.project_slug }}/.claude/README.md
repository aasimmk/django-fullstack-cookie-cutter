# Claude Code Workspace Notes

This directory is for Claude Code-specific project helpers.

## Recommended usage
- Keep shared project context in `AGENTS.md` at repository root.
- Store Claude-specific prompt snippets and command recipes in `.claude/commands/`.
- Put project-owned skills in `.claude/skills/<name>/SKILL.md` and commit them.
- Keep secrets out of this directory.

## Global skills
Claude Code loads `~/.claude/skills` (and your installed plugins) in every project on
your own machine. To make those skills travel with this repo (containers, cloud
sessions, other machines), copy them into `.claude/skills/`:

```bash
python .claude/scripts/sync_global_skills.py --dry-run   # preview
python .claude/scripts/sync_global_skills.py             # sync everything
python .claude/scripts/sync_global_skills.py --only engineering- --only design-
python .claude/scripts/sync_global_skills.py --no-plugins  # ~/.claude/skills only
python .claude/scripts/sync_global_skills.py --clean       # remove synced skills
```

- Plugin skills are written as `<plugin>-<skill>` (e.g. `engineering-code-review`) so
  names cannot collide; user skills keep their directory name.
- Synced skills are git-ignored via a generated `.claude/skills/.gitignore`; re-run to
  refresh, and skills you removed globally are pruned.
- Skills you author in `.claude/skills/` are never overwritten, pruned or ignored. A
  global skill with the same name as one of yours is skipped.
- Honors `CLAUDE_CONFIG_DIR` if your Claude config lives somewhere other than `~/.claude`.

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
