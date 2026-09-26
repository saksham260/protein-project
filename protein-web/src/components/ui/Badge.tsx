import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?:
    | "default"
    | "success"
    | "warning"
    | "danger"
    | "info"
    | "tier1"
    | "tier2"
    | "tier3"
    | "tier4"
    | "clean";
  size?: "sm" | "md";
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = "default",
  size = "sm",
  dot = false,
  children,
  ...props
}) => {
  const baseStyles =
    "inline-flex items-center font-medium rounded-full border select-none transition-colors whitespace-nowrap";

  const sizeStyles: Record<string, string> = {
    sm: "text-[11px] px-2.5 py-0.5 gap-1.5 leading-normal",
    md: "text-xs px-3 py-1 gap-2 leading-normal",
  };

  const variantStyles: Record<string, { className: string; dotColor?: string }> = {
    default: {
      className: "bg-[rgba(255,255,255,0.06)] text-[var(--text-secondary)] border-[var(--border-subtle)]",
      dotColor: "var(--text-muted)",
    },
    success: {
      className: "bg-[rgba(0,212,170,0.12)] text-[#00d4aa] border-[rgba(0,212,170,0.3)]",
      dotColor: "#00d4aa",
    },
    clean: {
      className: "bg-[rgba(0,212,170,0.15)] text-[#00e6b8] border-[rgba(0,212,170,0.4)] font-semibold shadow-sm",
      dotColor: "#00e6b8",
    },
    warning: {
      className: "bg-[rgba(245,158,11,0.12)] text-[#fbbf24] border-[rgba(245,158,11,0.3)]",
      dotColor: "#fbbf24",
    },
    danger: {
      className: "bg-[rgba(239,68,68,0.12)] text-[#f87171] border-[rgba(239,68,68,0.3)]",
      dotColor: "#f87171",
    },
    info: {
      className: "bg-[rgba(56,189,248,0.12)] text-[#38bdf8] border-[rgba(56,189,248,0.3)]",
      dotColor: "#38bdf8",
    },
    tier1: {
      className: "bg-[rgba(0,212,170,0.15)] text-[#00d4aa] border-[rgba(0,212,170,0.35)] font-semibold",
      dotColor: "#00d4aa",
    },
    tier2: {
      className: "bg-[rgba(56,189,248,0.15)] text-[#38bdf8] border-[rgba(56,189,248,0.35)] font-semibold",
      dotColor: "#38bdf8",
    },
    tier3: {
      className: "bg-[rgba(251,191,36,0.15)] text-[#fbbf24] border-[rgba(251,191,36,0.35)] font-semibold",
      dotColor: "#fbbf24",
    },
    tier4: {
      className: "bg-[rgba(248,113,113,0.15)] text-[#f87171] border-[rgba(248,113,113,0.35)] font-semibold",
      dotColor: "#f87171",
    },
  };

  const styleConfig = variantStyles[variant] || variantStyles.default;

  return (
    <span
      className={cn(baseStyles, sizeStyles[size], styleConfig.className, className)}
      {...props}
    >
      {dot && (
        <span
          style={{
            width: "6px",
            height: "6px",
            borderRadius: "50%",
            backgroundColor: styleConfig.dotColor || "currentColor",
            display: "inline-block",
          }}
        />
      )}
      {children}
    </span>
  );
};
