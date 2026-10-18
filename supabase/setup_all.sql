-- ==============================================================================
-- setup_all.sql: The Complete Protein Discovery Engine Database Setup
-- Combines migrations 001 through 007 in exact dependency order.
--
-- Instructions for Supabase SQL Editor:
-- 1. Open your Supabase Dashboard -> SQL Editor -> New query.
-- 2. Paste the ENTIRE contents of this file.
-- 3. Click "Run" (or Ctrl + Enter).
-- 4. If prompted with a warning about destructive operations (due to cleanup deletes/drops),
--    click "Run this query".
-- ==============================================================================

-- ##############################################################################
-- SECTION 1: 001_schema.sql (Core Database Schema)
-- ##############################################################################

-- Enable UUID extension if not already available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Function to handle automated updated_at timestamp refreshes
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------------------
-- 1.1 BRANDS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS brands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    logo_url TEXT,
    website_url TEXT,
    description TEXT,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 1.2 CATEGORIES
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    icon TEXT,
    display_order INT NOT NULL DEFAULT 0
);

-- ------------------------------------------------------------------------------
-- 1.3 PRODUCTS (Parent Products)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    image_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE TRIGGER update_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ------------------------------------------------------------------------------
-- 1.4 PRODUCT_VARIANTS (Atomic Unit of Truth)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    sku TEXT,
    barcode_ean TEXT,
    mrp_inr NUMERIC(10, 2) NOT NULL,
    net_weight_g NUMERIC(10, 2) NOT NULL,
    serving_size_g NUMERIC(10, 2) NOT NULL,
    servings_per_pack INT NOT NULL DEFAULT 1,
    serving_size_label TEXT,
    calories_kcal NUMERIC(10, 2) NOT NULL,
    protein_g NUMERIC(10, 2) NOT NULL,
    total_fat_g NUMERIC(10, 2) NOT NULL,
    saturated_fat_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    trans_fat_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    cholesterol_mg NUMERIC(10, 2) NOT NULL DEFAULT 0,
    total_carbs_g NUMERIC(10, 2) NOT NULL,
    dietary_fiber_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    total_sugars_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    added_sugars_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    sodium_mg NUMERIC(10, 2) NOT NULL DEFAULT 0,
    additional_nutrients JSONB NOT NULL DEFAULT '{}'::jsonb,
    ingredient_list TEXT[] NOT NULL DEFAULT '{}',
    ingredient_deck_raw JSONB NOT NULL DEFAULT '[]'::jsonb,
    allergens TEXT[] NOT NULL DEFAULT '{}',
    dietary_tags TEXT[] NOT NULL DEFAULT '{}',
    primary_protein_source TEXT,
    protein_tier TEXT,
    has_added_free_form_aminos BOOLEAN NOT NULL DEFAULT false,
    cost_per_g_protein NUMERIC(10, 2),
    protein_density_pct NUMERIC(5, 2),
    true_net_carbs_g NUMERIC(10, 2),
    image_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE TRIGGER update_product_variants_updated_at
BEFORE UPDATE ON product_variants
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ------------------------------------------------------------------------------
-- 1.5 VARIANT_RED_FLAGS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS variant_red_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    flag_type TEXT NOT NULL,
    flag_severity TEXT NOT NULL CHECK (flag_severity IN ('high', 'amber', 'info')),
    flag_label TEXT NOT NULL,
    flag_description TEXT NOT NULL,
    matched_ingredient TEXT,
    ins_number TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 1.6 REDIRECT_LINKS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS redirect_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL CHECK (platform IN ('amazon', 'blinkit', 'zepto', 'instamart', 'd2c')),
    url TEXT NOT NULL,
    platform_price_inr NUMERIC(10, 2),
    price_last_checked TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 1.7 USERS (Mirrors Supabase Auth auth.users)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 1.8 USER_PREFERENCES
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    daily_protein_target_g NUMERIC(10, 2),
    body_weight_kg NUMERIC(10, 2),
    dietary_restrictions TEXT[] NOT NULL DEFAULT '{}',
    allergens TEXT[] NOT NULL DEFAULT '{}',
    avoided_ingredients TEXT[] NOT NULL DEFAULT '{}',
    preferred_protein_tier TEXT,
    max_budget_per_g NUMERIC(10, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE TRIGGER update_user_preferences_updated_at
BEFORE UPDATE ON user_preferences
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ------------------------------------------------------------------------------
-- 1.9 USER_FAVORITES
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, variant_id)
);


