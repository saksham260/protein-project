import urllib.request, json, io
from pathlib import Path
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

def download_img(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except:
        return None

av_photos = json.load(open("protein-etl/data/demo_catalog/avvatar_photos.json", encoding="utf-8"))
av_results = {}

for h, data in av_photos.items():
    nut_urls = data.get("nutrition", [])
    prod_urls = data.get("product", [])
    urls_to_try = nut_urls + prod_urls[:5]
    
    ocr_outputs = []
    for u in urls_to_try:
        img = download_img(u)
        if img:
            res = ocr(np.array(img))
            txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
            if txts:
                ocr_outputs.append({"url": u, "txts": txts})
    
    av_results[h] = ocr_outputs
    print(f"Avvatar {h}: scanned {len(urls_to_try)} images -> {len(ocr_outputs)} had text")

with open("protein-etl/data/demo_catalog/avvatar_ocr_scans.json", "w", encoding="utf-8") as f:
    json.dump(av_results, f, indent=2, ensure_ascii=False)

print("Saved avvatar_ocr_scans.json")
