-- ==============================================================================
-- verify.sql: Verification Script for The Protein Discovery Engine Database
-- Paste and run in Supabase SQL Editor.
-- Returns an audit table confirming all tables, RLS status, policies, and row counts.
-- ==============================================================================

WITH table_stats AS (
    SELECT
        c.relname AS object_name,
        CASE c.relkind
            WHEN 'r' THEN 'table'
            WHEN 'v' THEN 'view'
            ELSE 'other'
        END AS object_type,
        c.relrowsecurity AS rls_enabled,
        (
            SELECT COUNT(*)
            FROM pg_policy p
            WHERE p.polrelid = c.oid
        ) AS policy_count,
        (
            SELECT string_agg(DISTINCT privilege_type, ', ' ORDER BY privilege_type)
            FROM information_schema.role_table_grants g
            WHERE g.table_schema = 'public'
              AND g.table_name = c.relname
              AND g.grantee = 'anon'
        ) AS anon_privileges,
        (
            SELECT string_agg(DISTINCT privilege_type, ', ' ORDER BY privilege_type)
            FROM information_schema.role_table_grants g
            WHERE g.table_schema = 'public'
              AND g.table_name = c.relname
              AND g.grantee = 'authenticated'
        ) AS auth_privileges
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public'
      AND c.relname IN (
          'brands',
          'categories',
          'products',
          'product_variants',
          'variant_red_flags',
          'redirect_links',
          'price_history',
          'availability_reports',
          'users',
          'user_preferences',
          'user_favorites',
          'availability_summary'
      )
)
SELECT
    t.object_name,
    t.object_type,
    CASE 
        WHEN t.object_type = 'view' THEN 'N/A (view)'
        WHEN t.rls_enabled THEN 'ENABLED'
        ELSE 'DISABLED (WARNING)'
    END AS rls_status,
    t.policy_count,
    COALESCE(t.anon_privileges, 'NONE') AS anon_grants,
    COALESCE(t.auth_privileges, 'NONE') AS authenticated_grants,
    CASE t.object_name
        WHEN 'brands' THEN (SELECT COUNT(*)::text FROM public.brands)
        WHEN 'categories' THEN (SELECT COUNT(*)::text FROM public.categories)
        WHEN 'products' THEN (SELECT COUNT(*)::text FROM public.products)
        WHEN 'product_variants' THEN (SELECT COUNT(*)::text FROM public.product_variants)
        WHEN 'variant_red_flags' THEN (SELECT COUNT(*)::text FROM public.variant_red_flags)
        WHEN 'redirect_links' THEN (SELECT COUNT(*)::text FROM public.redirect_links)
        WHEN 'price_history' THEN (SELECT COUNT(*)::text FROM public.price_history)
        WHEN 'availability_reports' THEN (SELECT COUNT(*)::text FROM public.availability_reports)
        WHEN 'users' THEN (SELECT COUNT(*)::text FROM public.users)
        WHEN 'user_preferences' THEN (SELECT COUNT(*)::text FROM public.user_preferences)
        WHEN 'user_favorites' THEN (SELECT COUNT(*)::text FROM public.user_favorites)
        ELSE 'N/A'
    END AS row_count
FROM table_stats t
ORDER BY t.object_type DESC, t.object_name ASC;
