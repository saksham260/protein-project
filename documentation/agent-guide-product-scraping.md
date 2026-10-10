# Agent Guide: Set Up and Run the Product Scraping

**For:** a coding agent (Claude Code, Cursor, etc.) working in this repo for a teammate.
**Goal:** run the product-data pipeline locally, add or refresh products, check quality, and update the website data.
Read this whole file before running anything. Commands are run from the repo root unless a step says otherwise.

---

## 0. Ground rules (do not break these)
1. **Only brand websites' public Shopify feeds** (`https://<store>/products/<handle>.json`, `/products.json`).
   **Never scrape Amazon, Blinkit, Zepto, Instamart or Swiggy.** Those get search links only. Amazon prices come from
   the official API in the price poller (`python src/cli.py poll-prices`), not from scraping.
2. Be polite: one request at a time per store (the scripts already do this). If a store returns 403/429, stop for that store.
3. **Never invent nutrition values.** Every number must come from a label photo (or the brand's lab report). If a value
   is not on the label, write `null`. If you cannot read the label, skip the product.
4. Do not commit `protein-etl/data/demo_catalog/labels/`, `protein-etl/data/drafts/` or any `.env` file (already git-ignored).
5. Ask the human before pushing to GitHub or uploading to Supabase.

## 1. One-time setup
Needs Python 3.11+ and Node 20+.
```bash
cd protein-etl
pip install -e ".[dev,ocr]"     # ocr = RapidOCR + onnxruntime, free local text reading (first run downloads ~tens of MB of models)
cd ../protein-web
npm install
```
No API keys are needed for the steps below. (Supabase / Amazon / Gemini keys are only for uploading, live Amazon
prices and the optional AI reader — see `documentation/how-to-test.md`.)

## 2. How the data is organised
```
protein-etl/data/demo_catalog/
  picks.txt            which products: store | product handle | category | brand   (line N = product number N)
  store_snapshot.json  prices, MRP, variants, main photo from the brand store (refreshed by step 3)
  readings.jsonl       nutrition read from each label photo, one JSON object per line (step 4)
  labels/              label photos found by step 3 (git-ignored)
protein-etl/scripts/
  find_label_photos.py   step 3: refresh store data + find label photos with OCR
  build_demo_catalog.py  step 5: readings → protein-etl/data/seed_products.json + protein-web/src/data/seedCatalog.json
  verify_demo_catalog.py step 6: quality checks + report in documentation/data-quality/
```
Categories (use exactly these slugs): `protein-powders`, `protein-bars`, `savory-snacks`, `rtd-drinks`, `protein-spreads`.

## 3. Add products and find their label photos
**To add a product:** append a line to `picks.txt`, e.g. `nakpro.com|nakpro-pea-protein-isolate|protein-powders|Nakpro`.
The handle is the last part of the product URL (`https://nakpro.com/products/<handle>`). Never reorder or delete lines —
the line number is the product's id in `readings.jsonl`. To drop a product, delete its line from `readings.jsonl` instead.

Working stores (checked 2026-10): superyou.in, nakpro.com, yogabars.in, wellbeingnutrition.com, originnutrition.in,
in.fastandup.com, asitisnutrition.com, beastlife.in, steadfastnutrition.in, alpino.store, maxprotein.in, eatanytime.in,
snackible.com, eatbetterco.com, epigamia.com, sleepyowl.co, myfitness.in, oziva.in. To test a new store:
`https://<store>/products.json?limit=5` must return JSON.

Then run (from `protein-etl/`):
```bash
python scripts/find_label_photos.py --only 101,102     # new products only; omit --only for all (slow: ~1 min/product)
```
For each product it writes `labels/NNN_n.jpg` (best nutrition-label guess), `labels/NNN_i.jpg` (ingredients, if separate)
and `labels/NNN_sheet.jpg` (all photos, numbered in red). If `_n.jpg` is wrong or missing, look at the sheet and save the
right photo full size: `python scripts/find_label_photos.py --photo NNN K` → `labels/NNN_xK.jpg`.
Small text? Crop with Pillow before reading — do not guess blurry digits.

## 4. Read each label into `readings.jsonl` (the important step)
Open the label image (you need image/vision input) and append **one line per product**:
```json
{"i":101,"v":1,"name":"Pea Protein Isolate","variant":"Unflavoured 1kg","net":1000,"serv":36,"label":"1 scoop (36g)",
 "n":[138.96,28.8,1.08,2.16,1.14,0.03,0.36,null,0.07,0,68.4],
 "ing":"Instantized Pea Protein Isolate (100%)","allergens":[],"tags":["Vegan","Vegetarian","No Added Sugar"]}
```
| Field | Meaning |
|---|---|
| `i` | line number in picks.txt |
| `v` | which store variant (size) to price — index into the variant list in `store_snapshot.json`; pick the size whose weight you put in `net` |
| `name` | short product name **without** the brand (e.g. "Pea Protein Isolate") |
| `variant` | size/flavour shown on the site, e.g. "Chocolate 1kg" |
| `net` | net weight of that size in g (ml for drinks), from the label or variant name |
| `serv` | serving size in g/ml **as printed on the label** |
| `n` | **per serving**, in this exact order: kcal, protein g, carbs g, fat g, saturated fat g, trans fat g, cholesterol mg, fibre g, total sugar g, added sugar g, sodium mg. `null` if not on the label |
| `poly` | optional: polyols g (maltitol etc.), common on "no added sugar" bars |
| `ing` | ingredient list exactly as printed, comma-separated (keep brackets). `""` if no photo shows it |
| `protein_source`, `protein_tier` | only when `ing` is empty: the protein source printed on the pack front (e.g. "Whey Protein (30%)") and `tier_1`…`tier_4` from `protein-etl/src/data/protein_sources.json` |
| `allergens` | lowercase: `milk`, `soy`, `peanuts`, `nuts`, `gluten`, `egg` |
| `tags` | any of: `Vegan`, `Vegetarian`, `No Added Sugar`, `Gluten-Free`, `No Palm Oil`, `Keto-Friendly` |

Label-reading rules:
- **Use the per-serving column.** If the label only has per 100 g, multiply by `serv/100` (round to 2 decimals) and
  use the label's own serving size. Never put per-100 g numbers in `n`.
- Ignore `%RDA` / `%DV` columns.
- kJ only? divide by 4.184 for kcal.
- Sodium in g → ×1000 for mg. Salt only (no sodium)? sodium mg = salt g × 400.
- If flavours have different labels, read the one matching the variant you chose.
- Sanity check before saving: kcal ≈ 4×protein + 4×carbs + 9×fat (within ~20%); protein ≤ serving size.

## 5. Build the website data
```bash
python protein-etl/scripts/build_demo_catalog.py
```
Prints the product count per category and a `PROBLEM` line for anything that fails validation. Fix the reading and re-run.
This writes `protein-etl/data/seed_products.json` and `protein-web/src/data/seedCatalog.json` (with ₹/g protein,
protein density, red flags and protein tier computed by `protein-etl/src/engine/`).

## 6. Verify quality
```bash
cd protein-etl
python scripts/verify_demo_catalog.py --live      # --live also compares prices with the stores today
```
- **ERROR** lines must be fixed (exit code 1). Typical causes: per-100 g values used as per-serving, a misread digit, wrong `net`.
- **WARN** lines need a human look (e.g. protein density unusual for the category, title claim "26g protein" ≠ reading).
- Price changes → refresh with `python scripts/find_label_photos.py --snapshot-only`, then repeat step 5.
- The report in `documentation/data-quality/<date>.md` ends with a **random spot-check list**: ask the human to open
  those product pages and tick ✅/❌ against the real labels.

## 7. See it on the website
```bash
cd protein-web
npx tsc --noEmit        # must print nothing
npm run dev             # http://localhost:3000 — uses seedCatalog.json when Supabase is not configured
```

## 8. Optional: load into Supabase
Needs `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` in `protein-etl/.env`.
```bash
cd protein-etl
python scripts/seed.py --dry-run   # validates all products, uploads nothing
python scripts/seed.py             # uploads (ask the human first)
```

## Alternative: fully automatic discovery (less accurate)
`python src/cli.py discover --limit 5` crawls the stores in `data/brands.json`, reads labels with OCR (and Gemini if
`GEMINI_API_KEY` is set) and writes drafts to `data/drafts/` for `python src/cli.py review`. OCR often mixes up
per-100 g and per-serving columns, so the hand-read flow above is preferred for demo data.
See `documentation/product-discovery-pipeline-walkthrough.md`.

## Done checklist
- [ ] `build_demo_catalog.py` shows no PROBLEM lines
- [ ] `verify_demo_catalog.py` shows 0 errors; warnings reviewed
- [ ] `npx tsc --noEmit` clean
- [ ] Human did the spot check in the report
- [ ] Commit `picks.txt`, `readings.jsonl`, `store_snapshot.json`, `seed_products.json`, `seedCatalog.json` and the report (not `labels/`)
