import React, { Suspense } from "react";
import { notFound } from "next/navigation";
import { CATEGORIES } from "@/lib/constants";
import { getProducts } from "@/lib/data";
import { CategoryClient } from "./CategoryClient";

export const revalidate = 3600; // 1 hour ISR

export async function generateStaticParams() {
  return CATEGORIES.map((category) => ({
    slug: category.slug,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const category = CATEGORIES.find((c) => c.slug === slug);

  if (!category) {
    return { title: "Category Not Found" };
  }

  return {
    title: `${category.name} in India — Best Value, Protein Density & Transparency`,
    description: `${category.description} Ranked strictly by Cost per Gram (₹/g) and protein quality tier with red-flag detection.`,
  };
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const category = CATEGORIES.find((c) => c.slug === slug);

  if (!category) {
    notFound();
  }

  const initialProducts = await getProducts({ categorySlug: slug });

  return (
    <Suspense
      fallback={
        <div className="container py-12">
          <div className="h-10 w-64 skeleton-shimmer mb-4" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-80 skeleton-shimmer rounded-2xl" />
            ))}
          </div>
        </div>
      }
    >
      <CategoryClient category={category} initialProducts={initialProducts} />
    </Suspense>
  );
}
