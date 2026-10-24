import { describe, expect, it } from "vitest";
import imageLoader from "./imageLoader";

describe("imageLoader", () => {
  it("asks Shopify's CDN for the needed width and keeps the version query", () => {
    expect(imageLoader({ src: "https://cdn.shopify.com/s/files/1/a.jpg?v=123", width: 640 })).toBe(
      "https://cdn.shopify.com/s/files/1/a.jpg?v=123&width=640"
    );
  });

  it("asks Unsplash for width, quality and auto format", () => {
    const out = new URL(imageLoader({ src: "https://images.unsplash.com/photo-1?ixlib=rb", width: 800, quality: 60 }));
    expect(out.searchParams.get("w")).toBe("800");
    expect(out.searchParams.get("q")).toBe("60");
    expect(out.searchParams.get("auto")).toBe("format");
  });

  it("leaves other hosts and local paths unchanged", () => {
    expect(imageLoader({ src: "https://cdn2.nutrabay.com/x.jpg", width: 640 })).toBe("https://cdn2.nutrabay.com/x.jpg");
    expect(imageLoader({ src: "/local.png", width: 640 })).toBe("/local.png");
  });
});
