"use client";

interface InvestigationStep {
  name: string;
  completed: boolean;
}

interface InvestigationProgressProps {
  steps: InvestigationStep[];
  isInvestigating: boolean;
}

export function InvestigationProgress({
  steps,
  isInvestigating,
}: InvestigationProgressProps) {
  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/10">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-white">Investigation Status</h2>
          <p className="mt-1 text-sm text-slate-400">Live progress updates as the cluster is examined.</p>
        </div>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
          {isInvestigating ? "Running" : "Idle"}
        </span>
      </div>

      <div className="mt-6 space-y-3">
        {steps.map((step, idx) => (
          <div key={idx} className="flex items-center gap-3 rounded-3xl border border-slate-800 bg-slate-950/80 px-4 py-3">
            <div
              className={`h-5 w-5 rounded-full flex items-center justify-center border-2 ${
                step.completed
                  ? "border-cyan-400 bg-cyan-400"
                  : isInvestigating
                    ? "border-slate-600 bg-slate-800"
                    : "border-slate-700 bg-slate-950"
              }`}
            >
              {step.completed && <span className="text-[0.55rem] font-bold text-slate-950">✓</span>}
            </div>
            <span className={`text-sm ${step.completed ? "text-cyan-300" : "text-slate-400"}`}>
              {step.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
