"use client";

import React, { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";

export interface LoginButtonProps {
  className?: string;
}

export const LoginButton: React.FC<LoginButtonProps> = ({ className }) => {
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
          "group flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 min-h-[36px] sm:min-h-[34px] rounded-xl text-xs sm:text-sm font-sans font-bold tracking-tight whitespace-nowrap transition-all duration-200 cursor-pointer shrink-0 border active:scale-95 touch-manipulation select-none bg-[#1C1916]/85 text-[#968E85] border-[#332D27] hover:bg-[#D97706] hover:border-[#D97706] hover:!text-white",
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
          className="transition-colors text-inherit group-hover:!text-white shrink-0"
        >
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span className="tracking-tight text-inherit group-hover:!text-white font-bold">Login</span>
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
