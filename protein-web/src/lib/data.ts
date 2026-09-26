import { ProductWithVariants, ProductVariant, Platform, FlagSeverity } from "@/types/product";
import { CATEGORIES } from "@/lib/constants";
import rawSeedData from "@/data/seedCatalog.json";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { getAvailabilitySummaries, isReportedAvailable } from "@/lib/availability";
import {
  METRIC_RANGES,
  caloriesPerGramProtein,
  effectiveCostPerGram,
  passesRange,
  proteinPer100Inr,
} from "@/lib/metrics";
import { AwardCategory, TOP_PICKS_CONFIG } from "@/lib/topPicksConfig";

interface RawSeedVariant {
  variant_name?: string;
  slug?: string;
  sku?: string | null;
  barcode_ean?: string | null;
  mrp_inr: number;
  net_weight_g: number;
  serving_size_g: number;
  servings_per_pack?: number;
  serving_size_label?: string | null;
  nutrition?: {
    calories_kcal?: number;
    protein_g?: number;
    total_fat_g?: number;
    saturated_fat_g?: number;
    trans_fat_g?: number;
    cholesterol_mg?: number;
    total_carbs_g?: number;
    dietary_fiber_g?: number;
    total_sugars_g?: number;
    added_sugars_g?: number;
    non_glycemic_polyols_g?: number;
    sodium_mg?: number;
    additional_nutrients?: Record<string, unknown>;
  };
  ingredient_list?: string[];
  ingredient_deck_raw?: Array<{ name: string; position: number }>;
  allergens?: string[];
  dietary_tags?: string[];
  protein_profile?: {
    primary_protein_source?: string;
    protein_tier?: string;
    has_added_free_form_aminos?: boolean;
  };
  computed_metrics?: {
    cost_per_g_protein?: number;
    protein_density_pct?: number;
    true_net_carbs_g?: number;
    best_price_inr?: number | null;
    best_cost_per_g_protein?: number | null;
  };
  image_url?: string | null;
  red_flags?: Array<{
    flag_type: string;
    flag_severity: FlagSeverity;
    flag_label: string;
    flag_description: string;
    matched_ingredient?: string | null;
    ins_number?: string | null;
  }>;
  redirect_links?: Array<{
    platform: Platform;
    url: string;
    platform_price_inr?: number | null;
  }>;
}

interface RawSeedProduct {
  name: string;
  brand_name: string;
  category_slug: string;
  slug: string;
  description?: string | null;
  image_url?: string | null;
  variants?: RawSeedVariant[];
}

