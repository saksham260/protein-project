"use client";

import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { logActivity } from "@/lib/activity";

/** Records that the signed-in user opened this product (once per browser session). Renders nothing. */
export function ProductViewTracker({ productId, variantId }: { productId: string; variantId?: string }) {
  const { user } = useAuth();
  const userId = user?.id;

  useEffect(() => {
    if (!userId) return;
    const key = `viewed:${userId}:${productId}`;
    try {
      if (sessionStorage.getItem(key)) return;
      sessionStorage.setItem(key, "1");
    } catch {
      // storage blocked: log anyway
    }
    void logActivity(userId, { productId, variantId, eventType: "view" });
  }, [userId, productId, variantId]);

  return null;
}
