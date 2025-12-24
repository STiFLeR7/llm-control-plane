"use client";

import { useState } from "react";

type ControlResponse = {
  status: "ALLOW" | "ABSTAIN";
  message: string;
  reason_code: string;
  confidence: number;
  evidence_count: number;
  answer: string | null;
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<ControlResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function submitQuery() {
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Query Input */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-neutral-400">
          Query
        </label>
        <textarea
          className="w-full resize-none rounded bg-neutral-900 border border-neutral-800 px-3 py-3 text-sm text-neutral-100 placeholder:text-neutral-500 focus:outline-none focus:ring-1 focus:ring-neutral-600 focus:border-neutral-600 transition-colors"
          rows={4}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter query for evaluation..."
        />
        <button
          onClick={submitQuery}
          disabled={loading}
          className="inline-flex items-center rounded bg-neutral-800 border border-neutral-700 text-neutral-100 px-4 py-2 text-sm font-medium hover:bg-neutral-700 hover:border-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Evaluating…" : "Submit"}
        </button>
      </div>

      {/* Response Panel */}
      {result && (
        <div className="rounded border border-neutral-800 bg-neutral-900 divide-y divide-neutral-800">
          {/* Status & Metrics */}
          <div className="p-4 space-y-4">
            {/* Decision Trace Label */}
            <div className="flex items-center justify-center text-xs text-neutral-600 mb-2">
              <span className="text-neutral-600">─────── </span>
              <span className="text-neutral-500 mx-2">Decision Trace</span>
              <span className="text-neutral-600"> ───────</span>
            </div>

            {/* Status Badge */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Status:
              </span>
              <span
                className={`inline-flex items-center text-xs font-mono font-medium uppercase tracking-wider px-2 py-1 rounded border ${
                  result.status === "ALLOW"
                    ? "border-emerald-400/30 bg-emerald-400/5 text-emerald-400"
                    : "border-red-400/30 bg-red-400/5 text-red-400"
                }`}
              >
                {result.status}
              </span>
            </div>

            {/* Reason Code */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Reason:
              </span>
              <span className="text-xs font-mono text-amber-400">
                {result.reason_code}
              </span>
            </div>

            {/* Confidence */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Confidence:
              </span>
              <span className="text-xs font-mono text-sky-400">
                {result.confidence.toFixed(2)}
              </span>
            </div>

            {/* Evidence Count */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Evidence:
              </span>
              <span className="text-xs font-mono text-violet-400">
                {result.evidence_count} {result.evidence_count === 1 ? "source" : "sources"}
              </span>
            </div>
          </div>

          {/* Answer (conditional) */}
          {result.status === "ALLOW" && result.answer && (
            <div className="p-4">
              <div className="text-xs text-neutral-600 uppercase tracking-wider mb-3">
                Answer
              </div>
              <div className="text-sm text-neutral-200 leading-relaxed">
                {result.answer}
              </div>
            </div>
          )}

          {/* Show refusal message if ABSTAIN */}
          {result.status === "ABSTAIN" && (
            <div className="p-4">
              <div className="text-xs text-neutral-500 uppercase tracking-wider mb-2">
                Response
              </div>
              <div className="text-sm text-neutral-400">
                {result.message}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
