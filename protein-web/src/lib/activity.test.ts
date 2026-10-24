import { describe, expect, it } from "vitest";
import { recentProducts, type ActivityRow } from "./activity";

const row = (product_id: string, event_type: ActivityRow["event_type"], created_at: string): ActivityRow => ({
  product_id,
  event_type,
  platform: event_type === "purchase_click" ? "amazon" : null,
  created_at,
});

describe("recentProducts", () => {
  it("lists each product once, newest activity first", () => {
    const rows = [
      row("a", "view", "2026-10-24T10:00:00Z"),
      row("b", "view", "2026-10-24T12:00:00Z"),
      row("a", "view", "2026-10-24T13:00:00Z"),
    ];
    expect(recentProducts(rows).map((r) => r.productId)).toEqual(["a", "b"]);
  });

  it("flags products the person clicked through to buy, even if viewed again later", () => {
    const rows = [
      row("a", "purchase_click", "2026-10-24T10:00:00Z"),
      row("a", "view", "2026-10-24T11:00:00Z"),
      row("b", "view", "2026-10-24T09:00:00Z"),
    ];
    expect(recentProducts(rows)).toEqual([
      { productId: "a", wentToBuy: true },
      { productId: "b", wentToBuy: false },
    ]);
  });

  it("respects the limit and handles no activity", () => {
    const rows = ["a", "b", "c"].map((id, i) => row(id, "view", `2026-10-24T1${i}:00:00Z`));
    expect(recentProducts(rows, 2)).toHaveLength(2);
    expect(recentProducts([])).toEqual([]);
  });
});
