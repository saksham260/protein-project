"use client";

import React, { useEffect, useState } from "react";
import { AvailabilitySummary, Platform, QuickCommercePlatform, RedirectLink } from "@/types/product";
import { buildRedirectUrl, getPriceDisplay, isPriceFresh, withAffiliateTag } from "@/lib/redirect";
import { formatDateTime, formatPrice, formatTimeAgo } from "@/lib/utils";
import { AMAZON_DISCLOSURE, AMAZON_PRICE_NOTE, PLATFORM_INFO } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { usePincode } from "@/hooks/usePincode";
import { getAvailabilitySummaries, isReportedAvailable, MIN_REPORTS_TO_TRUST, reportAvailability } from "@/lib/availability";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useAuth } from "@/context/AuthContext";
import { logActivity, logOutboundClick } from "@/lib/activity";
import { PincodeInput } from "@/components/location/PincodeInput";

export interface RedirectButtonsProps {
  redirectLinks: RedirectLink[];
  brandName: string;
  productName: string;
  variantId?: string;
  /** When set, clicks through to a purchase page are saved to the signed-in user's activity. */
  productId?: string;
}

const QUICK_COMMERCE: QuickCommercePlatform[] = ["blinkit", "zepto", "instamart"];

function isQuickCommerce(platform: Platform): platform is QuickCommercePlatform {
  return (QUICK_COMMERCE as Platform[]).includes(platform);
}

function priceSubtitle(link: RedirectLink | undefined, platform: Platform): string {
  const price = getPriceDisplay(platform, link?.platform_price_inr);
  if (link?.in_stock === false) return "Out of stock";
  if (price.type !== "stored" || !link) return "See current price";
  // No check time means the price's age is unknown: claim nothing, and never show an
  // Amazon price we cannot prove is under 24 hours old.
  if (!link.price_last_checked) return platform === "amazon" ? "See current price" : formatPrice(price.price);
  if (platform === "amazon") {
    return isPriceFresh(link)
      ? `${formatPrice(price.price)} · as of ${formatDateTime(link.price_last_checked)}`
      : "See current price";
  }
  return `${formatPrice(price.price)} · checked ${formatTimeAgo(link.price_last_checked)}`;
}

function availabilitySubtitle(summary: AvailabilitySummary | undefined, pincode: string): string {
  if (!pincode) return "Availability depends on your area";
  if (!summary) return `No reports near ${pincode} yet`;
  const counts = `${summary.yes_count} yes / ${summary.no_count} no`;
  if (isReportedAvailable(summary)) return `Reported in stock near you (${counts})`;
  return summary.yes_count + summary.no_count < MIN_REPORTS_TO_TRUST
    ? `Too few reports near you so far (${counts})`
    : `Reported unavailable near you (${counts})`;
}

