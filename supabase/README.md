# Supabase Infrastructure: The Protein Discovery Engine

This directory contains the database migration scripts, security policies, performance indexing, and configuration instructions for The Protein Discovery Engine.

---

## 1. Directory Structure

```
supabase/
├── migrations/
│   ├── 001_schema.sql       # Core database tables, constraints, triggers
│   ├── 002_rls.sql          # Row-Level Security policies & user auth sync
│   └── 003_indexes.sql      # B-Tree, GIN array, and pg_trgm fuzzy search indexes
└── README.md
```

---

## 2. Running the Migrations

You can run these migrations either through the **Supabase Dashboard** or via the **Supabase CLI**.

### Option A: Via Supabase Dashboard (Recommended for quick setup)
1. Go to [database.new](https://database.new) or open your Supabase project dashboard.
2. Navigate to **SQL Editor** in the left sidebar.
3. Open and run each migration in numeric order:
   - Run `001_schema.sql` (Creates all tables, types, and triggers).
   - Run `002_rls.sql` (Enables Row-Level Security and user sync trigger).
   - Run `003_indexes.sql` (Enables `pg_trgm` extension and performance indexes).

### Option B: Via Supabase CLI
```bash
# Link your local project to your Supabase project
supabase link --project-ref <your-project-id>

# Push the migrations to the linked remote database
supabase db push
```

---

## 3. Storage Bucket Configuration (`product-images`)

1. Go to **Storage** in the Supabase Dashboard.
2. Click **New Bucket**:
   - **Bucket Name**: `product-images`
   - **Public Bucket**: **Enabled** (Allows anonymous read for product pack photos in web client).
3. **Storage RLS Policies**:
   - By default, public buckets allow public `SELECT` access.
   - For `INSERT` / `UPDATE` / `DELETE`, create a policy restricting writes to `service_role` (used by the Python ETL script) or authenticated admins.

---

## 4. Authentication Configuration (Google OAuth)

1. Navigate to **Authentication** → **Providers** → **Google**.
2. Toggle Google to **Enabled**.
3. Create OAuth credentials in [Google Cloud Console](https://console.cloud.google.com/apis/credentials):
   - **Authorized redirect URI**: `https://<your-supabase-project-id>.supabase.co/auth/v1/callback`
   - Copy **Client ID** and **Client Secret** into the Supabase Dashboard.
4. (Optional) Under **URL Configuration**, add your local frontend URL (`http://localhost:3000`) and production domain to **Redirect URLs**.

---

## 5. Environment Variables Template

Add the following to `protein-etl/.env` and `protein-web/.env.local`:

```env
# Shared Supabase Cloud Configuration
SUPABASE_URL=https://<your-project-id>.supabase.co

# Public Anon Key (for Next.js client-side queries)
NEXT_PUBLIC_SUPABASE_URL=https://<your-project-id>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOi...

# Private Service Role Key (NEVER expose to frontend; used only in protein-etl)
SUPABASE_SERVICE_KEY=eyJhbGciOi...
```
