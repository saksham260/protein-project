import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/Button";
import { ProductCard } from "@/components/product/ProductCard";
import { SearchBar } from "@/components/search/SearchBar";
import { VolumetricText } from "@/components/ui/VolumetricText";
import { RotatingText } from "@/components/ui/RotatingText";
import { ArrowRevealButton } from "@/components/ui/ArrowRevealButton";
import { CATEGORIES } from "@/lib/constants";
import { getProducts } from "@/lib/data";

export const revalidate = 86400; // 24 hours ISR

const CATEGORY_IMAGES: Record<string, string> = {
  "protein-powders": "/images/products/whey-protein-tub.jpg",
  "protein-bars": "/images/products/protein-bar-pack.jpg",
  "rtd-drinks": "/images/products/rtd-protein-drink.jpg",
  "savory-snacks": "/images/products/savory-snack-pack.jpg",
};

export default async function HomePage() {
  const topEfficiencyProducts = await getProducts({ sortBy: "cost_per_g_asc" });
  const featured = topEfficiencyProducts.slice(0, 6);

  return (
    <div className="flex flex-col gap-28 pb-24 overflow-hidden">
      {/* Hero Section: Apple-like Minimalism & Stark Contrast */}
      <section className="relative pt-6 sm:pt-10 md:pt-14 pb-14 sm:pb-20 border-b border-[#27272A] overflow-hidden">
        <div className="container max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 flex flex-col items-center text-center gap-6 sm:gap-7">
          {/* Main Headline: 3-Line Alignment with Rotating Text on 'Products' */}
          <h1 className="flex flex-col items-center text-center gap-1 sm:gap-2 w-full max-w-4xl select-none">
            <span className="relative z-20 text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-black text-white leading-tight tracking-tight">
              Find the best
            </span>

            {/* Line 2: Protein (with Volumetric Hover Shadow Effect) + Stationary Morphed Text */}
            <div className="relative z-20 flex items-center justify-center w-full my-0.5">
              {/* Left Side: 'Protein' (Anchored right to screen midline, NEVER moves when text morphs) */}
              <div className="flex-1 flex justify-end items-center pr-1.5 sm:pr-2.5">
                {/* Mobile: Semantic Plain Text */}
                <span className="sm:hidden text-3xl font-black text-white leading-tight tracking-tight">
                  Protein
                </span>

                {/* Desktop: Volumetric Hover Shadow Effect specifically on 'Protein' */}
                <div className="hidden sm:flex relative w-full max-w-[240px] md:max-w-[300px] lg:max-w-[360px] sm:h-22 md:h-28 lg:h-32 items-center justify-end">
                  <div className="absolute -inset-x-32 md:-inset-x-48 -top-40 -bottom-48 pointer-events-none flex items-center justify-end">
                    <VolumetricText
                      text="Protein"
                      backgroundColor="transparent"
                      textColor="#ffffff"
                      shadowColor="#ffffff"
                      noWrap={true}
                      fitToWidth={true}
                      fitPadding={2}
                      align="right"
                      maxFontSize={84}
                      textMaxWidth={360}
                      textMaxHeight={115}
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
              </div>

              {/* Right Side: Morphing Words (Anchored left to screen midline, expands smoothly to the right) */}
              <div className="flex-1 flex justify-start items-center pl-1.5 sm:pl-2.5">
                <RotatingText
                  prefix=""
                  texts={["Products", "Powder", "Chips", "Drinks", "Bars", "Snacks"]}
                  font={{
                    fontFamily: "var(--font-inter), system-ui, -apple-system, sans-serif",
                    fontSize: "clamp(1.875rem, 5.5vw, 4.5rem)",
                    fontWeight: 900,
                    letterSpacing: "-0.03em",
                    lineHeight: "1.15em",
                    textAlign: "left",
                  }}
                  color="#0A0A0B"
                  badgeBackground="#10B981"
                  badgePaddingX={18}
                  badgePaddingY={4}
                  badgeRadius={16}
                  gap={0}
                  auto={true}
                />
              </div>
            </div>

            <span className="relative z-20 text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-black text-white leading-tight tracking-tight">
              For you
            </span>
          </h1>

          {/* Hero Search Bar */}
          <div className="relative z-30 w-full max-w-2xl">
            <SearchBar placeholder="Search 15 verified Indian products (e.g. Amul, Whey Isolate, Yoga Bar)..." />
          </div>

          {/* Quick Actions */}
          <div className="relative z-10 flex items-center justify-center w-full pt-1">
            <ArrowRevealButton
              label="Explore All Products"
              link="/explore"
              newTab={false}
              colors={{ fill: "#10B981", textColor: "#0A0A0B" }}
              fill="#10B981"
              textColor="#0A0A0B"
              padding="12px 20px 12px 26px"
              rounded={100}
              gap={14}
              font={{
                fontSize: "14px",
                fontWeight: 800,
                letterSpacing: "-0.01em",
              }}
              border={{ borderWidth: 0 }}
              icon={{
                side: "right",
                size: 15,
                type: "icon",
                icon: "arrow",
                strokeWidth: 3,
                color: "#10B981",
                background: "#0A0A0B",
                padding: 6,
                rounded: 100,
              }}
            />
          </div>

          {/* Raw Value Stats Strip (Oversized Monospace Metrics) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full mt-8 pt-10 border-t border-[#27272A]">
            <div className="flex flex-col items-center p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_32px_rgba(0,0,0,0.5)]">
              <span className="text-2xl sm:text-3xl font-black font-mono text-[#10B981]">
                ₹1.67
              </span>
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#A1A1AA] mt-1">
                Lowest ₹ / g
              </span>
            </div>

            <div className="flex flex-col items-center p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_32px_rgba(0,0,0,0.5)]">
              <span className="text-2xl sm:text-3xl font-black font-mono text-white">
                100%
              </span>
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#A1A1AA] mt-1">
                Verified Labels
              </span>
            </div>

            <div className="flex flex-col items-center p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_32px_rgba(0,0,0,0.5)]">
              <span className="text-2xl sm:text-3xl font-black font-mono text-white">
                4 Tiers
              </span>
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#A1A1AA] mt-1">
                Protein Quality
              </span>
            </div>

            <div className="flex flex-col items-center p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_32px_rgba(0,0,0,0.5)]">
              <span className="text-2xl sm:text-3xl font-black font-mono text-[#EF4444]">
                0 Tolerance
              </span>
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#A1A1AA] mt-1">
                Hidden Sugar / Spiking
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Category Navigation Visual Showcase */}
      <section className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-10">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
              Taxonomy
            </span>
            <h2 className="text-3xl sm:text-4xl font-black text-white mt-1 tracking-tight">
              Categories
            </h2>
          </div>
          <Link
            href="/explore"
            className="text-xs font-mono font-bold text-[#E4E4E7] hover:text-[#34D399] transition-colors flex items-center gap-1.5"
          >
            <span>View Complete Catalog</span>
            <span>→</span>
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {CATEGORIES.map((cat) => {
            const img = CATEGORY_IMAGES[cat.slug];
            return (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                className="group flex flex-col relative h-84 rounded-3xl overflow-hidden bg-[#18181B] border border-[#27272A] hover:border-[#3F3F46] transition-all duration-300 shadow-[0_12px_40px_rgba(0,0,0,0.6)] hover:shadow-[0_24px_60px_rgba(0,0,0,0.85)] hover:-translate-y-1.5 select-none"
              >
                {img && (
                  <Image
                    src={img}
                    alt={cat.name}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                    sizes="(max-width: 768px) 100vw, 25vw"
                  />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-[#0A0A0B] via-[#0A0A0B]/70 to-[#0A0A0B]/30 group-hover:via-[#0A0A0B]/55 transition-colors" />

                <div className="relative z-10 flex flex-col justify-between h-full p-6">
                  <div className="flex items-center justify-between">
                    <span className="text-3xl">{cat.icon}</span>
                    <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-[#18181B]/80 text-[#E4E4E7] border border-[#27272A]">
                      Explore
                    </span>
                  </div>

                  <div className="flex flex-col gap-2">
                    <h3 className="text-xl font-bold text-white group-hover:text-[#34D399] transition-colors tracking-tight">
                      {cat.name}
                    </h3>
                    <p className="text-xs text-[#A1A1AA] line-clamp-2 leading-relaxed">
                      {cat.description}
                    </p>
                    <div className="pt-2 flex items-center text-xs font-mono font-bold text-[#34D399] gap-1 group-hover:translate-x-1 transition-transform">
                      <span>Browse Products</span>
                      <span>→</span>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Featured: Top Cost-Efficiency Picks */}
      <section className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-10">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#10B981]">
              Economic Leaderboard
            </span>
            <h2 className="text-3xl sm:text-4xl font-black text-white mt-1 tracking-tight">
              Most Cost-Efficient Protein in India
            </h2>
            <p className="text-xs sm:text-sm font-mono text-[#A1A1AA] mt-1">
              Strictly ordered by verified Cost per Gram of Protein (₹/g). Zero sponsor bias.
            </p>
          </div>
          <Button href="/explore?sort=cost_per_g_asc" variant="secondary" size="md">
            Full Efficiency Rankings →
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featured.map((prod) => (
            <ProductCard key={prod.id} product={prod} />
          ))}
        </div>
      </section>

      {/* Transparency Standards */}
      <section className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-10 py-12 border-t border-[#27272A]">
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
    </div>
  );
}
