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
          "flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#18181B] hover:bg-[#27272A] border border-[#27272A] hover:border-[#3F3F46] text-[#E4E4E7] hover:text-white transition-all text-xs font-mono font-medium shadow-sm active:scale-95 cursor-pointer",
          className
        )}
      >
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-[#10B981]"
        >
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span className="hidden sm:inline">Login</span>
      </button>

      {/* Floating Tooltip / Toast */}
      {showToast && (
        <div className="absolute top-full right-0 mt-2 z-50 whitespace-nowrap px-3 py-1.5 rounded-xl bg-[#18181B] border border-[#10B981]/40 shadow-[0_8px_24px_rgba(0,0,0,0.8)] text-white text-[11px] font-sans flex items-center gap-2 animate-in fade-in slide-in-from-top-1 duration-200">
          <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse" />
          <span>Coming soon — Login with Google</span>
        </div>
      )}
    </div>
  );
};
