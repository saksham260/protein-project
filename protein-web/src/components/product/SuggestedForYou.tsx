"use client";

import React, { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ProductCard } from "@/components/product/ProductCard";
import { useAuth } from "@/context/AuthContext";
import { getRecentActivity, recentProducts, type RecentProduct } from "@/lib/activity";
import type { ProductWithVariants } from "@/types/product";

const cacheKey = (userId: string) => `suggested:v1:${userId}`;

/** Last list shown to this user, so the section can appear instantly on the next visit while fresh data loads. */
function readCache(userId: string): RecentProduct[] | null {
  try {
    const raw = localStorage.getItem(cacheKey(userId));
    return raw ? (JSON.parse(raw) as RecentProduct[]) : null;
  } catch {
    return null;
  }
}

function writeCache(userId: string, items: RecentProduct[]) {
  try {
    localStorage.setItem(cacheKey(userId), JSON.stringify(items));
  } catch {
    // storage blocked: the section simply loads fresh each time
  }
}

/** Home-page section for signed-in users: what they last viewed or clicked through to buy. Hidden when logged out. */
export const SuggestedForYou: React.FC<{ products: ProductWithVariants[] }> = ({ products }) => {
  const { user, isReady } = useAuth();
  const userId = user?.id;
  const [loaded, setLoaded] = useState<{ userId: string; recent: RecentProduct[] } | null>(null);

  // Only runs once a user exists (client side), so reading local storage here cannot cause a hydration mismatch.
  const cached = useMemo(() => (userId ? readCache(userId) : null), [userId]);

  useEffect(() => {
    if (!userId) return;
    let isMounted = true;
    getRecentActivity(userId).then((rows) => {
      if (!isMounted) return;
      const recent = recentProducts(rows);
      writeCache(userId, recent);
      setLoaded({ userId, recent });
    });
    return () => {
      isMounted = false;
    };
  }, [userId]);

  const recent = loaded && loaded.userId === userId ? loaded.recent : cached;

  const items = useMemo(() => {
    if (!recent) return null;
    const byId = new Map(products.map((p) => [p.id, p]));
    return recent.flatMap((r) => {
      const product = byId.get(r.productId);
      return product ? [{ product, wentToBuy: r.wentToBuy }] : [];
    });
  }, [recent, products]);

  if (!isReady || !user) return null;

  return (
    <section className="flex flex-col gap-4 sm:gap-6 pt-1">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 pb-3 border-b border-[#332D27]/70">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-base">✨</span>
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
              Picked up where you left off
            </span>
          </div>
          <h2 className="text-xl sm:text-3xl font-black text-[#F5F2EB] mt-0.5 tracking-tight">Suggested for You</h2>
        </div>
        <Link
          href="/explore"
          className="text-xs font-mono font-bold text-[#968E85] hover:text-[#F5F2EB] transition-colors flex items-center gap-1 self-start sm:self-auto"
        >
          <span>Explore Full Catalog</span>
          <span>→</span>
        </Link>
      </div>

      {items === null ? (
        // Holds the space while the list loads, so the page doesn't jump
        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch" aria-hidden>
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-72 rounded-2xl bg-[#1C1916] border border-[#332D27] skeleton-shimmer" />
          ))}
        </div>
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center text-center gap-3 p-8 rounded-2xl bg-[#1C1916] border border-[#332D27]">
          <p className="text-sm text-[#968E85] max-w-md font-sans">
            Nothing here yet. Open a few products and the ones you look at, or click through to buy, will show up here.
          </p>
          <Link href="/explore" className="text-xs font-mono font-bold text-[#D97706] hover:text-[#F59E0B]">
            Browse products →
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
          {items.map(({ product, wentToBuy }) => (
            <div key={`suggested-${product.id}`} className="relative h-full">
              {wentToBuy && (
                <span className="absolute top-2 right-2 z-20 px-2 py-0.5 rounded-full bg-[#D97706] text-white text-[10px] font-mono font-bold shadow">
                  Went to buy
                </span>
              )}
              <ProductCard product={product} />
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
