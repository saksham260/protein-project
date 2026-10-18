import urllib.request, json, re
from pathlib import Path

headers = {"User-Agent": "Mozilla/5.0"}

handles = [
    "100-performance-whey-belgain-chocolate-flavour-1-kg",
    "100-performance-whey-belgain-chocolate-flavour-2-kg",
    "100-performance-whey-malai-kulfi-flavour-1-kg",
    "100-performance-whey-malai-kulfi-flavour-2-kg",
    "100-performance-whey-cold-coffee-flavour-2-kg",
    "100-performance-whey-unflavored-1-kg",
    "isorich-protein-belgian-chocolate-flavour-1-kg",
    "isorich-protein-belgian-chocolate-flavour-2-kg",
    "isorich-protein-malai-kulfi-flavour-1-kg",
    "isorich-protein-malai-kulfi-flavour-2-kg",
    "isorich-protein-chocolate-hazelnut-flavour-1-kg",
    "alpha-whey-belgian-chocolate-flavour-1-kg-2509104129-263",
    "alpha-whey-belgian-chocolate-flavour-2-kg-2509104551-890",
    "alpha-whey-malai-kulfi-flavour-1-kg",
    "alpha-whey-cold-coffee-flavour-1-kg",
    "protein-wafer-bar-coffee-flavour-320g",
    "protein-wafer-bar-tiramisu-flavour-320g"
]

avvatar_photos = {}
for h in handles:
    url = f"https://www.avvatarindia.com/product/{h}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
        nut_imgs = re.findall(r'(/images/nutrition_images/[^"\'\s>]+)', html)
        prod_imgs = re.findall(r'(https://www.avvatarindia.com/images/product_images/[^"\'\s>]+)', html)
        avvatar_photos[h] = {
            "nutrition": [f"https://www.avvatarindia.com{x}" for x in set(nut_imgs)],
            "product": list(set(prod_imgs))
        }
        print(f"[OK] {h:<50} | Nut imgs: {len(nut_imgs)} | Prod imgs: {len(prod_imgs)}")
    except Exception as e:
        print(f"[ERR] {h}: {e}")

Path("protein-etl/data/demo_catalog/avvatar_photos.json").write_text(json.dumps(avvatar_photos, indent=2), encoding="utf-8")
