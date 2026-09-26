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
        <div className="container py-12">
          <div className="h-12 w-full max-w-xl skeleton-shimmer mb-8 mx-auto rounded-2xl" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-80 skeleton-shimmer rounded-2xl" />
            ))}
          </div>
        </div>
      }
    >
      <SearchClient />
    </Suspense>
  );
}
