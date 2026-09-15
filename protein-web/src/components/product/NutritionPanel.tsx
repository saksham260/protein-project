import React from "react";
import { ProductVariant } from "@/types/product";
import { computePer100g } from "@/lib/utils";
import { NutritionMode } from "./NutritionToggle";

export interface NutritionPanelProps {
  variant: ProductVariant;
  mode: NutritionMode;
}

export const NutritionPanel: React.FC<NutritionPanelProps> = ({ variant, mode }) => {
  const is100g = mode === "per_100g";
  const weight = variant.net_weight_g || 100;

  const val = (num: number | null | undefined, decimals = 1): string => {
    if (num === null || num === undefined) return "—";
    const computed = is100g ? computePer100g(num, weight) : num;
    return computed.toFixed(decimals);
  };

  return (
    <div className="flex flex-col rounded-3xl overflow-hidden bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
      {/* Header */}
      <div className="flex items-center justify-between p-5 border-b border-[#27272A]">
        <div className="flex flex-col">
          <span className="text-sm font-bold text-white tracking-tight">
            Nutritional Deck
          </span>
          <span className="text-xs font-mono text-[#A1A1AA] mt-0.5">
            {is100g
              ? "Standardized benchmark per 100g"
              : `Serving: ${variant.serving_size_g}g (${variant.servings_per_pack || 1} serving/pack)`}
          </span>
        </div>
        <span className="text-xs font-mono font-bold text-[#E4E4E7] bg-[#27272A] px-3 py-1 rounded-full border border-[#3F3F46]">
          {is100g ? "100g Normalized" : "Single Pack"}
        </span>
      </div>

      {/* Primary Highlight Macros Bar */}
      <div className="grid grid-cols-3 divide-x divide-[#27272A] bg-[#27272A]/60 border-b border-[#27272A] p-5 text-center">
        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-widest text-[#A1A1AA]">
            Energy
          </span>
          <span className="text-2xl font-black font-mono text-white mt-1">
            {val(variant.calories_kcal, 0)}
            <span className="text-xs font-normal text-[#A1A1AA] ml-1 font-mono">kcal</span>
          </span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-widest text-[#34D399] font-bold">
            Pure Protein
          </span>
          <span className="text-2xl font-black font-mono text-[#10B981] mt-1">
            {val(variant.protein_g)}
            <span className="text-xs font-normal text-[#34D399] ml-1 font-mono">g</span>
          </span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-widest text-[#A1A1AA]">
            True Net Carbs
          </span>
          <span className="text-2xl font-black font-mono text-white mt-1">
            {val(variant.true_net_carbs_g)}
            <span className="text-xs font-normal text-[#A1A1AA] ml-1 font-mono">g</span>
          </span>
        </div>
      </div>

      {/* Detailed Breakdown List */}
      <div className="flex flex-col divide-y divide-[#27272A]/60 text-xs font-mono">
        {/* Total Fat */}
        <div className="flex items-center justify-between px-5 py-3 hover:bg-[#27272A]/30 transition-colors">
          <span className="font-bold text-white">Total Fat</span>
          <span className="text-[#E4E4E7] font-semibold">{val(variant.total_fat_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span>Saturated Fat</span>
          <span>{val(variant.saturated_fat_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span>Trans Fat</span>
          <span className={Number(val(variant.trans_fat_g)) > 0 ? "text-[#EF4444] font-bold" : ""}>
            {val(variant.trans_fat_g)}g
          </span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span>Cholesterol</span>
          <span>{val(variant.cholesterol_mg, 0)}mg</span>
        </div>

        {/* Carbohydrates */}
        <div className="flex items-center justify-between px-5 py-3 hover:bg-white/[0.02]">
          <span className="font-bold text-white">Total Carbohydrates</span>
          <span className="text-[#E4E4E7] font-semibold">{val(variant.total_carbs_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span>Dietary Fiber</span>
          <span>{val(variant.dietary_fiber_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span>Total Sugars</span>
          <span>{val(variant.total_sugars_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-8 py-2 text-[#A1A1AA]">
          <span className="text-[#A1A1AA]">Added Sugars</span>
          <span className={Number(val(variant.added_sugars_g)) > 0 ? "text-[#EF4444]" : ""}>
            {val(variant.added_sugars_g)}g
          </span>
        </div>
        {variant.non_glycemic_polyols_g !== undefined && variant.non_glycemic_polyols_g > 0 && (
          <div className="flex items-center justify-between px-8 py-2 text-zinc-400">
            <span>Non-Glycemic Polyols (Erythritol)</span>
            <span>{val(variant.non_glycemic_polyols_g)}g</span>
          </div>
        )}

        {/* Sodium */}
        <div className="flex items-center justify-between px-5 py-3 hover:bg-white/[0.02]">
          <span className="font-bold text-white">Sodium</span>
          <span className="text-zinc-300 font-semibold">{val(variant.sodium_mg, 0)}mg</span>
        </div>
      </div>
    </div>
  );
};
