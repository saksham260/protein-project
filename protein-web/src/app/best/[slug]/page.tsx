import React from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ProductCard } from "@/components/product/ProductCard";
import { BEST_LISTS, buildBestList } from "@/lib/bestLists";
import { getProducts, toListProduct } from "@/lib/data";
import { siteUrl } from "@/lib/site";

export const revalidate = 86400; // 24 hours ISR

export function generateStaticParams() {
  return BEST_LISTS.map((list) => ({ slug: list.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const list = BEST_LISTS.find((l) => l.slug === slug);
  if (!list) return { title: "List Not Found" };
  return {
    title: list.title,
    description: list.description,
    alternates: { canonical: `/best/${slug}` },
    openGraph: { title: list.title, description: list.description, type: "website" },
  };
}

export default async function BestListPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const list = BEST_LISTS.find((l) => l.slug === slug);
  if (!list) notFound();

  const products = buildBestList(await getProducts(), list).map(toListProduct);
  const updated = new Intl.DateTimeFormat("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "Asia/Kolkata",
  }).format(new Date());

  // "<" is escaped so product text can't close the script tag.
  const jsonLd = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: list.title,
    itemListElement: products.map((product, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: product.name,
      url: `${siteUrl()}/product/${product.slug}`,
    })),
  }).replace(/</g, "\\u003c");

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex flex-col gap-6">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd }} />

      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#968E85]">
        <Link href="/" className="hover:text-[#F5F2EB] transition-colors">
          Home
        </Link>
        <span>/</span>
        <Link href="/best" className="hover:text-[#F5F2EB] transition-colors">
          Best Value Lists
        </Link>
        <span>/</span>
        <span className="text-[#F5F2EB] font-bold">{list.name}</span>
      </nav>

      <header className="flex flex-col gap-2">
        <h1 className="text-2xl sm:text-4xl font-black text-[#F5F2EB] tracking-tight">{list.title}</h1>
        <p className="text-sm text-[#968E85] max-w-3xl leading-relaxed">
          {list.rule} Ranked from the lowest cost per gram of protein, showing each product&apos;s best-value pack. Only in-stock
          products with an ingredient list and no label red flags qualify.
        </p>
        <p className="text-xs font-mono text-[#968E85]">
          Updated {updated}.{" "}
          <Link href="/how-we-rate" className="text-[#D97706] hover:underline">
            How we rate
          </Link>
        </p>
      </header>

      {products.length === 0 ? (
        <p className="text-sm text-[#968E85]">No products qualify for this list right now.</p>
      ) : (
        <ol className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
          {products.map((product, index) => (
            <li key={product.id} className="relative h-full">
              <span className="absolute -top-2 -left-2 z-20 w-7 h-7 rounded-full bg-[#D97706] text-white text-xs font-mono font-black flex items-center justify-center shadow">
                {index + 1}
              </span>
              <ProductCard product={product} />
            </li>
          ))}
        </ol>
      )}

      <p className="text-[11px] text-[#968E85] leading-relaxed">
        Lowest cost isn&apos;t the same as best for you. These rankings use label data and known store prices, which can change.
        We may earn a commission on some store links, and that plays no part in these rankings.
      </p>
    </div>
  );
}
