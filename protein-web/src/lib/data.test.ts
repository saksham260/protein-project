import { describe, it, expect } from "vitest";
import { applyFilters, getProducts } from "./data";
import { ProductWithVariants } from "@/types/product";

function makeProduct(overrides: Partial<ProductWithVariants> = {}): ProductWithVariants {
  return {
    id: "p-1",
    brand_id: "b-1",
    category_id: "protein-powders",
    name: "Biozyme Whey Isolate",
    slug: "biozyme-whey-isolate",
    description: "High quality whey isolate",
    image_url: "/images/product.jpg",
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    brand: {
      id: "b-1",
      name: "MuscleBlaze",
      slug: "muscleblaze",
      logo_url: null,
      website_url: null,
      description: null,
      is_verified: true,
      created_at: new Date().toISOString(),
    },
    category: {
      id: "protein-powders",
      name: "Protein Powders",
      slug: "protein-powders",
      description: "Whey, plant, casein powders",
      icon: "⚡",
      display_order: 1,
    },
    variants: [
      {
        id: "v-1",
        product_id: "p-1",
        variant_name: "Rich Chocolate 1kg",
        slug: "rich-chocolate-1kg",
        sku: null,
        barcode_ean: null,
        mrp_inr: 3499,
        net_weight_g: 1000,
        serving_size_g: 31,
        servings_per_pack: 32,
        serving_size_label: "1 scoop (31g)",
        calories_kcal: 118,
        protein_g: 25,
        total_fat_g: 1,
        saturated_fat_g: 0.5,
        trans_fat_g: 0,
        cholesterol_mg: 10,
        total_carbs_g: 2,
        dietary_fiber_g: 0.5,
        total_sugars_g: 0,
        added_sugars_g: 0,
        non_glycemic_polyols_g: 0,
        sodium_mg: 60,
        additional_nutrients: {},
        ingredient_list: ["whey protein isolate", "cocoa powder"],
        ingredient_deck_raw: [],
        allergens: ["milk"],
        dietary_tags: ["vegetarian", "gluten-free"],
        primary_protein_source: "Whey Protein Isolate",
        protein_tier: "Tier 1",
        has_added_free_form_aminos: false,
        cost_per_g_protein: 4.37,
        best_price_inr: 3199,
        best_cost_per_g_protein: 4.0,
        protein_density_pct: 84.75,
        true_net_carbs_g: 1.5,
        image_url: null,
        is_active: true,
        last_verified_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        red_flags: [],
        redirect_links: [],
      },
    ],
    ...overrides,
  };
}

describe("Suite 17: Data Layer and Filtering", () => {
  const p1 = makeProduct({
    id: "p-1",
    name: "Biozyme Whey Isolate",
    category: {
      id: "protein-powders",
      name: "Protein Powders",
      slug: "protein-powders",
      description: "",
      icon: "⚡",
      display_order: 1,
    },
  });

  const p2 = makeProduct({
    id: "p-2",
    name: "Double Cocoa Bar",
    slug: "double-cocoa-bar",
    brand: {
      id: "b-2",
      name: "The Whole Truth",
      slug: "the-whole-truth",
      logo_url: null,
      website_url: null,
      description: null,
      is_verified: true,
      created_at: new Date().toISOString(),
    },
    category: {
      id: "protein-bars",
      name: "Protein Bars",
      slug: "protein-bars",
      description: "",
      icon: "🍫",
      display_order: 2,
    },
    variants: [
      {
        ...makeProduct().variants[0],
        id: "v-2",
        product_id: "p-2",
        variant_name: "Single Bar 52g",
        protein_tier: "Tier 2",
        dietary_tags: ["vegan"],
        allergens: ["soy"],
        cost_per_g_protein: 7.5,
        best_cost_per_g_protein: 7.0,
        best_price_inr: 140,
        mrp_inr: 150,
        protein_density_pct: 37.7,
        red_flags: [
          {
            id: "rf-1",
            variant_id: "v-2",
            flag_type: "maltitol_alert",
            flag_severity: "high",
            flag_label: "Maltitol Detected",
            flag_description: "Contains maltitol",
            matched_ingredient: "maltitol",
            ins_number: null,
            created_at: new Date().toISOString(),
          },
        ],
      },
    ],
  });

  const products = [p1, p2];

  it("returns all products when no filters are given", () => {
    const res = applyFilters(products);
    expect(res.length).toBe(2);
  });

  it("filters by categorySlug", () => {
    const res = applyFilters(products, { categorySlug: "protein-bars" });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-2");
  });

  it("searches by product name", () => {
    const res = applyFilters(products, { searchQuery: "Biozyme" });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1");
  });

  it("searches by brand name", () => {
    const res = applyFilters(products, { searchQuery: "Whole Truth" });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-2");
  });

  it("searches by variant name", () => {
    const res = applyFilters(products, { searchQuery: "Rich Chocolate" });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1");
  });

  it("filters by protein tier", () => {
    const res = applyFilters(products, { proteinTiers: ["Tier 1"] });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1");
  });

  it("filters by dietary tag (case-insensitive)", () => {
    const res = applyFilters(products, { dietaryTags: ["VEGAN"] });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-2");
  });

  it("excludes allergens", () => {
    const res = applyFilters(products, { excludeAllergens: ["milk"] });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-2");
  });

  it("filters for zeroFlagsOnly", () => {
    const res = applyFilters(products, { zeroFlagsOnly: true });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1"); // p2 has maltitol red flag
  });

  it("filters by metric range (maxCostPerG)", () => {
    const res = applyFilters(products, { maxCostPerG: 5.0 });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1"); // p1 cost is 4.0, p2 is 7.0
  });

  it("filters by metric range (minDensity)", () => {
    const res = applyFilters(products, { minDensity: 50.0 });
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-1"); // p1 is 84.75%, p2 is 37.7%
  });

  it("filters by nearMe with availableNearIds", () => {
    const availableSet = new Set(["v-2"]);
    const res = applyFilters(products, {}, availableSet);
    expect(res.length).toBe(1);
    expect(res[0].id).toBe("p-2");
  });

  describe("sorting", () => {
    it("sorts by cost_per_g_asc by default", () => {
      const res = applyFilters(products);
      expect(res[0].id).toBe("p-1"); // ₹4.0/g vs ₹7.0/g
      expect(res[1].id).toBe("p-2");
    });

    it("sorts by density_desc", () => {
      const res = applyFilters(products, { sortBy: "density_desc" });
      expect(res[0].id).toBe("p-1"); // 84.75% vs 37.7%
    });

    it("sorts by price_asc", () => {
      const res = applyFilters(products, { sortBy: "price_asc" });
      expect(res[0].id).toBe("p-2"); // ₹150 vs ₹3499
      expect(res[1].id).toBe("p-1");
    });
  });

  it("loads 100 seed products in offline fallback mode", async () => {
    const catalog = await getProducts();
    expect(catalog.length).toBe(100);
  });
});
