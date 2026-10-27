import json
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")
client = create_client(url, key)

cats = client.table("categories").select("id, name, slug").execute().data
cat_map = {c["id"]: c["name"] for c in cats}
slug_map = {c["id"]: c["slug"] for c in cats}

with open("protein-etl/scratch/products_displaying_emoji.json", "r", encoding="utf-8") as f:
    products = json.load(f)

for p in products:
    p["category_name"] = cat_map.get(p["category"], p["category"])
    p["category_slug"] = slug_map.get(p["category"], p["category"])

with open("protein-etl/scratch/products_displaying_emoji.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)

# Print a nicely grouped summary
print(f"Total Products Failing to Show Images: {len(products)}\n")

from collections import defaultdict
by_reason = defaultdict(list)
for p in products:
    by_reason[p["reason_code"]].append(p)

print(f"=== Group 1: Domain Not Allowed in next.config.ts ({len(by_reason['UNALLOWED_HOSTNAME'])}) ===")
for p in by_reason['UNALLOWED_HOSTNAME']:
    print(f"- [{p['brand']}] {p['name']} ({p['category_name']})")
    print(f"    URL: {p['image_url']}")
    print(f"    Issue: {p['detail']}")

print(f"\n=== Group 2: Allowed Domain but Broken/Unreachable Link ({len(by_reason['BROKEN_HTTP'])}) ===")
for p in by_reason['BROKEN_HTTP']:
    print(f"- [{p['brand']}] {p['name']} ({p['category_name']})")
    print(f"    URL: {p['image_url']}")
    print(f"    Issue: {p['detail']}")
