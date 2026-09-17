"use client";

import React, { useState, useEffect, useRef } from "react";
import { CATEGORIES } from "@/lib/constants";
import { cn } from "@/lib/utils";

export interface CategoryBarProps {
  activeCategory?: string;
  onSelectCategory?: (slug: string) => void;
  className?: string;
}

export const CATEGORY_TABS = [
  { id: "all", name: "All Products", icon: "⚡" },
  { id: "top-picks", name: "Top Picks", icon: "🏆" },
  ...CATEGORIES.map((cat) => ({
    id: cat.slug,
    name: cat.name,
    icon: cat.icon,
  })),
];

export const CategoryBar: React.FC<CategoryBarProps> = ({
  activeCategory = "all",
  onSelectCategory,
  className = "",
}) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({});
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      const top = window.scrollY || document.documentElement.scrollTop || 0;
      setIsScrolled(top > 10);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Auto-scroll active category pill into center view on mobile/desktop
  useEffect(() => {
    if (activeCategory && tabRefs.current[activeCategory]) {
      tabRefs.current[activeCategory]?.scrollIntoView({
        behavior: "smooth",
        inline: "center",
        block: "nearest",
      });
    }
  }, [activeCategory]);

  return (
    <div
      style={{
        background: isScrolled ? "rgba(10, 10, 11, 0.75)" : "transparent",
        backdropFilter: isScrolled
          ? "blur(20px) saturate(180%) brightness(108%)"
          : "none",
        WebkitBackdropFilter: isScrolled
          ? "blur(20px) saturate(180%) brightness(108%)"
          : "none",
        borderBottom: isScrolled
          ? "1px solid rgba(39, 39, 42, 0.7)"
          : "1px solid transparent",
        boxShadow: isScrolled
          ? "0 8px 32px rgba(0, 0, 0, 0.5)"
          : "none",
      }}
      className={cn(
        "sticky top-16 z-40 w-full select-none transition-all duration-300",
        className
      )}
    >
      <div className="container max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 flex justify-center">
        <div
          ref={containerRef}
          className="flex items-center justify-start sm:justify-center gap-1.5 sm:gap-2 py-2 overflow-x-auto no-scrollbar scroll-smooth w-full sm:w-auto -mx-3 px-3 sm:mx-0 sm:px-0 touch-pan-x"
        >
          {CATEGORY_TABS.map((tab) => {
            const isActive = activeCategory === tab.id;
            return (
              <button
                key={tab.id}
                ref={(el) => {
                  tabRefs.current[tab.id] = el;
                }}
                type="button"
                onClick={() => onSelectCategory?.(tab.id)}
                className={cn(
                  "flex items-center gap-1.5 sm:gap-2 px-3 sm:px-3.5 py-1.5 sm:py-1.5 min-h-[38px] sm:min-h-[34px] rounded-full text-xs font-mono font-medium whitespace-nowrap transition-all duration-200 cursor-pointer shrink-0 border active:scale-95 touch-manipulation",
                  isActive
                    ? "bg-[#10B981]/15 text-[#10B981] border-[#10B981]/50 shadow-[0_0_12px_rgba(16,185,129,0.25)] font-bold"
                    : "bg-[#18181B]/80 text-[#A1A1AA] border-[#27272A] hover:text-white hover:bg-[#27272A] hover:border-[#3F3F46]"
                )}
              >
                <span className="text-sm select-none">{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default CategoryBar;
