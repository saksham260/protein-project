# Roadmap: The Protein Discovery Engine

## Overview

The Protein Discovery Engine proceeds in four logical execution phases: first establishing the Supabase schema and Python CLI ingestion pipeline to compute metrics and seed verified data; second building the high-performance Next.js 14 frontend for product exploration and comparison; third integrating Supabase Auth and the personalized recommendation engine; and fourth finalizing SEO, OpenGraph generation, responsive polish, and catalog expansion.

## Phases

- [ ] **Phase 1: Foundation & Data Ingestion Pipeline** - Supabase schema, RLS, metric computation, red-flag scanner, and interactive Python ETL CLI with initial seed.
- [ ] **Phase 2: Core Consumer Web App & Discovery** - Next.js 14 setup, UI design system, Explore grid with faceted filters, Product Detail page with Per-Pack/Per-100g toggle, and redirect links.
- [ ] **Phase 3: User Auth & Personalization Dashboard** - Google OAuth / email auth, user dietary preference onboarding, favorites management, and SQL rule-based recommendation feed.
- [ ] **Phase 4: SEO, Launch Optimization & Catalog Expansion** - Dynamic OpenGraph images, JSON-LD schema, sitemaps, mobile UX audit, and catalog expansion to 75–100 products.

---

## Phase Details

### Phase 1: Foundation & Data Ingestion Pipeline
**Goal**: Deliver a functioning Supabase database and working Python CLI tool that parses product nutrition, calculates metrics, flags questionable ingredients, classifies protein tiers, and seeds initial data.
**Depends on**: Nothing (first phase)
**Requirements**: DB-01, DB-02, DB-03, DB-04, ENG-01, ENG-02, ENG-03, ENG-04, ENG-05, ETL-01, ETL-02, ETL-03, ETL-04, ETL-05, ETL-06
**Success Criteria**:
  1. Supabase schema, RLS policies, and GIN/trigram indexes deploy without error.
  2. Test suite passes for metric formulas (₹/g, density %, net carbs) and red-flag alias detection (maltitol, aminos, palm fat, hidden sugars).
  3. Interactive Python CLI parses Shopify URLs / manual input and uploads verified products to Supabase.
  4. At least 10–20 real Indian protein products are seeded in the database.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Supabase database migration scripts (tables, RLS policies, GIN indexes, pg_trgm, storage bucket).
- [ ] 01-02: `protein-etl` engine modules (`metrics.py`, `red_flags.py`, `protein_tier.py`, alias dictionaries, unit tests).
- [ ] 01-03: `protein-etl` CLI interface, Shopify extractor, Supabase uploader, and initial 10-20 product seed.

---

### Phase 2: Core Consumer Web App & Discovery
**Goal**: Deliver a consumer-ready Next.js 14 web app allowing users to browse, search, filter, and inspect protein products with full nutritional transparency.
**Depends on**: Phase 1
**Requirements**: WEB-01, WEB-02, WEB-03, WEB-04, WEB-05, WEB-06, WEB-07, WEB-08
**Success Criteria**:
  1. User can browse products on the Explore page and filter by category, dietary tags, allergens, and protein tier.
  2. User can sort products by Cost per Gram (₹/g) ascending and Protein Density descending.
  3. User can view the Product Detail page with interactive variant switching, per-pack vs. per-100g toggle, and detailed red-flag explanations.
  4. Platform redirect buttons correctly display Amazon/D2C prices or quick-commerce local search links.
**Plans**: 3 plans

Plans:
- [ ] 02-01: Next.js 14 project setup, TypeScript configuration, `@supabase/ssr` client integration, and UI design system primitives.
- [ ] 02-02: Explore grid page, faceted filter sidebar, and fuzzy search integration with Supabase.
- [ ] 02-03: Product Detail page (`/product/[slug]`), NutritionPanel component with per-pack/per-100g toggle, red-flag badge list, and redirect link generators.

---

### Phase 3: User Auth & Personalization Dashboard
**Goal**: Enable user authentication, preference management, and personalized product recommendations based on individual dietary constraints and goals.
**Depends on**: Phase 2
**Requirements**: AUTH-01, AUTH-02, AUTH-03, AUTH-04
**Success Criteria**:
  1. User can sign in with Google OAuth (one-click) or email/password fallback.
  2. User can set daily protein targets, select dietary preferences (e.g. vegan, keto), and specify allergens or avoided ingredients.
  3. Recommendation feed displays products strictly excluding user allergens and avoided ingredients, sorted by protein density and zero red flags.
  4. User can save favorite products and manage them in `/dashboard`.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Supabase Auth integration (Google OAuth, callback routes, session middleware, login/signup UI).
- [ ] 03-02: User preferences form, favorites CRUD operations, and rule-based SQL recommendation engine.

---

### Phase 4: SEO, Launch Optimization & Catalog Expansion
**Goal**: Maximize search engine discoverability, ensure smooth mobile responsiveness, and expand catalog depth for launch readiness.
**Depends on**: Phase 3
**Requirements**: OPS-01, OPS-02, OPS-03, OPS-04
**Success Criteria**:
  1. Dynamic OpenGraph images render correctly on `/api/og` for product social sharing.
  2. JSON-LD structured data and dynamic sitemap.xml pass Google Rich Results validation.
  3. Mobile audit confirms touch targets, layout fluidity, and clean navigation on mobile viewports.
  4. Product catalog expanded to 75–100 verified Indian protein products.
**Plans**: 2 plans

Plans:
- [ ] 04-01: SEO meta tags, dynamic `/api/og` social cards, JSON-LD Product schema, and automated XML sitemap generation.
- [ ] 04-02: Mobile UX refinements, final audit, and catalog expansion to 75–100 products via the ETL CLI.

---

## Progress

**Execution Order:**
Phases execute in numeric order: 1 ➔ 2 ➔ 3 ➔ 4

| Phase | Plans Complete | Status | Completed |
|---|---|---|---|
| 1. Foundation & Data Ingestion Pipeline | 0/3 | Not started | - |
| 2. Core Consumer Web App & Discovery | 0/3 | Not started | - |
| 3. User Auth & Personalization Dashboard | 0/2 | Not started | - |
| 4. SEO, Launch Optimization & Catalog Expansion | 0/2 | Not started | - |
