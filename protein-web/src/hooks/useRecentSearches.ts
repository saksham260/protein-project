"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import {
  clearSearches,
  deleteSearch,
  getRecentSearches,
  saveSearch,
  toRecentSearch,
  withSearchFirst,
  type RecentSearch,
} from "@/lib/searchHistory";

/** The signed-in user's recent searches. Empty (and a no-op) when logged out. */
export function useRecentSearches() {
  const { user } = useAuth();
  const userId = user?.id;
  const [loaded, setLoaded] = useState<{ userId: string; items: RecentSearch[] } | null>(null);

  useEffect(() => {
    if (!userId) return;
    let isMounted = true;
    getRecentSearches(userId).then((items) => {
      if (isMounted) setLoaded({ userId, items });
    });
    return () => {
      isMounted = false;
    };
  }, [userId]);

  const items = userId && loaded?.userId === userId ? loaded.items : [];

  const record = useCallback(
    (raw: string) => {
      const search = toRecentSearch(raw);
      if (!userId || !search) return;
      setLoaded((prev) => ({ userId, items: withSearchFirst(prev?.userId === userId ? prev.items : [], search) }));
      void saveSearch(userId, search);
    },
    [userId]
  );

  const remove = useCallback(
    (key: string) => {
      if (!userId) return;
      setLoaded((prev) => (prev?.userId === userId ? { userId, items: prev.items.filter((s) => s.key !== key) } : prev));
      void deleteSearch(userId, key);
    },
    [userId]
  );

  const clear = useCallback(() => {
    if (!userId) return;
    setLoaded({ userId, items: [] });
    void clearSearches(userId);
  }, [userId]);

  return { isSignedIn: Boolean(userId), items, record, remove, clear };
}
