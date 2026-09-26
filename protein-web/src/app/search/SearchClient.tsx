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
    <div className="container max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20 flex flex-col gap-12">
      {/* Search Header */}
      <div className="flex flex-col items-center text-center gap-4">
        <span className="text-xs font-mono uppercase tracking-widest text-[#10B981] font-bold">
          Database Search
        </span>
        <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
          Find Any Protein Product in India
        </h1>
        <p className="text-xs sm:text-sm text-[#A1A1AA] max-w-lg leading-relaxed font-sans">
          Search by brand name (e.g. MuscleBlaze, The Whole Truth, Amul), protein source, or
          formulation keywords.
        </p>

        <div className="w-full max-w-2xl mt-4">
          <SearchBar initialValue={queryParam} autoFocus={!queryParam} />
        </div>
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between border-b border-[#27272A] pb-4 font-mono text-xs">
        <div className="text-[#A1A1AA]">
          {queryParam ? (
            <span>
              Matches for &quot;<strong className="text-white font-bold">{queryParam}</strong>&quot;:
            </span>
          ) : (
            <span>Verified catalog:</span>
          )}
        </div>
        <span className="font-bold text-[#10B981]">
          {products.length} {products.length === 1 ? "Product" : "Products"}
        </span>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-[460px] rounded-3xl bg-[#18181B] border border-[#27272A] skeleton-shimmer" />
          ))}
        </div>
      ) : products.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-16 text-center rounded-3xl bg-[#18181B] border border-[#27272A] gap-5">
          <span className="text-4xl">🔎</span>
          <h3 className="text-xl font-bold text-white tracking-tight">No matching products found</h3>
          <p className="text-xs sm:text-sm text-[#A1A1AA] max-w-sm font-sans">
            We couldn&apos;t find verified products matching &quot;{queryParam}&quot;. Try searching
            for &quot;whey&quot;, &quot;bar&quot;, or &quot;amul&quot;.
          </p>
          <Button href="/explore" variant="primary" size="sm">
            Browse All Products
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
  );
}
