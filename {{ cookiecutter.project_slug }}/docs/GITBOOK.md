# GitBook documentation

[GitBook](https://www.gitbook.com/) is a hosted documentation platform with Git sync, versioning, and collaboration.

## Connect this repository

1. Create a space at [gitbook.com](https://www.gitbook.com/).
2. Under **Integrations** (or **Space settings → Git Sync**), connect your **GitHub / GitLab** account and select this repository and branch (usually `main`).
3. Choose a **content root** (for example `/docs` or `/`) depending on where you want GitBook to read Markdown from.
4. Publish your space. GitBook will pull Markdown on each sync; resolve conflicts in the GitBook UI or via normal Git workflows.

## Tips

- Keep long-form user guides in GitBook; keep developer setup in this repo’s **`README.md`** / **`backend/`** docs to avoid duplication, or link between them.
- Use GitBook **OpenAPI** blocks if you document REST APIs generated from this template.
