import urllib.request, io
from PIL import Image
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

urls = {
    "plant-protein": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Plant-Protein-pdp-11.jpg?v=1785496451",
    "titan-whey": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Artboard15.jpg?v=1791792619",
    "gold-whey": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/9_b86a2612-d3fe-4e5a-816c-04222fb3c4b1.jpg?v=1790277827"
}

with open("protein-etl/data/demo_catalog/bm_safe_ocr.txt", "w", encoding="utf-8") as out:
    for name, u in urls.items():
        req = urllib.request.Request(u, headers=headers)
        img = Image.open(io.BytesIO(urllib.request.urlopen(req).read())).convert("RGB")
        # Resize to max 1600px width/height maintaining aspect ratio
        img.thumbnail((1600, 1600))
        save_path = f"protein-etl/data/demo_catalog/labels/bm_{name}_temp.jpg"
        img.save(save_path, "JPEG", quality=95)
        
        # Run OCR on saved JPEG
        res = ocr(save_path)
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        out.write(f"\n=== {name} ({len(txts)} lines) ===\n")
        for line in txts:
            out.write(line + "\n")
        print(f"Extracted {name}: {len(txts)} lines")

print("Saved bm_safe_ocr.txt")
