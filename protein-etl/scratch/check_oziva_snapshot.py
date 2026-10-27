import json

with open('protein-etl/data/demo_catalog/store_snapshot.json', 'r', encoding='utf-8') as f:
    snap = json.load(f)

oziva_prods = snap.get('oziva.in', [])
print(f"Total OZiva products in snapshot: {len(oziva_prods)}")

targets = ['protein-herbs-for-women', 'superfood-plant-protein', 'organic-plant-protein', 'clean-whey']
for p in oziva_prods:
    handle = p.get('handle', '')
    title = p.get('title', '')
    if any(t in handle.lower() or t in title.lower() for t in ['protein', 'herbs', 'women']):
        imgs = p.get('images', [])
        img_src = imgs[0].get('src') if imgs else None
        print(f"  Handle: {handle} | Title: {title}")
        print(f"    Image: {img_src}")
