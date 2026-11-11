# Data incident: 2026-11-02/03 batch uploads — findings and fixes

Checked 2026-11-09 against commits `98b4686` (378 products), `43a7ce2` (488) and `4313cab` (476, current `main`).
Live Supabase was **not** queried: no credentials on this machine. Live counts below come from the report.

## 1. Products removed from the catalog (confirmed, worse than the log says)

`4313cab` removed **150** products and added 139. **Every one of the 150 had no image.** The log says only
duplicates and made-up items were removed, but the removals line up with "missing image", not "duplicate/fake".

| Group | Count | What it means |
|---|---|---|
| Existed before the waves (in the 378-product catalog) | **46** | Real products with real D2C prices. Likely wrongly deleted. Includes all of Ensure, PediaSure, Horlicks, Complan, Myprotein, MuscleTech, Ultimate Nutrition, Milky Mist, Nutrela, Fortune, Aashirvaad. |
| Added by waves 1–4 (2 Nov) | 104 | Some are the duplicates and invented products the log names. Not all were checked. |

- The log says one of two Aashirvaad entries was kept (`i=432`) and one of two Ensure pairs was kept (`i=415/416`). **None remain.**
- The delete lists (`scratch/batch*_retired_slugs.json`) were never committed, so the live deletes can't be traced from the repo.
- The scripts **hard-deleted** rows (products, variants, links, flags), so the old live rows are gone. Rebuilding them needs the git copy.

**Files for the author to fill in** (`protein-etl/data/retirements/`):
- `2026-11-03-removed-products-review.json`: all 150, with origin, URL, price and a `decision` field.
- `2026-11-03-restore-candidates.json`: full product data for the 46 pre-wave products, from `43a7ce2`.

Restore after review: copy the kept entries into `data/seed_products.json` and run
`python scripts/seed.py --slugs-file <file with their slugs>` (dry run first with `--dry-run`).

## 2. Upload scripts skipped the uploader's safety checks (confirmed)

`scratch/sync_batch{1-6}_to_supabase.py` and `scratch/sync_wave_{1-4}_to_supabase.py` wrote with the service key directly:
- no `_require_migrations()` check ("stop if the database is behind");
- `is_vegan`, `is_combo` and `is_available` never sent. **31 of the 139 new products are vegan and are live as non-vegan.**
- wave scripts picked products by position (`all_products[-20:]`). After any rebuild, a re-run updates the wrong products.
- batch scripts hard-deleted from uncommitted lists.

**Fixed:** all 10 scripts, plus `scripts/seed_batches_5.py` (positional) and `scripts/sync_amul_live.py` (hard deletes), now stop immediately with a pointer to:
- `scripts/seed.py --slug X` / `--slugs-file F`: goes through `SupabaseUploader` (all checks and flags) and selects **by slug**. It refuses if a slug is missing or listed twice.
- `scripts/retire_products.py LIST.json [--apply]`: new. Needs a committed list with a reason per slug. Dry-run by default. Saves a full backup of the rows, then **hides** (`is_active = false`) instead of deleting.

**To do live:** `python scripts/seed.py --slugs-file data/resync/2026-11-09-batch-synced-slugs.json` re-sends the 139 batch products with the right flags.

## 3. Fake "price checked" times (confirmed, root cause also in the main uploader)

Both the sync scripts **and** `SupabaseUploader._live_upsert` set `price_last_checked = now` on every link at upload time,
including links with no price. The site then trusted that time: a weeks-old scraped D2C price looked "checked today" and could win "Cheapest Option".

**Fixed:**
- Uploader: writes `price_last_checked` only from a new `RedirectLinkItem.price_checked_at` (when the price was really read), and never on unpriced links. Only the pollers stamp "checked now".
- Site (`lib/redirect.ts`): a price with **no** check time, or an unreadable or future one, is no longer "fresh". It can be shown, but can't be "Cheapest" or go into search-engine data. Amazon prices with no check time show "See current price".
- Live data: `supabase/migrations/016_data_incident_repair.sql` clears the fake times. The upload wrote the same timestamp to `product_variants.last_verified_at`, which pollers never touch, so an exact match marks an upload stamp. Run its PREVIEW queries first.

## 4. Wrong protein tiers (confirmed)

`readings.jsonl` hand-labels **80** readings `tier_1` ("Premium Isolate"). These include milk, paneer, cheese, curd, whey *concentrate* and soy blends.
The hand label was used whenever the ingredient classifier didn't recognise the deck. Plain "cow milk" and "paneer" weren't in its vocabulary,
so in the repo the 7 Humpy Farms dairy variants show Tier 1. (The report counts 24 on live, which matches the 22 dairy items `apply_batch4.py` labelled `tier_1`.)

**Fixed:**
- `protein_sources.json`: whole dairy (cow/buffalo milk, paneer, cheese, curd, dahi, yogurt) is Tier 2.
- New `checked_manual_tier()`: a hand tier is capped by what its stated protein source supports, never raised. An unverifiable Tier 1 becomes Unclassified. Used by `build_demo_catalog.py` and the uploader.
- Rebuilt catalog: 7 dairy variants Tier 1 → 2. **0 Tier 1 dairy left.** Side effect: 2 TWF wheat flours go Tier 3 → 4, because the engine's own rules put wheat protein in Tier 4. Check whether that rule is what you want for plain flour.
- Live: migration 016 demotes Tier 1 rows whose source names no isolate or hydrolysate.

## 5. Images (confirmed exactly as reported)

Each non-storage, non-Shopify image URL was fetched on 2026-11-09:
- **11 return a web page** (`text/html`): 5 Amul (`shop.amul.com/media/catalog/...`), 3 Protinex, 3 The Whole Truth. The paths look guessed.
- **2 Unsplash stock photos**: Yoga Bar Oats Crisps, Whole Truth Protein Namkeen.
- **9 hotlinked from retailers**: 7 HealthKart (`hkrtcdn.com`), 1 Flipkart, 1 Blinkit (`grofers.com`).

**Fixed:** new `src/image_policy.py` refuses stock and retailer hosts plus a blocklist (`data/image_url_blocklist.json`). The build drops refused images, so the site shows its placeholder.
`scripts/audit_image_urls.py [--update]` fetches every image URL and adds failures to the blocklist. Run it before each upload.
These 22 products need real pack shots from the brands (upload to Supabase Storage).

## Not done here (needs credentials or a decision)
1. Author decides which of the 150 were really fake → restore the rest.
2. Run migration 016 (preview first) and the 139-product resync.
3. Replace the 22 images.
4. Turn on the D2C price poller schedule, so real check times replace the cleared ones (see the live-pricing plan).

## Verification
- `protein-etl`: 217 tests pass (195 before, plus 22 new for tiers, uploader timestamps and image policy).
- Catalog rebuilt with `scripts/build_demo_catalog.py`: 476 products before and after. The only differences are the 9 tier changes, 23 image drops and the new `price_checked_at` field on links.
