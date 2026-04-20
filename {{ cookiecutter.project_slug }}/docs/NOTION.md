# Notion as documentation

[Notion](https://www.notion.so/) is a common choice for internal wikis, runbooks, and product docs.

## Suggested setup

1. Create a **Notion workspace** (team or personal) and a top-level **page** or **database** for this product (e.g. “{{ cookiecutter.project_name }} — docs”).
2. Add subpages: **Architecture**, **API reference**, **Runbooks**, **On-call**, **Release notes**.
3. Link back to this repository in the Notion sidebar or home page (`https://github.com/YOUR_ORG/{{ cookiecutter.project_slug }}`).
4. Optionally embed **GitHub** issues/PRs or **Figma** using Notion embeds.

## Keeping docs in sync

Notion does not replace Git for code. Treat Notion as the **narrative** layer; keep canonical technical detail (endpoints, env vars, migrations) in-repo (`README.md`, especially **Celery and cache** when Redis or Celery is enabled, plus OpenAPI and ADRs) and link out from Notion.
