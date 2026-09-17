"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import { useCart } from "@/context/CartContext";
import { ProductVariant, Product, Brand, Category, VariantRedFlag } from "@/types/product";
import { cn } from "@/lib/utils";

export interface ProductCardProps {
  product: Product & {
    brand?: Brand;
    category?: Category;
    variants?: (ProductVariant & { red_flags?: VariantRedFlag[] })[];
  };
  variant?: ProductVariant & { red_flags?: VariantRedFlag[] };
  showTopBadges?: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  variant: explicitVariant,
  showTopBadges = true,
}) => {
  const { isInCart, toggleItem } = useCart();
  const variant = explicitVariant || (product.variants && product.variants[0]);
  const brand = product.brand;
  const category = product.category;

  const targetSlug = product.slug;
  const imageUrl = variant?.image_url || product.image_url;
  const isShortlisted = isInCart(product.id);

  // Check if product is a powder
  const isPowder =
    category?.slug === "protein-powders" ||
    category?.slug?.includes("powder") ||
    category?.name?.toLowerCase().includes("powder") ||
    product.name.toLowerCase().includes("powder") ||
    variant?.serving_size_label?.toLowerCase().includes("scoop") ||
    false;

  // Format values
  const mrpDisplay = variant?.mrp_inr != null ? variant.mrp_inr.toLocaleString("en-IN") : "—";
  const proteinDisplay = variant?.protein_g != null
    ? `${Number(variant.protein_g.toFixed(1))}g`
    : "—";
  const netWeightDisplay = variant?.net_weight_g
    ? variant.net_weight_g >= 1000
      ? `${Number((variant.net_weight_g / 1000).toFixed(1))}kg`
      : `${variant.net_weight_g}g`
    : "—";

  const handleShortlistClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleItem(product, variant);
  };

  return (
    <Link
      href={`/product/${targetSlug}`}
      className="group flex flex-col h-full bg-[#18181B] rounded-2xl border border-[#27272A] overflow-hidden shadow-[0_4px_20px_rgba(0,0,0,0.4)] hover:shadow-[0_12px_32px_rgba(0,0,0,0.6)] hover:border-[#3F3F46] hover:-translate-y-1 transition-all duration-300 ease-out select-none"
    >
      {/* Product Visual Area */}
      <div className="relative w-full h-36 sm:h-44 md:h-48 bg-[#121215] flex items-center justify-center overflow-hidden border-b border-[#27272A]">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
          />
        ) : (
          <div className="flex flex-col items-center justify-center text-center p-3 gap-1">
            <span className="text-3xl sm:text-4xl">{category?.icon || "⚡"}</span>
            <span className="text-[10px] uppercase font-mono tracking-widest text-zinc-500">
              {brand?.name || "Protein"}
            </span>
          </div>
        )}

        {/* Soft Vignette Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#18181B] via-transparent to-black/30 pointer-events-none" />

        {/* Top Badges & Shortlist Button */}
        <div className="absolute top-2 sm:top-3 left-2 sm:left-3 right-2 sm:right-3 flex items-center justify-between z-10">
          {showTopBadges && category ? (
            <span className="text-[9px] sm:text-[10px] font-sans font-medium px-2 py-0.5 rounded-full bg-[#27272A]/90 text-[#E4E4E7] border border-[#3F3F46] shadow-sm backdrop-blur-sm truncate max-w-[90px] sm:max-w-none">
              {category.name}
            </span>
          ) : (
            <span />
          )}

          <button
            type="button"
            onClick={handleShortlistClick}
            aria-label={isShortlisted ? "Remove from shortlist" : "Add to shortlist"}
            title={isShortlisted ? "Shortlisted" : "Add to shortlist"}
            className={cn(
              "w-7 h-7 sm:w-8 sm:h-8 rounded-full border transition-all duration-200 cursor-pointer shadow-md active:scale-90 ml-auto flex items-center justify-center relative touch-manipulation",
              isShortlisted
                ? "bg-[#10B981] border-[#10B981] text-[#0A0A0B]"
                : "bg-[#18181B]/85 hover:bg-[#27272A] border-[#3F3F46] text-[#A1A1AA] hover:text-white"
            )}
          >
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill={isShortlisted ? "currentColor" : "none"}
              stroke="currentColor"
              strokeWidth="2.5"
            >
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Card Body */}
      <div className="flex flex-col flex-1 p-2.5 sm:p-4 gap-2 sm:gap-3">
        {/* Brand & Title */}
        <div className="flex flex-col gap-0.5 min-h-[2.2rem] sm:min-h-[2.75rem]">
          <span className="text-[9px] sm:text-[10px] uppercase font-mono tracking-wider text-[#A1A1AA] font-semibold truncate">
            {brand?.name || "Independent"}
          </span>
          <h3 className="text-xs sm:text-base font-bold text-white line-clamp-2 leading-snug group-hover:text-[#34D399] transition-colors">
            {product.name}
          </h3>
        </div>

        {/* Key Metrics: ONLY MRP & Protein */}
        <div className="grid grid-cols-2 gap-1.5 sm:gap-2 py-1.5 sm:py-2 px-2 sm:px-3 rounded-xl bg-[#27272A]/60 border border-[#27272A] items-center">
          <div>
            <span className="text-[9px] sm:text-[10px] font-mono uppercase tracking-wider text-[#A1A1AA] block leading-tight">
              MRP
            </span>
            <span className="text-xs sm:text-base font-bold font-mono text-[#10B981] truncate block">
              ₹{mrpDisplay}
            </span>
          </div>
          <div className="text-right">
            <span className="text-[9px] sm:text-[10px] font-mono uppercase tracking-tight text-[#A1A1AA] block leading-tight truncate">
              {isPowder ? "Per Scoop" : "Protein"}
            </span>
            <span className="text-xs sm:text-base font-bold font-mono text-white truncate block">
              {proteinDisplay}
            </span>
          </div>
        </div>

        {/* Footer: ONLY Net Weight */}
        <div className="mt-auto pt-2 sm:pt-2.5 border-t border-[#27272A] flex items-center justify-between text-xs font-mono">
          <span className="text-[9px] sm:text-[10px] text-[#A1A1AA] uppercase tracking-wider font-semibold">
            Net Weight
          </span>
          <span className="text-[10px] sm:text-xs font-bold text-[#E4E4E7]">
            {netWeightDisplay}
          </span>
        </div>
      </div>
    </Link>
  );
};
