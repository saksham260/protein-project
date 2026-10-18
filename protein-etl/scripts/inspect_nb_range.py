import json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')
with open(ROOT / 'nb_page_props.json', encoding='utf-8') as f:
    d = json.load(f)

pp = d['initialState']['parentProduct']
ranges_data = pp.get('getProductRange', {}).get('data', {}).get('data', [])
print(f'Items in range: {len(ranges_data)}')

unique_products = {}
for item in ranges_data:
    pid = item.get('pid')
    slug = item.get('slug')
    name = item.get('name')
    price = item.get('discounted_price')
    mrp = item.get('price')
    stock = item.get('stock_status')
    if slug not in unique_products:
        unique_products[slug] = {
            'pid': pid,
            'name': name,
            'slug': slug,
            'price': price,
            'mrp': mrp,
            'variants': []
        }
    unique_products[slug]['variants'].append({
        'vid': item.get('vid'),
        'display_value': item.get('display_value'),
        'price': price,
        'mrp': mrp,
        'stock': stock,
        'thumb': item.get('thumbnail_image')
    })

print(f'\nUnique products: {len(unique_products)}')
for slug, p in unique_products.items():
    print(f"\n[{p['pid']}] {slug}")
    print(f"  Name: {p['name']}")
    print(f"  Variants count: {len(p['variants'])}")
    for v in p['variants']:
        print(f"    - {v['display_value']} -> Rs. {v['price']} (MRP: {v['mrp']}) in_stock={v['stock']}")

with open(ROOT / 'nb_range_products.json', 'w', encoding='utf-8') as f:
    json.dump(unique_products, f, indent=2)
