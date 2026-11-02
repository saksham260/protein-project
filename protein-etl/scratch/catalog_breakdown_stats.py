import json
from collections import defaultdict, Counter

catalog = json.load(open('protein-web/src/data/seedCatalog.json', encoding='utf-8'))

cat_brands = defaultdict(set)
cat_products = Counter()

for p in catalog:
    cat = p.get('category_slug') or (p.get('category') or {}).get('slug')
    brand = p.get('brand_name') or (p.get('brand') or {}).get('name')
    cat_brands[cat].add(brand)
    cat_products[cat] += 1

print("=== CATEGORY SUMMARY ===")
for cat, count in cat_products.most_common():
    brands = sorted(list(cat_brands[cat]))
    print(f"\n[{cat}] - {count} products across {len(brands)} brands:")
    print("  Brands: " + ", ".join(brands))
