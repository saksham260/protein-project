-- ==============================================================================
-- 001_schema.sql: Core Database Schema for The Protein Discovery Engine
-- ==============================================================================

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
-- 1. BRANDS
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
-- 2. CATEGORIES
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
-- 3. PRODUCTS (Parent Products)
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
-- 4. PRODUCT_VARIANTS (Atomic Unit of Truth)
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
-- 5. VARIANT_RED_FLAGS
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
-- 6. REDIRECT_LINKS
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
-- 7. USERS (Mirrors Supabase Auth auth.users)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 8. USER_PREFERENCES
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
-- 9. USER_FAVORITES
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, variant_id)
);
