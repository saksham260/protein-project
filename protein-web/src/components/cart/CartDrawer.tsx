"use client";

import React, { useEffect, useRef } from "react";
import Image from "next/image";
import Link from "next/link";
import { useCart } from "@/context/CartContext";
import { Platform } from "@/types/product";

const PLATFORM_LABELS: Record<Platform, { name: string; bg: string; text: string }> = {
  amazon: { name: "Amazon", bg: "bg-[#FF9900]/15 border-[#FF9900]/30 hover:bg-[#FF9900]/25", text: "text-[#FF9900]" },
  blinkit: { name: "Blinkit", bg: "bg-[#F8CB46]/15 border-[#F8CB46]/30 hover:bg-[#F8CB46]/25", text: "text-[#F8CB46]" },
  zepto: { name: "Zepto", bg: "bg-[#A55EEA]/15 border-[#A55EEA]/30 hover:bg-[#A55EEA]/25", text: "text-[#A55EEA]" },
  instamart: { name: "Instamart", bg: "bg-[#FC8019]/15 border-[#FC8019]/30 hover:bg-[#FC8019]/25", text: "text-[#FC8019]" },
  d2c: { name: "Direct Brand", bg: "bg-[#10B981]/15 border-[#10B981]/30 hover:bg-[#10B981]/25", text: "text-[#10B981]" },
};

