"use client";

import React, { useState, useEffect } from "react";
import { FilterPanel } from "@/components/search/FilterPanel";
import { SortDropdown } from "@/components/search/SortDropdown";
import { ProductCard } from "@/components/product/ProductCard";
import { Button } from "@/components/ui/Button";
import { useFilters } from "@/hooks/useFilters";
import { getProducts } from "@/lib/data";
import { ProductWithVariants } from "@/types/product";
import { CATEGORIES } from "@/lib/constants";

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

  // Active category display title
  const activeCategory = CATEGORIES.find((c) => c.slug === filters.categorySlug);

  return (
    <div className="container py-8 md:py-12 flex flex-col gap-8">
      {/* Top Header */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2 text-xs text-[var(--accent-emerald)] font-mono uppercase tracking-wider">
          <span>Discovery Engine</span>
          <span>•</span>
          <span>Faceted Search</span>
        </div>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
              {activeCategory ? activeCategory.name : "All Protein Products"}
            </h1>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] mt-1">
              {activeCategory
                ? activeCategory.description
                : "Real cost-per-gram (₹/g), protein density %, and red-flag ingredient breakdown."}
            </p>
          </div>

          {/* Mobile Filter Toggle */}
          <button
            type="button"
            onClick={() => setMobileFilterOpen(true)}
            className="sm:hidden flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-[rgba(255,255,255,0.06)] border border-[rgba(255,255,255,0.1)] text-xs font-semibold text-white"
          >
            <span>⚙️</span>
            <span>Filters</span>
            {filters.proteinTiers?.length || filters.dietaryTags?.length || filters.zeroFlagsOnly ? (
              <span className="w-2 h-2 rounded-full bg-[var(--accent-emerald)]" />
            ) : null}
          </button>
        </div>
      </div>

      {/* Main Grid & Sidebar Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Desktop Sidebar */}
        <div className="hidden lg:block lg:col-span-1 sticky top-24">
          <FilterPanel
            filters={filters}
            onCategoryChange={setCategory}
            onToggleTier={toggleTier}
            onToggleTag={toggleTag}
            onToggleAllergen={toggleAllergen}
            onSetZeroFlagsOnly={setZeroFlagsOnly}
            onClearFilters={clearFilters}
          />
        </div>

        {/* Product Results Column */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          {/* Results Bar */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-[rgba(18,18,26,0.5)] border border-[rgba(255,255,255,0.06)] backdrop-blur-md">
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-[var(--text-muted)]">
                Showing{" "}
                <strong className="text-white font-mono">{products.length}</strong>{" "}
                verified product{products.length === 1 ? "" : "s"}
              </span>
              {isPending && (
                <span className="text-xs text-[var(--accent-emerald)] animate-pulse">
                  Updating...
                </span>
              )}
            </div>

            <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
          </div>

          {/* Active Filter Badges */}
          {(filters.categorySlug ||
            filters.proteinTiers?.length ||
            filters.dietaryTags?.length ||
            filters.excludeAllergens?.length ||
            filters.zeroFlagsOnly) && (
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-[var(--text-faint)]">Active filters:</span>
              {filters.categorySlug && (
                <button
                  type="button"
                  onClick={() => setCategory(undefined)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-[rgba(0,212,170,0.15)] text-[#00d4aa] border border-[rgba(0,212,170,0.3)] hover:bg-[rgba(0,212,170,0.25)]"
                >
                  <span>Category: {activeCategory?.name || filters.categorySlug}</span>
                  <span>×</span>
                </button>
              )}
              {filters.zeroFlagsOnly && (
                <button
                  type="button"
                  onClick={() => setZeroFlagsOnly(false)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-[rgba(0,212,170,0.15)] text-[#00d4aa] border border-[rgba(0,212,170,0.3)] hover:bg-[rgba(0,212,170,0.25)]"
                >
                  <span>Zero Red Flags</span>
                  <span>×</span>
                </button>
              )}
              {filters.proteinTiers?.map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => toggleTier(t)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-[rgba(56,189,248,0.15)] text-[#38bdf8] border border-[rgba(56,189,248,0.3)] hover:bg-[rgba(56,189,248,0.25)]"
                >
                  <span>{t}</span>
                  <span>×</span>
                </button>
              ))}
              {filters.dietaryTags?.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleTag(tag)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-[rgba(139,92,246,0.15)] text-[#c084fc] border border-[rgba(139,92,246,0.3)] hover:bg-[rgba(139,92,246,0.25)]"
                >
                  <span>{tag}</span>
                  <span>×</span>
                </button>
              ))}
              {filters.excludeAllergens?.map((a) => (
                <button
                  key={a}
                  type="button"
                  onClick={() => toggleAllergen(a)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs bg-[rgba(239,68,68,0.15)] text-[#f87171] border border-[rgba(239,68,68,0.3)] hover:bg-[rgba(239,68,68,0.25)]"
                >
                  <span>No {a}</span>
                  <span>×</span>
                </button>
              ))}
              <button
                type="button"
                onClick={clearFilters}
                className="text-xs text-[var(--text-muted)] hover:text-white underline ml-1"
              >
                Reset all
              </button>
            </div>
          )}

          {/* Loading Skeletons */}
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div
                  key={i}
                  className="h-96 rounded-2xl skeleton-shimmer border border-[rgba(255,255,255,0.06)]"
                />
              ))}
            </div>
          ) : products.length === 0 ? (
            /* Empty State */
            <div className="flex flex-col items-center justify-center p-12 text-center rounded-2xl bg-[rgba(18,18,26,0.5)] border border-[rgba(255,255,255,0.06)] gap-4">
              <span className="text-4xl">🔍</span>
              <h3 className="text-lg font-bold text-white">No products match your criteria</h3>
              <p className="text-xs sm:text-sm text-[var(--text-muted)] max-w-sm">
                Try removing some allergen exclusions or dietary filters to broaden your search.
              </p>
              <Button onClick={clearFilters} variant="primary" size="sm">
                Clear Filters
              </Button>
            </div>
          ) : (
            /* Results Grid */
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
              {products.map((prod) => (
                <ProductCard key={prod.id} product={prod} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mobile Filters Drawer */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/80 backdrop-blur-sm lg:hidden animate-fade-in">
          <div className="w-full max-w-xs h-full bg-[#12121a] p-6 overflow-y-auto flex flex-col gap-4 border-l border-[rgba(255,255,255,0.1)]">
            <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-3">
              <span className="font-bold text-sm text-white">Filter Products</span>
              <button
                type="button"
                onClick={() => setMobileFilterOpen(false)}
                className="text-lg text-[var(--text-muted)] hover:text-white p-1"
              >
                ✕
              </button>
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
              className="border-0 p-0 bg-transparent"
            />
            <div className="mt-auto pt-4 border-t border-[rgba(255,255,255,0.08)]">
              <Button
                variant="primary"
                size="md"
                className="w-full"
                onClick={() => setMobileFilterOpen(false)}
              >
                Apply Filters ({products.length})
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
