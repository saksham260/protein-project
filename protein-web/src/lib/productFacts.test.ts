import { describe, expect, it } from "vitest";
import { cleanDietaryTags, correctedNetCarbs, polyolLabel } from "./productFacts";

const carbs = (ingredient_list: string[], non_glycemic_polyols_g: number) => ({
  ingredient_list,
  non_glycemic_polyols_g,
  total_carbs_g: 30,
  dietary_fiber_g: 5,
  true_net_carbs_g: 30 - 5 - non_glycemic_polyols_g,
});

describe("correctedNetCarbs", () => {
  it("keeps the subtraction for erythritol", () => {
    expect(correctedNetCarbs(carbs(["Erythritol"], 10))).toBe(15);
  });

  it("doesn't subtract maltitol, which raises blood sugar", () => {
    expect(correctedNetCarbs(carbs(["Maltitol Syrup"], 10))).toBe(25);
    expect(correctedNetCarbs(carbs(["Sweetener (INS 965)"], 10))).toBe(25);
  });

  it("leaves products with no polyols alone", () => {
    expect(correctedNetCarbs(carbs(["Whey"], 0))).toBe(25);
  });
});

describe("polyolLabel", () => {
  it("names the sweetener on the label", () => {
    expect(polyolLabel({ ingredient_list: ["Maltitol"] })).toBe("Polyols (Maltitol)");
    expect(polyolLabel({ ingredient_list: ["Erythritol", "Sorbitol"] })).toBe("Polyols (Sorbitol, Erythritol)");
    expect(polyolLabel({ ingredient_list: ["Sweetener (INS 965)"] })).toBe("Polyols (Maltitol)");
  });

  it("makes no claim when the label names none", () => {
    expect(polyolLabel({ ingredient_list: [] })).toBe("Polyols");
  });
});

describe("cleanDietaryTags", () => {
  const tags = (dietary_tags: string[], ingredient_list: string[], added_sugars_g = 0) =>
    cleanDietaryTags({ dietary_tags, ingredient_list, added_sugars_g });

  it("drops 'no added sugar' when a sugar is listed", () => {
    expect(tags(["No Added Sugar"], ["Jaggery"])).toEqual([]);
    expect(tags(["No Added Sugar"], ["Honey"])).toEqual([]);
    expect(tags(["No Added Sugar"], ["Date Syrup"])).toEqual([]);
    expect(tags(["No Added Sugar"], ["Coconut Sugar"])).toEqual([]);
    expect(tags(["No Added Sugar"], ["Brown Rice Syrup (Liquid Glucose)"])).toEqual([]);
  });

  it("drops it when the label shows added sugar", () => {
    expect(tags(["No Added Sugar"], ["Oats"], 2)).toEqual([]);
  });

  it("keeps it when the ingredient only says sugar-free", () => {
    expect(tags(["No Added Sugar"], ["Sugar-Free Chocolate"])).toEqual(["no-added-sugar"]);
  });

  it("keeps 'no refined sugar' as its own, weaker claim", () => {
    expect(tags(["No Refined Sugar"], ["Jaggery"])).toEqual(["no-refined-sugar"]);
  });

  it("drops 'vegetarian' when the label lists egg or gelatin", () => {
    expect(tags(["Vegetarian"], ["Egg Albumin"])).toEqual([]);
    expect(tags(["Vegetarian"], ["Gelatin"])).toEqual([]);
    expect(tags(["Vegetarian"], ["Whey Protein"])).toEqual(["vegetarian"]);
  });

  it("merges duplicate spellings", () => {
    expect(tags(["Gluten Free", "Gluten-Free"], ["Oats"])).toEqual(["gluten-free"]);
  });
});
