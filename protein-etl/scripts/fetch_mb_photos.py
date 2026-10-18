import urllib.request, json, re
from pathlib import Path

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

mb_urls = [
    ("muscleblaze-biozyme-performance-whey", "https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093"),
    ("fuel-one-whey-protein", "https://www.muscleblaze.com/sv/fuel-one-whey-protein/SP-72739"),
    ("muscleblaze-100-clean-raw-whey-protein-concentrate", "https://www.muscleblaze.com/sv/muscleblaze-100-clean-raw-whey-protein-concentrate/SP-40454"),
    ("muscleblaze-hi-protein-bar-30g-protein", "https://www.muscleblaze.com/sv/muscleblaze-hi-protein-bar-30g-protein/SP-44769")
]

mb_photos = {}
for h, url in mb_urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        imgs = list(dict.fromkeys(re.findall(r'(https://img\d*\.hkrtcdn\.com/[^"\'\s>]+)', html)))
        filtered = [i for i in imgs if any(k in i.lower() for k in ["prd_", "secprd", "product"]) and not any(k in i.lower() for k in ["banner", "icon", "logo", "review", "sprite"])]
        mb_photos[h] = filtered
        print(f"[OK] MB {h:<45} | Images: {len(filtered)}")
        for img in filtered[:4]:
            print("  ", img)
    except Exception as e:
        print(f"[ERR] MB {h}: {e}")

Path("protein-etl/data/demo_catalog/mb_photos.json").write_text(json.dumps(mb_photos, indent=2), encoding="utf-8")
