import urllib.request, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"

test_urls = [
    "https://www.plixlife.com/product/plant-protein-powder",
    "https://www.plixlife.com/product/strength",
    "https://www.plixlife.com/product/super-strength-fermented-yeast-protein",
    "https://www.plixlife.com/product/womens-protein-super-foods"
]

for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
            print(f"{url} -> HTTP {r.status}, length: {len(html)}")
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
            if m:
                d = json.loads(m.group(1))
                pp = d.get("props", {}).get("pageProps", {})
                print(f"  pageProps keys: {list(pp.keys())}")
                prod = pp.get("productData") or pp.get("product") or pp.get("data")
                if prod and isinstance(prod, dict):
                    print(f"  title: {prod.get('title') or prod.get('name')}")
    except Exception as e:
        print(f"{url} -> ERROR: {e}")
