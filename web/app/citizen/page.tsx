import Link from "next/link";
import { CitizenAssistant } from "@/components/citizen-assistant";

export default function CitizenLandingPage() {
  return (
    <main className="bg-navy-950 px-6 py-24 text-white">
      <div className="container-shell">
        <h1 className="text-display text-4xl font-bold">Halk Icin Hukuk</h1>
        <p className="mt-3 max-w-3xl text-slate-300">
          Hukuki metinleri sade dille anlamaniza, adim adim belge hazirlamaniza ve prosedurleri takip etmenize
          yardimci olan vatandas odakli moduldur.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link href="/citizen/documents" className="btn-gold">
            Dokuman Hazirlamaya Basla
          </Link>
          <Link href="/demo" className="btn-outline">
            Genel Chat Demoyu Ac
          </Link>
        </div>
        <CitizenAssistant />
      </div>
    </main>
  );
}

