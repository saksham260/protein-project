import React from "react";
import { VariantRedFlag } from "@/types/product";
import { cn } from "@/lib/utils";

export interface RedFlagWarningProps {
  flags: VariantRedFlag[] | undefined | null;
  mode?: "compact" | "banner" | "clinical-deck";
  /** False when we have no ingredient list, so finding no flags proves nothing. */
  hasIngredientData?: boolean;
  className?: string;
}

export const RedFlagWarning: React.FC<RedFlagWarningProps> = ({
  flags = [],
  mode = "compact",
  hasIngredientData = true,
  className,
}) => {
  const flagList = flags || [];
  const hasFlags = flagList.length > 0;

  if (mode === "compact") {
    if (!hasFlags) {
      return (
        <span className={cn("inline-flex items-center gap-1.5 text-xs font-mono font-medium text-zinc-400", className)}>
          <span className="w-2 h-2 rounded-full bg-zinc-600" />
          <span>0 Red Flags</span>
        </span>
      );
    }

    return (
      <span className={cn("inline-flex items-center gap-1.5 text-xs font-mono font-bold text-[#F87171]", className)}>
        <span className="w-2 h-2 rounded-full bg-[#EF4444] animate-pulse" />
        <span>{flagList.length} Red Flag{flagList.length > 1 ? "s" : ""}</span>
      </span>
    );
  }

  if (mode === "banner") {
    if (!hasFlags) {
      return (
        <div
          className={cn(
            "flex items-start gap-4 p-5 rounded-2xl bg-[#18181B] border border-[#27272A] shadow-[0_8px_30px_rgba(0,0,0,0.5)]",
            className
          )}
        >
          <div className="w-9 h-9 rounded-xl bg-[#27272A] border border-[#3F3F46] flex items-center justify-center text-base shrink-0 text-[#34D399]">
            🛡️
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-bold text-white tracking-tight">
              {hasIngredientData ? "No Red Flags on the Label" : "Ingredient List Not Available"}
            </span>
            <p className="text-xs text-[#A1A1AA] mt-1 leading-relaxed">
              {hasIngredientData
                ? "No maltitol, added amino acids, hydrogenated or palm fats, or hidden sugars listed."
                : "We have nothing to scan for this product, so check the pack."}
            </p>
          </div>
        </div>
      );
    }

    return (
      <div
        className={cn(
          "flex flex-col gap-3 p-5 rounded-2xl bg-[#18181B] border border-[#EF4444]/30 shadow-[0_8px_30px_rgba(239,68,68,0.08)]",
          className
        )}
      >
        <div className="flex items-center gap-2 text-[#F87171]">
          <span className="w-2.5 h-2.5 rounded-full bg-[#EF4444] shrink-0" />
          <span className="text-sm font-mono font-bold tracking-tight uppercase">
            {flagList.length} Label Warning{flagList.length > 1 ? "s" : ""}
          </span>
        </div>
        <p className="text-xs text-[#A1A1AA] leading-relaxed">
          Flagged from the ingredient list. See the breakdown below.
        </p>
      </div>
    );
  }

  // mode === "clinical-deck"
  if (!hasFlags) {
    return (
      <div className={cn("p-6 rounded-3xl bg-[#18181B] border border-[#27272A] text-center", className)}>
        <span className="text-sm font-mono text-[#A1A1AA]">
          {hasIngredientData
            ? "No red flags found in this variant's ingredient list."
            : "No ingredient list available, so this variant couldn't be scanned."}
        </span>
      </div>
    );
  }

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      {flagList.map((flag) => (
        <div
          key={flag.id || flag.flag_label}
          className="flex flex-col p-5 rounded-2xl bg-[#18181B] border border-[#EF4444]/25 shadow-[0_8px_24px_rgba(0,0,0,0.6)]"
        >
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#EF4444]" />
              <span className="text-sm font-bold text-white tracking-tight">
                {flag.flag_label}
              </span>
            </div>
            <span className="text-[10px] font-mono uppercase px-2.5 py-0.5 rounded-full bg-[#EF4444]/10 text-[#F87171] border border-[#EF4444]/20">
              {flag.flag_severity} Severity
            </span>
          </div>

          <p className="text-xs text-[#E4E4E7] mt-2.5 leading-relaxed font-sans">
            {flag.flag_description}
          </p>

          {flag.matched_ingredient && (
            <div className="mt-3 pt-3 border-t border-[#27272A] flex items-center justify-between text-[11px] font-mono">
              <span className="text-[#A1A1AA] uppercase">Matched Ingredient</span>
              <span className="text-[#EF4444] font-semibold">
                {flag.matched_ingredient} {flag.ins_number ? `(INS ${flag.ins_number})` : ""}
              </span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
