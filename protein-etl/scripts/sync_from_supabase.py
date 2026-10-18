"""
Sync the full 159 products from Supabase to seedCatalog.json and seed_products.json,
matching the RawSeedProduct schema expected by protein-web/src/lib/data.ts.
"""
import sys, json
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "protein-etl"))
from src.db.supabase_client import SupabaseUploader

u = SupabaseUploader()
res = u.client.table("products").select("*, brand:brands(*), category:categories(*), variants:product_variants(*, redirect_links(*), red_flags:variant_red_flags(*))").order("name").execute()
products = res.data

catalog_products = []
raw_products = []

for p in products:
    brand_name = p["brand"]["name"] if p.get("brand") else ""
    cat_slug = p["category"]["slug"] if p.get("category") else ""
    
    enriched_variants = []
    raw_variants = []
    
    for v in p.get("variants", []):
        nutrition = {
            "calories_kcal": v.get("calories_kcal"),
            "protein_g": v.get("protein_g"),
            "total_fat_g": v.get("total_fat_g"),
            "saturated_fat_g": v.get("saturated_fat_g"),
            "trans_fat_g": v.get("trans_fat_g"),
            "cholesterol_mg": v.get("cholesterol_mg"),
            "total_carbs_g": v.get("total_carbs_g"),
            "dietary_fiber_g": v.get("dietary_fiber_g"),
            "total_sugars_g": v.get("total_sugars_g"),
            "added_sugars_g": v.get("added_sugars_g"),
            "sodium_mg": v.get("sodium_mg"),
            "non_glycemic_polyols_g": v.get("non_glycemic_polyols_g"),
            "additional_nutrients": v.get("additional_nutrients") or {},
        }
        
        # Enriched variant for seedCatalog.json
        enriched_variants.append({
            "variant_name": v.get("variant_name"),
            "slug": v.get("slug"),
            "sku": v.get("sku"),
            "mrp_inr": v.get("mrp_inr"),
            "net_weight_g": v.get("net_weight_g"),
            "serving_size_g": v.get("serving_size_g"),
            "servings_per_pack": v.get("servings_per_pack"),
            "serving_size_label": v.get("serving_size_label"),
            "nutrition": nutrition,
            "ingredient_list": v.get("ingredient_list") or [],
            "ingredient_deck_raw": v.get("ingredient_deck_raw") or [],
            "allergens": v.get("allergens") or [],
            "dietary_tags": v.get("dietary_tags") or [],
            "protein_profile": {
                "primary_protein_source": v.get("primary_protein_source"),
                "protein_tier": v.get("protein_tier"),
                "has_added_free_form_aminos": v.get("has_added_free_form_aminos") or False,
            },
            "computed_metrics": {
                "cost_per_g_protein": v.get("cost_per_g_protein"),
                "best_price_inr": v.get("best_price_inr") or v.get("mrp_inr"),
                "best_cost_per_g_protein": v.get("best_cost_per_g_protein") or v.get("cost_per_g_protein"),
                "protein_density_pct": v.get("protein_density_pct"),
                "true_net_carbs_g": v.get("true_net_carbs_g"),
            },
            "image_url": v.get("image_url"),
            "red_flags": v.get("red_flags") or [],
            "redirect_links": v.get("redirect_links") or [],
            "is_combo": v.get("is_combo", False),
            "is_available": v.get("is_available", True),
        })
        
        # Raw variant for seed_products.json
        raw_variants.append({
            "variant_name": v.get("variant_name"),
            "slug": v.get("slug"),
            "sku": v.get("sku"),
            "mrp_inr": v.get("mrp_inr"),
            "net_weight_g": v.get("net_weight_g"),
            "serving_size_g": v.get("serving_size_g"),
            "servings_per_pack": v.get("servings_per_pack"),
            "nutrition": nutrition,
            "ingredient_list": v.get("ingredient_list") or [],
            "ingredient_deck_raw": v.get("ingredient_deck_raw") or [],
            "allergens": v.get("allergens") or [],
            "dietary_tags": v.get("dietary_tags") or [],
            "image_url": v.get("image_url"),
            "redirect_links": v.get("redirect_links") or [],
            "red_flags": v.get("red_flags") or [],
            "is_combo": v.get("is_combo", False),
            "is_available": v.get("is_available", True),
        })
        
    catalog_products.append({
        "name": p["name"],
        "brand_name": brand_name,
        "category_slug": cat_slug,
        "slug": p["slug"],
        "description": p.get("description"),
        "image_url": p.get("image_url"),
        "variants": enriched_variants
    })
    
    raw_products.append({
        "name": p["name"],
        "brand_name": brand_name,
        "category_slug": cat_slug,
        "slug": p["slug"],
        "description": p.get("description"),
        "image_url": p.get("image_url"),
        "variants": raw_variants
    })

web_seed = REPO / "protein-web" / "src" / "data" / "seedCatalog.json"
web_seed.write_text(json.dumps(catalog_products, indent=2, ensure_ascii=False), encoding="utf-8")

etl_seed = REPO / "protein-etl" / "data" / "seed_products.json"
etl_seed.write_text(json.dumps(raw_products, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Successfully synced {len(catalog_products)} products with full RawSeedProduct structure.")
