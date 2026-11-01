"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { ProductWithVariants } from "@/types/product";
import { AwardCategory } from "@/lib/topPicksConfig";
import { getProducts } from "@/lib/catalogClient";
import { CATEGORIES } from "@/lib/constants";
import { useCategory } from "@/context/CategoryContext";
import { ProductCard } from "@/components/product/ProductCard";
import { AwardProductCard } from "@/components/product/AwardProductCard";
import { SuggestedForYou } from "@/components/product/SuggestedForYou";
import { VolumetricText } from "@/components/ui/VolumetricText";
import { RotatingText } from "@/components/ui/RotatingText";

const CATEGORY_IMAGES: Record<string, string> = {
  "protein-powders": "/images/products/whey-protein-tub.jpg",
  "protein-bars": "/images/products/protein-bar-pack.jpg",
  "rtd-drinks": "/images/products/rtd-protein-drink.jpg",
  "savory-snacks": "/images/products/savory-snack-pack.jpg",
  "protein-spreads": "/images/products/peanut-butter-jar.jpg",
  "breakfast-cereals": "/images/products/savory-snack-pack.jpg",
  "dairy": "/images/products/rtd-protein-drink.jpg",
  "cookies-baked": "/images/products/protein-bar-pack.jpg",
};

export interface HomeClientProps {
  /** First batch only; the rest of the catalog loads on scroll. */
  initialProducts: ProductWithVariants[];
  totalProducts: number;
  categoryCounts: Record<string, number>;
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
  totalProducts,
  categoryCounts,
  topPicks,
}) => {
  const router = useRouter();
  const { activeCategory, setActiveCategory } = useCategory();
  const [visibleCount, setVisibleCount] = useState<number>(INITIAL_BATCH_SIZE);
  const [catalog, setCatalog] = useState<ProductWithVariants[]>(initialProducts);
  const fullCatalogRequested = useRef(false);
  const observerTarget = useRef<HTMLDivElement>(null);

  // Infinite scroll: the rest of the catalog downloads the first time the visitor gets near the end
  useEffect(() => {
    if (activeCategory !== "all") return;
    if (visibleCount >= totalProducts) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          if (!fullCatalogRequested.current) {
            fullCatalogRequested.current = true;
            getProducts()
              .then(setCatalog)
              .catch(() => {
                fullCatalogRequested.current = false;
              });
          }
          setVisibleCount((prev) => Math.min(prev + BATCH_INCREMENT, totalProducts));
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
  }, [activeCategory, visibleCount, totalProducts]);

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
    if (slug === "all") {
      setActiveCategory("all");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (slug === "top-picks") {
      setActiveCategory("top-picks");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      setActiveCategory(slug);
      router.push(`/category/${slug}`);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Morphing Discover Protein Products/Chips Banner */}
      <div className="relative z-20 py-3 sm:py-6 select-none bg-transparent">
        <div className="container max-w-5xl mx-auto px-3 sm:px-4 flex items-center justify-center">
          <div className="flex items-center justify-center gap-1.5 sm:gap-3 flex-wrap">
            {/* 'Discover' */}
            <span className="text-xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-white leading-none tracking-tight whitespace-nowrap relative z-10 translate-y-0 sm:-translate-y-[3px]">
              Discover
            </span>

            {/* 'Protein' (Mobile plain text) */}
            <span className="sm:hidden text-xl sm:text-3xl font-black text-white leading-none tracking-tight">
              Protein
            </span>

            {/* 'Protein' (Desktop VolumetricText) */}
            <div className="hidden sm:flex relative w-[140px] md:w-[170px] lg:w-[200px] h-12 md:h-14 lg:h-16 items-center justify-center shrink-0">
              <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[1400px] xl:w-[1800px] max-w-[98vw] h-[520px] md:h-[620px] pointer-events-none flex items-center justify-center z-0">
                <VolumetricText
                  text="Protein"
                  backgroundColor="transparent"
                  textColor="#F5F2EB"
                  shadowColor="#D97706"
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
                  rainbow={0}
                  dither={0}
                  samples={100}
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
            <div className="w-[125px] sm:w-[195px] md:w-[235px] lg:w-[265px] flex items-center justify-start shrink-0 relative z-10">
              <RotatingText
                prefix=""
                texts={ROTATING_WORDS}
                font={ROTATING_FONT}
                color="#FFFFFF"
                badgeBackground="#D97706"
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

        {/* CASE 2: Top Picks Active Tab View */}
        {activeCategory === "top-picks" && (
          <section className="flex flex-col gap-6 sm:gap-8 animate-in fade-in duration-200">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-3 border-b border-[#332D27]">
              <div>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
                  Picked by Formula
                </span>
                <h1 className="text-2xl sm:text-4xl font-black text-[#F5F2EB] mt-0.5 tracking-tight">
                  Top Value Picks
                </h1>
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

        {/* CASE 3: Default "All" Products Experience */}
        {activeCategory === "all" && (
          <>
            {/* SECTION 1: Suggested for You (signed-in users only) */}
            <SuggestedForYou />

            {/* SECTION 2: Explore by Categories */}
            <section className="flex flex-col gap-4 sm:gap-6 pt-8 sm:pt-12 border-t border-[#332D27]/80">
              <div className="flex items-center justify-between gap-2 pb-3 border-b border-[#332D27]/70">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base">🏷️</span>
                    <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
                      Browse By Form Factor
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-3xl font-black text-[#F5F2EB] mt-0.5 tracking-tight">
                    Explore by Categories
                  </h2>
                </div>
              </div>

              {/* Clickable Category Cards Grid */}
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3.5 sm:gap-6 items-stretch">
                {CATEGORIES.map((cat) => {
                  const catImage = CATEGORY_IMAGES[cat.slug] || "/images/products/whey-protein-tub.jpg";

                  return (
                    <Link
                      key={cat.slug}
                      href={`/category/${cat.slug}`}
                      className="group relative flex flex-col overflow-hidden rounded-2xl sm:rounded-3xl bg-[#1C1916] border border-[#332D27] hover:border-[#D97706]/70 transition-all duration-300 text-left p-0 shadow-lg hover:shadow-[0_12px_32px_rgba(217,119,6,0.18)] hover:-translate-y-1 cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#D97706]/50"
                    >
                      {/* Category Image Cover */}
                      <div className="relative w-full aspect-[4/3] sm:aspect-[16/10] overflow-hidden bg-[#141210]">
                        <Image
                          src={catImage}
                          alt={cat.name}
                          fill
                          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
                          className="object-cover object-center group-hover:scale-105 transition-transform duration-500 ease-out"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-[#1C1916] via-[#1C1916]/40 to-transparent" />

                        {/* Count Badge */}
                        <span className="absolute top-2.5 right-2.5 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-[#141210]/85 backdrop-blur-md text-[#F5F2EB] border border-[#332D27]">
                          {categoryCounts[cat.slug] ?? 0} items
                        </span>

                        {/* Floating Icon */}
                        <span className="absolute bottom-2.5 left-3 w-8 h-8 rounded-xl bg-[#141210]/90 border border-[#332D27] flex items-center justify-center text-base shadow-sm">
                          {cat.icon}
                        </span>
                      </div>

                      {/* Card Details */}
                      <div className="p-3.5 sm:p-4 flex flex-col flex-1 justify-between gap-2.5">
                        <div>
                          <h3 className="text-sm sm:text-base font-bold text-[#F5F2EB] group-hover:text-[#D97706] transition-colors tracking-tight flex items-center justify-between">
                            <span>{cat.name}</span>
                            <span className="text-xs text-[#968E85] group-hover:text-[#D97706] group-hover:translate-x-1 transition-all">→</span>
                          </h3>
                          <p className="text-[11px] sm:text-xs font-mono text-[#968E85] line-clamp-2 mt-1 leading-relaxed">
                            {cat.description}
                          </p>
                        </div>

                        <div className="pt-2 border-t border-[#332D27]/60 flex items-center justify-between text-[11px] font-mono font-semibold text-[#D97706]">
                          <span>Explore products</span>
                          <span className="group-hover:translate-x-0.5 transition-transform">↗</span>
                        </div>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </section>

            {/* SECTION 3: All Products with Infinite Scroll */}
            <section className="flex flex-col gap-4 sm:gap-6 pt-8 sm:pt-12 border-t border-[#332D27]/80">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 pb-3 border-b border-[#332D27]/70">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base">📦</span>
                    <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
                      Complete Catalog
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-3xl font-black text-[#F5F2EB] mt-0.5 tracking-tight">
                    All Products
                  </h2>
                </div>
                <Link
                  href="/explore"
                  className="text-xs font-mono font-bold text-[#968E85] hover:text-[#F5F2EB] transition-colors flex items-center gap-1 self-start sm:self-auto"
                >
                  <span>Filter Catalog</span>
                  <span>→</span>
                </Link>
              </div>

              {/* Product Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6 items-stretch">
                {catalog.slice(0, visibleCount).map((product) => (
                  <ProductCard key={`all-${product.id}`} product={product} />
                ))}
              </div>

              {/* Infinite scroll observer target */}
              <div ref={observerTarget} className="py-8 flex flex-col items-center justify-center">
                {visibleCount < totalProducts ? (
                  <div className="flex items-center gap-2.5 px-4 py-2 rounded-full bg-[#1C1916] border border-[#332D27] text-xs font-mono text-[#968E85] shadow-sm">
                    <span className="w-3.5 h-3.5 rounded-full border-2 border-[#D97706] border-t-transparent animate-spin inline-block" />
                    <span>Loading more products ({visibleCount} / {totalProducts})...</span>
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <span className="text-xs font-mono text-[#968E85] uppercase tracking-wider">
                      ✓ Showing all {totalProducts} products
                    </span>
                  </div>
                )}
              </div>
            </section>

            {/* How We Rate Section */}
            <section className="flex flex-col gap-10 py-12 border-t border-[#332D27]">
              <div className="text-center max-w-2xl mx-auto pb-2 flex flex-col items-center gap-1.5">
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#D97706]">
                  Label-Based Analysis
                </span>
                <h2 className="text-3xl sm:text-4xl font-black text-[#F5F2EB] tracking-tight">
                  What We Check
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#1C1916] border border-[#332D27] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">🚫</span>
                  <h3 className="text-lg font-bold text-[#F5F2EB] tracking-tight">Red-Flag Additive Scanner</h3>
                  <p className="text-xs sm:text-sm text-[#968E85] leading-relaxed">
                    We scan ingredient lists for maltitol (INS 965), added amino acids such as glycine and taurine,
                    hydrogenated or palm fats, and hidden sugars like corn syrup.
                  </p>
                </div>

                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#1C1916] border border-[#332D27] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">⚖️</span>
                  <h3 className="text-lg font-bold text-[#F5F2EB] tracking-tight">True Cost per Gram (₹/g)</h3>
                  <p className="text-xs sm:text-sm text-[#968E85] leading-relaxed">
                    Serving sizes make products hard to compare. We divide the price by the total protein in the
                    pack, so you can see the cost of each gram of protein.
                  </p>
                </div>

                <div className="flex flex-col gap-4 p-8 rounded-3xl bg-[#1C1916] border border-[#332D27] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
                  <span className="text-3xl">🧬</span>
                  <h3 className="text-lg font-bold text-[#F5F2EB] tracking-tight">4-Tier Protein Source Guide</h3>
                  <p className="text-xs sm:text-sm text-[#968E85] leading-relaxed">
                    From Tier 1 isolates to Tier 3 plant blends and Tier 4 collagen or added-amino products, based
                    on the protein source named on the label.{" "}
                    <Link href="/how-we-rate" className="text-[#D97706] hover:underline">
                      How we rate
                    </Link>
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
