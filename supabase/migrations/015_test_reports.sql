-- ==============================================================================
-- 015_test_reports.sql: Published lab reports linked from product pages
--   Rows are added by hand (Supabase table editor or service role). Each one must link
--   to the original report, and applies only to the batch tested.
-- Safe to run more than once.
-- ==============================================================================

CREATE TABLE IF NOT EXISTS test_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    -- Empty when the report covers the product rather than one pack size or flavour.
    variant_id UUID REFERENCES product_variants(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL CHECK (source_type IN ('independent', 'brand')),
    source_name TEXT NOT NULL,
    lab_name TEXT,
    batch_number TEXT,
    tested_on DATE NOT NULL,
    result TEXT NOT NULL CHECK (result IN ('pass', 'partial', 'fail')),
    tested_protein_g_per_100g NUMERIC(6, 2) CHECK (tested_protein_g_per_100g BETWEEN 0 AND 100),
    report_url TEXT NOT NULL CHECK (report_url LIKE 'https://%'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_test_reports_product_time
    ON test_reports (product_id, tested_on DESC);

ALTER TABLE test_reports ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read on test_reports" ON test_reports;
CREATE POLICY "Allow public read on test_reports"
    ON test_reports FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Allow service_role full access on test_reports" ON test_reports;
CREATE POLICY "Allow service_role full access on test_reports"
    ON test_reports FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

GRANT SELECT ON public.test_reports TO anon, authenticated;
GRANT ALL ON public.test_reports TO service_role;
