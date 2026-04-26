import Link from "next/link";

export default function LoginPage() {
  return (
    <section className="container-shell flex min-h-[80vh] items-center py-24">
      <div className="mx-auto w-full max-w-md">
        <h1 className="section-title">Giris Yap</h1>
        <p className="section-copy">Hesabiniza giris yaparak sorgu gecmisinize erisin.</p>
        <form className="card-surface mt-8 grid gap-4 p-6">
          <input
            className="rounded-lg border border-white/10 bg-navy-900 px-4 py-3 text-sm placeholder:text-slate-500"
            placeholder="E-posta"
            type="email"
          />
          <input
            className="rounded-lg border border-white/10 bg-navy-900 px-4 py-3 text-sm placeholder:text-slate-500"
            placeholder="Sifre"
            type="password"
          />
          <button type="button" className="button-primary w-full">
            Giris Yap
          </button>
          <p className="text-center text-sm text-slate-400">
            Hesabiniz yok mu?{" "}
            <Link href="/signup" className="text-gold-400 hover:text-gold-300">
              Uye Ol
            </Link>
          </p>
        </form>
      </div>
    </section>
  );
}
