-- ==============================================================================
-- 016_data_incident_repair.sql: repair data written by the batch/wave upload scripts
-- (2026-11-02 / 2026-11-03). See documentation/data-quality/2026-11-09-data-incident.md.
--
--   1. Fake "price checked" times. The upload scripts stamped every link "checked now" at
--      upload time, even links with no price. They wrote the same timestamp to the
--      variant's last_verified_at, which the price pollers never touch, so an exact match
--      identifies an upload stamp. Those are cleared (unknown age). The next poller run
--      sets real times on the prices it can confirm.
--   2. Hand-labelled "Tier 1" on products whose protein source is not an isolate or
--      hydrolysate (milk, paneer, cheese, concentrates, blends).
--
-- Run the two PREVIEW queries first and check the counts. Safe to run more than once.
-- Restoring the deleted products is NOT done here: see the incident note.
-- ==============================================================================

-- PREVIEW 1: upload-stamped check times (expect ~2,800, most of them with no price)
-- SELECT COUNT(*) AS stamped, COUNT(*) FILTER (WHERE rl.platform_price_inr IS NULL) AS stamped_without_price
-- FROM redirect_links rl JOIN product_variants pv ON pv.id = rl.variant_id
-- WHERE rl.price_last_checked IS NOT NULL
--   AND (rl.platform_price_inr IS NULL OR rl.price_last_checked = pv.last_verified_at);

-- PREVIEW 2: Tier 1 labels the protein source does not support
-- SELECT pv.slug, pv.primary_protein_source, pv.protein_tier
-- FROM product_variants pv
-- WHERE pv.protein_tier LIKE 'Tier 1%'
--   AND COALESCE(pv.primary_protein_source, '') !~* '(isolate|hydroly)';

BEGIN;

-- 1. A check time on a link with no price means nothing.
UPDATE redirect_links
SET price_last_checked = NULL
WHERE platform_price_inr IS NULL
  AND price_last_checked IS NOT NULL;

-- 1b. Priced links stamped by an upload rather than a poller.
UPDATE redirect_links rl
SET price_last_checked = NULL
FROM product_variants pv
WHERE pv.id = rl.variant_id
  AND rl.price_last_checked IS NOT NULL
  AND rl.price_last_checked = pv.last_verified_at;

-- 2. Tier 1 without an isolate/hydrolysate source: plant blends fall to Tier 3
--    (weakest link), everything else (milk, paneer, cheese, curd, concentrates, casein) to Tier 2.
UPDATE product_variants
SET protein_tier = CASE
        WHEN primary_protein_source ~* '(soy|soya|pea|rice|plant|peanut)'
            THEN 'Tier 3 – Plant & Yeast (Pea/Rice/Soy/Yeast/Peanut)'
        ELSE 'Tier 2 – Concentrate/Casein/Milk/Egg'
    END
WHERE protein_tier LIKE 'Tier 1%'
  AND COALESCE(primary_protein_source, '') !~* '(isolate|hydroly)';

COMMIT;
