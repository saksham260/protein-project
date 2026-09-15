import React from "react";
import Image from "next/image";
import Link from "next/link";
import { OversizedMetric } from "@/components/ui/OversizedMetric";
import { ProteinTierBadge } from "@/components/product/ProteinTierBadge";
import { RedFlagWarning } from "@/components/product/RedFlagWarning";
import { formatPrice } from "@/lib/utils";
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

  // Format values for raw typography display
  const costPerG = variant?.cost_per_g_protein != null ? variant.cost_per_g_protein.toFixed(1) : "—";
  const density = variant?.protein_density_pct != null ? variant.protein_density_pct.toFixed(0) : "—";
  const packProtein = variant?.protein_g != null ? variant.protein_g.toFixed(0) : "0";

  return (
    <Link
      href={`/product/${targetSlug}`}
      className="group flex flex-col h-full bg-[#18181B] rounded-3xl border border-[#27272A] overflow-hidden shadow-[0_8px_30px_rgba(0,0,0,0.5)] hover:shadow-[0_20px_50px_rgba(0,0,0,0.7)] hover:border-[#3F3F46] hover:-translate-y-1.5 transition-all duration-300 ease-out select-none"
    >
      {/* Product Visual Area */}
      <div className="relative w-full h-64 bg-[#121215] flex items-center justify-center overflow-hidden border-b border-[#27272A]">
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
            <span className="text-5xl">{category?.icon || "⚡"}</span>
            <span className="text-xs uppercase font-mono tracking-widest text-zinc-500">
              {brand?.name || "Protein"}
            </span>
          </div>
        )}

        {/* Soft Vignette Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#18181B] via-transparent to-black/30 pointer-events-none" />

        {/* Top Badges */}
        <div className="absolute top-4 left-4 right-4 flex items-center justify-between z-10">
          {category && (
            <span className="text-[11px] font-sans font-medium px-2.5 py-1 rounded-full bg-[#27272A]/90 text-[#E4E4E7] border border-[#3F3F46] shadow-sm backdrop-blur-sm">
              {category.name}
            </span>
          )}

          {variant?.protein_tier && (
            <ProteinTierBadge tier={variant.protein_tier} size="sm" />
          )}
        </div>

        {/* Bottom subtle weight badge */}
        {variant?.net_weight_g && (
          <div className="absolute bottom-3 right-4 z-10">
            <span className="text-[10px] font-mono font-medium text-zinc-400 px-2 py-0.5 rounded-md bg-[#27272A]/80 border border-[#3F3F46]">
              {variant.net_weight_g}g
            </span>
          </div>
        )}
      </div>

      {/* Card Body with Oversized Metrics */}
      <div className="flex flex-col flex-1 p-6 gap-5">
        {/* Brand & Title */}
        <div className="flex flex-col gap-1">
          <span className="text-[11px] uppercase font-mono tracking-widest text-[#A1A1AA] font-semibold">
            {brand?.name || "Independent"}
          </span>
          <h3 className="text-lg font-bold text-white line-clamp-1 leading-snug group-hover:text-[#34D399] transition-colors">
            {product.name}
          </h3>
          {variant?.variant_name && variant.variant_name !== product.name && (
            <p className="text-xs text-[#A1A1AA] line-clamp-1">
              {variant.variant_name}
            </p>
          )}
        </div>

        {/* DOMINANT RAW METRICS SECTION */}
        <div className="grid grid-cols-2 gap-4 py-4 px-4 rounded-2xl bg-[#27272A]/60 border border-[#27272A]">
          <OversizedMetric
            label="Cost / g Protein"
            prefix="₹"
            value={costPerG}
            size="md"
            accent="neon"
            subtext="Economic Value"
          />

          <OversizedMetric
            label="Protein Density"
            value={density}
            unit="%"
            size="md"
            accent="white"
            subtext={`${packProtein}g per pack`}
          />
        </div>

        {/* Clinical Red-Flags Status */}
        <div className="flex items-center justify-between pt-1 border-t border-[#27272A]">
          <span className="text-xs text-[#A1A1AA] font-mono uppercase tracking-wider">Formulation</span>
          <RedFlagWarning flags={redFlags} mode="compact" />
        </div>

        {/* Footer: MRP & Action */}
        <div className="mt-auto pt-3 border-t border-[#27272A] flex items-center justify-between">
          <div className="flex items-baseline gap-1 font-mono">
            <span className="text-[11px] text-[#A1A1AA] uppercase">MRP</span>
            <span className="text-base font-bold text-[#E4E4E7]">
              {formatPrice(variant?.mrp_inr)}
            </span>
          </div>

          <span className="inline-flex items-center gap-1 text-xs font-mono font-bold text-[#34D399] group-hover:translate-x-1 transition-transform">
            <span>Deconstruct</span>
            <span>→</span>
          </span>
        </div>
      </div>
    </Link>
  );
};
