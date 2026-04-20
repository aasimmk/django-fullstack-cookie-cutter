# Frontend tests (Vue)

| Directory | Runner | Typical scope |
|-----------|--------|----------------|
| `unit/` | Vitest + jsdom | Single components / composables |
| `integration/` | Vitest | Several pieces together, mocked network |
| `e2e/` | Playwright | Real browser against Django (`playwright.config.ts` `baseURL`; excluded from `npm run test` / Vitest) |
