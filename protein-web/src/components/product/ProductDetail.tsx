"use client";

import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ProductWithVariants } from "@/types/product";
import { VariantSelector } from "@/components/product/VariantSelector";
import { ProteinTierBadge } from "@/components/product/ProteinTierBadge";
import { NutritionPanel } from "@/components/product/NutritionPanel";
import { NutritionToggle, NutritionMode } from "@/components/product/NutritionToggle";
import { RedirectButtons } from "@/components/product/RedirectButtons";
import { RedFlagWarning } from "@/components/product/RedFlagWarning";
import { OversizedMetric } from "@/components/ui/OversizedMetric";
import { formatPrice, formatPricePerGram } from "@/lib/utils";

export interface ProductDetailProps {
  product: ProductWithVariants;
}

export const ProductDetail: React.FC<ProductDetailProps> = ({ product }) => {
  const [selectedVariantIndex, setSelectedVariantIndex] = useState(0);
  const [nutritionMode, setNutritionMode] = useState<NutritionMode>("per_pack");

  const variants = product.variants || [];
  const activeVariant = variants[selectedVariantIndex] || variants[0];
  const brand = product.brand;
  const category = product.category;
  const redFlags = activeVariant?.red_flags || [];
  const imageUrl = activeVariant?.image_url || product.image_url;

  const costPerG = activeVariant?.cost_per_g_protein != null ? activeVariant.cost_per_g_protein.toFixed(1) : "—";
  const density = activeVariant?.protein_density_pct != null ? activeVariant.protein_density_pct.toFixed(0) : "—";
  const totalProteinPack = activeVariant
    ? (activeVariant.protein_g * (activeVariant.servings_per_pack || 1)).toFixed(0)
    : "—";

  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 md:py-16 flex flex-col gap-12">
      {/* Minimalist Breadcrumbs */}
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono text-zinc-500">
        <Link href="/" className="hover:text-white transition-colors">
          Home
        </Link>
        <span>/</span>
        <Link href="/explore" className="hover:text-white transition-colors">
          Explore
        </Link>
        <span>/</span>
        <Link href={`/category/${category.slug}`} className="hover:text-white transition-colors">
          {category.name}
        </Link>
        <span>/</span>
        <span className="text-zinc-200 font-bold">{product.name}</span>
      </nav>

      {/* Asymmetrical Split-Screen Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-start">
        {/* Left Side: Product Image */}
        <div className="lg:col-span-5 lg:sticky lg:top-24 flex flex-col gap-6">
          <div className="relative w-full h-[380px] sm:h-[480px] rounded-3xl bg-[#121215] border border-[#27272A] flex items-center justify-center overflow-hidden shadow-[0_24px_70px_rgba(0,0,0,0.85)]">
            {imageUrl ? (
              <Image
                src={imageUrl}
                alt={product.name}
                fill
                priority
                className="object-cover object-center transition-transform duration-700 hover:scale-105"
                sizes="(max-width: 1024px) 100vw, 42vw"
              />
            ) : (
              <div className="flex flex-col items-center justify-center text-center p-8 gap-3">
                <span className="text-7xl">{category.icon}</span>
                <span className="text-xs uppercase font-mono tracking-widest text-[#A1A1AA]">
                  {brand.name}
                </span>
              </div>
            )}

            {/* Subtle Vignette */}
            <div className="absolute inset-0 bg-gradient-to-t from-[#18181B]/80 via-transparent to-black/30 pointer-events-none" />

            {/* Top Category Badge */}
            <div className="absolute top-5 left-5 z-10">
              <span className="text-xs font-mono px-3 py-1 rounded-full bg-[#27272A]/90 text-[#E4E4E7] border border-[#3F3F46] shadow-sm backdrop-blur-sm">
                {category.name}
              </span>
            </div>

            {/* Top Right Tier Badge */}
            {activeVariant?.protein_tier && (
              <div className="absolute top-5 right-5 z-10">
                <ProteinTierBadge tier={activeVariant.protein_tier} size="md" />
              </div>
            )}

            {/* Bottom Specs */}
            <div className="absolute bottom-5 left-5 right-5 z-10 flex items-center justify-between pointer-events-none">
              <span className="px-3 py-1 rounded-full bg-[#27272A]/90 text-xs font-mono text-[#E4E4E7] border border-[#3F3F46]">
                Net Wt: {activeVariant?.net_weight_g}g
              </span>
              <span className="px-3 py-1 rounded-full bg-[#27272A]/90 text-xs font-mono text-[#E4E4E7] border border-[#3F3F46]">
                Serving: {activeVariant?.serving_size_g}g
              </span>
            </div>
          </div>

          {/* Clinical Formulation Warning Banner */}
          <RedFlagWarning flags={redFlags} mode="banner" />
        </div>

        {/* Right Side: Data, Metrics, Actions */}
        <div className="lg:col-span-7 flex flex-col gap-8">
          {/* Brand & Title Header */}
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase tracking-widest text-[#10B981] font-bold">
                {brand.name}
              </span>
              {brand.is_verified && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#27272A] text-[#A1A1AA] border border-[#3F3F46]">
                  ✓ Verified Brand
                </span>
              )}
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
              {product.name}
            </h1>

            {product.description && (
              <p className="text-sm text-[#A1A1AA] leading-relaxed mt-1 font-sans">
                {product.description}
              </p>
            )}
          </div>

          {/* OVERSIZED CORE METRICS DISPLAY */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
            <OversizedMetric
              label="MRP"
              prefix="₹"
              value={activeVariant?.mrp_inr != null ? activeVariant.mrp_inr.toLocaleString("en-IN") : "—"}
              size="lg"
              accent="neon"
              subtext="Retail Price"
            />

            <OversizedMetric
              label="Protein Density"
              value={density}
              unit="%"
              size="lg"
              accent="white"
              subtext="Cals from protein"
            />

            <OversizedMetric
              label="Pack Total"
              value={totalProteinPack}
              unit="g"
              size="lg"
              accent="muted"
              subtext={activeVariant?.net_weight_g ? `${activeVariant.net_weight_g}g pack` : "Total Protein"}
            />
          </div>

          {/* Variant Selector */}
          <VariantSelector
            variants={variants}
            selectedIndex={selectedVariantIndex}
            onSelectIndex={setSelectedVariantIndex}
          />

          {/* Purchase Section with Cheapest in Neon Yellow */}
          <RedirectButtons
            redirectLinks={activeVariant?.redirect_links || []}
            brandName={brand.name}
            productName={product.name}
          />

          {/* Nutrition Panel with iOS-style Segmented Toggle */}
          <div className="flex flex-col gap-4 pt-4 border-t border-[#27272A]">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold text-white tracking-tight">
                  Nutritional Breakdown
                </h2>
                <p className="text-xs font-mono text-[#A1A1AA]">
                  Calculated directly from verified FSSAI lab labels
                </p>
              </div>

              <NutritionToggle
                mode={nutritionMode}
                onChange={setNutritionMode}
                packWeightG={activeVariant?.net_weight_g}
              />
            </div>

            <NutritionPanel variant={activeVariant} mode={nutritionMode} />
          </div>

          {/* Clinical Red-Flag Breakdown Section */}
          <div className="flex flex-col gap-4 pt-6 border-t border-[#27272A]">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-white tracking-tight">
                Clinical Formulation Audit
              </h2>
              <span className="text-xs font-mono text-[#A1A1AA]">
                Independent scanner analysis
              </span>
            </div>

            <RedFlagWarning flags={redFlags} mode="clinical-deck" />
          </div>

          {/* Protein Quality & Ingredients Deck */}
          <div className="flex flex-col gap-6 pt-6 border-t border-[#27272A]">
            <div className="p-6 rounded-3xl bg-[#18181B] border border-[#27272A] flex flex-col gap-4 shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
              <h3 className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
                Protein Quality & Bioavailability
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
                <div className="flex flex-col gap-1 p-4 rounded-2xl bg-[#27272A]/60 border border-[#27272A]">
                  <span className="text-[#A1A1AA] uppercase text-[10px]">Primary Protein Source</span>
                  <span className="text-white font-bold text-sm">
                    {activeVariant?.primary_protein_source || "Not Specified"}
                  </span>
                </div>

                <div className="flex flex-col gap-1 p-4 rounded-2xl bg-[#27272A]/60 border border-[#27272A]">
                  <span className="text-[#A1A1AA] uppercase text-[10px]">Amino Spiking Status</span>
                  <span
                    className={`font-bold text-sm ${
                      activeVariant?.has_added_free_form_aminos
                        ? "text-[#EF4444]"
                        : "text-[#10B981]"
                    }`}
                  >
                    {activeVariant?.has_added_free_form_aminos
                      ? "⚠️ Free-Form Aminos Added"
                      : "✓ Pure Formulation (Clean)"}
                  </span>
                </div>
              </div>
            </div>

            {/* Complete Ingredient Deck */}
            <div className="p-6 rounded-3xl bg-[#18181B] border border-[#27272A] flex flex-col gap-3 shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
                  Ingredient Deck ({activeVariant?.ingredient_list.length || 0})
                </h3>
                <span className="text-[10px] font-mono text-[#A1A1AA]">
                  Flagged items highlighted in Red
                </span>
              </div>

              <div className="flex flex-wrap gap-2 pt-1">
                {activeVariant?.ingredient_list.map((ing, idx) => {
                  const isFlagged = redFlags.some(
                    (rf) =>
                      rf.matched_ingredient &&
                      ing.toLowerCase().includes(rf.matched_ingredient.toLowerCase())
                  );

                  return (
                    <span
                      key={idx}
                      className={`px-3 py-1.5 rounded-full text-xs font-mono transition-colors ${
                        isFlagged
                          ? "bg-[#EF4444]/15 text-[#F87171] border border-[#EF4444]/30 font-bold"
                          : "bg-[#27272A] text-[#E4E4E7] border border-[#3F3F46]"
                      }`}
                    >
                      {ing}
                    </span>
                  );
                })}
              </div>
            </div>

            {/* Declared Allergens & Dietary Profile */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-6 rounded-3xl bg-[#18181B] border border-[#27272A] flex flex-col gap-2 shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                <span className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
                  Declared Allergens
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {activeVariant?.allergens.length ? (
                    activeVariant.allergens.map((a) => (
                      <span
                        key={a}
                        className="px-2.5 py-1 rounded-full text-xs font-mono bg-[#27272A] text-[#E4E4E7] border border-[#3F3F46]"
                      >
                        {a}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs font-mono text-[#A1A1AA]">None declared</span>
                  )}
                </div>
              </div>

              <div className="p-6 rounded-3xl bg-[#18181B] border border-[#27272A] flex flex-col gap-2 shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                <span className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">
                  Dietary Profile
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {activeVariant?.dietary_tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2.5 py-1 rounded-full text-xs font-mono bg-[#27272A] text-[#E4E4E7] border border-[#3F3F46]"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
