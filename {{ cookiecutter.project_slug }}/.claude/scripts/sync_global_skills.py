#!/usr/bin/env python3
"""Copy your global Claude Code skills into this project's ``.claude/skills/``.

Claude Code already loads ``~/.claude/skills`` in every project on *your* machine.
Run this when you want those skills to travel with the repo: other machines,
containers, cloud sessions, or teammates who sync from a shared home directory.

Sources (in order; the first skill with a given name wins):

1. User skills:   ``$CLAUDE_CONFIG_DIR/skills/**/SKILL.md`` (default ``~/.claude``)
2. Plugin skills: user-scoped plugins from ``plugins/installed_plugins.json``,
   plus synced plugins under ``plugins/synced/`` (cloud sessions).
   Plugin skills are written as ``<plugin>-<skill>`` so names cannot collide
   (``marketing-competitive-brief`` vs ``product-management-competitive-brief``).

Synced skills are git-ignored through a generated ``.claude/skills/.gitignore``,
so the repo history stays clean. Skills you author in ``.claude/skills/`` yourself
are never overwritten, pruned or ignored.

Usage::

    python .claude/scripts/sync_global_skills.py            # sync
    python .claude/scripts/sync_global_skills.py --dry-run  # preview
    python .claude/scripts/sync_global_skills.py --no-plugins
    python .claude/scripts/sync_global_skills.py --only engineering- --only design-
    python .claude/scripts/sync_global_skills.py --clean    # remove synced skills

Stdlib only; Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

MANIFEST = ".global-skills.json"
GITIGNORE = ".gitignore"
SKILL_FILE = "SKILL.md"
IGNORED_NAMES = {".git", "__pycache__", ".DS_Store", "node_modules"}
NAME_RE = re.compile(r"^name:\s*.*$", re.MULTILINE)


@dataclass(frozen=True)
class Skill:
    name: str  # directory name in the project (== invocation name)
    source: Path  # directory holding SKILL.md
    origin: str  # "user" or "plugin:<name>"
    rename: bool  # rewrite the frontmatter `name:` to match `name`


def claude_home() -> Path:
    return Path(
        os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude"
    ).expanduser()


def project_root() -> Path:
    # .claude/scripts/<this file> -> project root
    return Path(__file__).resolve().parents[2]


def find_skill_dirs(root: Path) -> list[Path]:
    """Dirs under ``root`` holding a SKILL.md (not nested in another skill)."""
    if not root.is_dir():
        return []
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_NAMES)
        if SKILL_FILE in filenames:
            found.append(Path(dirpath))
            dirnames[:] = []  # don't descend into a skill's own files
    return found


def plugin_name(plugin_dir: Path) -> str:
    meta = plugin_dir / ".claude-plugin" / "plugin.json"
    try:
        return json.loads(meta.read_text(encoding="utf-8"))["name"]
    except (OSError, ValueError, KeyError, TypeError):
        return plugin_dir.name


def disabled_plugins(home: Path) -> set[str]:
    """Plugin keys (``name@marketplace``) explicitly disabled in user settings."""
    try:
        settings = json.loads((home / "settings.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    enabled = settings.get("enabledPlugins") or {}
    return (
        {key for key, on in enabled.items() if on is False}
        if isinstance(enabled, dict)
        else set()
    )


def installed_plugin_dirs(home: Path) -> list[Path]:
    """User-scoped plugin paths from installed_plugins.json (v1 and v2)."""
    try:
        data = json.loads(
            (home / "plugins" / "installed_plugins.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return []
    off = disabled_plugins(home)
    dirs: list[Path] = []
    for key, entries in (data.get("plugins") or {}).items():
        if key in off:
            continue
        for entry in entries if isinstance(entries, list) else [entries]:
            if not isinstance(entry, dict) or entry.get("scope", "user") != "user":
                continue
            path = entry.get("installPath")
            if path and Path(path).is_dir():
                dirs.append(Path(path))
    return dirs


def synced_plugin_dirs(home: Path) -> list[Path]:
    """Plugins synced into cloud sessions: plugins/synced/<bucket>/<plugin>/skills."""
    base = home / "plugins" / "synced"
    if not base.is_dir():
        return []
    return sorted(p.parent for p in base.glob("*/*/skills") if p.is_dir())


def discover(home: Path, include_plugins: bool) -> list[Skill]:
    skills: list[Skill] = []
    for d in find_skill_dirs(home / "skills"):
        skills.append(Skill(d.name, d, "user", rename=False))

    if include_plugins:
        seen: set[Path] = set()
        for pdir in installed_plugin_dirs(home) + synced_plugin_dirs(home):
            if pdir.resolve() in seen:
                continue
            seen.add(pdir.resolve())
            pname = plugin_name(pdir)
            for d in find_skill_dirs(pdir / "skills"):
                skills.append(
                    Skill(f"{pname}-{d.name}", d, f"plugin:{pname}", rename=True)
                )

    unique: dict[str, Skill] = {}
    for s in skills:
        unique.setdefault(s.name, s)
    return sorted(unique.values(), key=lambda s: s.name)


def load_manifest(dest: Path) -> dict:
    try:
        return json.loads((dest / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"skills": {}}


def write_state(dest: Path, synced: dict[str, str]) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / MANIFEST).write_text(
        json.dumps({"skills": dict(sorted(synced.items()))}, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Generated by .claude/scripts/sync_global_skills.py -- do not edit.",
        "# Skills synced from ~/.claude are ignored; skills you add here are not.",
        f"/{GITIGNORE}",
        f"/{MANIFEST}",
        *(f"/{name}/" for name in sorted(synced)),
    ]
    (dest / GITIGNORE).write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_skill(skill: Skill, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        skill.source,
        target,
        symlinks=False,
        ignore=shutil.ignore_patterns(*IGNORED_NAMES, "*.pyc"),
    )
    if skill.rename:
        md = target / SKILL_FILE
        text = md.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                head, body = text[:end], text[end:]
                if NAME_RE.search(head):
                    head = NAME_RE.sub(f"name: {skill.name}", head, count=1)
                else:
                    head = head.replace("---", f"---\nname: {skill.name}", 1)
                md.write_text(head + body, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--dest", type=Path, default=project_root() / ".claude" / "skills"
    )
    parser.add_argument(
        "--no-plugins",
        action="store_true",
        help="only user skills from ~/.claude/skills",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="PREFIX",
        help="sync only names starting with PREFIX (repeatable); prunes the rest",
    )
    parser.add_argument("--dry-run", action="store_true", help="show what would change")
    parser.add_argument(
        "--clean", action="store_true", help="remove every previously synced skill"
    )
    args = parser.parse_args(argv)

    home, dest = claude_home(), args.dest.resolve()
    previous: dict[str, str] = load_manifest(dest).get("skills", {})

    skills = [] if args.clean else discover(home, include_plugins=not args.no_plugins)
    if args.only:
        skills = [s for s in skills if s.name.startswith(tuple(args.only))]

    synced: dict[str, str] = {}
    added = updated = skipped = 0
    for skill in skills:
        target = dest / skill.name
        if target.exists() and skill.name not in previous:
            print(f"  skip   {skill.name}  (project-owned skill with the same name)")
            skipped += 1
            continue
        verb = "update" if target.exists() else "add"
        print(f"  {verb:<6} {skill.name}  <- {skill.origin}")
        if not args.dry_run:
            copy_skill(skill, target)
        synced[skill.name] = skill.origin
        added += verb == "add"
        updated += verb == "update"

    removed = 0
    for name in sorted(set(previous) - set(synced)):
        target = dest / name
        if target.exists():
            print(f"  remove {name}  (no longer global or not selected)")
            if not args.dry_run:
                shutil.rmtree(target)
            removed += 1

    if not args.dry_run:
        if synced:
            write_state(dest, synced)
        else:
            for f in (MANIFEST, GITIGNORE):
                (dest / f).unlink(missing_ok=True)

    prefix = "[dry-run] " if args.dry_run else ""
    print(
        f"{prefix}{added} added, {updated} updated, {removed} removed, "
        f"{skipped} skipped -> {dest} (source: {home})"
    )
    if not skills and not args.clean:
        print(f"No global skills found under {home}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
