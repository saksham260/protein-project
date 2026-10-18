"""OCR inspection script for Batch 4C: Fuel One, Kapiva, Bolt Nutrition, XLR8."""
import json
import urllib.request
from pathlib import Path
from PIL import Image
from rapidocr import RapidOCR

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"
IMG_DIR = ROOT / "batch4c_images"
IMG_DIR.mkdir(parents=True, exist_ok=True)
engine = RapidOCR()

ocr_results = {}

def process_image(src, tag):
    dest = IMG_DIR / f"{tag}.jpg"
    try:
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=12) as r:
            dest.write_bytes(r.read())
        
        im = Image.open(dest).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(dest, "JPEG")
        
        lines = engine(str(dest)).txts or []
        nutr = [l for l in lines if any(k in l.lower() for k in ["protein", "energy", "calories", "carbohydrate", "fat", "serving", "ingredients", "bcaa"])]
        if len(nutr) >= 2:
            print(f"  [FOUND NUTRITION] {tag} ({len(lines)} lines)")
            ocr_results[tag] = lines
        else:
            print(f"  [No nutrition] {tag} ({len(lines)} lines)")
    except Exception as e:
        print(f"  [Error] {tag}: {e}")

# 1. Kapiva Testofuel
print("=== OCRing Kapiva ===")
with open(ROOT / "kapiva_testofuel.json", encoding="utf-8") as f:
    kd = json.load(f)
p_imgs = kd.get("product", {}).get("images", {}).get("edges", [])
for idx, edge in enumerate(p_imgs):
    url = edge.get("node", {}).get("urlOriginal") or edge.get("node", {}).get("url")
    if url:
        process_image(url, f"kapiva_testofuel_{idx}")

# 2. Fuel One
print("\n=== OCRing Fuel One ===")
with open(ROOT / "fuelone_products.json", encoding="utf-8") as f:
    fo_prods = json.load(f)
for slug, p in fo_prods.items():
    print(f"Checking {slug}...")
    for idx, img in enumerate(p.get("images", [])):
        url = img.get("o_link") or img.get("l_link")
        if url:
            process_image(url, f"fuelone_{slug}_{idx}")

# 3. Bolt Nutrition
print("\n=== OCRing Bolt Nutrition ===")
with open(ROOT / "bolt_products.json", encoding="utf-8") as f:
    bolt_prods = json.load(f)

bolt_targets = [
    "whey-protein-5lb",
    "whey-isolate-protein-2lb",
    "bolt-fermented-yeast-protein",
    "bolt-plant-protein",
    "protein-bar-22g-protein-cookies-cream"
]
for handle in bolt_targets:
    p = next((x for x in bolt_prods if x.get("handle") == handle), None)
    if not p:
        continue
    print(f"Checking {handle}...")
    for idx, img in enumerate(p.get("images", [])):
        src = img.get("src")
        if src:
            process_image(src, f"bolt_{handle[:15]}_{idx}")

# 4. XLR8
print("\n=== OCRing XLR8 ===")
with open(ROOT / "xlr8_products.json", encoding="utf-8") as f:
    xlr8_prods = json.load(f)
for slug, p in xlr8_prods.items():
    print(f"Checking {slug}...")
    # schema image
    img_obj = p.get("image", {})
    img_url = img_obj.get("url") if isinstance(img_obj, dict) else (img_obj if isinstance(img_obj, str) else None)
    if img_url:
        process_image(img_url, f"xlr8_{slug}_main")
    for idx, src in enumerate(p.get("gallery_images", [])[:8]):
        process_image(src, f"xlr8_{slug}_{idx}")

with open(ROOT / "batch4c_ocr.json", "w", encoding="utf-8") as f:
    json.dump(ocr_results, f, indent=2)

print(f"\nDone OCRing Batch 4C! Found {len(ocr_results)} labels.")
