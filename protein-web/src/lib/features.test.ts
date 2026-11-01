import { describe, expect, it } from "vitest";
import type { ProductVariant, ProductWithVariants } from "@/types/product";
import { BEST_LISTS, bestValueVariant, buildBestList } from "./bestLists";
import {
  bestColumns,
  compareHref,
  compareKey,
  COMPARE_ROWS,
  findCompareItems,
  MAX_COMPARE,
  parseCompareKeys,
} from "./compare";
import { costPerTestedGram, priceLabel, proteinInPack } from "./metrics";
import { icmrReferenceGrams, rankByDailyCost } from "./proteinCost";

function variant(overrides: Partial<ProductVariant> = {}): ProductVariant {
  return {
    id: "v-1",
    slug: "chocolate-1kg",
    variant_name: "Chocolate 1kg",
    mrp_inr: 3000,
    net_weight_g: 1000,
    serving_size_g: 40,
    protein_g: 30,
    calories_kcal: 150,
    total_sugars_g: 1,
    protein_density_pct: 80,
    cost_per_g_protein: 4,
    best_cost_per_g_protein: null,
    best_price_inr: null,
    primary_protein_source: "Whey Protein Isolate",
    protein_tier: "Tier 1",
    ingredient_list: ["Whey Protein Isolate"],
    allergens: ["milk"],
    dietary_tags: ["vegetarian"],
    red_flags: [],
    ...overrides,
  } as ProductVariant;
}

function product(overrides: Partial<ProductWithVariants> = {}): ProductWithVariants {
  return {
    id: "p-1",
    slug: "acme-whey",
    name: "Acme Whey",
    brand: { name: "Acme" },
    category: { slug: "protein-powders", name: "Protein Powders" },
    variants: [variant()],
    ...overrides,
  } as ProductWithVariants;
}

describe("compare", () => {
  it("makes a key unique across products, without doubling a prefix", () => {
    expect(compareKey({ slug: "acme-whey" }, { slug: "chocolate-1kg" })).toBe("acme-whey-chocolate-1kg");
    expect(compareKey({ slug: "acme-whey" }, { slug: "acme-whey-chocolate-1kg" })).toBe("acme-whey-chocolate-1kg");
  });

  it("reads a link, dropping blanks and repeats, and capping the count", () => {
    expect(parseCompareKeys("a, b,,a")).toEqual(["a", "b"]);
    expect(parseCompareKeys("a,b,c,d,e,f")).toHaveLength(MAX_COMPARE);
    expect(parseCompareKeys(null)).toEqual([]);
  });

  it("builds a link that reads back the same", () => {
    expect(parseCompareKeys(compareHref(["a", "b"]).split("v=")[1])).toEqual(["a", "b"]);
    expect(compareHref([])).toBe("/compare");
  });

  it("finds items in link order and skips unknown keys", () => {
    const other = product({ id: "p-2", slug: "zed-whey" });
    const items = findCompareItems([product(), other], ["zed-whey-chocolate-1kg", "missing", "acme-whey-chocolate-1kg"]);
    expect(items.map((i) => i.product.slug)).toEqual(["zed-whey", "acme-whey"]);
  });

  const row = (label: string) => COMPARE_ROWS.find((r) => r.label === label)!;
  const items = (...variants: ProductVariant[]) =>
    variants.map((v, i) => ({ key: String(i), product: product(), variant: v }));

  it("marks the lower cost as best", () => {
    const best = bestColumns(row("Cost per gram of protein"), items(variant({ cost_per_g_protein: 4 }), variant({ cost_per_g_protein: 3 })));
    expect([...best]).toEqual([1]);
  });

  it("marks no winner on a tie, or on rows packs can't be ranked by", () => {
    expect(bestColumns(row("Cost per gram of protein"), items(variant(), variant())).size).toBe(0);
    expect(bestColumns(row("Price"), items(variant({ mrp_inr: 100 }), variant({ mrp_inr: 200 }))).size).toBe(0);
    expect(bestColumns(row("Label red flags"), items(variant(), variant())).size).toBe(0);
  });

  it("says when there's no ingredient list instead of showing a clean result", () => {
    const flags = row("Label red flags");
    if (flags.kind !== "text") throw new Error("expected a text row");
    expect(flags.value(items(variant({ ingredient_list: [] }))[0])).toBe("No ingredient list");
  });
});