// Transform raw seed data to ProductWithVariants format
const normalizedSeedCatalog: ProductWithVariants[] = (rawSeedData as RawSeedProduct[]).map(
  (p, idx) => {
    const category = CATEGORIES.find((c) => c.slug === p.category_slug) || {
      name: "General",
      slug: p.category_slug,
      description: "",
      icon: "⚡",
    };

    const brand = {
      id: `brand-${idx}`,
      name: p.brand_name,
      slug: p.brand_name.toLowerCase().replace(/\s+/g, "-"),
      logo_url: null,
      website_url: null,
      description: null,
      is_verified: true,
      created_at: new Date().toISOString(),
    };

    const variants = (p.variants || []).map((v, vIdx) => {
      let tier = v.protein_profile?.protein_tier || "Tier 2";
      if (tier.startsWith("Tier 1")) tier = "Tier 1";
      else if (tier.startsWith("Tier 2")) tier = "Tier 2";
      else if (tier.startsWith("Tier 3")) tier = "Tier 3";
      else if (tier.startsWith("Tier 4")) tier = "Tier 4";

      return {
        id: `variant-${idx}-${vIdx}`,
        product_id: `product-${idx}`,
        variant_name: v.variant_name || p.name,
        slug: v.slug || `${p.slug}-${vIdx}`,
        sku: v.sku || null,
        barcode_ean: v.barcode_ean || null,
        mrp_inr: v.mrp_inr,
        net_weight_g: v.net_weight_g,
        serving_size_g: v.serving_size_g,
        servings_per_pack: v.servings_per_pack || 1,
        serving_size_label: v.serving_size_label || null,
        calories_kcal: v.nutrition?.calories_kcal || 0,
        protein_g: v.nutrition?.protein_g || 0,
        total_fat_g: v.nutrition?.total_fat_g || 0,
        saturated_fat_g: v.nutrition?.saturated_fat_g || 0,
        trans_fat_g: v.nutrition?.trans_fat_g || 0,
        cholesterol_mg: v.nutrition?.cholesterol_mg || 0,
        total_carbs_g: v.nutrition?.total_carbs_g || 0,
        dietary_fiber_g: v.nutrition?.dietary_fiber_g || 0,
        total_sugars_g: v.nutrition?.total_sugars_g || 0,
        added_sugars_g: v.nutrition?.added_sugars_g || 0,
        non_glycemic_polyols_g: v.nutrition?.non_glycemic_polyols_g || 0,
        sodium_mg: v.nutrition?.sodium_mg || 0,
        additional_nutrients: v.nutrition?.additional_nutrients || {},
        ingredient_list: v.ingredient_list || [],
        ingredient_deck_raw: v.ingredient_deck_raw || [],
        allergens: v.allergens || [],
        dietary_tags: v.dietary_tags || [],
        primary_protein_source: v.protein_profile?.primary_protein_source || null,
        protein_tier: tier,
        has_added_free_form_aminos: !!v.protein_profile?.has_added_free_form_aminos,
        cost_per_g_protein: v.computed_metrics?.cost_per_g_protein ?? null,
        protein_density_pct: v.computed_metrics?.protein_density_pct ?? null,
        true_net_carbs_g: v.computed_metrics?.true_net_carbs_g ?? null,
        best_price_inr: v.computed_metrics?.best_price_inr ?? null,
        best_cost_per_g_protein: v.computed_metrics?.best_cost_per_g_protein ?? null,
        image_url:
          v.image_url ||
          (p.category_slug === "protein-powders"
            ? "/images/products/whey-protein-tub.jpg"
            : p.category_slug === "protein-bars"
            ? "/images/products/protein-bar-pack.jpg"
            : p.category_slug === "rtd-drinks"
            ? "/images/products/rtd-protein-drink.jpg"
            : "/images/products/savory-snack-pack.jpg"),
        is_active: true,
        last_verified_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        red_flags: (v.red_flags || []).map((rf, rfIdx) => ({
          id: `rf-${idx}-${vIdx}-${rfIdx}`,
          variant_id: `variant-${idx}-${vIdx}`,
          flag_type: rf.flag_type,
          flag_severity: rf.flag_severity,
          flag_label: rf.flag_label,
          flag_description: rf.flag_description,
          matched_ingredient: rf.matched_ingredient || null,
          ins_number: rf.ins_number || null,
          created_at: new Date().toISOString(),
        })),
        redirect_links: (v.redirect_links || []).map((rl, rlIdx) => ({
          id: `rl-${idx}-${vIdx}-${rlIdx}`,
          variant_id: `variant-${idx}-${vIdx}`,
          platform: rl.platform,
          url: rl.url,
          platform_price_inr: rl.platform_price_inr ?? null,
          price_last_checked: new Date().toISOString(),
          created_at: new Date().toISOString(),
        })),
      };
    });

    const defaultCategoryImages: Record<string, string> = {
      "protein-powders": "/images/products/whey-protein-tub.jpg",
      "protein-bars": "/images/products/protein-bar-pack.jpg",
      "rtd-drinks": "/images/products/rtd-protein-drink.jpg",
      "savory-snacks": "/images/products/savory-snack-pack.jpg",
    };

    const resolvedImage =
      p.image_url || defaultCategoryImages[p.category_slug] || "/images/products/whey-protein-tub.jpg";

    return {
      id: `product-${idx}`,
      brand_id: brand.id,
      category_id: category.slug,
      name: p.name,
      slug: p.slug,
      description: p.description || null,
      image_url: resolvedImage,
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      brand,
      category: {
        id: category.slug,
        name: category.name,
        slug: category.slug,
        description: category.description,
        icon: category.icon,
        display_order: idx,
      },
      variants,
    };
  }
);

export interface QueryFilters {
  categorySlug?: string;
  searchQuery?: string;
  proteinTiers?: string[];
  dietaryTags?: string[];
  excludeAllergens?: string[];
  zeroFlagsOnly?: boolean;
  sortBy?: string;
  maxCostPerG?: number;
  minProteinPer100?: number;
  maxCaloriesPerGProtein?: number;
  minDensity?: number;
  /** Keep only products reported available on quick commerce near `pincode`. */
  nearMe?: boolean;
  /** The viewer's pincode (from local storage, never the URL). */
  pincode?: string;
}

const PRODUCT_SELECT = `
  *,
  brand:brands(*),
  category:categories(*),
  variants:product_variants(
    *,
    red_flags:variant_red_flags(*),
    redirect_links:redirect_links(*)
  )
`;

async function loadCatalog(): Promise<ProductWithVariants[]> {
  if (isSupabaseConfigured()) {
    try {
      const { data, error } = await createClient()
        .from("products")
        .select(PRODUCT_SELECT)
        .eq("is_active", true);
      if (!error && data && data.length > 0) {
        return data as ProductWithVariants[];
      }
    } catch {
      // Fall back to seed catalog on connection error
    }
  }
  return normalizedSeedCatalog;
}

