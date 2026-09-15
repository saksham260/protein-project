import React from "react";
import Link from "next/link";
import { CATEGORIES } from "@/lib/constants";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-[#27272A] bg-[#0A0A0B] mt-28 py-16 text-[#A1A1AA] text-sm">
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Brand Col */}
          <div className="flex flex-col gap-3 md:col-span-2">
            <div className="flex items-center gap-2.5">
              <span className="w-7 h-7 rounded-lg bg-[#10B981] text-[#0A0A0B] flex items-center justify-center text-xs font-black">
                ⚡
              </span>
              <span className="font-extrabold text-base tracking-tight text-white font-sans">
                The Protein Discovery Engine
              </span>
            </div>
            <p className="text-xs text-[#A1A1AA] max-w-md leading-relaxed">
              India&apos;s independent, objective protein intelligence database. We deconstruct product
              formulations mathematically, scan for deceptive maltitol and amino spiking, and rank
              by true economic cost per gram.
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono bg-[#18181B] text-[#E4E4E7] border border-[#27272A]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
                100% Mathematically Audited
              </span>
            </div>
          </div>

          {/* Categories */}
          <div className="flex flex-col gap-3 font-mono">
            <h4 className="text-xs font-bold uppercase tracking-widest text-white">
              Categories
            </h4>
            <ul className="flex flex-col gap-2 text-xs">
              {CATEGORIES.map((cat) => (
                <li key={cat.slug}>
                  <Link
                    href={`/category/${cat.slug}`}
                    className="text-[#A1A1AA] hover:text-[#34D399] transition-colors"
                  >
                    {cat.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Quality Hierarchy */}
          <div className="flex flex-col gap-3 font-mono">
            <h4 className="text-xs font-bold uppercase tracking-widest text-white">
              Quality Tiers
            </h4>
            <ul className="flex flex-col gap-2 text-xs text-[#A1A1AA]/80">
              <li>
                <span className="text-[#E4E4E7]">Tier 1:</span> Pure Isolates (&gt;90%)
              </li>
              <li>
                <span className="text-[#E4E4E7]">Tier 2:</span> Concentrates (70–80%)
              </li>
              <li>
                <span className="text-[#E4E4E7]">Tier 3:</span> Complete Plant Blends
              </li>
              <li>
                <span className="text-[#E4E4E7]">Tier 4:</span> Incomplete / Fillers
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 border-t border-[#27272A] text-xs font-mono text-[#A1A1AA]/70">
          <p>© {new Date().getFullYear()} The Protein Discovery Engine. All rights reserved.</p>
          <p>Uncompromising transparency for the Indian packaged nutrition market.</p>
        </div>
      </div>
    </footer>
  );
};
