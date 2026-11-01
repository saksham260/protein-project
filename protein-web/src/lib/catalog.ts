import { ProductWithVariants, ProductVariant } from "@/types/product";
import { featuredScore } from "@/lib/ranking";
import { passesAllergenExclusions } from "@/lib/allergens";
import {
  METRIC_RANGES,
  caloriesPerGramProtein,
  effectiveCostPerGram,
  passesRange,
  proteinPer100Inr,
} from "@/lib/metrics";
import { searchRank } from "@/lib/search";
import { canonicalDietaryTag } from "@/lib/utils";

// Filtering and sorting only. This file is shared with the browser, so it must never import the seed catalog.

export interface QueryFilters {
  categorySlug?: string;
  searchQuery?: string;
  proteinTiers?: string[];
  dietaryTags?: string[];
  veganOnly?: boolean;
  excludeAllergens?: string[];
  zeroFlagsOnly?: boolean;
  sortBy?: string;
  maxCostPerG?: number;
  minProteinPer100?: number;
  minProteinPer100Calories?: number;
  maxCaloriesPerGProtein?: number;
  minDensity?: number;
  /** Keep only products reported available on quick commerce near `pincode`. */
  nearMe?: boolean;
  /** The viewer's pincode (from local storage, never the URL). */
  pincode?: string;
}

export function normalizeTier(tier?: string | null): string {
  if (!tier) return "Tier 2";
  if (tier.startsWith("Tier 1")) return "Tier 1";
  if (tier.startsWith("Tier 2")) return "Tier 2";
  if (tier.startsWith("Tier 3")) return "Tier 3";
  if (tier.startsWith("Tier 4")) return "Tier 4";
  return tier;
}

function variantMatches(
  v: ProductVariant,
  filters: QueryFilters,
  availableNearIds: Set<string> | undefined,
  productIsVegan?: boolean
): boolean {
  if (filters.proteinTiers?.length) {
    const normTier = normalizeTier(v.protein_tier);
    if (
      !v.protein_tier ||
      (!filters.proteinTiers.includes(v.protein_tier) &&
        !filters.proteinTiers.includes(normTier))
    ) {
      return false;
    }
  }
  if (filters.dietaryTags?.length) {
    const normTags = v.dietary_tags.map(canonicalDietaryTag);
    if (
      !filters.dietaryTags.every((tag) => {
        const canonical = canonicalDietaryTag(tag);
        if (canonical === "vegan") {
          return Boolean(productIsVegan || normTags.includes("vegan"));
        }
        return normTags.includes(canonical);
      })
    ) {
      return false;
    }
  }
  if (!passesAllergenExclusions(v, filters.excludeAllergens)) return false;
  // With no ingredient list there was nothing to scan, so "no flags" proves nothing.
  if (filters.zeroFlagsOnly && ((v.red_flags && v.red_flags.length > 0) || v.ingredient_list.length === 0)) {
    return false;
  }
  if (!METRIC_RANGES.every((range) => passesRange(range, v, filters[range.key]))) return false;
  if (availableNearIds && !availableNearIds.has(v.id)) return false;
  return true;
}

function sortValue(p: ProductWithVariants, v: ProductVariant, sort: string): number {
  switch (sort) {
    case "featured":
      return featuredScore({
        productName: p.name,
        variantName: v.variant_name,
        isCombo: v.is_combo,
        brandName: p.brand?.name,
        costPerGram: effectiveCostPerGram(v),
      });
    case "density_desc":
      return -(v.protein_density_pct ?? 0);
    case "p100_desc":
      return -(proteinPer100Inr(v) ?? 0);
    case "kcal_per_g_asc":
      return caloriesPerGramProtein(v) ?? 999;
    case "best_price_asc":
      return v.best_price_inr ?? v.mrp_inr;
    case "price_asc":
      return v.mrp_inr;
    case "price_desc":
      return -v.mrp_inr;
    case "protein_desc":
      return -v.protein_g;
    case "cost_per_g_asc":
    default:
      return effectiveCostPerGram(v) ?? 999;
  }
}

/**
 * Filter and sort products. A product is kept when at least one variant passes every filter;
 * its first passing variant decides its sort position and is the one its card shows.
 * While searching, products matched by name or brand come before ingredient-only matches.
 */
export function applyFilters(
  products: ProductWithVariants[],
  filters: QueryFilters = {},
  availableNearIds?: Set<string>
): ProductWithVariants[] {
  const q = filters.searchQuery?.trim();
  const sort = filters.sortBy || "featured";

  const matches: { product: ProductWithVariants; key: number; rank: number }[] = [];
  for (const p of products) {
    if (filters.categorySlug && p.category?.slug !== filters.categorySlug) continue;
    if (filters.veganOnly) {
      const isVegan = Boolean(
        p.is_vegan ||
        p.variants.some((v) => v.dietary_tags?.some((t) => t.toLowerCase() === "vegan"))
      );
      if (!isVegan) continue;
    }
    const rank = q ? searchRank(p, q) : 2;
    if (rank === 0) continue;
    const variant = p.variants.find((v) =>
      variantMatches(v, filters, availableNearIds, p.is_vegan)
    );
    if (variant) {
      matches.push({
        product: { ...p, matched_variant_id: variant.id },
        key: sortValue(p, variant, sort),
        rank,
      });
    }
  }

  return matches.sort((a, b) => b.rank - a.rank || a.key - b.key).map((m) => m.product);
}
