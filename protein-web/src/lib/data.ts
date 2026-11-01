import "server-only";
import { ProductWithVariants, Platform, FlagSeverity, TestReport } from "@/types/product";
import { CATEGORIES } from "@/lib/constants";
import rawSeedData from "@/data/seedCatalog.json";
import { applyFilters, normalizeTier, QueryFilters } from "@/lib/catalog";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { createAnonClient } from "@/lib/supabase/anon";
import { normalizeVariantFacts } from "@/lib/productFacts";
import { AwardCategory, TOP_PICKS_CONFIG } from "@/lib/topPicksConfig";
import { sortVariantsDefaultFirst } from "@/lib/utils";

// Server only: this file holds the seed catalog, which must never reach the browser bundle.
// Browser code reads the catalog through /api/catalog (see lib/catalogClient.ts).

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
  is_combo?: boolean;
  is_available?: boolean;
}

interface RawSeedProduct {
  name: string;
  brand_name: string;
  category_slug: string;
  slug: string;
  description?: string | null;
  image_url?: string | null;
  is_vegan?: boolean;
  variants?: RawSeedVariant[];
}

const defaultCategoryImages: Record<string, string> = {
  "protein-powders": "/images/products/whey-protein-tub.jpg",
  "protein-bars": "/images/products/protein-bar-pack.jpg",
  "rtd-drinks": "/images/products/rtd-protein-drink.jpg",
  "savory-snacks": "/images/products/savory-snack-pack.jpg",
  "protein-spreads": "/images/products/peanut-butter-jar.jpg",
  "breakfast-cereals": "/images/products/savory-snack-pack.jpg",
  "dairy": "/images/products/rtd-protein-drink.jpg",
  "cookies-baked": "/images/products/protein-bar-pack.jpg",
  "mass-gainers": "/images/products/whey-protein-tub.jpg",
  "adult-nutrition": "/images/products/whey-protein-tub.jpg",
  "staples": "/images/products/savory-snack-pack.jpg",
};

function normalizeLiveProduct(p: ProductWithVariants): ProductWithVariants {
  const normalizedVariants = (p.variants || []).map((v) =>
    normalizeVariantFacts({
      ...v,
      protein_tier: normalizeTier(v.protein_tier),
      is_combo: Boolean(v.is_combo),
      is_available: v.is_available ?? true,
    })
  );

  return {
    ...p,
    is_vegan: Boolean(p.is_vegan),
    variants: sortVariantsDefaultFirst(normalizedVariants),
  };
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
      is_verified: false,
      created_at: new Date().toISOString(),
    };

    const fallbackImage =
      defaultCategoryImages[p.category_slug] || "/images/products/whey-protein-tub.jpg";

    const variants = (p.variants || []).map((v, vIdx) => {
      const tier = normalizeTier(v.protein_profile?.protein_tier);

      return normalizeVariantFacts({
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
        image_url: v.image_url || fallbackImage,
        is_active: true,
        is_combo: Boolean(v.is_combo),
        is_available: v.is_available ?? true,
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
          price_last_checked: null,
          created_at: new Date().toISOString(),
        })),
      });
    });

    const resolvedImage = p.image_url || fallbackImage;

    return {
      id: `product-${idx}`,
      brand_id: brand.id,
      category_id: category.slug,
      name: p.name,
      slug: p.slug,
      description: p.description || null,
      image_url: resolvedImage,
      is_active: true,
      is_vegan: Boolean(p.is_vegan),
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
      variants: sortVariantsDefaultFirst(variants),
    };
  }
);

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

/**
 * The live catalog, or the seed catalog when no database is configured (local demos).
 * A database failure throws instead of falling back: cached pages keep their last good version,
 * rather than quietly swapping in old data.
 */
async function loadCatalog(): Promise<ProductWithVariants[]> {
  if (!isSupabaseConfigured()) return normalizedSeedCatalog;

  const { data, error } = await createAnonClient()
    .from("products")
    .select(PRODUCT_SELECT)
    .eq("is_active", true);
  if (error) throw new Error(`Could not load the catalog: ${error.message}`);
  return ((data ?? []) as unknown as ProductWithVariants[]).map(normalizeLiveProduct);
}

export async function getProducts(filters?: QueryFilters): Promise<ProductWithVariants[]> {
  return applyFilters(await loadCatalog(), filters);
}

export async function getProductBySlug(slug: string): Promise<ProductWithVariants | null> {
  if (!isSupabaseConfigured()) return normalizedSeedCatalog.find((p) => p.slug === slug) || null;

  const { data, error } = await createAnonClient()
    .from("products")
    .select(PRODUCT_SELECT)
    .eq("slug", slug)
    .eq("is_active", true)
    .maybeSingle();
  if (error) throw new Error(`Could not load product ${slug}: ${error.message}`);
  return data ? normalizeLiveProduct(data as unknown as ProductWithVariants) : null;
}

/** Newest first. Fetched separately, so a failure here can't take the product page down. */
export async function getTestReports(productId: string): Promise<TestReport[]> {
  if (!isSupabaseConfigured()) return [];

  const { data, error } = await createAnonClient()
    .from("test_reports")
    .select("*")
    .eq("product_id", productId)
    .order("tested_on", { ascending: false });
  return error || !data ? [] : (data as TestReport[]);
}

/** Drops what product cards and filters don't use, so lists stay small on the wire. */
export function toListProduct(p: ProductWithVariants): ProductWithVariants {
  return {
    ...p,
    description: null,
    variants: p.variants.map((v) => ({
      ...v,
      additional_nutrients: {},
      ingredient_deck_raw: [],
      red_flags: (v.red_flags ?? []).map((flag) => ({ ...flag, flag_description: "" })),
    })),
  };
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

    // A product can't win on a variant the store has run out of.
    const winner = candidates.find((p) =>
      p.variants.some((v) => v.id === p.matched_variant_id && v.is_available !== false)
    );
    if (winner) {
      results.push({
        award,
        product: winner,
        editorialBlurb: award.description,
      });
    }
  }

  return results;
}
