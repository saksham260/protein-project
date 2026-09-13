import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProductCard } from "@/components/product/ProductCard";
import { SearchBar } from "@/components/search/SearchBar";
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
    <div className="flex flex-col gap-24 pb-20 overflow-hidden">
      {/* Hero Section */}
      <section className="relative pt-12 md:pt-20 pb-16 border-b border-white/10 overflow-hidden">
        {/* Ambient Glows */}
        <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-gradient-to-tr from-[#8b5cf6]/20 via-[#00d4aa]/20 to-transparent blur-[140px] pointer-events-none rounded-full" />
        <div className="absolute top-1/2 -left-48 w-[400px] h-[400px] bg-[#00d4aa]/10 blur-[120px] pointer-events-none rounded-full" />
        <div className="absolute top-1/3 -right-48 w-[400px] h-[400px] bg-[#38bdf8]/10 blur-[120px] pointer-events-none rounded-full" />

        <div className="container relative z-10 flex flex-col items-center text-center gap-8 max-w-5xl mx-auto">
          {/* Tagline Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/[0.04] border border-white/15 backdrop-blur-xl shadow-lg">
            <span className="w-2 h-2 rounded-full bg-[#00d4aa] animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-widest text-white/90">
              India&apos;s Independent Protein Transparency Engine
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight leading-[1.08] text-white">
            Stop Paying for Filler. <br />
            Discover{" "}
            <span className="bg-gradient-to-r from-[#00d4aa] via-[#38bdf8] to-[#a855f7] bg-clip-text text-transparent drop-shadow-sm">
              True Protein Value.
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-xl text-slate-300 max-w-3xl leading-relaxed font-normal">
            We analyze Indian whey powders, bars, and drinks to detect maltitol, amino spiking,
            and hidden fillers — calculating your exact cost-per-gram (₹/g) and bioavailability
            tier with zero brand sponsor bias.
          </p>

          {/* Hero Search Bar */}
          <div className="w-full max-w-2xl mt-2">
            <SearchBar placeholder="Search 15 verified Indian products (e.g. Amul, Whey Isolate, Yoga Bar)..." />
          </div>

          {/* Quick Action CTAs */}
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button href="/explore" variant="primary" size="lg" className="shadow-lg shadow-[#00d4aa]/20">
              Explore All Products →
            </Button>
            <Button href="/category/protein-powders" variant="outline" size="lg">
              Browse Whey Powders
            </Button>
          </div>

          {/* Value Stats Strip */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full mt-6 pt-10 border-t border-white/10">
            <div className="flex flex-col items-center p-4 rounded-2xl bg-white/[0.02] border border-white/5">
              <span className="text-3xl sm:text-4xl font-black font-mono text-[#00d4aa]">
                ₹1.67/g
              </span>
              <span className="text-xs text-slate-400 mt-1 font-medium">Lowest ₹ per Gram</span>
            </div>
            <div className="flex flex-col items-center p-4 rounded-2xl bg-white/[0.02] border border-white/5">
              <span className="text-3xl sm:text-4xl font-black font-mono text-white">
                100%
              </span>
              <span className="text-xs text-slate-400 mt-1 font-medium">Human Verified Labels</span>
            </div>
            <div className="flex flex-col items-center p-4 rounded-2xl bg-white/[0.02] border border-white/5">
              <span className="text-3xl sm:text-4xl font-black font-mono text-[#c084fc]">
                4 Tiers
              </span>
              <span className="text-xs text-slate-400 mt-1 font-medium">Bioavailability Grading</span>
            </div>
            <div className="flex flex-col items-center p-4 rounded-2xl bg-white/[0.02] border border-white/5">
              <span className="text-3xl sm:text-4xl font-black font-mono text-[#fbbf24]">
                0 Tolerated
              </span>
              <span className="text-xs text-slate-400 mt-1 font-medium">Hidden Sugar Tricks</span>
            </div>
          </div>
        </div>
      </section>

      {/* Category Navigation Visual Showcase */}
      <section className="container flex flex-col gap-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#00d4aa]">
              Categories
            </span>
            <h2 className="text-3xl sm:text-4xl font-black text-white mt-1">
              Explore by Commodity
            </h2>
          </div>
          <Link
            href="/explore"
            className="text-sm font-bold text-[#00d4aa] hover:underline flex items-center gap-1.5"
          >
            View all categories →
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {CATEGORIES.map((cat) => {
            const img = CATEGORY_IMAGES[cat.slug];
            return (
              <Card
                key={cat.slug}
                href={`/category/${cat.slug}`}
                hoverEffect
                padding="none"
                className="group flex flex-col relative h-80 rounded-3xl overflow-hidden border border-white/10 hover:border-[#00d4aa]/50 transition-all duration-300 shadow-xl"
              >
                {/* Background Image with Dark Vignette */}
                {img && (
                  <Image
                    src={img}
                    alt={cat.name}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                    sizes="(max-width: 768px) 100vw, 25vw"
                  />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-black/30 group-hover:via-black/50 transition-colors" />

                {/* Content Overlay */}
                <div className="relative z-10 flex flex-col justify-between h-full p-6">
                  <div className="flex items-center justify-between">
                    <span className="text-4xl filter drop-shadow">{cat.icon}</span>
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-white/15 backdrop-blur-md text-white border border-white/20">
                      Explore
                    </span>
                  </div>

                  <div className="flex flex-col gap-2">
                    <h3 className="text-2xl font-black text-white group-hover:text-[#00d4aa] transition-colors">
                      {cat.name}
                    </h3>
                    <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
                      {cat.description}
                    </p>
                    <div className="pt-2 flex items-center text-xs font-bold text-[#00d4aa] gap-1 group-hover:translate-x-1 transition-transform">
                      <span>Browse Products</span>
                      <span>→</span>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Featured: Top Cost-Efficiency Picks */}
      <section className="container flex flex-col gap-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#00d4aa]/15 text-[#00d4aa] border border-[#00d4aa]/30 mb-2">
              ⚡ Live Benchmark
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-white">
              Most Cost-Efficient Protein in India
            </h2>
            <p className="text-sm text-slate-400 mt-1 max-w-xl">
              Strictly ordered by verified Cost per Gram of Protein (₹/g). No sponsored placement.
            </p>
          </div>
          <Button href="/explore?sort=cost_per_g_asc" variant="outline" size="md">
            View Complete Leaderboard →
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featured.map((prod) => (
            <ProductCard key={prod.id} product={prod} />
          ))}
        </div>
      </section>

      {/* Transparency Pillars */}
      <section className="container flex flex-col gap-10 py-12 border-t border-white/10">
        <div className="text-center max-w-3xl mx-auto flex flex-col gap-3">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-[#c084fc]">
            Our Audit Standard
          </span>
          <h2 className="text-3xl sm:text-4xl font-black text-white">
            Why Nutritional Transparency Matters
          </h2>
          <p className="text-sm text-slate-400 leading-relaxed">
            Indian protein packaging routinely exploits marketing loopholes. We analyze the raw chemical deck
            and real serving weights to expose misleading claims.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card padding="lg" className="flex flex-col gap-4 rounded-3xl bg-[#141420]/80 border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-red-500/15 text-red-400 border border-red-500/30 flex items-center justify-center font-bold text-2xl">
              🚫
            </div>
            <h3 className="text-lg font-bold text-white">Red-Flag Additive Scanner</h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              We flag laxative polyols (INS 965 Maltitol), cheap amino fillers (Glycine, Taurine spiking),
              hydrogenated palm fats, and hidden high-GI corn syrups marketed as clean.
            </p>
          </Card>

          <Card padding="lg" className="flex flex-col gap-4 rounded-3xl bg-[#141420]/80 border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-[#00d4aa]/15 text-[#00d4aa] border border-[#00d4aa]/30 flex items-center justify-center font-bold text-2xl">
              ⚖️
            </div>
            <h3 className="text-lg font-bold text-white">True Cost per Gram (₹/g)</h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Serving sizes mislead buyers. We calculate the exact protein yield of the entire package
              against the purchase price so you know your true cost per gram of real protein.
            </p>
          </Card>

          <Card padding="lg" className="flex flex-col gap-4 rounded-3xl bg-[#141420]/80 border-white/10">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/15 text-purple-400 border border-purple-500/30 flex items-center justify-center font-bold text-2xl">
              🧬
            </div>
            <h3 className="text-lg font-bold text-white">4-Tier Bioavailability Rating</h3>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              From pure Tier 1 Isolate to complete Tier 3 plant blends and Tier 4 collagen/gelatin fillers,
              our weakest-link algorithm ranks biological muscle-building effectiveness.
            </p>
          </Card>
        </div>
      </section>
    </div>
  );
}
