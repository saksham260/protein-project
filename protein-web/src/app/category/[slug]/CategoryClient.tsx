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
    <div className="container py-8 md:py-12 flex flex-col gap-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
        <Link href="/" className="hover:text-white">
          Home
        </Link>
        <span>/</span>
        <Link href="/explore" className="hover:text-white">
          Categories
        </Link>
        <span>/</span>
        <span className="text-[var(--accent-emerald)] font-semibold">{category.name}</span>
      </div>

      {/* Category Hero Header */}
      <div className="flex flex-col gap-4 p-8 rounded-3xl bg-gradient-to-r from-[rgba(18,18,26,0.9)] to-[rgba(26,26,38,0.7)] border border-[rgba(255,255,255,0.08)] backdrop-blur-xl">
        <div className="flex items-center gap-4">
          <span className="text-5xl filter drop-shadow">{category.icon}</span>
          <div className="flex flex-col">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white">{category.name}</h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1 max-w-2xl">
              {category.description}
            </p>
          </div>
        </div>
      </div>

      {/* Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Scoped Sidebar */}
        <div className="hidden lg:block lg:col-span-1 sticky top-24">
          <FilterPanel
            filters={filters}
            hideCategoryFilter
            onToggleTier={toggleTier}
            onToggleTag={toggleTag}
            onToggleAllergen={toggleAllergen}
            onSetZeroFlagsOnly={setZeroFlagsOnly}
            onClearFilters={clearFilters}
          />
        </div>

        {/* Results Area */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-[rgba(18,18,26,0.5)] border border-[rgba(255,255,255,0.06)]">
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-[var(--text-muted)]">
                Showing <strong className="text-white font-mono">{products.length}</strong>{" "}
                product{products.length === 1 ? "" : "s"} in {category.name}
              </span>
              {isPending && (
                <span className="text-xs text-[var(--accent-emerald)] animate-pulse">
                  Updating...
                </span>
              )}
            </div>

            <SortDropdown currentSort={filters.sortBy} onSortChange={setSortBy} />
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-96 rounded-2xl skeleton-shimmer" />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-12 text-center rounded-2xl bg-[rgba(18,18,26,0.5)] border border-[rgba(255,255,255,0.06)] gap-4">
              <span className="text-4xl">🔍</span>
              <h3 className="text-lg font-bold text-white">No products found with these filters</h3>
              <Button onClick={clearFilters} variant="primary" size="sm">
                Clear Filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
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
