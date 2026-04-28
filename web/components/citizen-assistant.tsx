"use client";

import { FormEvent, useState } from "react";

type AssistResult = {
  rights_analysis?: { category: string; rights: string[]; first_step: string };
  procedure_guide?: { checklist: { step: number; action: string }[] };
  cost_duration_estimate?: {
    city: string;
    duration_estimate: { estimated_month_range?: string };
    cost_breakdown: Record<string, number>;
  };
};

export function CitizenAssistant() {
  const [narrative, setNarrative] = useState("");
  const [city, setCity] = useState("istanbul");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AssistResult | null>(null);
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!narrative.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("/api/citizen/assist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ narrative, city }),
      });
      const data = (await res.json()) as AssistResult & { error?: string };
      if (!res.ok) throw new Error(data.error || "Analiz alinamadi");
      setResult(data);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="surface mt-8 p-6">
      <h3 className="text-xl font-semibold text-white">Haklarim Neler? Hemen Ogren</h3>
      <form onSubmit={onSubmit} className="mt-4 space-y-3">
        <textarea
          className="w-full rounded-md border border-white/20 bg-navy-900 p-3 text-sm text-white"
          rows={4}
          placeholder="Ornegin: Dugun salonu iptal etti ve parami iade etmiyor."
          value={narrative}
          onChange={(e) => setNarrative(e.target.value)}
        />
        <input
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="w-full rounded-md border border-white/20 bg-navy-900 p-3 text-sm text-white"
          placeholder="Sehir (orn: istanbul)"
        />
        <button className="btn-gold" type="submit" disabled={loading}>
          {loading ? "Analiz Ediliyor..." : "Analizi Baslat"}
        </button>
      </form>
      {error ? <p className="mt-3 text-sm text-red-400">{error}</p> : null}
      {result ? (
        <div className="mt-6 grid gap-4 text-sm text-slate-200 md:grid-cols-3">
          <div className="rounded-md border border-white/10 bg-white/5 p-4">
            <p className="font-semibold text-gold-400">Temel Haklar</p>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {result.rights_analysis?.rights?.map((right) => <li key={right}>{right}</li>)}
            </ul>
          </div>
          <div className="rounded-md border border-white/10 bg-white/5 p-4">
            <p className="font-semibold text-gold-400">Adim Adim Rehber</p>
            <ul className="mt-2 space-y-1">
              {result.procedure_guide?.checklist?.map((step) => (
                <li key={step.step}>
                  {step.step}. {step.action}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-md border border-white/10 bg-white/5 p-4">
            <p className="font-semibold text-gold-400">Masraf ve Sure Tahmini</p>
            <p className="mt-2">
              Tahmini Sure: {result.cost_duration_estimate?.duration_estimate?.estimated_month_range ?? "-"}
            </p>
            <ul className="mt-2 space-y-1">
              {Object.entries(result.cost_duration_estimate?.cost_breakdown ?? {}).map(([key, value]) => (
                <li key={key}>
                  {key}: {value} TRY
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : null}
    </section>
  );
}

