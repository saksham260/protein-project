import React, { Suspense } from "react";
import { notFound } from "next/navigation";
import { CATEGORIES } from "@/lib/constants";
import { ProductPreviewGrid } from "@/components/product/ProductPreviewGrid";
import { getProducts, toListProduct } from "@/lib/data";
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
    description: `${category.description} Compare by cost per gram (₹/g), protein source tier and label red flags.`,
    alternates: { canonical: `/category/${slug}` },
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

  const initialProducts = (await getProducts({ categorySlug: slug })).map(toListProduct);

  return (
    <Suspense fallback={<ProductPreviewGrid products={initialProducts.slice(0, 24)} />}>
      <CategoryClient category={category} initialProducts={initialProducts} />
    </Suspense>
  );
}
