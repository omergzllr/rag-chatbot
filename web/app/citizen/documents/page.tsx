"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type DocTypeItem = {
  doc_type: string;
  title: string;
  description: string;
};

export default function CitizenDocumentsPage() {
  const [items, setItems] = useState<DocTypeItem[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const run = async () => {
      try {
        const res = await fetch("/api/citizen/doc-types");
        const data = (await res.json()) as { items?: DocTypeItem[]; error?: string };
        if (!res.ok) throw new Error(data.error || "Dokuman turleri yuklenemedi");
        setItems(data.items ?? []);
      } catch (err) {
        setError(String(err));
      } finally {
        setLoading(false);
      }
    };
    void run();
  }, []);

  return (
    <main className="bg-navy-950 px-6 py-24 text-white">
      <div className="container-shell">
        <h1 className="text-display text-4xl font-bold">Vatandas Dokuman Sablonlari</h1>
        <p className="mt-3 text-slate-300">Ihtiyac duydugunuz belgeyi secin, sistem adim adim sorularla hazirlasin.</p>
        {loading ? <p className="mt-6 text-slate-400">Yukleniyor...</p> : null}
        {error ? <p className="mt-6 text-red-400">{error}</p> : null}
        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {items.map((item) => (
            <article key={item.doc_type} className="surface p-5">
              <h2 className="text-lg font-semibold">{item.title}</h2>
              <p className="mt-2 text-sm text-slate-300">{item.description}</p>
              <Link className="btn-gold mt-4 inline-flex" href={`/citizen/session/new?docType=${item.doc_type}`}>
                Bu Sablonu Baslat
              </Link>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}

