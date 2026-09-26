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
    <div className="flex flex-col gap-2.5">
      <span className="text-xs font-mono uppercase tracking-widest text-zinc-400 font-bold">
        Select Variant / Size
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
                "flex items-center gap-2.5 px-4 py-2.5 rounded-2xl text-xs font-mono border transition-all cursor-pointer select-none",
                isSelected
                  ? "bg-[#10B981]/15 text-white border-[#10B981] shadow-[0_0_15px_rgba(16,185,129,0.2)] ring-1 ring-[#10B981]"
                  : "bg-[#18181B] text-[#A1A1AA] border-[#27272A] hover:border-[#3F3F46] hover:text-white"
              )}
            >
              <span className="font-bold text-white">{v.variant_name}</span>
              <span className="text-zinc-500">
                {formatWeight(v.net_weight_g)}
              </span>
              <span className={isSelected ? "text-[#34D399] font-black" : "text-[#A1A1AA] font-bold"}>
                {formatPrice(v.mrp_inr)}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
