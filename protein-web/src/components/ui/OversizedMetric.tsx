import React from "react";
import { cn } from "@/lib/utils";

export interface OversizedMetricProps {
  label: string;
  value: string | number;
  unit?: string;
  prefix?: string;
  subtext?: string;
  size?: "sm" | "md" | "lg" | "xl";
  accent?: "white" | "neon" | "crimson" | "muted";
  className?: string;
}

export const OversizedMetric: React.FC<OversizedMetricProps> = ({
  label,
  value,
  unit,
  prefix,
  subtext,
  size = "md",
  accent = "white",
  className,
}) => {
  const sizeStyles = {
    sm: {
      value: "text-2xl sm:text-3xl",
      label: "text-[10px]",
      unit: "text-xs",
    },
    md: {
      value: "text-3xl sm:text-4xl",
      label: "text-[11px]",
      unit: "text-sm",
    },
    lg: {
      value: "text-4xl sm:text-5xl",
      label: "text-xs",
      unit: "text-base",
    },
    xl: {
      value: "text-5xl sm:text-6xl",
      label: "text-xs",
      unit: "text-lg",
    },
  };

  const accentColors = {
    white: "text-white",
    neon: "text-[#10B981]",
    emerald: "text-[#10B981]",
    crimson: "text-[#EF4444]",
    danger: "text-[#EF4444]",
    muted: "text-[#A1A1AA]",
  };

  const conf = sizeStyles[size];

  return (
    <div className={cn("flex flex-col select-none", className)}>
      <span className={cn("uppercase font-mono tracking-widest text-zinc-500 font-medium mb-1", conf.label)}>
        {label}
      </span>
      <div className="flex items-baseline gap-1 font-mono">
        {prefix && (
          <span className={cn("font-bold text-zinc-400 font-mono", conf.unit)}>
            {prefix}
          </span>
        )}
        <span className={cn("font-black tracking-tight font-mono", conf.value, accentColors[accent])}>
          {value}
        </span>
        {unit && (
          <span className={cn("font-medium text-zinc-400 font-mono ml-0.5", conf.unit)}>
            {unit}
          </span>
        )}
      </div>
      {subtext && (
        <span className="text-[11px] font-mono text-zinc-500 mt-1">
          {subtext}
        </span>
      )}
    </div>
  );
};
