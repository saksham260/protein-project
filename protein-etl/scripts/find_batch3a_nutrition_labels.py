import urllib.request, json, re, io
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
    except Exception as e:
        return None

def score_text(txts):
    joined = " ".join(txts).lower()
    score = sum(1 for kw in KEYWORDS if kw in joined)
    return score, joined

print("Testing Bigmuscles Nutrition photos...")
bm = json.load(open("protein-etl/data/demo_catalog/bm_extracted.json", encoding="utf-8"))
for h, p in bm.items():
    best_img = None
    best_score = 0
    best_txt = ""
    best_url = ""
    for idx, img_obj in enumerate(p["images"][:12]):
        url = img_obj["src"]
        img = download_img(url)
        if img:
            res = ocr(np.array(img))
            txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
            s, j = score_text(txts)
            if s > best_score:
                best_score = s
                best_img = img
                best_txt = j
                best_url = url
    print(f"BM {h}: best score {best_score} from {best_url}")
    if best_score > 0:
        print("  Sample text:", best_txt[:150])
