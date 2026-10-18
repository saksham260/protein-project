import json

with open('protein-web/src/data/seedCatalog.json', encoding='utf-8') as f:
    products = json.load(f)

print(f'Total products in seedCatalog: {len(products)}')
batch4a_brands = {'One Science Nutrition', 'Nutrabay', 'Plix'}
found = [p for p in products if p.get('brand_name') in batch4a_brands]
print(f'Found {len(found)} products for Batch 4A:')
for p in found:
    brand = p.get('brand_name')
    name = p.get('name')
    vegan = p.get('is_vegan')
    n_vars = len(p.get('variants', []))
    cat = p.get('category_slug')
    score = p.get('overall_score')
    price = p.get('variants', [{}])[0].get('mrp_inr')
    print(f"  [{brand}] {name}")
    print(f"      Category: {cat} | Vegan: {vegan} | Variants: {n_vars} | Score: {score} | MRP: Rs.{price}")

with open('protein-etl/data/seed_products.json', encoding='utf-8') as f:
    seed_prods = json.load(f)

print(f'\nTotal products in seed_products.json: {len(seed_prods)}')
seed_found = [p for p in seed_prods if p.get('brand_name') in batch4a_brands]
print(f'Found {len(seed_found)} products in seed_products.json')
