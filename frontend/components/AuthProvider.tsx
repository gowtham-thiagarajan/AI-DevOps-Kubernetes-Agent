"use client";

import { ReactNode } from "react";
import { useAuth } from "@/hooks/useAuth";

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <div className="text-slate-400">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
        <div className="max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-10">
          <h1 className="text-2xl font-bold text-white">AI Kubernetes Agent</h1>
          <p className="mt-2 text-slate-400">Sign in with your account</p>
          <div className="mt-8 space-y-4">
            <input
              type="email"
              placeholder="Email"
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white placeholder-slate-500"
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white placeholder-slate-500"
            />
            <button className="w-full rounded-lg bg-cyan-500 py-2 font-semibold text-slate-950 transition hover:bg-cyan-400">
              Sign In
            </button>
          </div>
          <p className="mt-6 text-center text-sm text-slate-500">
            Authentication via InsForge
          </p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
