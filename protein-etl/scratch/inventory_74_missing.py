import json
from pathlib import Path
from collections import defaultdict

with open("protein-etl/scratch/browser_image_status.json", "r", encoding="utf-8") as f:
    broken = json.load(f)["broken"]

# Filter out the 74 currently missing/broken
missing_products = [b for b in broken]
print(f"Total products to find images for: {len(missing_products)}")

# Group by brand
by_brand = defaultdict(list)
for p in missing_products:
    by_brand[p["brand"]].append(p)

for b, prods in sorted(by_brand.items(), key=lambda x: -len(x[1])):
    print(f"\nBrand: {b} ({len(prods)} products)")
    for p in prods:
        print(f"  - {p['name']} ({p['slug']}) [Category: {p['category']}]")

