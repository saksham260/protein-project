import { describe, it, expect } from "vitest";
import {
  PINCODE_PATTERN,
  areaCode,
  isReportedAvailable,
  getAvailabilitySummaries,
  reportAvailability,
} from "./availability";

describe("Suite 16: Availability System", () => {
  describe("PINCODE_PATTERN", () => {
    it("accepts valid 6-digit Indian postal codes not starting with 0", () => {
      expect(PINCODE_PATTERN.test("560034")).toBe(true);
      expect(PINCODE_PATTERN.test("110001")).toBe(true);
      expect(PINCODE_PATTERN.test("400001")).toBe(true);
    });

    it("rejects pincodes starting with 0", () => {
      expect(PINCODE_PATTERN.test("060034")).toBe(false);
    });

    it("rejects pincodes with wrong length", () => {
      expect(PINCODE_PATTERN.test("56003")).toBe(false);
      expect(PINCODE_PATTERN.test("5600345")).toBe(false);
    });

    it("rejects alphanumeric strings", () => {
      expect(PINCODE_PATTERN.test("56003A")).toBe(false);
      expect(PINCODE_PATTERN.test("abc123")).toBe(false);
    });
  });

  describe("areaCode", () => {
    it("extracts first 3 digits as postal area code", () => {
      expect(areaCode("560034")).toBe("560");
      expect(areaCode("110001")).toBe("110");
    });
  });

  describe("isReportedAvailable", () => {
    it("returns true when yes_count > no_count", () => {
      expect(isReportedAvailable({ yes_count: 5, no_count: 1 })).toBe(true);
    });

    it("returns false when yes_count <= no_count", () => {
      expect(isReportedAvailable({ yes_count: 1, no_count: 5 })).toBe(false);
      expect(isReportedAvailable({ yes_count: 3, no_count: 3 })).toBe(false);
    });

    it("returns false when both counts are 0", () => {
      expect(isReportedAvailable({ yes_count: 0, no_count: 0 })).toBe(false);
    });
  });

  describe("offline/unconfigured behavior", () => {
    it("getAvailabilitySummaries returns empty array when unconfigured or invalid pincode", async () => {
      const summaries = await getAvailabilitySummaries(["v-1"], "060034");
      expect(summaries).toEqual([]);
    });

    it("reportAvailability returns false for invalid pincode", async () => {
      const res = await reportAvailability("v-1", "blinkit", "invalid", true);
      expect(res).toBe(false);
    });
  });
});
