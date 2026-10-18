import urllib.request, json, io
from pathlib import Path
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}
KEYWORDS = ["nutrition", "nutritional", "protein", "energy", "carbohydrate", "fat", "serving", "ingredients", "contains"]

def download_img(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except:
        return None

def score_text(txts):
    joined = " ".join(txts).lower()
    score = sum(1 for kw in KEYWORDS if kw in joined)
    return score, joined, txts

# 1. Scan The Whole Truth photos
print("--- Scanning The Whole Truth Photos ---")
twt = json.load(open("protein-etl/data/demo_catalog/twt_extracted.json", encoding="utf-8"))
twt_results = {}
for h, p in twt.items():
    best_score = 0
    best_url = ""
    best_txts = []
    for img_obj in p["images"]:
        url = img_obj["src"]
        img = download_img(url)
        if img:
            res = ocr(np.array(img))
            txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
            s, j, t = score_text(txts)
            if s > best_score:
                best_score = s
                best_url = url
                best_txts = t
    print(f"TWT {h}: best score {best_score} from {best_url}")
    twt_results[h] = {"url": best_url, "score": best_score, "txts": best_txts}

# 2. Scan MuscleBlaze Photos
print("\n--- Scanning MuscleBlaze Photos ---")
mb_photos = json.load(open("protein-etl/data/demo_catalog/mb_photos.json", encoding="utf-8"))
mb_results = {}
for h, urls in mb_photos.items():
    best_score = 0
    best_url = ""
    best_txts = []
    # Test top 15 candidate images per product
    for url in urls[:15]:
        img = download_img(url)
        if img:
            res = ocr(np.array(img))
            txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
            s, j, t = score_text(txts)
            if s > best_score:
                best_score = s
                best_url = url
                best_txts = t
    print(f"MB {h}: best score {best_score} from {best_url}")
    mb_results[h] = {"url": best_url, "score": best_score, "txts": best_txts}

with open("protein-etl/data/demo_catalog/batch3a_ocr_scans.json", "w", encoding="utf-8") as f:
    json.dump({"twt": twt_results, "mb": mb_results}, f, indent=2, ensure_ascii=False)

print("\nSaved batch3a_ocr_scans.json")
