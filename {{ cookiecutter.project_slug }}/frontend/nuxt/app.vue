<template>
  <div class="min-h-screen bg-slate-50 p-8 text-slate-900">
    <h1 class="text-3xl font-bold tracking-tight">{{ cookiecutter.project_name }}</h1>
    <p class="mt-2 max-w-xl text-slate-600">{{ cookiecutter.description }}</p>
    <p class="mt-6 text-sm font-medium text-slate-700">Nuxt 3 · SPA mode · Vitest · Playwright</p>
    <p class="mt-2 max-w-xl text-sm text-slate-500">
      Django runs on port 8000; call your API from composables or
      <code class="rounded bg-white px-1 py-0.5 font-mono text-xs shadow">useFetch</code>
      toward the origin in
      <code class="rounded bg-white px-1 py-0.5 font-mono text-xs shadow">runtimeConfig.public.djangoOrigin</code>
      (see <code class="font-mono">nuxt.config.ts</code>).
    </p>
  </div>
</template>
