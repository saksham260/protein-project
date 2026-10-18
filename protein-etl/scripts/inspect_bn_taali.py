import json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')

with open(ROOT / 'butternut_products.json', encoding='utf-8') as f:
    bn_prods = json.load(f)

with open(ROOT / 'taalifoods_products.json', encoding='utf-8') as f:
    taali_prods = json.load(f)

print("=== THE BUTTERNUT COMPANY CANDIDATES ===")
bn_candidates = []
for p in bn_prods:
    title = p.get('title', '')
    handle = p.get('handle', '')
    t_lower = title.lower()
    if any(k in t_lower for k in ['protein', 'peanut butter', 'almond butter', 'spread', 'tahini', 'balls', 'bar']):
        bn_candidates.append(p)

print(f"Total Butternut candidates: {len(bn_candidates)}")
for p in bn_candidates[:15]:
    title = p.get('title')
    handle = p.get('handle')
    v_count = len(p.get('variants', []))
    print(f"  [{v_count} vars] {title} ({handle})")

print("\n=== TAALI FOODS CANDIDATES ===")
taali_candidates = []
for p in taali_prods:
    title = p.get('title', '')
    handle = p.get('handle', '')
    t_lower = title.lower()
    if any(k in t_lower for k in ['protein', 'puff', 'makhana', 'peanut', 'snack']):
        taali_candidates.append(p)

print(f"Total Taali candidates: {len(taali_candidates)}")
for p in taali_candidates[:15]:
    title = p.get('title')
    handle = p.get('handle')
    v_count = len(p.get('variants', []))
    print(f"  [{v_count} vars] {title} ({handle})")
