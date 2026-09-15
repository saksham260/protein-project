"use client";

import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useSearch } from "@/hooks/useSearch";
import { AnimatedSearchButton } from "@/components/ui/AnimatedSearchButton";
import { formatPricePerGram, cn } from "@/lib/utils";

export interface NavbarSearchProps {
  isScrolled: boolean;
  isHome: boolean;
  className?: string;
}

export const NavbarSearch: React.FC<NavbarSearchProps> = ({
  isScrolled,
  isHome,
  className = "",
}) => {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const { results, isLoading } = useSearch(query, 250);
  const suggestions = results.slice(0, 5);

  // On the landing page, only expand after scrolling down. When unscrolled, it remains just an icon that redirects to the mainpage searchbar.
  const isExpanded = !isHome || isScrolled;

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setIsFocused(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleRedirectToMainSearch = (e?: React.MouseEvent | React.FormEvent) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const heroInput = document.getElementById("hero-search-input");
    if (heroInput) {
      heroInput.scrollIntoView({ behavior: "smooth", block: "center" });
      setTimeout(() => {
        (heroInput as HTMLInputElement).focus();
      }, 200);
    } else {
      window.scrollTo({ top: 250, behavior: "smooth" });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isExpanded) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : suggestions.length - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (selectedIndex >= 0 && suggestions[selectedIndex]) {
        router.push(`/product/${suggestions[selectedIndex].slug}`);
        setIsOpen(false);
        setIsFocused(false);
      } else if (query.trim()) {
        router.push(`/search?q=${encodeURIComponent(query.trim())}`);
        setIsOpen(false);
        setIsFocused(false);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
      setIsFocused(false);
      inputRef.current?.blur();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isExpanded) {
      handleRedirectToMainSearch(e);
      return;
    }
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
      setIsOpen(false);
      setIsFocused(false);
      inputRef.current?.blur();
    } else {
      inputRef.current?.focus();
    }
  };

  const handleContainerClick = (e: React.MouseEvent) => {
    if (!isExpanded) {
      handleRedirectToMainSearch(e);
    }
  };

  return (
    <div ref={containerRef} className={cn("relative flex items-center", className)}>
      <form
        onSubmit={handleSubmit}
        onClick={handleContainerClick}
        className={cn(
          "relative flex items-center transition-all duration-300 ease-out rounded-full border",
          isExpanded
            ? "w-44 sm:w-56 md:w-64 lg:w-72 bg-[#18181B] border-[#27272A] focus-within:border-[#10B981] shadow-[0_4px_20px_rgba(0,0,0,0.5)] h-[38px] overflow-hidden"
            : "w-[38px] h-[38px] bg-transparent border-transparent cursor-pointer overflow-visible"
        )}
      >
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
            setSelectedIndex(-1);
          }}
          onFocus={() => {
            setIsFocused(true);
            if (query.trim()) setIsOpen(true);
          }}
          onKeyDown={handleKeyDown}
          placeholder="Search..."
          tabIndex={isExpanded ? 0 : -1}
          className={cn(
            "h-full text-white text-xs font-sans placeholder-[#A1A1AA] bg-transparent outline-none transition-all duration-200",
            isExpanded
              ? "w-full pl-3.5 pr-14 opacity-100"
              : "w-0 p-0 opacity-0 pointer-events-none"
          )}
        />

        {/* Clear button when query is present */}
        {isExpanded && query && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setQuery("");
              setIsOpen(false);
              inputRef.current?.focus();
            }}
            className="absolute right-10 text-[11px] text-[#A1A1AA] hover:text-white p-1 transition-colors"
            aria-label="Clear search text"
          >
            ✕
          </button>
        )}

        {/* Morphing Search Icon Button */}
        <AnimatedSearchButton
          size={isExpanded ? 34 : 38}
          className={cn(
            isExpanded ? "absolute right-0.5 top-1/2 -translate-y-1/2" : ""
          )}
          title={isExpanded ? "Search" : "Open search"}
        />
      </form>

      {/* Live Dropdown Suggestions */}
      {isOpen && isExpanded && query.trim() && (
        <div className="absolute top-full right-0 z-50 mt-2 w-72 sm:w-80 md:w-96 rounded-2xl bg-[#18181B] border border-[#27272A] shadow-[0_20px_50px_rgba(0,0,0,0.9)] overflow-hidden py-2 animate-fade-in font-mono text-xs">
          {isLoading ? (
            <div className="p-4 text-[#A1A1AA] text-center">
              Searching database...
            </div>
          ) : suggestions.length === 0 ? (
            <div className="p-4 text-[#A1A1AA] text-center">
              No matching products. Press Enter to full-text search.
            </div>
          ) : (
            <div className="flex flex-col">
              <div className="px-4 py-1.5 text-[10px] uppercase tracking-widest text-[#A1A1AA]">
                Matches
              </div>
              {suggestions.map((p, idx) => {
                const variant = p.variants[0];
                const isSelected = idx === selectedIndex;
                return (
                  <Link
                    key={p.id}
                    href={`/product/${p.slug}`}
                    onClick={() => {
                      setIsOpen(false);
                      setIsFocused(false);
                    }}
                    className={`flex items-center justify-between px-4 py-3 transition-colors ${
                      isSelected
                        ? "bg-[#10B981]/15 text-white"
                        : "text-[#E4E4E7] hover:bg-[#27272A] hover:text-white"
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="font-bold text-white font-sans">{p.name}</span>
                      <span className="text-[11px] text-[#A1A1AA]">
                        {p.brand.name} • {p.category.name}
                      </span>
                    </div>
                    {variant?.cost_per_g_protein && (
                      <div className="flex items-center gap-1 font-mono font-bold text-[#10B981]">
                        <span>{formatPricePerGram(variant.cost_per_g_protein)}</span>
                      </div>
                    )}
                  </Link>
                );
              })}
              <Link
                href={`/search?q=${encodeURIComponent(query.trim())}`}
                onClick={() => {
                  setIsOpen(false);
                  setIsFocused(false);
                }}
                className="px-4 py-2.5 bg-[#121215] text-center text-[#10B981] font-mono text-xs hover:bg-[#10B981]/10 border-t border-[#27272A] transition-colors"
              >
                View all results for &quot;{query}&quot; →
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
