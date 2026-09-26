import { Platform } from "@/types/product";

export type PriceDisplay =
  | { type: "stored"; price: number }
  | { type: "check_local" };

export interface RedirectLinkOption {
  platform: Platform;
  url: string;
  priceDisplay: PriceDisplay;
  label: string;
}

const QUICK_COMMERCE_PLATFORMS: Platform[] = ["blinkit", "zepto", "instamart"];

export function buildRedirectUrl(
  platform: Platform,
  ctx: {
    brandName: string;
    productName: string;
    directUrl?: string | null;
  }
): string {
  const query = encodeURIComponent(`${ctx.brandName} ${ctx.productName}`.trim());

  switch (platform) {
    case "amazon":
      if (ctx.directUrl && ctx.directUrl.startsWith("http")) {
        const url = new URL(ctx.directUrl);
        url.searchParams.set("tag", process.env.NEXT_PUBLIC_AMAZON_AFFILIATE_TAG || "proteineng-21");
        return url.toString();
      }
      return `https://www.amazon.in/s?k=${query}&tag=${process.env.NEXT_PUBLIC_AMAZON_AFFILIATE_TAG || "proteineng-21"}`;
    case "blinkit":
      return `https://blinkit.com/s/?q=${query}`;
    case "zepto":
      return `https://www.zeptonow.com/search?query=${query}`;
    case "instamart":
      return `https://www.swiggy.com/instamart/search?query=${query}`;
    case "d2c":
      return ctx.directUrl && ctx.directUrl.startsWith("http") ? ctx.directUrl : "#";
  }
}

export function getPriceDisplay(platform: Platform, storedPrice?: number | null): PriceDisplay {
  if (QUICK_COMMERCE_PLATFORMS.includes(platform)) {
    return { type: "check_local" };
  }
  if (storedPrice !== null && storedPrice !== undefined && storedPrice > 0) {
    return { type: "stored", price: storedPrice };
  }
  return { type: "check_local" };
}
