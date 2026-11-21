# Claude Code (cookiecutter development)

This `.claude/` folder is for working on the cookiecutter itself. It is **not** part of
generated projects (only `{{ cookiecutter.project_slug }}/` is rendered).

## Global skills

Copy your global Claude Code skills (`~/.claude/skills` plus user-scoped plugin skills)
into this repo's `.claude/skills/`:

```bash
python .claude/scripts/sync_global_skills.py --dry-run   # preview
python .claude/scripts/sync_global_skills.py             # sync everything
python .claude/scripts/sync_global_skills.py --only engineering- --only design-
python .claude/scripts/sync_global_skills.py --no-plugins  # ~/.claude/skills only
python .claude/scripts/sync_global_skills.py --clean       # remove synced skills
```

- Plugin skills are written as `<plugin>-<skill>` (e.g. `engineering-code-review`).
- Synced skills are git-ignored via a generated `.claude/skills/.gitignore`; re-run to
  refresh. Skills removed globally are pruned.
- Skills you write yourself in `.claude/skills/` are never overwritten or ignored.
- Honors `CLAUDE_CONFIG_DIR` if your config is not in `~/.claude`.
