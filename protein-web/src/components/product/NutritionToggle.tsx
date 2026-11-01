"use client";

import React from "react";
import { cn } from "@/lib/utils";

export type NutritionMode = "per_serving" | "per_100g";

export interface NutritionToggleProps {
  mode: NutritionMode;
  onChange: (mode: NutritionMode) => void;
  servingSizeG?: number;
}

export const NutritionToggle: React.FC<NutritionToggleProps> = ({
  mode,
  onChange,
  servingSizeG,
}) => {
  return (
    <div
      role="group"
      aria-label="Nutrition View Options"
      className="inline-flex p-1 rounded-full bg-[#18181B] border border-[#27272A] select-none shadow-[0_2px_10px_rgba(0,0,0,0.5)]"
    >
      <button
        type="button"
        aria-pressed={mode === "per_serving"}
        onClick={() => onChange("per_serving")}
        className={cn(
          "px-4 py-1.5 rounded-full text-xs font-mono font-bold transition-all duration-200 cursor-pointer",
          mode === "per_serving"
            ? "bg-[#10B981] text-[#0A0A0B] shadow-md"
            : "text-[#A1A1AA] hover:text-[#E4E4E7]"
        )}
      >
        Per Serving {servingSizeG ? `(${servingSizeG}g)` : ""}
      </button>

      <button
        type="button"
        aria-pressed={mode === "per_100g"}
        onClick={() => onChange("per_100g")}
        className={cn(
          "px-4 py-1.5 rounded-full text-xs font-mono font-bold transition-all duration-200 cursor-pointer",
          mode === "per_100g"
            ? "bg-[#10B981] text-[#0A0A0B] shadow-md"
            : "text-[#A1A1AA] hover:text-[#E4E4E7]"
        )}
      >
        Per 100g
      </button>
    </div>
  );
};
