# Phase 1 Fixes — Walkthrough (2026-09-12)

Follow-up to [codebase-review-2026-09-12.md](codebase-review-2026-09-12.md). Fixes the Phase 1 bugs found in the review.
Not committed yet — all changes are in the working tree.

## 1. ₹/g protein (critical)
**Problem:** `mrp_inr / protein_g` used protein for *one serving*, so a 1kg tub looked ~30× too expensive.

**Fix:** `src/engine/metrics.py`
- New `calculate_protein_per_pack(protein_g, net_weight_g, serving_size_g)` = `protein_g × net_weight_g / serving_size_g`.
- `compute_all_metrics(...)` now takes `net_weight_g`, `serving_size_g`, `platform_prices`.
- New metrics: `best_price_inr` (lowest known platform price) and `best_cost_per_g_protein`.
- Nutrition is now documented as **per serving** (`NutritionPerPack` docstring in `src/models.py`).

| Product | Before | After |
|---|---|---|
| MuscleBlaze Biozyme 1kg | ₹139.96/g | ₹4.34/g |
| Nakpro Gold 1kg | ₹74.96/g | ₹2.47/g |
| Plantigo 1kg | ₹104.12/g | ₹3.64/g |
| Cosmix 750g | ₹86.00/g | ₹4.36/g |
| TWT Namkeen 120g | ₹19.90/g | ₹6.63/g |

Bars and drinks are unchanged (serving = pack).

## 2. Pack math validation
`VariantCreate` (`src/models.py`):
- `servings_per_pack` is derived from `net_weight_g / serving_size_g` if omitted.
- Rejects packs where `servings × serving size` is off from net weight by >25%, or serving > pack.
- Rejects two redirect links for the same platform.

## 3. Fake / broken links in seed data
Checked live: Amazon ASINs like `dp/B08XYZ1234` → 404, The Whole Truth product pages → 404,
others unreachable. `data/seed_products.json` now:
- Amazon links → Amazon search links (`amazon.in/s?k=Brand+Product`), no made-up price.
- Unverified D2C links removed.
- Unverified `image_url`s set to `null`.
- Blinkit / Zepto search links kept.

New helpers in `src/links.py` (`build_search_url`, `check_url`) and a new CLI command:
```bash
python src/cli.py check-links data/seed_products.json
```
Exits with code 1 if any link is broken (404/410). `blocked`/`unreachable` usually means bot protection.

Side effect: seed has no platform prices now, so `best_*` metrics are empty until real links + prices are added via the CLI.

## 4. Duplicate redirect links + stale fields
- `supabase/migrations/004_phase1_fixes.sql`: removes existing duplicates, adds `UNIQUE (variant_id, platform)`,
  adds `non_glycemic_polyols_g`, `best_price_inr`, `best_cost_per_g_protein` columns + index.
- `src/db/supabase_client.py`: redirect links are **upserted** on `(variant_id, platform)`, platforms no longer
  listed are deleted, `price_last_checked` and `last_verified_at` are set to now, polyols and
  `additional_nutrients` are now saved.

## 5. Auth trigger
Migration 004 recreates `on_auth_user_created` as `AFTER INSERT OR UPDATE OF email, raw_user_meta_data`
so it no longer runs on every login.

## 6. Ingredient matching
New `src/engine/text_match.py`: whole-word matching + "longest match wins" for overlapping aliases.
- **Red flags** (`red_flags.py`): "hydrogenated glucose syrup" is only a maltitol flag (not also hidden sugar);
  "high fructose corn syrup" no longer also reports "corn syrup". Bare `"1400"` removed from the dictionary.
- **Protein tier** (`protein_tier.py`): primary source follows label order *inside* blends
  (RiteBite Choco Slim now → Soy Protein Isolate, was Whey Concentrate); "calcium caseinate" no longer
  also matches Micellar Casein.
- Unchanged by design: the weakest-link rule (any collagen → Tier 4) is in the spec (ENG-05) and its test.

## 7. Shopify importer (`src/parsers/shopify.py`)
- `mrp_inr` = `compare_at_price` when the item is on sale, else `price`; `price_inr` = selling price.
- `weight_g` read from the variant title (`1kg`, `500 g`, `200ml`, `2 lbs`); falls back to Shopify's
  shipping weight with `weight_source: "shipping"` so the CLI warns you to check it.

## 8. Manual entry CLI (`src/parsers/manual.py`)
- Asks servings per pack (pre-filled from weights), labels nutrition "per serving".
- Amazon price is optional (no longer copied from MRP); D2C URL/price default from Shopify.
- Offers auto search links for Amazon / Blinkit / Zepto / Instamart.
- Keeps Shopify SKU, barcode and first product image.

## 9. Tests
- `test_cli.py` no longer writes into `data/dry_run_exports` (that was what corrupted the Plantigo export).
- New tests: multi-serving ₹/g, best price, pack validation (`test_models.py`), blend order, overlap
  handling, Shopify MRP/weight, `check-links`.
- Per project rules only a compile check was run (`python -m compileall` → OK). Unit tests were **not** run:
  `cd protein-etl && pytest`.

## Deploy steps
1. Run `supabase/migrations/004_phase1_fixes.sql` in the Supabase SQL editor.
2. Re-seed so stored metrics are recomputed: `python scripts/seed.py`.
3. Add real product URLs + prices through `python src/cli.py interactive`, then `check-links`.

## Still open (not in this pass)
- No location / pincode / availability tables — needs a product decision on how "near me" should work.
- Nutrition is still typed in by hand (Shopify doesn't expose it in `products.json`).
