import { describe, expect, it } from "vitest";
import { publicOrigin, safeNextPath } from "./auth";

describe("safeNextPath", () => {
  it("keeps same-site paths", () => {
    expect(safeNextPath("/explore?cat=bars")).toBe("/explore?cat=bars");
  });

  it("falls back for missing or off-site targets", () => {
    expect(safeNextPath(null)).toBe("/");
    expect(safeNextPath("")).toBe("/");
    expect(safeNextPath("https://evil.com")).toBe("/");
    expect(safeNextPath("//evil.com")).toBe("/");
    expect(safeNextPath("/\\evil.com")).toBe("/");
  });
});

describe("publicOrigin", () => {
  it("uses forwarded headers when behind a proxy", () => {
    const headers = new Headers({ "x-forwarded-host": "app.onrender.com", "x-forwarded-proto": "https" });
    expect(publicOrigin("http://localhost:10000/auth/callback", headers)).toBe("https://app.onrender.com");
  });

  it("uses the request origin otherwise", () => {
    expect(publicOrigin("http://localhost:3000/auth/callback", new Headers())).toBe("http://localhost:3000");
  });
});
