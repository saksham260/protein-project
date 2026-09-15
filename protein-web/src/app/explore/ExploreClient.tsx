"use client";

import React, { useState, useEffect } from "react";
import { FilterPanel } from "@/components/search/FilterPanel";
import { SortDropdown } from "@/components/search/SortDropdown";
import { ProductCard } from "@/components/product/ProductCard";
import { useFilters } from "@/hooks/useFilters";
import { getProducts } from "@/lib/data";
import { ProductWithVariants } from "@/types/product";
import { CATEGORIES } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function ExploreClient() {
  const {
    filters,
    isPending,
    setCategory,
    toggleTier,
    toggleTag,
    toggleAllergen,
    setZeroFlagsOnly,
    setSortBy,
    clearFilters,
  } = useFilters();

  const [products, setProducts] = useState<ProductWithVariants[]>([]);
  const [loading, setLoading] = useState(true);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const timer = setTimeout(() => {
      setLoading(true);
      getProducts(filters)
        .then((data) => {
          if (isMounted) {
            setProducts(data);
            setLoading(false);
          }
        })
        .catch(() => {
          if (isMounted) setLoading(false);
        });
    }, 0);

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, [filters]);

  const activeCategory = CATEGORIES.find((c) => c.slug === filters.categorySlug);

  const activeFiltersCount =
    (filters.categorySlug ? 1 : 0) +
    (filters.proteinTiers?.length || 0) +
    (filters.dietaryTags?.length || 0) +
    (filters.excludeAllergens?.length || 0) +
    (filters.zeroFlagsOnly ? 1 : 0);

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 md:py-16 flex flex-col gap-10">
      {/* Top Header with High Negative Space */}
      <div className="flex flex-col gap-4 border-b border-[#27272A] pb-8">
        <div className="flex items-center gap-2 text-xs font-mono tracking-widest text-[#10B981] uppercase font-bold">
          <span>Discovery Engine</span>
          <span className="text-[#A1A1AA]">/</span>
          <span>Independent Transparency</span>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div className="max-w-2xl">
            <h1 className="text-4xl sm:text-5xl font-black text-white tracking-tight">
              {activeCategory ? activeCategory.name : "All Protein Products"}
            </h1>
            <p className="text-sm sm:text-base text-[#A1A1AA] mt-2 leading-relaxed">
              {activeCategory
                ? activeCategory.description
                : "Objective, mathematically deconstructed protein database. Raw ₹/g efficiency, true density, and red-flag audits."}
            </p>
          </div>

          {/* Desktop Summary & Sort / Mobile Filter Toggle */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:block">
              <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
            </div>

            {/* Mobile Filter Button */}
            <button
              type="button"
              onClick={() => setMobileFilterOpen(true)}
              className="lg:hidden flex items-center justify-center gap-2 px-4 py-2.5 rounded-full bg-[#18181B] border border-[#27272A] text-xs font-mono text-white select-none shadow-[0_4px_16px_rgba(0,0,0,0.4)]"
            >
              <span>⚙️ Filters</span>
              {activeFiltersCount > 0 && (
                <span className="px-1.5 py-0.5 rounded-full bg-[#10B981] text-[#0A0A0B] text-[10px] font-bold">
                  {activeFiltersCount}
                </span>
              )}
            </button>
          </div>
        </div>

        {/* Mobile Sort Dropdown */}
        <div className="sm:hidden pt-2">
          <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
        </div>
      </div>

      {/* Main Grid & Sidebar Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        {/* Sticky Desktop Left Sidebar */}
        <aside className="hidden lg:block lg:col-span-3 sticky top-24">
          <FilterPanel
            filters={filters}
            onCategoryChange={setCategory}
            onToggleTier={toggleTier}
            onToggleTag={toggleTag}
            onToggleAllergen={toggleAllergen}
            onSetZeroFlagsOnly={setZeroFlagsOnly}
            onClearFilters={clearFilters}
          />
        </aside>

        {/* Product Results Column */}
        <div className="lg:col-span-9 flex flex-col gap-8">
          {/* Results Status Bar */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono uppercase tracking-wider text-[#A1A1AA]">
                Verified Catalog
              </span>
              <span className="text-xs font-mono font-bold text-[#E4E4E7] px-2.5 py-0.5 rounded-full bg-[#18181B] border border-[#27272A]">
                {products.length} Products
              </span>
              {isPending && (
                <span className="text-xs font-mono text-[#10B981] animate-pulse">
                  Updating...
                </span>
              )}
            </div>

            {activeFiltersCount > 0 && (
              <button
                type="button"
                onClick={clearFilters}
                className="text-xs font-mono text-[#A1A1AA] hover:text-[#34D399] transition-colors cursor-pointer"
              >
                Reset All Filters
              </button>
            )}
          </div>

          {/* Active Filter Chips */}
          {activeFiltersCount > 0 && (
            <div className="flex flex-wrap items-center gap-2 select-none">
              {filters.categorySlug && (
                <button
                  type="button"
                  onClick={() => setCategory(undefined)}
                  className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-[#10B981]/15 text-[#34D399] border border-[#10B981]/30 hover:bg-[#10B981]/25 transition-colors"
                >
                  <span>Category: {activeCategory?.name || filters.categorySlug}</span>
                  <span>×</span>
                </button>
              )}

              {filters.zeroFlagsOnly && (
                <button
                  type="button"
                  onClick={() => setZeroFlagsOnly(false)}
                  className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-[#10B981] text-[#0A0A0B] font-bold shadow-[0_0_12px_rgba(16,185,129,0.25)] transition-colors"
                >
                  <span>Zero Red Flags</span>
                  <span>×</span>
                </button>
              )}

              {filters.proteinTiers?.map((tier) => (
                <button
                  key={tier}
                  type="button"
                  onClick={() => toggleTier(tier)}
                  className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-[#18181B] text-[#E4E4E7] border border-[#27272A] hover:border-[#3F3F46] transition-colors"
                >
                  <span>{tier}</span>
                  <span>×</span>
                </button>
              ))}

              {filters.dietaryTags?.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleTag(tag)}
                  className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-[#18181B] text-[#E4E4E7] border border-[#27272A] hover:border-[#3F3F46] transition-colors"
                >
                  <span>{tag}</span>
                  <span>×</span>
                </button>
              ))}

              {filters.excludeAllergens?.map((allergen) => (
                <button
                  key={allergen}
                  type="button"
                  onClick={() => toggleAllergen(allergen)}
                  className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono bg-[#EF4444]/15 text-[#F87171] border border-[#EF4444]/30 hover:bg-[#EF4444]/25 transition-colors"
                >
                  <span>No {allergen}</span>
                  <span>×</span>
                </button>
              ))}
            </div>
          )}

          {/* Clean CSS Grid for Products with High Negative Space */}
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div
                  key={i}
                  className="h-[460px] rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.5)] skeleton-shimmer"
                />
              ))}
            </div>
          ) : products.length === 0 ? (
            /* Empty State */
            <div className="flex flex-col items-center justify-center p-16 text-center rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.5)] gap-5">
              <span className="text-5xl">🔍</span>
              <h3 className="text-xl font-bold text-white tracking-tight">
                No matching formulations found
              </h3>
              <p className="text-sm text-[#A1A1AA] max-w-md leading-relaxed">
                Try loosening your allergen exclusions or tier filters to explore more verified products.
              </p>
              <button
                type="button"
                onClick={clearFilters}
                className="mt-2 px-6 py-2.5 rounded-full bg-[#10B981] hover:bg-[#34D399] text-[#0A0A0B] font-mono font-bold text-xs shadow-[0_0_20px_rgba(16,185,129,0.25)] transition-all cursor-pointer"
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            /* High-Space Product Grid */
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 items-stretch animate-fade-in">
              {products.map((prod) => (
                <ProductCard key={prod.id} product={prod} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Sticky Bottom Mobile Filter Drawer (Apple-like bottom sheet) */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end bg-[#0A0A0B]/85 backdrop-blur-sm lg:hidden animate-fade-in">
          <div
            className="w-full max-h-[85vh] bg-[#18181B] rounded-t-3xl border-t border-[#27272A] p-6 overflow-y-auto flex flex-col gap-5 shadow-[0_-20px_60px_rgba(0,0,0,0.9)] animate-slide-up"
          >
            {/* Sheet Handle & Header */}
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-1.5 rounded-full bg-[#27272A]" />
              <div className="w-full flex items-center justify-between pb-3 border-b border-[#27272A]">
                <span className="font-mono text-sm uppercase tracking-widest text-white font-bold">
                  Faceted Filters
                </span>
                <button
                  type="button"
                  onClick={() => setMobileFilterOpen(false)}
                  className="w-8 h-8 rounded-full bg-[#27272A] flex items-center justify-center text-[#A1A1AA] hover:text-white text-sm"
                  aria-label="Close filters"
                >
                  ✕
                </button>
              </div>
            </div>

            <FilterPanel
              filters={filters}
              onCategoryChange={(slug) => {
                setCategory(slug);
                setMobileFilterOpen(false);
              }}
              onToggleTier={toggleTier}
              onToggleTag={toggleTag}
              onToggleAllergen={toggleAllergen}
              onSetZeroFlagsOnly={setZeroFlagsOnly}
              onClearFilters={clearFilters}
              className="border-0 p-0 bg-transparent shadow-none"
            />

            <div className="sticky bottom-0 pt-4 bg-[#18181B] border-t border-[#27272A]">
              <button
                type="button"
                className="w-full py-3.5 rounded-2xl bg-[#10B981] hover:bg-[#34D399] text-[#0A0A0B] font-mono font-bold text-sm shadow-[0_0_20px_rgba(16,185,129,0.3)] transition-all cursor-pointer"
                onClick={() => setMobileFilterOpen(false)}
              >
                View {products.length} Products
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
