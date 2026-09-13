"use client";

import React from "react";
import Link from "next/link";
import { CATEGORIES } from "@/lib/constants";
import { Button } from "@/components/ui/Button";

export interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileNav: React.FC<MobileNavProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex flex-col justify-between bg-[#0a0a0f]/95 backdrop-blur-2xl p-6 md:hidden animate-fade-in">
      <div className="flex flex-col gap-6">
        {/* Header with Close Button */}
        <div className="flex items-center justify-between border-b border-[var(--border-subtle)] pb-4">
          <Link href="/" onClick={onClose} className="flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-[var(--accent-emerald)] to-[var(--accent-cyan)] bg-clip-text text-transparent">
              Protein Engine
            </span>
          </Link>
          <button
            onClick={onClose}
            aria-label="Close menu"
            className="p-2 text-[var(--text-muted)] hover:text-white rounded-lg hover:bg-[rgba(255,255,255,0.08)]"
          >
            ✕
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="flex flex-col gap-3">
          <Link
            href="/explore"
            onClick={onClose}
            className="flex items-center justify-between p-3 rounded-xl bg-[rgba(255,255,255,0.04)] hover:bg-[rgba(255,255,255,0.08)] font-semibold text-base"
          >
            <span>Explore All Products</span>
            <span>→</span>
          </Link>

          <div className="pt-2">
            <span className="text-xs uppercase font-mono tracking-wider text-[var(--text-faint)] px-3">
              Categories
            </span>
            <div className="flex flex-col gap-1 mt-2">
              {CATEGORIES.map((cat) => (
                <Link
                  key={cat.slug}
                  href={`/category/${cat.slug}`}
                  onClick={onClose}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-[rgba(255,255,255,0.05)] text-[var(--text-secondary)] hover:text-white transition-colors"
                >
                  <span className="text-xl">{cat.icon}</span>
                  <span className="font-medium text-sm">{cat.name}</span>
                </Link>
              ))}
            </div>
          </div>
        </nav>
      </div>

      {/* Footer CTA */}
      <div className="flex flex-col gap-3 pt-6 border-t border-[var(--border-subtle)]">
        <Button href="/explore" variant="primary" size="lg" onClick={onClose}>
          Browse Catalog
        </Button>
      </div>
    </div>
  );
};
