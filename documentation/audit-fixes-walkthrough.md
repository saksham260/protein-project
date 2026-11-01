# Audit Fixes Walkthrough (2026-11-01)

Implements the findings in [codebase-audit-2026-11-01.md](codebase-audit-2026-11-01.md). Work is on the branch `audit-fixes`, started from `main` at `2fe3026`. Nothing is committed or pushed yet.

## What you need to do

The code can't finish these on its own.

1. **Run the tests before merging.** New and changed tests were written but not run, because the project rules say to run them only when asked.
   ```bash
   cd protein-web && npm test
   cd protein-etl && python -m pytest -q
   ```
2. **Run five migrations in the Supabase SQL editor**, in this order. All are safe to re-run.
   1. `supabase/migrations/008_variant_flags_breakfast.sql`
   2. `supabase/migrations/010_vegan_cookies.sql`
   3. `supabase/migrations/012_user_searches.sql`
   4. `supabase/migrations/014_audit_fixes.sql`
   5. `supabase/migrations/015_test_reports.sql` (from the [feature build](feature-build-walkthrough.md))

   Until then: recent searches stay broken, "Out of stock" labels can't appear, account deletion and click counting don't work, and raw pincodes stay publicly readable.
3. **Re-upload the catalog** so the out-of-stock flags reach the database. Do a dry run first, and check whether it would overwrite newer brand-store prices. The uploader now stops with a clear error if 008 or 010 hasn't been run.
4. **Set environment variables** on the host:
   - `NEXT_PUBLIC_SITE_URL`: the real site address. Without it, canonical links and the sitemap may point at `localhost`.
   - `NEXT_PUBLIC_AMAZON_AFFILIATE_TAG`: your real Associates tag. The fallback `proteineng-21` is unconfirmed, and if it isn't yours, the commission goes nowhere.
   - `NEXT_PUBLIC_CONTACT_EMAIL`: optional, shown on the privacy page.
5. **Have a lawyer read** `/privacy`, `/terms` and `/how-we-rate`. They were written to match what the code does, but they aren't legal advice.
6. **Look at the site in a browser.** It wasn't opened during this work. Check the product card and product page first, as their layouts changed.
7. **Optional:** clear the 2 test rows from `availability_reports`, both written by the old check script:
   ```sql
   DELETE FROM availability_reports WHERE pincode = '560034' AND platform = 'zepto';
   ```
   Check the rows first; a real shopper at that pincode could have the same values.

## Before and after

Measured on the production build and the live catalog (379 products, 489 variants), except allergens, which use the shipped catalog so the numbers compare with the audit.

| Measure | Before | After |
|---|---|---|
| Tree-nut variants slipping past the filter | 53 of 54 | 0 |
| Gluten variants slipping past | 34 of 69 | 0 |
| Egg variants slipping past | 2 of 2 | 0 |
| Peanut variants slipping past | 1 of 68 | 0 |
| Variants with a wrong nutrition table | 411 of 469 | 0 (by the fixed formula) |
| Biozyme 2 kg protein "per 100g" | 1.2 g | 69.4 g |
| npm audit, critical + high | 1 + 5 | 0 + 0 |
| Amazon links tagged at click time | 0 of 471 | 471 of 471 |
| Top Picks winners with red flags | 2 of 5 | 0 of 5 |
| JavaScript per page, compressed | 0.38 MB | 0.27 MB |
| JavaScript per page, uncompressed | 2.1 MB | 0.9 MB |
| Home page HTML | 2.43 MB | 0.23 MB |
| Top Picks HTML | 2.38 MB | 0.10 MB |
| Catalog downloads | Every search or filter change | Once per 10 minutes, on demand (256 KB compressed) |
| Products in `/explore` HTML | None | First 24 |
| Lint | 97 errors | 0 errors |

| Search | Before | After |
|---|---|---|
| `muscle blaze` | 0 | 12 |
| `wholetruth` | 0 | 12 |
| `chocolate whey` | 0 | 106 |
| `protien` | 0 | 336 |
| `maltitol` | 0 | 31 |
| `soy` | 4 | 108 |

## How the data flow changed

**Before:** every browser page bundled the seed catalog, and each search or filter change downloaded the full catalog from Supabase.

**After:**
- [lib/data.ts](../protein-web/src/lib/data.ts) is server-only and holds the seed. Importing it from browser code now fails the build.
- [lib/catalog.ts](../protein-web/src/lib/catalog.ts) holds the filter and sort logic, and is safe for the browser.
- [api/catalog/route.ts](../protein-web/src/app/api/catalog/route.ts) serves a trimmed catalog, cached for an hour.
- [lib/catalogClient.ts](../protein-web/src/lib/catalogClient.ts) fetches it once, keeps it for 10 minutes and filters in memory.
- Home sends 12 products and loads the rest on scroll. Explore and category pages render their first 24 products on the server for search engines.

**Failure behaviour:** the seed is now used only when no database is configured. If the database fails, the error is raised, so cached pages keep their last good version and fresh pages show an error page. A failed deploy-time read now fails the build instead of shipping old data.

## Status of each finding

### Critical

