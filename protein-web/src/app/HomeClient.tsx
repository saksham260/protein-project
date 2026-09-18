"use client";

import React, { useState, useEffect, useRef, useMemo } from "react";
import Link from "next/link";
import { ProductWithVariants } from "@/types/product";
import { AwardCategory } from "@/lib/topPicksConfig";
import { CATEGORIES } from "@/lib/constants";
import { useCategory } from "@/context/CategoryContext";
import { ProductCard } from "@/components/product/ProductCard";
import { AwardProductCard } from "@/components/product/AwardProductCard";
import { ExploreAllCard } from "@/components/product/ExploreAllCard";
import { VolumetricText } from "@/components/ui/VolumetricText";
import { RotatingText } from "@/components/ui/RotatingText";

const CATEGORY_IMAGES: Record<string, string> = {
  "protein-powders": "/images/products/whey-protein-tub.jpg",
  "protein-bars": "/images/products/protein-bar-pack.jpg",
  "rtd-drinks": "/images/products/rtd-protein-drink.jpg",
  "savory-snacks": "/images/products/savory-snack-pack.jpg",
};

export interface HomeClientProps {
  initialProducts: ProductWithVariants[];
  topPicks: Array<{
    award: AwardCategory;
    product: ProductWithVariants;
    editorialBlurb?: string;
  }>;
}

const INITIAL_BATCH_SIZE = 12;
const BATCH_INCREMENT = 12;

const ROTATING_WORDS = ["Products", "Powder", "Chips", "Drinks", "Bars", "Snacks"];
const ROTATING_FONT = {
  fontFamily: "var(--font-inter), system-ui, -apple-system, sans-serif",
  fontSize: "clamp(1.2rem, 3.5vw, 2.75rem)",
  fontWeight: 900,
  letterSpacing: "-0.03em",
  lineHeight: "1.15em",
  textAlign: "left" as const,
};

