import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import type { Platform } from "@/types/product";

export type ActivityType = "view" | "purchase_click";

export interface ActivityRow {
  product_id: string;
  event_type: ActivityType;
  platform: Platform | null;
  created_at: string;
}

export interface RecentProduct {
  productId: string;
  /** True when the person also clicked through to a purchase page for this product. */
  wentToBuy: boolean;
}

/** One entry per product, newest activity first, flagged if they ever clicked through to buy. */
export function recentProducts(rows: ActivityRow[], limit = 8): RecentProduct[] {
  const byProduct = new Map<string, RecentProduct>();
  const newestFirst = [...rows].sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  for (const row of newestFirst) {
    const existing = byProduct.get(row.product_id);
    if (!existing) {
      byProduct.set(row.product_id, { productId: row.product_id, wentToBuy: row.event_type === "purchase_click" });
    } else if (row.event_type === "purchase_click") {
      existing.wentToBuy = true;
    }
  }
  return [...byProduct.values()].slice(0, limit);
}

/** Save a product view or a click to a purchase page for the signed-in user. Fails quietly. */
export async function logActivity(
  userId: string,
  activity: { productId: string; variantId?: string; eventType: ActivityType; platform?: Platform }
): Promise<boolean> {
  if (!isSupabaseConfigured()) return false;
  const { error } = await createClient().from("user_activity").insert({
    user_id: userId,
    product_id: activity.productId,
    variant_id: activity.variantId ?? null,
    event_type: activity.eventType,
    platform: activity.platform ?? null,
  });
  return !error;
}

/** The signed-in user's latest activity rows (newest first). */
export async function getRecentActivity(userId: string, limit = 60): Promise<ActivityRow[]> {
  if (!isSupabaseConfigured()) return [];
  const { data, error } = await createClient()
    .from("user_activity")
    .select("product_id, event_type, platform, created_at")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })
    .limit(limit);
  return error || !data ? [] : (data as ActivityRow[]);
}
