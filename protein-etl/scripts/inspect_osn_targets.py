import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
json_file = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch" / "osn_products.json"

with open(json_file, encoding="utf-8") as f:
    products = json.load(f)

targets = [
    "hydro-gold-5lbs",
    "iso-gold-protein-2lbs",
    "iso-gold-protein-5lbs",
    "one-science-nutrition-premium-whey-protein-5lbs",
    "one-science-nutrition-premium-whey-protein-2lbs",
    "one-science-nutrition-premium-whey-1lb",
    "one-science-nutrition-nitra-whey-4lbs",
    "one-science-nutrition-nitra-whey-2lbs",
    "ripped-professional-whey-4lbs",
    "one-science-nutrition-fermented-yeast-protein-1kg",
    "one-science-nutrition-plant-protein-pea-protein-isolate-1kg",
    "one-science-nutrition-high-protein-muesli-dark-choco-crunchy",
    "one-science-nutrition-high-protein-oats-dark-chocolate"
]

for p in products:
    if p["handle"] in targets:
        print(f"=== {p['title']} ===")
        print(f"Handle: {p['handle']}")
        print(f"Variants ({len(p['variants'])}):")
        for v in p["variants"]:
            print(f"  - id: {v['id']}, title: {v['title']}, price: {v['price']}, compare_at: {v.get('compare_at_price')}, available: {v.get('available')}")
        print(f"Images ({len(p['images'])}):")
        for img in p["images"]:
            print(f"  - {img['src']}")
        print()
