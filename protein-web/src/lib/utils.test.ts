import { describe, it, expect } from "vitest";
import {
  formatPrice,
  formatPricePerGram,
  formatPercentage,
  formatWeight,
  computePer100g,
  cn,
  formatTimeAgo,
  splitProductName,
  canonicalDietaryTag,
  formatDateTime,
} from "./utils";

describe("Suite 14: Formatters and Utils", () => {
  describe("formatPrice", () => {
    it("formats valid prices with INR currency symbol", () => {
      const res = formatPrice(150);
      expect(res).toContain("150");
      expect(res).toContain("₹");
    });

    it("returns dash for null, undefined, and NaN", () => {
      expect(formatPrice(null)).toBe("—");
      expect(formatPrice(undefined)).toBe("—");
      expect(formatPrice(NaN)).toBe("—");
    });
  });

  describe("formatPricePerGram", () => {
    it("formats valid price per gram", () => {
      expect(formatPricePerGram(7.5)).toBe("₹7.50/g");
    });

    it("returns dash for null, undefined, and NaN", () => {
      expect(formatPricePerGram(null)).toBe("—");
      expect(formatPricePerGram(undefined)).toBe("—");
      expect(formatPricePerGram(NaN)).toBe("—");
    });
  });

  describe("formatPercentage", () => {
    it("formats percentage with one decimal", () => {
      expect(formatPercentage(37.74)).toBe("37.7%");
    });

    it("returns dash for invalid values", () => {
      expect(formatPercentage(null)).toBe("—");
      expect(formatPercentage(undefined)).toBe("—");
      expect(formatPercentage(NaN)).toBe("—");
    });
  });

  describe("formatWeight", () => {
    it("formats weights >= 1000g as kg", () => {
      expect(formatWeight(1000)).toBe("1kg");
      expect(formatWeight(1500)).toBe("1.5kg");
      expect(formatWeight(2000)).toBe("2kg");
    });

    it("formats weights < 1000g as g", () => {
      expect(formatWeight(52)).toBe("52g");
      expect(formatWeight(500)).toBe("500g");
    });

    it("returns dash for 0, null, or undefined", () => {
      expect(formatWeight(0)).toBe("—");
      expect(formatWeight(null)).toBe("—");
      expect(formatWeight(undefined)).toBe("—");
    });
  });

  describe("computePer100g", () => {
    it("scales value to per-100g basis correctly", () => {
      expect(computePer100g(20, 52)).toBe(38.46);
    });

    it("scales a powder's per-serving protein by the serving, not the tub", () => {
      expect(computePer100g(25, 36)).toBe(69.44);
    });

    it("returns 0 when the serving size is zero or negative", () => {
      expect(computePer100g(20, 0)).toBe(0);
      expect(computePer100g(20, -50)).toBe(0);
    });
  });

  describe("cn (classnames helper)", () => {
    it("joins class names and filters falsy values", () => {
      expect(cn("base-class", false && "hidden", "active", null, undefined, "flex")).toBe(
        "base-class active flex"
      );
    });
  });

  describe("formatTimeAgo", () => {
    const fixedNow = 1700000000000;

    it("returns 'just now' for diff under 1 minute", () => {
      const recent = new Date(fixedNow - 20000).toISOString();
      expect(formatTimeAgo(recent, fixedNow)).toBe("just now");
    });

    it("returns minutes ago for diff under 60 minutes", () => {
      const fiveMinAgo = new Date(fixedNow - 5 * 60000).toISOString();
      expect(formatTimeAgo(fiveMinAgo, fixedNow)).toBe("5 min ago");
    });

    it("returns hours ago for diff under 48 hours", () => {
      const threeHoursAgo = new Date(fixedNow - 3 * 3600000).toISOString();
      expect(formatTimeAgo(threeHoursAgo, fixedNow)).toBe("3 h ago");
    });

    it("returns days ago for diff >= 48 hours", () => {
      const threeDaysAgo = new Date(fixedNow - 3 * 86400000).toISOString();
      expect(formatTimeAgo(threeDaysAgo, fixedNow)).toBe("3 days ago");
    });

    it("returns dash for null or undefined", () => {
      expect(formatTimeAgo(null)).toBe("—");
      expect(formatTimeAgo(undefined)).toBe("—");
    });
  });

  describe("formatDateTime", () => {
    it("shows a full date and time in India time", () => {
      expect(formatDateTime("2026-11-01T10:15:00Z")).toMatch(/1 Nov 2026.*3:45/i);
    });

    it("returns dash for null", () => {
      expect(formatDateTime(null)).toBe("—");
    });
  });

  describe("canonicalDietaryTag", () => {
    it("treats spelling variants as one tag", () => {
      expect(canonicalDietaryTag("No Added Sugar")).toBe("no-added-sugar");
      expect(canonicalDietaryTag("Gluten Free")).toBe("gluten-free");
    });

    it("doesn't upgrade a tag into a stronger claim", () => {
      expect(canonicalDietaryTag("Dairy Free")).toBe("dairy-free");
      expect(canonicalDietaryTag("Peanut Free")).toBe("peanut-free");
      expect(canonicalDietaryTag("No Refined Sugar")).toBe("no-refined-sugar");
    });
  });

  describe("splitProductName", () => {
    it("splits (Pack of 8) cleanly from Chase products", () => {
      const res = splitProductName("Millionaire Brownie 20g Protein Bar (Pack of 8)");
      expect(res.baseName).toBe("Millionaire Brownie 20g Protein Bar");
      expect(res.packInfo).toBe("Pack of 8");
    });

    it("splits (Pack of 6) from SuperYou mega wafers", () => {
      const res = splitProductName("20g MEGA Protein Wafer Kesar Pista Badam (Pack of 6)");
      expect(res.baseName).toBe("20g MEGA Protein Wafer Kesar Pista Badam");
      expect(res.packInfo).toBe("Pack of 6");
    });

    it("splits (Box of 30) from sachet products", () => {
      const res = splitProductName("Whey Protein Sachets (Box of 30)");
      expect(res.baseName).toBe("Whey Protein Sachets");
      expect(res.packInfo).toBe("Box of 30");
    });

    it("returns null packInfo for single unit products", () => {
      const res = splitProductName("Unflavoured Fermented Yeast Protein");
      expect(res.baseName).toBe("Unflavoured Fermented Yeast Protein");
      expect(res.packInfo).toBeNull();
    });

    it("extracts pack info from variantName if not present in product name", () => {
      const res = splitProductName("Protein Bar", "Pack of 12 x 50g");
      expect(res.baseName).toBe("Protein Bar");
      expect(res.packInfo).toBe("Pack of 12 x 50g");
    });
  });
});

