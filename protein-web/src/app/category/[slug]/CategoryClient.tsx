"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { FilterPanel } from "@/components/search/FilterPanel";
import { SortDropdown } from "@/components/search/SortDropdown";
import { ProductCard } from "@/components/product/ProductCard";
import { Button } from "@/components/ui/Button";
import { useFilters } from "@/hooks/useFilters";
import { getProducts } from "@/lib/data";
import { ProductWithVariants } from "@/types/product";

export interface CategoryClientProps {
  category: {
    name: string;
    slug: string;
    description: string;
    icon: string;
  };
  initialProducts: ProductWithVariants[];
}

export function CategoryClient({ category, initialProducts }: CategoryClientProps) {
  const {
    filters,
    isPending,
    toggleTier,
    toggleTag,
    toggleAllergen,
    setZeroFlagsOnly,
    setSortBy,
    clearFilters,
  } = useFilters();

  const [products, setProducts] = useState<ProductWithVariants[]>(initialProducts);
  const [loading, setLoading] = useState(false);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  const activeFiltersCount = useMemo(() => {
    return (
      (filters.proteinTiers?.length || 0) +
      (filters.dietaryTags?.length || 0) +
      (filters.excludeAllergens?.length || 0) +
      (filters.zeroFlagsOnly ? 1 : 0)
    );
  }, [filters]);

  useEffect(() => {
    let isMounted = true;

    getProducts({
      ...filters,
      categorySlug: category.slug,
    })
      .then((data) => {
        if (isMounted) {
          setProducts(data);
        }
      })
      .catch(() => {});

    return () => {
      isMounted = false;
    };
  }, [filters, category.slug]);

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex flex-col gap-8">
      {/* Minimalist Breadcrumb */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#968E85]">
        <Link href="/" className="hover:text-[#F5F2EB] transition-colors">
          Home
        </Link>
        <span>/</span>
        <span className="text-[#968E85]">Categories</span>
        <span>/</span>
        <span className="text-[#F5F2EB] font-bold">{category.name}</span>
      </nav>

      {/* Category Hero Header */}
      <div className="flex flex-col gap-4 p-6 sm:p-8 rounded-2xl sm:rounded-3xl bg-[#1C1916] border border-[#332D27] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
        <div className="flex items-center gap-4 sm:gap-5">
          <span className="text-3xl sm:text-5xl">{category.icon}</span>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-[#D97706]">
                Form Factor Category
              </span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-black text-[#F5F2EB] tracking-tight mt-0.5">
              {category.name}
            </h1>
            <p className="text-xs sm:text-sm text-[#968E85] mt-1 max-w-2xl font-sans">
              {category.description}
            </p>
          </div>
        </div>
      </div>

      {/* Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 items-start min-h-[85vh]">
        {/* Scoped Desktop Sidebar with all filters */}
        <aside className="hidden lg:block lg:col-span-3 sticky top-24 max-h-[calc(100vh-7rem)] overflow-y-auto pr-1.5 custom-scrollbar overscroll-contain">
          <FilterPanel
            filters={filters}
            hideCategoryFilter
            onToggleTier={toggleTier}
            onToggleTag={toggleTag}
            onToggleAllergen={toggleAllergen}
            onSetZeroFlagsOnly={setZeroFlagsOnly}
            onClearFilters={clearFilters}
          />
        </aside>

        {/* Results Area */}
        <div className="lg:col-span-9 flex flex-col gap-6 min-h-[75vh]">
          <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#332D27]/80">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono uppercase tracking-wider text-[#968E85]">
                Verified
              </span>
              <span className="text-xs font-mono font-bold text-[#F5F2EB] px-2.5 py-0.5 rounded-full bg-[#1C1916] border border-[#332D27]">
                {products.length} Products
              </span>
              {isPending && (
                <span className="text-xs font-mono text-[#D97706] animate-pulse">
                  Updating...
                </span>
              )}
            </div>

            <div className="flex items-center gap-2.5">
              {/* Mobile Filter Drawer Trigger */}
              <button
                type="button"
                onClick={() => setMobileFilterOpen(true)}
                className="lg:hidden flex items-center justify-center gap-1.5 px-3.5 py-2 rounded-full bg-[#1C1916] border border-[#332D27] text-xs font-mono text-[#F5F2EB] select-none shadow-sm cursor-pointer hover:border-[#D97706]/60 transition-colors"
              >
                <span>⚙️ Filters</span>
                {activeFiltersCount > 0 && (
                  <span className="px-1.5 py-0.2 rounded-full bg-[#D97706] text-black text-[10px] font-bold">
                    {activeFiltersCount}
                  </span>
                )}
              </button>

              {/* Sort Dropdown */}
              <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
            </div>
          </div>

          {loading ? (
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="h-[320px] sm:h-[460px] rounded-2xl sm:rounded-3xl bg-[#1C1916] border border-[#332D27] skeleton-shimmer" />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-16 text-center rounded-3xl bg-[#1C1916] border border-[#332D27] gap-4">
              <span className="text-4xl">🔍</span>
              <h3 className="text-lg font-bold text-[#F5F2EB] tracking-tight">No products match these filters</h3>
              <p className="text-xs font-mono text-[#968E85]">Try unchecking some filter criteria or clearing them.</p>
              <Button onClick={clearFilters} variant="primary" size="sm">
                Clear Filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-6 animate-fade-in">
              {products.map((prod) => (
                <ProductCard key={prod.id} product={prod} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mobile Bottom Filter Drawer */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end bg-black/80 backdrop-blur-sm lg:hidden animate-fade-in">
          <div className="w-full max-h-[85vh] bg-[#1C1916] rounded-t-3xl border-t border-[#332D27] p-6 overflow-y-auto flex flex-col gap-5 shadow-[0_-20px_60px_rgba(0,0,0,0.9)] animate-slide-up">
            {/* Sheet Handle & Header */}
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-1.5 rounded-full bg-[#332D27]" />
              <div className="w-full flex items-center justify-between pb-3 border-b border-[#332D27]">
                <span className="font-mono text-sm uppercase tracking-widest text-[#F5F2EB] font-bold">
                  {category.name} Filters
                </span>
                <button
                  type="button"
                  onClick={() => setMobileFilterOpen(false)}
                  className="w-8 h-8 rounded-full bg-[#332D27] flex items-center justify-center text-[#968E85] hover:text-[#F5F2EB] text-sm"
                  aria-label="Close filters"
                >
                  ✕
                </button>
              </div>
            </div>

            <FilterPanel
              filters={filters}
              hideCategoryFilter
              onToggleTier={toggleTier}
              onToggleTag={toggleTag}
              onToggleAllergen={toggleAllergen}
              onSetZeroFlagsOnly={setZeroFlagsOnly}
              onClearFilters={clearFilters}
              className="border-0 p-0 bg-transparent shadow-none"
            />

            <div className="sticky bottom-0 pt-4 bg-[#1C1916] border-t border-[#332D27]">
              <button
                type="button"
                className="w-full py-3.5 rounded-2xl bg-[#D97706] hover:bg-[#F59E0B] text-black font-mono font-bold text-sm shadow-[0_0_20px_rgba(217,119,6,0.3)] transition-all cursor-pointer"
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
