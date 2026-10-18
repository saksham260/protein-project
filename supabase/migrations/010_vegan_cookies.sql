-- ==============================================================================
-- 010_vegan_cookies.sql: Vegan Flag & Cookies & Baked Category
-- Safe to re-run.
-- ==============================================================================

-- 1. Add is_vegan to products
ALTER TABLE public.products 
ADD COLUMN IF NOT EXISTS is_vegan boolean NOT NULL DEFAULT false;

CREATE INDEX IF NOT EXISTS idx_products_is_vegan ON public.products (is_vegan);

-- 2. Insert Cookies & Baked category
INSERT INTO public.categories (name, slug, description, icon, display_order)
VALUES
    (
        'Cookies & Baked',
        'cookies-baked',
        'High-protein cookies, brownies, baked snacks, and confectionery.',
        '🍪',
        8
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order;
