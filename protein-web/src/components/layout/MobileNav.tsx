"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { CATEGORIES } from "@/lib/constants";
import { Button } from "@/components/ui/Button";

export interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileNav: React.FC<MobileNavProps> = ({ isOpen, onClose }) => {
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
      className="fixed inset-0 z-50 flex flex-col justify-between bg-[#0A0A0B]/95 backdrop-blur-2xl p-5 md:hidden animate-fade-in overflow-hidden select-none cursor-pointer"
      aria-modal="true"
      role="dialog"
    >
      <div
        className="flex flex-col gap-3.5 max-h-full"
        onClick={(e) => {
          // If user clicks in empty gap between elements, return to page
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
        className="flex flex-col gap-2 pt-3 border-t border-[#27272A]"
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
