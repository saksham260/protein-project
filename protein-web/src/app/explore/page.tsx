import React, { Suspense } from "react";
import { ProductPreviewGrid } from "@/components/product/ProductPreviewGrid";
import { getProducts, toListProduct } from "@/lib/data";
import { ExploreClient } from "./ExploreClient";

export const revalidate = 3600; // 1 hour ISR

/** Rendered into the page's HTML for search engines; the full catalog loads in the browser. */
const FIRST_BATCH = 24;

export const metadata = {
  title: "Explore Protein Products — Transparent Comparison & Filter Grid",
  description:
    "Filter and rank Indian protein powders, bars, and drinks by cost per gram (₹/g), protein density, tiers, dietary preferences, and label red flags.",
  alternates: { canonical: "/explore" },
};

export default async function ExplorePage() {
  const firstProducts = (await getProducts()).slice(0, FIRST_BATCH).map(toListProduct);

  return (
    <Suspense fallback={<ProductPreviewGrid products={firstProducts} />}>
      <ExploreClient initialProducts={firstProducts} />
    </Suspense>
  );
}
