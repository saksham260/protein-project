"use client";

import React from "react";
import { RedirectLink, Platform } from "@/types/product";
import { buildRedirectUrl, getPriceDisplay } from "@/lib/redirect";
import { formatPrice } from "@/lib/utils";
import { PLATFORM_INFO } from "@/lib/constants";

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
  // Ensure default platforms if none stored
  const platformsToDisplay: Platform[] = ["amazon", "blinkit", "zepto", "instamart"];

  // Map existing links or fallback to search queries
  const linkItems = platformsToDisplay.map((platform) => {
    const existing = redirectLinks.find((l) => l.platform === platform);
    const targetUrl = existing
      ? existing.url
      : buildRedirectUrl(platform, { brandName, productName });

    const priceInfo = getPriceDisplay(platform, existing?.platform_price_inr);
    const config = PLATFORM_INFO[platform];

    return {
      platform,
      url: targetUrl,
      priceInfo,
      config,
    };
  });

  return (
    <div className="flex flex-col gap-3 p-5 rounded-2xl bg-[rgba(18,18,26,0.7)] border border-[rgba(255,255,255,0.08)] backdrop-blur-xl">
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">
          Where to Buy
        </span>
        <span className="text-[11px] text-[var(--text-faint)]">
          Prices verified or local store search
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {linkItems.map((item) => {
          const priceSubtitle =
            item.priceInfo.type === "stored"
              ? `From ${formatPrice(item.priceInfo.price)}`
              : "Check Local Price →";

          return (
            <a
              key={item.platform}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-3.5 rounded-xl border transition-all duration-200 group bg-[rgba(255,255,255,0.03)] hover:bg-[rgba(255,255,255,0.07)] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.2)] hover:-translate-y-0.5"
            >
              <div className="flex items-center gap-2.5">
                <span className="text-xl filter drop-shadow">{item.config.icon}</span>
                <div className="flex flex-col">
                  <span className="text-xs font-bold text-white group-hover:text-[var(--accent-emerald)] transition-colors">
                    {item.config.name}
                  </span>
                  <span className="text-[10px] text-[var(--text-muted)]">
                    {priceSubtitle}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-1 text-xs font-semibold text-[var(--text-muted)] group-hover:text-[var(--accent-emerald)] transition-colors">
                <span>View</span>
                <span className="group-hover:translate-x-0.5 transition-transform">↗</span>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
};
