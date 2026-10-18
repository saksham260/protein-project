import json, urllib.request
from pathlib import Path
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

bm_urls = {
    "plant-protein": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Plant-Protein-pdp-11.jpg?v=1785496451",
    "titan-whey": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Artboard15.jpg?v=1791792619",
    "gold-whey": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/9_b86a2612-d3fe-4e5a-816c-04222fb3c4b1.jpg?v=1790277827"
}

with open("protein-etl/data/demo_catalog/bm_ocr_details.txt", "w", encoding="utf-8") as f:
    for name, url in bm_urls.items():
        req = urllib.request.Request(url, headers=headers)
        temp_path = Path(f"protein-etl/data/demo_catalog/labels/temp_{name}.jpg")
        temp_path.write_bytes(urllib.request.urlopen(req).read())
        res = ocr(str(temp_path))
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        f.write(f"\n=== {name}: {url} ===\n")
        for line in txts:
            f.write(line + "\n")

print("Saved bm_ocr_details.txt successfully.")
