// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  ssr: false,
  devServer: {
    host: "0.0.0.0",
    port: 3000,
  },
  vite: {
    server: {
      strictPort: true,
    },
  },
  runtimeConfig: {
    public: {
      djangoOrigin: "http://127.0.0.1:8000",
    },
  },
});
