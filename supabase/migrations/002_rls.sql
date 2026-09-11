-- ==============================================================================
-- 002_rls.sql: Row-Level Security (RLS) & User Profile Trigger
-- ==============================================================================

-- Enable RLS across all tables
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE variant_red_flags ENABLE ROW LEVEL SECURITY;
ALTER TABLE redirect_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------------------
-- 1. CATALOG TABLES: Public Read (Anon + Authenticated), Write via Service Role
-- ------------------------------------------------------------------------------

-- BRANDS
CREATE POLICY "Allow public read on brands"
    ON brands FOR SELECT
    USING (true);

CREATE POLICY "Allow service_role full access on brands"
    ON brands FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- CATEGORIES
CREATE POLICY "Allow public read on categories"
    ON categories FOR SELECT
    USING (true);

CREATE POLICY "Allow service_role full access on categories"
    ON categories FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- PRODUCTS
CREATE POLICY "Allow public read on active products"
    ON products FOR SELECT
    USING (is_active = true);

CREATE POLICY "Allow service_role full access on products"
    ON products FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- PRODUCT_VARIANTS
CREATE POLICY "Allow public read on active product_variants"
    ON product_variants FOR SELECT
    USING (is_active = true);

CREATE POLICY "Allow service_role full access on product_variants"
    ON product_variants FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- VARIANT_RED_FLAGS
CREATE POLICY "Allow public read on variant_red_flags"
    ON variant_red_flags FOR SELECT
    USING (true);

CREATE POLICY "Allow service_role full access on variant_red_flags"
    ON variant_red_flags FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- REDIRECT_LINKS
CREATE POLICY "Allow public read on redirect_links"
    ON redirect_links FOR SELECT
    USING (true);

CREATE POLICY "Allow service_role full access on redirect_links"
    ON redirect_links FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 2. USER TABLES: User-Scoped CRUD via auth.uid()
-- ------------------------------------------------------------------------------

-- USERS
CREATE POLICY "Users can read their own profile"
    ON users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Allow service_role full access on users"
    ON users FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- USER_PREFERENCES
CREATE POLICY "Users can read own preferences"
    ON user_preferences FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own preferences"
    ON user_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences"
    ON user_preferences FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own preferences"
    ON user_preferences FOR DELETE
    USING (auth.uid() = user_id);

CREATE POLICY "Allow service_role full access on user_preferences"
    ON user_preferences FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- USER_FAVORITES
CREATE POLICY "Users can read own favorites"
    ON user_favorites FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can add own favorites"
    ON user_favorites FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove own favorites"
    ON user_favorites FOR DELETE
    USING (auth.uid() = user_id);

CREATE POLICY "Allow service_role full access on user_favorites"
    ON user_favorites FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 3. AUTOMATED USER PROFILE SYNCHRONIZATION TRIGGER
-- ------------------------------------------------------------------------------
-- Automatically creates a corresponding row in public.users when a user signs up via Supabase Auth
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

-- Drop trigger if already exists and recreate
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT OR UPDATE ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();
