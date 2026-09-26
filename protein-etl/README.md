# Protein Discovery Engine - ETL Pipeline

ETL pipeline and CLI helper for ingestion, nutrition computation, protein tier classification, and red flag scanning for Indian packaged foods.

## Installation

```bash
cd protein-etl
pip install -e .
```

## Usage

Interactive CLI:
```bash
python src/cli.py interactive
```

Batch ingestion:
```bash
python src/cli.py --dry-run batch data/seed_products.json
```

Check that every redirect and image link still works:
```bash
python src/cli.py check-links data/seed_products.json
```

Refresh Amazon prices (needs Supabase + Amazon Creators API keys, see `.env.example`):
```bash
python src/cli.py --dry-run poll-prices   # read and report only
python src/cli.py poll-prices             # write prices, history, best-price metrics, refresh website
python src/cli.py poll-prices --force     # also accept price changes larger than 50%
```
Runs every 6 hours via `.github/workflows/poll-prices.yml`. Amazon links need a real product URL
(`amazon.in/dp/<ASIN>`); search links are skipped.

Discover products from brand Shopify stores (brands listed in `data/brands.json`):
```bash
python src/cli.py discover                 # all brands; uses Gemini only if GEMINI_API_KEY is set
python src/cli.py discover --no-ai         # free layers only
python src/cli.py discover --brand Nakpro --limit 5
python src/cli.py review                   # approve / skip / reject each draft (add --dry-run before 'review' to skip upload)
```
Nutrition layers, first complete result wins: Open Food Facts (barcode) → Shopify description → product page
(JSON-LD / tables / text) → Gemini label photos. Drafts live in `data/drafts/`; fix a `needs_input` draft by editing its JSON.

Seed database:
```bash
python scripts/seed.py --dry-run
```

Run tests:
```bash
pytest
```

## Data conventions

- Nutrition values are **per labelled serving** (`serving_size_g`). For bars and bottles the serving is the whole pack.
- `servings_per_pack` is derived from `net_weight_g / serving_size_g` when omitted; packs whose numbers disagree by more than 25% are rejected.
- `cost_per_g_protein` = MRP ÷ protein in the whole pack. `best_cost_per_g_protein` uses the lowest known platform price instead.
- One redirect link per platform per variant. Use search links (Amazon/Blinkit/Zepto/Instamart) when a verified product URL is not available.
