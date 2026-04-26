import Link from "next/link";
import { siteConfig } from "@/lib/site";
import { ScalesLogoIcon } from "@/components/icons";

export function Footer() {
  return (
    <footer className="border-t border-white/5 bg-navy-950 py-10">
      <div className="container-shell flex flex-col items-center justify-between gap-4 text-sm text-slate-400 md:flex-row">
        <div className="flex items-center gap-2">
          <ScalesLogoIcon className="h-5 w-5 text-gold-400" />
          <span className="text-display text-lg text-white">{siteConfig.name}</span>
          <span className="text-slate-500">— {siteConfig.tagline}</span>
        </div>
        <div className="flex items-center gap-6">
          {siteConfig.nav.map((item) => (
            <Link key={item.href} href={item.href} className="hover:text-white">
              {item.label}
            </Link>
          ))}
        </div>
        <span>© {new Date().getFullYear()} {siteConfig.name}</span>
      </div>
    </footer>
  );
}
