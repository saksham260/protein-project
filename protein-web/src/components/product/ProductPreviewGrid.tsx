import React from "react";
import { ProductCard } from "@/components/product/ProductCard";
import type { ProductWithVariants } from "@/types/product";

/**
 * Server-rendered first batch of products, used as the Suspense fallback on filterable pages.
 * Search engines and slow connections get real products instead of a loading skeleton.
 */
export const ProductPreviewGrid: React.FC<{ products: ProductWithVariants[] }> = ({ products }) => (
  <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 md:py-16">
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  </div>
);
