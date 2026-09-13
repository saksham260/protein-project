"use client";

import React from "react";
import { cn } from "@/lib/utils";

export type NutritionMode = "per_pack" | "per_100g";

export interface NutritionToggleProps {
  mode: NutritionMode;
  onChange: (mode: NutritionMode) => void;
  packWeightG?: number;
}

export const NutritionToggle: React.FC<NutritionToggleProps> = ({
  mode,
  onChange,
  packWeightG,
}) => {
  return (
    <div className="inline-flex p-1 rounded-xl bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.08)] select-none">
      <button
        type="button"
        onClick={() => onChange("per_pack")}
        className={cn(
          "px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer",
          mode === "per_pack"
            ? "bg-[var(--accent-emerald)] text-[#0a0a0f] shadow-md shadow-[rgba(0,212,170,0.25)]"
            : "text-[var(--text-muted)] hover:text-white"
        )}
      >
        Per Pack {packWeightG ? `(${packWeightG}g)` : ""}
      </button>

      <button
        type="button"
        onClick={() => onChange("per_100g")}
        className={cn(
          "px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer",
          mode === "per_100g"
            ? "bg-[var(--accent-emerald)] text-[#0a0a0f] shadow-md shadow-[rgba(0,212,170,0.25)]"
            : "text-[var(--text-muted)] hover:text-white"
        )}
      >
        Per 100g
      </button>
    </div>
  );
};
