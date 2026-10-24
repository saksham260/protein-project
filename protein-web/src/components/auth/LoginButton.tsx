"use client";

import React, { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/context/AuthContext";

export interface LoginButtonProps {
  className?: string;
  hideTextOnMobile?: boolean;
}

export const LoginButton: React.FC<LoginButtonProps> = ({
  className,
  hideTextOnMobile = false,
}) => {
  const { user, isReady, isAvailable, signInWithGoogle, signOut } = useAuth();
  const [showToast, setShowToast] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const wrapperRef = useRef<HTMLDivElement | null>(null);

  const displayName: string =
    user?.user_metadata?.full_name || user?.user_metadata?.name || user?.email || "Account";
  const firstName = displayName.split(" ")[0];

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    if (user) {
      setMenuOpen((open) => !open);
      return;
    }
    if (isAvailable) {
      void signInWithGoogle();
      return;
    }
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

  // Close the account menu when clicking elsewhere
  useEffect(() => {
    if (!menuOpen) return;
    const onPointerDown = (e: PointerEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) setMenuOpen(false);
    };
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [menuOpen]);

  return (
    <div ref={wrapperRef} className="relative inline-flex items-center">
      <button
        type="button"
        onClick={handleClick}
        aria-label={user ? "Account menu" : "Login with Google"}
        aria-expanded={user ? menuOpen : undefined}
        disabled={!isReady}
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
          {user ? firstName : "Login"}
        </span>
      </button>

      {/* Floating Tooltip / Toast */}
      {showToast && (
        <div className="absolute top-full right-0 mt-2 z-50 whitespace-nowrap px-3 py-1.5 rounded-xl bg-[#1C1916] border border-[#D97706]/40 shadow-[0_8px_24px_rgba(0,0,0,0.8)] text-[#F5F2EB] text-[11px] font-sans flex items-center gap-2 animate-in fade-in slide-in-from-top-1 duration-200">
          <span className="w-2 h-2 rounded-full bg-[#D97706] animate-pulse" />
          <span>Login isn&apos;t set up yet</span>
        </div>
      )}

      {/* Account menu */}
      {user && menuOpen && (
        <div className="absolute top-full right-0 mt-2 z-50 min-w-[200px] rounded-xl bg-[#1C1916] border border-[#332D27] shadow-[0_8px_24px_rgba(0,0,0,0.8)] p-1.5 font-sans">
          <p className="px-3 py-2 text-[11px] text-[#968E85] truncate max-w-[240px]">{user.email}</p>
          <button
            type="button"
            onClick={() => {
              setMenuOpen(false);
              void signOut();
            }}
            className="w-full text-left px-3 py-2 rounded-lg text-xs font-bold text-[#F5F2EB] hover:bg-[#26221E] cursor-pointer"
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );
};