export const HomeClient: React.FC<HomeClientProps> = ({
  initialProducts,
  topPicks,
}) => {
  const { activeCategory, setActiveCategory } = useCategory();
  const [visibleCount, setVisibleCount] = useState<number>(INITIAL_BATCH_SIZE);
  const observerTarget = useRef<HTMLDivElement>(null);

  // Group products by category for quick lookup and category sections
  const productsByCategory = useMemo(() => {
    const map: Record<string, ProductWithVariants[]> = {};
    for (const cat of CATEGORIES) {
      map[cat.slug] = [];
    }
    for (const prod of initialProducts) {
      const slug = prod.category?.slug;
      if (slug && map[slug]) {
        map[slug].push(prod);
      }
    }
    return map;
  }, [initialProducts]);

  // Products to display in current view
  const filteredProducts = useMemo(() => {
    if (activeCategory === "all") {
      return initialProducts.slice(0, visibleCount);
    }
    if (activeCategory === "top-picks") {
      return [];
    }
    return productsByCategory[activeCategory] || [];
  }, [activeCategory, initialProducts, visibleCount, productsByCategory]);

  // Infinite scroll observer for "all" products
  useEffect(() => {
    if (activeCategory !== "all") return;
    if (visibleCount >= initialProducts.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((prev) => Math.min(prev + BATCH_INCREMENT, initialProducts.length));
        }
      },
      { threshold: 0.1, rootMargin: "300px" }
    );

    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }

    return () => {
      if (currentTarget) observer.unobserve(currentTarget);
    };
  }, [activeCategory, visibleCount, initialProducts.length]);

  // Scroll spy for category sections when in "all" view
  useEffect(() => {
    if (activeCategory !== "all") return;

    const sections = [
      { id: "top-picks-section", tab: "top-picks" },
      ...CATEGORIES.map((cat) => ({ id: `cat-${cat.slug}`, tab: cat.slug })),
    ];

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const found = sections.find((s) => s.id === entry.target.id);
            if (found && activeCategory === "all") {
              // We keep activeCategory as "all" so we don't break the mixed view,
              // but we can observe active sections.
            }
          }
        }
      },
      { threshold: 0.3 }
    );

    for (const sec of sections) {
      const el = document.getElementById(sec.id);
      if (el) observer.observe(el);
    }

    return () => observer.disconnect();
  }, [activeCategory]);

  const handleSelectCategory = (slug: string) => {
    setActiveCategory(slug);
    window.scrollTo({ top: 0, behavior: "instant" });
  };

  const activeCategoryMeta = CATEGORIES.find((c) => c.slug === activeCategory);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Morphing Discover Protein Products/Chips Banner */}
      <div className="relative z-20 py-3 sm:py-6 select-none bg-transparent">
        <div className="container max-w-5xl mx-auto px-3 sm:px-4 flex items-center justify-center">
          <div className="flex items-center justify-center gap-1.5 sm:gap-3 flex-wrap">
            {/* 'Discover' */}
            <span className="text-xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-white leading-none tracking-tight whitespace-nowrap relative translate-y-0 sm:-translate-y-[3px]">
              Discover
            </span>

            {/* 'Protein' (Mobile plain text) */}
            <span className="sm:hidden text-xl sm:text-3xl font-black text-white leading-none tracking-tight">
              Protein
            </span>

            {/* 'Protein' (Desktop VolumetricText) */}
            <div className="hidden sm:flex relative w-[140px] md:w-[170px] lg:w-[200px] h-12 md:h-14 lg:h-16 items-center justify-center shrink-0">
              <div className="absolute -inset-x-20 -inset-y-20 pointer-events-none flex items-center justify-center">
                <VolumetricText
                  text="Protein"
                  backgroundColor="transparent"
                  textColor="#ffffff"
                  shadowColor="#ffffff"
                  noWrap={true}
                  fitToWidth={true}
                  fitPadding={2}
                  align="center"
                  maxFontSize={54}
                  textMaxWidth={200}
                  textMaxHeight={65}
                  lightX={50}
                  lightY={25}
                  lightSize={36}
                  lightFalloff={48}
                  shadowStrength={180}
                  rainbow={25}
                  samples={96}
                  quality={100}
                  font={{
                    fontFamily: "Inter, system-ui, sans-serif",
                    fontWeight: 900,
                    lineHeight: 1,
                    letterSpacing: "-0.03em",
                  }}
                />
              </div>
            </div>

            {/* Morphing Words (Fixed reserved width: expands to the right without moving 'Discover Protein') */}
            <div className="w-[125px] sm:w-[195px] md:w-[235px] lg:w-[265px] flex items-center justify-start shrink-0">
              <RotatingText
                prefix=""
                texts={ROTATING_WORDS}
                font={ROTATING_FONT}
                color="#0A0A0B"
                badgeBackground="#10B981"
                badgePaddingX={12}
                badgePaddingY={3}
                badgeRadius={12}
                gap={0}
                auto={true}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="container max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 pt-3 sm:pt-6 pb-20 flex flex-col gap-8 sm:gap-14">
        {/* CASE 1: Filtered Specific Category View */}
        {activeCategory !== "all" && activeCategory !== "top-picks" && activeCategoryMeta && (
          <section className="flex flex-col gap-6 animate-in fade-in duration-200">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#27272A]">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{activeCategoryMeta.icon}</span>
                <div>
                  <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                    {activeCategoryMeta.name}
                  </h1>
                  <p className="text-xs font-mono text-[#A1A1AA] mt-0.5">
                    Showing {filteredProducts.length} verified products • {activeCategoryMeta.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => handleSelectCategory("all")}
                  className="px-3.5 py-1.5 rounded-full bg-[#18181B] hover:bg-[#27272A] border border-[#27272A] text-xs font-mono text-[#E4E4E7] hover:text-white transition-colors"
                >
                  ← Show All Products
                </button>
                <Link
                  href={`/category/${activeCategoryMeta.slug}`}
                  className="px-3.5 py-1.5 rounded-full bg-[#10B981]/15 hover:bg-[#10B981]/25 border border-[#10B981]/30 text-xs font-mono text-[#10B981] font-bold transition-colors"
                >
                  Advanced Filters →
                </Link>
              </div>
            </div>

            {filteredProducts.length === 0 ? (
              <div className="p-12 text-center text-[#A1A1AA] font-mono text-sm">
                No products found in this category.
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
                {filteredProducts.slice(0, 11).map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
                {filteredProducts.length > 11 && (
                  <ExploreAllCard
                    href={`/category/${activeCategoryMeta.slug}`}
                  />
                )}
              </div>
            )}
          </section>
        )}

        {/* CASE 2: Top Picks Active Tab View */}
        {activeCategory === "top-picks" && (
          <section className="flex flex-col gap-6 sm:gap-8 animate-in fade-in duration-200">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-4 border-b border-[#27272A]">
              <div>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
                  Editor&apos;s Picks
                </span>
                <h1 className="text-2xl sm:text-4xl font-black text-white mt-1 tracking-tight">
                  Top Picks of the Month
                </h1>
                <p className="text-xs sm:text-sm font-mono text-[#A1A1AA] mt-1">
                  Hand-verified and ranked by real nutritional data. No sponsorships, zero brand bias.
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleSelectCategory("all")}
                className="px-4 py-2 rounded-full bg-[#18181B] hover:bg-[#27272A] border border-[#27272A] text-xs font-mono text-[#E4E4E7] hover:text-white transition-colors self-start sm:self-auto"
              >
                ← Back to All Products
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch pt-2">
              {topPicks.map(({ award, product, editorialBlurb }) => (
                <AwardProductCard
                  key={award.id}
                  award={award}
                  product={product}
                  editorialBlurb={editorialBlurb}
                />
              ))}
            </div>
          </section>
        )}

        {/* CASE 3: Default "All" Products Experience (Zepto-style discovery) */}
        {activeCategory === "all" && (
          <>
            {/* All Products Catalog: 11 Products + 12th Explore All Card */}
            <section className="flex flex-col gap-4 sm:gap-6 pt-1">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 pb-2 border-b border-[#27272A]/70">
                <div>
                  <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
                    Direct Catalog
                  </span>
                  <h2 className="text-xl sm:text-3xl font-black text-white mt-0.5 tracking-tight">
                    All Products
                  </h2>
                  <p className="text-xs font-mono text-[#A1A1AA] mt-0.5">
                    Showing {Math.min(11, filteredProducts.length)} of {initialProducts.length} verified products
                  </p>
                </div>
                <Link
                  href="/explore"
                  className="text-xs font-mono font-bold text-[#A1A1AA] hover:text-white transition-colors flex items-center gap-1"
                >
                  Sort & Filter Catalog →
                </Link>
              </div>

              {/* Product Grid: 11 products + 12th Explore All Card */}
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
                {filteredProducts.slice(0, 11).map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
                {filteredProducts.length > 11 && (
                  <ExploreAllCard
                    href="/explore"
                  />
                )}
              </div>
            </section>

            {/* Top Picks Showcase (Available while scrolling down right after All Products catalog) */}
            <section id="top-picks-section" className="flex flex-col gap-4 sm:gap-5 pt-6 sm:pt-8 border-t border-[#27272A]/70">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base">🏆</span>
                    <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
                      Editor&apos;s Verified Selection
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-3xl font-black text-white mt-0.5 tracking-tight">
                    Top Picks of the Month
                  </h2>
                  <p className="text-xs font-mono text-[#A1A1AA] mt-0.5">
                    Highest biological purity, density, and value across Indian brands.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => handleSelectCategory("top-picks")}
                  className="text-xs font-mono font-bold text-[#E4E4E7] hover:text-[#34D399] transition-colors flex items-center gap-1.5 self-start sm:self-auto"
                >
                  <span>View All Awards</span>
                  <span>→</span>
                </button>
              </div>

              {/* Product Grid: Top Picks matching identical catalog card dimensions */}
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch pt-2">
                {topPicks.map(({ award, product, editorialBlurb }) => (
                  <AwardProductCard
                    key={award.id}
                    award={award}
                    product={product}
                    editorialBlurb={editorialBlurb}
                  />
                ))}
              </div>
            </section>

            {/* Category Showcases (Zepto/Blinkit Grouped Sections) */}
            <div className="flex flex-col gap-12 sm:gap-16 pt-4">
              {CATEGORIES.map((cat) => {
                const prods = productsByCategory[cat.slug] || [];
                if (prods.length === 0) return null;
                const hasMore = prods.length > 11;
                const previewProds = hasMore ? prods.slice(0, 11) : prods;
                const catImage = CATEGORY_IMAGES[cat.slug] || "/images/products/whey-protein-tub.jpg";

                return (
                  <section
                    key={cat.slug}
                    id={`cat-${cat.slug}`}
                    className="flex flex-col gap-4 sm:gap-6 pt-6 sm:pt-8 border-t border-[#27272A]/70"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 pb-2">
                      <div className="flex items-center gap-2 sm:gap-3">
                        <span className="text-2xl sm:text-3xl">{cat.icon}</span>
                        <div>
                          <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                            {cat.name}
                          </h2>
                          <p className="text-xs font-mono text-[#A1A1AA] line-clamp-1">
                            {cat.description}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3 self-start sm:self-auto">
                        <button
                          type="button"
                          onClick={() => handleSelectCategory(cat.slug)}
                          className="text-xs font-mono font-bold text-[#10B981] hover:underline"
                        >
                          View all {prods.length} in {cat.name}
                        </button>
                        <Link
                          href={`/category/${cat.slug}`}
                          className="text-xs font-mono font-bold text-[#E4E4E7] hover:text-[#34D399] transition-colors flex items-center gap-1"
                        >
                          <span>Full Specs</span>
                          <span>→</span>
                        </Link>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
                      {previewProds.map((p) => (
                        <ProductCard key={p.id} product={p} />
                      ))}
                      {hasMore && (
                        <ExploreAllCard
                          href={`/category/${cat.slug}`}
                        />
                      )}
                    </div>
                  </section>
                );
              })}
            </div>

            {/* Scientific Deconstruction Trust Section */}
            <section className="flex flex-col gap-10 py-12 border-t border-[#27272A]">
              <div className="text-center max-w-2xl mx-auto flex flex-col gap-3">
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
                  Audit Methodology
                </span>
                <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                  Scientific Deconstruction
                </h2>
                <p className="text-sm text-[#A1A1AA] leading-relaxed font-sans">
                  Indian packaged food labeling routinely exploits loopholes. We audit chemical decks and
                  exact pack weights to expose deceptive claims.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">🚫</span>
                  <h3 className="text-lg font-bold text-white tracking-tight">Red-Flag Additive Scanner</h3>
                  <p className="text-xs sm:text-sm text-[#A1A1AA] leading-relaxed">
                    We flag laxative polyols (INS 965 Maltitol GI 35-52), cheap amino spiking (Glycine, Taurine),
                    hydrogenated palm fats, and hidden high-GI corn syrups marketed as clean.
                  </p>
                </div>

                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">⚖️</span>
                  <h3 className="text-lg font-bold text-white tracking-tight">True Cost per Gram (₹/g)</h3>
                  <p className="text-xs sm:text-sm text-[#A1A1AA] leading-relaxed">
                    Serving sizes mislead buyers. We compute the exact net protein yield across the entire package
                    against the retail price so you discover your true cost per gram of real protein.
                  </p>
                </div>

                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">🧬</span>
                  <h3 className="text-lg font-bold text-white tracking-tight">4-Tier Bioavailability Rating</h3>
                  <p className="text-xs sm:text-sm text-[#A1A1AA] leading-relaxed">
                    From pure Tier 1 Isolate to complete Tier 3 plant blends and Tier 4 collagen/gelatin fillers,
                    our weakest-link algorithm ranks biological muscle-building effectiveness.
                  </p>
                </div>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
};
