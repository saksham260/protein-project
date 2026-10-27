import json
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
client = create_client(cfg.get("SUPABASE_URL"), cfg.get("SUPABASE_SERVICE_KEY"))

with open("protein-etl/scratch/browser_image_status.json", "r", encoding="utf-8") as f:
    broken = json.load(f)["broken"]

remaining_broken_slugs = [b["slug"] for b in broken if b["status"] != "MISSING"]
print(f"Cleaning remaining {len(remaining_broken_slugs)} broken slugs in Supabase to clean null...")

for slug in remaining_broken_slugs:
    # Set product image_url to None
    prod_res = client.table("products").update({"image_url": None}).eq("slug", slug).execute()
    # Also set variant image_urls to None
    if prod_res.data:
        pid = prod_res.data[0]["id"]
        client.table("product_variants").update({"image_url": None}).eq("product_id", pid).execute()
        print(f"  Cleaned: {slug}")

# Also update seed_products.json and seedCatalog.json
seed_path = Path("protein-etl/data/seed_products.json")
web_seed_path = Path("protein-web/src/data/seedCatalog.json")

with open(seed_path, "r", encoding="utf-8") as f:
    seed_prods = json.load(f)

for p in seed_prods:
    if p["slug"] in remaining_broken_slugs:
        p["image_url"] = None
        for v in p.get("variants", []):
            v["image_url"] = None

with open(seed_path, "w", encoding="utf-8") as f:
    json.dump(seed_prods, f, indent=2)

with open(web_seed_path, "r", encoding="utf-8") as f:
    web_seed = json.load(f)

for p in web_seed:
    if p["slug"] in remaining_broken_slugs:
        p["image_url"] = None
        for v in p.get("variants", []):
            v["image_url"] = None

with open(web_seed_path, "w", encoding="utf-8") as f:
    json.dump(web_seed, f, indent=2)

print("\nFinished cleaning remaining broken products to clean null fallback emojis!")
