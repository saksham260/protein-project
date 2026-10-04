# Supabase Database & Migrations

This directory contains the database migration scripts and verification tools for **The Protein Discovery Engine**.

---

## 1. Directory Structure

| File | Purpose | Safe to re-run? |
|---|---|---|
| [`setup_all.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/setup_all.sql) | Combined single-paste setup script containing 001–007 in exact order. | ✅ Yes |
| [`verify.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/verify.sql) | Audit query checking tables, views, RLS status, policies, grants, and row counts. | ✅ Yes |
| [`migrations/001_schema.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/001_schema.sql) | Core schema: brands, categories, products, product_variants, red flags, redirect links, users, preferences, favorites. | ✅ Yes |
| [`migrations/002_rls.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/002_rls.sql) | Row Level Security policies (public catalog reads, user-scoped CRUD) and auth user trigger. | ✅ Yes |
| [`migrations/003_indexes.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/003_indexes.sql) | B-tree metric indexes, GIN array indexes, and trigram fuzzy search indexes. | ✅ Yes |
| [`migrations/004_phase1_fixes.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/004_phase1_fixes.sql) | Unique constraint on `(variant_id, platform)`, polyols, and best-price columns. | ✅ Yes |
| [`migrations/005_prices_availability.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/005_prices_availability.sql) | `price_history`, crowd-sourced `availability_reports`, ASIN tracking, and `availability_summary` view. | ✅ Yes |
| [`migrations/006_api_grants.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/006_api_grants.sql) | Explicit Data API table grants for `anon`, `authenticated`, and `service_role`. | ✅ Yes |
| [`migrations/007_seed_categories.sql`](file:///c:/Users/Saksham/Documents/new-project/supabase/migrations/007_seed_categories.sql) | Populates the 4 core categories matching frontend `constants.ts`. | ✅ Yes |

---

## 2. Pre-Flight Verification Commands

Before and after migrations or data operations, run the pre-flight checks:

### Python ETL Pre-Flight Check (Tests service_role write & read)
```bash
python protein-etl/scripts/check_connection.py
```

### Next.js Frontend Pre-Flight Check (Tests publishable key & anonymous report insert)
```bash
cd protein-web
npm run check:supabase
```

---

## 3. Seeding Products

To seed or refresh the 15 curated Indian protein products:

```bash
cd protein-etl

# Dry-run test (local validation without database writes)
python scripts/seed.py --dry-run

# Live upload to Supabase (idempotent, safe to repeat)
python scripts/seed.py
```
