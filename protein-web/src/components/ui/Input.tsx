import React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, leftIcon, rightIcon, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]"
          >
            {label}
          </label>
        )}
        <div className="relative flex items-center w-full">
          {leftIcon && (
            <div className="absolute left-3.5 flex items-center pointer-events-none text-[var(--text-muted)]">
              {leftIcon}
            </div>
          )}
          <input
            id={inputId}
            ref={ref}
            className={cn(
              "w-full rounded-xl px-4 py-2.5 text-sm transition-all duration-200",
              "bg-[var(--bg-input)] text-[var(--text-primary)] placeholder-[var(--text-faint)]",
              "border border-[var(--border-subtle)] focus:outline-none focus:border-[var(--accent-emerald)] focus:ring-1 focus:ring-[var(--accent-emerald)]",
              leftIcon ? "pl-10" : "",
              rightIcon ? "pr-10" : "",
              error ? "border-[var(--accent-red)] focus:border-[var(--accent-red)] focus:ring-[var(--accent-red)]" : "",
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className="absolute right-3.5 flex items-center text-[var(--text-muted)]">
              {rightIcon}
            </div>
          )}
        </div>
        {error && <span className="text-xs text-[var(--accent-red)]">{error}</span>}
      </div>
    );
  }
);

Input.displayName = "Input";
