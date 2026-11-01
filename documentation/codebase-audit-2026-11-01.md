# Codebase Audit (2026-11-01)

**Audited:** `main` at commit `2fe3026`. `round2` is 13 commits behind `main` and has nothing of its own, so `main` is the newest code.

**Companion document:** [feature-research-2026-11-01.md](feature-research-2026-11-01.md)

**Status:** fixes are on the `audit-fixes` branch. See [audit-fixes-walkthrough.md](audit-fixes-walkthrough.md) for what is done and what still needs you.

## How this was checked

- Read the web app, database migrations and the ETL (data pipeline) pricing code.
- Ran the type check, lint, `npm audit` and a production build.
- Measured the shipped catalog with read-only scripts: 378 products, 469 variants (pack sizes or flavours).
- Ran read-only queries against the Supabase project in `protein-web/.env.local`, using the public key: 379 products, 489 variants.

**Assumption:** that Supabase project is production. If it isn't, re-check C4.

**Not done:**
- Test suites were not run. Repo and user rules say to run them only when asked.
- The app was not opened in a browser, and the deployed site was not visited (its URL is not in the repo).
- The Python code was not type-checked.
- Label accuracy was not checked against real packs. "Correct" below means the catalog agrees with itself.

## Summary

The foundations are better than the product on top of them. The catalog maths is correct, and database security for user data is sound. The serious problems are at the points where the site makes a promise to a shopper:

- A safety filter that doesn't filter.
- A nutrition table that is wrong on most products.
- Claims that the code doesn't back up.
- A revenue link that isn't connected.

| ID | Problem | Effort |
|---|---|---|
| C1 | Allergen filter lets allergens through (53 of 54 tree-nut variants) | S |
| C2 | Nutrition table wrong on 411 of 469 variants | S |
| C3 | Next.js version has critical security advisories | S |
| C4 | Live database is missing migrations 008, 010 and 012 | S |
| C5 | Trust claims the code doesn't support, and no legal pages | S to M |
| C6 | Amazon links earn nothing and can't be priced (0 of 471 tagged) | M |

Effort: S = up to 2 days, M = up to 2 weeks, L = longer.

---

## Critical

### C1. Allergen filter lets allergens through

This is a health-safety bug, and the most important item here.

**Measured on the shipped catalog:**

| "Exclude" option | Variants removed today | Should remove | Slip through |
|---|---|---|---|
| Tree Nuts | 1 | 54 | **53** (about 50 products) |
| Gluten / Wheat | 35 | 69 | **34** (16 wheat or barley, 18 oats only) |
| Eggs | 0 | 2 | **2** |
| Peanuts | 67 | 68 | 1 |
| Milk | 319 | 319 | 0 |
| Soy | 159 | 159 | 0 |

**Cause:** the filter does an exact text match, but allergens are free text in the data. The filter looks for `tree_nuts`, while the data says `nuts`, `almonds`, `tree nuts`, `cashews` and so on. It looks for `eggs`, while the data says `egg`. The live database has the same mix of words.

**Also:**
- 4 variants have no allergens and no ingredient list. They show "None declared" and pass every exclude filter.
- Open Secret cookies list peanuts in the ingredients but declare only `nuts`.
- Oats are arguably not gluten. That is a product decision, but 16 wheat or barley variants are plainly wrong.

