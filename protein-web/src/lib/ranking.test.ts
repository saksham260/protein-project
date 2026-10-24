import { describe, expect, it } from "vitest";
import { brandTier, bundleLevel, featuredScore } from "./ranking";

describe("bundleLevel", () => {
  it("treats a normal tub or bar as an individual item", () => {
    expect(bundleLevel("Whey Protein", "Chocolate 1kg")).toBe(0);
    expect(bundleLevel("Choco Bar", "Single Bar 55g")).toBe(0);
    expect(bundleLevel("Cold Coffee", "Box of 5 sachets x 25g")).toBe(0); // 5 sachets is how it is sold, not a bundle name
  });

  it("flags multi-packs of the same item", () => {
    expect(bundleLevel("Protein Minis (Pack of 24)", "Pack of 24 x 20g")).toBe(1);
    expect(bundleLevel("Buttermilk", "30 Packs")).toBe(1);
    expect(bundleLevel("Shake", "Multipack")).toBe(1);
  });

  it("flags combos, bundles and free gifts as the lowest priority", () => {
    expect(bundleLevel("Ripped Whey", "Chocolate 1.8kg (Combo)")).toBe(2);
    expect(bundleLevel("Plant Protein", "Cookies 1kg + Free Shaker")).toBe(2);
    expect(bundleLevel("Variety Pack Bars", "Pack of 12")).toBe(2);
    expect(bundleLevel("Anything", "1kg", true)).toBe(2);
  });
});

describe("brandTier", () => {
  it("ranks household brands above well-known above the rest, ignoring case", () => {
    expect(brandTier("MuscleBlaze")).toBe(1);
    expect(brandTier("  amul ")).toBe(1);
    expect(brandTier("Chase")).toBe(2);
    expect(brandTier("Some New Brand")).toBe(3);
    expect(brandTier(undefined)).toBe(3);
  });
});

describe("featuredScore", () => {
  const base = { variantName: "1kg", costPerGram: 2 };

  it("puts individual items before multi-packs before combos, whatever the brand", () => {
    const single = featuredScore({ ...base, productName: "Whey", brandName: "Unknown" });
    const multi = featuredScore({ ...base, productName: "Whey (Pack of 6)", brandName: "MuscleBlaze" });
    const combo = featuredScore({ ...base, productName: "Whey Combo", brandName: "MuscleBlaze" });
    expect(single).toBeLessThan(multi);
    expect(multi).toBeLessThan(combo);
  });

  it("puts bigger brands first within the same bundle level, then cheaper protein", () => {
    const big = featuredScore({ ...base, productName: "Whey", brandName: "MuscleBlaze", costPerGram: 5 });
    const mid = featuredScore({ ...base, productName: "Whey", brandName: "Chase", costPerGram: 1 });
    const cheapBig = featuredScore({ ...base, productName: "Whey", brandName: "MuscleBlaze", costPerGram: 3 });
    expect(big).toBeLessThan(mid);
    expect(cheapBig).toBeLessThan(big);
  });

  it("copes with a missing cost", () => {
    expect(Number.isFinite(featuredScore({ productName: "Whey", variantName: "1kg", costPerGram: null }))).toBe(true);
  });
});
