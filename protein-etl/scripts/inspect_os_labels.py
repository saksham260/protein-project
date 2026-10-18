import json
from pathlib import Path
import urllib.request
from rapidocr import RapidOCR
from PIL import Image

ROOT = Path('protein-etl/data/demo_catalog/scratch')
IMG_DIR = ROOT / 'batch4b_images'
IMG_DIR.mkdir(parents=True, exist_ok=True)
engine = RapidOCR()

with open(ROOT / 'opensecret_products.json', encoding='utf-8') as f:
    products = json.load(f)

targets = [
    'daily-whey-blend-of-whey-plant-protein-1kg',
    'open-secret-high-protein-rusk-elaichi-80g',
    'choco-almond-story-box-x5-nutty-cookies',
    'peanut-butter-story-box-x6-nutty-cookies',
    'open-secret-high-protein-healthy-breakfast-oats',
    'open-secret-ragi-chips-chatpata-30g'
]

os_ocr_results = {}

for handle in targets:
    p = next((x for x in products if x.get('handle') == handle), None)
    if not p:
        continue
    print(f"\nProcessing {p.get('title')} ({handle})...")
    images = p.get('images', [])
    for idx, img in enumerate(images):
        src = img.get('src')
        if not src:
            continue
        try:
            fname = f"os_{handle[:20]}_{idx}.jpg"
            dest = IMG_DIR / fname
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                dest.write_bytes(r.read())
            
            im = Image.open(dest).convert('RGB')
            im.thumbnail((1600, 1600))
            im.save(dest, 'JPEG')
            
            out = engine(str(dest))
            lines = out.txts or []
            nutr = [l for l in lines if any(k in l.lower() for k in ['energy', 'protein', 'carbohydrate', 'fat', 'serving size', 'sugar', 'ingredients'])]
            if len(nutr) >= 3:
                print(f"  -> Found Nutrition in img {idx} ({len(lines)} lines)")
                os_ocr_results[f"{handle}_{idx}"] = {
                    "product": p.get('title'),
                    "handle": handle,
                    "lines": lines
                }
        except Exception as e:
            pass

with open(ROOT / "opensecret_ocr.json", "w", encoding="utf-8") as f:
    json.dump(os_ocr_results, f, indent=2)

print(f"\nDone OCRing Open Secret targets! Found {len(os_ocr_results)} labels.")
