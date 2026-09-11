---
phase: 01-foundation-data-ingestion-pipeline
plan: 03
subsystem: etl-cli
tags:
  - python
  - shopify-parser
  - rich
  - questionary
  - cli
  - supabase-uploader
  - seed-data

requires:
  - phase: 01-01
    provides: "Supabase database schema, RLS policies, and indexes"
  - phase: 01-02
    provides: "Pydantic models, metrics engine, red-flag scanner, and protein tier classifier"
provides:
  - "Shopify endpoint parser (src/parsers/shopify.py) for automated /products.json extraction"
  - "Manual entry interactive wizard and ingredient tokenizer (src/parsers/manual.py)"
  - "Supabase uploader with offline dry-run fallback (src/db/supabase_client.py)"
  - "Dual-mode terminal CLI application (src/cli.py) with interactive prompts and batch JSON ingestion"
  - "Curated seed dataset of 15 real Indian protein products across all 4 categories (data/seed_products.json)"
  - "Seed runner script (scripts/seed.py) with dry-run support"
  - "27 unit tests passing across the entire ETL test suite"
affects:
  - "02-core-consumer-web-app-discovery"

actuals:
  tokens: 4600
  tasks: 4
  commits: 1

tech-stack:
  added:
    - "httpx"
    - "beautifulsoup4"
    - "rich"
    - "questionary"
    - "supabase-py"
  patterns:
    - "Offline dry-run fallback when live credentials are absent"
    - "Parenthetical-aware ingredient deck tokenizer"
    - "Dual-mode CLI: interactive single-item wizard + batch directory processor"

key-files:
  created:
    - protein-etl/src/parsers/__init__.py
    - protein-etl/src/parsers/shopify.py
    - protein-etl/src/parsers/manual.py
    - protein-etl/src/db/__init__.py
    - protein-etl/src/db/supabase_client.py
    - protein-etl/src/cli.py
    - protein-etl/data/seed_products.json
    - protein-etl/scripts/seed.py
    - protein-etl/tests/test_parsers.py
    - protein-etl/tests/test_cli.py
  modified: []

key-decisions:
  - "Supabase uploader automatically falls back to dry-run mode when SUPABASE_URL / SUPABASE_SERVICE_KEY are omitted."
  - "Raw ingredient string tokenizer preserves nested parenthetical compounds like 'Dark Chocolate (Cocoa Mass, Sugar)'."
  - "CLI provides both single-product interactive prompts and batch directory JSON ingestion."

patterns-established:
  - "Dry-run export directory (data/dry_run_exports/) for local verification of enriched JSON payloads"
  - "Automated slug generation for brands, products, and variants"

requirements-completed:
  - ETL-02
  - ETL-03
  - ETL-04
  - ETL-05
  - ETL-06
---

# Plan 01-03 Summary: CLI Ingestion, Batch Importer & Initial Seed

## Overview
Delivered the operational Human-in-the-Loop CLI, Shopify parser, Supabase uploader with offline dry-run capability, and curated a seed catalog of 15 verified Indian protein products across all 4 top-level categories.

## Accomplishments
1. **Parsers (`src/parsers/`)**:
   - `shopify.py`: Extracts titles, handles, descriptions, pricing, and variant weights from `/products.json` endpoints.
   - `manual.py`: Parenthetical-aware ingredient deck tokenizer that cleanly parses complex Indian FSSAI labeling decks.
2. **Supabase Client & Offline Dry-Run (`src/db/supabase_client.py`)**:
   - Supports live cloud upsert to Supabase PostgreSQL or local offline validation exporting to `data/dry_run_exports/{slug}.json`.
3. **Dual-Mode CLI (`src/cli.py`)**:
   - Built with `rich` and `questionary` supporting both interactive single-product entry and bulk batch JSON file/folder ingestion (`protein-etl batch <path> --dry-run`).
4. **Curated Seed Catalog (`data/seed_products.json` & `scripts/seed.py`)**:
   - 15 real Indian products across RTD drinks (Amul Lassi, Amul Buttermilk, Epigamia), Protein Bars (The Whole Truth Cocoa, TWT Peanut Butter, Yoga Bar, RiteBite Max Protein, Phab), Protein Powders (MuscleBlaze Biozyme Isolate, Nakpro Gold Whey, Plantigo, Cosmix), and Savory Snacks (The Whole Truth Namkeen, RiteBite Chips, Yoga Bar Oats Crisps).
   - Demonstrates clean benchmarks (Amul, The Whole Truth, MuscleBlaze) and dirty benchmarks (RiteBite Max with Maltitol INS 965(ii), Palm Oil, and Hydrolyzed Collagen Tier 4 demotion).
   - Seeding verified with `scripts/seed.py --dry-run`.
