-- ==============================================================================
-- 013_new_categories.sql: Mass Gainers, Adult Nutrition, and Staples Categories
-- Safe to re-run.
-- ==============================================================================

INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Mass & Weight Gainers',
        'mass-gainers',
        'High-calorie, high-protein formulations designed for bulking and hardgainers.',
        '🏋️',
        9
    ),
    (
        'Adult & Medical Nutrition',
        'adult-nutrition',
        'Clinical, senior, diabetic-care, and recovery nutrition formulas.',
        '🩺',
        10
    ),
    (
        'High-Protein Staples',
        'staples',
        'High-protein atta, pasta, soya chunks, flour blends, and everyday kitchen essentials.',
        '🌾',
        11
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;
