"""Download and OCR back-of-pack nutrition labels for Batch 4A (One Science, Nutrabay, Plix)."""
import json, re, sys, os
from pathlib import Path
from PIL import Image
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"
img_dir = scratch / "batch4a_images"
img_dir.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def download_and_preprocess(url: str, filename: str) -> Path | None:
    dest = img_dir / filename
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        tmp = img_dir / f"tmp_{filename}"
        tmp.write_bytes(data)
        
        # Preprocess with PIL to RGB JPEG (max 1600x1600)
        im = Image.open(tmp).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(dest, "JPEG", quality=92)
        if tmp.exists():
            tmp.unlink()
        print(f"Downloaded & preprocessed: {filename}")
        return dest
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

# Target label images across Batch 4A
ALL_TARGETS = [
    # One Science Nutrition
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/back_44a5d8b6-2884-4d0c-9860-90fae2759362.png?v=1779193153", "osn_premium_whey_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/WhatsApp_Image_2026-05-19_at_4.56.20_PM.jpg?v=1779193092", "osn_premium_whey_front.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/WhatsApp_Image_2026-05-19_at_11.16.51_AM.jpg?v=1779175335", "osn_iso_gold_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/Image_20260309_175322_313.jpg?v=1775718199", "osn_iso_gold_facts.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/1a_aee738a0-d48f-4951-87fa-c635fe51e0f2.jpg?v=1791286036", "osn_nitra_whey_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/4lb_-_Ripped_whey_-_Venilla_-_Back.png?v=1771328451", "osn_ripped_whey_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/WhatsApp_Image_2026-05-19_at_11.33.20_AM.jpg?v=1779185489", "osn_yeast_protein_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/WhatsApp_Image_2026-05-19_at_11.38.16_AM.jpg?v=1779185565", "osn_plant_protein_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/4_9a351b92-dccf-41f2-8d7a-dc066b20edbb.png?v=1781248985", "osn_oats_label.jpg"),
    ("https://cdn.shopify.com/s/files/1/0952/0483/5648/files/4_653ec3db-4c4f-4ee3-be12-9c1bb82e6d97.png?v=1781249068", "osn_muesli_label.jpg"),

    # Plix
    ("https://plixlifefc-media.farziengineer.co/products/14-db35331cfe894494bad990afe12bbe38.jpg", "plix_evolve_plant_label1.jpg"),
    ("https://plixlifefc-media.farziengineer.co/products/14-12964b83a7cb46b8a2dbcd69ead39081.png", "plix_evolve_plant_label2.png"),
    ("https://plixlifefc-media.farziengineer.co/products/14-69878b0bd256456aa0b0aa15969966ab.png", "plix_evolve_plant_facts.png"),
    ("https://plixlifefc-media.farziengineer.co/products/14-4dc5de02775f40bc912f5d06487b993d.png", "plix_evolve_ingredients.png"),

    # Nutrabay
    ("https://cdn2.nutrabay.com/images/product/nutrabay-gold-100-whey-protein-concentrate/nutrabay-gold-100-whey-protein-concentrate-rich-chocolate-rich-chocolate-1-kg-2-2-lbs-13930510.png", "nb_gold_whey_pack.png"),
    ("https://cdn2.nutrabay.com/images/product/nutrabay-pure-100-pea-protein-isolate/nutrabay-pure-100-pea-protein-isolate-unflavoured-unflavoured-1-kg-2-2-lbs-13930773.png", "nb_pea_protein_pack.png"),
    ("https://cdn2.nutrabay.com/images/product/nutrabay-pure-100-soy-protein-isolate/nutrabay-pure-100-soy-protein-isolate-unflavoured-unflavoured-1-kg-2-2-lbs-13930784.png", "nb_soy_protein_pack.png"),
    ("https://cdn2.nutrabay.com/images/product/nutrabay-yeast-protein/nutrabay-yeast-protein-unflavoured-unflavoured-500-g-1-1-lbs-13931604.png", "nb_yeast_protein_pack.png"),
]

# Run OCR using RapidOCR
from rapidocr import RapidOCR
engine = RapidOCR()

ocr_results = {}

for url, fname in ALL_TARGETS:
    path = download_and_preprocess(url, fname)
    if path and path.exists():
        output = engine(str(path))
        lines = output.txts or []
        ocr_results[fname] = lines
        print(f"OCR {fname}: extracted {len(lines)} lines")

with open(scratch / "batch4a_all_ocr.json", "w", encoding="utf-8") as f:
    json.dump(ocr_results, f, indent=2, ensure_ascii=False)

print("Saved Batch 4A OCR results to scratch/batch4a_all_ocr.json")
