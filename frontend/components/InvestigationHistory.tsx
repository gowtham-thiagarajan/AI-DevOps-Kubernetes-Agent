"use client";

interface Investigation {
  timestamp: string;
  root_cause: string;
  namespace: string;
  confidence: number;
  status: "success" | "failed";
}

interface HistoryProps {
  investigations: Investigation[];
}

export function InvestigationHistory({ investigations }: HistoryProps) {
  if (investigations.length === 0) {
    return (
      <div className="rounded-[2rem] border border-slate-800 bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/10">
        <h2 className="text-lg font-semibold text-white">Previous Investigations</h2>
        <p className="mt-4 text-slate-400">No investigations yet. Run your first diagnosis to build history.</p>
      </div>
    );
  }

  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/10">
      <h2 className="text-lg font-semibold text-white">Previous Investigations</h2>

      <div className="mt-6 space-y-4">
        {investigations.map((inv, idx) => (
          <div key={idx} className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-sm shadow-slate-950/10">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="font-semibold text-slate-100">{inv.root_cause}</p>
                <p className="mt-2 text-sm text-slate-500">{inv.timestamp} • {inv.namespace}</p>
              </div>
              <div className="flex flex-col items-start gap-2 text-right sm:items-end">
                <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold text-slate-400">
                  {inv.status === "success" ? "Success" : "Failed"}
                </span>
                <span className={`rounded-full px-3 py-1 text-xs font-semibold ${inv.status === "success" ? "bg-cyan-500/15 text-cyan-300" : "bg-rose-500/15 text-rose-300"}`}>
                  {inv.confidence}% confidence
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
