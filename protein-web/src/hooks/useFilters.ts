"use client";

import { useSearchParams, usePathname } from "next/navigation";
import { useCallback, useState, useEffect, useRef } from "react";
import { QueryFilters } from "@/lib/data";

function parseFiltersFromSearchParams(
  sp: URLSearchParams | { get: (k: string) => string | null; getAll: (k: string) => string[] }
): QueryFilters {
  const categorySlug = sp.get("category") || undefined;
  const sortBy = sp.get("sort") || "cost_per_g_asc";
  const proteinTiers = sp.getAll("tier").filter(Boolean);
  const dietaryTags = sp.getAll("tag").filter(Boolean);
  const excludeAllergens = sp.getAll("exclude_allergen").filter(Boolean);
  const zeroFlagsOnly = sp.get("clean") === "true";
  const searchQuery = sp.get("q") || undefined;

  return {
    categorySlug,
    sortBy,
    proteinTiers: proteinTiers.length > 0 ? proteinTiers : undefined,
    dietaryTags: dietaryTags.length > 0 ? dietaryTags : undefined,
    excludeAllergens: excludeAllergens.length > 0 ? excludeAllergens : undefined,
    zeroFlagsOnly,
    searchQuery,
  };
}

export function useFilters() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const [filters, setFilters] = useState<QueryFilters>(() => {
    return parseFiltersFromSearchParams(searchParams);
  });

  // Keep in sync when popstate occurs (browser back/forward)
  useEffect(() => {
    const onPopState = () => {
      const sp = new URLSearchParams(window.location.search);
      setFilters(parseFiltersFromSearchParams(sp));
    };
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  // Sync URL in useEffect to avoid calling history.replaceState during render
  const isFirstRender = useRef(true);
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    if (typeof window !== "undefined") {
      const params = new URLSearchParams();
      if (filters.categorySlug) params.set("category", filters.categorySlug);
      if (filters.sortBy && filters.sortBy !== "cost_per_g_asc") params.set("sort", filters.sortBy);
      if (filters.proteinTiers?.length) {
        filters.proteinTiers.forEach((t) => params.append("tier", t));
      }
      if (filters.dietaryTags?.length) {
        filters.dietaryTags.forEach((t) => params.append("tag", t));
      }
      if (filters.excludeAllergens?.length) {
        filters.excludeAllergens.forEach((a) => params.append("exclude_allergen", a));
      }
      if (filters.zeroFlagsOnly) params.set("clean", "true");
      if (filters.searchQuery) params.set("q", filters.searchQuery);

      const query = params.toString();
      const targetUrl = query ? `${window.location.pathname}?${query}` : window.location.pathname;
      window.history.replaceState(null, "", targetUrl);
    }
  }, [filters]);

  const updateFilters = useCallback(
    (updater: (prev: QueryFilters) => QueryFilters) => {
      setFilters(updater);
    },
    []
  );

  const setCategory = useCallback(
    (slug?: string) => {
      updateFilters((prev) => ({
        ...prev,
        categorySlug: slug || undefined,
      }));
    },
    [updateFilters]
  );

  const toggleTier = useCallback(
    (tier: string) => {
      updateFilters((prev) => {
        const current = prev.proteinTiers || [];
        const nextTiers = current.includes(tier)
          ? current.filter((t) => t !== tier)
          : [...current, tier];
        return {
          ...prev,
          proteinTiers: nextTiers.length > 0 ? nextTiers : undefined,
        };
      });
    },
    [updateFilters]
  );

  const toggleTag = useCallback(
    (tag: string) => {
      updateFilters((prev) => {
        const current = prev.dietaryTags || [];
        const nextTags = current.includes(tag)
          ? current.filter((t) => t !== tag)
          : [...current, tag];
        return {
          ...prev,
          dietaryTags: nextTags.length > 0 ? nextTags : undefined,
        };
      });
    },
    [updateFilters]
  );

  const toggleAllergen = useCallback(
    (allergen: string) => {
      updateFilters((prev) => {
        const current = prev.excludeAllergens || [];
        const nextAllergens = current.includes(allergen)
          ? current.filter((a) => a !== allergen)
          : [...current, allergen];
        return {
          ...prev,
          excludeAllergens: nextAllergens.length > 0 ? nextAllergens : undefined,
        };
      });
    },
    [updateFilters]
  );

  const setZeroFlagsOnly = useCallback(
    (value: boolean) => {
      updateFilters((prev) => ({
        ...prev,
        zeroFlagsOnly: value,
      }));
    },
    [updateFilters]
  );

  const setSortBy = useCallback(
    (sort: string) => {
      updateFilters((prev) => ({
        ...prev,
        sortBy: sort,
      }));
    },
    [updateFilters]
  );

  const clearFilters = useCallback(() => {
    updateFilters((prev) => ({
      categorySlug: pathname.startsWith("/category") ? prev.categorySlug : undefined,
      sortBy: "cost_per_g_asc",
      proteinTiers: undefined,
      dietaryTags: undefined,
      excludeAllergens: undefined,
      zeroFlagsOnly: false,
      searchQuery: undefined,
    }));
  }, [pathname, updateFilters]);

  return {
    filters,
    isPending: false,
    setCategory,
    toggleTier,
    toggleTag,
    toggleAllergen,
    setZeroFlagsOnly,
    setSortBy,
    clearFilters,
  };
}
