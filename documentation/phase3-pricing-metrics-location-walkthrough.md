# Phase 3 Walkthrough — Metric Filters, Live Amazon Prices, Location-Aware Links

Date: 2026-09-26 · Branch: `phase2ui` · Plan: [phase3-pricing-metrics-location-plan.md](phase3-pricing-metrics-location-plan.md)

## What was built

### 1. Protein-metric filters and sorts (website)
- `protein-web/src/lib/metrics.ts` — the single place metric formulas live, plus `METRIC_RANGES` (slider config + URL param names).
  - ₹ per g protein uses the **best known price** (e.g. live Amazon), falling back to MRP.
  - Protein per ₹100 = `100 ÷ ₹/g`. Calories per g protein = `calories ÷ protein` (per serving).
- `FilterPanel` has a new **Protein Metrics** section (4 sliders; the far end = "Any"). Slider changes are debounced 250 ms.
- URL params: `max_cost`, `min_p100`, `max_kcal_pg`, `min_density`, `near=1`.
- New sorts: "Protein per ₹100 — High to Low", "Calories per g Protein — Low to High". The default ₹/g sort now uses best price.
- `data.ts` refactor: `applyFilters()` is now used for **both** Supabase and seed data. Before this, with Supabase connected,
  every filter and sort except category was silently ignored. A product now matches when **one variant** passes **all** filters.

### 2. Location ("near me") without scraping
- `usePincode` hook — pincode kept in this browser's localStorage, shared live across components.
- `PincodeInput` — shown in the filter panel and on the product page.
- Product page (`RedirectButtons`):
  - Amazon: price, "checked X ago" (only for database prices), "Out of stock" when Amazon says so.
  - Blinkit / Zepto / Instamart: "Availability depends on your area" → with a pincode, "Reported in stock near you (5 yes / 1 no)".
  - After clicking a quick-commerce link: "Was it available on Zepto near 560034?" Yes / No / Skip → saved to `availability_reports`.
- Filter "Only products reported on Blinkit / Zepto / Instamart near me" uses reports from the same postal district
  (first 3 pincode digits), last 30 days, where yes > no.

### 3. Database — `supabase/migrations/005_prices_availability.sql`
- `redirect_links.external_id` (ASIN) and `redirect_links.in_stock`.
- `price_history` (public read, service-role write).
- `availability_reports` (public read + insert; pincode validated by a CHECK constraint; platform limited to quick commerce).
- `availability_summary` view (yes/no counts per variant × platform × area, last 30 days).

### 4. Price poller — `protein-etl`
- `src/pricing/amazon.py` — Amazon **Creators API** client (PA-API 5 was retired May 2026). OAuth client-credentials token,
  `getItems` in batches of 10, 1 request/second. Token/API URLs are env-overridable.
- `src/pricing/poller.py` — reads Amazon links → gets ASIN (`external_id` or from `/dp/<ASIN>` URL) → fetches offers →
  rejects >50% jumps (unless `--force`) → updates `redirect_links`, adds `price_history`, recomputes
  `best_price_inr` / `best_cost_per_g_protein` → calls the website's `/api/revalidate`.
- CLI: `python src/cli.py [--dry-run] poll-prices [--force]`.
- Schedule: `.github/workflows/poll-prices.yml` every 6 hours (+ manual "Run workflow" button).
- Tests: `protein-etl/tests/test_pricing.py` (ASIN parsing, sanity check, response parsing, best-price math, poll with a fake DB).

### 5. Fresh prices on the website
- `protein-web/src/app/api/revalidate/route.ts` — POST with `Authorization: Bearer <REVALIDATE_SECRET>` marks all pages stale;
  next visit rebuilds them. Explore/category filtering already fetches on the client, so it is always current.

## How to turn it on (blockers)
1. Create a Supabase project → run migrations `001`–`005` in order (SQL editor) → fill `protein-web/.env.local` and `protein-etl/.env`
   (see `.env.local.example` / `.env.example`) → `python scripts/seed.py` to upload products.
2. Replace placeholder Amazon links in `protein-etl/data/seed_products.json` with real `https://www.amazon.in/dp/<ASIN>` URLs.
3. Amazon Associates India → reach 10 qualifying sales in 30 days → create Creators API credentials → set `AMAZON_*` vars.
   Verify the token URL / API URL shown in Amazon's docs for your credential version; override via env if they differ.
4. Deploy the website; set `REVALIDATE_SECRET` there. Add all ETL env vars as GitHub Actions secrets
   (`REVALIDATE_URL` = `https://<site>/api/revalidate`).
5. Try `python src/cli.py --dry-run poll-prices` first.

## Verification done
- `npx tsc --noEmit` clean; eslint clean on changed files (2 pre-existing unused-variable warnings remain).
- `python -m py_compile` on new Python files. Unit tests written but not run (run `pytest` in `protein-etl`).
- Not run: the app itself, any live Supabase/Amazon calls (no credentials yet).

## Known limits / follow-ups
- Availability reports are anonymous; spam is only limited by DB constraints. Add rate limiting (API route + IP throttle) before launch.
- `protein-web/middleware.ts` is outside `src/`, so Next.js never runs it (and Next 16 renamed it to `proxy.ts`) → auth session refresh is not running.
- No browser geolocation (would need a reverse-geocoding API); pincode is typed in.
- Price history is stored but not yet charted on the product page.
