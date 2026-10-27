import json
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")
client = create_client(url, key)

print("Connecting to live Supabase...")

# 1. Load newly rebuilt seed_products.json
seed_path = Path("protein-etl/data/seed_products.json")
with open(seed_path, "r", encoding="utf-8") as f:
    seed_products = json.load(f)

print(f"Loaded {len(seed_products)} products from seed_products.json")

# Map of slug -> seed_product
seed_map = {p["slug"]: p for p in seed_products}

# 2. Get all live products from Supabase
res = client.table("products").select("id, slug, name, image_url").execute()
live_products = res.data
print(f"Loaded {len(live_products)} live products from Supabase")

prod_updates_count = 0
variant_updates_count = 0

for lp in live_products:
    slug = lp["slug"]
    sp = seed_map.get(slug)
    if not sp:
        continue
        
    target_img = sp.get("image_url")
    current_img = lp.get("image_url")
    
    # Check if product image_url needs updating
    if current_img != target_img:
        client.table("products").update({"image_url": target_img}).eq("id", lp["id"]).execute()
        prod_updates_count += 1
        
    # Check and update variants for this product
    sp_variants = sp.get("variants", [])
    # Get live variants
    lv_res = client.table("product_variants").select("id, slug, variant_name, mrp_inr, image_url").eq("product_id", lp["id"]).execute()
    live_vars = lv_res.data
    
    for lv in live_vars:
        # Match variant by slug or position
        matched_sv = next((sv for sv in sp_variants if sv.get("slug") == lv.get("slug") or sv.get("variant_name") == lv.get("variant_name")), None)
        if matched_sv:
            target_v_img = matched_sv.get("image_url") or target_img
            target_mrp = matched_sv.get("mrp_inr")
            
            var_update = {}
            if lv.get("image_url") != target_v_img:
                var_update["image_url"] = target_v_img
            if target_mrp and lv.get("mrp_inr") != target_mrp:
                var_update["mrp_inr"] = target_mrp
                
            if var_update:
                client.table("product_variants").update(var_update).eq("id", lv["id"]).execute()
                variant_updates_count += 1

# Special explicit fix for Avvatar Wafer Bar
avvatar_encoded = "https://www.avvatarindia.com/images/product_images/1754284949_WhatsApp%20Image%202025-07-25%20at%2012.08.28%20PM.jpeg"
client.table("products").update({"image_url": avvatar_encoded}).ilike("slug", "%wafer-bar%").execute()
client.table("product_variants").update({"image_url": avvatar_encoded}).ilike("slug", "%wafer-bar%").execute()

print(f"\nSupabase live sync complete:")
print(f"  - Products updated: {prod_updates_count}")
print(f"  - Variants updated: {variant_updates_count}")
