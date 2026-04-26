"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { siteConfig } from "@/lib/site";
import { ScalesLogoIcon } from "@/components/icons";

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="absolute inset-x-0 top-0 z-30">
      <div className="container-shell flex h-20 items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-11 w-11 items-center justify-center rounded-md bg-gold-500/10 text-gold-400 ring-1 ring-gold-500/30">
            <ScalesLogoIcon className="h-7 w-7" />
          </span>
          <span className="leading-tight">
            <span className="block text-display text-xl font-bold tracking-wide text-white">
              {siteConfig.name}
            </span>
            <span className="block text-[11px] uppercase tracking-[0.2em] text-slate-400">
              {siteConfig.tagline}
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-9 md:flex">
          {siteConfig.nav.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                data-active={active}
                className="nav-link"
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="hidden rounded-md border border-white/20 px-5 py-2 text-sm font-medium text-white transition hover:bg-white/10 md:inline-flex"
          >
            Giris Yap
          </Link>
          <Link
            href="/signup"
            className="rounded-md bg-gold-500 px-5 py-2 text-sm font-semibold text-navy-950 transition hover:bg-gold-400"
          >
            Uye Ol
          </Link>
        </div>
      </div>
    </header>
  );
}
