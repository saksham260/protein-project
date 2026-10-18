import json
from pathlib import Path
from rapidocr import RapidOCR
from PIL import Image

IMG_DIR = Path('protein-etl/data/demo_catalog/scratch/batch4a_images')
engine = RapidOCR()

# Scan all png/jpg images in IMG_DIR matching nb_gold_isolate, nb_pure_whey, nb_gold_tri_blend, etc.
found_tables = {}

for img_file in sorted(IMG_DIR.glob('nb_*.jpg')):
    tag = img_file.stem
    try:
        out = engine(str(img_file))
        lines = out.txts or []
        nutr_matches = [l for l in lines if any(k in l.lower() for k in ['per serving', 'nutrition facts', 'nutritional info', 'typical values', 'energy', 'total fat', 'carbohydrate', 'added sugars', 'ingredients:'])]
        if len(nutr_matches) >= 4:
            print(f'*** Found Nutrition Table in {tag} ({len(lines)} lines, {len(nutr_matches)} matches) ***')
            txt_path = IMG_DIR / f'{tag}_full.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            found_tables[tag] = {
                'file': str(img_file.name),
                'matches': nutr_matches,
                'sample': lines[:30]
            }
    except Exception as e:
        print(f'Error processing {img_file.name}:', e)

with open(IMG_DIR / 'all_found_tables.json', 'w', encoding='utf-8') as f:
    json.dump(found_tables, f, indent=2)

print(f'\nTotal nutrition tables found: {len(found_tables)}')
