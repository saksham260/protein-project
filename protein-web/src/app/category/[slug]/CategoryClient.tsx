"use client";

import React, { useState, useEffect } from "react";
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

  useEffect(() => {
    let isMounted = true;

    const timer = setTimeout(() => {
      setLoading(true);
      getProducts({
        ...filters,
        categorySlug: category.slug,
      })
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
  }, [filters, category.slug]);

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 md:py-16 flex flex-col gap-10">
      {/* Minimalist Breadcrumb */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#A1A1AA]">
        <Link href="/" className="hover:text-white transition-colors">
          Home
        </Link>
        <span>/</span>
        <Link href="/explore" className="hover:text-white transition-colors">
          Categories
        </Link>
        <span>/</span>
        <span className="text-[#E4E4E7] font-bold">{category.name}</span>
      </nav>

      {/* Category Hero Header */}
      <div className="flex flex-col gap-4 p-8 sm:p-10 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
        <div className="flex items-center gap-5">
          <span className="text-4xl sm:text-5xl">{category.icon}</span>
          <div className="flex flex-col">
            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
              {category.name}
            </h1>
            <p className="text-xs sm:text-sm text-[#A1A1AA] mt-1 max-w-2xl font-sans">
              {category.description}
            </p>
          </div>
        </div>
      </div>

      {/* Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        {/* Scoped Sidebar */}
        <aside className="hidden lg:block lg:col-span-3 sticky top-24">
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
        <div className="lg:col-span-9 flex flex-col gap-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono uppercase tracking-wider text-[#A1A1AA]">
                Verified
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

            <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-[460px] rounded-3xl bg-[#18181B] border border-[#27272A] skeleton-shimmer" />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-16 text-center rounded-3xl bg-[#18181B] border border-[#27272A] gap-4">
              <span className="text-4xl">🔍</span>
              <h3 className="text-lg font-bold text-white tracking-tight">No products match these filters</h3>
              <Button onClick={clearFilters} variant="primary" size="sm">
                Clear Filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
              {products.map((prod) => (
                <ProductCard key={prod.id} product={prod} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
