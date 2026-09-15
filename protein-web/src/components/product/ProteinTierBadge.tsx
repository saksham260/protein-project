import React from "react";
import { PROTEIN_TIERS } from "@/lib/constants";
import { ProteinTier } from "@/types/product";
import { cn } from "@/lib/utils";

export interface ProteinTierBadgeProps {
  tier: ProteinTier | string | null | undefined;
  size?: "sm" | "md";
  className?: string;
}

export const ProteinTierBadge: React.FC<ProteinTierBadgeProps> = ({
  tier,
  size = "sm",
  className,
}) => {
  if (!tier) {
    return (
      <span className="text-[10px] font-mono uppercase text-zinc-500 tracking-wider">
        Unrated
      </span>
    );
  }

  const tierKey = (tier.startsWith("Tier") ? tier : `Tier ${tier}`) as keyof typeof PROTEIN_TIERS;
  const config = PROTEIN_TIERS[tierKey];
  const isTier1 = tierKey === "Tier 1";

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 font-mono select-none rounded-full px-2.5 py-0.5 border transition-colors",
        size === "sm" ? "text-[10px]" : "text-xs px-3 py-1",
        isTier1
          ? "bg-[#10B981]/15 text-[#34D399] border-[#10B981]/30 font-bold shadow-[0_0_12px_rgba(16,185,129,0.2)]"
          : "bg-[#18181B] text-[#E4E4E7] border-[#27272A] font-medium",
        className
      )}
      title={config?.description}
    >
      <span
        className={cn(
          "w-1.5 h-1.5 rounded-full",
          isTier1 ? "bg-[#10B981]" : "bg-zinc-500"
        )}
      />
      <span>{config ? config.badgeLabel : tier}</span>
    </div>
  );
};
