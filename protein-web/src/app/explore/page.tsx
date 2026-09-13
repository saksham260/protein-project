import React, { Suspense } from "react";
import { ExploreClient } from "./ExploreClient";

export const metadata = {
  title: "Explore Protein Products — Transparent Comparison & Filter Grid",
  description:
    "Filter and rank Indian protein powders, bars, and drinks by cost per gram (₹/g), protein density, tiers, dietary preferences, and zero red flags.",
};

export default function ExplorePage() {
  return (
    <Suspense
      fallback={
        <div className="container py-12">
          <div className="h-8 w-48 skeleton-shimmer mb-6" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-80 skeleton-shimmer rounded-2xl" />
            ))}
          </div>
        </div>
      }
    >
      <ExploreClient />
    </Suspense>
  );
}
