export default function HomePage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-16">
      <h1 className="text-3xl font-bold tracking-tight">{{ cookiecutter.project_name }}</h1>
      <p className="mt-2 max-w-xl text-slate-600">{{ cookiecutter.description }}</p>
      <p className="mt-6 text-sm font-medium text-slate-700">Next.js 15 · App Router · Vitest · Playwright</p>
      <p className="mt-2 max-w-xl text-sm text-slate-500">
        Django runs on port 8000. Use <code className="rounded bg-white px-1 py-0.5 font-mono text-xs shadow">fetch</code>{" "}
        or <code className="rounded bg-white px-1 py-0.5 font-mono text-xs shadow">server actions</code> toward your API;
        enable <strong>api_project</strong> in the template (or add CORS) for browser calls from this origin.
      </p>
    </main>
  );
}