-- ##############################################################################
-- SECTION 2: 002_rls.sql (Row-Level Security Policies & Auth Sync)
-- ##############################################################################

ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE variant_red_flags ENABLE ROW LEVEL SECURITY;
ALTER TABLE redirect_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- 2.1 CATALOG TABLES: Public Read (Anon + Authenticated), Write via Service Role
DROP POLICY IF EXISTS "Allow public read on brands" ON brands;
CREATE POLICY "Allow public read on brands"
    ON brands FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on brands" ON brands;
CREATE POLICY "Allow service_role full access on brands"
    ON brands FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on categories" ON categories;
CREATE POLICY "Allow public read on categories"
    ON categories FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on categories" ON categories;
CREATE POLICY "Allow service_role full access on categories"
    ON categories FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on active products" ON products;
CREATE POLICY "Allow public read on active products"
    ON products FOR SELECT
    USING (is_active = true);

DROP POLICY IF EXISTS "Allow service_role full access on products" ON products;
CREATE POLICY "Allow service_role full access on products"
    ON products FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on active product_variants" ON product_variants;
CREATE POLICY "Allow public read on active product_variants"
    ON product_variants FOR SELECT
    USING (is_active = true);

DROP POLICY IF EXISTS "Allow service_role full access on product_variants" ON product_variants;
CREATE POLICY "Allow service_role full access on product_variants"
    ON product_variants FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on variant_red_flags" ON variant_red_flags;
CREATE POLICY "Allow public read on variant_red_flags"
    ON variant_red_flags FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on variant_red_flags" ON variant_red_flags;
CREATE POLICY "Allow service_role full access on variant_red_flags"
    ON variant_red_flags FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on redirect_links" ON redirect_links;
CREATE POLICY "Allow public read on redirect_links"
    ON redirect_links FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on redirect_links" ON redirect_links;
CREATE POLICY "Allow service_role full access on redirect_links"
    ON redirect_links FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- 2.2 USER TABLES: User-Scoped CRUD via auth.uid()
DROP POLICY IF EXISTS "Users can read their own profile" ON users;
CREATE POLICY "Users can read their own profile"
    ON users FOR SELECT
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update their own profile" ON users;
CREATE POLICY "Users can update their own profile"
    ON users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Allow service_role full access on users" ON users;
CREATE POLICY "Allow service_role full access on users"
    ON users FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Users can read own preferences" ON user_preferences;
CREATE POLICY "Users can read own preferences"
    ON user_preferences FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own preferences" ON user_preferences;
CREATE POLICY "Users can insert own preferences"
    ON user_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own preferences" ON user_preferences;
CREATE POLICY "Users can update own preferences"
    ON user_preferences FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own preferences" ON user_preferences;
CREATE POLICY "Users can delete own preferences"
    ON user_preferences FOR DELETE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Allow service_role full access on user_preferences" ON user_preferences;
CREATE POLICY "Allow service_role full access on user_preferences"
    ON user_preferences FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Users can read own favorites" ON user_favorites;
CREATE POLICY "Users can read own favorites"
    ON user_favorites FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can add own favorites" ON user_favorites;
CREATE POLICY "Users can add own favorites"
    ON user_favorites FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can remove own favorites" ON user_favorites;
CREATE POLICY "Users can remove own favorites"
    ON user_favorites FOR DELETE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Allow service_role full access on user_favorites" ON user_favorites;
CREATE POLICY "Allow service_role full access on user_favorites"
    ON user_favorites FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- 2.3 AUTOMATED USER PROFILE SYNCHRONIZATION TRIGGER
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, display_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)),
        NEW.raw_user_meta_data->>'avatar_url'
    )
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        display_name = COALESCE(EXCLUDED.display_name, public.users.display_name),
        avatar_url = COALESCE(EXCLUDED.avatar_url, public.users.avatar_url);

    -- Also initialize an empty default preferences row
    INSERT INTO public.user_preferences (user_id)
    VALUES (NEW.id)
    ON CONFLICT (user_id) DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- ##############################################################################
-- SECTION 3: 003_indexes.sql (Performance, GIN & Fuzzy Search Indexes)
-- ##############################################################################

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Metric sorting indexes
CREATE INDEX IF NOT EXISTS idx_variants_cost_per_g 
    ON product_variants (cost_per_g_protein) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_variants_protein_density 
    ON product_variants (protein_density_pct DESC) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_variants_protein_tier 
    ON product_variants (protein_tier) 
    WHERE is_active = true;

