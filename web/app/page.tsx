import Link from "next/link";
import { LegalChatWidget } from "@/components/legal-chat-widget";
import { Announcements } from "@/components/announcements";
import {
  ShieldIcon,
  LockIcon,
  BoltIcon,
  PlayIcon,
  BookIcon,
  GavelIcon,
  DocumentIcon,
  ChatIcon,
  ArrowRightIcon,
  DatabaseIcon,
  ScaleIcon,
  CheckIcon
} from "@/components/icons";

const services = [
  {
    icon: BookIcon,
    title: "Mevzuat Arama",
    description: "Guncel yasa, tuzuk ve yonetmelik aramasi yapin.",
    accent: false
  },
  {
    icon: GavelIcon,
    title: "Ictihat Arama",
    description: "Yargitay ve Danistay kararlarina hizlica ulasin.",
    accent: true
  },
  {
    icon: DocumentIcon,
    title: "Doktrin Arama",
    description: "Makale, gorus ve hukuki yayinlari inceleyin.",
    accent: false
  },
  {
    icon: ChatIcon,
    title: "Akilli Soru-Cevap",
    description: "Yapay zeka ile hukuki sorulariniza yanit alin.",
    accent: true
  }
];

const steps = [
  {
    icon: ChatIcon,
    title: "Soru Sorun",
    description: "Hukuki probleminizi anlasilir sekilde yazin."
  },
  {
    icon: DatabaseIcon,
    title: "Analiz Etsin",
    description: "Yapay zeka, kaynaklari tarayip analiz etsin."
  },
  {
    icon: ScaleIcon,
    title: "Yanitlasin",
    description: "Size en dogru ve guncel yaniti sunsun."
  },
  {
    icon: CheckIcon,
    title: "Kaynak Gosterir",
    description: "Dayanak ve kaynaklarla seffaf sekilde sunsun."
  }
];

const features = [
  {
    icon: ShieldIcon,
    title: "Guvenilir Kaynaklar",
    description: "Mevzuat, ictihat ve doktrin tabanli yanitlar"
  },
  {
    icon: LockIcon,
    title: "Gizlilik Onceligimiz",
    description: "Sorulariniz ve verileriniz guvende"
  },
  {
    icon: BoltIcon,
    title: "Hizli ve Dogru",
    description: "Yapay zeka ile aninda akilli yanitlar"
  }
];

export default function HomePage() {
  return (
    <>
      {/* HERO */}
      <section className="relative overflow-hidden bg-navy-900 pb-20 pt-28 md:pb-28 md:pt-32">
        {/* AI-generated Lady Justice — photo hero, blends into navy */}
        <div
          className="pointer-events-none absolute inset-y-0 right-0 w-[min(100%,56rem)] bg-[url('/justice-hero.png')] bg-cover bg-[center_22%] opacity-[0.38] md:opacity-45"
          aria-hidden
        />
        <div
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-navy-900 from-40% via-navy-900/88 to-navy-900/25"
          aria-hidden
        />
        <div
          className="pointer-events-none absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              "radial-gradient(800px 400px at 30% 0%, rgba(212,168,83,0.12), transparent 60%), radial-gradient(600px 400px at 90% 100%, rgba(34,56,90,0.35), transparent 60%)"
          }}
          aria-hidden
        />

        <div className="container-shell relative grid items-center gap-12 lg:grid-cols-[1.05fr_0.95fr]">
          <div>
            <h1 className="text-display text-4xl font-bold leading-tight tracking-tight text-white md:text-5xl lg:text-6xl">
              Hukuki Sorulariniz Icin
              <br />
              <span className="text-gold-500">Akilli Cozumler</span>
            </h1>
            <p className="mt-6 max-w-xl text-base leading-relaxed text-slate-300 md:text-lg">
              HUKUK RAG, gelismis yapay zeka teknolojisi ile mevzuat, ictihat ve doktrin
              bilgilerine dayali dogru ve guncel yanitlar sunar.
            </p>

            <div className="mt-8 flex flex-wrap items-center gap-4">
              <Link href="/demo" className="btn-gold">
                Hemen Sor
              </Link>
              <Link href="#nasil-calisir" className="btn-outline">
                Nasil Calisir? <PlayIcon className="h-3.5 w-3.5" />
              </Link>
            </div>

            <ul className="mt-12 grid gap-6 sm:grid-cols-3">
              {features.map((f) => (
                <li key={f.title} className="flex items-start gap-3">
                  <span className="mt-0.5 flex h-9 w-9 flex-none items-center justify-center rounded-md border border-white/10 bg-white/5 text-gold-400">
                    <f.icon className="h-4 w-4" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-white">{f.title}</p>
                    <p className="text-xs leading-relaxed text-slate-400">
                      {f.description}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div className="hidden justify-end lg:flex">
            <LegalChatWidget anchorId="demo-chat" />
          </div>
        </div>

        {/* mobile chat — ayni canli demo widget */}
        <div className="container-shell mt-12 flex justify-center lg:hidden">
          <LegalChatWidget anchorId="demo-chat-mobile" />
        </div>
      </section>

      {/* SERVICE CARDS */}
      <section className="bg-navy-950 py-14">
        <div className="container-shell grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {services.map((s) => (
            <article key={s.title} className="surface group flex flex-col p-6">
              <span
                className={
                  "mb-5 flex h-12 w-12 items-center justify-center rounded-md " +
                  (s.accent
                    ? "bg-gold-500/15 text-gold-400 ring-1 ring-gold-500/30"
                    : "bg-white/5 text-slate-200 ring-1 ring-white/10")
                }
              >
                <s.icon className="h-6 w-6" />
              </span>
              <h3 className="text-lg font-semibold text-white">{s.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-400">
                {s.description}
              </p>
              <Link
                href="/features"
                className="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-gold-400 transition group-hover:text-gold-300"
              >
                Kesfet <ArrowRightIcon className="h-3.5 w-3.5" />
              </Link>
            </article>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="nasil-calisir" className="bg-navy-950 py-16">
        <div className="container-shell">
          <h2 className="text-display text-center text-3xl font-bold text-white md:text-4xl">
            Nasil Calisir?
          </h2>
          <ol className="relative mx-auto mt-12 grid max-w-5xl gap-10 sm:grid-cols-2 lg:grid-cols-4">
            <span
              aria-hidden
              className="pointer-events-none absolute left-10 right-10 top-7 hidden h-px bg-white/10 lg:block"
            />
            {steps.map((step, i) => (
              <li key={step.title} className="relative flex flex-col items-center text-center">
                <span className="relative flex h-14 w-14 items-center justify-center rounded-full border border-white/15 bg-navy-800 text-gold-400 shadow-lg">
                  <step.icon className="h-6 w-6" />
                </span>
                <p className="mt-4 text-base font-semibold text-white">
                  {i + 1}. {step.title}
                </p>
                <p className="mt-1 max-w-[220px] text-sm text-slate-400">
                  {step.description}
                </p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ANNOUNCEMENTS */}
      <section className="bg-navy-950 pb-20">
        <div className="container-shell flex justify-center">
          <Announcements />
        </div>
      </section>
    </>
  );
}
