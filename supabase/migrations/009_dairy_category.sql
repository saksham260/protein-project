-- ==============================================================================
-- 009_dairy_category.sql: Dairy Category Addition
-- Safe to re-run.
-- ==============================================================================

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Dairy',
        'dairy',
        'High-protein paneer, Greek yogurt, fresh curd, and everyday dairy staples.',
        '🧀',
        7
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;
