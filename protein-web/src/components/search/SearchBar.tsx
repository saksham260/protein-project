"use client";

import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useSearch } from "@/hooks/useSearch";
import { AnimatedSearchButton } from "@/components/ui/AnimatedSearchButton";
import { formatPricePerGram } from "@/lib/utils";

export interface SearchBarProps {
  id?: string;
  placeholder?: string;
  initialValue?: string;
  autoFocus?: boolean;
  className?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  id = "hero-search-input",
  placeholder = "Search verified products, brands, or ingredients (e.g. Whey, Amul, Isolate)...",
  initialValue = "",
  autoFocus = false,
  className = "",
}) => {
  const router = useRouter();
  const [query, setQuery] = useState(initialValue);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const { results, isLoading } = useSearch(query, 250);
  const suggestions = results.slice(0, 5);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
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
      } else if (query.trim()) {
        router.push(`/search?q=${encodeURIComponent(query.trim())}`);
        setIsOpen(false);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
      setIsOpen(false);
    }
  };

  return (
    <div ref={containerRef} className={`relative w-full ${className}`}>
      <form onSubmit={handleSubmit} className="relative flex items-center w-full">
        <input
          ref={inputRef}
          id={id}
          type="text"
          value={query}
          autoFocus={autoFocus}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
            setSelectedIndex(-1);
          }}
          onFocus={() => setIsOpen(Boolean(query.trim()))}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full pl-5 sm:pl-6 pr-14 sm:pr-16 py-3.5 rounded-full bg-[#18181B] border border-[#27272A] text-white text-xs sm:text-sm font-sans placeholder-[#A1A1AA] focus:outline-none focus:border-[#10B981] focus:ring-1 focus:ring-[#10B981] shadow-[0_4px_24px_rgba(0,0,0,0.5)] transition-all"
        />
        <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
          {query && (
            <button
              type="button"
              onClick={() => {
                setQuery("");
                setIsOpen(false);
                inputRef.current?.focus();
              }}
              className="text-xs text-[#A1A1AA] hover:text-white p-1.5 transition-colors"
              aria-label="Clear search"
            >
              ✕
            </button>
          )}
          <AnimatedSearchButton />
        </div>
      </form>

      {/* Live Dropdown Suggestions */}
      {isOpen && query.trim() && (
        <div className="absolute top-full left-0 right-0 z-50 mt-2 rounded-2xl bg-[#18181B] border border-[#27272A] shadow-[0_20px_50px_rgba(0,0,0,0.9)] overflow-hidden py-2 animate-fade-in font-mono text-xs">
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
                    onClick={() => setIsOpen(false)}
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
                      <div className="flex items-center gap-1 font-bold text-[#10B981]">
                        <span>{formatPricePerGram(variant.cost_per_g_protein)}</span>
                      </div>
                    )}
                  </Link>
                );
              })}
              <div className="border-t border-[#27272A] mt-1 pt-1 px-4">
                <button
                  type="button"
                  onClick={handleSubmit}
                  className="w-full text-left py-2 text-xs text-[#34D399] hover:underline font-bold"
                >
                  View all results for &quot;{query}&quot; →
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
