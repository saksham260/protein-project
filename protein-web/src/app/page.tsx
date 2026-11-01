import React from "react";
import { getProducts, getTopPicks, toListProduct } from "@/lib/data";
import { HomeClient } from "@/app/HomeClient";

export const revalidate = 86400; // 24 hours ISR

export const metadata = { alternates: { canonical: "/" } };

/** Products sent with the page; the rest load when the visitor scrolls to them. */
const FIRST_BATCH = 12;

export default async function HomePage() {
  const [allProducts, topPicks] = await Promise.all([
    getProducts(),
    getTopPicks(),
  ]);

  const categoryCounts: Record<string, number> = {};
  for (const product of allProducts) {
    const slug = product.category?.slug;
    if (slug) categoryCounts[slug] = (categoryCounts[slug] ?? 0) + 1;
  }

  return (
    <HomeClient
      initialProducts={allProducts.slice(0, FIRST_BATCH).map(toListProduct)}
      totalProducts={allProducts.length}
      categoryCounts={categoryCounts}
      topPicks={topPicks.map((pick) => ({ ...pick, product: toListProduct(pick.product) }))}
    />
  );
}
