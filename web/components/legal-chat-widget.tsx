"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { ScalesLogoIcon, MinusIcon, CloseIcon, SendIcon } from "@/components/icons";

type Role = "user" | "assistant";

type ChatMessage = {
  id: string;
  role: Role;
  content: string;
};

function uid() {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : String(Date.now()) + Math.random().toString(16).slice(2);
}

type LegalChatWidgetProps = {
  className?: string;
  /** Tek sayfada birden fazla widget varsa benzersiz id (varsayilan: demo-chat) */
  anchorId?: string;
};

export function LegalChatWidget({ className = "", anchorId = "demo-chat" }: LegalChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Merhaba! Size nasil yardimci olabilirim? Hukuki sorunuzu yazabilirsiniz."
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setError("");
    const userMsg: ChatMessage = { id: uid(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
      });
      const data = (await res.json()) as { error?: string; answer?: string };
      if (!res.ok) {
        throw new Error(data.error || "Istek basarisiz");
      }
      const answer = data.answer ?? "Cevap alinamadi.";
      setMessages((prev) => [
        ...prev,
        { id: uid(), role: "assistant", content: String(answer) }
      ]);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    void sendMessage();
  }

  return (
    <div
      id={anchorId}
      className={`relative w-full max-w-md rounded-2xl bg-white text-slate-800 shadow-2xl ring-1 ring-white/10 ${className}`}
    >
      <div className="flex items-center justify-between rounded-t-2xl border-b border-slate-200 bg-white px-4 py-3">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-md bg-navy-900 text-gold-400">
            <ScalesLogoIcon className="h-5 w-5" />
          </span>
          <div className="leading-tight">
            <p className="text-sm font-semibold text-navy-900">HUKUK RAG Asistan</p>
            <p className="flex items-center gap-1.5 text-xs text-emerald-600">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              Cevrimici
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          <button type="button" className="rounded p-1 hover:bg-slate-100" aria-label="Kucult">
            <MinusIcon className="h-4 w-4" />
          </button>
          <button type="button" className="rounded p-1 hover:bg-slate-100" aria-label="Kapat">
            <CloseIcon className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="max-h-[min(420px,55vh)] space-y-4 overflow-y-auto px-4 py-5">
        {messages.map((m) =>
          m.role === "assistant" ? (
            <div key={m.id} className="flex items-start gap-2">
              <span className="mt-1 flex h-7 w-7 flex-none items-center justify-center rounded-md bg-navy-900 text-gold-400">
                <ScalesLogoIcon className="h-4 w-4" />
              </span>
              <div className="max-w-[85%] rounded-lg rounded-tl-sm bg-slate-100 px-3 py-2 text-sm text-slate-700">
                <p className="whitespace-pre-wrap">{m.content}</p>
              </div>
            </div>
          ) : (
            <div key={m.id} className="flex justify-end">
              <div className="max-w-[85%] rounded-lg rounded-tr-sm bg-navy-900 px-3 py-2 text-sm text-white">
                <p className="whitespace-pre-wrap">{m.content}</p>
              </div>
            </div>
          )
        )}

        {loading ? (
          <div className="flex items-start gap-2">
            <span className="mt-1 flex h-7 w-7 flex-none items-center justify-center rounded-md bg-navy-900 text-gold-400">
              <ScalesLogoIcon className="h-4 w-4" />
            </span>
            <div className="rounded-lg rounded-tl-sm bg-slate-100 px-3 py-2 text-sm text-slate-500">
              Yanit hazirlaniyor...
            </div>
          </div>
        ) : null}

        <div ref={endRef} />
      </div>

      {error ? (
        <p className="px-4 pb-1 text-center text-xs text-red-600">{error}</p>
      ) : null}

      <form onSubmit={onSubmit} className="border-t border-slate-200 px-4 py-3">
        <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
          <input
            type="text"
            placeholder="Sorunuzu yazin..."
            className="flex-1 bg-transparent text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            autoComplete="off"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex h-9 w-9 flex-none items-center justify-center rounded-md bg-navy-900 text-gold-400 transition hover:bg-navy-800 disabled:opacity-40"
            aria-label="Gonder"
          >
            <SendIcon className="h-4 w-4" />
          </button>
        </div>
        <p className="mt-2 text-center text-[11px] text-slate-500">
          Yanitlar bilgilendirme amaclidir, hukuki tavsiye niteligi tasimaz.
        </p>
      </form>
    </div>
  );
}
