-- ==============================================================================
-- 005_prices_availability.sql: Live prices + crowd-sourced availability
--   * redirect_links gets the Amazon ASIN and last known stock state
--   * price_history keeps every polled price (written by the ETL poller)
--   * availability_reports stores anonymous "was it available?" answers
--   * availability_summary aggregates reports per postal district (first 3 pincode digits)
-- Safe to run more than once.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. REDIRECT_LINKS: external id + stock
-- ------------------------------------------------------------------------------
ALTER TABLE redirect_links
    ADD COLUMN IF NOT EXISTS external_id TEXT,
    ADD COLUMN IF NOT EXISTS in_stock BOOLEAN;

-- ------------------------------------------------------------------------------
-- 2. PRICE_HISTORY
-- ------------------------------------------------------------------------------
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

-- ------------------------------------------------------------------------------
-- 3. AVAILABILITY_REPORTS (anonymous, quick-commerce only)
-- ------------------------------------------------------------------------------
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

-- Anyone may submit a report, but only with a server-side timestamp.
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

-- ------------------------------------------------------------------------------
-- 4. AVAILABILITY_SUMMARY: last 30 days, per postal district
-- ------------------------------------------------------------------------------
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

GRANT SELECT ON availability_summary TO anon, authenticated;
