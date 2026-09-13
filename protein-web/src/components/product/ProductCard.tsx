import React from "react";
import Image from "next/image";
import { Card } from "@/components/ui/Card";
import { ProteinTierBadge } from "@/components/product/ProteinTierBadge";
import { RedFlagBadges } from "@/components/product/RedFlagBadges";
import { formatPrice, formatPricePerGram, formatPercentage, formatWeight } from "@/lib/utils";
import { ProductVariant, Product, Brand, Category, VariantRedFlag } from "@/types/product";

export interface ProductCardProps {
  product: Product & {
    brand?: Brand;
    category?: Category;
    variants?: (ProductVariant & { red_flags?: VariantRedFlag[] })[];
  };
  variant?: ProductVariant & { red_flags?: VariantRedFlag[] };
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, variant: explicitVariant }) => {
  const variant = explicitVariant || (product.variants && product.variants[0]);
  const brand = product.brand;
  const category = product.category;
  const redFlags = variant?.red_flags || [];

  const targetSlug = product.slug;
  const imageUrl = variant?.image_url || product.image_url;

  return (
    <Card
      href={`/product/${targetSlug}`}
      hoverEffect
      padding="none"
      className="group flex flex-col h-full bg-[#12121c]/90 hover:bg-[#181826] border border-white/10 hover:border-[#00d4aa]/40 transition-all duration-300 rounded-3xl overflow-hidden shadow-xl hover:shadow-[0_16px_40px_-10px_rgba(0,212,170,0.25)]"
    >
      {/* Visual Product Showcase Area */}
      <div className="relative w-full h-60 sm:h-64 bg-gradient-to-b from-[#1a1a28] to-[#101018] flex items-center justify-center overflow-hidden border-b border-white/5">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="flex flex-col items-center justify-center text-center p-6 gap-2">
            <span className="text-5xl filter drop-shadow">{category?.icon || "⚡"}</span>
            <span className="text-xs uppercase font-mono tracking-widest text-[var(--text-faint)]">
              {brand?.name || "Protein"}
            </span>
          </div>
        )}

        {/* Gradient shadow for text contrast */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#12121c] via-black/20 to-transparent pointer-events-none" />

        {/* Top Badges */}
        <div className="absolute top-3.5 left-3.5 right-3.5 flex items-center justify-between z-10">
          {category && (
            <span className="text-[11px] font-semibold px-3 py-1 rounded-full bg-black/60 backdrop-blur-md text-white border border-white/15 shadow-sm">
              {category.icon} {category.name}
            </span>
          )}

          {variant?.protein_tier && (
            <ProteinTierBadge tier={variant.protein_tier} showTooltip={false} size="sm" />
          )}
        </div>

        {/* Bottom image overlay metrics */}
        {variant?.cost_per_g_protein && (
          <div className="absolute bottom-3 left-3.5 z-10">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl bg-black/75 backdrop-blur-md border border-[#00d4aa]/30 shadow-md">
              <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--text-muted)]">
                ₹/g:
              </span>
              <span className="text-xs font-black font-mono text-[#00d4aa]">
                {formatPricePerGram(variant.cost_per_g_protein)}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Content Area */}
      <div className="flex flex-col flex-1 p-5 sm:p-6 gap-4">
        {/* Brand & Title */}
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between gap-2">
            <span className="text-[11px] font-extrabold uppercase tracking-widest text-[#00d4aa] font-mono">
              {brand?.name || "Verified"}
            </span>
            {variant?.net_weight_g && (
              <span className="text-xs font-mono font-medium text-[var(--text-muted)] px-2 py-0.5 rounded-md bg-white/5">
                {formatWeight(variant.net_weight_g)}
              </span>
            )}
          </div>
          <h3 className="text-base sm:text-lg font-bold text-white line-clamp-1 group-hover:text-[#00d4aa] transition-colors leading-snug">
            {product.name}
          </h3>
          {variant?.variant_name && variant.variant_name !== product.name && (
            <p className="text-xs text-[var(--text-muted)] line-clamp-1">
              {variant.variant_name}
            </p>
          )}
        </div>

        {/* Highlighted Macros Strip */}
        <div className="grid grid-cols-2 gap-2 p-3 rounded-2xl bg-white/[0.03] border border-white/[0.06] text-center">
          <div className="flex flex-col items-center justify-center p-1 border-r border-white/5">
            <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--text-muted)]">
              Protein / Pack
            </span>
            <span className="text-base font-extrabold font-mono text-white">
              {variant?.protein_g || 0}
              <span className="text-xs font-normal text-[var(--text-muted)] ml-0.5">g</span>
            </span>
          </div>

          <div className="flex flex-col items-center justify-center p-1">
            <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--text-muted)]">
              Protein Density
            </span>
            <span className="text-base font-extrabold font-mono text-[#38bdf8]">
              {formatPercentage(variant?.protein_density_pct)}
            </span>
          </div>
        </div>

        {/* Clean / Red-Flags Status */}
        <div className="flex items-center justify-between gap-2 pt-1 border-t border-white/5">
          <span className="text-xs font-medium text-[var(--text-muted)]">Formulation:</span>
          <RedFlagBadges flags={redFlags} compact />
        </div>

        {/* Price & Action Footer */}
        <div className="mt-auto pt-3 border-t border-white/5 flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-[10px] uppercase font-mono tracking-wider text-[var(--text-faint)]">
              MRP
            </span>
            <span className="text-lg font-black font-mono text-white">
              {formatPrice(variant?.mrp_inr)}
            </span>
          </div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 group-hover:bg-[#00d4aa] text-xs font-bold text-white group-hover:text-[#0a0a0f] transition-all">
            <span>Details</span>
            <span className="group-hover:translate-x-0.5 transition-transform">→</span>
          </span>
        </div>
      </div>
    </Card>
  );
};
