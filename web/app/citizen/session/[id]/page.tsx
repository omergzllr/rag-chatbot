"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";

type SessionPayload = {
  session_id: string;
  doc_type?: string;
  flow_state: string;
  draft: string;
  answers?: Record<string, string>;
  asked_field?: string;
  assistant_message?: string;
  safety_notice?: string;
};

type ChatTurn = { role: "user" | "assistant"; content: string };

export default function CitizenSessionPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [session, setSession] = useState<SessionPayload | null>(null);
  const [chat, setChat] = useState<ChatTurn[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [bootstrapping, setBootstrapping] = useState(true);
  const [error, setError] = useState("");
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    const apply = (data: SessionPayload, append: boolean) => {
      if (cancelled) return;
      setSession(data);
      if (data.assistant_message) {
        setChat((prev) =>
          append && prev.some((c) => c.role === "assistant" && c.content === data.assistant_message)
            ? prev
            : [...prev, { role: "assistant", content: data.assistant_message! }],
        );
      }
    };

    const cacheKey = `citizen-session:${id}`;
    try {
      const cached = sessionStorage.getItem(cacheKey);
      if (cached) {
        const data = JSON.parse(cached) as SessionPayload;
        apply(data, false);
        sessionStorage.removeItem(cacheKey);
        setBootstrapping(false);
        return () => {
          cancelled = true;
        };
      }
    } catch {
    }

    const load = async () => {
      try {
        const res = await fetch(`/api/citizen/session/${id}`);
        const data = (await res.json()) as SessionPayload;
        apply(data, false);
      } catch (err) {
        if (!cancelled) setError(String(err));
      } finally {
        if (!cancelled) setBootstrapping(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [id]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!message.trim() || loading) return;
    const userText = message.trim();
    setChat((prev) => [...prev, { role: "user", content: userText }]);
    setMessage("");
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`/api/citizen/session/${id}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });
      const data = (await res.json()) as SessionPayload & { error?: string };
      if (!res.ok) throw new Error(data.error || "Mesaj gonderilemedi");
      setSession(data);
      if (data.assistant_message) {
        setChat((prev) => [...prev, { role: "assistant", content: data.assistant_message! }]);
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  const flowLabel: Record<string, string> = {
    collecting: "Bilgi topluyoruz",
    draft_ready: "Taslak hazir",
    review: "Inceleme / revizyon",
  };

  return (
    <main className="bg-navy-950 px-6 py-24 text-white">
      <div className="container-shell grid gap-6 lg:grid-cols-[1fr_1fr]">
        <section className="surface flex flex-col p-5">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold">Akilli Soru Akisi</h1>
            <span className="rounded-full bg-white/10 px-3 py-1 text-xs uppercase tracking-wide">
              {flowLabel[session?.flow_state ?? ""] ?? session?.flow_state ?? "yukleniyor"}
            </span>
          </div>
          {session?.doc_type ? (
            <p className="mt-1 text-xs text-slate-400">Dokuman: {session.doc_type}</p>
          ) : null}

          <div className="mt-4 flex max-h-[440px] flex-1 flex-col gap-3 overflow-auto rounded-md bg-navy-900/40 p-3">
            {bootstrapping && chat.length === 0 ? (
              <p className="text-sm text-slate-400">Akilli soru hazirlaniyor...</p>
            ) : null}
            {chat.map((turn, idx) => (
              <div
                key={idx}
                className={
                  turn.role === "assistant"
                    ? "self-start max-w-[85%] rounded-lg bg-white/10 px-3 py-2 text-sm text-slate-100"
                    : "self-end max-w-[85%] rounded-lg bg-amber-500/20 px-3 py-2 text-sm text-amber-50"
                }
              >
                {turn.content}
              </div>
            ))}
            {loading ? (
              <div className="self-start rounded-lg bg-white/5 px-3 py-2 text-xs text-slate-300">
                Yaniti hazirliyorum...
              </div>
            ) : null}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={onSubmit} className="mt-4 space-y-3">
            <textarea
              className="w-full rounded-md border border-white/20 bg-navy-900 p-3"
              rows={3}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={
                session?.flow_state === "draft_ready"
                  ? "Ornek: 'Sureyi 30 gun yap' veya 'Tahliye gerekcesini guncelle: ...'"
                  : "Sorulan bilgiyi yazin..."
              }
            />
            <div className="flex items-center gap-3">
              <button className="btn-gold" type="submit" disabled={loading || !message.trim()}>
                {loading ? "Gonderiliyor..." : "Gonder"}
              </button>
              {session?.asked_field ? (
                <span className="text-xs text-slate-400">Beklenen alan: {session.asked_field}</span>
              ) : null}
            </div>
          </form>
          {error ? <p className="mt-3 text-sm text-red-400">{error}</p> : null}
          <p className="mt-4 text-xs text-slate-400">{session?.safety_notice}</p>
        </section>

        <section className="surface p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Taslak Onizleme</h2>
            {session?.draft ? (
              <button
                type="button"
                className="rounded-md border border-white/20 px-3 py-1 text-xs text-slate-200 hover:bg-white/10"
                onClick={() => navigator.clipboard?.writeText(session.draft)}
              >
                Kopyala
              </button>
            ) : null}
          </div>
          <pre className="mt-3 max-h-[550px] overflow-auto whitespace-pre-wrap rounded-md bg-navy-900 p-4 text-sm text-slate-200">
            {session?.draft || "Bilgiler tamamlandiginda taslak burada olusturulacak."}
          </pre>
          {session?.answers && Object.keys(session.answers).length > 0 ? (
            <div className="mt-4 rounded-md border border-white/10 p-3 text-xs text-slate-300">
              <p className="mb-2 font-semibold text-slate-200">Toplanan bilgiler</p>
              <ul className="space-y-1">
                {Object.entries(session.answers).map(([key, value]) => (
                  <li key={key}>
                    <span className="text-slate-400">{key}:</span> {value}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}
