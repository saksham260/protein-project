-- ==============================================================================
-- 014_audit_fixes.sql: Fixes from the 2026-11-01 audit
--   * availability reports: raw rows (full pincodes) become private, one area can't be flooded
--   * outbound_clicks: anonymous count of clicks through to stores
--   * delete_my_account: lets a signed-in person delete their own account
--   * handle_new_user: fixed search_path, because it runs with raised privileges
-- Safe to run more than once.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. AVAILABILITY: only the district-level summary stays public
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Allow public read on availability_reports" ON availability_reports;
REVOKE SELECT ON public.availability_reports FROM anon, authenticated;

-- The view must now run as its owner, or visitors could no longer read the summary.
-- It exposes only counts per postal district, never a pincode.
ALTER VIEW public.availability_summary SET (security_invoker = false);
GRANT SELECT ON public.availability_summary TO anon, authenticated;

-- Without accounts there's no per-person limit, so cap reports per product, platform and district.
CREATE OR REPLACE FUNCTION public.limit_availability_reports()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    recent_reports INTEGER;
BEGIN
    SELECT COUNT(*) INTO recent_reports
    FROM public.availability_reports
    WHERE variant_id = NEW.variant_id
      AND platform = NEW.platform
      AND LEFT(pincode, 3) = LEFT(NEW.pincode, 3)
      AND created_at >= NOW() - INTERVAL '1 hour';

    IF recent_reports >= 20 THEN
        RAISE EXCEPTION 'Too many availability reports for this product and area';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_availability_report ON public.availability_reports;
CREATE TRIGGER on_availability_report
    BEFORE INSERT ON public.availability_reports
    FOR EACH ROW
    EXECUTE FUNCTION public.limit_availability_reports();

-- ------------------------------------------------------------------------------
-- 2. OUTBOUND_CLICKS: which products and stores people click through to
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS outbound_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    variant_id UUID REFERENCES product_variants(id) ON DELETE SET NULL,
    platform TEXT NOT NULL CHECK (platform IN ('amazon', 'blinkit', 'zepto', 'instamart', 'd2c')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_outbound_clicks_product_time
    ON outbound_clicks (product_id, created_at DESC);

ALTER TABLE outbound_clicks ENABLE ROW LEVEL SECURITY;

-- Anyone may add a click, but only with a server-side timestamp. Nobody but the service role can read them.
DROP POLICY IF EXISTS "Allow public insert on outbound_clicks" ON outbound_clicks;
CREATE POLICY "Allow public insert on outbound_clicks"
    ON outbound_clicks FOR INSERT
    WITH CHECK (created_at >= NOW() - INTERVAL '1 minute');

DROP POLICY IF EXISTS "Allow service_role full access on outbound_clicks" ON outbound_clicks;
CREATE POLICY "Allow service_role full access on outbound_clicks"
    ON outbound_clicks FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

GRANT INSERT ON public.outbound_clicks TO anon, authenticated;
GRANT ALL ON public.outbound_clicks TO service_role;

-- ------------------------------------------------------------------------------
-- 3. DELETE_MY_ACCOUNT: removes the auth user; their rows cascade from there
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.delete_my_account()
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
    IF auth.uid() IS NULL THEN
        RAISE EXCEPTION 'Not signed in';
    END IF;

    DELETE FROM auth.users WHERE id = auth.uid();
END;
$$;

REVOKE ALL ON FUNCTION public.delete_my_account() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.delete_my_account() TO authenticated;

-- ------------------------------------------------------------------------------
-- 4. HANDLE_NEW_USER: every table it touches is already schema-qualified
-- ------------------------------------------------------------------------------
ALTER FUNCTION public.handle_new_user() SET search_path = '';
