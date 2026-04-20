<script setup lang="ts">
import { ref } from "vue";

const title = ref("Vue + Vite + Tailwind");
</script>

<template>
  <div class="text-center">
    <h2 class="text-xl font-semibold text-emerald-700">{{ title }}</h2>
    <p class="mt-2 text-sm text-slate-600">Mounted into <code>#app</code> from Django template.</p>
  </div>
</template>
