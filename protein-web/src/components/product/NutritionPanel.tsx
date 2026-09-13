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
    <div className="flex flex-col rounded-2xl overflow-hidden bg-[rgba(18,18,26,0.7)] border border-[rgba(255,255,255,0.08)] backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-[rgba(255,255,255,0.02)] border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex flex-col">
          <span className="text-sm font-bold text-white">Nutritional Facts</span>
          <span className="text-xs text-[var(--text-muted)]">
            {is100g
              ? "Values normalized per 100 grams"
              : `Serving Size: ${variant.serving_size_g}g (${variant.servings_per_pack} servings/pack)`}
          </span>
        </div>
        <span className="text-xs font-mono font-bold text-[var(--accent-emerald)] bg-[rgba(0,212,170,0.1)] px-2.5 py-1 rounded-full border border-[rgba(0,212,170,0.25)]">
          {is100g ? "Per 100g" : "Per Pack"}
        </span>
      </div>

      {/* Primary Highlight Macros Bar */}
      <div className="grid grid-cols-3 divide-x divide-[rgba(255,255,255,0.06)] bg-[rgba(0,212,170,0.04)] border-b border-[rgba(255,255,255,0.06)] p-3 text-center">
        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--text-faint)]">
            Calories
          </span>
          <span className="text-lg font-black font-mono text-white">
            {val(variant.calories_kcal, 0)}
            <span className="text-xs font-normal text-[var(--text-muted)] ml-0.5">kcal</span>
          </span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--accent-emerald)] font-bold">
            Protein
          </span>
          <span className="text-lg font-black font-mono text-[#00d4aa]">
            {val(variant.protein_g)}
            <span className="text-xs font-normal text-[var(--accent-emerald)] ml-0.5">g</span>
          </span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--accent-purple)] font-bold">
            True Net Carbs
          </span>
          <span className="text-lg font-black font-mono text-[#c084fc]">
            {val(variant.true_net_carbs_g)}
            <span className="text-xs font-normal text-[var(--text-muted)] ml-0.5">g</span>
          </span>
        </div>
      </div>

      {/* Detailed Nutrient Breakdown Table */}
      <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.04)] text-xs">
        {/* Total Fat */}
        <div className="flex items-center justify-between px-4 py-2.5 hover:bg-[rgba(255,255,255,0.02)]">
          <span className="font-bold text-white">Total Fat</span>
          <span className="font-mono text-[var(--text-secondary)]">{val(variant.total_fat_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span>Saturated Fat</span>
          <span className="font-mono">{val(variant.saturated_fat_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span>Trans Fat</span>
          <span className="font-mono">{val(variant.trans_fat_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span>Cholesterol</span>
          <span className="font-mono">{val(variant.cholesterol_mg, 0)}mg</span>
        </div>

        {/* Carbohydrates */}
        <div className="flex items-center justify-between px-4 py-2.5 hover:bg-[rgba(255,255,255,0.02)]">
          <span className="font-bold text-white">Total Carbohydrates</span>
          <span className="font-mono text-[var(--text-secondary)]">
            {val(variant.total_carbs_g)}g
          </span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span>Dietary Fiber</span>
          <span className="font-mono">{val(variant.dietary_fiber_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span>Total Sugars</span>
          <span className="font-mono">{val(variant.total_sugars_g)}g</span>
        </div>
        <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
          <span className="text-[var(--accent-amber)] font-medium">Added Sugars</span>
          <span className="font-mono text-[var(--accent-amber)]">{val(variant.added_sugars_g)}g</span>
        </div>
        {variant.non_glycemic_polyols_g !== undefined && variant.non_glycemic_polyols_g > 0 && (
          <div className="flex items-center justify-between px-6 py-2 bg-[rgba(255,255,255,0.01)] text-[var(--text-muted)]">
            <span>Non-Glycemic Polyols (Erythritol)</span>
            <span className="font-mono">{val(variant.non_glycemic_polyols_g)}g</span>
          </div>
        )}

        {/* Sodium */}
        <div className="flex items-center justify-between px-4 py-2.5 hover:bg-[rgba(255,255,255,0.02)]">
          <span className="font-bold text-white">Sodium</span>
          <span className="font-mono text-[var(--text-secondary)]">{val(variant.sodium_mg, 0)}mg</span>
        </div>
      </div>
    </div>
  );
};
