import React from "react";
import { getProducts, getTopPicks } from "@/lib/data";
import { HomeClient } from "@/app/HomeClient";

export const revalidate = 86400; // 24 hours ISR

export default async function HomePage() {
  const [allProducts, topPicks] = await Promise.all([
    getProducts(),
    getTopPicks(),
  ]);

  return <HomeClient initialProducts={allProducts} topPicks={topPicks} />;
}
