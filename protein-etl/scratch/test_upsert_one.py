import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.db.supabase_client import SupabaseUploader
from src.models import ProductCreate

items = json.load(open(ROOT / "protein-etl/data/seed_products.json", encoding="utf-8"))

# Find the first product that is missing in live Supabase
uploader = SupabaseUploader(dry_run=False)
live_slugs = {p["slug"] for p in uploader.client.table("products").select("slug").execute().data}

missing = [p for p in items if p["slug"] not in live_slugs]
print(f"Total missing products to seed: {len(missing)}")

if missing:
    test_prod = ProductCreate(**missing[0])
    print(f"Testing upsert on: {test_prod.name} ({test_prod.slug})")
    res = uploader.upsert_product(test_prod)
    print("Upsert result:", res)
