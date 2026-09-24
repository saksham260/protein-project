import React from "react";
import { cn } from "@/lib/utils";

export interface OversizedMetricProps {
  label: string;
  value: string | number;
  unit?: string;
  prefix?: string;
  subtext?: string;
  size?: "sm" | "md" | "lg" | "xl";
  accent?: "white" | "neon" | "crimson" | "muted" | "orange";
  labelClassName?: string;
  align?: "left" | "center";
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
  labelClassName,
  align = "left",
  className,
}) => {
  const strVal = String(value);
  const isLong = strVal.length >= 5;
  const isMedium = strVal.length === 4;

  const sizeStyles = {
    sm: {
      value: isLong ? "text-sm sm:text-base" : isMedium ? "text-base sm:text-lg" : "text-lg sm:text-xl",
      label: "text-[10px]",
      unit: "text-xs",
    },
    md: {
      value: isLong ? "text-lg sm:text-xl" : isMedium ? "text-xl sm:text-2xl" : "text-2xl sm:text-3xl",
      label: "text-[10px]",
      unit: "text-xs sm:text-sm",
    },
    lg: {
      value: isLong ? "text-2xl sm:text-3xl" : "text-4xl sm:text-5xl",
      label: "text-xs",
      unit: "text-base",
    },
    xl: {
      value: isLong ? "text-4xl sm:text-5xl" : "text-5xl sm:text-6xl",
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
    orange: "text-[#F59E0B]",
  };

  const conf = sizeStyles[size];
  const isCenter = align === "center";

  return (
    <div className={cn("flex flex-col select-none min-w-0", isCenter && "items-center text-center", className)}>
      <span
        className={cn(
          "uppercase font-mono tracking-widest font-medium mb-1 truncate",
          labelClassName || "text-zinc-500",
          conf.label
        )}
      >
        {label}
      </span>
      <div className={cn("flex items-baseline gap-0.5 font-mono whitespace-nowrap", isCenter && "justify-center")}>
        {prefix && (
          <span className={cn("font-bold font-mono shrink-0", conf.unit, accent === "white" ? "text-white" : "text-zinc-400")}>
            {prefix}
          </span>
        )}
        <span className={cn("font-black tracking-tight font-mono whitespace-nowrap leading-none", conf.value, accentColors[accent])}>
          {value}
        </span>
        {unit && (
          <span className={cn("font-medium text-zinc-400 font-mono ml-0.5 shrink-0", conf.unit)}>
            {unit}
          </span>
        )}
      </div>
      {subtext && (
        <span className={cn("text-[11px] font-mono text-zinc-500 mt-1 truncate", isCenter && "text-center")}>
          {subtext}
        </span>
      )}
    </div>
  );
};
