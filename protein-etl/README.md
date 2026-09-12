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
