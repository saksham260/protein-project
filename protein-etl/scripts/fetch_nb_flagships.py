import urllib.request
import json
from pathlib import Path
from rapidocr import RapidOCR
from PIL import Image

ROOT = Path('protein-etl/data/demo_catalog/scratch')
IMG_DIR = ROOT / 'batch4a_images'
IMG_DIR.mkdir(parents=True, exist_ok=True)
engine = RapidOCR()

target_pids = [
    (3275798, 'nb_gold_isolate'),
    (7275894, 'nb_pure_whey_raw'),
    (5912065, 'nb_gold_tri_blend'),
    (3302532, 'nb_gold_pea_protein'),
    (6173422, 'nb_yeast_protein'),
    (4698878, 'nb_vegan_superfoods')
]

nutrition_extracted = {}

for pid, tag in target_pids:
    print(f'\n=== Processing {tag} (pid: {pid}) ===')
    pdp_url = f'https://nutrabay.com/api/product-details/product-detail-page?product_id={pid}'
    try:
        req = urllib.request.Request(pdp_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            pdp = json.loads(r.read()).get('data', {})
        
        variants = pdp.get('variants', [])
        if not variants:
            print('  No variants found')
            continue
        
        # Pick the first in-stock variant or first variant
        v = variants[0]
        vid = v.get('variant_id')
        print(f"  Variant {vid}: {v.get('name')}")
        
        v_url = f'https://nutrabay.com/api/product-details/variant-detail?product_id={pid}&variant_id={vid}'
        req_v = urllib.request.Request(v_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req_v, timeout=10) as rv:
            v_data = json.loads(rv.read()).get('data', {})
            
        gallery = v_data.get('gallery', [])
        print(f'  Gallery has {len(gallery)} images')
        
        for idx, g_url in enumerate(gallery):
            try:
                dest_png = IMG_DIR / f'{tag}_{idx}.png'
                req_img = urllib.request.Request(g_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_img, timeout=10) as ri:
                    dest_png.write_bytes(ri.read())
                
                im = Image.open(dest_png).convert('RGB')
                im.thumbnail((1800, 1800))
                dest_jpg = IMG_DIR / f'{tag}_{idx}.jpg'
                im.save(dest_jpg, 'JPEG')
                
                out = engine(str(dest_jpg))
                lines = out.txts or []
                nutr_lines = [l for l in lines if any(k in l.lower() for k in ['serving size', 'energy', 'calories', 'protein', 'carbohydrate', 'total fat', 'ingredients:'])]
                if len(nutr_lines) >= 3:
                    print(f'    -> SUCCESS in image {idx}: {len(lines)} lines, {len(nutr_lines)} nutrition lines')
                    nutrition_extracted[tag] = {
                        'product_name': v_data.get('parent_name') or v_data.get('name'),
                        'variant_name': v_data.get('name'),
                        'specs': v_data.get('specifications', []),
                        'lines': lines
                    }
                    with open(IMG_DIR / f'{tag}_nutrition.json', 'w', encoding='utf-8') as f_out:
                        json.dump(nutrition_extracted[tag], f_out, indent=2)
                    break
            except Exception as e:
                # ignore image download / ocr failure and continue
                pass
    except Exception as e:
        print(f'  Error for {tag}:', e)

with open(ROOT / 'nb_flagship_nutrition_all.json', 'w', encoding='utf-8') as f:
    json.dump(nutrition_extracted, f, indent=2)

print('\nDone processing Nutrabay flagships!')
