import React from "react";
import { notFound } from "next/navigation";
import { getProductBySlug, getProducts, getTestReports } from "@/lib/data";
import { ProductDetail } from "@/components/product/ProductDetail";
import { effectiveCostPerGram } from "@/lib/metrics";
import { isPriceFresh } from "@/lib/redirect";
import { siteUrl } from "@/lib/site";
import { formatPricePerGram } from "@/lib/utils";
import type { ProductWithVariants } from "@/types/product";

export const revalidate = 3600; // 1 hour ISR

/** Product details for search engines. Only brand-store prices are included: Amazon's expire within a day. */
function productJsonLd(product: ProductWithVariants) {
  const v = product.variants[0];
  const offer = v?.redirect_links?.find(
    (l) => l.platform === "d2c" && l.platform_price_inr && l.in_stock !== false && isPriceFresh(l)
  );
  const image = v?.image_url || product.image_url;

  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    brand: { "@type": "Brand", name: product.brand.name },
    category: product.category.name,
    url: `${siteUrl()}/product/${product.slug}`,
    ...(product.description && { description: product.description }),
    ...(image && { image: image.startsWith("http") ? image : `${siteUrl()}${image}` }),
    ...(offer && {
      offers: {
        "@type": "Offer",
        url: offer.url,
        price: offer.platform_price_inr,
        priceCurrency: "INR",
        availability: "https://schema.org/InStock",
      },
    }),
  };
}

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
  const costPerGram = v ? effectiveCostPerGram(v) : null;
  const cost = costPerGram ? formatPricePerGram(costPerGram) : "unrated";
  const title = `${product.name} by ${product.brand.name} – Nutrition Facts, Red Flags & Price | Protein Engine`;
  const description = `${product.name}: ${v?.protein_g || 0}g protein, ${cost}, ${v?.calories_kcal || 0} kcal. ${flagCount} label red flags. Find it on Amazon, Blinkit, and Zepto.`;
  const image = v?.image_url || product.image_url;

  return {
    title,
    description,
    alternates: { canonical: `/product/${slug}` },
    openGraph: { title, description, type: "website", ...(image && { images: [image] }) },
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

  const testReports = await getTestReports(product.id);

  // "<" is escaped so product text can't close the script tag.
  const jsonLd = JSON.stringify(productJsonLd(product)).replace(/</g, "\\u003c");

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd }} />
      <ProductDetail product={product} testReports={testReports} />
    </>
  );
}
