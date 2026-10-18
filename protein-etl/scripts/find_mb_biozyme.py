import json, re, urllib.request, io
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}
KEYWORDS = ["nutrition", "nutritional", "protein", "energy", "carbohydrate", "fat", "serving", "bcaa", "eaas"]

def download_img(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except:
        return None

mb_photos = json.load(open("protein-etl/data/demo_catalog/mb_photos.json", encoding="utf-8"))
urls = mb_photos.get("muscleblaze-biozyme-performance-whey", [])

# Filter for original images (_o.jpg)
orig_urls = [u for u in urls if u.endswith("_o.jpg") and not "banner" in u.lower()]
print(f"Total orig urls for Biozyme Performance Whey: {len(orig_urls)}")

best_score = 0
best_url = ""
best_txts = []

for u in orig_urls[:30]:
    img = download_img(u)
    if img:
        res = ocr(np.array(img))
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        joined = " ".join(txts).lower()
        score = sum(1 for kw in KEYWORDS if kw in joined)
        if score > best_score:
            best_score = score
            best_url = u
            best_txts = txts
            print(f"New best score {score} from {u}")

print(f"\nFinal best for Biozyme Performance Whey: score={best_score}, url={best_url}")
if best_txts:
    print("Sample:", best_txts[:10])
    with open("protein-etl/data/demo_catalog/mb_biozyme_ocr.json", "w", encoding="utf-8") as f:
        json.dump({"url": best_url, "txts": best_txts}, f, indent=2, ensure_ascii=False)
