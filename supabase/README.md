# Supabase Database & Migrations

This directory contains the database migration scripts and verification tools for **The Protein Discovery Engine**.

---

## 1. Directory Structure

| File | Purpose | Safe to re-run? |
|---|---|---|
| [`setup_all.sql`](setup_all.sql) | All migrations (001-015) combined, for a fresh project. | ✅ Yes |
| [`verify.sql`](verify.sql) | Audit query checking tables, views, RLS status, policies, grants and row counts. | ✅ Yes |
| [`migrations/001_schema.sql`](migrations/001_schema.sql) | Core schema: brands, categories, products, variants, red flags, redirect links, users, preferences, favorites. | ✅ Yes |
| [`migrations/002_rls.sql`](migrations/002_rls.sql) | Row Level Security policies and the auth user trigger. | ✅ Yes |
| [`migrations/003_indexes.sql`](migrations/003_indexes.sql) | Metric, array and trigram search indexes. | ✅ Yes |
| [`migrations/004_phase1_fixes.sql`](migrations/004_phase1_fixes.sql) | Unique `(variant_id, platform)`, polyols and best-price columns. | ✅ Yes |
| [`migrations/005_prices_availability.sql`](migrations/005_prices_availability.sql) | `price_history`, `availability_reports`, ASIN tracking and `availability_summary`. | ✅ Yes |
| [`migrations/006_api_grants.sql`](migrations/006_api_grants.sql) | Data API grants for `anon`, `authenticated` and `service_role`. | ✅ Yes |
| [`migrations/007_seed_categories.sql`](migrations/007_seed_categories.sql) | The 4 core categories. | ✅ Yes |
| [`migrations/008_variant_flags_breakfast.sql`](migrations/008_variant_flags_breakfast.sql) | `is_combo`, `is_available`, Breakfast category. | ✅ Yes |
| [`migrations/009_dairy_category.sql`](migrations/009_dairy_category.sql) | Dairy category. | ✅ Yes |
| [`migrations/010_vegan_cookies.sql`](migrations/010_vegan_cookies.sql) | `is_vegan`, Cookies category. | ✅ Yes |
| [`migrations/011_user_activity.sql`](migrations/011_user_activity.sql) | `user_activity` for Suggested for You. | ✅ Yes |
| [`migrations/012_user_searches.sql`](migrations/012_user_searches.sql) | `user_searches` for recent searches. | ✅ Yes |
| [`migrations/013_new_categories.sql`](migrations/013_new_categories.sql) | Mass Gainers, Adult Nutrition, Staples categories. | ✅ Yes |
| [`migrations/014_audit_fixes.sql`](migrations/014_audit_fixes.sql) | Private availability reports, `outbound_clicks`, `delete_my_account`. | ✅ Yes |
| [`migrations/015_test_reports.sql`](migrations/015_test_reports.sql) | `test_reports`, the lab reports shown on product pages. | ✅ Yes |

Nothing records which migrations have run, so check with `verify.sql`. The ETL uploader stops with a clear error if a required migration is missing.

---

## 2. Pre-Flight Verification Commands

Before and after migrations or data operations, run the pre-flight checks:

### Python ETL Pre-Flight Check (Tests service_role write & read)
```bash
python protein-etl/scripts/check_connection.py
```

### Next.js Frontend Pre-Flight Check (Read-only)
```bash
cd protein-web
npm run check:supabase
```

---

## 3. Seeding Products

To seed or refresh the catalog:

```bash
cd protein-etl

# Dry-run test (local validation without database writes)
python scripts/seed.py --dry-run

# Live upload to Supabase (idempotent, safe to repeat)
python scripts/seed.py
```
