import type { MetadataRoute } from "next";
import { BEST_LISTS } from "@/lib/bestLists";
import { CATEGORIES } from "@/lib/constants";
import { getProducts } from "@/lib/data";
import { siteUrl } from "@/lib/site";

export const revalidate = 3600; // 1 hour ISR

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = siteUrl();
  const products = await getProducts();
  const staticPaths = [
    "",
    "/explore",
    "/top-picks",
    "/best",
    "/protein-cost-calculator",
    "/how-we-rate",
    "/privacy",
    "/terms",
  ];

  return [
    ...staticPaths.map((path) => ({ url: `${base}${path}` })),
    ...CATEGORIES.map((category) => ({ url: `${base}/category/${category.slug}` })),
    ...BEST_LISTS.map((list) => ({ url: `${base}/best/${list.slug}` })),
    ...products.map((product) => ({ url: `${base}/product/${product.slug}`, lastModified: product.updated_at })),
  ];
}
