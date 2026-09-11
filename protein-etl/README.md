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
python src/cli.py --interactive
```

Batch ingestion:
```bash
python src/cli.py --batch data/seed_products.json --dry-run
```

Seed database:
```bash
python scripts/seed.py --dry-run
```

Run tests:
```bash
pytest
```
