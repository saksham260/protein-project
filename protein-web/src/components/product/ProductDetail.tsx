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
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { formatPrice, formatPricePerGram, formatPercentage } from "@/lib/utils";

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

  return (
    <div className="container py-8 md:py-12 flex flex-col gap-10 max-w-6xl mx-auto">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
        <Link href="/" className="hover:text-white">
          Home
        </Link>
        <span>/</span>
        <Link href="/explore" className="hover:text-white">
          Explore
        </Link>
        <span>/</span>
        <Link href={`/category/${category.slug}`} className="hover:text-white">
          {category.name}
        </Link>
        <span>/</span>
        <span className="text-[var(--accent-emerald)] font-semibold">{product.name}</span>
      </div>

      {/* Top Product Hero Block */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Image Area */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          <div className="relative w-full h-80 sm:h-96 rounded-3xl bg-gradient-to-br from-[#1c1c2b] to-[#12121a] border border-[rgba(255,255,255,0.08)] flex items-center justify-center overflow-hidden shadow-2xl backdrop-blur-xl">
            {imageUrl ? (
              <Image
                src={imageUrl}
                alt={product.name}
                fill
                priority
                className="object-contain p-6"
                sizes="(max-width: 1024px) 100vw, 40vw"
              />
            ) : (
              <div className="flex flex-col items-center justify-center text-center p-8 gap-3">
                <span className="text-6xl filter drop-shadow">{category.icon}</span>
                <span className="text-xs uppercase font-mono tracking-widest text-[var(--text-faint)]">
                  {brand.name}
                </span>
              </div>
            )}

            {/* Category tag */}
            <div className="absolute top-4 left-4">
              <span className="text-xs font-semibold px-3 py-1 rounded-full bg-black/60 backdrop-blur-md text-[var(--text-secondary)] border border-[rgba(255,255,255,0.1)]">
                {category.name}
              </span>
            </div>

            {/* Tier badge */}
            {activeVariant?.protein_tier && (
              <div className="absolute top-4 right-4">
                <ProteinTierBadge tier={activeVariant.protein_tier} size="md" />
              </div>
            )}
          </div>

          {/* Quick Metrics Bar Under Image */}
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="p-3 rounded-xl bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.06)]">
              <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">
                Cost / g
              </span>
              <span className="block text-sm font-bold font-mono text-[#00d4aa]">
                {formatPricePerGram(activeVariant?.cost_per_g_protein)}
              </span>
            </div>

            <div className="p-3 rounded-xl bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.06)]">
              <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">
                Density
              </span>
              <span className="block text-sm font-bold font-mono text-white">
                {formatPercentage(activeVariant?.protein_density_pct)}
              </span>
            </div>

            <div className="p-3 rounded-xl bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.06)]">
              <span className="text-[10px] uppercase tracking-wider text-[var(--text-faint)]">
                Pack MRP
              </span>
              <span className="block text-sm font-bold font-mono text-white">
                {formatPrice(activeVariant?.mrp_inr)}
              </span>
            </div>
          </div>
        </div>

        {/* Right Column: Title, Variants, Actions */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-[var(--accent-emerald)] font-mono">
                {brand.name}
              </span>
              {brand.is_verified && (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-[rgba(0,212,170,0.1)] text-[#00d4aa] border border-[rgba(0,212,170,0.25)]">
                  ✓ Verified Brand
                </span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white">
              {product.name}
            </h1>
            {product.description && (
              <p className="text-xs sm:text-sm text-[var(--text-secondary)] leading-relaxed">
                {product.description}
              </p>
            )}
          </div>

          {/* Variant Selector */}
          <VariantSelector
            variants={variants}
            selectedIndex={selectedVariantIndex}
            onSelectIndex={setSelectedVariantIndex}
          />

          {/* Red Flag Alert Summary Box */}
          {redFlags.length === 0 ? (
            <div className="flex items-center gap-3 p-4 rounded-2xl bg-[rgba(0,212,170,0.08)] border border-[rgba(0,212,170,0.3)] text-xs text-[#00e6b8]">
              <span className="text-2xl">🛡️</span>
              <div className="flex flex-col">
                <span className="font-bold text-sm">Clean Formulation — Zero Red Flags</span>
                <span className="text-[var(--text-secondary)]">
                  No maltitol, amino spiking, hydrogenated fats, or hidden sugars detected.
                </span>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-3 p-4 rounded-2xl bg-[rgba(239,68,68,0.08)] border border-[rgba(239,68,68,0.3)]">
              <div className="flex items-center gap-2 text-[var(--accent-red)]">
                <span className="text-xl">⚠️</span>
                <span className="font-bold text-sm">
                  {redFlags.length} Formulation Red Flag{redFlags.length > 1 ? "s" : ""} Detected
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                {redFlags.map((flag) => (
                  <div
                    key={flag.id || flag.flag_label}
                    className="flex flex-col p-2.5 rounded-xl bg-[rgba(0,0,0,0.4)] border border-[rgba(239,68,68,0.2)]"
                  >
                    <span className="font-bold text-[var(--text-primary)]">{flag.flag_label}</span>
                    <span className="text-[11px] text-[var(--text-muted)] mt-0.5">
                      {flag.flag_description}
                    </span>
                    {flag.matched_ingredient && (
                      <span className="text-[10px] text-[var(--accent-red)] font-mono mt-1">
                        Matched: {flag.matched_ingredient} {flag.ins_number ? `(${flag.ins_number})` : ""}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Where to Buy CTA Buttons */}
          <RedirectButtons
            redirectLinks={activeVariant?.redirect_links || []}
            brandName={brand.name}
            productName={product.name}
          />
        </div>
      </div>

      {/* Nutritional Facts & Protein Profile Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start pt-6 border-t border-[rgba(255,255,255,0.08)]">
        {/* Left: Nutrition Facts Table with Toggle */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">Full Nutritional Panel</h2>
            <NutritionToggle
              mode={nutritionMode}
              onChange={setNutritionMode}
              packWeightG={activeVariant?.net_weight_g}
            />
          </div>

          <NutritionPanel variant={activeVariant} mode={nutritionMode} />
        </div>

        {/* Right: Protein Profile & Ingredients */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* Protein Quality Breakdown */}
          <Card padding="lg" className="flex flex-col gap-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-[var(--accent-emerald)]">
              Protein Quality Breakdown
            </h3>

            <div className="flex flex-col gap-3 text-xs">
              <div className="flex items-center justify-between pb-2 border-b border-[rgba(255,255,255,0.06)]">
                <span className="text-[var(--text-muted)]">Primary Protein Source:</span>
                <span className="font-bold text-white">
                  {activeVariant?.primary_protein_source || "Unspecified Source"}
                </span>
              </div>

              <div className="flex items-center justify-between pb-2 border-b border-[rgba(255,255,255,0.06)]">
                <span className="text-[var(--text-muted)]">Bioavailability Tier:</span>
                <ProteinTierBadge tier={activeVariant?.protein_tier} />
              </div>

              <div className="flex items-center justify-between pb-2 border-b border-[rgba(255,255,255,0.06)]">
                <span className="text-[var(--text-muted)]">Amino Spiking Status:</span>
                <span
                  className={`font-semibold ${
                    activeVariant?.has_added_free_form_aminos
                      ? "text-[var(--accent-red)]"
                      : "text-[#00d4aa]"
                  }`}
                >
                  {activeVariant?.has_added_free_form_aminos
                    ? "⚠️ Spiked with Free-Form Aminos"
                    : "✓ No Spiking Detected"}
                </span>
              </div>
            </div>
          </Card>

          {/* Full Ingredients Deck */}
          <Card padding="lg" className="flex flex-col gap-3">
            <h3 className="text-sm font-bold uppercase tracking-wider text-[var(--text-primary)]">
              Ingredient Deck ({activeVariant?.ingredient_list.length || 0})
            </h3>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {activeVariant?.ingredient_list.map((ing, idx) => {
                const isFlagged = redFlags.some(
                  (rf) =>
                    rf.matched_ingredient &&
                    ing.toLowerCase().includes(rf.matched_ingredient.toLowerCase())
                );

                return (
                  <span
                    key={idx}
                    className={`px-2.5 py-1 rounded-lg text-xs font-medium border ${
                      isFlagged
                        ? "bg-[rgba(239,68,68,0.15)] text-[#f87171] border-[rgba(239,68,68,0.4)]"
                        : "bg-[rgba(255,255,255,0.03)] text-[var(--text-secondary)] border-[rgba(255,255,255,0.08)]"
                    }`}
                  >
                    {ing}
                  </span>
                );
              })}
            </div>
          </Card>

          {/* Allergens & Dietary Tags */}
          <Card padding="lg" className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <span className="text-xs font-semibold text-[var(--text-muted)]">Allergens:</span>
              <div className="flex flex-wrap gap-1.5">
                {activeVariant?.allergens.length ? (
                  activeVariant.allergens.map((a) => (
                    <Badge key={a} variant="warning" size="sm">
                      Contains {a}
                    </Badge>
                  ))
                ) : (
                  <span className="text-xs text-[var(--text-faint)]">None declared</span>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-2 pt-2 border-t border-[rgba(255,255,255,0.06)]">
              <span className="text-xs font-semibold text-[var(--text-muted)]">Dietary Tags:</span>
              <div className="flex flex-wrap gap-1.5">
                {activeVariant?.dietary_tags.map((tag) => (
                  <Badge key={tag} variant="default" size="sm">
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
