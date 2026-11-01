import React, { Suspense } from "react";
import { SITE_NAME } from "@/lib/site";
import { CompareClient } from "./CompareClient";

export const metadata = {
  title: `Compare Protein Products — ${SITE_NAME}`,
  description: "Compare protein products side by side on cost per gram, protein, sugars and label red flags.",
  // Every link is a different mix of products, so these pages don't belong in search results.
  robots: { index: false, follow: true },
};

export default function ComparePage() {
  return (
    <Suspense>
      <CompareClient />
    </Suspense>
  );
}
