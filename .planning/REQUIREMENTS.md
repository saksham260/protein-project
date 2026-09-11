# Requirements: The Protein Discovery Engine

**Defined:** 2026-09-09
**Core Value:** Provide uncompromised, objective nutritional transparency and value-per-gram rankings so Indian consumers can make truly informed protein purchase decisions without deceptive marketing claims.

## v1 Requirements

### Database & Storage (DB)

- [x] **DB-01**: PostgreSQL schema implemented in Supabase with `brands`, `categories`, `products`, `product_variants`, `variant_red_flags`, `redirect_links`, `users`, `user_preferences`, and `user_favorites`.
- [x] **DB-02**: Row-Level Security (RLS) configured with public read on catalog tables and strict user-scoped CRUD on user profile/preference/favorite tables.
- [x] **DB-03**: Performance indexes created including GIN indexes on `allergens` and `dietary_tags`, trigram indexes on product/variant names, and B-tree indexes on `cost_per_g_protein` and `protein_density_pct`.
- [x] **DB-04**: Supabase Storage bucket created for product and variant pack images.

### Metrics & Flagging Engine (ENG)

- [x] **ENG-01**: Metric calculator calculates `cost_per_g_protein` (mrp_inr / protein_g) and handles 0/null guards.
- [x] **ENG-02**: Metric calculator calculates `protein_density_pct` ((protein_g * 4) / calories_kcal * 100) with division-by-zero protection.
- [x] **ENG-03**: Metric calculator computes `true_net_carbs_g` (total carbs - dietary fiber - polyols).
- [x] **ENG-04**: Red-flag engine matches ingredients and INS numbers against maltitol, amino spiking, hydrogenated/palm fat, and hidden sugars.
- [x] **ENG-05**: Protein tier engine classifies variant into Tiers 1-4 based on the lowest quality protein source in the blend, identifying primary protein source by ingredient deck position.

### ETL & Ingestion CLI (ETL)

- [x] **ETL-01**: Python project skeleton set up with Pydantic models for product, variant, nutrition, and flag schemas.
- [x] **ETL-02**: Shopify scraper extracts product title, pricing, variants, and weight from `/products.json`.
- [x] **ETL-03**: Interactive CLI prompts user for nutrition facts, ingredient paste, and platform redirect links.
- [x] **ETL-04**: CLI auto-runs metrics calculator, red-flag scanner, and tier classifier with formatted preview.
- [x] **ETL-05**: CLI upserts verified product data and red flags directly to Supabase via service role key.
- [x] **ETL-06**: Seed initial catalog with 10–20 real Indian protein products across RTD, bars, powders, and snacks.

### Web Application & UI (WEB)

- [ ] **WEB-01**: Next.js 14+ App Router project configured with TypeScript, Supabase client (@supabase/ssr), and environment variables.
- [ ] **WEB-02**: Custom design system and UI primitives created (Cards, Badges, Buttons, Tooltips, Efficiency Meter).
- [ ] **WEB-03**: Landing / Hero page (`/`) showcasing value prop, quick category shortcuts, and featured top-efficiency products.
- [ ] **WEB-04**: Explore page (`/explore`) with faceted sidebar filters (category, dietary tags, allergens, tier) and multi-option sort.
- [ ] **WEB-05**: Category pages (`/category/[slug]`) statically generated (SSG/ISR) for high-intent SEO ranking.
- [ ] **WEB-06**: Autocomplete and search page (`/search`) powered by Postgres trigram text search.
- [ ] **WEB-07**: Product Detail Page (`/product/[slug]`) displaying variant selector, full nutrition panel, Per-Pack / Per-100g toggle, and red-flag alerts.
- [ ] **WEB-08**: Platform redirect buttons built with conditional price display (Amazon & D2C show price; Blinkit/Zepto/Instamart show search links).

### Auth & Personalization (AUTH)

- [ ] **AUTH-01**: Supabase Auth integrated with Google OAuth one-click login and email/password fallback.
- [ ] **AUTH-02**: User preference onboarding allowing selection of daily protein target, dietary tags, avoided ingredients, and allergens.
- [ ] **AUTH-03**: Protected dashboard (`/dashboard`) showing saved favorite products and customizable preferences.
- [ ] **AUTH-04**: Rule-based recommendation engine filtering out user allergens/avoided ingredients and ranking by protein density and zero red flags.

### Launch & SEO (OPS)

- [ ] **OPS-01**: Dynamic metadata, OpenGraph cards (`/api/og`), and JSON-LD `Product` structured schema implemented.
- [ ] **OPS-02**: Dynamic XML sitemap and robots.txt auto-generated from active products and categories.
- [ ] **OPS-03**: Mobile responsiveness and tap target validation across standard phone breakpoints.
- [ ] **OPS-04**: Catalog expanded to 75–100 verified Indian protein products.

## v2 Requirements

### Scanner & Expansion

- **SCAN-01**: Mobile camera barcode / label OCR scanner for instant in-store product analysis.
- **SCAN-02**: Automated daily price tracker and deal alert notifications for saved favorites.
- **COMM-01**: User reviews and verified lab test report uploads (Trustified/Labdoor integration).
- **COMM-02**: Brand owner portal for claiming products and submitting batch COAs.

## Out of Scope

| Feature | Reason |
|---|---|
| Unattended automated web scraping | Risk of bot blocks and hallucinated nutrition; human-in-the-loop CLI ensures 100% data fidelity. |
| Stored dynamic quick-commerce prices | Blinkit/Zepto dark-store pricing varies wildly by location and time; showing outdated prices loses trust. |
| Complex ML recommendation models | Rule-based SQL filtering with Postgres array operators is fast, explainable, and zero-cost. |
| Native iOS/Android apps | Web-first responsive architecture covers mobile users with lower maintenance overhead. |

## Traceability

| Requirement | Phase | Status |
|---|---|---|
| DB-01 | Phase 1 | Complete |
| DB-02 | Phase 1 | Complete |
| DB-03 | Phase 1 | Complete |
| DB-04 | Phase 1 | Complete |
| ENG-01 | Phase 1 | Complete |
| ENG-02 | Phase 1 | Complete |
| ENG-03 | Phase 1 | Complete |
| ENG-04 | Phase 1 | Complete |
| ENG-05 | Phase 1 | Complete |
| ETL-01 | Phase 1 | Complete |
| ETL-02 | Phase 1 | Complete |
| ETL-03 | Phase 1 | Complete |
| ETL-04 | Phase 1 | Complete |
| ETL-05 | Phase 1 | Complete |
| ETL-06 | Phase 1 | Complete |
| WEB-01 | Phase 2 | Pending |
| WEB-02 | Phase 2 | Pending |
| WEB-03 | Phase 2 | Pending |
| WEB-04 | Phase 2 | Pending |
| WEB-05 | Phase 2 | Pending |
| WEB-06 | Phase 2 | Pending |
| WEB-07 | Phase 2 | Pending |
| WEB-08 | Phase 2 | Pending |
| AUTH-01 | Phase 3 | Pending |
| AUTH-02 | Phase 3 | Pending |
| AUTH-03 | Phase 3 | Pending |
| AUTH-04 | Phase 3 | Pending |
| OPS-01 | Phase 4 | Pending |
| OPS-02 | Phase 4 | Pending |
| OPS-03 | Phase 4 | Pending |
| OPS-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 30 total
- Completed: 15 / 30 (50%)
- Mapped to phases: 30
- Unmapped: 0 ✅

---
*Requirements defined: 2026-09-09*
*Last updated: 2026-09-11 after Phase 1 execution*
