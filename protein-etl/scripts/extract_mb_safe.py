import urllib.request, io
from PIL import Image
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

mb_targets = {
    "fuel-one": "https://img8.hkrtcdn.com/28330/prd_2832957-MB-Fuel-One-Whey-Protein-2.2-lb-Chocolate_o.jpg",
    "raw-whey": "https://img4.hkrtcdn.com/39859/prd_3985853-MuscleBlaze-80-Raw-Whey-Protein-Supplement-Powder-8.8-lb-Unflavoured_o.jpg",
    "protein-bar-30g": "https://img10.hkrtcdn.com/13966/prd_1396579-MuscleBlaze-HiProtein-Bar-30g-Protein-6-PiecesPack-Choco-Almond_o.jpg",
    "biozyme": "https://img8.hkrtcdn.com/41389/prd_4138827-MuscleBlaze-Biozyme-Performance-Whey-4.4-lb-Rich-Chocolate_o.jpg"
}

with open("protein-etl/data/demo_catalog/mb_safe_ocr.txt", "w", encoding="utf-8") as out:
    for name, u in mb_targets.items():
        req = urllib.request.Request(u, headers=headers)
        img = Image.open(io.BytesIO(urllib.request.urlopen(req).read())).convert("RGB")
        img.thumbnail((1600, 1600))
        save_path = f"protein-etl/data/demo_catalog/labels/mb_{name}_temp.jpg"
        img.save(save_path, "JPEG", quality=95)
        
        res = ocr(save_path)
        txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
        out.write(f"\n=== {name} ({len(txts)} lines) ===\n")
        for line in txts:
            out.write(line + "\n")
        print(f"Extracted MB {name}: {len(txts)} lines")

print("Saved mb_safe_ocr.txt")