**Where:** [data.ts:336-339](../protein-web/src/lib/data.ts#L336-L339), [constants.ts:124-131](../protein-web/src/lib/constants.ts#L124-L131)

**Fix:**
1. Clean allergens to one fixed word list when data is loaded, and repair existing rows.
2. Treat "no allergen data" as unknown, not safe. Show "Allergen info missing" and exclude those items when an allergen filter is on.
3. Add a test per filter option.
4. Add a line telling people with allergies to check the pack.

### C2. Nutrition table wrong on 411 of 469 variants

Stored values are per serving, but the table treats them as whole-pack values.

**Example, MuscleBlaze Biozyme Performance Whey 2 kg:**

| Shown as | Displayed | Real value |
|---|---|---|
| "Per 100g" protein | 1.2 g | 69.4 g |
| "Per 100g" energy | 7.2 kcal | 400 kcal |
| "Per Pack" protein (badge "Single Pack") | 25 g | 1,389 g (25 g is one serving) |

The "Per Pack" tab is the default view.

**Where:** [NutritionPanel.tsx:13-17](../protein-web/src/components/product/NutritionPanel.tsx#L13-L17) divides by `net_weight_g`. Labels are in [NutritionToggle.tsx:36](../protein-web/src/components/product/NutritionToggle.tsx#L36) and [NutritionPanel.tsx:36](../protein-web/src/components/product/NutritionPanel.tsx#L36).

**Fix:** divide by `serving_size_g` for per-100g. Offer "Per serving" and "Per 100g", and either multiply up or remove "Per Pack". `computePer100g` itself is correct, so its unit test passes; the fault is how it is called, and no component test covers that.

### C3. Next.js has critical security advisories

`next` 16.3.5 has 11 advisories, 3 of them critical. `npm audit` reports 22 affected packages: 1 critical, 5 high and 16 moderate.

- Two critical remote-code-execution issues need `next/og` or `use cache`. This code uses neither.
- The third involves the image optimizer and SVG files. The catalog has no SVG links and uses a custom image loader, but I did not confirm the `/_next/image` route is unreachable.
- The cache-poisoning advisories for self-hosted sites do look relevant, because the site runs its own server on Render.

**Fix:** upgrade `next` and `eslint-config-next` to 16.4.3, then run `npm audit fix` for `vite`, `sharp` and others. The app-side change should be small. Do this first.

### C4. Live database is missing migrations

| Migration | Missing from live | Effect |
|---|---|---|
| 008 | `product_variants.is_combo`, `is_available` | 53 out-of-stock variants (44 products) show as in stock. The "Out of stock" label can never appear. |
| 010 | `products.is_vegan` | No visible harm today: all 84 vegan products also carry a vegan tag. |
| 012 | `user_searches` table | **Recent searches can't save or load.** The site hides the error. |

**Why nobody noticed:**
- The uploader catches the error and silently drops those fields: [supabase_client.py:255-257](../protein-etl/src/db/supabase_client.py#L255-L257).
- The uploader creates missing categories itself, so the category lists from these migrations look applied even though the columns aren't.
- The web app's reads and writes fail quietly.

**Related:**
- [setup_all.sql](../supabase/setup_all.sql) stops at 012 and leaves out 013.
- [supabase/README.md](../supabase/README.md) still describes 001-007 and 15 products.
- Nothing records which migrations have run.

**Fix:** run 008, 010 and 012, re-upload so the flags land, add 013 to `setup_all.sql`, and make the uploader fail loudly on a missing column.

### C5. Trust claims the code doesn't support, and no legal pages

The product's whole pitch is honesty, so these do more damage here than on an ordinary shop. They also carry real exposure. Have a lawyer review the final wording.

| Claim shown | What is actually true | Where |
|---|---|---|
| "Hand-verified" | Winner is picked automatically by lowest ₹/g | [top-picks/page.tsx:7](../protein-web/src/app/top-picks/page.tsx#L7), [TopPicksClient.tsx:45](../protein-web/src/app/top-picks/TopPicksClient.tsx#L45) |
| "Strict chemical deck audit passed" | 2 of 5 winners have red flags (maltitol alert on the RTD drink, hidden sugars on the snack) | [TopPicksClient.tsx:64](../protein-web/src/app/top-picks/TopPicksClient.tsx#L64) |
| "Gold & Tier-1 Winners" | None of the 5 winners is Tier 1 | [TopPicksClient.tsx:61](../protein-web/src/app/top-picks/TopPicksClient.tsx#L61) |
| "Zero brand bias" | Default "Featured" order ranks a hard-coded list of big brands first | [ranking.ts:26-69](../protein-web/src/lib/ranking.ts#L26-L69) |
| "Verified Partners" | No partnerships; quick-commerce and Amazon links are just search pages | [RedirectButtons.tsx:137](../protein-web/src/components/product/RedirectButtons.tsx#L137) |
| "Verified FSSAI lab labels" | Data comes from brand sites and label photos, not FSSAI or a lab | [ProductDetail.tsx:304](../protein-web/src/components/product/ProductDetail.tsx#L304) |
| "✓ Pure Formulation (Clean)" | Shown when no spiking was found on the label, including 11 variants with **no ingredient list at all** | [ProductDetail.tsx:358](../protein-web/src/components/product/ProductDetail.tsx#L358) |
| "100% Mathematically Audited" | No audit process exists beyond the formulas | [Footer.tsx:28](../protein-web/src/components/layout/Footer.tsx#L28) |

**"Spiked" is applied inconsistently, which is a risk with brands:**
- 8 variants are flagged for amino spiking from label text. Ensure and Complan are among them, flagged for taurine, and get the "Tier 4: Incomplete / Spiked" badge.
- Optimum Nutrition Platinum Hydrowhey lists L-leucine and One Science Nitra Whey lists creatine, yet both show "Pure Formulation (Clean)".
- A label can't prove spiking. "Contains added amino acids (from label)" is a safer description.

**Missing altogether:**
- No privacy policy or terms page, although the site tracks signed-in users' views and clicks. Google sign-in is also in use.
- No affiliate disclosure. Amazon's agreement (section 10) requires a clear "As an Amazon Associate I earn from qualifying purchases."
- No way for users to clear their history or delete their account.
- The "Zero Red Flags" filter also passes those 11 variants with no ingredient data.

### C6. Amazon links earn nothing and can't be priced

**Measured on live data:** 471 Amazon links; **0 have an affiliate tag**, **0 are product pages** (all are search pages), and **0 have a price**.

**Causes:**
- Tagging only happens in `buildRedirectUrl`, and that is skipped whenever a stored link exists, which is every time: [RedirectButtons.tsx:97-99](../protein-web/src/components/product/RedirectButtons.tsx#L97-L99). The cart drawer also uses raw links: [CartDrawer.tsx:205](../protein-web/src/components/cart/CartDrawer.tsx#L205), [223](../protein-web/src/components/cart/CartDrawer.tsx#L223).
- The Amazon price poller needs a product ID (ASIN). Search links have none, so it would skip all 471: [poller.py:83-89](../protein-etl/src/pricing/poller.py#L83-L89).
- `NEXT_PUBLIC_AMAZON_AFFILIATE_TAG` isn't in `.env.local.example` or the local `.env.local`, so the code falls back to `proteineng-21`. Confirm that tag is really yours.

**Fix:** apply the tag at click time for every Amazon link, including the cart. Then add real ASINs, starting with the top sellers.

---

## High

### H1. Whole seed catalog ships to every visitor

`Navbar` → `NavbarSearch` → `useSearch` → `data.ts` → `seedCatalog.json`, so the 1.26 MB catalog file loads on **every page**, even though the live site doesn't normally use it.

| Page | HTML | JavaScript |
|---|---|---|
| Home | 2.43 MB (303 KB compressed) | 2.2 MB (0.41 MB compressed) |
| Top Picks | 2.38 MB (300 KB compressed) | 2.1 MB (0.38 MB compressed) |
| Any other page | Small | About 2.1 MB (0.38 MB compressed) |

Top Picks is especially wasteful: it sends the whole catalog to the browser and shows 5 products. The `allProducts` prop is never used: [top-picks/page.tsx:18](../protein-web/src/app/top-picks/page.tsx#L18), [TopPicksClient.tsx:19](../protein-web/src/app/top-picks/TopPicksClient.tsx#L19).

**Fix:** move catalog loading to the server only (API route or server action), and send cards a small summary, not full ingredient lists. Keep the seed out of browser code.

### H2. Each search or filter change downloads the full catalog

One call takes 2.22 MB (before compression) and about 2.1 seconds in one test. It runs on every search pause (250 ms after typing stops) and every filter change, with no caching. Category pages also refetch on load the data the server just sent: [CategoryClient.tsx:56-74](../protein-web/src/app/category/[slug]/CategoryClient.tsx#L56-L74). Sliders do already wait before applying, so that part is fine.

This is slow on mobile and uses up Supabase bandwidth: about 2,300 filter changes is 5 GB before compression.

**Fix:** fetch once and filter in memory, or use a server search endpoint with caching.

### H3. Silent fallback to old data

If Supabase fails or returns nothing, the site quietly shows the seed catalog: [data.ts:279-294](../protein-web/src/lib/data.ts#L279-L294).

- A brief outage can be cached on Home for up to 24 hours.
- Seed prices get today's date ([data.ts:214](../protein-web/src/lib/data.ts#L214)), so they can display "checked just now". The guard at [RedirectButtons.tsx:36](../protein-web/src/components/product/RedirectButtons.tsx#L36) only checks that Supabase keys exist.
- Seed product IDs aren't database IDs, so activity logging and availability reports fail while the fallback is active.
- A product removed from the live catalog stays reachable by URL via the seed: [data.ts:427-442](../protein-web/src/lib/data.ts#L427-L442).
- Seed and live already differ: 378 vs 379 products, 469 vs 489 variants, 53 vs 0 out-of-stock.

**Fix:** in production, show a clear error or a labelled "may be out of date" state. Never fake a check time. Use the seed for local demos only.

### H4. The headline number and the real price are hidden

The site's pitch is true cost per gram, and it sorts by it, but ₹/g isn't shown on product cards or in the product page's main metrics. `costPerG` is computed and never used ([ProductDetail.tsx:49](../protein-web/src/components/product/ProductDetail.tsx#L49)), and `EfficiencyMeter` is used nowhere. Shoppers see the order but not the reason.

Cards and the page's main metrics also show MRP (printed price), though 307 of 469 variants have a lower selling price. The search dropdown's ₹/g is also based on MRP: [SearchBar.tsx:203](../protein-web/src/components/search/SearchBar.tsx#L203).

The removal dates back to commit `9113c6a`, and no reason is recorded. It may have been deliberate, so this needs a decision.

### H5. Search misses obvious queries

Search is one plain text match on name, brand and variant name, so word order, spacing and spelling all break it.

| Query | Results today | Possible |
|---|---|---|
| `muscle blaze` | 0 | 12 |
| `chocolate whey` | 0 | 55 |
| `isolate whey` | 0 | 25 |
| `protien` | 0 | Everything |
| `maltitol` | 0 | 31 with it in ingredients |
| `soy` | 4 | 108 with it in ingredients |

The search box itself promises "products, brands, or ingredients": [SearchBar.tsx:21](../protein-web/src/components/search/SearchBar.tsx#L21). The database already has fuzzy-search (trigram) indexes that nothing uses: [003_indexes.sql:62-69](../supabase/migrations/003_indexes.sql#L62-L69).

**Fix:** match word by word, add ingredients and protein source, and add typo tolerance.

### H6. Maltitol shown as "Erythritol", and subtracted from net carbs

Of 24 variants with polyol values, 23 list non-erythritol sweeteners such as maltitol. The panel labels them all "Non-Glycemic Polyols (Erythritol)": [NutritionPanel.tsx:116](../protein-web/src/components/product/NutritionPanel.tsx#L116).

"True Net Carbs" subtracts them too: [metrics.py](../protein-etl/src/engine/metrics.py). But maltitol does raise blood sugar, which is why the site flags it. So the site warns about maltitol and also hides its carbs, which matters most to diabetic shoppers.

Handling is also uneven: of 33 variants with maltitol, 11 have a polyol value of 0.

**Fix:** store polyol type, subtract only truly non-glycemic ones, and show the real name.

### H7. Diet tags are too generous

- **"No Added Sugar":** on 362 of 469 variants (77%). 8 products have sugar-type ingredients such as jaggery, honey, date syrup, coconut sugar or brown rice syrup, and 2 of those show added sugar on their own label data. Another 13 contain maltodextrin.
- **Tag merging:** `no-refined-sugar` is turned into `no-added-sugar`, but jaggery and coconut sugar are added sugars: [utils.ts:261](../protein-web/src/lib/utils.ts#L261).
- **Same logic, no rows affected yet:** `dairy-free` becomes `vegan` ([utils.ts:269](../protein-web/src/lib/utils.ts#L269)) and `peanut-free` becomes `nut-free` ([utils.ts:267](../protein-web/src/lib/utils.ts#L267)). Dairy-free egg protein isn't vegan, and peanut-free isn't free of tree nuts.
- **Vegetarian conflict:** 2 products list egg and are tagged Vegetarian (Optimum Nutrition Serious Mass, Labrada Muscle Mass Gainer). In India that matters; check both.

### H8. "Near me" is effectively empty and open to abuse

"Available near you" is the core of the original brief, and it has almost no data.

- Only 2 reports exist in the whole database. Both are `zepto / available`, which is exactly what [check-supabase.mjs:120-127](../protein-web/scripts/check-supabase.mjs#L120-L127) writes on each run, so there may be **no real reports at all**.
- Anyone with the public key can post unlimited reports, and one vote can flip the result: [005_prices_availability.sql](../supabase/migrations/005_prices_availability.sql), [availability.ts:40-42](../protein-web/src/lib/availability.ts#L40-L42).
- Raw reports are publicly readable with the full 6-digit pincode (confirmed with a read). The design promised grouping by 3-digit district.

**Fix:** make reports readable only through the summary, add rate limits, require more than one report, and stop the check script writing to production. The bigger question of how to fill this data is in the feature research.

### H9. Prices aren't refreshing

- Both price jobs are paused (schedules commented out): [poll-prices.yml](../.github/workflows/poll-prices.yml), [poll-d2c-prices.yml](../.github/workflows/poll-d2c-prices.yml).
- `price_history` has 0 rows.
- The oldest brand-store price check is from 2026-10-13.
- "Cheapest Option" has no age limit, so an old price can still win it.
- Best price can come from an out-of-stock listing, because [poller.py:158-162](../protein-etl/src/pricing/poller.py#L158-L162) doesn't filter on stock, while the page does.

**Before turning polling on, see the Amazon rules in the feature research:** the poller stores Amazon prices forever in `price_history`, which conflicts with Amazon's 24-hour rule. No Amazon rows exist yet, so nothing is in breach today.

### H10. Basic SEO and error handling are missing

- No `sitemap`, `robots`, structured data (Product tags for Google), Open Graph tags (link previews), canonical URLs or `metadataBase`.
- `/explore` and `/search` contain no products in their HTML, so search engines may not see them.
- No `error.tsx`, `not-found.tsx` or `loading.tsx`, so crashes show the default page.
- A product with no variants would crash [ProductDetail.tsx:315](../protein-web/src/components/product/ProductDetail.tsx#L315). None exists today.
- No analytics or error monitoring. Clicks to stores are only logged for signed-in users, so you can't measure the main thing the site does.

---

## Medium

| ID | Problem | Where |
|---|---|---|
| M1 | **Search box loses focus.** `resetMobileZoom` blurs the active element before its mobile check, on desktop too. This cancels `autoFocus` on `/search` and can interrupt typing when results load. | [utils.ts:104-106](../protein-web/src/lib/utils.ts#L104-L106), [SearchClient.tsx:23](../protein-web/src/app/search/SearchClient.tsx#L23) |
| M2 | `/search` briefly shows "No matching products" before loading starts. | [SearchClient.tsx:19](../protein-web/src/app/search/SearchClient.tsx#L19) |
| M3 | **Filter and card disagree.** A product stays because some variant matched, but the card shows the default variant, which may not match. Sort position has the same issue. | [data.ts:408-411](../protein-web/src/lib/data.ts#L408-L411) |
| M4 | **Cart limits.** One variant per product, and it stores a full product copy in the browser, so prices and links go stale. `syncToAccount` is a stub, and `user_favorites` is unused. | [CartContext.tsx](../protein-web/src/context/CartContext.tsx) |
| M5 | Cart wording mixes "Add to Cart" and "Shortlist". The empty state mentions a "bookmark" and "compare" that don't exist. | [CartDrawer.tsx:105](../protein-web/src/components/cart/CartDrawer.tsx#L105) |
| M6 | A brief network failure on the session check can show a signed-in user as signed out. | [AuthContext.tsx:33-36](../protein-web/src/context/AuthContext.tsx#L33-L36) |
| M7 | No security headers (CSP, HSTS, frame protection). | [next.config.ts](../protein-web/next.config.ts) |
| M8 | Login redirect trusts `x-forwarded-host`. Low risk if the host overwrites it, but a fixed site URL is safer. | [auth.ts:14-18](../protein-web/src/lib/auth.ts#L14-L18) |
| M9 | `handle_new_user` runs with raised privileges and has no fixed `search_path`. | [002_rls.sql](../supabase/migrations/002_rls.sql) |
| M10 | 3 quick-commerce links hold a stored price, against the "no quick-commerce prices" decision, and they feed best-price and "Cheapest". | Live data, [RedirectButtons.tsx:86-88](../protein-web/src/components/product/RedirectButtons.tsx#L86-L88) |
| M11 | Accessibility: a button inside a link on every card, cart drawer without focus handling, 9-10 px text. | [ProductCard.tsx:78-118](../protein-web/src/components/product/ProductCard.tsx#L78-L118), [CartDrawer.tsx](../protein-web/src/components/cart/CartDrawer.tsx) |
| M12 | Hero `SearchBar` doesn't save recent searches; only the navbar one does. | [SearchBar.tsx](../protein-web/src/components/search/SearchBar.tsx) |
| M13 | Filters read the URL only on load or back/forward, so a link to `/explore` from `/explore` can leave old filters on. | [useFilters.ts:46-58](../protein-web/src/hooks/useFilters.ts#L46-L58) |
| M14 | Product images are hot-linked from many brand sites, so they can break or be blocked without warning. | [imageLoader.ts](../protein-web/src/lib/imageLoader.ts) |

## Low and cleanup

- **Lint:** 97 errors and 20 warnings, mostly in copied animation components (`ArrowRevealButton`, `VolumetricText`, `ExploreAllCard`). `next build` doesn't fail on them, so they build up unseen.
- **Unused packages:** `three`, `@react-three/fiber`, `shadergradient`, `@shadergradient/react`, `camera-controls` and `three-stdlib` are only reachable through `BackgroundShader`, which nothing uses.
- **Dead code:** `EfficiencyMeter`, `isPending` (always false), `SORT_OPTIONS.column`, `displayMonth`.
- **No CI:** the only workflows are the two paused price jobs, so no tests, type check or lint run on pull requests. All 11 test files are for library code; components have none.
- **Duplicated code:** `ExploreClient` and `CategoryClient`, `SearchBar` and `NavbarSearch`. Two colour palettes are hard-coded across them.
- **Large file:** `Navbar.tsx` is 857 lines.
- **Repo clutter:** 133 files in `protein-etl/scripts` and 93 in `protein-etl/scratch` are tracked, mostly one-off scripts and data dumps.
- **Docs:** `AGENTS.md`, `GEMINI.md` and `.agents/rules/` are copies of each other. `supabase/README.md` links to another machine's paths.

---

## Product gaps

These are missing rather than broken. The feature research covers them in detail.

- Nothing compares products side by side, though the cart text promises it.
- There is no lab evidence. Tiers and "spiking" come from label text only, and can't show what is really in a tub.
- There are no brand pages or buying guides.
- There is no way to edit the catalog except scripts. Every data fix means a developer.

---

## What is solid

- **Catalog maths:** all 469 variants' ₹/g in the seed file match a fresh calculation within 5%. No impossible values were found there (protein above serving size, calories far from macros, density out of range).
  - **Correction:** this check covered the seed file only. The live database has 6 variants with an MRP below the brand's own store price, which can't be right. See [feature-build-walkthrough.md](feature-build-walkthrough.md).
- **Links:** no malformed URLs, and all 469 brand-store links go to product pages.
- **User data security:** row-level rules limit each user to their own rows. The `users` table has no role column to abuse.
- **Secrets:** a pattern scan of tracked files found no real keys, and `.env` files are ignored.
- **Safe endpoints:** the `next` redirect check and the `/api/revalidate` secret check are both done properly.
- **Brand-store poller:** sensible safeguards (rejects jumps over 50%, skips shared listings, reports failed stores).
- **Build:** type check and production build both pass.

## Checked and ruled out

These looked like bugs but aren't:

- **Near-me query size:** sending all 489 IDs works (HTTP 200). It only trips Node's default header limit, and this query runs in the browser.
- **Slider spam:** sliders already wait before applying.
- **Vegan mislabelling:** the first scan's hits were plant milks and peanut butter. One item remains worth a look: SuperYou Strawberry's flavouring text says "Cream Plus".

---

## Suggested order

**Now (days):**
1. C3: upgrade Next.js.
2. C1: fix the allergen filter.
3. C2: fix the nutrition table.
4. C4: apply the missing migrations.
5. C5: remove unsupported claims, add disclosure and legal pages.
6. C6: tag Amazon links at click time.

**Next (weeks):**
7. H1 and H2: move catalog loading to the server.
8. H3: remove the silent fallback.
9. H4: decide on showing ₹/g and selling price.
10. H5: improve search.
11. H6 and H7: clean sugar, polyol and diet data.
12. H8: close the availability table.

**Then:**
13. H10: SEO, error pages, analytics.
14. CI on pull requests, with tests for C1 and C2.
15. H9: restart price jobs under the Amazon rules.
16. Medium items and cleanup.
