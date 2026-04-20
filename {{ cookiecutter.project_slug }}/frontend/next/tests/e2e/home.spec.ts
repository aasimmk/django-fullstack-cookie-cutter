import { expect, test } from "@playwright/test";

test("home loads Next shell", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByText("Next.js 15 · App Router · Vitest · Playwright"),
  ).toBeVisible();
});
