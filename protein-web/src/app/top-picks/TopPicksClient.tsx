"use client";

import React from "react";
import Link from "next/link";
import { AwardCategory } from "@/lib/topPicksConfig";
import { ProductWithVariants } from "@/types/product";
import { AwardProductCard } from "@/components/product/AwardProductCard";
import { CATEGORIES } from "@/lib/constants";

export interface TopPicksClientProps {
  topPicks: Array<{
    award: AwardCategory;
    product: ProductWithVariants;
    editorialBlurb?: string;
  }>;
}

export function TopPicksClient({ topPicks }: TopPicksClientProps) {
  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex flex-col gap-8 sm:gap-10">
      {/* Breadcrumb Navigation */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#968E85]">
        <Link href="/" className="hover:text-[#F5F2EB] transition-colors">
          Home
        </Link>
        <span>/</span>
        <span className="text-[#F5F2EB] font-bold">Top Value Picks</span>
      </nav>

      {/* Hero Header */}
      <div className="flex flex-col gap-4 p-6 sm:p-8 rounded-2xl sm:rounded-3xl bg-[#1C1916] border border-[#332D27] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base">🏆</span>
              <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
                Picked by Formula
              </span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-black text-[#F5F2EB] mt-1 tracking-tight">
              Top Value Picks
            </h1>
            <p className="text-xs sm:text-sm font-mono text-[#968E85] mt-1 max-w-2xl">
              The lowest cost per gram of protein in each category, among in-stock products with no red flags on their
              label. Commissions play no part in these picks.{" "}
              <Link href="/how-we-rate" className="text-[#D97706] hover:underline">
                How we rate
              </Link>
            </p>
          </div>
          <Link
            href="/explore"
            className="px-4 py-2 rounded-full bg-[#1C1916] hover:bg-[#26221E] border border-[#332D27] text-xs font-mono text-[#F5F2EB] hover:text-white transition-colors self-start sm:self-auto shrink-0"
          >
            Explore All Catalog →
          </Link>
        </div>
      </div>

      {/* Award Grid */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between pb-2 border-b border-[#332D27]/80">
          <span className="text-xs font-mono uppercase tracking-wider text-[#968E85]">
            Category Winners ({topPicks.length})
          </span>
          <span className="text-xs font-mono text-[#D97706]">
            No label red flags
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3.5 sm:gap-6 items-stretch pt-2">
          {topPicks.map(({ award, product, editorialBlurb }) => (
            <AwardProductCard
              key={award.id}
              award={award}
              product={product}
              editorialBlurb={editorialBlurb}
            />
          ))}
        </div>
      </div>

      {/* Category Exploration Shortcuts */}
      <section className="flex flex-col gap-4 pt-6 border-t border-[#332D27]/80">
        <div>
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
            Explore by Form Factor
          </span>
          <h2 className="text-xl sm:text-2xl font-black text-[#F5F2EB] mt-0.5 tracking-tight">
            Inspect Full Categories with Filters & Sorting
          </h2>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
          {CATEGORIES.map((cat) => (
            <Link
              key={cat.slug}
              href={`/category/${cat.slug}`}
              className="p-4 rounded-2xl bg-[#1C1916] border border-[#332D27] hover:border-[#D97706]/70 transition-all flex flex-col gap-1.5 group"
            >
              <div className="flex items-center justify-between">
                <span className="text-2xl">{cat.icon}</span>
                <span className="text-xs text-[#968E85] group-hover:text-[#D97706] group-hover:translate-x-0.5 transition-all">→</span>
              </div>
              <span className="text-sm font-bold text-[#F5F2EB] group-hover:text-[#D97706] transition-colors mt-1">
                {cat.name}
              </span>
              <span className="text-[11px] font-mono text-[#968E85] line-clamp-1">
                {cat.description}
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
