"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { SearchBar } from "@/components/search/SearchBar";
import { ProductCard } from "@/components/product/ProductCard";
import { Button } from "@/components/ui/Button";
import { getProducts } from "@/lib/data";
import { ProductWithVariants } from "@/types/product";

export function SearchClient() {
  const searchParams = useSearchParams();
  const queryParam = searchParams.get("q") || "";

  const [products, setProducts] = useState<ProductWithVariants[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const timer = setTimeout(() => {
      setLoading(true);
      getProducts({ searchQuery: queryParam })
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
  }, [queryParam]);

  return (
    <div className="container py-8 md:py-12 flex flex-col gap-10 max-w-5xl mx-auto">
      {/* Search Header */}
      <div className="flex flex-col items-center text-center gap-4">
        <span className="text-xs font-mono uppercase tracking-widest text-[var(--accent-emerald)]">
          Search Database
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          Find Any Protein Product in India
        </h1>
        <p className="text-xs sm:text-sm text-[var(--text-muted)] max-w-md">
          Search by brand name (e.g. MuscleBlaze, The Whole Truth, Amul), protein source, or
          specific product keywords.
        </p>

        <div className="w-full max-w-2xl mt-2">
          <SearchBar initialValue={queryParam} autoFocus={!queryParam} />
        </div>
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-4">
        <div className="text-xs text-[var(--text-secondary)]">
          {queryParam ? (
            <span>
              Showing results for &quot;<strong className="text-white">{queryParam}</strong>&quot;:
            </span>
          ) : (
            <span>All verified catalog products:</span>
          )}
        </div>
        <span className="text-xs font-mono text-[var(--accent-emerald)] font-bold">
          {products.length} match{products.length === 1 ? "" : "es"}
        </span>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-96 rounded-2xl skeleton-shimmer" />
          ))}
        </div>
      ) : products.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-16 text-center rounded-2xl bg-[rgba(18,18,26,0.5)] border border-[rgba(255,255,255,0.06)] gap-4">
          <span className="text-4xl">🔎</span>
          <h3 className="text-lg font-bold text-white">No matching products found</h3>
          <p className="text-xs sm:text-sm text-[var(--text-muted)] max-w-sm">
            We couldn&apos;t find any verified protein products matching &quot;{queryParam}&quot;. Try searching
            for &quot;whey&quot;, &quot;bar&quot;, or &quot;amul&quot;.
          </p>
          <Button href="/explore" variant="primary" size="sm">
            Browse All Products
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
  );
}
