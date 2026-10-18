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

nutrition_tables = {}

for pid, tag in target_pids:
    print(f'\n=== Fetching all back label images for {tag} (pid: {pid}) ===')
    pdp_url = f'https://nutrabay.com/api/product-details/product-detail-page?product_id={pid}'
    try:
        req = urllib.request.Request(pdp_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            pdp = json.loads(r.read()).get('data', {})
        
        variants = pdp.get('variants', [])
        if not variants:
            continue
        
        v = variants[0]
        vid = v.get('variant_id')
        v_url = f'https://nutrabay.com/api/product-details/variant-detail?product_id={pid}&variant_id={vid}'
        req_v = urllib.request.Request(v_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req_v, timeout=10) as rv:
            v_data = json.loads(rv.read()).get('data', {})
            
        gallery = v_data.get('gallery', [])
        print(f'  Gallery has {len(gallery)} images')
        
        # Check from back to front (since nutrition label is almost always in the last 2-3 images)
        for idx in range(len(gallery) - 1, 0, -1):
            g_url = gallery[idx]
            try:
                dest_png = IMG_DIR / f'{tag}_img_{idx}.png'
                req_img = urllib.request.Request(g_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_img, timeout=10) as ri:
                    dest_png.write_bytes(ri.read())
                
                im = Image.open(dest_png).convert('RGB')
                im.thumbnail((1800, 1800))
                dest_jpg = IMG_DIR / f'{tag}_img_{idx}.jpg'
                im.save(dest_jpg, 'JPEG')
                
                out = engine(str(dest_jpg))
                lines = out.txts or []
                
                # Check for explicit nutrition table markers
                has_serving = any('serving' in l.lower() for l in lines)
                has_protein = any('protein' in l.lower() for l in lines)
                has_energy = any('energy' in l.lower() or 'calorie' in l.lower() or 'kcal' in l.lower() for l in lines)
                has_facts = any('nutrition' in l.lower() or 'nutrients' in l.lower() or 'ingredients' in l.lower() for l in lines)
                
                if (has_serving and has_protein and (has_energy or has_facts)) or len(lines) > 50:
                    print(f'    -> Found Nutrition/Ingredients in {tag}_img_{idx}.jpg ({len(lines)} lines)!')
                    nutrition_tables[f'{tag}_{idx}'] = {
                        'product_name': v_data.get('parent_name') or v_data.get('name'),
                        'variant_name': v_data.get('name'),
                        'specs': v_data.get('specifications', []),
                        'image_idx': idx,
                        'lines': lines
                    }
                    with open(IMG_DIR / f'{tag}_label_text.json', 'w', encoding='utf-8') as f_out:
                        json.dump(nutrition_tables[f'{tag}_{idx}'], f_out, indent=2)
                    # Don't break immediately if it might be an ingredients panel vs nutrition panel, check up to 2
            except Exception as e:
                pass
    except Exception as e:
        print(f'  Error for {tag}:', e)

with open(ROOT / 'nb_all_extracted_nutrition.json', 'w', encoding='utf-8') as f:
    json.dump(nutrition_tables, f, indent=2)

print('\nDone scanning all Nutrabay back labels!')
