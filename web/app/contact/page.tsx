export default function ContactPage() {
  return (
    <section className="container-shell py-28">
      <h1 className="section-title">Iletisim</h1>
      <p className="section-copy">Demo, fiyatlandirma ve kurumsal entegrasyon talepleriniz icin ulasin.</p>
      <form className="card-surface mt-8 grid gap-4 p-6 md:max-w-2xl">
        <input className="rounded-lg border border-white/10 bg-navy-900 px-4 py-3 text-sm placeholder:text-slate-500" placeholder="Ad Soyad" />
        <input className="rounded-lg border border-white/10 bg-navy-900 px-4 py-3 text-sm placeholder:text-slate-500" placeholder="E-posta" />
        <textarea className="min-h-32 rounded-lg border border-white/10 bg-navy-900 px-4 py-3 text-sm placeholder:text-slate-500" placeholder="Mesajiniz" />
        <button type="button" className="button-primary w-fit">Gonder</button>
      </form>
    </section>
  );
}
