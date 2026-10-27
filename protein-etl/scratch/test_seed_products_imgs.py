import json
import urllib.request

with open('protein-etl/data/seed_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in seed_products.json: {len(products)}")

null_count = 0
valid_count = 0
broken = []

headers = {"User-Agent": "Mozilla/5.0"}

for p in products:
    img = p.get("image_url")
    if not img:
        null_count += 1
        continue
    try:
        req = urllib.request.Request(img, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as r:
            if r.status == 200:
                valid_count += 1
            else:
                broken.append((p['slug'], f"HTTP {r.status}", img))
    except Exception as e:
        broken.append((p['slug'], str(e), img))

print(f"Verified 200 OK:      {valid_count}")
print(f"Clean Null (emoji):   {null_count}")
print(f"Broken:               {len(broken)}")

if broken:
    for slug, err, img in broken:
        print(f"  {slug}: {err} | {img}")
