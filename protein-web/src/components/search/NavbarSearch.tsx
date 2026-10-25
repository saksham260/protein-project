"use client";

import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { useSearch } from "@/hooks/useSearch";
import { useRecentSearches } from "@/hooks/useRecentSearches";
import { formatPricePerGram, cn, splitProductName, resetMobileZoom } from "@/lib/utils";

const SEARCH_SUGGESTIONS = [
  // Categories
  "Chips",
  "Bars",
  "Powders",
  "Drinks",
  "Snacks",
  // Brands
  "Amul",
  "MuscleBlaze",
  "Yoga Bar",
  "The Whole Truth",
  "Nakpro",
  "Cosmix",
  "Epigamia",
  "RiteBite",
  "Plantigo",
  "Phab",
  // Product first words & key terms
  "Whey",
  "Isolate",
  "Buttermilk",
  "Biozyme",
  "Peanut",
  "Oats",
  "Plant",
];

export interface NavbarSearchProps {
  className?: string;
  placeholder?: string;
  isScrolled?: boolean;
  isSearchOpen?: boolean;
  onSearchOpenChange?: (open: boolean) => void;
}

export const NavbarSearch: React.FC<NavbarSearchProps> = ({
  className = "",
  placeholder,
  isScrolled = false,
  isSearchOpen: controlledSearchOpen,
  onSearchOpenChange,
}) => {
  const router = useRouter();
  const [internalSearchOpen, setInternalSearchOpen] = useState(false);
  const isSearchOpen = controlledSearchOpen ?? internalSearchOpen;

  const setSearchOpen = (open: boolean) => {
    setInternalSearchOpen(open);
    onSearchOpenChange?.(open);
  };

  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const isExpanded = isScrolled || isSearchOpen || Boolean(query.trim());

  const [wordIndex, setWordIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  // Typewriter effect cycling through categories, brands, and product keywords
  useEffect(() => {
    const currentWord = SEARCH_SUGGESTIONS[wordIndex];
    let timer: NodeJS.Timeout;

    if (!isDeleting) {
      if (displayedText.length < currentWord.length) {
        timer = setTimeout(() => {
          setDisplayedText(currentWord.slice(0, displayedText.length + 1));
        }, 75);
      } else {
        timer = setTimeout(() => {
          setIsDeleting(true);
        }, 1500);
      }
    } else {
      if (displayedText.length > 0) {
        timer = setTimeout(() => {
          setDisplayedText(currentWord.slice(0, displayedText.length - 1));
        }, 40);
      } else {
        timer = setTimeout(() => {
          setIsDeleting(false);
          setWordIndex((prev) => (prev + 1) % SEARCH_SUGGESTIONS.length);
        }, 250);
      }
    }

    return () => clearTimeout(timer);
  }, [displayedText, isDeleting, wordIndex]);

  const activePlaceholder = placeholder || `Search for "${displayedText}"`;

  const { results, isLoading } = useSearch(query, 250);
  const suggestions = results.slice(0, 5);

  // Signed-in users see their recent searches when they click the empty search bar
  const recent = useRecentSearches();
  const showRecent = isFocused && !query.trim() && recent.isSignedIn && recent.items.length > 0;

  const runSearch = (term: string) => {
    inputRef.current?.blur();
    resetMobileZoom();
    recent.record(term);
    router.push(`/search?q=${encodeURIComponent(term.trim())}`);
  };

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent | TouchEvent) => {
      const target = e.target as Node;

      // If clicking inside container, do nothing
      if (containerRef.current && containerRef.current.contains(target)) {
        return;
      }

      // If clicking outside, close suggestions dropdown
      setIsOpen(false);
      setIsFocused(false);
      resetMobileZoom();
      if (!query.trim() && !isScrolled) {
        setSearchOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside, { passive: true });
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
    };
  }, [query, isScrolled]);

  const handleOpenSearch = (e: React.MouseEvent) => {
    if (!isExpanded) {
      setSearchOpen(true);
      setIsFocused(true);
      inputRef.current?.focus();
    } else if (e.target !== inputRef.current) {
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : suggestions.length - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      inputRef.current?.blur();
      resetMobileZoom();
      if (selectedIndex >= 0 && suggestions[selectedIndex]) {
        recent.record(query);
        router.push(`/product/${suggestions[selectedIndex].slug}`);
        setIsOpen(false);
        setIsFocused(false);
      } else if (query.trim()) {
        runSearch(query);
        setIsOpen(false);
        setIsFocused(false);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
      setIsFocused(false);
      inputRef.current?.blur();
      resetMobileZoom();
      if (!query.trim() && !isScrolled) {
        setSearchOpen(false);
      }
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isExpanded) {
      setSearchOpen(true);
      setIsFocused(true);
      inputRef.current?.focus();
      return;
    }
    inputRef.current?.blur();
    resetMobileZoom();
    if (query.trim()) {
      runSearch(query);
      setIsOpen(false);
      setIsFocused(false);
    } else {
      inputRef.current?.focus();
    }
  };

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative md:flex-1 md:w-full md:max-w-xl md:transition-none",
        (isOpen && query.trim()) || showRecent ? "z-50" : "z-30",
        isExpanded
          ? "flex-1 w-full max-w-xl transition-[max-width,width,flex] duration-300 ease-out"
          : "max-md:w-10 max-md:max-w-[40px] max-md:shrink-0 transition-[max-width,width,flex] duration-300 ease-out",
        className
      )}
    >
      <form
        onSubmit={handleSubmit}
        onClick={handleOpenSearch}
        className={cn(
          "group relative flex items-center rounded-full border shadow-inner overflow-hidden h-10 select-none bg-[#1C1916]/85 border-[#332D27] text-[#968E85] md:hover:bg-[#26221E] md:hover:border-[#D97706]/50 md:hover:shadow-[0_0_16px_rgba(217,119,6,0.18),0_2px_8px_rgba(0,0,0,0.4)] focus-within:bg-[#26221E] focus-within:border-[#D97706] focus-within:shadow-[0_0_20px_rgba(217,119,6,0.25)] transition-all duration-300 ease-out",
          "md:w-full md:cursor-auto",
          isExpanded
            ? "w-full cursor-auto"
            : "max-md:w-10 max-md:cursor-pointer"
        )}
      >
        {/* Search Icon */}
        <div className="w-10 h-10 flex items-center justify-center shrink-0 text-[#968E85] md:group-hover:text-[#D97706] group-focus-within:text-[#D97706] transition-colors duration-300 pointer-events-none">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </div>

        {/* Input */}
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
            setSearchOpen(true);
            if (query.trim()) setIsOpen(true);
          }}
          onBlur={(e) => {
            if (containerRef.current && containerRef.current.contains(e.relatedTarget as Node)) {
              return;
            }
            setIsFocused(false);
            resetMobileZoom();
            if (!query.trim() && !isScrolled) {
              setSearchOpen(false);
            }
          }}
          onKeyDown={handleKeyDown}
          placeholder={activePlaceholder}
          tabIndex={0}
          className={cn(
            "h-full text-[#F5F2EB] text-xs sm:text-sm font-sans placeholder-[#787067] bg-transparent outline-none pr-9 md:w-full md:opacity-100 md:pointer-events-auto md:relative md:block md:transition-none",
            isExpanded
              ? "relative w-full opacity-100 block transition-opacity duration-300"
              : "max-md:absolute max-md:inset-0 max-md:w-full max-md:h-full max-md:opacity-0 max-md:z-10 max-md:cursor-pointer"
          )}
        />

        {/* Clear button */}
        {query && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setQuery("");
              setIsOpen(false);
              inputRef.current?.focus();
            }}
            className={cn(
              "absolute right-3 text-xs text-[#968E85] hover:text-[#F5F2EB] p-1 transition-colors duration-200 cursor-pointer z-20",
              !isExpanded && "max-md:hidden"
            )}
            aria-label="Clear search text"
          >
            ✕
          </button>
        )}
      </form>

      {/* Recent searches (signed-in users, empty search bar) */}
      {showRecent && (
        <div className="absolute top-full left-0 right-0 z-[100] mt-2 rounded-2xl bg-[#1C1916] border border-[#332D27] shadow-[0_20px_50px_rgba(0,0,0,0.95)] overflow-hidden py-2 font-mono text-xs animate-in fade-in slide-in-from-top-1 duration-150">
          <div className="px-4 py-1.5 flex items-center justify-between">
            <span className="text-[10px] uppercase tracking-widest text-[#968E85]">Recent searches</span>
            <button
              type="button"
              onClick={recent.clear}
              className="text-[10px] uppercase tracking-widest text-[#968E85] hover:text-[#D97706] transition-colors cursor-pointer"
            >
              Clear all
            </button>
          </div>
          {recent.items.map((item) => (
            <div key={item.key} className="flex items-center hover:bg-[#26221E] transition-colors">
              <button
                type="button"
                onClick={() => {
                  setQuery(item.query);
                  setIsOpen(false);
                  setIsFocused(false);
                  runSearch(item.query);
                }}
                className="flex-1 min-w-0 flex items-center gap-3 px-4 py-2.5 text-left text-[#F5F2EB] cursor-pointer"
              >
                <span aria-hidden className="text-[#968E85]">🕘</span>
                <span className="truncate font-sans text-xs sm:text-sm">{item.query}</span>
              </button>
              <button
                type="button"
                onClick={() => recent.remove(item.key)}
                aria-label={`Remove ${item.query} from recent searches`}
                className="px-3.5 py-2.5 text-[#968E85] hover:text-[#F5F2EB] transition-colors cursor-pointer"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Live Dropdown Suggestions */}
      {isOpen && query.trim() && (
        <div className="absolute top-full left-0 right-0 z-[100] mt-2 rounded-2xl bg-[#1C1916] border border-[#332D27] shadow-[0_20px_50px_rgba(0,0,0,0.95)] overflow-hidden py-2 font-mono text-xs animate-in fade-in slide-in-from-top-1 duration-150">
          {isLoading ? (
            <div className="p-4 text-[#968E85] text-center">
              Searching verified database...
            </div>
          ) : suggestions.length === 0 ? (
            <div className="p-4 text-[#968E85] text-center">
              No matching products. Press Enter for full search.
            </div>
          ) : (
            <div className="flex flex-col">
              <div className="px-4 py-1.5 text-[10px] uppercase tracking-widest text-[#968E85]">
                Matches
              </div>
              {suggestions.map((p, idx) => {
                const variant = p.variants[0];
                const imageUrl = variant?.image_url || p.image_url;
                const isSelected = idx === selectedIndex;
                const { baseName, packInfo } = splitProductName(p.name, variant?.variant_name);

                return (
                  <Link
                    key={p.id}
                    href={`/product/${p.slug}`}
                    onClick={() => {
                      recent.record(query);
                      setIsOpen(false);
                      setIsFocused(false);
                      inputRef.current?.blur();
                      resetMobileZoom();
                    }}
                    className={`flex items-center justify-between px-3.5 py-2.5 transition-colors gap-3 ${
                      isSelected
                        ? "bg-[#D97706]/15 text-[#F5F2EB]"
                        : "text-[#F5F2EB] hover:bg-[#26221E] hover:text-white"
                    }`}
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      {/* Product Thumbnail */}
                      <div className="relative w-10 h-10 rounded-lg bg-[#141210] border border-[#332D27] overflow-hidden shrink-0 flex items-center justify-center">
                        {imageUrl ? (
                          <Image
                            src={imageUrl}
                            alt={p.name}
                            fill
                            className="object-cover"
                            sizes="40px"
                          />
                        ) : (
                          <span className="text-base select-none">{p.category?.icon || "⚡"}</span>
                        )}
                      </div>

                      <div className="flex flex-col min-w-0">
                        <span className="font-bold text-[#F5F2EB] font-sans text-xs sm:text-sm line-clamp-1">
                          {baseName}
                        </span>
                        {packInfo && (
                          <span className="text-[10px] sm:text-[11px] font-bold text-[#F59E0B] font-mono leading-tight">
                            {packInfo}
                          </span>
                        )}
                        <span className="text-[11px] text-[#968E85] truncate">
                          {p.brand.name} • {p.category.name}
                        </span>
                      </div>
                    </div>

                    {variant?.mrp_inr && (
                      <div className="flex items-baseline gap-0.5 font-mono text-[#D97706] shrink-0 pl-2">
                        <span className="text-xs font-semibold text-[#D97706]/80">₹</span>
                        <span className="text-base sm:text-lg font-extrabold tracking-tight">
                          {variant.mrp_inr.toLocaleString("en-IN")}
                        </span>
                      </div>
                    )}
                  </Link>
                );
              })}
              <Link
                href={`/search?q=${encodeURIComponent(query.trim())}`}
                onClick={() => {
                  recent.record(query);
                  setIsOpen(false);
                  setIsFocused(false);
                  inputRef.current?.blur();
                  resetMobileZoom();
                }}
                className="px-4 py-2.5 bg-[#141210] text-center text-[#D97706] font-mono text-xs hover:bg-[#D97706]/10 border-t border-[#332D27] transition-colors"
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
