import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
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
      input: path.resolve(__dirname, "src/main.tsx"),
    },
  },
});
