import json
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
client = create_client(cfg.get("SUPABASE_URL"), cfg.get("SUPABASE_SERVICE_KEY"))

# Fetch all live product slugs
live_slugs = set()
page = 0
while True:
    res = client.table("products").select("slug").range(page * 500, (page + 1) * 500 - 1).execute()
    if not res.data:
        break
    for p in res.data:
        live_slugs.add(p["slug"])
    page += 1

# Load local seed catalog
local_catalog = json.load(open("protein-web/src/data/seedCatalog.json", encoding="utf-8"))
local_slugs = set(p["slug"] for p in local_catalog)

missing_in_supabase = local_slugs - live_slugs
extra_in_supabase = live_slugs - local_slugs

print(f"Total Local Products: {len(local_slugs)}")
print(f"Total Live Supabase Products: {len(live_slugs)}")
print(f"Products in local catalog but NOT in Supabase: {len(missing_in_supabase)}")
print(f"Products in Supabase but NOT in local catalog: {len(extra_in_supabase)}")
