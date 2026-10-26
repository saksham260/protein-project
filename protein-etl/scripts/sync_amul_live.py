import os
import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.db.supabase_client import SupabaseUploader
from src.models import ProductCreate

def main():
    uploader = SupabaseUploader(dry_run=False)
    client = uploader.client

    seed_file = ROOT / "protein-etl" / "data" / "seed_products.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        all_products = json.load(f)

    amul_slugs = [
        "amul-high-protein-paneer",
        "amul-high-protein-whey-protein-sachets",
        "amul-high-protein-blueberry-milkshake",
        "amul-high-protein-buttermilk",
        "amul-high-protein-lassi",
        "amul-high-protein-milk",
        "amul-high-protein-probiotic-dahi",
    ]

    amul_seed_data = [p for p in all_products if p.get("slug") in amul_slugs]
    print(f"Found {len(amul_seed_data)} Amul products in seed_products.json")

    p_res = client.table("products").select("id,slug").in_("slug", amul_slugs).execute()
    prod_map = {p["slug"]: p["id"] for p in p_res.data}

    # 1. Clean up old/stale variants for Lassi and Buttermilk in Supabase
    for slug in ["amul-high-protein-lassi", "amul-high-protein-buttermilk"]:
        pid = prod_map.get(slug)
        if pid:
            vars_res = client.table("product_variants").select("id,variant_name,slug").eq("product_id", pid).execute()
            for v in vars_res.data:
                vid = v["id"]
                vname = v["variant_name"]
                print(f"Deleting old links & flags for {slug} variant {vname} ({vid})...")
                client.table("redirect_links").delete().eq("variant_id", vid).execute()
                client.table("variant_red_flags").delete().eq("variant_id", vid).execute()
                # If it is the 200ml single bottle, delete the variant itself so the Pack of 30 takes its place
                if "200ml" in vname and "pack of 30" not in vname.lower():
                    print(f"Deleting stale variant {vname} ({v['slug']})...")
                    client.table("product_variants").delete().eq("id", vid).execute()

    # 2. For Blueberry Shake, delete old redirect links on the pack of 30
    bb_pid = prod_map.get("amul-high-protein-blueberry-milkshake")
    if bb_pid:
        vars_res = client.table("product_variants").select("id,variant_name,slug").eq("product_id", bb_pid).execute()
        for v in vars_res.data:
            vid = v["id"]
            print(f"Cleaning redirect links for Blueberry Shake {v['variant_name']} ({vid})...")
            client.table("redirect_links").delete().eq("variant_id", vid).execute()

    # 3. For all other Amul products, remove non-d2c redirect links
    for slug in ["amul-high-protein-paneer", "amul-high-protein-whey-protein-sachets", "amul-high-protein-milk", "amul-high-protein-probiotic-dahi"]:
        pid = prod_map.get(slug)
        if pid:
            vars_res = client.table("product_variants").select("id,variant_name").eq("product_id", pid).execute()
            for v in vars_res.data:
                vid = v["id"]
                print(f"Deleting non-d2c links for {slug} variant {v['variant_name']}...")
                client.table("redirect_links").delete().eq("variant_id", vid).neq("platform", "d2c").execute()

    # 4. Upsert all 7 Amul products using SupabaseUploader
    for p_data in amul_seed_data:
        print(f"Upserting product to live Supabase: {p_data['slug']}")
        product = ProductCreate(**p_data)
        uploader.upsert_product(product)

    print("Successfully updated live Supabase for all Amul products!")

if __name__ == "__main__":
    main()
