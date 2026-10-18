import json
from pathlib import Path
import urllib.request
from rapidocr import RapidOCR
from PIL import Image

ROOT = Path('protein-etl/data/demo_catalog/scratch')
IMG_DIR = ROOT / 'batch4b_images'
IMG_DIR.mkdir(parents=True, exist_ok=True)
engine = RapidOCR()

# 1. Butternut Co targets
with open(ROOT / 'butternut_products.json', encoding='utf-8') as f:
    bn_prods = json.load(f)

bn_targets = [
    'the-butternut-co-natural-peanut-butter-crunchy-1kg-3000000094778',
    'chocolate-peanut-butter-crunchy-200g-no-refined-sugar-nut-butter-health-enthusiasts',
    'the-butternut-co-energy-balls-almond-butter-oats-ebabo211',
    'chocolate-plant-protein-powder-25g-protein-serving-1-kg-vegan-easy-to-digest',
    'the-butternut-co-coffee-caramel-peanut-butter-1000000013459'
]

# 2. Taali targets
with open(ROOT / 'taalifoods_products.json', encoding='utf-8') as f:
    taali_prods = json.load(f)

taali_targets = [
    'taali-protein-puffs-all-flavours-variety-pack-6-flavours-1-pack-each-6-packs-10g-protein-per-pack-roasted-not-fried-no-palm-oil-clean-protein-crunch',
    'masala-mania-pack-of-6',
    'taali-korean-style-protein-puffs-pack-of-6-korean-puff',
    'pudina-pop-60gm-x-3',
    'taali-roasted-peanuts-korean-style-pack-of-4'
]

ocr_results = {}

def process_targets(products, targets, prefix):
    for handle in targets:
        p = next((x for x in products if x.get('handle') == handle), None)
        if not p:
            continue
        print(f"\nProcessing {p.get('title')[:40]} ({handle[:25]})...")
        images = p.get('images', [])
        for idx, img in enumerate(images):
            src = img.get('src')
            if not src:
                continue
            try:
                fname = f"{prefix}_{handle[:15]}_{idx}.jpg"
                dest = IMG_DIR / fname
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as r:
                    dest.write_bytes(r.read())
                
                im = Image.open(dest).convert('RGB')
                im.thumbnail((1600, 1600))
                im.save(dest, 'JPEG')
                
                out = engine(str(dest))
                lines = out.txts or []
                nutr = [l for l in lines if any(k in l.lower() for k in ['energy', 'protein', 'carbohydrate', 'fat', 'serving', 'sugar', 'ingredient', 'calories'])]
                if len(nutr) >= 3:
                    print(f"  -> Found Nutrition in img {idx} ({len(lines)} lines)")
                    ocr_results[f"{prefix}_{handle[:15]}_{idx}"] = {
                        "product": p.get('title'),
                        "handle": handle,
                        "lines": lines
                    }
            except Exception as e:
                pass

print("=== Processing The Butternut Company ===")
process_targets(bn_prods, bn_targets, "bn")

print("\n=== Processing Taali Foods ===")
process_targets(taali_prods, taali_targets, "taali")

with open(ROOT / "bn_taali_ocr.json", "w", encoding="utf-8") as f:
    json.dump(ocr_results, f, indent=2)

print(f"\nDone OCRing Butternut & Taali! Found {len(ocr_results)} labels.")
