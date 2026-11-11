import { Platform, RedirectLink } from "@/types/product";

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

/** Amazon's agreement allows its price data to be kept for 24 hours before it must be refreshed. */
const AMAZON_PRICE_MAX_AGE_MS = 24 * 60 * 60 * 1000;
/** Older than this, a brand-store price still shows, but can't be called the cheapest. */
const STORE_PRICE_MAX_AGE_MS = 14 * 24 * 60 * 60 * 1000;

const AMAZON_HOST = /(^|\.)amazon\.(in|com)$/;

function amazonTag(): string {
  return process.env.NEXT_PUBLIC_AMAZON_AFFILIATE_TAG || "proteineng-21";
}

/** Adds our Associates tag to Amazon links. Every other store's link comes back unchanged. */
export function withAffiliateTag(url: string): string {
  try {
    const parsed = new URL(url);
    if (!AMAZON_HOST.test(parsed.hostname)) return url;
    parsed.searchParams.set("tag", amazonTag());
    return parsed.toString();
  } catch {
    return url;
  }
}

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
        return withAffiliateTag(ctx.directUrl);
      }
      return `https://www.amazon.in/s?k=${query}&tag=${amazonTag()}`;
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

/**
 * Whether a stored price is recent enough to rely on (e.g. to call it the cheapest).
 * A price with no check time is of unknown age: it may be shown, but never relied on.
 * Only the price pollers set price_last_checked; uploads leave it empty.
 */
export function isPriceFresh(
  link: Pick<RedirectLink, "platform" | "price_last_checked">,
  now: number = Date.now()
): boolean {
  if (!link.price_last_checked) return false;
  const checkedAt = new Date(link.price_last_checked).getTime();
  if (Number.isNaN(checkedAt) || checkedAt > now + 60_000) return false;
  const age = now - checkedAt;
  return age <= (link.platform === "amazon" ? AMAZON_PRICE_MAX_AGE_MS : STORE_PRICE_MAX_AGE_MS);
}
