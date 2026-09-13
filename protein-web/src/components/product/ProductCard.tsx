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
  // Use explicit variant or first active variant from product
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
      className="group flex flex-col h-full bg-[rgba(18,18,26,0.65)] hover:bg-[rgba(24,24,36,0.8)] border-[rgba(255,255,255,0.07)] hover:border-[rgba(0,212,170,0.3)] transition-all duration-300 rounded-2xl overflow-hidden"
    >
      {/* Top Banner / Image Area */}
      <div className="relative w-full h-48 bg-gradient-to-br from-[#1c1c2b] to-[#12121a] flex items-center justify-center overflow-hidden border-b border-[rgba(255,255,255,0.06)]">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={product.name}
            fill
            className="object-contain p-4 group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="flex flex-col items-center justify-center text-center p-6 gap-2">
            <span className="text-4xl filter drop-shadow">{category?.icon || "⚡"}</span>
            <span className="text-xs uppercase font-mono tracking-widest text-[var(--text-faint)]">
              {brand?.name || "Protein"}
            </span>
          </div>
        )}

        {/* Category Pill Tag */}
        {category && (
          <div className="absolute top-3 left-3 z-10">
            <span className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-[rgba(0,0,0,0.6)] backdrop-blur-md text-[var(--text-secondary)] border border-[rgba(255,255,255,0.1)]">
              {category.name}
            </span>
          </div>
        )}

        {/* Tier Badge */}
        {variant?.protein_tier && (
          <div className="absolute top-3 right-3 z-10">
            <ProteinTierBadge tier={variant.protein_tier} showTooltip={false} size="sm" />
          </div>
        )}
      </div>

      {/* Content Body */}
      <div className="flex flex-col flex-1 p-5 gap-3.5">
        {/* Brand & Title */}
        <div className="flex flex-col gap-1">
          <div className="flex items-center justify-between gap-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--accent-emerald)]">
              {brand?.name || "Verified Brand"}
            </span>
            {variant?.net_weight_g && (
              <span className="text-xs font-mono text-[var(--text-faint)]">
                {formatWeight(variant.net_weight_g)}
              </span>
            )}
          </div>
          <h3 className="text-base font-bold text-[var(--text-primary)] line-clamp-1 group-hover:text-[var(--accent-emerald)] transition-colors">
            {product.name}
          </h3>
          {variant?.variant_name && variant.variant_name !== product.name && (
            <p className="text-xs text-[var(--text-muted)] line-clamp-1">
              {variant.variant_name}
            </p>
          )}
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-2 p-2.5 rounded-xl bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.05)] text-center">
          <div className="flex flex-col items-center justify-center p-1 border-r border-[rgba(255,255,255,0.06)]">
            <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">
              Cost / g Protein
            </span>
            <span className="text-sm font-bold font-mono text-[#00d4aa]">
              {formatPricePerGram(variant?.cost_per_g_protein)}
            </span>
          </div>
          <div className="flex flex-col items-center justify-center p-1">
            <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">
              Protein Density
            </span>
            <span className="text-sm font-bold font-mono text-[var(--text-primary)]">
              {formatPercentage(variant?.protein_density_pct)}
            </span>
          </div>
        </div>

        {/* Red Flags Status */}
        <div className="flex items-center justify-between gap-2 pt-1 border-t border-[rgba(255,255,255,0.06)]">
          <span className="text-xs text-[var(--text-muted)]">Ingredients:</span>
          <RedFlagBadges flags={redFlags} compact />
        </div>

        {/* Price & CTA Footer */}
        <div className="mt-auto pt-2 flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">MRP</span>
            <span className="text-base font-extrabold text-[var(--text-primary)]">
              {formatPrice(variant?.mrp_inr)}
            </span>
          </div>
          <span className="text-xs font-semibold text-[var(--accent-emerald)] flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
            View Details →
          </span>
        </div>
      </div>
    </Card>
  );
};
