-- ==============================================================================
-- 008_variant_flags_breakfast.sql: Variant Flags & Breakfast-Cereals Category
-- Safe to re-run.
-- ==============================================================================

-- 1. Add is_combo and is_available to product_variants
ALTER TABLE public.product_variants 
ADD COLUMN IF NOT EXISTS is_combo boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS is_available boolean DEFAULT true;

-- 2. Insert Breakfast & Cereals category
INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Breakfast & Cereals',
        'breakfast-cereals',
        'High-protein muesli, breakfast cereals, protein oats, and morning granola bowls.',
        '🥣',
        6
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;
