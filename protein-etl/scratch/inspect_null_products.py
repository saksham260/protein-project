import json

with open('protein-web/src/data/seedCatalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open('protein-etl/data/demo_catalog/manual_entries.jsonl', 'r', encoding='utf-8') as f:
    manual = {}
    for line in f:
        line = line.strip()
        if line:
            obj = json.loads(line)
            manual[obj.get('handle', '')] = obj

with open('protein-etl/data/demo_catalog/store_snapshot.json', 'r', encoding='utf-8') as f:
    snapshot = json.load(f)

null_prods = [p for p in cat if not p.get('imageUrl') and not p.get('image_url')]

print(f"Total null products: {len(null_prods)}")

records = []
for p in null_prods:
    slug = p['slug']
    m = manual.get(slug, {})
    s = snapshot.get(slug, {})
    
    rec = {
        'slug': slug,
        'name': p['name'],
        'brand': p.get('brandName') or p.get('brand_name'),
        'category': p.get('categorySlug') or p.get('category_slug'),
        'manual_url': m.get('url'),
        'variants': [v.get('title') for v in p.get('variants', [])]
    }
    records.append(rec)

with open('protein-etl/scratch/null_products_detailed.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2)

print("Saved to protein-etl/scratch/null_products_detailed.json")
