import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.db.supabase_client import SupabaseUploader

uploader = SupabaseUploader(dry_run=False)

live_v_slugs = set()
page = 0
while True:
    res = uploader.client.table("product_variants").select("slug").range(page * 500, (page + 1) * 500 - 1).execute()
    if not res.data:
        break
    for v in res.data:
        live_v_slugs.add(v["slug"])
    page += 1

items = json.load(open(ROOT / "protein-etl/data/seed_products.json", encoding="utf-8"))
local_v_slugs = set()
for p in items:
    for v in p["variants"]:
        v_slug = v["slug"] if v.get("slug", "").startswith(f"{p['slug']}-") else f"{p['slug']}-{v['slug']}"
        local_v_slugs.add(v_slug)

missing_v = local_v_slugs - live_v_slugs
print(f"Total Local Variants: {len(local_v_slugs)}")
print(f"Total Live Supabase Variants: {len(live_v_slugs)}")
print(f"Missing Variants in Supabase: {len(missing_v)}")
if missing_v:
    print(f"Sample missing: {list(missing_v)[:5]}")
