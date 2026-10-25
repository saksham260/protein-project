import React, { Suspense } from "react";
import { SearchClient } from "./SearchClient";

export const metadata = {
  title: "Search Protein Products — Transparent Verification & Analysis",
  description:
    "Instant search across Indian protein powders, bars, and RTD drinks with nutrition facts, tiers, and ingredient scans.",
};

export default function SearchPage() {
  return (
    <Suspense
      fallback={
        <div className="container max-w-6xl mx-auto px-3 sm:px-6 lg:px-8 py-8 sm:py-12 md:py-20">
          <div className="h-12 w-full max-w-xl skeleton-shimmer mb-8 mx-auto rounded-2xl" />
          <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <div key={i} className="h-[320px] sm:h-[460px] skeleton-shimmer rounded-2xl sm:rounded-3xl" />
            ))}
          </div>
        </div>
      }
    >
      <SearchClient />
    </Suspense>
  );
}
