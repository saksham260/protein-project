import urllib.request, re, json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')
ROOT.mkdir(parents=True, exist_ok=True)

test_urls = [
    ("plant-protein-powder", "https://www.plixlife.com/product/plant-protein-powder"),
    ("strength", "https://www.plixlife.com/product/strength"),
    ("super-strength-fermented-yeast-protein", "https://www.plixlife.com/product/super-strength-fermented-yeast-protein"),
    ("womens-protein-super-foods", "https://www.plixlife.com/product/womens-protein-super-foods")
]

results = {}

for slug, url in test_urls:
    try:
        print(f"Fetching {slug}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode("utf-8", errors="ignore")
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        if m:
            d = json.loads(m.group(1))
            ppd = d.get("props", {}).get("pageProps", {}).get("productPageData", {})
            prod = ppd.get("product", {})
            results[slug] = prod
            print(f"  Name: {prod.get('name')}")
            print(f"  Variants ({len(prod.get('variants', []))}):")
            for v in prod.get('variants', []):
                price = v.get('pricing', {}).get('price', {}).get('gross', {}).get('amount')
                mrp = v.get('pricing', {}).get('priceUndiscounted', {}).get('gross', {}).get('amount')
                print(f"    - {v.get('name')} -> Rs. {price} (MRP: {mrp})")
    except Exception as e:
        print(f"  Failed {slug}:", e)

with open(ROOT / "plix_products_extracted.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nDone extracting Plix products!")
