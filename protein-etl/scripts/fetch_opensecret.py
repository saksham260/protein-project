import urllib.request
import json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')
ROOT.mkdir(parents=True, exist_ok=True)

all_products = []
page = 1
while True:
    url = f"https://opensecret.in/products.json?limit=250&page={page}"
    print(f"Fetching Open Secret page {page}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read())
            prods = data.get("products", [])
            print(f"  Page {page}: {len(prods)} products")
            if not prods:
                break
            all_products.extend(prods)
            page += 1
            if len(prods) < 250:
                break
    except Exception as e:
        print("Failed:", e)
        break

print(f"\nTotal Open Secret products: {len(all_products)}")
with open(ROOT / "opensecret_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2)

# Filter for protein/cookie/snack products
relevant = []
for p in all_products:
    t = p.get("title", "").lower()
    h = p.get("handle", "")
    if any(k in t for k in ["rusk", "cookie", "whey", "protein", "chip", "nutty", "oats"]):
        relevant.append(p)

print(f"Relevant products: {len(relevant)}")
for p in relevant[:20]:
    print(f"  - {p.get('title')} (handle: {p.get('handle')})")