-- Relational foreign key lookup indexes
CREATE INDEX IF NOT EXISTS idx_variants_product_id 
    ON product_variants (product_id);

CREATE INDEX IF NOT EXISTS idx_products_category 
    ON products (category_id) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_products_brand 
    ON products (brand_id) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_red_flags_variant 
    ON variant_red_flags (variant_id);

CREATE INDEX IF NOT EXISTS idx_red_flags_type 
    ON variant_red_flags (flag_type);

-- GIN indexes for array containment & overlap
CREATE INDEX IF NOT EXISTS idx_variants_allergens 
    ON product_variants USING gin (allergens);

CREATE INDEX IF NOT EXISTS idx_variants_dietary_tags 
    ON product_variants USING gin (dietary_tags);

-- Trigram GIN indexes for typo-tolerant fuzzy search
CREATE INDEX IF NOT EXISTS idx_products_name_trgm 
    ON products USING gin (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_variants_name_trgm 
    ON product_variants USING gin (variant_name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_brands_name_trgm 
    ON brands USING gin (name gin_trgm_ops);


-- ##############################################################################
-- SECTION 4: 004_phase1_fixes.sql (Best-Price Metrics, Unique Links, Trigger Optimization)
-- ##############################################################################

ALTER TABLE product_variants
    ADD COLUMN IF NOT EXISTS non_glycemic_polyols_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS best_price_inr NUMERIC(10, 2),
    ADD COLUMN IF NOT EXISTS best_cost_per_g_protein NUMERIC(10, 2);

CREATE INDEX IF NOT EXISTS idx_variants_best_cost_per_g
    ON product_variants (best_cost_per_g_protein)
    WHERE is_active = true;

-- Ensure one redirect link per (variant, platform)
DELETE FROM redirect_links r
USING (
    SELECT id,
           ROW_NUMBER() OVER (PARTITION BY variant_id, platform ORDER BY created_at DESC, id) AS rn
    FROM redirect_links
) ranked
WHERE r.id = ranked.id
  AND ranked.rn > 1;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'redirect_links_variant_platform_key'
    ) THEN
        ALTER TABLE redirect_links
            ADD CONSTRAINT redirect_links_variant_platform_key UNIQUE (variant_id, platform);
    END IF;
END $$;

DROP INDEX IF EXISTS idx_redirect_platform;

-- Trigger optimization: only fire on actual profile or email changes
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT OR UPDATE OF email, raw_user_meta_data ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();


-- ##############################################################################
-- SECTION 5: 005_prices_availability.sql (Price History & Availability)
-- ##############################################################################

ALTER TABLE redirect_links
    ADD COLUMN IF NOT EXISTS external_id TEXT,
    ADD COLUMN IF NOT EXISTS in_stock BOOLEAN;

-- Price history table
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL CHECK (platform IN ('amazon', 'blinkit', 'zepto', 'instamart', 'd2c')),
    price_inr NUMERIC(10, 2),
    in_stock BOOLEAN,
    source TEXT NOT NULL DEFAULT 'poller',
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_price_history_variant_platform_time
    ON price_history (variant_id, platform, recorded_at DESC);

ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read on price_history" ON price_history;
CREATE POLICY "Allow public read on price_history"
    ON price_history FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on price_history" ON price_history;
CREATE POLICY "Allow service_role full access on price_history"
    ON price_history FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Crowd-sourced availability reports
CREATE TABLE IF NOT EXISTS availability_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL CHECK (platform IN ('blinkit', 'zepto', 'instamart')),
    pincode TEXT NOT NULL CHECK (pincode ~ '^[1-9][0-9]{5}$'),
    is_available BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_availability_reports_lookup
    ON availability_reports (variant_id, platform, created_at DESC);

ALTER TABLE availability_reports ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read on availability_reports" ON availability_reports;
CREATE POLICY "Allow public read on availability_reports"
    ON availability_reports FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow public insert on availability_reports" ON availability_reports;
CREATE POLICY "Allow public insert on availability_reports"
    ON availability_reports FOR INSERT
    WITH CHECK (created_at >= NOW() - INTERVAL '1 minute');

DROP POLICY IF EXISTS "Allow service_role full access on availability_reports" ON availability_reports;
CREATE POLICY "Allow service_role full access on availability_reports"
    ON availability_reports FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Availability summary view (last 30 days per 3-digit pincode area)
CREATE OR REPLACE VIEW availability_summary
WITH (security_invoker = true) AS
SELECT
    variant_id,
    platform,
    LEFT(pincode, 3) AS area_code,
    COUNT(*) FILTER (WHERE is_available) AS yes_count,
    COUNT(*) FILTER (WHERE NOT is_available) AS no_count,
    MAX(created_at) AS last_reported_at
FROM availability_reports
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY variant_id, platform, LEFT(pincode, 3);


-- ##############################################################################
-- SECTION 6: 006_api_grants.sql (Data API Permissions)
-- ##############################################################################

GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;

GRANT SELECT ON public.brands TO anon, authenticated;
GRANT ALL ON public.brands TO service_role;

GRANT SELECT ON public.categories TO anon, authenticated;
GRANT ALL ON public.categories TO service_role;

GRANT SELECT ON public.products TO anon, authenticated;
GRANT ALL ON public.products TO service_role;

GRANT SELECT ON public.product_variants TO anon, authenticated;
GRANT ALL ON public.product_variants TO service_role;

GRANT SELECT ON public.variant_red_flags TO anon, authenticated;
GRANT ALL ON public.variant_red_flags TO service_role;

GRANT SELECT ON public.redirect_links TO anon, authenticated;
GRANT ALL ON public.redirect_links TO service_role;

GRANT SELECT ON public.price_history TO anon, authenticated;
GRANT ALL ON public.price_history TO service_role;

GRANT SELECT, INSERT ON public.availability_reports TO anon, authenticated;
GRANT ALL ON public.availability_reports TO service_role;

GRANT SELECT, UPDATE ON public.users TO authenticated;
GRANT ALL ON public.users TO service_role;

GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO authenticated;
GRANT ALL ON public.user_preferences TO service_role;

GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_favorites TO authenticated;
GRANT ALL ON public.user_favorites TO service_role;

GRANT SELECT ON public.availability_summary TO anon, authenticated, service_role;


-- ##############################################################################
-- SECTION 7: 007_seed_categories.sql (Initial Category Population)
-- ##############################################################################

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Protein Powders',
        'protein-powders',
        'Whey isolates, concentrates, plant protein blends, and casein powders.',
        '🥛',
        1
    ),
    (
        'Protein Bars',
        'protein-bars',
        'On-the-go snack bars analyzed for hidden sugars, maltitol, and protein density.',
        '🍫',
        2
    ),
    (
        'RTD Drinks',
        'rtd-drinks',
        'Ready-to-drink high protein milkshakes, lassi, buttermilk, and greek yogurt.',
        '🥤',
        3
    ),
    (
        'Savory Snacks',
        'savory-snacks',
        'Protein chips, namkeen mixtures, crisps, and roasted savory protein bites.',
        '🥨',
        4
    ),
    (
        'Peanut Butter & Spreads',
        'protein-spreads',
        'High-protein peanut butters and nut spreads checked for added sugar, palm oil, and protein per spoon.',
        '🥜',
        5
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;

-- ##############################################################################
-- SECTION 8: 008_variant_flags_breakfast.sql (Variant Flags & Breakfast Cereals)
-- ##############################################################################

ALTER TABLE public.product_variants 
ADD COLUMN IF NOT EXISTS is_combo boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS is_available boolean DEFAULT true;

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Breakfast & Cereals',
        'breakfast-cereals',
        'High-protein muesli, breakfast cereals, protein oats, and morning granola bowls.',
        '🥣',
        6
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;

-- ##############################################################################
-- SECTION 9: 009_dairy_category.sql (Dairy Category Addition)
-- ##############################################################################

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Dairy',
        'dairy',
        'High-protein paneer, Greek yogurt, fresh curd, and everyday dairy staples.',
        '🧀',
        7
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;

-- ##############################################################################
-- SECTION 10: 010_vegan_cookies.sql (Vegan Flag & Cookies & Baked Category)
-- ##############################################################################

ALTER TABLE public.products 
ADD COLUMN IF NOT EXISTS is_vegan boolean NOT NULL DEFAULT false;

CREATE INDEX IF NOT EXISTS idx_products_is_vegan ON public.products (is_vegan);

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Cookies & Baked',
        'cookies-baked',
        'High-protein cookies, brownies, baked snacks, and confectionery.',
        '🍪',
        8
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;


