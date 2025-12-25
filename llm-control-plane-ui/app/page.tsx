"use client";

import { useState } from "react";

/**
 * Bytez embedding models (curated, free-tier friendly)
 * Capability switch ONLY — does not affect control logic.
 */
const BYTEZ_MODELS = [
  "sentence-transformers/all-MiniLM-L6-v2",
  "ibm-granite/granite-embedding-small-english-r2",
  "nomic-ai/nomic-embed-text-v1.5",
  "mesolitica/llama2-embedding-600m-8k",
  "Lajavaness/bilingual-embedding-large",
  "embedding-light-128",
  "embedding-base-768",
  "embedding-xl-2048",
];

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
  const [selectedModel, setSelectedModel] = useState<string>(
    BYTEZ_MODELS[0]
  );
  const [result, setResult] = useState<ControlResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function submitQuery() {
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        embedding_model: selectedModel,
      }),
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
          placeholder="Enter query for evaluation…"
        />

        {/* Embedding Model Selector */}
        <div className="space-y-1">
          <label className="block text-xs uppercase tracking-wider text-neutral-500">
            Embedding Model (Bytez)
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full rounded bg-neutral-900 border border-neutral-800 px-3 py-2 text-sm text-neutral-100 focus:outline-none focus:ring-1 focus:ring-neutral-600"
          >
            {BYTEZ_MODELS.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>

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
          <div className="p-4 space-y-4">
            {/* Decision Trace Label */}
            <div className="flex items-center justify-center text-xs text-neutral-600 mb-2">
              <span className="text-neutral-600">─────── </span>
              <span className="text-neutral-500 mx-2">Decision Trace</span>
              <span className="text-neutral-600"> ───────</span>
            </div>

            {/* Status */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Status:
              </span>
              <span
                className={`inline-flex items-center text-xs font-mono uppercase tracking-wider px-2 py-1 rounded border ${
                  result.status === "ALLOW"
                    ? "border-emerald-400/30 bg-emerald-400/5 text-emerald-400"
                    : "border-red-400/30 bg-red-400/5 text-red-400"
                }`}
              >
                {result.status}
              </span>
            </div>

            {/* Reason */}
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

            {/* Evidence */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-neutral-500 uppercase tracking-wider">
                Evidence:
              </span>
              <span className="text-xs font-mono text-violet-400">
                {result.evidence_count}{" "}
                {result.evidence_count === 1 ? "source" : "sources"}
              </span>
            </div>
          </div>

          {/* Answer */}
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

          {/* Refusal */}
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
