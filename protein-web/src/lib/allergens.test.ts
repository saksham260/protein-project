import { describe, expect, it } from "vitest";
import { allergenGroups, hasAllergenData, passesAllergenExclusions, variantAllergenGroups } from "./allergens";

const variant = (allergens: string[], ingredient_list: string[] = ["water"]) => ({ allergens, ingredient_list });

describe("allergenGroups", () => {
  it("understands every spelling used in the catalog", () => {
    expect(allergenGroups("Almonds")).toEqual(["tree_nuts"]);
    expect(allergenGroups("tree nuts")).toEqual(["tree_nuts"]);
    expect(allergenGroups("tree_nuts")).toEqual(["tree_nuts"]);
    expect(allergenGroups("egg")).toEqual(["eggs"]);
    expect(allergenGroups("Wheat")).toEqual(["gluten"]);
    expect(allergenGroups("peanut")).toEqual(["peanuts"]);
  });

  it("treats a plain 'nuts' label as both kinds of nut", () => {
    expect(allergenGroups("nuts")).toEqual(["tree_nuts", "peanuts"]);
  });

  it("returns nothing for words it doesn't know", () => {
    expect(allergenGroups("sesame")).toEqual([]);
  });
});

describe("passesAllergenExclusions", () => {
  it("removes products the old exact-text match let through", () => {
    expect(passesAllergenExclusions(variant(["nuts"]), ["tree_nuts"])).toBe(false);
    expect(passesAllergenExclusions(variant(["Almonds"]), ["tree_nuts"])).toBe(false);
    expect(passesAllergenExclusions(variant(["egg"]), ["eggs"])).toBe(false);
    expect(passesAllergenExclusions(variant(["wheat"]), ["gluten"])).toBe(false);
    expect(passesAllergenExclusions(variant(["barley"]), ["gluten"])).toBe(false);
    expect(passesAllergenExclusions(variant(["oats"]), ["gluten"])).toBe(false);
    expect(passesAllergenExclusions(variant(["nuts"]), ["peanuts"])).toBe(false);
  });

  it("catches allergens that appear only in the ingredient list", () => {
    expect(passesAllergenExclusions(variant([], ["Roasted Peanuts", "Salt"]), ["peanuts"])).toBe(false);
    expect(passesAllergenExclusions(variant(["milk"], ["Egg Albumin"]), ["eggs"])).toBe(false);
    expect(passesAllergenExclusions(variant([], ["Whey Protein Isolate"]), ["milk"])).toBe(false);
  });

  it("doesn't treat plant milks and peanut butter as dairy", () => {
    expect(passesAllergenExclusions(variant([], ["Coconut Milk Powder"]), ["milk"])).toBe(true);
    expect(passesAllergenExclusions(variant([], ["Peanut Butter"]), ["milk"])).toBe(true);
  });

  it("keeps products that are clear of the excluded groups", () => {
    expect(passesAllergenExclusions(variant(["soy"], ["Soy Protein"]), ["milk", "eggs"])).toBe(true);
  });

  it("hides products with no allergen data while a filter is on", () => {
    expect(passesAllergenExclusions(variant([], []), ["milk"])).toBe(false);
    expect(passesAllergenExclusions(variant([], []), [])).toBe(true);
    expect(passesAllergenExclusions(variant([], []), undefined)).toBe(true);
  });
});

describe("helpers", () => {
  it("combines declared allergens and ingredients", () => {
    expect([...variantAllergenGroups(variant(["Milk"], ["Soy Lecithin"]))].sort()).toEqual(["milk", "soy"]);
  });

  it("knows when a label gave us nothing", () => {
    expect(hasAllergenData(variant([], []))).toBe(false);
    expect(hasAllergenData(variant(["milk"], []))).toBe(true);
    expect(hasAllergenData(variant([], ["water"]))).toBe(true);
  });
});
