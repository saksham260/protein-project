import { describe, it, expect } from "vitest";
import {
  formatPrice,
  formatPricePerGram,
  formatPercentage,
  formatWeight,
  computePer100g,
  cn,
  formatTimeAgo,
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

    it("returns 0 when netWeightG is zero or negative", () => {
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
});
