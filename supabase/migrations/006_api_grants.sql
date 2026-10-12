-- ==============================================================================
-- 006_api_grants.sql: Explicit Data API Table Grants
-- Required by Supabase 2026+ where public tables are not auto-exposed to the API.
-- (Grants permit table-level access; RLS policies govern row-level permissions).
-- Safe to re-run.
-- ==============================================================================

-- 1. Ensure API roles have schema usage
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;

-- 2. Catalog tables (Public read via API, managed via service_role)
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

-- 3. Crowd-sourced availability reports (Anonymous read + insert)
GRANT SELECT, INSERT ON public.availability_reports TO anon, authenticated;
GRANT ALL ON public.availability_reports TO service_role;

-- 4. User profile, preferences and favorites (Scoped via RLS auth.uid())
GRANT SELECT, UPDATE ON public.users TO authenticated;
GRANT ALL ON public.users TO service_role;

GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_preferences TO authenticated;
GRANT ALL ON public.user_preferences TO service_role;

GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_favorites TO authenticated;
GRANT ALL ON public.user_favorites TO service_role;

-- 5. Availability summary view
GRANT SELECT ON public.availability_summary TO anon, authenticated, service_role;
