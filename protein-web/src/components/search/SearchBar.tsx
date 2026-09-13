"use client";

import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useSearch } from "@/hooks/useSearch";
import { formatPricePerGram } from "@/lib/utils";

export interface SearchBarProps {
  placeholder?: string;
  initialValue?: string;
  autoFocus?: boolean;
  className?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = "Search by brand, product name, or variant (e.g. Whey, Amul, Yoga Bar)...",
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
        <span className="absolute left-4 text-base text-[var(--text-muted)] pointer-events-none">
          🔍
        </span>
        <input
          ref={inputRef}
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
          className="w-full pl-12 pr-10 py-3.5 rounded-2xl bg-[rgba(18,18,26,0.85)] backdrop-blur-xl border border-[rgba(255,255,255,0.12)] text-white text-sm placeholder-[var(--text-faint)] focus:outline-none focus:border-[var(--accent-emerald)] focus:ring-2 focus:ring-[rgba(0,212,170,0.2)] shadow-xl shadow-black/30 transition-all"
        />
        {query && (
          <button
            type="button"
            onClick={() => {
              setQuery("");
              setIsOpen(false);
              inputRef.current?.focus();
            }}
            className="absolute right-4 text-xs text-[var(--text-muted)] hover:text-white p-1"
          >
            ✕
          </button>
        )}
      </form>

      {/* Live Dropdown Suggestions */}
      {isOpen && query.trim() && (
        <div className="absolute top-full left-0 right-0 z-50 mt-2 rounded-2xl bg-[#161624] border border-[rgba(255,255,255,0.12)] shadow-2xl backdrop-blur-2xl overflow-hidden py-2 animate-fade-in">
          {isLoading ? (
            <div className="p-4 text-xs text-[var(--text-muted)] text-center">
              Searching verified labels...
            </div>
          ) : suggestions.length === 0 ? (
            <div className="p-4 text-xs text-[var(--text-muted)] text-center">
              No matching protein products found. Press Enter to search all.
            </div>
          ) : (
            <div className="flex flex-col">
              <div className="px-3.5 py-1 text-[10px] font-mono uppercase tracking-wider text-[var(--text-faint)]">
                Matching Products
              </div>
              {suggestions.map((p, idx) => {
                const variant = p.variants[0];
                const isSelected = idx === selectedIndex;
                return (
                  <Link
                    key={p.id}
                    href={`/product/${p.slug}`}
                    onClick={() => setIsOpen(false)}
                    className={`flex items-center justify-between px-4 py-2.5 text-xs transition-colors ${
                      isSelected
                        ? "bg-[rgba(0,212,170,0.15)] text-white"
                        : "text-[var(--text-secondary)] hover:bg-[rgba(255,255,255,0.05)] hover:text-white"
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="font-bold text-[var(--text-primary)]">{p.name}</span>
                      <span className="text-[11px] text-[var(--accent-emerald)] font-medium">
                        {p.brand.name} • {p.category.name}
                      </span>
                    </div>
                    {variant?.cost_per_g_protein && (
                      <div className="flex items-center gap-1 font-mono text-xs font-bold text-[#00d4aa]">
                        <span>{formatPricePerGram(variant.cost_per_g_protein)}</span>
                      </div>
                    )}
                  </Link>
                );
              })}
              <div className="border-t border-[rgba(255,255,255,0.06)] mt-1 pt-1 px-3">
                <button
                  type="button"
                  onClick={handleSubmit}
                  className="w-full text-left py-1.5 text-xs text-[var(--accent-emerald)] hover:underline font-medium"
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
