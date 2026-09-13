import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger" | "emerald";
  size?: "sm" | "md" | "lg";
  href?: string;
  target?: string;
  rel?: string;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      href,
      target,
      rel,
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:pointer-events-none select-none text-center";

    const variantStyles: Record<string, string> = {
      primary:
        "bg-[var(--accent-emerald)] text-[#0a0a0f] hover:brightness-110 active:scale-[0.98] shadow-md shadow-[rgba(0,212,170,0.2)] font-semibold",
      emerald:
        "bg-[var(--accent-emerald)] text-[#0a0a0f] hover:brightness-110 active:scale-[0.98] shadow-md shadow-[rgba(0,212,170,0.2)] font-semibold",
      secondary:
        "bg-[var(--bg-elevated)] text-[var(--text-primary)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-subtle)] hover:border-[var(--border-strong)] active:scale-[0.98]",
      outline:
        "bg-transparent text-[var(--text-primary)] border border-[var(--border-strong)] hover:border-[var(--accent-emerald)] hover:text-[var(--accent-emerald)] active:scale-[0.98]",
      ghost:
        "bg-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.06)] active:scale-[0.98]",
      danger:
        "bg-[var(--accent-red)] text-white hover:brightness-110 active:scale-[0.98] shadow-md shadow-[rgba(239,68,68,0.25)]",
    };

    const sizeStyles: Record<string, string> = {
      sm: "text-xs px-3 py-1.5 gap-1.5",
      md: "text-sm px-4 py-2.5 gap-2",
      lg: "text-base px-6 py-3.5 gap-2.5",
    };

    const content = (
      <>
        {isLoading && (
          <span
            style={{
              width: "14px",
              height: "14px",
              border: "2px solid currentColor",
              borderRightColor: "transparent",
              borderRadius: "50%",
              display: "inline-block",
              animation: "spin 0.7s linear infinite",
            }}
          />
        )}
        {!isLoading && leftIcon && <span className="icon-left">{leftIcon}</span>}
        <span>{children}</span>
        {!isLoading && rightIcon && <span className="icon-right">{rightIcon}</span>}
      </>
    );

    const combinedClassName = cn(
      baseStyles,
      variantStyles[variant],
      sizeStyles[size],
      className
    );

    if (href) {
      return (
        <Link
          href={href}
          target={target}
          rel={rel}
          className={combinedClassName}
          style={{ textDecoration: "none" }}
        >
          {content}
        </Link>
      );
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={combinedClassName}
        {...props}
      >
        {content}
      </button>
    );
  }
);

Button.displayName = "Button";
