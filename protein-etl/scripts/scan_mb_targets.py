import urllib.request, json, io, re
from PIL import Image
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

def scan_urls(urls, label):
    print(f"Scanning {len(urls)} urls for {label}...")
    for idx, u in enumerate(urls):
        try:
            req = urllib.request.Request(u, headers=headers)
            img = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=8).read())).convert("RGB")
            img.thumbnail((1600, 1600))
            temp_path = f"protein-etl/data/demo_catalog/labels/temp_scan_{label}_{idx}.jpg"
            img.save(temp_path, "JPEG")
            res = ocr(temp_path)
            txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
            joined = " ".join(txts).lower()
            if any(k in joined for k in ["nutrition", "serving size", "energy", "nutrients"]) and len(txts) > 15:
                print(f"[FOUND] {label} in {u} ({len(txts)} lines)")
                with open(f"protein-etl/data/demo_catalog/{label}_ocr_found.txt", "w", encoding="utf-8") as out:
                    out.write(f"URL: {u}\n")
                    for t in txts:
                        out.write(t + "\n")
                return u, txts
        except Exception:
            pass
    return None, []

mb_photos = json.load(open("protein-etl/data/demo_catalog/mb_photos.json", encoding="utf-8"))

# 1. 30g bar
bar_urls = [u for u in mb_photos.get("muscleblaze-hi-protein-bar-30g-protein", []) if u.endswith("_o.jpg")]
scan_urls(bar_urls[:15], "mb_30g_bar")

# 2. Biozyme Whey
biozyme_urls = [u for u in mb_photos.get("muscleblaze-biozyme-performance-whey", []) if u.endswith("_o.jpg")]
scan_urls(biozyme_urls[10:40], "mb_biozyme_whey")
