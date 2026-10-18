import urllib.request, io
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
url = "https://www.avvatarindia.com/images/nutrition_images/1759476453_ALPHA_WHEY_NUTRITIONAL_DETAILS_BELGIAN_CHOCOLATE_15-09-25_-02.jpg"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
img = Image.open(io.BytesIO(urllib.request.urlopen(req).read())).convert("RGB")
res = ocr(np.array(img))
txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
with open("protein-etl/data/demo_catalog/alpha_whey_macros.txt", "w", encoding="utf-8") as f:
    for t in txts:
        f.write(t + "\n")
print("Saved alpha_whey_macros.txt")
