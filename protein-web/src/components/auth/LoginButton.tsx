"use client";

import React, { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";

export interface LoginButtonProps {
  className?: string;
  hideTextOnMobile?: boolean;
}

export const LoginButton: React.FC<LoginButtonProps> = ({
  className,
  hideTextOnMobile = false,
}) => {
  const [showToast, setShowToast] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowToast(true);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      setShowToast(false);
    }, 2800);
  };

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  return (
    <div className="relative inline-flex items-center">
      <button
        type="button"
        onClick={handleClick}
        aria-label="Account Login"
        className={cn(
          "group flex items-center gap-1.5 sm:gap-2 min-h-[36px] sm:min-h-[34px] rounded-xl text-xs sm:text-sm font-sans font-bold tracking-tight whitespace-nowrap cursor-pointer shrink-0 border select-none touch-manipulation",
          hideTextOnMobile ? "max-md:px-2.5 px-3 sm:px-4" : "px-2.5 sm:px-4",
          "bg-[#1C1916]/85 text-[#968E85] border-[#332D27]",
          "md:hover:bg-[#26221E] md:hover:text-[#F5F2EB] md:hover:border-[#D97706]/50 md:hover:shadow-[0_0_16px_rgba(217,119,6,0.18),0_2px_8px_rgba(0,0,0,0.4)]",
          "active:scale-[0.98]",
          "transition-all duration-300 ease-out",
          className
        )}
      >
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="transition-colors duration-300 text-[#968E85] md:group-hover:text-[#D97706] shrink-0"
        >
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span
          className={cn(
            "tracking-tight transition-colors duration-300 font-bold",
            hideTextOnMobile ? "max-md:hidden" : "inline"
          )}
        >
          Login
        </span>
      </button>

      {/* Floating Tooltip / Toast */}
      {showToast && (
        <div className="absolute top-full right-0 mt-2 z-50 whitespace-nowrap px-3 py-1.5 rounded-xl bg-[#1C1916] border border-[#D97706]/40 shadow-[0_8px_24px_rgba(0,0,0,0.8)] text-[#F5F2EB] text-[11px] font-sans flex items-center gap-2 animate-in fade-in slide-in-from-top-1 duration-200">
          <span className="w-2 h-2 rounded-full bg-[#D97706] animate-pulse" />
          <span>Coming soon — Login with Google</span>
        </div>
      )}
    </div>
  );
};
