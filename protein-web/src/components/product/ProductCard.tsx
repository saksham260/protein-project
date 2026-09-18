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
  const { isInCart, addItem, removeItem } = useCart();
  const variant = explicitVariant || (product.variants && product.variants[0]);
  const brand = product.brand;
  const category = product.category;

  const targetSlug = product.slug;
  const imageUrl = variant?.image_url || product.image_url;
  const isAdded = isInCart(product.id);

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

  const handleCartClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isAdded) {
      removeItem(product.id);
    } else {
      addItem(product, variant);
    }
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

        {/* Top Category Badge */}
        {showTopBadges && category && (
          <div className="absolute top-2 sm:top-3 left-2 sm:left-3 z-10">
            <span className="text-[9px] sm:text-[10px] font-sans font-medium px-2 py-0.5 rounded-full bg-[#27272A]/90 text-[#E4E4E7] border border-[#3F3F46] shadow-sm backdrop-blur-sm truncate max-w-[120px] sm:max-w-none">
              {category.name}
            </span>
          </div>
        )}

        {/* Bottom Right: Add / Remove Cart Button */}
        <div className="absolute bottom-2 sm:bottom-2.5 right-2 sm:right-2.5 z-10">
          <button
            type="button"
            onClick={handleCartClick}
            aria-label={isAdded ? "Remove from cart" : "Add to cart"}
            title={isAdded ? "Remove from cart" : "Add to cart"}
            className={cn(
              "flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-3 sm:py-1.5 rounded-full font-sans font-bold text-[9.5px] sm:text-xs",
              "transition-all duration-200 cursor-pointer shadow-lg active:scale-95 touch-manipulation backdrop-blur-md",
              isAdded
                ? "bg-[#DC2626]/90 hover:bg-[#EF4444] text-white border border-[#EF4444] shadow-[0_0_14px_rgba(239,68,68,0.35)]"
                : "bg-[#18181B]/90 hover:bg-[#27272A] text-white hover:text-[#34D399] border border-[#3F3F46] hover:border-[#10B981]/60 shadow-[0_4px_12px_rgba(0,0,0,0.6)]"
            )}
          >
            {isAdded ? (
              <>
                <svg
                  className="w-3 h-3 sm:w-3.5 sm:h-3.5 stroke-[2.5] shrink-0"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
                <span className="leading-none select-none tracking-tight whitespace-nowrap">
                  Remove from Cart
                </span>
              </>
            ) : (
              <>
                <svg
                  className="w-3 h-3 sm:w-3.5 sm:h-3.5 shrink-0 text-[#10B981]"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="8" cy="21" r="1" />
                  <circle cx="19" cy="21" r="1" />
                  <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
                </svg>
                <span className="leading-none select-none tracking-tight whitespace-nowrap">
                  Add to Cart
                </span>
              </>
            )}
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
