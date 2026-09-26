import React from "react";
import { getTopPicks, getProducts } from "@/lib/data";
import { TopPicksClient } from "./TopPicksClient";

export const metadata = {
  title: "Top Picks of the Month — Independent Protein Engine Awards",
  description: "Hand-verified and ranked by real nutritional data. No sponsorships, zero brand bias.",
};

export const revalidate = 86400; // 24 hours ISR

export default async function TopPicksPage() {
  const [topPicks, allProducts] = await Promise.all([
    getTopPicks(),
    getProducts(),
  ]);

  return <TopPicksClient topPicks={topPicks} allProducts={allProducts} />;
}
