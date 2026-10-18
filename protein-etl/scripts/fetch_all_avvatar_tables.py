import urllib.request, urllib.parse, re, json, io
from pathlib import Path
from PIL import Image
import numpy as np
from rapidocr import RapidOCR

ocr = RapidOCR()
headers = {"User-Agent": "Mozilla/5.0"}

handles = [
    "100-performance-whey-belgain-chocolate-flavour-1-kg",
    "100-performance-whey-belgain-chocolate-flavour-2-kg",
    "100-performance-whey-malai-kulfi-flavour-1-kg",
    "100-performance-whey-cold-coffee-flavour-2-kg",
    "100-performance-whey-unflavored-1-kg",
    "isorich-protein-belgian-chocolate-flavour-1-kg",
    "isorich-protein-malai-kulfi-flavour-1-kg",
    "isorich-protein-chocolate-hazelnut-flavour-1-kg",
    "alpha-whey-belgian-chocolate-flavour-1-kg-2509104129-263",
    "alpha-whey-malai-kulfi-flavour-1-kg",
    "alpha-whey-cold-coffee-flavour-1-kg",
    "protein-wafer-bar-coffee-flavour-320g",
    "protein-wafer-bar-tiramisu-flavour-320g"
]

all_avvatar = {}

for h in handles:
    page_url = f"https://www.avvatarindia.com/product/{h}"
    try:
        html = urllib.request.urlopen(urllib.request.Request(page_url, headers=headers), timeout=10).read().decode("utf-8")
        nut_imgs = list(set(re.findall(r'(/images/nutrition_images/[^"\'\s>]+)', html)))
        
        parsed_panels = {}
        for img_rel in nut_imgs:
            # URL encode path correctly
            full_url = "https://www.avvatarindia.com" + urllib.parse.quote(img_rel)
            try:
                data = urllib.request.urlopen(urllib.request.Request(full_url, headers=headers), timeout=10).read()
                img = Image.open(io.BytesIO(data)).convert("RGB")
                res = ocr(np.array(img))
                txts = list(res.txts) if hasattr(res, "txts") and res.txts else []
                panel_type = "ing" if "ING" in img_rel else ("bcaa" if "BCAA" in img_rel else "nutrition")
                parsed_panels[panel_type] = {"url": full_url, "txts": txts}
            except Exception as e:
                print(f"Error fetching {full_url}: {e}")
        
        all_avvatar[h] = parsed_panels
        print(f"[OK] Avvatar {h}: {list(parsed_panels.keys())}")
    except Exception as e:
        print(f"[ERR] {h}: {e}")

with open("protein-etl/data/demo_catalog/avvatar_all_parsed.json", "w", encoding="utf-8") as f:
    json.dump(all_avvatar, f, indent=2, ensure_ascii=False)

print("Saved avvatar_all_parsed.json")
