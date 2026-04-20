import { expect, test } from "@playwright/test";

test("home loads Nuxt shell", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Nuxt 3 · SPA mode · Vitest · Playwright")).toBeVisible();
});
