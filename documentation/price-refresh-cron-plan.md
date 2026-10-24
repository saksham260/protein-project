# Plan — Scheduled price refresh (cron)

Date: 2026-10-24 · Status: **Job A built and tested (193 ETL tests pass); schedule left OFF until the steps below are done. Job B unchanged.**

## Goal
Keep prices on the site fresh without anyone running a script by hand.

## Where it runs
**GitHub Actions scheduled workflow** (recommended). The Python price code already runs there, it is free for this size of job, and the secrets live in GitHub.
Alternatives considered: a Render Cron Job (works, but paid, ~$1/month minimum, and needs the Python code deployed there too); Supabase pg_cron (can't run our Python).

Things to know about GitHub schedules:
- They only fire from the **default branch** (`main`), so this branch must be merged first.
- Runs can start a few minutes late; GitHub switches schedules off after 60 days with no repo activity (any commit or a manual run resets it).
- Cost: 4 runs/day x ~3 min = ~360 min/month. Free for public repos; private repos get 2,000 free minutes/month.

## Two jobs

### Job A — Brand-store (D2C) prices (new, can be built now)
| Item | Plan |
|---|---|
| Source | Each brand's public Shopify feed: `https://<store>/products.json?limit=250` (one page of up to 250 products). ~50 stores = ~50 requests per run. |
| Frequency | Every 6 hours (`30 */6 * * *`). Brand prices rarely change faster; it can be tightened later. |
| Matching | Our variant `sku` -> the store variant `sku`. Today 358 of 371 variants match. The 13 that don't (Steadfast, Proburst, a few Phab/Pintola/Epigamia/Cosmix) fall back to matching by store and variant title, and are logged if still unmatched. |
| Writes | `redirect_links.platform_price_inr` (selling price), `in_stock`, `price_last_checked`; one `price_history` row (`platform = 'd2c'`, already allowed by the table); recompute `best_price_inr` and `best_cost_per_g_protein` on the variant. MRP is left alone, so discounts keep showing. |
| Safety | Reuse the existing >50%-jump check (`is_plausible_price`); one request per second per store with a clear User-Agent; one store failing doesn't fail the run; the run fails only if >30% of stores fail, so you get a GitHub email. Only changed prices write to history, to keep the table small. |
| Page refresh | After a run that changed prices, call `/api/revalidate` so pages update straight away instead of waiting for the 1h/24h cache. |

Files to add or change:
- `protein-etl/src/pricing/d2c.py` — fetch store feeds, match variants, build updates.
- `protein-etl/src/pricing/poller.py` — pull the shared "write price, history, recompute best price" part out of the Amazon poller so both jobs use it.
- `protein-etl/src/cli.py` — new command `poll-d2c-prices [--dry-run] [--force]`.
- `.github/workflows/poll-d2c-prices.yml` — scheduled + manual run.
- `protein-etl/tests/test_d2c.py` — matching, plausibility, unmatched fallback.
- Site: show "checked X ago" on D2C buttons too (Amazon already does).

### Job B — Amazon prices (already built, waiting on prerequisites)
Turn it on by uncommenting the `schedule:` lines in `.github/workflows/poll-prices.yml` (every 6 hours) once:
1. Amazon Associates India account is approved (10 qualifying sales in 30 days) and Creators API credentials exist.
2. Amazon links are changed from search links (`/s?k=`) to product links (`/dp/<ASIN>`). All 371 are search links today, so the job would currently update nothing.
3. Creators API token/API URLs are checked against Amazon's docs (noted in the earlier pricing plan).

### Not scheduled
Blinkit, Zepto and Instamart stay as links plus crowd availability reports (your earlier decision).

## Steps in order
1. **Merge to `main`** (schedules only run there).
2. **Database ready:** apply migrations 001-010 and upload the full catalog so `sku` and links exist in Supabase.
3. **GitHub secrets:** `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `REVALIDATE_URL` (`https://<app>.onrender.com/api/revalidate`), `REVALIDATE_SECRET` (same value set on Render).
4. **Build Job A** with a `--dry-run` first: it prints "would update N prices" without writing.
5. **Run once by hand** from the Actions tab, check `price_history` and a product page, then enable the schedule.
6. **Watch the first 24h** (4 runs), then decide whether to change the frequency.
7. When Amazon access arrives: swap in ASINs, uncomment the Job B schedule.

## Risks
- A brand changes store platform or renames a SKU: that variant is logged as unmatched and keeps its old price; the "checked X ago" label shows it going stale.
- Stores that are not Shopify (some of the 50) may not have `products.json`: skipped and listed in the run log.
- A store blocks automated requests: counts as a failed store; the 30% rule raises the alarm.

---

## Build log — Job A (2026-10-24)

### What was built
| File | What |
|---|---|
| `protein-etl/src/pricing/d2c.py` | New. Reads `https://<store>/products.json` (1 request/second, up to 6 pages of 250), matches variants (SKU, then single-variant page, then variant name), applies the safety rules, writes prices |
| `protein-etl/src/pricing/poller.py` | Shared `write_price()` and `recompute_best_prices()` pulled out of the Amazon poller (Amazon tests still pass) |
| `protein-etl/src/cli.py` | New command `poll-d2c-prices` |
| `.github/workflows/poll-d2c-prices.yml` | Manual run (dry-run ticked by default); the `schedule:` is commented out |
| `protein-etl/tests/test_d2c.py` | 13 tests: parsing, matching, dry run, price-jump guard, failed store, shared listing |
| `protein-web/src/components/product/RedirectButtons.tsx` | Product page now shows a **Brand Store** button (first) when a brand-store link exists, with "checked X ago". Before, there was no such button at all, so the "Cheapest Option" tag could never land on the brand store |

### Safety rules in the job
- A change of more than 50% is skipped unless `--force`.
- If two of our variants match the same store listing (e.g. a SKU copied between variants), both are skipped.
- Unmatched variants and unreachable stores keep their old price and are listed in the log.
- The run exits with an error (GitHub emails you) if more than 30% of stores are unreachable.
- History rows are only added when the price or stock actually changed; "checked at" is stamped on every successful match.

### How to run
```
cd protein-etl
python src/cli.py --dry-run poll-d2c-prices      # report only (note: --dry-run goes BEFORE the command)
python src/cli.py poll-d2c-prices                # live (needs SUPABASE_URL + SUPABASE_SERVICE_KEY)
```
On GitHub: Actions → "Poll brand-store prices" → Run workflow (dry run is ticked by default).

### Trial against the real stores (read-only, using the seed catalog, no database)
- 48 stores: 38 readable, 10 not (no `products.json`: Avvatar, MuscleBlaze, Fuel One, The Whole Truth, Amul, Nutrabay, Plix, Kapiva, XLR8, plus the bad `unknown.com`). Those keep their snapshot price. 10 of 48 is under the 30% alarm.
- 276 links: **250 matched (91%)**, 26 unmatched (mostly One Science Nutrition, whose store names flavours differently, plus a few others).
- 27 prices differ from the 2026-10-24 snapshot (e.g. SuperYou Chocolate 1 kg ₹2349 -> ₹2199), which shows why a scheduled refresh is worth having.

### Problems found while testing
1. **Duplicate SKUs in our catalog** (e.g. Nakpro `GOLD2P` used on two variants): would have put one variant's price on the other. Now guarded (see rules).
2. **Four products had a brand-store link on `unknown.com`** (Epigamia Greek Yogurt Drink, Yoga Bar Oats Crisps, Cosmix Plant Protein, The Whole Truth Namkeen). Removed from `seed_products.json` and `seedCatalog.json`. Still to do: remove the same links from the Supabase database if the catalog was already uploaded, and find the real product pages. `scripts/sync_picks_and_readings.py` (fallback host `unknown.com`) and `picks.txt` lines 363, 365, 368, 371 would recreate them if the demo-catalog builder is re-run.
3. **26 unmatched variants** could be improved later with a small per-brand name-mapping table.

### Still to do before turning the schedule on
1. Merge to `main`; apply migrations 001-010; upload the catalog to Supabase.
2. Add GitHub secrets: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `REVALIDATE_URL`, `REVALIDATE_SECRET`.
3. Run the workflow once manually with dry run ticked, read the log, then once live.
4. Uncomment the `schedule:` lines in `poll-d2c-prices.yml`.
