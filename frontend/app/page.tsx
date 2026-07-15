"use client";

import Link from "next/link";
import { useState, useEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchHealth, fetchInvestigationHistory, fetchClusters, InvestigationResult } from "../services/api";
import { InvestigationProgress } from "../components/InvestigationProgress";
import { DiagnosisCard } from "../components/DiagnosisCard";
import { InvestigationHistory } from "../components/InvestigationHistory";

interface InvestigationStep {
  name: string;
  completed: boolean;
}

const INITIAL_STEPS: InvestigationStep[] = [
  { name: "Checking Pods", completed: false },
  { name: "Reading Logs", completed: false },
  { name: "Analyzing Events", completed: false },
  { name: "Inspecting Deployments", completed: false },
  { name: "Checking Networking", completed: false },
  { name: "AI Reasoning", completed: false },
  { name: "Root Cause Found", completed: false },
];

export default function HomePage() {
  const { data: healthData } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
  });

  const { data: historyData } = useQuery({
    queryKey: ["investigations"],
    queryFn: fetchInvestigationHistory,
  });

  const { data: clustersData } = useQuery({ queryKey: ["clusters"], queryFn: fetchClusters });

  const [steps, setSteps] = useState<InvestigationStep[]>(INITIAL_STEPS);
  const [historyItems, setHistoryItems] = useState<any[]>([]);

  useEffect(() => {
    if (historyData?.investigations) {
      setHistoryItems(
        historyData.investigations.map((inv: any) => ({
          timestamp: new Date(inv.timestamp).toLocaleString(),
          root_cause: inv.root_cause,
          namespace: inv.namespace,
          confidence: inv.confidence,
          status: inv.status,
        }))
      );
    }
  }, [historyData]);

  useEffect(() => {
    if (clustersData?.current && !selectedContext) {
      setSelectedContext(clustersData.current);
    }
  }, [clustersData]);

  const [selectedContext, setSelectedContext] = useState<string | null>(null);
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [diagnosis, setDiagnosis] = useState<any | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const isPending = isInvestigating;
  const activeContext = clustersData?.current ?? "Default Context";

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <section className="rounded-[2rem] border border-slate-800 bg-slate-950/90 p-8 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-3xl">
              <span className="inline-flex rounded-full bg-cyan-500/10 px-4 py-1 text-sm font-semibold text-cyan-300 ring-1 ring-cyan-500/20">
                Kubernetes troubleshooting made faster
              </span>
              <h1 className="mt-6 text-4xl font-bold tracking-tight text-white sm:text-5xl">
                AI-powered cluster diagnosis with a polished dashboard.
              </h1>
              <p className="mt-5 max-w-2xl text-slate-400 sm:text-lg">
                Run live investigations, watch step-by-step progress, and get actionable fixes for your Kubernetes cluster.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:w-auto lg:grid-cols-1">
              <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-4 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
                <p className="font-semibold text-slate-100">Current context</p>
                <p className="mt-2 text-base text-cyan-300">{activeContext}</p>
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-4 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
                <p className="font-semibold text-slate-100">Investigation history</p>
                <p className="mt-2 text-base text-cyan-300">{historyItems.length} recent review{historyItems.length === 1 ? "" : "s"}</p>
              </div>
            </div>
          </div>

          <div className="mt-10 rounded-[2rem] border border-slate-800 bg-slate-950/95 p-6 shadow-2xl shadow-slate-950/10">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div className="space-y-1">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Start a cluster investigation</p>
                <h2 className="text-2xl font-semibold text-white">Choose your cluster and begin analysis.</h2>
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <label className="block text-sm font-medium text-slate-200">
                  Select context
                  <select
                    className="mt-2 block w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-400"
                    value={selectedContext ?? ""}
                    onChange={(e) => setSelectedContext(e.target.value || null)}
                  >
                    <option value="">Default Context</option>
                    {clustersData?.contexts?.map((c: string) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </label>

                <button
                  className="rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-60"
                  onClick={() => startInvestigation(selectedContext)}
                  disabled={isPending}
                >
                  {isPending ? "Investigating..." : "Investigate Cluster"}
                </button>
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <div className="rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-5 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
                <p className="font-semibold text-slate-100">System Status</p>
                <p className="mt-2 text-base text-cyan-300">{healthData?.status ?? "Loading..."}</p>
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-900/90 px-4 py-5 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
                <p className="font-semibold text-slate-100">Sign In</p>
                <p className="mt-2 text-base text-slate-300">Visit the login page to access saved investigations.</p>
                <Link
                  href="/sign-in"
                  className="mt-4 inline-flex items-center justify-center rounded-2xl bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
                >
                  Go to Sign In
                </Link>
              </div>
            </div>
          </div>
        </section>

        <div className="grid gap-8 xl:grid-cols-[1.05fr_0.95fr]">
          <div className="space-y-8">
            <InvestigationProgress steps={steps} isInvestigating={isPending} />
            <InvestigationHistory investigations={historyItems} />
          </div>

          <div className="space-y-6">
            {diagnosis ? (
              (diagnosis.root_cause && typeof diagnosis.root_cause === "string" && (diagnosis.root_cause.includes("Unable to determine") || (diagnosis.confidence !== undefined && diagnosis.confidence < 10))) ? (
                <div className="rounded-[2rem] border border-emerald-700/30 bg-emerald-950/90 p-6 shadow-2xl shadow-emerald-500/10">
                  <h2 className="text-lg font-semibold text-white">No critical Kubernetes issues detected</h2>
                  <p className="mt-3 text-slate-300">Cluster appears healthy. Review logs and events for non-critical warnings.</p>
                </div>
              ) : (
                <DiagnosisCard diagnosis={diagnosis} />
              )
            ) : null}
            {errorMsg ? (
              <div className="rounded-[2rem] border border-rose-700/30 bg-rose-950/95 p-6 shadow-2xl shadow-rose-500/10">
                <h2 className="text-lg font-semibold text-white">Investigation Failed</h2>
                <p className="mt-3 text-slate-300">{errorMsg}</p>
              </div>
            ) : !isPending && !diagnosis ? (
              <div className="rounded-[2rem] border border-slate-800 bg-slate-900/90 p-6 shadow-2xl shadow-slate-950/10">
                <h2 className="text-lg font-semibold text-white">Ready when you are</h2>
                <p className="mt-3 text-slate-400">
                  Click Investigate to begin a step-by-step diagnosis of your Kubernetes cluster.
                </p>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </main>
  );

  function startInvestigation(context: string | null) {
    setSteps(INITIAL_STEPS);
    setDiagnosis(null);
    setIsInvestigating(true);

    const url = new URL((process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000") + "/investigate/stream");
    if (context) url.searchParams.append("context", context);

    const es = new EventSource(url.toString());
    eventSourceRef.current = es;

    es.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        const type = data.type;
        const payload = data.payload;

        if (type === "step") {
          // show current step (no change to completed state)
        } else if (type === "step_result") {
          const stepName: string = payload.step;
          setSteps((prev) => {
            return prev.map((s) => (s.name === stepName ? { ...s, completed: true } : s));
          });
        } else if (type === "result") {
          // investigation result arrives (raw evidence)
          // mark all analysis steps as complete (AI reasoning pending)
          setSteps((prev) => prev.map((s) => ({ ...s, completed: true })));
        } else if (type === "diagnosis") {
          setDiagnosis(payload);
          setHistoryItems((prev) => [
            {
              timestamp: new Date().toLocaleString(),
              root_cause: payload.root_cause || payload.payload?.root_cause || "Unknown",
              namespace: "default",
              confidence: payload.confidence || payload.payload?.confidence || 0,
              status: payload.success === false ? "failed" : "success",
            },
            ...prev,
          ]);
          setIsInvestigating(false);
          es.close();
        }
      } catch (err) {
        console.error("Failed to parse SSE data", err);
      }
    };

    es.onerror = (err) => {
      console.error("SSE error", err);
      setErrorMsg("Realtime connection lost. Investigation may be incomplete.");
      setIsInvestigating(false);
      es.close();
    };
  }
}
