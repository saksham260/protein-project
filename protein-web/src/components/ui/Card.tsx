import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  href?: string;
  hoverEffect?: boolean;
  padding?: "none" | "sm" | "md" | "lg";
  glow?: boolean;
}

export const Card: React.FC<CardProps> = ({
  className,
  href,
  hoverEffect = false,
  padding = "md",
  glow = false,
  children,
  ...props
}) => {
  const paddingStyles: Record<string, string> = {
    none: "p-0",
    sm: "p-3 sm:p-4",
    md: "p-4 sm:p-6",
    lg: "p-6 sm:p-8",
  };

  const baseStyles = cn(
    "relative overflow-hidden rounded-2xl border transition-all duration-300",
    "bg-[rgba(18,18,26,0.7)] backdrop-blur-xl border-[rgba(255,255,255,0.08)]",
    paddingStyles[padding],
    hoverEffect &&
      "hover:border-[rgba(255,255,255,0.18)] hover:bg-[rgba(26,26,38,0.85)] hover:-translate-y-1 hover:shadow-xl hover:shadow-[rgba(0,0,0,0.5)] cursor-pointer",
    glow && "border-[rgba(0,212,170,0.3)] shadow-[0_0_20px_rgba(0,212,170,0.12)]",
    className
  );

  if (href) {
    return (
      <Link href={href} className={baseStyles} style={{ textDecoration: "none", display: "block" }}>
        {children}
      </Link>
    );
  }

  return (
    <div className={baseStyles} {...props}>
      {children}
    </div>
  );
};
