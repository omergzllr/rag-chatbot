import { LegalChatWidget } from "@/components/legal-chat-widget";

export default function DemoPage() {
  return (
    <section className="relative min-h-[calc(100vh-5rem)] overflow-hidden bg-navy-900 pt-24 pb-16 md:pt-28">
      <div
        className="pointer-events-none absolute inset-y-0 right-0 w-full max-w-[min(100%,48rem)] bg-[url('/justice-hero.png')] bg-cover bg-[center_25%] opacity-[0.32] md:opacity-40"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-gradient-to-b from-navy-900/95 via-navy-900/90 to-navy-950"
        aria-hidden
      />

      <div className="container-shell relative flex flex-col items-center px-4">
        <h1 className="text-display text-center text-3xl font-bold text-white md:text-4xl">
          Canli Demo
        </h1>
        <p className="mt-3 max-w-lg text-center text-sm text-slate-300 md:text-base">
          Asistan ile ayni arayuzu kullanarak sorunuzu yazin; yanitlar bilgilendirme amaclidir.
        </p>
        <div className="mt-10 flex w-full justify-center">
          <LegalChatWidget className="w-full sm:max-w-md" anchorId="demo-page-chat" />
        </div>
      </div>
    </section>
  );
}