export const RedirectButtons: React.FC<RedirectButtonsProps> = ({
  redirectLinks = [],
  brandName,
  productName,
  variantId,
  productId,
}) => {
  const { user } = useAuth();
  // Priority ordering for purchase channels
  const PLATFORM_ORDER: Platform[] = ["d2c", "amazon", "blinkit", "zepto", "instamart"];

  // When redirectLinks are explicitly defined for a variant, only display channels that are actually available.
  // If no links are provided at all, fall back to searching across the standard channels.
  const platformsToDisplay: Platform[] =
    redirectLinks.length > 0
      ? PLATFORM_ORDER.filter((p) => redirectLinks.some((l) => l.platform === p))
      : ["amazon", "blinkit", "zepto", "instamart"];
  const { pincode } = usePincode();
  const [summaries, setSummaries] = useState<AvailabilitySummary[]>([]);
  const [askFor, setAskFor] = useState<QuickCommercePlatform | null>(null);
  const [thanked, setThanked] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const canReport = Boolean(variantId) && isSupabaseConfigured();

  useEffect(() => {
    if (!variantId || !pincode) return;
    let isMounted = true;
    getAvailabilitySummaries([variantId], pincode).then((data) => {
      if (isMounted) setSummaries(data);
    });
    return () => {
      isMounted = false;
    };
  }, [variantId, pincode, refreshKey]);

  // Find the lowest recent price across stores that publish one (quick-commerce prices vary by area)
  const pricesWithPlatform = redirectLinks
    .filter(
      (l) =>
        !isQuickCommerce(l.platform) &&
        l.platform_price_inr != null &&
        l.platform_price_inr > 0 &&
        l.in_stock !== false &&
        isPriceFresh(l)
    )
    .map((l) => ({ platform: l.platform, price: l.platform_price_inr! }));
  const showsAmazonPrice = pricesWithPlatform.some((p) => p.platform === "amazon");

  const lowestPrice =
    pricesWithPlatform.length > 0
      ? Math.min(...pricesWithPlatform.map((p) => p.price))
      : null;

  const linkItems = platformsToDisplay.map((platform) => {
    const existing = redirectLinks.find((l) => l.platform === platform);
    const targetUrl = existing
      ? withAffiliateTag(existing.url)
      : buildRedirectUrl(platform, { brandName, productName });

    const summary = pincode ? summaries.find((s) => s.platform === platform) : undefined;
    const subtitle = isQuickCommerce(platform)
      ? availabilitySubtitle(summary, pincode)
      : priceSubtitle(existing, platform);
    const config = PLATFORM_INFO[platform];
    const isCheapest =
      pricesWithPlatform.length > 1 &&
      lowestPrice != null &&
      pricesWithPlatform.some((p) => p.platform === platform && p.price === lowestPrice);

    return {
      platform,
      url: targetUrl,
      subtitle,
      config,
      isCheapest,
    };
  });

  const answer = async (isAvailable: boolean) => {
    if (!askFor || !variantId || !pincode) return;
    const ok = await reportAvailability(variantId, askFor, pincode, isAvailable);
    setAskFor(null);
    setThanked(ok);
    if (ok) setRefreshKey((k) => k + 1);
  };

  return (
    <div className="flex flex-col gap-4 p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
      <div className="flex items-center justify-between border-b border-[#27272A] pb-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
            Purchase Channels
          </span>
        </div>
        <span className="text-[11px] font-mono text-zinc-500">
          Opens the store&apos;s site
        </span>
      </div>

      <PincodeInput />

      <div className={cn("grid grid-cols-1 gap-3.5", linkItems.length > 1 && "sm:grid-cols-2")}>
        {linkItems.map((item) => (
          <a
            key={item.platform}
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => {
              void logOutboundClick({ productId, variantId, platform: item.platform });
              if (user && productId) {
                void logActivity(user.id, { productId, variantId, eventType: "purchase_click", platform: item.platform });
              }
              if (isQuickCommerce(item.platform) && canReport) {
                setAskFor(item.platform);
                setThanked(false);
              }
            }}
            className={cn(
              "relative flex items-center justify-between p-4 rounded-2xl border select-none cursor-pointer group active:scale-[0.98] transition-all duration-300 ease-out",
              item.isCheapest
                ? "bg-[#10B981] text-black border-[#10B981] shadow-[0_0_24px_rgba(16,185,129,0.25)] md:hover:bg-[#26221E] md:hover:text-[#F5F2EB] md:hover:border-[#D97706]/50 md:hover:shadow-[0_0_16px_rgba(217,119,6,0.18),0_2px_8px_rgba(0,0,0,0.4)]"
                : "bg-[#27272A] text-white border-[#3F3F46] md:hover:bg-[#26221E] md:hover:text-[#F5F2EB] md:hover:border-[#D97706]/50 md:hover:shadow-[0_0_16px_rgba(217,119,6,0.18),0_2px_8px_rgba(0,0,0,0.4)]"
            )}
          >
            {/* Cheapest Option Tag */}
            {item.isCheapest && (
              <span className="absolute -top-2.5 right-4 px-2.5 py-0.5 rounded-full bg-[#0A0A0B] text-[#34D399] text-[10px] font-mono font-black tracking-wider uppercase border border-[#10B981]">
                Cheapest Option
              </span>
            )}

            <div className="flex items-center gap-3 min-w-0">
              <span className="text-2xl">{item.config.icon}</span>
              <div className="flex flex-col min-w-0">
                <span
                  className={cn(
                    "text-sm font-bold tracking-tight font-sans transition-colors duration-300",
                    item.isCheapest ? "text-black md:group-hover:text-[#F5F2EB]" : "text-white md:group-hover:text-[#F5F2EB]"
                  )}
                >
                  {item.platform === "d2c"
                    ? `${brandName} Official Store`
                    : /\/s\?k=|\/s\/\?q=|\/search\?|[?&]q=|\/search\//i.test(item.url)
                    ? `Search on ${item.config.name}`
                    : item.config.name}
                </span>
                <span
                  suppressHydrationWarning
                  className={cn(
                    "text-xs font-mono font-medium transition-colors duration-300",
                    item.isCheapest ? "text-black/80 font-bold md:group-hover:text-[#968E85]" : "text-zinc-400 md:group-hover:text-[#968E85]"
                  )}
                >
                  {item.subtitle}
                </span>
              </div>
            </div>

            <div
              className={cn(
                "flex items-center gap-1 text-xs font-mono font-bold transition-all duration-300 md:group-hover:translate-x-1",
                item.isCheapest ? "text-black md:group-hover:text-[#D97706]" : "text-zinc-400 md:group-hover:text-[#D97706]"
              )}
            >
              <span>{/\/s\?k=|\/s\/\?q=|\/search\?|[?&]q=|\/search\//i.test(item.url) ? "Search" : "Buy"}</span>
              <span>↗</span>
            </div>
          </a>
        ))}
      </div>

      {/* Crowd-sourced availability prompt, shown after a quick-commerce click */}
      {askFor && (
        <div className="flex flex-col gap-3 p-4 rounded-2xl bg-[#27272A]/60 border border-[#3F3F46]">
          {pincode ? (
            <>
              <span className="text-xs font-mono text-[#E4E4E7]">
                Was it available on {PLATFORM_INFO[askFor].name} near {pincode}?
              </span>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => answer(true)}
                  className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-[#10B981] text-black cursor-pointer"
                >
                  Yes
                </button>
                <button
                  type="button"
                  onClick={() => answer(false)}
                  className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-[#3F3F46] text-white cursor-pointer"
                >
                  No
                </button>
                <button
                  type="button"
                  onClick={() => setAskFor(null)}
                  className="px-3 py-2 text-xs font-mono text-zinc-500 hover:text-white cursor-pointer"
                >
                  Skip
                </button>
              </div>
            </>
          ) : (
            <span className="text-xs font-mono text-[#E4E4E7]">
              Add your pincode above to tell other shoppers if {PLATFORM_INFO[askFor].name} had it.
            </span>
          )}
        </div>
      )}
      {thanked && (
        <span className="text-xs font-mono text-[#34D399]">Thanks — your report helps shoppers near you.</span>
      )}

      <p className="text-[11px] font-sans text-zinc-500 leading-relaxed">
        {showsAmazonPrice && `${AMAZON_PRICE_NOTE} `}
        Prices can change, so check the store before buying. We may earn a commission on some links.{" "}
        {AMAZON_DISCLOSURE}
      </p>
    </div>
  );
};
