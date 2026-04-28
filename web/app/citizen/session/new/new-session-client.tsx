"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

type NewSessionClientProps = {
  docType: string;
};

export default function NewSessionClient({ docType }: NewSessionClientProps) {
  const router = useRouter();
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!docType) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/citizen/session/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_type: docType, prompt }),
      });
      const data = (await res.json()) as { error?: string; session_id?: string };
      if (!res.ok || !data.session_id) throw new Error(data.error || "Oturum baslatilamadi");
      try {
        sessionStorage.setItem(`citizen-session:${data.session_id}`, JSON.stringify(data));
      } catch {
      }
      router.push(`/citizen/session/${data.session_id}`);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="bg-navy-950 px-6 py-24 text-white">
      <div className="container-shell max-w-2xl">
        <h1 className="text-display text-3xl font-bold">Vatandas Oturumu Baslat</h1>
        <p className="mt-2 text-slate-300">Secilen dokuman: {docType || "Belirtilmedi"}</p>
        <form onSubmit={onSubmit} className="surface mt-6 space-y-4 p-5">
          <textarea
            className="w-full rounded-md border border-white/20 bg-navy-900 p-3"
            rows={4}
            placeholder="Durumunuzu kisaca anlatin..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button className="btn-gold" type="submit" disabled={loading || !docType}>
            {loading ? "Baslatiliyor..." : "Oturumu Baslat"}
          </button>
          {error ? <p className="text-sm text-red-400">{error}</p> : null}
        </form>
      </div>
    </main>
  );
}

