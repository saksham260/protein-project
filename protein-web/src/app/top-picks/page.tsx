import React from "react";
import { getTopPicks, toListProduct } from "@/lib/data";
import { TopPicksClient } from "./TopPicksClient";

export const metadata = {
  title: "Top Value Picks — Lowest Cost per Gram by Category",
  description: "The lowest cost per gram of protein in each category, among in-stock products with no label red flags. Picked by formula.",
  alternates: { canonical: "/top-picks" },
};

export const revalidate = 86400; // 24 hours ISR

export default async function TopPicksPage() {
  const topPicks = await getTopPicks();

  return (
    <TopPicksClient topPicks={topPicks.map((pick) => ({ ...pick, product: toListProduct(pick.product) }))} />
  );
}
