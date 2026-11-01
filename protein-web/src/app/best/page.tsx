import React from "react";
import Link from "next/link";
import { InfoPage } from "@/components/layout/InfoPage";
import { BEST_LISTS } from "@/lib/bestLists";
import { SITE_NAME } from "@/lib/site";

export const metadata = {
  title: `Best Value Protein Lists — ${SITE_NAME}`,
  description: "Protein products in India ranked by cost per gram of protein, using label data and known store prices.",
  alternates: { canonical: "/best" },
};

export default function BestListsPage() {
  return (
    <InfoPage title="Best Value Lists">
      <p>
        Each list ranks products by cost per gram of protein. Only in-stock products with an ingredient list and no label
        red flags can appear. No brand can pay to be on a list.
      </p>
      <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {BEST_LISTS.map((list) => (
          <li key={list.slug}>
            <Link
              href={`/best/${list.slug}`}
              className="flex flex-col gap-1 h-full p-4 rounded-2xl bg-[#1C1916] border border-[#332D27] hover:border-[#D97706]/70 transition-colors"
            >
              <span className="text-sm font-bold text-[#F5F2EB]">{list.name}</span>
              <span className="text-xs text-[#968E85]">{list.rule}</span>
            </Link>
          </li>
        ))}
      </ul>
    </InfoPage>
  );
}
