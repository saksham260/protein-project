"use client";

import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { useCallback, useMemo, useTransition } from "react";
import { QueryFilters } from "@/lib/data";

export function useFilters() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();

  const filters: QueryFilters = useMemo(() => {
    const categorySlug = searchParams.get("category") || undefined;
    const sortBy = searchParams.get("sort") || "cost_per_g_asc";
    const proteinTiers = searchParams.getAll("tier").filter(Boolean);
    const dietaryTags = searchParams.getAll("tag").filter(Boolean);
    const excludeAllergens = searchParams.getAll("exclude_allergen").filter(Boolean);
    const zeroFlagsOnly = searchParams.get("clean") === "true";
    const searchQuery = searchParams.get("q") || undefined;

    return {
      categorySlug,
      sortBy,
      proteinTiers: proteinTiers.length > 0 ? proteinTiers : undefined,
      dietaryTags: dietaryTags.length > 0 ? dietaryTags : undefined,
      excludeAllergens: excludeAllergens.length > 0 ? excludeAllergens : undefined,
      zeroFlagsOnly,
      searchQuery,
    };
  }, [searchParams]);

  const updateUrl = useCallback(
    (params: URLSearchParams) => {
      startTransition(() => {
        router.push(`${pathname}?${params.toString()}`, { scroll: false });
      });
    },
    [router, pathname]
  );

  const setCategory = useCallback(
    (slug?: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (slug) {
        params.set("category", slug);
      } else {
        params.delete("category");
      }
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const toggleTier = useCallback(
    (tier: string) => {
      const params = new URLSearchParams(searchParams.toString());
      const current = params.getAll("tier");
      params.delete("tier");
      if (current.includes(tier)) {
        current.filter((t) => t !== tier).forEach((t) => params.append("tier", t));
      } else {
        [...current, tier].forEach((t) => params.append("tier", t));
      }
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const toggleTag = useCallback(
    (tag: string) => {
      const params = new URLSearchParams(searchParams.toString());
      const current = params.getAll("tag");
      params.delete("tag");
      if (current.includes(tag)) {
        current.filter((t) => t !== tag).forEach((t) => params.append("tag", t));
      } else {
        [...current, tag].forEach((t) => params.append("tag", t));
      }
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const toggleAllergen = useCallback(
    (allergen: string) => {
      const params = new URLSearchParams(searchParams.toString());
      const current = params.getAll("exclude_allergen");
      params.delete("exclude_allergen");
      if (current.includes(allergen)) {
        current.filter((a) => a !== allergen).forEach((a) => params.append("exclude_allergen", a));
      } else {
        [...current, allergen].forEach((a) => params.append("exclude_allergen", a));
      }
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const setZeroFlagsOnly = useCallback(
    (value: boolean) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set("clean", "true");
      } else {
        params.delete("clean");
      }
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const setSortBy = useCallback(
    (sort: string) => {
      const params = new URLSearchParams(searchParams.toString());
      params.set("sort", sort);
      updateUrl(params);
    },
    [searchParams, updateUrl]
  );

  const clearFilters = useCallback(() => {
    const params = new URLSearchParams();
    if (searchParams.get("category") && pathname.startsWith("/category")) {
      // Keep category on category-specific pages
      params.set("category", searchParams.get("category")!);
    }
    updateUrl(params);
  }, [searchParams, pathname, updateUrl]);

  return {
    filters,
    isPending,
    setCategory,
    toggleTier,
    toggleTag,
    toggleAllergen,
    setZeroFlagsOnly,
    setSortBy,
    clearFilters,
  };
}
