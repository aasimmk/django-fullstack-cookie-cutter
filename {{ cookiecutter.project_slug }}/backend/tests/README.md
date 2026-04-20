# Backend tests

| Directory | Role | Pytest marker |
|-----------|------|---------------|
| `unit/` | Fast tests without Django DB (pure logic, helpers). | `@pytest.mark.unit` |
| `integration/` | Django + database + `client` HTTP checks. | `@pytest.mark.integration` |
| `e2e/` | Full HTTP stack via `live_server` (or swap in browser drivers). | `@pytest.mark.e2e` |

Examples:

```bash
cd backend
uv run pytest                           # everything
uv run pytest -m unit                   # unit only
uv run pytest -m "not e2e"              # skip e2e (faster)
```
