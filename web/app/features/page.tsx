const services = [
  {
    title: "Mevzuat Arama",
    description:
      "Guncel yasa, tuzuk ve yonetmeliklere madde duzeyinde dogal dil ile erisim."
  },
  {
    title: "Ictihat Arama",
    description: "Yargitay ve Danistay kararlari uzerinde semantik benzerlik tabanli arama."
  },
  {
    title: "Doktrin Arama",
    description: "Akademik makaleler ve hukuki yayinlardan ilgili pasajlari ozetler."
  },
  {
    title: "Akilli Soru-Cevap",
    description: "RAG mimarisi ile kaynak gostererek dogru ve guncel yanitlar."
  },
  {
    title: "Kaynak Sorgulama",
    description: "Her yanitin altinda atif yapilan dosya ve madde referanslari."
  },
  {
    title: "Ekip Calismasi",
    description: "Ekip uyeleri ile paylasilabilir oturumlar ve calisma alanlari."
  }
];

export default function FeaturesPage() {
  return (
    <section className="container-shell py-28">
      <h1 className="section-title">Hizmetler</h1>
      <p className="section-copy">
        Hukuk profesyonelleri icin gelistirilmis yapay zeka ve RAG yetenekleri.
      </p>
      <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {services.map((s) => (
          <article key={s.title} className="card-surface p-6">
            <h2 className="text-lg font-semibold text-white">{s.title}</h2>
            <p className="mt-2 text-sm text-slate-300">{s.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
