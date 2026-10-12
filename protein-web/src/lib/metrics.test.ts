import { describe, it, expect } from "vitest";
import {
  effectiveCostPerGram,
  proteinPer100Inr,
  caloriesPerGramProtein,
  passesRange,
  METRIC_RANGES,
} from "./metrics";
import { ProductVariant } from "@/types/product";

function makeMockVariant(overrides: Partial<ProductVariant> = {}): ProductVariant {
  return {
    id: "v-1",
    product_id: "p-1",
    variant_name: "Test Variant",
    slug: "test-variant",
    sku: null,
    barcode_ean: null,
    mrp_inr: 150,
    net_weight_g: 50,
    serving_size_g: 50,
    servings_per_pack: 1,
    serving_size_label: null,
    calories_kcal: 200,
    protein_g: 25,
    total_fat_g: 5,
    saturated_fat_g: 1,
    trans_fat_g: 0,
    cholesterol_mg: 0,
    total_carbs_g: 10,
    dietary_fiber_g: 2,
    total_sugars_g: 1,
    added_sugars_g: 0,
    non_glycemic_polyols_g: 0,
    sodium_mg: 50,
    additional_nutrients: {},
    ingredient_list: ["whey protein isolate"],
    ingredient_deck_raw: [],
    allergens: ["milk"],
    dietary_tags: ["vegetarian"],
    primary_protein_source: "Whey Protein Isolate",
    protein_tier: "Tier 1",
    has_added_free_form_aminos: false,
    cost_per_g_protein: 7.5,
    best_price_inr: 120,
    best_cost_per_g_protein: 6.0,
    protein_density_pct: 50.0,
    true_net_carbs_g: 8.0,
    image_url: null,
    is_active: true,
    last_verified_at: new Date().toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    red_flags: [],
    redirect_links: [],
    ...overrides,
  };
}

describe("Suite 13: Client-side Metrics", () => {
  describe("effectiveCostPerGram", () => {
    it("returns best_cost_per_g_protein when present", () => {
      const v = makeMockVariant({ best_cost_per_g_protein: 5.5, cost_per_g_protein: 7.0 });
      expect(effectiveCostPerGram(v)).toBe(5.5);
    });

    it("falls back to cost_per_g_protein when best_cost is null", () => {
      const v = makeMockVariant({ best_cost_per_g_protein: null, cost_per_g_protein: 7.0 });
      expect(effectiveCostPerGram(v)).toBe(7.0);
    });

    it("returns null when both are null/undefined", () => {
      const v = makeMockVariant({ best_cost_per_g_protein: null, cost_per_g_protein: null });
      expect(effectiveCostPerGram(v)).toBeNull();
    });
  });

  describe("proteinPer100Inr", () => {
    it("calculates 100 / cost correctly", () => {
      const v = makeMockVariant({ best_cost_per_g_protein: 5.0 });
      expect(proteinPer100Inr(v)).toBe(20);
    });

    it("returns null when cost is 0 or null", () => {
      const vZero = makeMockVariant({ best_cost_per_g_protein: 0, cost_per_g_protein: 0 });
      expect(proteinPer100Inr(vZero)).toBeNull();

      const vNull = makeMockVariant({ best_cost_per_g_protein: null, cost_per_g_protein: null });
      expect(proteinPer100Inr(vNull)).toBeNull();
    });
  });

  describe("caloriesPerGramProtein", () => {
    it("calculates calories / protein correctly", () => {
      const v = makeMockVariant({ calories_kcal: 200, protein_g: 25 });
      expect(caloriesPerGramProtein(v)).toBe(8);
    });

    it("returns null when protein_g is 0", () => {
      const v = makeMockVariant({ calories_kcal: 200, protein_g: 0 });
      expect(caloriesPerGramProtein(v)).toBeNull();
    });

    it("returns null when calories_kcal is 0", () => {
      const v = makeMockVariant({ calories_kcal: 0, protein_g: 20 });
      expect(caloriesPerGramProtein(v)).toBeNull();
    });
  });

  describe("passesRange", () => {
    const maxCostConfig = METRIC_RANGES.find((r) => r.key === "maxCostPerG")!;
    const minDensityConfig = METRIC_RANGES.find((r) => r.key === "minDensity")!;

    it("returns true when limit is undefined", () => {
      const v = makeMockVariant();
      expect(passesRange(maxCostConfig, v, undefined)).toBe(true);
    });

    it("handles max bound correctly", () => {
      const v = makeMockVariant({ best_cost_per_g_protein: 6.0 });
      expect(passesRange(maxCostConfig, v, 7.0)).toBe(true);
      expect(passesRange(maxCostConfig, v, 5.0)).toBe(false);
      expect(passesRange(maxCostConfig, v, 6.0)).toBe(true);
    });

    it("handles min bound correctly", () => {
      const v = makeMockVariant({ protein_density_pct: 60.0 });
      expect(passesRange(minDensityConfig, v, 50.0)).toBe(true);
      expect(passesRange(minDensityConfig, v, 70.0)).toBe(false);
      expect(passesRange(minDensityConfig, v, 60.0)).toBe(true);
    });

    it("returns false when metric value is null and limit is active", () => {
      const v = makeMockVariant({ protein_density_pct: null });
      expect(passesRange(minDensityConfig, v, 40.0)).toBe(false);
    });
  });
});