| ID | Status | Notes |
|---|---|---|
| C1 Allergen filter | Done | [allergens.ts](../protein-web/src/lib/allergens.ts) maps every label word to a group and also scans ingredients. Plain "nuts" counts as both tree nuts and peanuts. Oats count under gluten. Products with no allergen data are hidden while a filter is on. |
| C2 Nutrition table | Done | Tabs are now "Per Serving" and "Per 100g". Pack totals stay in the main metrics. |
| C3 Next.js | Done | On 16.4.3. Unused 3D and animation packages removed. 16 moderate advisories remain, all in lint tooling that never ships. |
| C4 Live database | **Needs you** | SQL is ready. The uploader now fails loudly instead of dropping fields. `setup_all.sql` includes 013 and 014. |
| C5 Claims and legal | Done, needs legal read | Claims reworded, 3 new pages, Amazon disclosure in the footer and beside buy buttons, clear-history and delete-account controls. Delete-account needs 014. |
| C6 Amazon links | Partly | Tag added at click time everywhere. **Real product links (ASINs) still need adding**, and Amazon prices can't start until they are. |

### High

| ID | Status | Notes |
|---|---|---|
| H1 Seed in browser | Done | |
| H2 Repeated downloads | Done | |
| H3 Silent fallback | Done | |
| H4 ₹/g and selling price | Done | Cards show the selling price with MRP struck through, plus ₹/g. The product page shows them above the pack picker. The existing calories and protein metrics stay. |
| H5 Search | Done | Word order, spacing, typos, ingredients, and `on`/`mb` shortcuts. Name matches rank above ingredient matches. |
| H6 Maltitol | Done | Real sweetener names shown; glycemic polyols stay in net carbs, in the web app and the ETL. 11 maltitol variants have a polyol value of 0, which is a data gap, not fixed. |
| H7 Diet tags | Done | Tags the label contradicts are dropped as data loads. Maltodextrin products keep "No Added Sugar" (a judgment call: it isn't legally a sugar). |
| H8 Availability | Code done | Summary now needs 2 yes reports. Privacy and rate limit arrive with 014. **The real gap remains: there's almost no availability data.** |
| H9 Price jobs | Partly | Best price ignores out-of-stock and quick-commerce links. Amazon rows never go into `price_history`. Amazon prices hide after 24 hours and show a time stamp. "Cheapest" needs a price under 14 days old. **Jobs are still paused**, so once brand prices pass 14 days the "Cheapest" label disappears until you run them. |
| H10 SEO and errors | Mostly | Sitemap, robots, canonical URLs, link previews, Product data, error and 404 pages. Store clicks are counted after 014. No analytics or error-monitoring tool was added, as that's a vendor choice. |

### Medium

| ID | Status | Notes |
|---|---|---|
| M1 Focus loss | Done | |
| M2 Empty-state flash | Done | |
| M3 Card vs filter | Done | Cards show the variant that matched. |
| M4 Cart | Partly | Each pack size is now its own item, and prices refresh when the cart opens. Syncing to an account isn't built. |
| M5 Cart wording | Done | Settled on "Cart", matching the buttons. |
| M6 Sign-out on network blip | Done | |
| M7 Security headers | Done | A minimal content policy, so it can't break scripts or brand images. |
| M8 Forwarded host | Done | The configured site address wins. |
| M9 `search_path` | In 014 | |
| M10 Quick-commerce prices | Done | Ignored in "Cheapest", best price and the cart. |
| M11 Accessibility | Partly | Button-inside-link fixed and cart focus handled. Small text sizes unchanged. |
| M12 Hero search history | Done | |
| M13 Filters and URL | Done | |
| M14 Hot-linked images | Not done | Needs a decision on hosting and image rights. |

### Cleanup

| Item | Status |
|---|---|
| Lint errors | Done: 0 errors, 1 warning. The two copied animation components have their own lint rules. |
| Unused packages and dead code | Done |
| CI on pull requests | Done: [ci.yml](../.github/workflows/ci.yml) runs types, lint, tests and build. It first runs on your next push. |
| `supabase/README.md` | Done |
| Duplicated Explore/Category and search bar code | Not done: a risky refactor with no visible benefit yet |
| Repo clutter (`scripts`, `scratch`) | Not done: left for you and the team to review |

## Other changes you may notice

- "Diabetic-Friendly" is gone from the filter list, because it reads as a health claim. The tag still shows on products under "Dietary Profile (As Labelled)".
- The "Verified Brand" badge is gone. Nothing defined what it meant.
- Top Picks is now "Top Value Picks", and winners changed because red-flagged products can't win.
- "Spiked" wording is now "Added Aminos", and products with no ingredient list say so instead of showing as clean.
- Search pages are blocked in `robots.txt`, to avoid thin pages in search results.

## Known limits

- **Red-flag rules are unchanged.** Ensure and Complan are still flagged for taurine, and Platinum Hydrowhey isn't flagged for L-leucine. The wording is softer, but the rule itself needs a product decision, then a re-run.
- **Rate limiting on reports is per product and district.** A determined attacker could still post across many products. Real limits need a server route.
- **Allergen filtering depends on labels.** It over-excludes on purpose, and the pages tell shoppers to check the pack.
- **The feature ideas were not built** (compare page, lab evidence panel, and so on). Only the items that overlapped with audit findings were done.
