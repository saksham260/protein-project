"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { CATEGORIES } from "@/lib/constants";
import { Button } from "@/components/ui/Button";
import { MobileNav } from "@/components/layout/MobileNav";
import { cn } from "@/lib/utils";

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <header
        className={cn(
          "sticky top-0 z-40 w-full transition-all duration-300",
          isScrolled
            ? "bg-[#0a0a0f]/85 backdrop-blur-xl border-b border-[rgba(255,255,255,0.08)] py-3 shadow-lg shadow-black/40"
            : "bg-transparent py-4 border-b border-transparent"
        )}
      >
        <div className="container flex items-center justify-between gap-4">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[var(--accent-purple)] to-[var(--accent-emerald)] flex items-center justify-center text-lg font-bold shadow-md shadow-[rgba(0,212,170,0.25)] group-hover:scale-105 transition-transform">
              ⚡
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-base tracking-tight text-[var(--text-primary)]">
                Protein Engine
              </span>
              <span className="text-[10px] font-mono tracking-wider text-[var(--accent-emerald)] uppercase">
                India Discovery
              </span>
            </div>
          </Link>

          {/* Desktop Categories Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            <Link
              href="/explore"
              className={cn(
                "px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors",
                pathname === "/explore"
                  ? "text-[var(--accent-emerald)] bg-[rgba(0,212,170,0.1)]"
                  : "text-[var(--text-secondary)] hover:text-white hover:bg-[rgba(255,255,255,0.05)]"
              )}
            >
              All Products
            </Link>
            {CATEGORIES.map((cat) => {
              const active = pathname === `/category/${cat.slug}`;
              return (
                <Link
                  key={cat.slug}
                  href={`/category/${cat.slug}`}
                  className={cn(
                    "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5",
                    active
                      ? "text-[var(--accent-emerald)] bg-[rgba(0,212,170,0.1)]"
                      : "text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.05)]"
                  )}
                >
                  <span className="text-xs">{cat.icon}</span>
                  <span>{cat.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Search CTA & Actions */}
          <div className="flex items-center gap-2.5">
            <Button
              href="/search"
              variant="outline"
              size="sm"
              className="hidden sm:inline-flex items-center gap-2 text-xs text-[var(--text-muted)] border-[rgba(255,255,255,0.1)] hover:border-[var(--accent-emerald)] px-3 py-2 rounded-xl bg-[rgba(255,255,255,0.02)]"
            >
              <span>🔍</span>
              <span>Search products...</span>
              <kbd className="text-[10px] bg-[rgba(255,255,255,0.08)] px-1.5 py-0.5 rounded text-[var(--text-faint)] font-mono">
                ⌘K
              </kbd>
            </Button>

            <Button href="/explore" variant="primary" size="sm" className="hidden sm:inline-flex">
              Explore
            </Button>

            {/* Mobile Hamburger Toggle */}
            <button
              onClick={() => setIsMobileOpen(true)}
              aria-label="Open mobile navigation"
              className="p-2 rounded-xl bg-[rgba(255,255,255,0.05)] border border-[rgba(255,255,255,0.08)] text-[var(--text-secondary)] hover:text-white lg:hidden"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <MobileNav isOpen={isMobileOpen} onClose={() => setIsMobileOpen(false)} />
    </>
  );
};
