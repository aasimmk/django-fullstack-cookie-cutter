# Documentation tooling

This folder exists when you selected a **documentation provider** in Cookiecutter. Unused provider files are removed by `hooks/post_gen_project.py`.

| Provider | What was kept |
|----------|----------------|
| **gitbook** | [`GITBOOK.md`](GITBOOK.md) — connect GitBook to Git |
| **readthedocs** | MkDocs sources here + [`.readthedocs.yaml`](../.readthedocs.yaml) at repo root |
| **mkdocs** | MkDocs sources + [GitHub Actions workflow](../.github/workflows/docs.yml) publishing to `gh-pages` |
| **notion** | [`NOTION.md`](NOTION.md) — using Notion alongside this repo |

Build MkDocs locally: `pip install -r docs/requirements.txt && mkdocs serve` from the repository root.
