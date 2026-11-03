import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "protein-etl"))
from src.models import slugify

cfg = dotenv_values(REPO / "protein-etl" / ".env")
client = create_client(cfg["SUPABASE_URL"], cfg["SUPABASE_SERVICE_KEY"])

retired_slugs = json.loads((REPO / "protein-etl" / "scratch" / "batch5_retired_slugs.json").read_text(encoding="utf-8"))
print(f"Removing {len(retired_slugs)} retired duplicate/synthetic slugs from live Supabase...")

for r_slug in retired_slugs:
    res = client.table("products").select("id").eq("slug", r_slug).execute()
    for row in res.data:
        pid = row["id"]
        vres = client.table("product_variants").select("id").eq("product_id", pid).execute()
        for vrow in vres.data:
            vid = vrow["id"]
            client.table("redirect_links").delete().eq("variant_id", vid).execute()
            client.table("variant_red_flags").delete().eq("variant_id", vid).execute()
        client.table("product_variants").delete().eq("product_id", pid).execute()
        client.table("products").delete().eq("id", pid).execute()
        print(f"  [DELETED] {r_slug} (id={pid})")

batch5_slugs = set(json.loads((REPO / "protein-etl" / "scratch" / "batch5_active_slugs.json").read_text(encoding="utf-8")))
seed_catalog = json.loads((REPO / "protein-web" / "src" / "data" / "seedCatalog.json").read_text(encoding="utf-8"))
to_sync = [p for p in seed_catalog if p["slug"] in batch5_slugs]
print(f"Syncing {len(to_sync)} Batch 5 products to live Supabase...")

cat_res = client.table("categories").select("id, slug").execute()
cat_map = {c["slug"]: c["id"] for c in cat_res.data}
now_iso = datetime.now(timezone.utc).isoformat()

for idx, p in enumerate(to_sync, 1):
    brand_name = p.get("brand_name") or (p.get("brand") or {}).get("name")
    brand_slug = slugify(brand_name)
    cat_slug = p.get("category_slug") or (p.get("category") or {}).get("slug")
    cat_id = cat_map[cat_slug]

    brand_res = client.table("brands").upsert({"name": brand_name, "slug": brand_slug}, on_conflict="slug").execute()
    brand_id = brand_res.data[0]["id"]

    prod_res = client.table("products").upsert({
        "brand_id": brand_id,
        "category_id": cat_id,
        "name": p["name"],
        "slug": p["slug"],
        "description": p.get("description"),
        "image_url": p.get("image_url"),
        "is_active": True,
    }, on_conflict="slug").execute()
    product_id = prod_res.data[0]["id"]

    for v in p.get("variants", []):
        v_slug = v.get("slug") or slugify(f"{p['slug']}-{v.get('variant_name', 'default')}")
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
            "calories_kcal": nut.get("calories_kcal", v.get("calories_kcal")),
            "protein_g": nut.get("protein_g", v.get("protein_g")),
            "total_fat_g": nut.get("total_fat_g", v.get("total_fat_g")),
            "saturated_fat_g": nut.get("saturated_fat_g", v.get("saturated_fat_g")),
            "trans_fat_g": nut.get("trans_fat_g", v.get("trans_fat_g")),
            "cholesterol_mg": nut.get("cholesterol_mg", v.get("cholesterol_mg")),
            "total_carbs_g": nut.get("total_carbs_g", v.get("total_carbs_g")),
            "dietary_fiber_g": nut.get("dietary_fiber_g", v.get("dietary_fiber_g")),
            "total_sugars_g": nut.get("total_sugars_g", v.get("total_sugars_g")),
            "added_sugars_g": nut.get("added_sugars_g", v.get("added_sugars_g")),
            "sodium_mg": nut.get("sodium_mg", v.get("sodium_mg")),
            "non_glycemic_polyols_g": nut.get("non_glycemic_polyols_g", v.get("non_glycemic_polyols_g")),
            "additional_nutrients": nut.get("additional_nutrients", v.get("additional_nutrients", {})),
            "ingredient_list": v.get("ingredient_list", []),
            "ingredient_deck_raw": v.get("ingredient_deck_raw", []),
            "allergens": v.get("allergens", []),
            "dietary_tags": v.get("dietary_tags", []),
            "primary_protein_source": profile.get("primary_protein_source", v.get("primary_protein_source")),
            "protein_tier": profile.get("protein_tier", v.get("protein_tier")),
            "has_added_free_form_aminos": profile.get("has_added_free_form_aminos", v.get("has_added_free_form_aminos", False)),
            "cost_per_g_protein": metrics.get("cost_per_g_protein", v.get("cost_per_g_protein")),
            "best_price_inr": metrics.get("best_price_inr", v.get("best_price_inr")),
            "best_cost_per_g_protein": metrics.get("best_cost_per_g_protein", v.get("best_cost_per_g_protein")),
            "protein_density_pct": metrics.get("protein_density_pct", v.get("protein_density_pct")),
            "true_net_carbs_g": metrics.get("true_net_carbs_g", v.get("true_net_carbs_g")),
            "image_url": v.get("image_url") or p.get("image_url"),
            "is_active": True,
            "last_verified_at": now_iso,
        }
        var_res = client.table("product_variants").upsert(var_payload, on_conflict="slug").execute()
        variant_id = var_res.data[0]["id"]

        client.table("variant_red_flags").delete().eq("variant_id", variant_id).execute()
        red_flags = v.get("red_flags") or []
        if red_flags:
            client.table("variant_red_flags").insert([
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
            ]).execute()

        links = v.get("redirect_links") or []
        if links:
            client.table("redirect_links").upsert([
                {
                    "variant_id": variant_id,
                    "platform": rl.get("platform"),
                    "url": rl.get("url"),
                    "platform_price_inr": rl.get("platform_price_inr"),
                    "price_last_checked": now_iso,
                }
                for rl in links
            ], on_conflict="variant_id,platform").execute()

    print(f"  [{idx:2d}/{len(to_sync)}] Synced {p['slug']} -> {p.get('image_url')}")

print("Batch 5 Live Supabase Sync Complete!")

