"use client";

import React from "react";
import { ProductVariant } from "@/types/product";
import { formatPrice, formatWeight, cn } from "@/lib/utils";

export interface VariantSelectorProps {
  variants: ProductVariant[];
  selectedIndex: number;
  onSelectIndex: (index: number) => void;
}

export const VariantSelector: React.FC<VariantSelectorProps> = ({
  variants,
  selectedIndex,
  onSelectIndex,
}) => {
  if (!variants || variants.length <= 1) {
    return null;
  }

  return (
    <div className="flex flex-col gap-2">
      <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
        Select Variant / Size:
      </span>
      <div className="flex flex-wrap gap-2.5">
        {variants.map((v, idx) => {
          const isSelected = idx === selectedIndex;
          return (
            <button
              key={v.id || idx}
              type="button"
              onClick={() => onSelectIndex(idx)}
              className={cn(
                "flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium border transition-all cursor-pointer select-none",
                isSelected
                  ? "bg-[rgba(0,212,170,0.15)] text-white border-[var(--accent-emerald)] shadow-md shadow-[rgba(0,212,170,0.15)] ring-1 ring-[var(--accent-emerald)]"
                  : "bg-[rgba(255,255,255,0.03)] text-[var(--text-secondary)] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.2)] hover:text-white"
              )}
            >
              <span className="font-bold">{v.variant_name}</span>
              <span className="text-[var(--text-faint)] font-mono">
                {formatWeight(v.net_weight_g)}
              </span>
              <span className="text-[var(--accent-emerald)] font-mono font-bold">
                {formatPrice(v.mrp_inr)}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
