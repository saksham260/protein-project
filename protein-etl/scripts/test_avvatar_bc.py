import urllib.request, io
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
url = "https://www.avvatarindia.com/images/nutrition_images/1737610649_1KG%20BC.jpeg"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    data = urllib.request.urlopen(req, timeout=10).read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    print(f"Downloaded! Size: {img.size}")
    res = ocr(np.array(img))
    txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
    print(f"Lines recognized: {len(txts)}")
    with open("protein-etl/data/demo_catalog/bc_1kg_ocr.txt", "w", encoding="utf-8") as f:
        for line in txts:
            f.write(line + "\n")
    print("Saved bc_1kg_ocr.txt")
except Exception as e:
    print("Error:", e)
