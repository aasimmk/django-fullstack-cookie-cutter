import path from "node:path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  base: "/static/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
  build: {
    manifest: true,
    outDir: path.resolve(__dirname, "../../backend/static/dist"),
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, "src/main.ts"),
    },
  },
});
