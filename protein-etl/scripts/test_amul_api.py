import urllib.request
import json

test_urls = [
    "https://shop.amul.com/api/1.1/entity/ms.products?limit=20",
    "https://shop.amul.com/api/1.1/entity/ms.products?q={\"category\":\"6304be509be215ee6c695973\"}",
    "https://shop.amul.com/api/1.1/entity/ms.products?q={\"alias\":\"amul-high-protein-paneer-400-g-or-pack-of-2\"}"
]

for url in test_urls:
    print("Testing URL:", url[:80])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            items = data.get("data", [])
            print(f"-> SUCCESS! Status: {r.status}, items: {len(items)}")
            for item in items[:5]:
                print(f"   - {item.get('name')} | alias: {item.get('alias')}")
            if items:
                with open("protein-etl/data/demo_catalog/scratch/amul_api_sample.json", "w", encoding="utf-8") as f:
                    json.dump(items[0], f, indent=2)
                break
    except Exception as e:
        print("  Failed:", e)
