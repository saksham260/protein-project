import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger" | "neon";
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
      "inline-flex items-center justify-center font-mono font-bold rounded-full transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:pointer-events-none select-none text-center";

    const variantStyles: Record<string, string> = {
      primary:
        "bg-[#10B981] text-black hover:bg-[#34D399] active:scale-[0.98] shadow-[0_0_20px_rgba(16,185,129,0.25)]",
      neon:
        "bg-[#10B981] text-black hover:bg-[#34D399] active:scale-[0.98] shadow-[0_0_20px_rgba(16,185,129,0.25)]",
      secondary:
        "bg-[#18181B] text-[#E4E4E7] hover:bg-[#27272A] border border-[#27272A] active:scale-[0.98]",
      outline:
        "bg-transparent text-[#E4E4E7] border border-[#27272A] hover:border-[#3F3F46] hover:bg-[#18181B] active:scale-[0.98]",
      ghost:
        "bg-transparent text-[#A1A1AA] hover:text-[#E4E4E7] hover:bg-[#18181B] active:scale-[0.98]",
      danger:
        "bg-[#EF4444] text-white hover:bg-[#DC2626] active:scale-[0.98] shadow-[0_0_20px_rgba(239,68,68,0.25)]",
    };

    const sizeStyles: Record<string, string> = {
      sm: "text-xs px-3.5 py-1.5 gap-1.5",
      md: "text-xs sm:text-sm px-5 py-2.5 gap-2",
      lg: "text-sm sm:text-base px-6 py-3.5 gap-2.5",
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
