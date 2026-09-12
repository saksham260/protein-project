-- ==============================================================================
-- 004_phase1_fixes.sql: Phase 1 review fixes
--   * Store polyols + best-price metrics on variants
--   * One redirect link per (variant, platform) so re-uploads update instead of duplicating
--   * Profile sync trigger only fires on sign-up or profile changes, not every login
-- Safe to run more than once.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. PRODUCT_VARIANTS: new columns
-- ------------------------------------------------------------------------------
ALTER TABLE product_variants
    ADD COLUMN IF NOT EXISTS non_glycemic_polyols_g NUMERIC(10, 2) NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS best_price_inr NUMERIC(10, 2),
    ADD COLUMN IF NOT EXISTS best_cost_per_g_protein NUMERIC(10, 2);

CREATE INDEX IF NOT EXISTS idx_variants_best_cost_per_g
    ON product_variants (best_cost_per_g_protein)
    WHERE is_active = true;

-- ------------------------------------------------------------------------------
-- 2. REDIRECT_LINKS: remove duplicates, then enforce one link per platform
-- ------------------------------------------------------------------------------
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

-- The unique constraint's index already covers (variant_id, platform) lookups.
DROP INDEX IF EXISTS idx_redirect_platform;

-- ------------------------------------------------------------------------------
-- 3. AUTH PROFILE SYNC: skip updates that only touch login timestamps
-- ------------------------------------------------------------------------------
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT OR UPDATE OF email, raw_user_meta_data ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();
