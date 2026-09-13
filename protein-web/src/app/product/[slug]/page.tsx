import React from "react";
import { notFound } from "next/navigation";
import { getProductBySlug, getProducts } from "@/lib/data";
import { ProductDetail } from "@/components/product/ProductDetail";
import { formatPricePerGram } from "@/lib/utils";

export const revalidate = 3600; // 1 hour ISR

export async function generateStaticParams() {
  const products = await getProducts();
  return products.map((product) => ({
    slug: product.slug,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);

  if (!product) {
    return { title: "Product Not Found" };
  }

  const v = product.variants[0];
  const flagCount = v?.red_flags?.length || 0;
  const cost = v?.cost_per_g_protein ? formatPricePerGram(v.cost_per_g_protein) : "unrated";

  return {
    title: `${product.name} by ${product.brand.name} – Nutrition Facts, Red Flags & Price | Protein Engine`,
    description: `${product.name}: ${v?.protein_g || 0}g protein, ${cost}, ${v?.protein_density_pct || 0}% density. ${flagCount} red flags analyzed. Compare prices on Amazon, Blinkit, and Zepto.`,
  };
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);

  if (!product) {
    notFound();
  }

  return <ProductDetail product={product} />;
}
