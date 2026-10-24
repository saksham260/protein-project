-- ==============================================================================
-- 012_user_searches.sql: Per-user search history ("Recent searches" in the search bar)
--   One row per person per distinct search; searching the same thing again just
--   refreshes its time. Each person can only see and change their own rows.
-- Safe to run more than once.
-- ==============================================================================

CREATE TABLE IF NOT EXISTS user_searches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL CHECK (char_length(query) BETWEEN 2 AND 80),
    query_key TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, query_key)
);

CREATE INDEX IF NOT EXISTS idx_user_searches_user_time
    ON user_searches (user_id, created_at DESC);

ALTER TABLE user_searches ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can read own searches" ON user_searches;
CREATE POLICY "Users can read own searches"
    ON user_searches FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can add own searches" ON user_searches;
CREATE POLICY "Users can add own searches"
    ON user_searches FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can refresh own searches" ON user_searches;
CREATE POLICY "Users can refresh own searches"
    ON user_searches FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own searches" ON user_searches;
CREATE POLICY "Users can delete own searches"
    ON user_searches FOR DELETE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Allow service_role full access on user_searches" ON user_searches;
CREATE POLICY "Allow service_role full access on user_searches"
    ON user_searches FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Data API permissions (see 006_api_grants.sql); RLS above limits rows to the owner.
GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_searches TO authenticated;
GRANT ALL ON public.user_searches TO service_role;
