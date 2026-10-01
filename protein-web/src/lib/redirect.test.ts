import { describe, it, expect } from "vitest";
import { buildRedirectUrl, getPriceDisplay } from "./redirect";

describe("Suite 15: Redirect URL and Price Display", () => {
  describe("buildRedirectUrl", () => {
    it("appends affiliate tag to direct Amazon URL", () => {
      const url = buildRedirectUrl("amazon", {
        brandName: "MuscleBlaze",
        productName: "Biozyme Whey",
        directUrl: "https://www.amazon.in/dp/B07XJ8C8F5",
      });
      expect(url).toContain("https://www.amazon.in/dp/B07XJ8C8F5");
      expect(url).toContain("tag=proteineng-21");
    });

    it("builds Amazon search URL with affiliate tag when directUrl is absent", () => {
      const url = buildRedirectUrl("amazon", {
        brandName: "Nakpro",
        productName: "Gold Whey",
      });
      expect(url).toContain("https://www.amazon.in/s?k=Nakpro%20Gold%20Whey");
      expect(url).toContain("tag=proteineng-21");
    });

    it("builds Blinkit search URL", () => {
      const url = buildRedirectUrl("blinkit", {
        brandName: "The Whole Truth",
        productName: "Cocoa Bar",
      });
      expect(url).toBe("https://blinkit.com/s/?q=The%20Whole%20Truth%20Cocoa%20Bar");
    });

    it("builds Zepto search URL", () => {
      const url = buildRedirectUrl("zepto", {
        brandName: "Yoga Bar",
        productName: "Whey Bar",
      });
      expect(url).toBe("https://www.zeptonow.com/search?query=Yoga%20Bar%20Whey%20Bar");
    });

    it("builds Instamart search URL", () => {
      const url = buildRedirectUrl("instamart", {
        brandName: "Amul",
        productName: "Protein Lassi",
      });
      expect(url).toBe("https://www.swiggy.com/instamart/search?query=Amul%20Protein%20Lassi");
    });

    it("returns direct D2C URL when provided", () => {
      const url = buildRedirectUrl("d2c", {
        brandName: "Brand",
        productName: "Product",
        directUrl: "https://brand.com/products/protein-bar",
      });
      expect(url).toBe("https://brand.com/products/protein-bar");
    });

    it("returns '#' for D2C when directUrl is missing", () => {
      const url = buildRedirectUrl("d2c", {
        brandName: "Brand",
        productName: "Product",
      });
      expect(url).toBe("#");
    });
  });

  describe("getPriceDisplay", () => {
    it("returns stored price for Amazon when available", () => {
      expect(getPriceDisplay("amazon", 2499)).toEqual({ type: "stored", price: 2499 });
    });

    it("returns check_local for Amazon when price is null or zero", () => {
      expect(getPriceDisplay("amazon", null)).toEqual({ type: "check_local" });
      expect(getPriceDisplay("amazon", 0)).toEqual({ type: "check_local" });
    });

    it("always returns check_local for quick commerce platforms even if price is provided", () => {
      expect(getPriceDisplay("blinkit", 99)).toEqual({ type: "check_local" });
      expect(getPriceDisplay("zepto", 150)).toEqual({ type: "check_local" });
      expect(getPriceDisplay("instamart", 200)).toEqual({ type: "check_local" });
    });

    it("returns stored price for D2C when available", () => {
      expect(getPriceDisplay("d2c", 135)).toEqual({ type: "stored", price: 135 });
    });
  });
});