/** Variant ids reported available on any quick-commerce platform in the pincode's area. */
async function getVariantIdsAvailableNear(
  products: ProductWithVariants[],
  pincode: string
): Promise<Set<string>> {
  const variantIds = products.flatMap((p) => p.variants.map((v) => v.id));
  const summaries = await getAvailabilitySummaries(variantIds, pincode);
  return new Set(summaries.filter(isReportedAvailable).map((s) => s.variant_id));
}

function variantMatches(
  v: ProductVariant,
  filters: QueryFilters,
  availableNearIds: Set<string> | undefined
): boolean {
  if (filters.proteinTiers?.length && !(v.protein_tier && filters.proteinTiers.includes(v.protein_tier))) {
    return false;
  }
  if (filters.dietaryTags?.length) {
    const tags = v.dietary_tags.map((t) => t.toLowerCase());
    if (!filters.dietaryTags.every((tag) => tags.includes(tag.toLowerCase()))) return false;
  }
  if (filters.excludeAllergens?.length) {
    const excluded = filters.excludeAllergens.map((e) => e.toLowerCase());
    if (v.allergens.some((a) => excluded.includes(a.toLowerCase()))) return false;
  }
  if (filters.zeroFlagsOnly && v.red_flags && v.red_flags.length > 0) return false;
  if (!METRIC_RANGES.every((range) => passesRange(range, v, filters[range.key]))) return false;
  if (availableNearIds && !availableNearIds.has(v.id)) return false;
  return true;
}

function sortValue(v: ProductVariant, sort: string): number {
  switch (sort) {
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
 * its first passing variant decides its sort position.
 */
export function applyFilters(
  products: ProductWithVariants[],
  filters: QueryFilters = {},
  availableNearIds?: Set<string>
): ProductWithVariants[] {
  const q = filters.searchQuery?.toLowerCase().trim();
  const sort = filters.sortBy || "cost_per_g_asc";

  const matches: { product: ProductWithVariants; key: number }[] = [];
  for (const p of products) {
    if (filters.categorySlug && p.category?.slug !== filters.categorySlug) continue;
    if (
      q &&
      !(
        p.name.toLowerCase().includes(q) ||
        p.brand?.name.toLowerCase().includes(q) ||
        p.variants.some((v) => v.variant_name.toLowerCase().includes(q))
      )
    ) {
      continue;
    }
    const variant = p.variants.find((v) => variantMatches(v, filters, availableNearIds));
    if (variant) matches.push({ product: p, key: sortValue(variant, sort) });
  }

  return matches.sort((a, b) => a.key - b.key).map((m) => m.product);
}

export async function getProducts(filters?: QueryFilters): Promise<ProductWithVariants[]> {
  const catalog = await loadCatalog();
  const availableNearIds =
    filters?.nearMe && filters.pincode
      ? await getVariantIdsAvailableNear(catalog, filters.pincode)
      : undefined;
  return applyFilters(catalog, filters, availableNearIds);
}

export async function getProductBySlug(slug: string): Promise<ProductWithVariants | null> {
  if (isSupabaseConfigured()) {
    try {
      const { data, error } = await createClient()
        .from("products")
        .select(PRODUCT_SELECT)
        .eq("slug", slug)
        .single();
      if (!error && data) {
        return data as ProductWithVariants;
      }
    } catch {
      // Fall back to seed catalog
    }
  }

  return normalizedSeedCatalog.find((p) => p.slug === slug) || null;
}

export interface TopPickResult {
  award: AwardCategory;
  product: ProductWithVariants;
  editorialBlurb: string;
}

export async function getTopPicks(): Promise<TopPickResult[]> {
  const allProducts = await getProducts();
  const results: TopPickResult[] = [];

  for (const award of TOP_PICKS_CONFIG.awards) {
    if (award.manualOverride?.productSlug) {
      const matched = allProducts.find((p) => p.slug === award.manualOverride?.productSlug);
      if (matched) {
        results.push({
          award,
          product: matched,
          editorialBlurb: award.manualOverride.editorialBlurb || award.description,
        });
        continue;
      }
    }

    // Auto-rule calculation
    const rule = award.autoRule;
    const candidates = applyFilters(allProducts, {
      categorySlug: rule.categorySlug,
      sortBy: rule.sortBy || "cost_per_g_asc",
      zeroFlagsOnly: rule.requireZeroFlags,
      proteinTiers: rule.requireTier ? [rule.requireTier] : undefined,
    });

    if (candidates.length > 0) {
      results.push({
        award,
        product: candidates[0],
        editorialBlurb: award.description,
      });
    }
  }

  return results;
}
