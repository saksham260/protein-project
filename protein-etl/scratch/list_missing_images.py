import json
import os
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client

load_dotenv("protein-etl/.env")
load_dotenv("protein-web/.env.local")

url = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
sb = create_client(url, key)

res = sb.table("products").select("slug, name, image_url, is_active, categories(slug, name), brands(slug, name)").eq("is_active", True).execute()
live_prods = res.data

missing_live = [p for p in live_prods if not p.get("image_url")]

seed_web = json.loads(Path("protein-web/src/data/seedCatalog.json").read_text(encoding="utf-8"))
missing_web = [p for p in seed_web if not p.get("image_url")]

# Also check if any files exist in Supabase Storage bucket 'product-images' that were overwritten when build_demo_catalog.py ran during Waves 1-4!
storage_files = sb.storage.from_("product-images").list()
storage_names = {f["name"] for f in storage_files if f.get("name")}

print(f"Live active products: {len(live_prods)}")
print(f"Live missing image_url: {len(missing_live)}")
print(f"Local seedCatalog products: {len(seed_web)}, missing image_url: {len(missing_web)}")
print(f"Files in Supabase Storage 'product-images': {len(storage_names)}")

# Check which missing_live slugs actually have a matching file in Supabase Storage 'product-images'
recovered_in_storage = []
for p in missing_live:
    slug = p["slug"]
    for ext in [".webp", ".jpg", ".png", ".jpeg"]:
        if f"{slug}{ext}" in storage_names:
            recovered_in_storage.append((slug, f"{slug}{ext}"))

print(f"Missing products that ALREADY have an image in Supabase Storage 'product-images': {len(recovered_in_storage)}")
for s, fn in recovered_in_storage:
    print(f"  * {s} -> {fn}")

out_path = Path("protein-etl/scratch/missing_images_report.json")
out_path.write_text(json.dumps({
    "total_live_products": len(live_prods),
    "total_missing_live": len(missing_live),
    "already_in_storage_bucket": recovered_in_storage,
    "missing_products": sorted(
        [
            {
                "slug": p["slug"],
                "name": p["name"],
                "brand": p["brands"]["name"],
                "brand_slug": p["brands"]["slug"],
                "category": p["categories"]["name"],
                "category_slug": p["categories"]["slug"],
            }
            for p in missing_live
        ],
        key=lambda x: (x["category"], x["brand"], x["name"])
    )
}, indent=2), encoding="utf-8")
print("Wrote protein-etl/scratch/missing_images_report.json")

