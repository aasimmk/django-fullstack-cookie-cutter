import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";
import App from "../../src/App.vue";

describe("App", () => {
  it("renders title", () => {
    const wrapper = mount(App);
    expect(wrapper.text()).toContain("Vue + Vite + Tailwind");
  });
});
