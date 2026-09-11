-- ==============================================================================
-- 003_indexes.sql: Performance, Array (GIN), and Fuzzy Text Search Indexes
-- ==============================================================================

-- Enable pg_trgm for trigram-based fuzzy search on product/variant names
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ------------------------------------------------------------------------------
-- 1. B-TREE INDEXES: Sorting, Joining, and Metric Queries
-- ------------------------------------------------------------------------------

-- Metric sorting indexes (filtered by active variants)
CREATE INDEX IF NOT EXISTS idx_variants_cost_per_g 
    ON product_variants (cost_per_g_protein) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_variants_protein_density 
    ON product_variants (protein_density_pct DESC) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_variants_protein_tier 
    ON product_variants (protein_tier) 
    WHERE is_active = true;

-- Relational foreign key lookup indexes
CREATE INDEX IF NOT EXISTS idx_variants_product_id 
    ON product_variants (product_id);

CREATE INDEX IF NOT EXISTS idx_products_category 
    ON products (category_id) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_products_brand 
    ON products (brand_id) 
    WHERE is_active = true;

CREATE INDEX IF NOT EXISTS idx_red_flags_variant 
    ON variant_red_flags (variant_id);

CREATE INDEX IF NOT EXISTS idx_red_flags_type 
    ON variant_red_flags (flag_type);

CREATE INDEX IF NOT EXISTS idx_redirect_platform 
    ON redirect_links (variant_id, platform);

-- ------------------------------------------------------------------------------
-- 2. GIN INDEXES: High-Speed Array Containment & Overlap
-- ------------------------------------------------------------------------------

-- Crucial for recommendation engine: NOT (pv.allergens && user_prefs.allergens)
CREATE INDEX IF NOT EXISTS idx_variants_allergens 
    ON product_variants USING gin (allergens);

-- Crucial for category & dietary filter chips (Vegan, Keto, Gluten-Free)
CREATE INDEX IF NOT EXISTS idx_variants_dietary_tags 
    ON product_variants USING gin (dietary_tags);

-- ------------------------------------------------------------------------------
-- 3. TRIGRAM GIN INDEXES: Substring & Typo-Tolerant Search
-- ------------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_products_name_trgm 
    ON products USING gin (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_variants_name_trgm 
    ON product_variants USING gin (variant_name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_brands_name_trgm 
    ON brands USING gin (name gin_trgm_ops);
