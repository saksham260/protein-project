import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProductCard } from "@/components/product/ProductCard";
import { CATEGORIES } from "@/lib/constants";
import { getProducts } from "@/lib/data";

export const revalidate = 86400; // 24 hours ISR

export default async function HomePage() {
  const topEfficiencyProducts = await getProducts({ sortBy: "cost_per_g_asc" });
  const featured = topEfficiencyProducts.slice(0, 6);

  return (
    <div className="flex flex-col gap-20 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 md:pt-20 pb-12 border-b border-[rgba(255,255,255,0.06)]">
        {/* Glow background accents */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-[rgba(139,92,246,0.18)] to-[rgba(0,212,170,0.18)] blur-[120px] pointer-events-none rounded-full" />

        <div className="container relative z-10 flex flex-col items-center text-center gap-6 max-w-4xl mx-auto">
          {/* Tagline Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.1)] backdrop-blur-md">
            <span className="w-2 h-2 rounded-full bg-[var(--accent-emerald)] animate-ping" />
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
              Independent Nutrition Transparency • India
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight leading-[1.1] text-white">
            Stop Paying for Filler. <br />
            Discover{" "}
            <span className="bg-gradient-to-r from-[var(--accent-emerald)] via-[#38bdf8] to-[var(--accent-purple)] bg-clip-text text-transparent">
              Real Protein Value.
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-[var(--text-secondary)] max-w-2xl leading-relaxed">
            We scan Indian protein powders, bars, and drinks to detect maltitol, amino spiking, and
            hidden sugars — rating true cost-per-gram (₹/g) and protein density without brand bias.
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Button href="/explore" variant="primary" size="lg">
              Explore All Products →
            </Button>
            <Button href="/search" variant="secondary" size="lg">
              Search by Brand
            </Button>
          </div>

          {/* Trust Metrics Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 w-full mt-8 pt-8 border-t border-[rgba(255,255,255,0.06)]">
            <div className="flex flex-col items-center">
              <span className="text-2xl sm:text-3xl font-extrabold font-mono text-[var(--accent-emerald)]">
                ₹1.67/g
              </span>
              <span className="text-xs text-[var(--text-muted)]">Lowest Cost per Gram</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-2xl sm:text-3xl font-extrabold font-mono text-white">
                100%
              </span>
              <span className="text-xs text-[var(--text-muted)]">Human Label Verified</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-2xl sm:text-3xl font-extrabold font-mono text-[var(--accent-purple)]">
                4 Tiers
              </span>
              <span className="text-xs text-[var(--text-muted)]">Bioavailability Grading</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-2xl sm:text-3xl font-extrabold font-mono text-[var(--accent-amber)]">
                0 Tolerated
              </span>
              <span className="text-xs text-[var(--text-muted)]">Hidden Sugar Deception</span>
            </div>
          </div>
        </div>
      </section>

      {/* Category Navigation Shortcuts */}
      <section className="container flex flex-col gap-6">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2">
          <div>
            <span className="text-xs font-mono uppercase tracking-widest text-[var(--accent-emerald)]">
              Browse Categories
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold mt-1">Explore by Product Type</h2>
          </div>
          <Link
            href="/explore"
            className="text-xs font-semibold text-[var(--accent-emerald)] hover:underline flex items-center gap-1"
          >
            View all categories →
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {CATEGORIES.map((cat) => (
            <Card
              key={cat.slug}
              href={`/category/${cat.slug}`}
              hoverEffect
              padding="lg"
              className="flex flex-col gap-3 group"
            >
              <span className="text-3xl filter drop-shadow">{cat.icon}</span>
              <div className="flex flex-col gap-1">
                <h3 className="text-lg font-bold group-hover:text-[var(--accent-emerald)] transition-colors">
                  {cat.name}
                </h3>
                <p className="text-xs text-[var(--text-muted)] line-clamp-2">
                  {cat.description}
                </p>
              </div>
              <div className="mt-auto pt-2 flex items-center text-xs font-semibold text-[var(--text-secondary)] group-hover:text-[var(--accent-emerald)] transition-colors">
                Browse products →
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Featured: Top Cost-Efficiency Picks */}
      <section className="container flex flex-col gap-6">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[rgba(0,212,170,0.1)] text-[#00d4aa] border border-[rgba(0,212,170,0.25)] mb-1">
              Top Value Benchmark
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold">Most Efficient Protein Picks</h2>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] mt-1">
              Ranked strictly by Cost per Gram of Protein (₹/g) across verified Indian labels.
            </p>
          </div>
          <Button href="/explore?sort=cost_per_g_asc" variant="outline" size="sm">
            See Full Ranked Grid
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featured.map((prod) => (
            <ProductCard key={prod.id} product={prod} />
          ))}
        </div>
      </section>

      {/* How The Engine Works */}
      <section className="container flex flex-col gap-8 py-8 border-t border-[rgba(255,255,255,0.06)]">
        <div className="text-center max-w-2xl mx-auto flex flex-col gap-2">
          <span className="text-xs font-mono uppercase tracking-widest text-[var(--accent-purple)]">
            Our Rating Methodology
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold">Why Protein Transparency Matters</h2>
          <p className="text-xs sm:text-sm text-[var(--text-muted)]">
            Not all protein is created equal. Most packaging hides cheap fillers behind deceptive
            serving sizes and chemical aliases.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card padding="lg" className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-[rgba(239,68,68,0.15)] text-[var(--accent-red)] border border-[rgba(239,68,68,0.3)] flex items-center justify-center font-bold text-lg">
              🚫
            </div>
            <h3 className="text-base font-bold">Red-Flag Ingredient Scanner</h3>
            <p className="text-xs text-[var(--text-secondary)] leading-relaxed">
              We audit ingredient lists for Maltitol (INS 965), Hydrogenated Palm Oils, added
              Glycine/Taurine (amino spiking), and hidden high-GI syrups masquerading as &quot;clean&quot;.
            </p>
          </Card>

          <Card padding="lg" className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-[rgba(0,212,170,0.15)] text-[var(--accent-emerald)] border border-[rgba(0,212,170,0.3)] flex items-center justify-center font-bold text-lg">
              ⚖️
            </div>
            <h3 className="text-base font-bold">True Cost per Gram (₹/g)</h3>
            <p className="text-xs text-[var(--text-secondary)] leading-relaxed">
              We scale protein content across entire tubs and packs. You see exactly how many rupees
              you pay for 1 gram of usable protein, not arbitrary serving marketing.
            </p>
          </Card>

          <Card padding="lg" className="flex flex-col gap-3">
            <div className="w-10 h-10 rounded-xl bg-[rgba(139,92,246,0.15)] text-[var(--accent-purple)] border border-[rgba(139,92,246,0.3)] flex items-center justify-center font-bold text-lg">
              🧬
            </div>
            <h3 className="text-base font-bold">4-Tier Bioavailability Rating</h3>
            <p className="text-xs text-[var(--text-secondary)] leading-relaxed">
              From pure Tier 1 Isolate to Tier 3 complete plant blends and Tier 4 collagen-spiked
              fillers, know the biological quality of your protein before purchasing.
            </p>
          </Card>
        </div>
      </section>
    </div>
  );
}
