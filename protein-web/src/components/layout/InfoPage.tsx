import React from "react";
import Link from "next/link";

/** Shared layout for plain reading pages (privacy, terms, how we rate). */
export const InfoPage: React.FC<{ title: string; updated?: string; children: React.ReactNode }> = ({
  title,
  updated,
  children,
}) => (
  <div className="container max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-16 flex flex-col gap-8">
    <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#968E85]">
      <Link href="/" className="hover:text-[#F5F2EB] transition-colors">
        Home
      </Link>
      <span>/</span>
      <span className="text-[#F5F2EB] font-bold">{title}</span>
    </nav>

    <header className="flex flex-col gap-2 pb-6 border-b border-[#332D27]">
      <h1 className="text-3xl sm:text-4xl font-black text-[#F5F2EB] tracking-tight">{title}</h1>
      {updated && <p className="text-xs font-mono text-[#968E85]">Last updated: {updated}</p>}
    </header>

    <div className="flex flex-col gap-8 text-sm leading-relaxed text-[#C9C3BA] font-sans">{children}</div>
  </div>
);

export const InfoSection: React.FC<{ id?: string; title: string; children: React.ReactNode }> = ({
  id,
  title,
  children,
}) => (
  <section id={id} className="flex flex-col gap-3 scroll-mt-24">
    <h2 className="text-lg font-bold text-[#F5F2EB] tracking-tight">{title}</h2>
    {children}
  </section>
);
