"use client";

import React from "react";
import { RedirectLink, Platform } from "@/types/product";
import { buildRedirectUrl, getPriceDisplay } from "@/lib/redirect";
import { formatPrice } from "@/lib/utils";
import { PLATFORM_INFO } from "@/lib/constants";
import { cn } from "@/lib/utils";

export interface RedirectButtonsProps {
  redirectLinks: RedirectLink[];
  brandName: string;
  productName: string;
}

export const RedirectButtons: React.FC<RedirectButtonsProps> = ({
  redirectLinks = [],
  brandName,
  productName,
}) => {
  const platformsToDisplay: Platform[] = ["amazon", "blinkit", "zepto", "instamart"];

  // Find the lowest known price across all platforms
  const pricesWithPlatform = redirectLinks
    .filter((l) => l.platform_price_inr != null && l.platform_price_inr > 0)
    .map((l) => ({ platform: l.platform, price: l.platform_price_inr! }));

  const lowestPrice =
    pricesWithPlatform.length > 0
      ? Math.min(...pricesWithPlatform.map((p) => p.price))
      : null;

  const linkItems = platformsToDisplay.map((platform) => {
    const existing = redirectLinks.find((l) => l.platform === platform);
    const targetUrl = existing
      ? existing.url
      : buildRedirectUrl(platform, { brandName, productName });

    const priceInfo = getPriceDisplay(platform, existing?.platform_price_inr);
    const config = PLATFORM_INFO[platform];
    const isCheapest =
      lowestPrice != null && existing?.platform_price_inr === lowestPrice;

    return {
      platform,
      url: targetUrl,
      priceInfo,
      config,
      isCheapest,
    };
  });

  return (
    <div className="flex flex-col gap-4 p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
      <div className="flex items-center justify-between border-b border-[#27272A] pb-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
            Purchase Channels
          </span>
          <span className="text-[10px] font-mono text-zinc-500">
            • Verified Partners
          </span>
        </div>
        <span className="text-[11px] font-mono text-zinc-500">
          Independent Links
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
        {linkItems.map((item) => {
          const priceSubtitle =
            item.priceInfo.type === "stored"
              ? `₹${item.priceInfo.price}`
              : "Check Local Price";

          return (
            <a
              key={item.platform}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
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

              <div className="flex items-center gap-3">
                <span className="text-2xl">{item.config.icon}</span>
                <div className="flex flex-col">
                  <span
                    className={cn(
                      "text-sm font-bold tracking-tight font-sans transition-colors duration-300",
                      item.isCheapest ? "text-black md:group-hover:text-[#F5F2EB]" : "text-white md:group-hover:text-[#F5F2EB]"
                    )}
                  >
                    {item.config.name}
                  </span>
                  <span
                    className={cn(
                      "text-xs font-mono font-medium transition-colors duration-300",
                      item.isCheapest ? "text-black/80 font-bold md:group-hover:text-[#968E85]" : "text-zinc-400 md:group-hover:text-[#968E85]"
                    )}
                  >
                    {priceSubtitle}
                  </span>
                </div>
              </div>

              <div
                className={cn(
                  "flex items-center gap-1 text-xs font-mono font-bold transition-all duration-300 md:group-hover:translate-x-1",
                  item.isCheapest ? "text-black md:group-hover:text-[#D97706]" : "text-zinc-400 md:group-hover:text-[#D97706]"
                )}
              >
                <span>Buy</span>
                <span>↗</span>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
};
