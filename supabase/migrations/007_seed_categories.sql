-- ==============================================================================
-- 007_seed_categories.sql: Standard Category Seed
-- Synchronized with protein-web/src/lib/constants.ts
-- Safe to re-run.
-- ==============================================================================

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Protein Powders',
        'protein-powders',
        'Whey isolates, concentrates, plant protein blends, and casein powders.',
        '🥛',
        1
    ),
    (
        'Protein Bars',
        'protein-bars',
        'On-the-go snack bars analyzed for hidden sugars, maltitol, and protein density.',
        '🍫',
        2
    ),
    (
        'RTD Drinks',
        'rtd-drinks',
        'Ready-to-drink high protein milkshakes, lassi, buttermilk, and greek yogurt.',
        '🥤',
        3
    ),
    (
        'Savory Snacks',
        'savory-snacks',
        'Protein chips, namkeen mixtures, crisps, and roasted savory protein bites.',
        '🥨',
        4
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;
