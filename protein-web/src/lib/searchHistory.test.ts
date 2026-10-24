import { describe, expect, it } from "vitest";
import { toRecentSearch, withSearchFirst } from "./searchHistory";

describe("toRecentSearch", () => {
  it("tidies spaces and builds a lower-case key", () => {
    expect(toRecentSearch("  Whey   Protein ")).toEqual({ query: "Whey Protein", key: "whey protein" });
  });

  it("ignores empty or one-letter searches", () => {
    expect(toRecentSearch("   ")).toBeNull();
    expect(toRecentSearch("a")).toBeNull();
  });

  it("caps very long searches", () => {
    expect(toRecentSearch("x".repeat(200))?.query).toHaveLength(80);
  });
});

describe("withSearchFirst", () => {
  const a = { query: "whey", key: "whey" };
  const b = { query: "bars", key: "bars" };
  const c = { query: "Amul", key: "amul" };

  it("moves a repeated search to the top without duplicating it", () => {
    expect(withSearchFirst([a, b, c], { query: "Bars", key: "bars" }).map((s) => s.key)).toEqual(["bars", "whey", "amul"]);
  });

  it("keeps the list within the limit", () => {
    expect(withSearchFirst([a, b], c, 2).map((s) => s.key)).toEqual(["amul", "whey"]);
  });
});
