const faqs = [
  {
    q: "HUKUK RAG nedir?",
    a: "Mevzuat, ictihat ve doktrin kaynaklari uzerinde calisan, kaynak gosteren bir yapay zeka asistanidir."
  },
  {
    q: "Verilerim guvende mi?",
    a: "Sorgulariniz gizli tutulur, KVKK ve sektor standartlarina uygun sekilde islenir."
  },
  {
    q: "Yanitlar hukuki tavsiye yerine gecer mi?",
    a: "Hayir. Yanitlar bilgilendirme amaclidir; kesin durumlar icin bir hukuk profesyonelinden gorus alinmasi onerilir."
  },
  {
    q: "Hangi kaynaklar taranir?",
    a: "Resmi mevzuat, yuksek mahkeme kararlari ve secilmis akademik yayinlar."
  }
];

export default function FaqPage() {
  return (
    <section className="container-shell py-28">
      <h1 className="section-title">Sikca Sorulan Sorular</h1>
      <p className="section-copy">HUKUK RAG hakkinda en sik sorulan sorular ve yanitlari.</p>
      <div className="mt-10 grid gap-4 md:max-w-3xl">
        {faqs.map((f) => (
          <details key={f.q} className="card-surface p-5 open:border-gold-500/40">
            <summary className="cursor-pointer list-none text-base font-semibold text-white">
              {f.q}
            </summary>
            <p className="mt-3 text-sm text-slate-300">{f.a}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
