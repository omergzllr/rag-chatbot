import { BellIcon, ArrowRightIcon } from "@/components/icons";

const announcements = [
  { title: "Yeni Ictihatlar Sisteme Eklendi", date: "20 Mayis 2024" },
  { title: "KVKK Rehberi Guncellendi", date: "15 Mayis 2024" },
  { title: "E-ticaret Mevzuati Degisiklikleri", date: "10 Mayis 2024" }
];

export function Announcements() {
  return (
    <div className="surface w-full max-w-md p-5">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BellIcon className="h-5 w-5 text-gold-400" />
          <h3 className="text-base font-semibold text-white">Duyurular</h3>
        </div>
        <a
          href="#"
          className="flex items-center gap-1 text-xs font-medium text-gold-400 hover:text-gold-300"
        >
          Tumu <ArrowRightIcon className="h-3.5 w-3.5" />
        </a>
      </div>
      <ul className="divide-y divide-white/5">
        {announcements.map((a) => (
          <li key={a.title} className="flex items-center justify-between gap-4 py-3">
            <span className="text-sm text-slate-200">{a.title}</span>
            <span className="text-xs text-slate-400">{a.date}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
