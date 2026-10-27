import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

with open('protein-etl/data/seed_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in seed_products.json: {len(products)}")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def check_product(p):
    img = p.get("image_url")
    if not img:
        return ("null", p['slug'], None, None)
    try:
        req = urllib.request.Request(img, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as r:
            if r.status == 200:
                return ("ok", p['slug'], img, None)
            else:
                return ("broken", p['slug'], img, f"HTTP {r.status}")
    except Exception as e:
        return ("broken", p['slug'], img, str(e))

with ThreadPoolExecutor(max_workers=25) as executor:
    results = list(executor.map(check_product, products))

ok_list = [r for r in results if r[0] == "ok"]
null_list = [r for r in results if r[0] == "null"]
broken_list = [r for r in results if r[0] == "broken"]

print(f"Verified 200 OK:      {len(ok_list)}")
print(f"Clean Null (emoji):   {len(null_list)}")
print(f"Broken:               {len(broken_list)}")

if broken_list:
    for _, slug, img, err in broken_list:
        print(f"  {slug}: {err} | {img}")
