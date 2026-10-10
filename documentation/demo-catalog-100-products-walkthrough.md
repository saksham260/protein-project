# Demo Catalogue: 100 Real Products — Walkthrough

Date: 2026-10-07 · Branch: `phase2ui`

## What was built
The 15 sample products were replaced with **100 real Indian protein products** in **5 categories**. Each product's
nutrition was read from its real nutrition-label photo on the brand's own website.

| Category | Slug | Products |
|---|---|---|
| Protein Powders | `protein-powders` | 30 |
| Protein Bars | `protein-bars` | 20 |
| Savory Snacks | `savory-snacks` | 18 |
| RTD Drinks | `rtd-drinks` | 16 |
| Peanut Butter & Spreads (new) | `protein-spreads` | 16 |

17 brands: SuperYou, Nakpro, Yoga Bar, Wellbeing Nutrition, Origin Nutrition, Fast&Up, AS-IT-IS Nutrition, Beastlife,
Steadfast Nutrition, Alpino, Max Protein (RiteBite), Eat Anytime, Snackible, Eat Better, Epigamia, Sleepy Owl, MyFitness.

## How the data was collected
1. **Store feeds** — each brand's public Shopify feed (`/products.json`) gave the name, price, MRP (compare-at price),
   pack sizes and photos. 18 stores were reachable out of ~60 tried.
2. **Finding the label photo** — RapidOCR (free, local text reading) scanned each product's photos and picked the one
   that looked most like a nutrition table. No brand publishes nutrition as text, only in photos.
3. **Reading the label** — the nutrition table and ingredient list were read from the photo **by hand (Claude)**, not
   by OCR, because OCR often mixed up the per-100g and per-serving columns.
4. **Per serving** — all values are stored per serving. Where a label only gave per-100g, values were scaled to the
   label's own serving size (e.g. 32 g / 2 tbsp for peanut butter).
5. **Checks** — every product passed: calories ≈ 4×protein + 4×carbs + 9×fat (within 20%), protein ≤ serving size,
   and the ETL's `ProductCreate` validation (pack math). `scripts/seed.py --dry-run` loads all 100.

## Files
| File | Purpose |
|---|---|
| `protein-etl/data/demo_catalog/picks.txt` | Chosen products: store, handle, category, brand (line number = reading id) |
| `protein-etl/data/demo_catalog/readings.jsonl` | The hand-read label values, one product per line |
| `protein-etl/data/demo_catalog/store_snapshot.json` | Price/variant/image snapshot from the stores (2026-10-06) |
| `protein-etl/scripts/find_label_photos.py` | Refreshes store_snapshot.json and finds each product's label photo with OCR (→ `demo_catalog/labels/`, git-ignored) |
| `protein-etl/scripts/build_demo_catalog.py` | Builds both outputs below from those three files |
| `protein-etl/scripts/verify_demo_catalog.py` | Quality checks + live price check + spot-check list → `documentation/data-quality/<date>.md` |
| `documentation/agent-guide-product-scraping.md` | Step-by-step guide for a teammate's coding agent to run all of this |
| `protein-etl/data/seed_products.json` | 100 products for `scripts/seed.py` → Supabase |
| `protein-web/src/data/seedCatalog.json` | Same 100, enriched (₹/g protein, density, red flags, protein tier); the website uses it when Supabase is not set up |

Reading format (`n` = calories, protein, carbs, fat, sat fat, trans fat, cholesterol mg, fibre, total sugar, added sugar, sodium mg; `null` = not on label):
```json
{"i":5,"v":1,"name":"Platinum Raw Whey Protein Isolate","variant":"Unflavoured 1kg","net":1000,"serv":34,
 "n":[127,30.6,0.85,0.1,0.02,0.01,3.4,null,0.14,0,70],"ing":"Instantized Whey Protein Isolate (100%)",
 "allergens":["milk"],"tags":["Vegetarian"]}
```
`i` = line in picks.txt, `v` = which store variant (size) is used for price, `poly` = polyols (bars).

Rebuild after editing a reading: `python protein-etl/scripts/build_demo_catalog.py`

## Website changes (5th category)
- `src/lib/constants.ts` — added **Peanut Butter & Spreads** (`protein-spreads`, 🥜).
- `src/app/HomeClient.tsx` — category tile image, "suggested" mix includes spreads, category grid is 5 wide on desktop.
- `src/lib/data.ts` — fallback image for spreads.
- `src/lib/topPicksConfig.ts` — new award "Best Peanut Butter".
- `public/images/products/peanut-butter-jar.jpg` — category tile (Alpino product photo).
- Product photos load from `cdn.shopify.com` (already allowed in `next.config.ts`).

## Limits — read before the demo
- **Prices are a snapshot** from each brand's own store on 2026-10-06; Amazon/Blinkit/Zepto/Instamart links are search links.
- **One size per product** (e.g. 1 kg tub); other sizes and flavours are not listed as variants.
- **Hand-read values**: careful, but a typo is possible — compare against the brand page if a number looks off.
- 11 products have **no ingredient list** (label photo had none), so red flags may be missed.
- Only **1 product shows protein tier "Unknown"** (Max Protein Choco Chips Bliss Cookies — no source stated anywhere).

## Protein tier fix (2026-10-07)
50 products first showed tier "Unknown" because the classifier didn't know common Indian protein sources.
`protein-etl/src/data/protein_sources.json` now also recognises:
- **Tier 2** (label now "Concentrate/Casein/Milk/Egg"): skimmed / ultrafiltered milk, milk solids, toned milk, whole milk powder.
- **Tier 3** (label now "Plant & Yeast (Pea/Rice/Soy/Yeast/Peanut)"): fermented yeast protein, peanut protein / peanut flour,
  roasted peanuts, pulse & millet flours (chickpea, urad, lentil, chana dal, green gram), pumpkin seed protein.

10 products with no ingredient list get their source from the pack front or the same product line
(`protein_source` / `protein_tier` fields in `readings.jsonl`, e.g. "30% whey protein", "blend of 3 plant proteins").

Result: Tier 1: 4 · Tier 2: 30 · Tier 3: 60 · Tier 4: 5 · Unknown: 1.
Website tier text updated to match (`constants.ts`, `Footer.tsx`, `FilterPanel.tsx`).
- Assumptions: Origin "Daily Plant Protein Mocha" — values from the brand's lab report (per 100 g) scaled to the 40.5 g serving
  of its sister product, pack assumed 810 g. Eat Anytime bars (chocolate) ingredients not shown.
- Some products are currently **out of stock** on the brand store (still real products with real labels).
- Skipped: jowar puffs (~3 g protein), products whose photos had no readable label (Oziva, some Max Protein items).
- The old 15 sample products were removed (their data was placeholder-quality).
