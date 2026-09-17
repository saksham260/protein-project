"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { CATEGORIES } from "@/lib/constants";
import { Button } from "@/components/ui/Button";
import { useCart } from "@/context/CartContext";

export interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileNav: React.FC<MobileNavProps> = ({ isOpen, onClose }) => {
  const { itemCount, openCart } = useCart();
  const [showLoginToast, setShowLoginToast] = useState(false);

  // Lock body scroll when mobile nav is open
  useEffect(() => {
    if (!isOpen) return;
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = originalOverflow;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 flex flex-col justify-between bg-[#0A0A0B]/95 backdrop-blur-2xl p-5 md:hidden animate-fade-in overflow-y-auto select-none cursor-pointer"
      aria-modal="true"
      role="dialog"
    >
      <div
        className="flex flex-col gap-4 max-h-full"
        onClick={(e) => {
          if (e.target === e.currentTarget) onClose();
        }}
      >
        {/* Header with Close Button */}
        <div
          className="flex items-center justify-between border-b border-[#27272A] pb-3"
          onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
          }}
        >
          <Link
            href="/"
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            className="flex items-center gap-2.5 cursor-pointer"
          >
            <span className="w-8 h-8 rounded-xl bg-[#10B981] text-[#0A0A0B] flex items-center justify-center text-sm font-black shadow-[0_0_16px_rgba(16,185,129,0.35)]">
              ⚡
            </span>
            <span className="font-extrabold text-base tracking-tight text-white font-sans">
              Protein Engine
            </span>
          </Link>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            aria-label="Close menu"
            className="w-8 h-8 rounded-full bg-[#18181B] border border-[#27272A] flex items-center justify-center text-[#A1A1AA] hover:text-white text-sm cursor-pointer active:scale-95"
          >
            ✕
          </button>
        </div>

        {/* User Quick Actions (Shortlist & Login) */}
        <div className="grid grid-cols-2 gap-2 font-mono">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onClose();
              openCart();
            }}
            className="flex items-center justify-center gap-2 p-3 rounded-2xl bg-[#18181B] border border-[#27272A] text-white text-xs font-bold active:scale-[0.98] transition-all"
          >
            <span>🛒 Shortlist</span>
            {itemCount > 0 && (
              <span className="px-1.5 py-0.5 rounded-full bg-[#10B981] text-[#0A0A0B] text-[10px] font-black">
                {itemCount}
              </span>
            )}
          </button>

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setShowLoginToast(true);
              setTimeout(() => setShowLoginToast(false), 2500);
            }}
            className="flex items-center justify-center gap-2 p-3 rounded-2xl bg-[#18181B] border border-[#27272A] text-[#E4E4E7] text-xs font-medium active:scale-[0.98] transition-all relative"
          >
            <span>👤 Login</span>
            {showLoginToast && (
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap px-2.5 py-1 rounded-lg bg-[#18181B] border border-[#10B981]/50 text-[10px] text-white shadow-lg">
                Coming soon
              </span>
            )}
          </button>
        </div>

        {/* Navigation Links */}
        <nav
          className="flex flex-col gap-2.5 font-mono"
          onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
          }}
        >
          <Link
            href="/explore"
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            className="flex items-center justify-between p-3 rounded-2xl bg-[#18181B] border border-[#27272A] hover:border-[#3F3F46] text-[#E4E4E7] font-bold text-sm cursor-pointer active:scale-[0.98] transition-all"
          >
            <span>Explore All Products</span>
            <span className="text-[#34D399]">→</span>
          </Link>

          <div
            className="pt-1"
            onClick={(e) => {
              if (e.target === e.currentTarget) onClose();
            }}
          >
            <span className="text-[10px] uppercase font-mono tracking-widest text-[#A1A1AA] px-2">
              Categories
            </span>
            <div
              className="flex flex-col gap-1.5 mt-1.5"
              onClick={(e) => {
                if (e.target === e.currentTarget) onClose();
              }}
            >
              {CATEGORIES.map((cat) => (
                <Link
                  key={cat.slug}
                  href={`/category/${cat.slug}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    onClose();
                  }}
                  className="flex items-center gap-3 p-2.5 rounded-xl bg-[#18181B] hover:bg-[#27272A] border border-[#27272A] text-[#E4E4E7] hover:text-white transition-colors text-xs font-mono cursor-pointer active:scale-[0.98]"
                >
                  <span className="text-base">{cat.icon}</span>
                  <span className="font-medium">{cat.name}</span>
                </Link>
              ))}
            </div>
          </div>
        </nav>
      </div>

      {/* Footer CTA */}
      <div
        className="flex flex-col gap-2 pt-3 border-t border-[#27272A] mt-4"
        onClick={(e) => {
          if (e.target === e.currentTarget) onClose();
        }}
      >
        <Button
          href="/explore"
          variant="primary"
          size="md"
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
        >
          Browse Catalog
        </Button>
      </div>
    </div>
  );
};
