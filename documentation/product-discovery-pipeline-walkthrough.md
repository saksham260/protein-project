# Product Discovery Pipeline — Walkthrough

Date: 2026-09-26 · Branch: `phase2ui` · Package: `protein-etl/src/discovery/`

## Why
Typing every product in by hand doesn't scale. This pipeline finds protein products on brand websites and fills in
as much as it can, starting with the free, exact sources. A human still approves every product before it goes live.

## How it works
```
data/brands.json ──► discover ──► data/drafts/<slug>.json ──► review ──► Supabase ──► website refresh
```

1. **Catalogue** — `fetch_store_catalog` reads each brand's public Shopify feed (`/products.json`, 250 per page, 1 s between requests).
2. **Filter** — `infer_category` keeps only single protein products (needs protein/whey/casein/isolate in the text; skips combos,
   bundles, packs of N) and maps them to `protein-powders`, `protein-bars`, `savory-snacks` or `rtd-drinks`.
3. **Nutrition layers** (`find_label_facts`); the first *complete* result (calories, protein, fat, carbs) wins:

| # | Layer | File | Cost | Notes |
|---|---|---|---|---|
| 1 | Open Food Facts by barcode | `open_food_facts.py` | free | Only when Shopify has a barcode (rare for Indian D2C stores). ODbL licence: credit Open Food Facts. |
| 2 | Shopify description text | `html_facts.py` | free | Tables (per-serving column preferred; per-100g scaled when serving size is printed) and `Protein: 25g` lines (only when the text says "per serving"). |
| 3 | Live product page | `html_facts.py` | free | schema.org JSON-LD `NutritionInformation`, then tables/text. |
| 4a | OCR reads label photos | `ocr.py` + `label_text.py` | free (local CPU) | RapidOCR (PaddleOCR models, `pip install -e ".[ocr]"`). OCRs gallery photos from the back forward; text boxes are grouped into rows, the header row picks the per-serving column (skips %RDA), per-100g is scaled when the serving size is printed. |
| 4b | Gemini reads label photos | `gemini.py` | ~$0.02 / product | Only with `GEMINI_API_KEY` and without `--no-ai`. Sends the last 6 gallery images (resized to 1200 px). Answers cached in `data/cache/gemini/` (git-ignored). |

Photo readers run in the order of `--readers` (default `ocr,gemini`): Gemini is only called when OCR could not read a
complete panel. If no layer is complete, the best partial read is kept and the draft lists the missing fields.

4. **Draft** — `build_draft` writes a JSON file whose `product` matches `ProductCreate`, plus `status`
   (`ready` / `needs_input`), `nutrition_source`, `layers_tried` and `warnings` (shipping weight used, per-100g scaling,
   AI-read values, same nutrition applied to all flavours, missing ingredients). Links: brand store (with price) + Amazon/Blinkit/Zepto/Instamart search links.
5. **Review** — `review` shows each draft with the normal preview (metrics, red flags, protein tier).
   Approve → upload (dry-run respected) → moved to `data/drafts/approved/`. Reject → `data/drafts/rejected/` (never re-drafted).
   Skip → edit the JSON, run `review` again. After approvals the website's `/api/revalidate` is called.

## Comparing OCR vs Gemini
`python src/cli.py compare-readers --limit 3` runs every reader on the same products (no drafts written) and saves
`documentation/reader-comparisons/<date-time>.md` (+ `.json`): complete/partial counts, speed, estimated cost, how often the
two readers agree, and a per-product table with an empty **Correct on pack?** column to score each reader against the real label.
Code: `src/discovery/compare.py`.

## Commands
```bash
cd protein-etl
python src/cli.py discover --no-ai --limit 5    # free layers only, max 5 new drafts per brand
python src/cli.py discover                      # OCR, then Gemini when GEMINI_API_KEY is set
python src/cli.py discover --readers gemini     # Gemini only
python src/cli.py compare-readers --limit 3     # OCR vs Gemini report
python src/cli.py --dry-run review              # practise reviewing without uploading
python src/cli.py review                        # live upload (needs Supabase keys)
```

## What we found checking real stores (2026-09-26)
- Working Shopify feeds: SuperYou, Nakpro, Yoga Bar (in `data/brands.json`), also Wellbeing Nutrition and MyFitness.
- Not Shopify / blocked: The Whole Truth, Avvatar, RiteBite, Phab, Pintola, MyPro.
- None of the sampled products had barcodes, and none had nutrition as text (only in label photos).
  **Expect the free layers to fill few products; most will need Gemini or manual entry from the pack.**

## Other changes
- `parsers/shopify.py`: split into `extract_shopify_product` (fetch one URL) and `parse_shopify_product` (parse raw JSON) so the crawler reuses it; extract now also carries `product_type` and `body_html`.
- `protein-web/next.config.ts`: allows `cdn.shopify.com` images.
- Tests: `protein-etl/tests/test_discovery.py` (units, label matching, table/JSON-LD/OFF/Gemini/OCR-row parsing, category rules, draft → `ProductCreate`, comparison maths). Compiled, not run.
- `pyproject.toml`: optional `ocr` extra (`rapidocr`, `onnxruntime`).

## Known limits
- One nutrition result is applied to every variant of a product; flavours can differ — check in review.
- `infer_category` is keyword-based; fix a wrong category by editing `category_slug` in the draft.
- The Gemini model id (`gemini-3.5-flash`) and request format follow Google's public v1beta `generateContent` API; override with `GEMINI_MODEL` if Google names it differently.
- Brand stores can change or block their feed at any time; `discover` reports unreachable stores and carries on.