describe("bestLists", () => {
  const whey = BEST_LISTS.find((list) => list.slug === "whey-isolate")!;

  it("uses each product's cheapest in-stock pack", () => {
    const p = product({
      variants: [
        variant({ id: "small", cost_per_g_protein: 6 }),
        variant({ id: "big", cost_per_g_protein: 3 }),
        variant({ id: "gone", cost_per_g_protein: 2, is_available: false }),
      ],
    });
    expect(bestValueVariant(p, () => true)?.id).toBe("big");
  });

  it("ranks by cost and leaves out flagged or unlisted products", () => {
    const pricey = product({ id: "pricey", variants: [variant({ cost_per_g_protein: 6 })] });
    const cheap = product({ id: "cheap", variants: [variant({ cost_per_g_protein: 3 })] });
    const flagged = product({
      id: "flagged",
      variants: [variant({ cost_per_g_protein: 1, red_flags: [{ flag_type: "maltitol_alert" } as never] })],
    });
    const unlisted = product({ id: "unlisted", variants: [variant({ cost_per_g_protein: 1, ingredient_list: [] })] });
    const list = buildBestList([pricey, flagged, unlisted, cheap], whey);
    expect(list.map((p) => p.id)).toEqual(["cheap", "pricey"]);
  });

  it("doesn't count isolate-and-concentrate blends as whey isolate", () => {
    const blend = variant({ protein_tier: "Tier 2", ingredient_list: ["Protein Blend (Whey Protein Isolate, Whey Protein Concentrate)"] });
    expect(whey.matches(blend)).toBe(false);
    expect(whey.matches(variant({ ingredient_list: ["Whey Protein Isolate", "Whey Protein Concentrate"] }))).toBe(false);
    expect(whey.matches(variant())).toBe(true);
  });

  it("keeps maltitol out of the no-maltitol bars list", () => {
    const bars = BEST_LISTS.find((list) => list.slug === "protein-bars-without-maltitol")!;
    expect(bars.matches(variant({ ingredient_list: ["Maltitol Syrup"] }))).toBe(false);
    expect(bars.matches(variant({ ingredient_list: ["Dates"] }))).toBe(true);
  });
});

describe("proteinCost", () => {
  it("uses the ICMR-NIN figure", () => {
    expect(icmrReferenceGrams(70)).toBe(58);
  });

  it("works out cost per day, per month and packs used", () => {
    const [result] = rankByDailyCost([product()], { gramsPerDay: 25 });
    expect(result.perDay).toBe(100);
    expect(result.perMonth).toBe(3000);
    expect(result.packsPerMonth).toBeCloseTo((25 * 30) / 750);
  });

  it("applies the form, diet and red-flag choices", () => {
    const flagged = product({ id: "flagged", variants: [variant({ red_flags: [{ flag_type: "x" } as never] })] });
    expect(rankByDailyCost([flagged], { gramsPerDay: 25, hideRedFlags: true })).toEqual([]);
    expect(rankByDailyCost([product()], { gramsPerDay: 25, diet: "vegan" })).toEqual([]);
    expect(rankByDailyCost([product()], { gramsPerDay: 25, categorySlug: "protein-bars" })).toEqual([]);
  });
});

describe("pack-level metrics", () => {
  it("scales per-serving protein up to the whole pack", () => {
    expect(proteinInPack(variant())).toBe(750);
  });

  it("never calls a store price the MRP", () => {
    expect(priceLabel(variant({ best_price_inr: null }))).toBe("MRP");
    expect(priceLabel(variant({ best_price_inr: 2500 }))).toBe("From");
    expect(priceLabel(variant({ best_price_inr: 3500 }))).toBe("Price");
  });

  it("works out cost on the protein a lab measured", () => {
    expect(costPerTestedGram(variant(), 60)).toBe(5);
    expect(costPerTestedGram(variant(), 0)).toBeNull();
  });
});
