# Phase 1: Foundation & Data Ingestion Pipeline - Context

**Gathered:** 2026-09-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers the foundational data and ingestion infrastructure for The Protein Discovery Engine:
1. Supabase PostgreSQL schema, RLS policies, indexing, and storage bucket configuration.
2. Metrics computation engine (Cost per g of protein, protein density %, true net carbs).
3. Red-flag detection engine (maltitol, amino spiking, hydrogenated/palm fat, hidden sugars) and 4-tier protein blend classifier.
4. Python ETL CLI tool (`protein-etl`) supporting single-product interactive entry (Shopify URL & manual) and batch JSON ingestion.
5. Initial seed catalog of 10–20 verified Indian protein products across RTD drinks, bars, powders, and snacks.

</domain>

<decisions>
## Implementation Decisions

### Database Migration & Schema Setup
- **D-01:** Implement modular SQL migration files (`001_schema.sql`, `002_rls.sql`, `003_indexes.sql`) under `supabase/migrations/` — **Reversibility:** costly — Schema migrations define column names and foreign keys across all downstream web and ETL components.
- **D-02:** Support standard `.env` configuration (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`) plus an offline dry-run / mock mode in `protein-etl` so tests and ingestion validation can run without requiring an active cloud DB connection — **Reversibility:** reversible.
- **D-03:** Enable `pg_trgm` extension in PostgreSQL for fuzzy text search across product, brand, and variant names — **Reversibility:** reversible.

### ETL Tooling & CLI UX
- **D-04:** Standardize `protein-etl` on `pyproject.toml` compatible with `uv` or standard Python `venv` + `pip` — **Reversibility:** reversible.
- **D-05:** Build a dual-mode CLI supporting an interactive single-product wizard (`rich` + `questionary` with live formula preview) alongside a batch JSON file/directory ingestion command for bulk dataset operations — **Reversibility:** reversible.
- **D-06:** Model ingredient decks as `ingredient_list text[]` (normalized lowercase for fast containment) and `ingredient_deck_raw jsonb` (preserving audit position order) — **Reversibility:** one-way — Changing ingredient representation breaks both the flag scanner and Supabase schema.

### Seed Data Selection
- **D-07:** Curate the initial 10–20 seed catalog with a balanced distribution across all 4 categories:
  - *RTD Dairy & Drinks*: Amul High Protein Lassi / Buttermilk, Epigamia Greek Yogurt, Raw Pressery.
  - *Protein Bars*: The Whole Truth (clean benchmark), Yoga Bar (clean/concentrate), RiteBite Max Protein (red-flag benchmark with maltitol/collagen/soy isolate blend).
  - *Protein Powders*: MuscleBlaze Biozyme Whey Isolate (Tier 1 benchmark), Nakpro Gold Whey (Tier 2 budget concentrate), Plantigo / Cosmix (Tier 3 plant blend).
  - *Savory Snacks*: The Whole Truth protein namkeen/cookies, RiteBite protein chips.
  — **Reversibility:** reversible.

### Agent Discretion
- Specific test fixtures and mocking libraries (`pytest`, `pytest-mock`, `responses`/`respx` for HTTP mocking).
- Internal layout of CLI prompts and ANSI color styling for flag alerts in the terminal.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Architecture & Specs
- [implementation_plan.md](file:///c:/Users/Saksham/Documents/new-project/implementation_plan.md) — Core system topology, ERD, calculated metrics formulas, red-flag alias dictionary, and CLI specification.
- [.planning/REQUIREMENTS.md](file:///c:/Users/Saksham/Documents/new-project/.planning/REQUIREMENTS.md) — Scope contracts DB-01 to DB-04, ENG-01 to ENG-05, and ETL-01 to ETL-06.
- [.planning/PROJECT.md](file:///c:/Users/Saksham/Documents/new-project/.planning/PROJECT.md) — Overarching vision, constraints, and locked decisions.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None (greenfield project initialization).

### Established Patterns
- Python Pydantic models for strict data validation before database insertion.
- Precomputed stored metrics (`cost_per_g_protein`, `protein_density_pct`, `true_net_carbs_g`) on `product_variants`.

### Integration Points
- Supabase REST API via `supabase-py` using the service role key for ETL writes.

</code_context>

<specifics>
## Specific Ideas

- Ensure red-flag engine reports the exact matched alias and INS number (e.g., "INS 965(i) Maltitol") for transparency.
- Ensure the protein tier classifier identifies the primary protein source from the first position of the ingredient deck while deriving the tier rating from the lowest-quality source in the blend.

</specifics>

<deferred>
## Deferred Ideas

- None — discussion stayed strictly within Phase 1 scope. Next.js web application, search UI, and user auth belong in Phases 2 and 3.

</deferred>

---

*Phase: 1-Foundation & Data Ingestion Pipeline*
*Context gathered: 2026-09-09*
