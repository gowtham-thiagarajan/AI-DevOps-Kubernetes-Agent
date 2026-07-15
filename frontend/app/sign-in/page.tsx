"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Login failed");
      }

      await response.json();
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-6 py-16">
        <div className="grid w-full gap-10 rounded-[2rem] border border-slate-800 bg-slate-950/95 p-8 shadow-2xl shadow-slate-950/20 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-6">
            <div className="inline-flex rounded-full bg-cyan-500/10 px-4 py-2 text-sm font-semibold text-cyan-300 ring-1 ring-cyan-500/20">
              Demo login page
            </div>
            <div>
              <h1 className="text-4xl font-bold text-white">Sign in to your workspace</h1>
              <p className="mt-4 text-slate-400 sm:text-lg">
                Use any email and password for the MVP. Authentication is mocked for the demo experience.
              </p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-5 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
              <p className="font-semibold text-slate-100">Need access?</p>
              <p className="mt-3 leading-6">
                This page is a placeholder for InsForge authentication. Press Sign In to continue to the dashboard.
              </p>
            </div>
          </div>

          <div className="rounded-[1.75rem] bg-slate-950/90 p-8 shadow-2xl shadow-slate-950/20">
            <form className="space-y-6" onSubmit={handleSubmit}>
              <label className="block text-sm font-medium text-slate-300">
                Email
                <input
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  type="email"
                  required
                  className="mt-3 w-full rounded-3xl border border-slate-800 bg-slate-900 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
                />
              </label>

              <label className="block text-sm font-medium text-slate-300">
                Password
                <input
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  type="password"
                  required
                  className="mt-3 w-full rounded-3xl border border-slate-800 bg-slate-900 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400"
                />
              </label>

              {error ? (
                <p className="rounded-3xl border border-rose-700 bg-rose-950/70 px-4 py-3 text-sm text-rose-200">
                  {error}
                </p>
              ) : null}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full rounded-3xl bg-gradient-to-r from-cyan-500 to-blue-500 px-4 py-3 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:brightness-105 disabled:opacity-60"
              >
                {isLoading ? "Signing in..." : "Sign In"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
}
