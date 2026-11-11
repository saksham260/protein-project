raise SystemExit("RETIRED after the 2026-11-09 data incident: this script wrote to live Supabase without the uploader's checks (picked products by list position / hard-deleted rows / stamped fake price check times). Use scripts/seed.py --slug <slug> to upsert and scripts/retire_products.py to retire.")
"""Sync Wave 1 (35 High-Protein Dairy & Everyday Staples) to live Supabase PostgreSQL."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "protein-etl"))
from src.models import slugify

def sync_wave_1():
    cfg = dotenv_values(REPO / "protein-etl" / ".env")
    url = cfg.get("SUPABASE_URL")
    key = cfg.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL or SUPABASE_SERVICE_KEY not set in protein-etl/.env")
        sys.exit(1)

    client = create_client(url, key)
    print("Connected to Supabase.")

    seed_file = REPO / "protein-etl" / "data" / "seed_products.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        all_products = json.load(f)

    wave_1_products = all_products[-35:]
    print(f"Loaded {len(all_products)} total products; syncing Wave 1: {len(wave_1_products)} products.")

    # Cache categories
    cat_res = client.table("categories").select("id, slug").execute()
    cat_map = {c["slug"]: c["id"] for c in cat_res.data}

    success_count = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for idx, p in enumerate(wave_1_products, 1):
        brand_name = p["brand_name"]
        brand_slug = slugify(brand_name)
        cat_slug = p["category_slug"]
        cat_id = cat_map.get(cat_slug)

        if not cat_id:
            print(f"[{idx}/35] Category not found: {cat_slug}")
            continue

        # 1. Upsert Brand
        brand_res = client.table("brands").upsert(
            {"name": brand_name, "slug": brand_slug},
            on_conflict="slug"
        ).execute()
        brand_id = brand_res.data[0]["id"]

        # 2. Upsert Product
        prod_payload = {
            "brand_id": brand_id,
            "category_id": cat_id,
            "name": p["name"],
            "slug": p["slug"],
            "description": p.get("description"),
            "image_url": p.get("image_url"),
            "is_active": True,
        }
        prod_res = client.table("products").upsert(
            prod_payload,
            on_conflict="slug"
        ).execute()
        product_id = prod_res.data[0]["id"]

        # 3. Upsert Variants
        for v in p.get("variants", []):
            v_slug = v.get("slug")
            if not v_slug.startswith(f"{p['slug']}-"):
                v_slug = f"{p['slug']}-{v_slug}"

            nut = v.get("nutrition") or {}
            metrics = v.get("computed_metrics") or {}
            profile = v.get("protein_profile") or {}

            var_payload = {
                "product_id": product_id,
                "variant_name": v.get("variant_name") or p["name"],
                "slug": v_slug,
                "sku": v.get("sku"),
                "barcode_ean": v.get("barcode_ean"),
                "mrp_inr": v.get("mrp_inr"),
                "net_weight_g": v.get("net_weight_g"),
                "serving_size_g": v.get("serving_size_g"),
                "servings_per_pack": v.get("servings_per_pack"),
                "serving_size_label": v.get("serving_size_label"),
                "calories_kcal": nut.get("calories_kcal"),
                "protein_g": nut.get("protein_g"),
                "total_fat_g": nut.get("total_fat_g"),
                "saturated_fat_g": nut.get("saturated_fat_g"),
                "trans_fat_g": nut.get("trans_fat_g"),
                "cholesterol_mg": nut.get("cholesterol_mg"),
                "total_carbs_g": nut.get("total_carbs_g"),
                "dietary_fiber_g": nut.get("dietary_fiber_g"),
                "total_sugars_g": nut.get("total_sugars_g"),
                "added_sugars_g": nut.get("added_sugars_g"),
                "sodium_mg": nut.get("sodium_mg"),
                "non_glycemic_polyols_g": nut.get("non_glycemic_polyols_g"),
                "additional_nutrients": nut.get("additional_nutrients", {}),
                "ingredient_list": v.get("ingredient_list", []),
                "ingredient_deck_raw": v.get("ingredient_deck_raw", []),
                "allergens": v.get("allergens", []),
                "dietary_tags": v.get("dietary_tags", []),
                "primary_protein_source": profile.get("primary_protein_source"),
                "protein_tier": profile.get("protein_tier"),
                "has_added_free_form_aminos": profile.get("has_added_free_form_aminos", False),
                "cost_per_g_protein": metrics.get("cost_per_g_protein"),
                "best_price_inr": metrics.get("best_price_inr"),
                "best_cost_per_g_protein": metrics.get("best_cost_per_g_protein"),
                "protein_density_pct": metrics.get("protein_density_pct"),
                "true_net_carbs_g": metrics.get("true_net_carbs_g"),
                "image_url": v.get("image_url") or p.get("image_url"),
                "is_active": True,
                "last_verified_at": now_iso,
            }

            var_res = client.table("product_variants").upsert(
                var_payload,
                on_conflict="slug"
            ).execute()
            variant_id = var_res.data[0]["id"]

            # Red Flags
            client.table("variant_red_flags").delete().eq("variant_id", variant_id).execute()
            red_flags = v.get("red_flags") or []
            if red_flags:
                flag_rows = [
                    {
                        "variant_id": variant_id,
                        "flag_type": rf.get("flag_type"),
                        "flag_severity": rf.get("flag_severity"),
                        "flag_label": rf.get("flag_label"),
                        "flag_description": rf.get("flag_description"),
                        "matched_ingredient": rf.get("matched_ingredient"),
                        "ins_number": rf.get("ins_number"),
                    }
                    for rf in red_flags
                ]
                client.table("variant_red_flags").insert(flag_rows).execute()

            # Redirect Links
            links = v.get("redirect_links") or []
            if links:
                links_payload = [
                    {
                        "variant_id": variant_id,
                        "platform": rl.get("platform"),
                        "url": rl.get("url"),
                        "platform_price_inr": rl.get("platform_price_inr"),
                        "price_last_checked": now_iso,
                    }
                    for rl in links
                ]
                client.table("redirect_links").upsert(
                    links_payload,
                    on_conflict="variant_id,platform"
                ).execute()

        success_count += 1
        print(f"[{idx}/35] Synced: {brand_name} - {p['name']} -> product_id={product_id}")

    print("\n" + "="*50)
    print(f"Supabase Sync Complete: {success_count}/35 products successfully upserted.")

if __name__ == "__main__":
    sync_wave_1()
