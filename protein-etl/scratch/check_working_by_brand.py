import json
from collections import defaultdict

with open("protein-etl/scratch/browser_image_status.json", "r", encoding="utf-8") as f:
    broken = json.load(f)["broken"]
broken_slugs = set(b["slug"] for b in broken)

# Load seedCatalog
with open("protein-web/src/data/seedCatalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Total catalog products: {len(catalog)}")
by_brand = defaultdict(list)
for p in catalog:
    b = p.get("brand_name")
    img = p.get("image_url")
    if p["slug"] not in broken_slugs and img and img.startswith("http"):
        by_brand[b].append((p["name"], img))

for b, prods in sorted(by_brand.items()):
    print(f"Brand '{b}': {len(prods)} working images (sample: {prods[0][1][:60]}...)")
