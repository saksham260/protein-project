import urllib.request, json

headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("https://bigmusclesnutrition.com/products.json?limit=250", headers=headers)
data = json.loads(urllib.request.urlopen(req, timeout=12).read().decode("utf-8"))

target_handles = [
    "premium-gold-whey-protein-1",
    "titan-whey",
    "plant-protein-isolate-vegan-protein-powder-clean-recovery-pea-brown-rice-protein-copy"
]

found = {}
for p in data.get("products", []):
    if p.get("handle") in target_handles:
        found[p["handle"]] = {
            "handle": p["handle"],
            "title": p["title"],
            "variants": [{"title": v["title"], "price": v["price"], "compare_at_price": v.get("compare_at_price"), "sku": v.get("sku"), "available": v.get("available")} for v in p.get("variants", [])],
            "images": [{"src": img["src"]} for img in p.get("images", [])]
        }

with open("protein-etl/data/demo_catalog/bm_extracted.json", "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(found)} products for Bigmuscles Nutrition.")
for h, item in found.items():
    print(f"  {h}: {item['title']} -> {len(item['variants'])} variants, {len(item['images'])} images")
