# Phase 2: Core Consumer Web App & Discovery - Context

**Gathered:** 2026-09-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 delivers the consumer-facing Next.js 14 web application for The Protein Discovery Engine:
1. Next.js 14 App Router project with TypeScript, `@supabase/ssr` client integration, and environment variables.
2. Custom design system with UI primitives (Cards, Badges, Buttons, Tooltips, Efficiency Meter) using a premium dark-mode aesthetic.
3. Landing / Hero page (`/`) with value proposition, category shortcuts, and featured top-efficiency products.
4. Explore page (`/explore`) with faceted sidebar filters (category, dietary tags, allergens, protein tier) and multi-option sort (₹/g ascending, protein density descending).
5. Category pages (`/category/[slug]`) statically generated (SSG/ISR) for high-intent SEO.
6. Autocomplete and search page (`/search`) powered by Postgres trigram text search.
7. Product Detail Page (`/product/[slug]`) with variant selector, full nutrition panel, Per-Pack / Per-100g toggle, red-flag alerts, and protein tier badge.
8. Platform redirect buttons with conditional price display (Amazon & D2C show stored price; Blinkit/Zepto/Instamart show "Check Local Price →").

</domain>

<decisions>
## Implementation Decisions

### Project Setup & Architecture
- **D-01:** Initialize Next.js 14+ project with App Router inside `protein-web/` directory at the workspace root. Use `npx create-next-app@latest` with TypeScript, ESLint, Tailwind CSS disabled (vanilla CSS), and `src/` directory enabled — **Reversibility:** reversible.
- **D-02:** Use `@supabase/ssr` for server-side and client-side Supabase client creation, following the official SSR pattern with cookies-based session management — **Reversibility:** reversible.
- **D-03:** Environment variables: `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env.local` — **Reversibility:** reversible.

### Design System & Aesthetics
- **D-04:** Build a premium dark-mode design system with vibrant accent colors, glassmorphism effects, smooth micro-animations, and Inter/Outfit typography from Google Fonts. CSS variables for all design tokens — **Reversibility:** reversible.
- **D-05:** Components follow the architecture spec: `components/ui/` for primitives, `components/product/` for product-specific, `components/search/` for discovery, `components/layout/` for chrome — **Reversibility:** reversible.

### Data Fetching Strategy
- **D-06:** Landing page (`/`): SSG with `revalidate: 86400` (24h). Explore page (`/explore`): SSR initial load + client-side Supabase queries for filters/sort. Product Detail (`/product/[slug]`): SSG with ISR `revalidate: 3600` (1h). Category (`/category/[slug]`): SSG with ISR. Search (`/search`): SSR — **Reversibility:** reversible.
- **D-07:** Nutrition toggle (Per-Pack vs Per-100g) is computed client-side: `(nutrient_value / net_weight_g) * 100` — **Reversibility:** reversible.

### Redirect & Purchase Links
- **D-08:** Amazon and D2C redirect buttons display the stored `platform_price_inr`. Quick-commerce platforms (Blinkit, Zepto, Instamart) display "Check Local Price →" with no stored price. All redirect clicks go through an internal click-tracking mechanism — **Reversibility:** reversible.

### Agent Discretion
- Specific animation timings, color values, and micro-interaction details.
- Internal component composition within the specified architecture boundaries.
- CSS class naming conventions.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Architecture & Specs
- [implementation_plan.md](file:///c:/Users/Saksham/Documents/new-project/implementation_plan.md) — Section 6 (Next.js Frontend), Section 6.3 (Redirect URL Builder), Section 6.4 (SEO Strategy).
- [.planning/REQUIREMENTS.md](file:///c:/Users/Saksham/Documents/new-project/.planning/REQUIREMENTS.md) — Scope contracts WEB-01 to WEB-08.
- [.planning/PROJECT.md](file:///c:/Users/Saksham/Documents/new-project/.planning/PROJECT.md) — Overarching vision and locked decisions.

### Phase 1 Deliverables (Dependencies)
- [supabase/migrations/001_schema.sql](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/001_schema.sql) — Full database schema with column names and types.
- [protein-etl/src/models.py](file:///c:/Users/Saksham/Documents/new-project/protein-etl/src/models.py) — Pydantic models to mirror as TypeScript types.
- [protein-etl/data/seed_products.json](file:///c:/Users/Saksham/Documents/new-project/protein-etl/data/seed_products.json) — 15 seeded products for frontend development.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Supabase PostgreSQL schema with 9 tables, RLS policies, and GIN/trigram indexes (Phase 1).
- 15 seed products across 4 categories with computed metrics, red flags, and tier classifications.
- Redirect link entries with platform-specific URLs (Amazon, Blinkit, Zepto, D2C).

### Established Patterns
- Product → Variant hierarchy with nutrition on variants.
- Pre-computed stored metrics: `cost_per_g_protein`, `protein_density_pct`, `true_net_carbs_g`.
- Red flags in separate `variant_red_flags` table with severity levels.
- Redirect links in `redirect_links` table with platform CHECK constraint.

### Integration Points
- Supabase client (anon key) for public catalog reads via `@supabase/ssr`.
- Trigram search via `pg_trgm` indexes on `products.name`, `product_variants.variant_name`, `brands.name`.
- GIN array indexes on `allergens` and `dietary_tags` for fast filter queries.

</code_context>

<deferred>
## Deferred Ideas

- Auth integration (Google OAuth, user sessions) → Phase 3.
- User dashboard, favorites, preferences → Phase 3.
- SEO metadata, OG images, sitemaps → Phase 4.
- Catalog expansion to 75-100 products → Phase 4.

</deferred>

---

*Phase: 2-Core Consumer Web App & Discovery*
*Context gathered: 2026-09-12*
