import React from "react";
import { formatPricePerGram, formatPercentage, cn } from "@/lib/utils";

export interface EfficiencyMeterProps {
  costPerGram: number | null | undefined;
  proteinDensityPct: number | null | undefined;
  compact?: boolean;
}

export const EfficiencyMeter: React.FC<EfficiencyMeterProps> = ({
  costPerGram,
  proteinDensityPct,
  compact = false,
}) => {
  // Determine cost efficiency color badge
  const getCostColorClass = (cost: number | null | undefined) => {
    if (!cost) return "text-[var(--text-muted)]";
    if (cost < 3.5) return "text-[#00d4aa]"; // Very economical
    if (cost < 6.0) return "text-[#38bdf8]"; // Good value
    if (cost < 10.0) return "text-[#fbbf24]"; // Moderate
    return "text-[#f87171]"; // Premium / Expensive
  };

  const density = proteinDensityPct ?? 0;
  // Cap at 100%
  const densityBarWidth = Math.min(Math.max(density, 0), 100);

  if (compact) {
    return (
      <div className="flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-1.5">
          <span className="text-[var(--text-muted)]">Cost/g:</span>
          <span className={cn("font-bold font-mono", getCostColorClass(costPerGram))}>
            {formatPricePerGram(costPerGram)}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[var(--text-muted)]">Density:</span>
          <span className="font-semibold text-[var(--text-primary)]">
            {formatPercentage(proteinDensityPct)}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2 p-3 rounded-xl bg-[rgba(255,255,255,0.03)] border border-[var(--border-subtle)]">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-[var(--text-muted)]">Efficiency (₹/g)</span>
        <span className={cn("text-base font-bold font-mono", getCostColorClass(costPerGram))}>
          {formatPricePerGram(costPerGram)}
        </span>
      </div>

      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between text-xs">
          <span className="text-[var(--text-muted)]">Protein Density</span>
          <span className="font-semibold text-[var(--text-primary)]">
            {formatPercentage(proteinDensityPct)}
          </span>
        </div>
        <div className="w-full h-1.5 rounded-full bg-[rgba(255,255,255,0.08)] overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-500 bg-gradient-to-r from-[var(--accent-purple)] to-[var(--accent-emerald)]"
            style={{ width: `${densityBarWidth}%` }}
          />
        </div>
      </div>
    </div>
  );
};
