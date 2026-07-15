"use client";

interface DiagnosisData {
  root_cause: string;
  explanation: string;
  fix: string;
  kubectl_command: string;
  prevention: string;
  confidence: number;
}

interface DiagnosisCardProps {
  diagnosis: DiagnosisData;
}

export function DiagnosisCard({ diagnosis }: DiagnosisCardProps) {
  return (
    <div className="rounded-[2rem] border border-slate-800 bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/10">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white">Diagnosis</h2>
          <p className="mt-1 text-sm text-slate-400">Root cause and remediation for your cluster issue.</p>
        </div>
        <span className="rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1 text-sm font-semibold text-cyan-300">
          Confidence {diagnosis.confidence}%
        </span>
      </div>

      <div className="mt-8 grid gap-6">
        <section className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5">
          <h3 className="text-sm font-semibold text-cyan-400">Root Cause</h3>
          <p className="mt-3 text-slate-200">{diagnosis.root_cause}</p>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5">
          <h3 className="text-sm font-semibold text-cyan-400">Explanation</h3>
          <p className="mt-3 text-slate-300">{diagnosis.explanation}</p>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5">
          <h3 className="text-sm font-semibold text-cyan-400">Suggested Fix</h3>
          <p className="mt-3 text-slate-200">{diagnosis.fix}</p>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5">
          <h3 className="text-sm font-semibold text-cyan-400">kubectl Command</h3>
          <pre className="mt-3 overflow-x-auto rounded-2xl bg-slate-950 px-4 py-3 text-xs text-slate-300">
            {diagnosis.kubectl_command}
          </pre>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-950/90 p-5">
          <h3 className="text-sm font-semibold text-cyan-400">Prevention</h3>
          <p className="mt-3 text-slate-300">{diagnosis.prevention}</p>
        </section>
      </div>
    </div>
  );
}
