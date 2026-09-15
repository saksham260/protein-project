import { ProductWithVariants, Platform, FlagSeverity } from "@/types/product";
import { CATEGORIES } from "@/lib/constants";
import rawSeedData from "@/data/seedCatalog.json";
import { createClient } from "@/lib/supabase/client";

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
}

export async function getProducts(filters?: QueryFilters): Promise<ProductWithVariants[]> {
  try {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    // If live Supabase credentials are configured and not placeholders, attempt Supabase query
    if (
      supabaseUrl &&
      !supabaseUrl.includes("placeholder") &&
      supabaseKey &&
      !supabaseKey.includes("placeholder")
    ) {
      const supabase = createClient();

      let query = supabase
        .from("products")
        .select(
          `
          *,
          brand:brands(*),
          category:categories(*),
          variants:product_variants(
            *,
            red_flags:variant_red_flags(*),
            redirect_links:redirect_links(*)
          )
        `
        )
        .eq("is_active", true);

      if (filters?.categorySlug) {
        query = query.eq("category.slug", filters.categorySlug);
      }

      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        return data as ProductWithVariants[];
      }
    }
  } catch {
    // Fall back to seed catalog on connection error
  }

  // Use normalized seed catalog with client-side filtering and sorting
  let list = [...normalizedSeedCatalog];

  if (filters?.categorySlug) {
    list = list.filter((p) => p.category.slug === filters.categorySlug);
  }

  if (filters?.searchQuery) {
    const q = filters.searchQuery.toLowerCase().trim();
    list = list.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.brand.name.toLowerCase().includes(q) ||
        p.variants.some((v) => v.variant_name.toLowerCase().includes(q))
    );
  }

  if (filters?.proteinTiers && filters.proteinTiers.length > 0) {
    list = list.filter((p) =>
      p.variants.some((v) => v.protein_tier && filters.proteinTiers?.includes(v.protein_tier))
    );
  }

  if (filters?.dietaryTags && filters.dietaryTags.length > 0) {
    list = list.filter((p) =>
      p.variants.some((v) =>
        filters.dietaryTags?.every((tag) =>
          v.dietary_tags.map((t) => t.toLowerCase()).includes(tag.toLowerCase())
        )
      )
    );
  }

  if (filters?.excludeAllergens && filters.excludeAllergens.length > 0) {
    list = list.filter((p) =>
      p.variants.some(
        (v) =>
          !v.allergens.some((a) =>
            filters.excludeAllergens?.map((e) => e.toLowerCase()).includes(a.toLowerCase())
          )
      )
    );
  }

  if (filters?.zeroFlagsOnly) {
    list = list.filter((p) =>
      p.variants.some((v) => !v.red_flags || v.red_flags.length === 0)
    );
  }

  // Sort logic
  const sort = filters?.sortBy || "cost_per_g_asc";
  list.sort((a, b) => {
    const vA = a.variants[0];
    const vB = b.variants[0];
    if (!vA || !vB) return 0;

    switch (sort) {
      case "cost_per_g_asc":
        return (vA.cost_per_g_protein ?? 999) - (vB.cost_per_g_protein ?? 999);
      case "density_desc":
        return (vB.protein_density_pct ?? 0) - (vA.protein_density_pct ?? 0);
      case "best_price_asc":
        return (vA.best_price_inr ?? vA.mrp_inr) - (vB.best_price_inr ?? vB.mrp_inr);
      case "price_asc":
        return vA.mrp_inr - vB.mrp_inr;
      case "price_desc":
        return vB.mrp_inr - vA.mrp_inr;
      case "protein_desc":
        return vB.protein_g - vA.protein_g;
      default:
        return (vA.cost_per_g_protein ?? 999) - (vB.cost_per_g_protein ?? 999);
    }
  });

  return list;
}

export async function getProductBySlug(slug: string): Promise<ProductWithVariants | null> {
  try {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    if (
      supabaseUrl &&
      !supabaseUrl.includes("placeholder") &&
      supabaseKey &&
      !supabaseKey.includes("placeholder")
    ) {
      const supabase = createClient();

      const { data, error } = await supabase
        .from("products")
        .select(
          `
          *,
          brand:brands(*),
          category:categories(*),
          variants:product_variants(
            *,
            red_flags:variant_red_flags(*),
            redirect_links:redirect_links(*)
          )
        `
        )
        .eq("slug", slug)
        .single();

      if (!error && data) {
        return data as ProductWithVariants;
      }
    }
  } catch {
    // Fall back to seed catalog
  }

  const found = normalizedSeedCatalog.find((p) => p.slug === slug);
  return found || null;
}
