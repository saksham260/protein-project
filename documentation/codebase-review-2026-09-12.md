# Codebase Review — Protein Discovery Engine (2026-09-12)

Repo: https://github.com/saksham260/protein-project (branch `main`, head `a43bdeb`)

## Problem statement being judged against
A website/service that helps users find protein products **available near them**, with
**redirect links** and **filters** to find the best products for their needs.

## What exists today
Only Phase 1 of 4 is built (the backend data layer). No website.

| Part | Status |
|---|---|
| `supabase/migrations` — DB schema, RLS, indexes | Done |
| `protein-etl` — Python CLI to add products, compute metrics, red flags, protein tier | Done |
| Seed catalog | 15 products (dry-run JSON only) |
| Unit tests | 27 pass (`python -m pytest -q`) |
| `protein-web` (Next.js site: explore, filters, product page, redirects) | Not started |
| Auth / personalisation | Not started |
| Location / "near me" | Not planned at all |

## Rating: 4/10 against the problem statement
- Planning & data model quality: ~7.5/10 (thoughtful, well documented, good schema)
- Delivery against the brief: ~2/10 (no UI, no location, no usable filters for a user yet)

## Phase 1-only rating: 6.5/10
Judged only on what Phase 1 set out to do (schema, engines, CLI, seed); no marks lost for Phases 2–4.

| Area | Score | Notes |
|---|---|---|
| Database schema / RLS / indexes | 8/10 | Clean variant-level model, good indexes. No location/availability tables (brief needs "near me"); redirect links lack a unique key. |
| Metrics engine | 4/10 | Density and net carbs fine; ₹/g, the headline metric, is wrong for multi-serving packs. |
| Red-flag scanner | 7.5/10 | Good alias/INS dictionary; a few loose patterns. |
| Protein tier classifier | 6/10 | Sensible idea; wrong primary source in blends, harsh Tier-4 demotion. |
| ETL CLI + uploader | 6.5/10 | Nice dry-run + batch UX; duplicate links on re-upload, `last_verified_at` never updates. |
| Shopify parser | 5/10 | Wrong weight/MRP fields, no nutrition extraction. |
| Seed data | 4/10 | 15 products meets target, but fake Amazon ASINs and bad powder numbers. |
| Tests | 6/10 | 27 pass, but none caught the ₹/g bug (no multi-serving case). |
| Docs / planning | 9/10 | Excellent. |

> **Update:** bugs 1–7 and the loose red-flag patterns in 8 were fixed the same day — see [phase1-fixes-walkthrough.md](phase1-fixes-walkthrough.md). Still open: Tier-4 weakest-link rule (kept, it is in the spec) and the dual import paths.

## Bugs found
1. **₹/g protein is wrong for multi-serving packs (critical).**
   `engine/metrics.py` uses `mrp_inr / protein_g`, but `protein_g` is per serving for powders.
   - MuscleBlaze Biozyme 1kg: shows ₹139.96/g, real ≈ ₹3499 / (25 × 32) = ₹4.37/g
   - Nakpro: ₹74.96 (real ≈ ₹2.50), Cosmix: ₹86.00 (real ≈ ₹4.30), Namkeen: ₹19.90 (real ≈ ₹6.63)
   - Plantigo has `servings_per_pack: 1` for a tub — data error on top of the bug.
   Powders — the best-value category — would rank as the worst.
   Fix: divide by `protein_g × servings_per_pack` (or store nutrition per 100 g and use net weight).
2. **Fake Amazon links in seed data** — e.g. `dp/B08XYZ1234`, `dp/B08ABC5678`, `dp/B07RITE001`. Placeholder ASINs → dead redirects.
3. **Duplicate redirect links on re-upload** — `_live_upsert` always `insert`s into `redirect_links`; no delete and no unique `(variant_id, platform)`.
4. **Primary protein source wrong in blends** — ingredients inside one "Protein Blend (...)" token all share one index, so order follows tier-file order, not label order (RiteBite: Soy listed first, reports Whey Concentrate).
5. **Shopify parser maps wrong fields** — `grams` is shipping weight (not net weight) and `price` is selling price (not MRP; that is `compare_at_price`). Nutrition is not extracted at all.
6. **Ranking uses MRP, not the price users pay** — Amazon/D2C prices are stored but metrics ignore them.
7. `last_verified_at` never updates on re-upload; auth trigger fires on every login (`AFTER INSERT OR UPDATE`).
8. Minor: loose red-flag patterns (bare `"1400"`, `"glucose syrup"` also hits maltitol alias), a whole blend drops to Tier 4 for trace collagen, try/except dual import paths.

## Gaps vs the brief
- **No "near me"**: no user location, pincode, store table, or availability data. Quick-commerce links are just search URLs.
- **No website**: nothing a user can open, browse or filter.
- **Filters are only planned**: category, diet, allergen, tier, sort by ₹/g. Missing need-based filters like budget, protein per serving, sugar cap, veg/vegan/Jain, lactose-free, goal presets (muscle gain, weight loss, diabetic).
- **Tiny, manual catalog**: 15 products, all typed in by hand; no refresh or price-staleness job.
- **No affiliate tags or click tracking**, even though affiliate revenue and CTR are the stated business model.
- No product images stored, no admin UI (CLI only), no CI.

## Suggested next steps (priority order)
1. Fix ₹/g formula + powder data, add a test for a multi-serving pack.
2. Replace fake ASINs with real links; add unique `(variant_id, platform)` + upsert.
3. Build the minimum website: explore grid + filters + product page + redirect buttons.
4. Add location: pincode input → deep links to Blinkit/Zepto/Instamart with location, or an availability table per pincode/city.
5. Grow catalog (open food data / brand Shopify feeds), add a scheduled price/link-health check.
6. Add affiliate tags + click logging (`/go/[id]` redirect route).
