import { describe, expect, it } from "vitest";
import type { ProductWithVariants } from "@/types/product";
import { editDistance, searchRank } from "./search";

function product(name: string, brand: string, ingredients: string[] = [], source: string | null = null): ProductWithVariants {
  return {
    name,
    brand: { name: brand },
    category: { name: "Protein Powders" },
    variants: [{ variant_name: "Chocolate 1kg", ingredient_list: ingredients, primary_protein_source: source }],
  } as unknown as ProductWithVariants;
}

const biozyme = product("Biozyme Whey Isolate", "MuscleBlaze", ["Whey Protein Isolate", "Maltitol"], "Whey Isolate");
const yogaBar = product("Protein Bar", "Yoga Bar", ["Soy Protein"]);
const gold = product("Gold Standard Whey", "Optimum Nutrition");

describe("searchRank", () => {
  it("matches words in any order", () => {
    expect(searchRank(biozyme, "isolate whey")).toBe(2);
    expect(searchRank(biozyme, "chocolate whey")).toBe(2);
  });

  it("ignores spacing differences in brand names", () => {
    expect(searchRank(biozyme, "muscle blaze")).toBe(2);
    expect(searchRank(yogaBar, "yogabar")).toBe(2);
  });

  it("forgives small typos", () => {
    expect(searchRank(yogaBar, "protien bar")).toBe(2);
    expect(searchRank(biozyme, "isolat")).toBe(2);
  });

  it("finds ingredients, ranked below name matches", () => {
    expect(searchRank(biozyme, "maltitol")).toBe(1);
    expect(searchRank(yogaBar, "soya")).toBe(1);
  });

  it("needs every word to match", () => {
    expect(searchRank(biozyme, "whey paneer")).toBe(0);
  });

  it("doesn't let very short words match inside longer ones", () => {
    expect(searchRank(biozyme, "on")).toBe(0);
    expect(searchRank(gold, "on whey")).toBe(2);
  });
});

describe("editDistance", () => {
  it("counts a swapped pair of letters as one slip", () => {
    expect(editDistance("protien", "protein")).toBe(1);
    expect(editDistance("whey", "whey")).toBe(0);
    expect(editDistance("whey", "soya")).toBe(4);
  });
});
