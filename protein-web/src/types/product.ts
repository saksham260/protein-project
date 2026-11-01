export type ProteinTier = "Tier 1" | "Tier 2" | "Tier 3" | "Tier 4";

export type FlagSeverity = "high" | "amber" | "info";

export type Platform = "amazon" | "blinkit" | "zepto" | "instamart" | "d2c";

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo_url: string | null;
  website_url: string | null;
  description: string | null;
  is_verified: boolean;
  created_at: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  icon: string | null;
  display_order: number;
}

export interface VariantRedFlag {
  id: string;
  variant_id: string;
  flag_type: string;
  flag_severity: FlagSeverity;
  flag_label: string;
  flag_description: string;
  matched_ingredient: string | null;
  ins_number: string | null;
  created_at: string;
}

export interface RedirectLink {
  id: string;
  variant_id: string;
  platform: Platform;
  url: string;
  platform_price_inr: number | null;
  /** Null for seed-catalog prices, which were never checked by the price jobs. */
  price_last_checked: string | null;
  external_id?: string | null;
  in_stock?: boolean | null;
  created_at: string;
}

export type QuickCommercePlatform = "blinkit" | "zepto" | "instamart";

export interface AvailabilitySummary {
  variant_id: string;
  platform: QuickCommercePlatform;
  area_code: string;
  yes_count: number;
  no_count: number;
  last_reported_at: string;
}

/** A published lab report. It covers one tested batch, never the product as a whole. */
export interface TestReport {
  id: string;
  product_id: string;
  variant_id: string | null;
  source_type: "independent" | "brand";
  source_name: string;
  lab_name: string | null;
  batch_number: string | null;
  tested_on: string;
  result: "pass" | "partial" | "fail";
  tested_protein_g_per_100g: number | null;
  report_url: string;
}

export interface ProductVariant {
  id: string;
  product_id: string;
  variant_name: string;
  slug: string;
  sku: string | null;
  barcode_ean: string | null;
  mrp_inr: number;
  net_weight_g: number;
  serving_size_g: number;
  servings_per_pack: number;
  serving_size_label: string | null;
  calories_kcal: number;
  protein_g: number;
  total_fat_g: number;
  saturated_fat_g: number;
  trans_fat_g: number;
  cholesterol_mg: number;
  total_carbs_g: number;
  dietary_fiber_g: number;
  total_sugars_g: number;
  added_sugars_g: number;
  non_glycemic_polyols_g?: number;
  sodium_mg: number;
  additional_nutrients: Record<string, unknown>;
  ingredient_list: string[];
  ingredient_deck_raw: Array<{ name: string; position: number }>;
  allergens: string[];
  dietary_tags: string[];
  primary_protein_source: string | null;
  protein_tier: ProteinTier | string | null;
  has_added_free_form_aminos: boolean;
  cost_per_g_protein: number | null;
  protein_density_pct: number | null;
  true_net_carbs_g: number | null;
  best_price_inr?: number | null;
  best_cost_per_g_protein?: number | null;
  image_url: string | null;
  is_active: boolean;
  is_combo?: boolean;
  is_available?: boolean;
  last_verified_at: string;
  created_at: string;
  updated_at: string;
  red_flags?: VariantRedFlag[];
  redirect_links?: RedirectLink[];
}

export interface Product {
  id: string;
  brand_id: string;
  category_id: string;
  name: string;
  slug: string;
  description: string | null;
  image_url: string | null;
  is_active: boolean;
  is_vegan?: boolean;
  created_at: string;
  updated_at: string;
  /** The variant that satisfied the active filters; cards show this one instead of the default. */
  matched_variant_id?: string;
  brand?: Brand;
  category?: Category;
  variants?: ProductVariant[];
}

export interface ProductWithVariants extends Product {
  variants: ProductVariant[];
  brand: Brand;
  category: Category;
}
