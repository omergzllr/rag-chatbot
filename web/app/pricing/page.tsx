const plans = [
  { name: "Starter", price: "₺3.999", desc: "Kucuk ekipler icin", items: ["5.000 sorgu/ay", "Temel destek", "Tek bilgi tabani"] },
  { name: "Growth", price: "₺9.999", desc: "Buyuyen hukuk ekipleri", items: ["25.000 sorgu/ay", "Oncelikli destek", "Coklu bilgi tabani"] },
  { name: "Enterprise", price: "Teklif", desc: "Kurumsal olcek", items: ["Sinirsiz olcek", "SSO/SAML", "Ozel guvenlik gereksinimleri"] }
];

export default function PricingPage() {
  return (
    <section className="container-shell py-20">
      <h1 className="section-title">Fiyatlandirma</h1>
      <p className="section-copy">Sadece kullandiginiz kadar odediginiz esnek ve kurumsal planlar.</p>
      <div className="mt-10 grid gap-4 md:grid-cols-3">
        {plans.map((plan) => (
          <article key={plan.name} className="card-surface p-6">
            <h2 className="text-xl font-semibold">{plan.name}</h2>
            <p className="mt-2 text-3xl font-semibold">{plan.price}</p>
            <p className="mt-2 text-sm text-slate-300">{plan.desc}</p>
            <ul className="mt-4 space-y-2 text-sm text-slate-200">
              {plan.items.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
