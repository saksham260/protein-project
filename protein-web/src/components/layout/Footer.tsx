import React from "react";
import Link from "next/link";
import { CATEGORIES } from "@/lib/constants";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-[rgba(255,255,255,0.08)] bg-[#0c0c14] mt-24 py-16 text-[var(--text-muted)] text-sm">
      <div className="container flex flex-col gap-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Col */}
          <div className="flex flex-col gap-3 md:col-span-2">
            <div className="flex items-center gap-2">
              <span className="text-xl">⚡</span>
              <span className="font-extrabold text-base tracking-tight text-[var(--text-primary)]">
                The Protein Discovery Engine
              </span>
            </div>
            <p className="text-xs text-[var(--text-secondary)] max-w-md leading-relaxed">
              India&apos;s independent protein transparency catalog. We analyze ingredient decks,
              detect hidden sugars &amp; maltitol, classify protein source tiers, and calculate
              unbiased cost-per-gram metrics.
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[rgba(0,212,170,0.1)] text-[#00d4aa] border border-[rgba(0,212,170,0.25)]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00d4aa]" />
                100% Human Verified Data
              </span>
            </div>
          </div>

          {/* Categories */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-primary)]">
              Categories
            </h4>
            <ul className="flex flex-col gap-2 text-xs">
              {CATEGORIES.map((cat) => (
                <li key={cat.slug}>
                  <Link
                    href={`/category/${cat.slug}`}
                    className="hover:text-[var(--accent-emerald)] transition-colors"
                  >
                    {cat.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Standards & Transparency */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-primary)]">
              Standards
            </h4>
            <ul className="flex flex-col gap-2 text-xs">
              <li>
                <span className="text-[var(--text-faint)]">Tier 1: Pure Isolate &gt;90%</span>
              </li>
              <li>
                <span className="text-[var(--text-faint)]">Tier 2: Concentrates 70–80%</span>
              </li>
              <li>
                <span className="text-[var(--text-faint)]">Tier 3: Plant Blends</span>
              </li>
              <li>
                <span className="text-[var(--text-faint)]">Tier 4: Incomplete / Spiked</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 border-t border-[rgba(255,255,255,0.06)] text-xs text-[var(--text-faint)]">
          <p>© {new Date().getFullYear()} The Protein Discovery Engine. All rights reserved.</p>
          <p>Prices and nutritional formulas are verified against Indian market labels.</p>
        </div>
      </div>
    </footer>
  );
};
