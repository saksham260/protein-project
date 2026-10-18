import json, urllib.request, io
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}
mb_photos = json.load(open("protein-etl/data/demo_catalog/mb_photos.json", encoding="utf-8"))
urls = mb_photos.get("muscleblaze-biozyme-performance-whey", [])
orig_urls = [u for u in urls if u.endswith("_o.jpg") and not "banner" in u.lower()]

print("Searching remaining orig_urls...")
found = []
for idx, u in enumerate(orig_urls[25:80], 25):
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            img = Image.open(io.BytesIO(r.read())).convert("RGB")
        res = ocr(np.array(img))
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        joined = " ".join(txts).lower()
        if "serving size" in joined or "per serving" in joined or "energy (kcal)" in joined or "typical amino acid" in joined:
            print(f"MATCH in {idx}: {u}")
            found.append({"url": u, "txts": txts})
    except Exception as e:
        pass

with open("protein-etl/data/demo_catalog/biozyme_nut_panel.json", "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2, ensure_ascii=False)
print(f"Done. Found {len(found)} nutrition tables.")
