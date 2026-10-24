-- ==============================================================================
-- 011_user_activity.sql: Per-user activity (product views + clicks to a purchase page)
--   Powers the "Suggested for You" section on the home page (only shown when logged in).
--   Each person can only see, add and delete their own rows.
-- Safe to run more than once.
-- ==============================================================================

CREATE TABLE IF NOT EXISTS user_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_id UUID REFERENCES product_variants(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('view', 'purchase_click')),
    platform TEXT CHECK (platform IN ('amazon', 'blinkit', 'zepto', 'instamart', 'd2c')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_activity_user_time
    ON user_activity (user_id, created_at DESC);

ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can read own activity" ON user_activity;
CREATE POLICY "Users can read own activity"
    ON user_activity FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can add own activity" ON user_activity;
CREATE POLICY "Users can add own activity"
    ON user_activity FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own activity" ON user_activity;
CREATE POLICY "Users can delete own activity"
    ON user_activity FOR DELETE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Allow service_role full access on user_activity" ON user_activity;
CREATE POLICY "Allow service_role full access on user_activity"
    ON user_activity FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Data API permissions (see 006_api_grants.sql); RLS above limits rows to the owner.
GRANT SELECT, INSERT, DELETE ON public.user_activity TO authenticated;
GRANT ALL ON public.user_activity TO service_role;
