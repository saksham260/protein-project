import urllib.request, json, re, io
from PIL import Image
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

twt_items = [
    ("unflavoured-30-g-pure-whey-protein-isolate", "https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate"),
    ("unflavored-26g-whey-protein-isolate-concentrate", "https://thewholetruthfoods.com/products/unflavored-26g-whey-protein-isolate-concentrate"),
    ("light-cocoa-24g-whey-protein-isolate-concentrate", "https://thewholetruthfoods.com/products/light-cocoa-24g-whey-protein-isolate-concentrate"),
    ("cold-coffee-24g-whey-protein-isolate-concentrate", "https://thewholetruthfoods.com/products/cold-coffee-24g-whey-protein-isolate-concentrate"),
    ("double-cocoa-25g-plant-protein", "https://thewholetruthfoods.com/products/double-cocoa-25g-plant-protein"),
    ("pista-badaam-24g-plant-protein", "https://thewholetruthfoods.com/products/pista-badaam-24g-plant-protein")
]

with open("protein-etl/data/demo_catalog/twt_tables_ocr.txt", "w", encoding="utf-8") as out:
    for h, page_url in twt_items:
        try:
            html = urllib.request.urlopen(urllib.request.Request(page_url, headers=headers), timeout=10).read().decode("utf-8")
            media_urls = list(set(re.findall(r'(https://media\.thewholetruthfoods\.com/public/backend-assets/[^"\'\s>]+)', html)))
            out.write(f"\n=====================================\nTWT {h} ({len(media_urls)} imgs)\n=====================================\n")
            for u in media_urls:
                if any(k in u for k in ["banner", "logo", "icon"]):
                    continue
                try:
                    clean_u = u.split("?")[0]
                    img = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(clean_u, headers=headers), timeout=8).read())).convert("RGB")
                    img.thumbnail((1600, 1600))
                    temp_p = f"protein-etl/data/demo_catalog/labels/twt_temp.jpg"
                    img.save(temp_p, "JPEG")
                    res = ocr(temp_p)
                    txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
                    joined = " ".join(txts).lower()
                    if any(k in joined for k in ["energy", "protein", "carbohydrate", "fat", "nutrition", "serving size"]):
                        out.write(f"--- IMG: {clean_u} ({len(txts)} lines) ---\n")
                        for t in txts:
                            out.write(f"  {t}\n")
                        print(f"[FOUND] {h}: {clean_u} ({len(txts)} lines)")
                except Exception:
                    pass
        except Exception as e:
            print(f"[ERR] {h}: {e}")

print("Saved twt_tables_ocr.txt")