export const CartDrawer: React.FC = () => {
  const { items, itemCount, isCartOpen, closeCart, removeItem, clearCart } = useCart();
  const drawerRef = useRef<HTMLDivElement>(null);

  // Lock body scroll and handle Escape key
  useEffect(() => {
    if (!isCartOpen) return;
    const orig = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeCart();
    };
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = orig;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isCartOpen, closeCart]);

  if (!isCartOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden select-none" aria-modal="true" role="dialog">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity animate-in fade-in duration-200 cursor-pointer"
        onClick={closeCart}
      />

      {/* Drawer Container */}
      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div
          ref={drawerRef}
          className="w-screen max-w-md bg-[#121215] border-l border-[#27272A] shadow-2xl flex flex-col transform transition-transform duration-300 ease-out animate-in slide-in-from-right duration-300"
        >
          {/* Header */}
          <div className="p-5 border-b border-[#27272A] flex items-center justify-between bg-[#18181B]/70">
            <div className="flex items-center gap-2.5">
              <span className="w-7 h-7 rounded-lg bg-[#10B981]/20 border border-[#10B981]/40 flex items-center justify-center text-[#10B981]">
                🛒
              </span>
              <div>
                <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                  Your Shortlist
                  <span className="text-xs px-2 py-0.5 rounded-full bg-[#27272A] text-[#A1A1AA] font-mono">
                    {itemCount}
                  </span>
                </h2>
                <p className="text-[11px] text-[#A1A1AA] font-mono mt-0.5">
                  Saved products with instant direct buy links
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {itemCount > 0 && (
                <button
                  type="button"
                  onClick={clearCart}
                  className="text-[11px] font-mono text-[#A1A1AA] hover:text-red-400 px-2 py-1 rounded transition-colors"
                >
                  Clear
                </button>
              )}
              <button
                type="button"
                onClick={closeCart}
                className="w-8 h-8 rounded-full bg-[#27272A] hover:bg-[#3F3F46] text-[#E4E4E7] flex items-center justify-center text-sm transition-colors cursor-pointer"
                aria-label="Close shortlist"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Body Content */}
          <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
            {itemCount === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-8 gap-4 text-[#A1A1AA]">
                <div className="w-16 h-16 rounded-2xl bg-[#18181B] border border-[#27272A] flex items-center justify-center text-3xl">
                  🏷️
                </div>
                <div className="flex flex-col gap-1">
                  <h3 className="text-base font-bold text-white font-sans">No products shortlisted yet</h3>
                  <p className="text-xs font-mono max-w-xs leading-relaxed">
                    Click the shortlist bookmark on any product card to compare and buy directly from top stores.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={closeCart}
                  className="mt-2 px-5 py-2 rounded-full bg-[#10B981] text-[#0A0A0B] text-xs font-mono font-bold hover:bg-[#34D399] transition-colors"
                >
                  Explore Catalog
                </button>
              </div>
            ) : (
              items.map(({ productId, product, variant }) => {
                const imageUrl = variant?.image_url || product.image_url;
                const redirectLinks = variant?.redirect_links || [];

                return (
                  <div
                    key={productId}
                    className="p-4 rounded-2xl bg-[#18181B] border border-[#27272A] hover:border-[#3F3F46] transition-all flex flex-col gap-3 group relative"
                  >
                    {/* Top Row: Thumbnail + Title + Remove */}
                    <div className="flex items-start gap-3">
                      <div className="relative w-14 h-14 rounded-xl bg-[#121215] border border-[#27272A] overflow-hidden shrink-0 flex items-center justify-center">
                        {imageUrl ? (
                          <Image
                            src={imageUrl}
                            alt={product.name}
                            fill
                            className="object-cover"
                            sizes="56px"
                          />
                        ) : (
                          <span className="text-xl select-none">{product.category?.icon || "⚡"}</span>
                        )}
                      </div>

                      <div className="flex-1 min-w-0 pr-6">
                        <span className="text-[10px] uppercase font-mono tracking-wider text-[#A1A1AA]">
                          {product.brand?.name || "Brand"}
                        </span>
                        <Link
                          href={`/product/${product.slug}`}
                          onClick={closeCart}
                          className="block font-bold text-white text-sm hover:text-[#34D399] transition-colors line-clamp-1 leading-snug"
                        >
                          {product.name}
                        </Link>
                        {variant?.variant_name && variant.variant_name !== product.name && (
                          <span className="text-[11px] text-[#A1A1AA] line-clamp-1">
                            {variant.variant_name}
                          </span>
                        )}

                        {variant?.mrp_inr && (
                          <div className="flex items-baseline gap-1 font-mono text-[#10B981] mt-1">
                            <span className="text-xs">₹</span>
                            <span className="text-sm font-black">
                              {variant.mrp_inr.toLocaleString("en-IN")}
                            </span>
                            <span className="text-[10px] text-[#A1A1AA]">MRP</span>
                          </div>
                        )}
                      </div>

                      {/* Remove Button */}
                      <button
                        type="button"
                        onClick={() => removeItem(productId)}
                        className="absolute top-3 right-3 text-[#A1A1AA] hover:text-red-400 p-1 rounded-md transition-colors"
                        title="Remove from shortlist"
                        aria-label="Remove item"
                      >
                        ✕
                      </button>
                    </div>

                    {/* Buy Links Row */}
                    <div className="flex flex-col gap-1.5 pt-2 border-t border-[#27272A]/80">
                      <span className="text-[10px] font-mono uppercase tracking-widest text-[#A1A1AA]">
                        Instant Buy Options:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {redirectLinks.length > 0 ? (
                          redirectLinks.map((link) => {
                            const info = PLATFORM_LABELS[link.platform] || {
                              name: link.platform,
                              bg: "bg-white/10 border-white/20 hover:bg-white/15",
                              text: "text-white",
                            };
                            return (
                              <a
                                key={link.id}
                                href={link.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border text-[11px] font-mono font-bold transition-colors ${info.bg} ${info.text}`}
                              >
                                <span>{info.name}</span>
                                {link.platform_price_inr && (
                                  <span className="opacity-85 font-normal">
                                    ₹{link.platform_price_inr.toLocaleString("en-IN")}
                                  </span>
                                )}
                                <span className="text-[9px]">↗</span>
                              </a>
                            );
                          })
                        ) : (
                          <div className="flex items-center gap-2">
                            <a
                              href={`https://www.amazon.in/s?k=${encodeURIComponent(product.name)}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border text-[11px] font-mono font-bold bg-[#FF9900]/15 border-[#FF9900]/30 hover:bg-[#FF9900]/25 text-[#FF9900] transition-colors"
                            >
                              <span>Search Amazon</span>
                              <span className="text-[9px]">↗</span>
                            </a>
                            <Link
                              href={`/product/${product.slug}`}
                              onClick={closeCart}
                              className="text-[11px] font-mono text-[#34D399] hover:underline"
                            >
                              View Details →
                            </Link>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Drawer Footer */}
          {itemCount > 0 && (
            <div className="p-4 border-t border-[#27272A] bg-[#18181B]/80 flex flex-col gap-2">
              <div className="flex items-center justify-between text-xs font-mono text-[#A1A1AA]">
                <span>Total Shortlisted</span>
                <span className="text-white font-bold">{itemCount} items</span>
              </div>
              <p className="text-[10px] text-zinc-400 font-mono text-center">
                Prices and availability are tracked live across Indian stores.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
