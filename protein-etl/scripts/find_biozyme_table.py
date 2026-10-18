import urllib.request, json, io
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

mb_photos = json.load(open("protein-etl/data/demo_catalog/mb_photos.json", encoding="utf-8"))
urls = mb_photos.get("muscleblaze-biozyme-performance-whey", [])

# Let's find images that have "nutrition" or let's test images with 41388 or 39078
candidates = [u for u in urls if any(k in u for k in ["41388", "39077", "41389", "39078"]) and u.endswith("_o.jpg")]
print(f"Candidate images for Biozyme: {len(candidates)}")

results = []
for u in candidates[:25]:
    img = download_img(u)
    if img:
        res = ocr(np.array(img))
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        joined = " ".join(txts).lower()
        if any(k in joined for k in ["energy", "protein", "carbohydrate", "serving", "nutritional"]):
            print(f"Found nutrition text in: {u}")
            results.append({"url": u, "txts": txts})

with open("protein-etl/data/demo_catalog/biozyme_found.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Saved biozyme_found.json")
