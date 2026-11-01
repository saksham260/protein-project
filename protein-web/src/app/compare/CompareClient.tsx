"use client";

import React, { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { ImageWithFallback } from "@/components/ui/ImageWithFallback";
import { useCart } from "@/context/CartContext";
import { fetchCatalog } from "@/lib/catalogClient";
import {
  bestColumns,
  compareHref,
  compareKey,
  COMPARE_ROWS,
  findCompareItems,
  MAX_COMPARE,
  parseCompareKeys,
} from "@/lib/compare";
import { cn, splitProductName } from "@/lib/utils";
import type { ProductWithVariants } from "@/types/product";

export function CompareClient() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const keysParam = searchParams.get("v");
  const keys = useMemo(() => parseCompareKeys(keysParam), [keysParam]);
  const { items: cartItems } = useCart();

  const [catalog, setCatalog] = useState<ProductWithVariants[] | null>(null);
  const [loadFailed, setLoadFailed] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let isMounted = true;
    fetchCatalog()
      .then((products) => {
        if (isMounted) setCatalog(products);
      })
      .catch(() => {
        if (isMounted) setLoadFailed(true);
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const items = useMemo(() => (catalog ? findCompareItems(catalog, keys) : []), [catalog, keys]);

  const showKeys = (next: string[]) => {
    setCopied(false);
    router.replace(compareHref(next), { scroll: false });
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
    } catch {
      // Clipboard blocked: the address bar still has the link.
    }
  };

  const cartSuggestions = cartItems.flatMap((item) => {
    if (!item.variant) return [];
    const key = compareKey(item.product, item.variant);
    return keys.includes(key) ? [] : [{ key, label: `${item.product.brand?.name ?? ""} ${item.product.name}`.trim() }];
  });

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex flex-col gap-6">
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-[#968E85]">
        <Link href="/" className="hover:text-[#F5F2EB] transition-colors">
          Home
        </Link>
        <span>/</span>
        <span className="text-[#F5F2EB] font-bold">Compare</span>
      </nav>

      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl sm:text-4xl font-black text-[#F5F2EB] tracking-tight">Compare Products</h1>
          <p className="text-xs sm:text-sm text-[#968E85] mt-1">Up to {MAX_COMPARE} products side by side, from label data.</p>
        </div>
        {items.length > 0 && (
          <button
            type="button"
            onClick={copyLink}
            className="self-start sm:self-auto px-4 py-2 rounded-xl bg-[#1C1916] hover:bg-[#26221E] border border-[#332D27] text-xs font-mono font-bold text-[#F5F2EB] transition-colors cursor-pointer"
          >
            {copied ? "Link copied" : "Copy link to share"}
          </button>
        )}
      </div>

      {loadFailed && (
        <p role="alert" className="text-xs font-mono text-[#F87171]">
          Couldn&apos;t load the products. Please refresh the page.
        </p>
      )}

      {!catalog && !loadFailed && keys.length > 0 && (
        <div className="h-96 rounded-2xl bg-[#1C1916] border border-[#332D27] skeleton-shimmer" aria-hidden />
      )}

      {catalog && items.length === 0 && (
        <div className="flex flex-col items-center text-center gap-3 p-10 rounded-2xl bg-[#1C1916] border border-[#332D27]">
          <h2 className="text-lg font-bold text-[#F5F2EB]">Nothing to compare yet</h2>
          <p className="text-sm text-[#968E85] max-w-md">
            Add a few products to your cart, then choose Compare in the cart.
          </p>
          <Link href="/explore" className="text-xs font-mono font-bold text-[#D97706] hover:text-[#F59E0B]">
            Browse products →
          </Link>
        </div>
      )}

      {items.length > 0 && (
        <div className="overflow-x-auto rounded-2xl border border-[#332D27] bg-[#1C1916]">
          <table className="w-full min-w-[640px] border-collapse text-xs">
            <thead>
              <tr className="border-b border-[#332D27] align-top">
                <th scope="col" className="sticky left-0 z-10 bg-[#1C1916] p-3 text-left font-mono text-[#968E85] font-medium w-40">
                  <span className="sr-only">Detail</span>
                </th>
                {items.map(({ key, product, variant }) => {
                  const { baseName, packInfo } = splitProductName(product.name, variant.variant_name);
                  const image = variant.image_url || product.image_url;
                  return (
                    <th key={key} scope="col" className="p-3 text-left font-normal min-w-[160px]">
                      <div className="flex flex-col gap-2">
                        <div className="relative w-16 h-16 rounded-xl bg-[#141210] border border-[#332D27] overflow-hidden flex items-center justify-center">
                          {image && (
                            <ImageWithFallback src={image} alt="" fill sizes="64px" className="object-cover" fallback={<span>{product.category?.icon}</span>} />
                          )}
                        </div>
                        <span className="text-[11px] uppercase font-mono tracking-wider text-[#F59E0B] font-bold">
                          {product.brand?.name}
                        </span>
                        <Link href={`/product/${product.slug}`} className="text-sm font-bold text-[#F5F2EB] hover:text-[#F59E0B] leading-snug">
                          {baseName}
                        </Link>
                        <span className="text-[11px] font-mono text-[#968E85]">{packInfo ?? variant.variant_name}</span>
                        <button
                          type="button"
                          onClick={() => showKeys(keys.filter((k) => k !== key))}
                          aria-label={`Remove ${product.name} from comparison`}
                          className="self-start text-[11px] font-mono text-[#968E85] hover:text-red-400 cursor-pointer"
                        >
                          Remove
                        </button>
                      </div>
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {COMPARE_ROWS.map((row) => {
                const best = bestColumns(row, items);
                return (
                  <tr key={row.label} className="border-b border-[#332D27]/60 last:border-b-0">
                    <th scope="row" className="sticky left-0 z-10 bg-[#1C1916] p-3 text-left font-mono font-medium text-[#968E85]">
                      {row.label}
                    </th>
                    {items.map((item, column) => (
                      <td key={item.key} className={cn("p-3 font-mono", best.has(column) ? "text-[#34D399] font-bold" : "text-[#F5F2EB]")}>
                        {row.kind === "number" ? row.format(row.value(item)) : row.value(item)}
                        {best.has(column) && <span className="ml-1.5 text-[9px] uppercase tracking-wider">Best</span>}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {items.length > 0 && items.length < MAX_COMPARE && cartSuggestions.length > 0 && (
        <div className="flex flex-col gap-2">
          <span className="text-xs font-mono text-[#968E85]">Add from your cart:</span>
          <div className="flex flex-wrap gap-2">
            {cartSuggestions.map(({ key, label }) => (
              <button
                key={key}
                type="button"
                onClick={() => showKeys([...keys, key])}
                className="px-3 py-1.5 rounded-full bg-[#1C1916] hover:bg-[#26221E] border border-[#332D27] text-xs font-mono text-[#F5F2EB] transition-colors cursor-pointer"
              >
                + {label}
              </button>
            ))}
          </div>
        </div>
      )}

      {items.length > 0 && (
        <p className="text-[11px] text-[#968E85] leading-relaxed">
          &quot;Best&quot; marks the better number in that row, not a better product. Figures come from labels and known store
          prices, which can change.{" "}
          <Link href="/how-we-rate" className="text-[#D97706] hover:underline">
            How we rate
          </Link>
        </p>
      )}
    </div>
  );
}
