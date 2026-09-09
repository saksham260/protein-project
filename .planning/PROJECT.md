# The Protein Discovery Engine

## What This Is

An independent, evidence-based protein product comparison and discovery platform targeting the Indian consumer market. It cuts through deceptive FMCG marketing by analyzing packaged protein products (bars, shakes, powders, snacks), calculating true economic efficiency (₹/g protein) and nutritional density (% calories from protein), detecting red-flag ingredients (maltitol, amino spiking, hydrogenated oils, hidden sugars), and routing consumers to the best purchase channels (Amazon, Blinkit, Zepto, D2C).

## Core Value

Provide uncompromised, objective nutritional transparency and value-per-gram rankings so Indian consumers can make truly informed protein purchase decisions without deceptive marketing claims.

## Business Context

- **Customer**: Health-conscious Indian consumers, gym-goers, diabetics, and keto/fitness enthusiasts purchasing packaged protein products in India.
- **Revenue model**: Affiliate commissions from Amazon and D2C partner redirects, plus future sponsored brand verification (clearly badged and non-conflicting).
- **Success metric**: Monthly active product comparisons, outbound purchase redirect CTR, and catalog depth across Indian protein brands.
- **Strategy notes**: Initial focus on high-intent categories (RTD drinks, protein bars, whey/plant powders, savory protein snacks) with trusted, unbiased red-flag badges.

## Requirements

### Validated

(None yet — greenfield project bootstrapping from architecture specification)

### Active

- [ ] **Data Model & Storage**: Supabase PostgreSQL database schema with products, variants, red flags, categories, brands, redirect links, and user preferences.
- [ ] **Row-Level Security & Indexing**: Public read for catalog, user-scoped RLS for preferences/favorites, and GIN/trigram indexes for fast filtering and search.
- [ ] **Calculated Metrics Engine**: Per-pack and per-100g computation of Cost per Gram of Protein (₹/g), Protein Density (% calories from protein), and True Net Carbs.
- [ ] **Red-Flag Detection Engine**: Ingredient scanner matching against curated alias dictionary (maltitol GI 35-52, amino spiking, hydrogenated/palm fat, hidden sugars).
- [ ] **Protein Tier Classifier**: Four-tier hierarchy classification (Tier 1 Isolate to Tier 4 Fillers) based on the weakest link in protein blends.
- [ ] **Interactive Python ETL CLI**: Human-in-the-loop CLI (`protein-etl`) supporting Shopify `/products.json` scraping, manual entry, auto-flagging, and Supabase upsert.
- [ ] **Frontend Application**: Next.js 14+ (App Router, TypeScript) responsive web application (`protein-web`) with custom design system.
- [ ] **Explore & Search**: Faceted product discovery filtering by category, dietary tags, allergens, protein tier, with sorting by ₹/g and density.
- [ ] **Product Detail Experience**: Nutrition panel with Per-Pack / Per-100g toggle, red-flag explanations, and redirect buttons with smart price display.
- [ ] **Personalization & Auth**: Supabase Google OAuth + email fallback, user dietary profile, and rule-based recommendation feed.

### Out of Scope

- **Automated unmonitored scraping bots**: Scrapers run exclusively through human-in-the-loop CLI verification to maintain 100% data integrity and avoid legal/blocking friction.
- **Dynamic quick-commerce price scraping**: Blinkit, Zepto, and Swiggy Instamart prices vary by dark store / pincode; showing stale prices erodes trust, so quick-commerce redirects show "Check Local Price →".
- **Heavy machine learning recommendation systems**: Rule-based SQL filtering (`NOT (pv.allergens && user_prefs.allergens)`) is fully deterministic, transparent, and performant at this scale.
- **Native mobile apps**: Responsive web app first with PWA capabilities; native apps deferred to future milestones.

## Context

- **Target Market**: Indian packaged food/supplement ecosystem governed by FSSAI labeling guidelines.
- **Common Industry Deceptions**: Maltitol in "sugar-free" bars causing glucose spikes; amino spiking (glycine/taurine) artificially boosting Kjeldahl nitrogen tests; palm oil and hydrogenated fat used as cheap texturizers.
- **Data Architecture**: Two independent repositories communicating through a cloud Supabase instance:
  - `protein-etl` (Python 3.11+ data pipeline & CLI)
  - `protein-web` (Next.js 14+ consumer frontend)

## Constraints

- **Tech Stack**: Next.js 14+ (App Router, TypeScript), Supabase (PostgreSQL 15, Auth, Storage), Python 3.11+ (`httpx`, `pydantic`, `supabase-py`, `rich`, `questionary`).
- **Data Integrity**: Variants are the atomic unit of truth (macros and ingredients vary by flavor/size).
- **Authentication**: Google OAuth prioritized as default CTA to eliminate Indian consumer drop-off from mandatory email verification.
- **Database Search**: `pg_trgm` extension in Supabase for fuzzy matching across brand, product, and variant names.

## Key Decisions

| Decision | Rationale | Outcome |
|---|---|---|
| Split into `protein-etl` and `protein-web` | Keeps data ingestion, validation, and curation isolated from consumer web delivery; allows Python for data wrangling and Next.js for high-performance frontend. | 🟢 Good |
| Nutrition at `product_variants` level | Different flavors and pack sizes have different ingredients, macros, and prices. The variant is the single source of truth. | 🟢 Good |
| Stored precomputed metrics | `cost_per_g_protein`, `protein_density_pct`, and `true_net_carbs_g` are stored to enable fast indexed sorting and filtering. | 🟢 Good |
| Dedicated `variant_red_flags` table | Normalizes red flags for 0-flag filtering and allows flag dictionary evolution without table schema alterations. | 🟢 Good |
| Per-Pack primary with Per-100g toggle | Matches how consumers eat while allowing standardized comparisons across varying pack weights. | 🟢 Good |
| Google OAuth primary with email fallback | Maximizes frictionless sign-in for Indian mobile web users. | 🟢 Good |
| No quick-commerce price display | Stale hyper-local prices destroy user trust; show "Check Local Price" search query links instead. | 🟢 Good |

---
*Last updated: 2026-09-09 after initial GSD extraction from implementation_plan.md*
