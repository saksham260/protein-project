# Phase 3 Plan — Metric Filters, Live Amazon Prices, Location-Aware Links

Date: 2026-09-26 · Branch: `phase2ui`

## Goal
1. Filter/sort by protein metrics (₹ per g protein, protein per ₹100, calories per g protein, protein density).
2. "Best near me": the user enters a pincode; quick-commerce links show crowd-sourced availability for their area, and a "Quick delivery near me" filter keeps only products reported available nearby.
3. Database stores prices (current + history) and nutrition.
4. A poller refreshes Amazon prices on a schedule (official Amazon **Creators API** — no scraping).
5. The website shows the latest prices, with "checked X ago", and refreshes pages right after each poll.

Decision (agreed): **no scraping of Blinkit / Zepto / Instamart**. We show their search links, labelled
"availability depends on your area", and ask users "Was it available?" after they click (crowd-sourced availability).

## Metric definitions (derived in the web app from stored columns — no new DB columns)
| Metric | Formula | Better |
|---|---|---|
| Cost per g protein (₹/g) | `best_cost_per_g_protein ?? cost_per_g_protein` | lower |
| Protein per ₹100 (g) | `100 / cost per g protein` | higher |
| Calories per g protein | `calories_kcal / protein_g` (per serving) | lower (4 = pure protein) |
| Protein density (%) | `protein_density_pct` (already stored) | higher |

## Work items

### A. Database — `supabase/migrations/005_prices_availability.sql`
- `redirect_links`: add `external_id` (Amazon ASIN) and `in_stock`.
- `price_history`: one row per poll per link (variant, platform, price, in_stock, source, recorded_at). Public read, service-role write.
- `availability_reports`: anonymous "was it available?" answers (variant, platform, pincode, is_available). Public insert (validated), public read.
- `availability_summary` view: yes/no counts per variant × platform × area (first 3 pincode digits = postal district), last 30 days.

### B. ETL (`protein-etl`)
- `src/pricing/amazon.py` — Creators API client: OAuth client-credentials token, `getItems` in batches of 10 ASINs, parse `offersV2.listings[0].price.money.amount` + `availability.type`.
- `src/pricing/poller.py` — load Amazon links from Supabase → fetch prices → sanity check (reject >50% jumps unless `--force`) → update `redirect_links`, insert `price_history`, recompute variant `best_price_inr` / `best_cost_per_g_protein` → call the website's `/api/revalidate`.
- CLI: `python src/cli.py poll-prices [--dry-run] [--force]`.
- `.github/workflows/poll-prices.yml` — runs every 6 hours.
- Unit tests for the pure parts (ASIN extraction, response parsing, sanity check, best-price recompute).

### C. Website (`protein-web`)
- `src/lib/metrics.ts` — metric helpers (single source of truth for the formulas above).
- `data.ts` — one shared `applyFilters()` for **both** Supabase and seed data. Fixes an existing bug: with Supabase connected, every filter/sort except category was ignored.
- New filters (URL params): `max_cost`, `min_p100`, `max_kcal_pg`, `min_density`, `near=1`. New sorts: protein per ₹100, calories per g protein.
- `FilterPanel` — "Protein Metrics" range sliders + "Quick delivery near me" toggle.
- `usePincode` hook (localStorage) + `PincodeInput` component.
- `RedirectButtons` — Amazon shows live price + "checked X ago" + stock; quick-commerce shows area reports and a "Was it available?" prompt after click.
- `src/lib/availability.ts` — read summary / submit report via Supabase (no-ops without DB).
- `src/app/api/revalidate/route.ts` — secret-protected; poller calls it to rebuild pages.

## Blockers for Parth
1. **Supabase project** — create one, run migrations 001–005, put keys in `protein-web/.env.local` and `protein-etl/.env`, run the seed upload.
2. **Amazon Associates India + Creators API** — needs **10 qualifying sales in the last 30 days** before API access. Then create Creators API credentials (client id/secret, credential version) and fill `AMAZON_*` env vars. Until then the poller runs but reports "no credentials".
3. **Real ASINs** — seed data has placeholder Amazon links; each variant needs its real `amazon.in/dp/<ASIN>` URL.
4. **Hosting + secrets** — deploy the site (e.g. Vercel), set `REVALIDATE_SECRET` there and in GitHub Actions secrets along with Supabase + Amazon keys.
5. **Verify Creators API endpoints** — token URL / API URL are env-configurable; defaults are taken from public migration notes and must be checked against the docs shown once credentials are issued.

## Out of scope (noted)
- `protein-web/middleware.ts` sits outside `src/`, so Next.js never runs it; Next 16 also renamed middleware → `proxy.ts`. Auth session refresh is therefore not running. Separate fix.
- Browser geolocation → pincode needs a paid reverse-geocoding API; manual pincode entry only for now.
