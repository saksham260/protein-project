import json
from pathlib import Path
from rapidocr import RapidOCR

ocr = RapidOCR()
LABELS_DIR = Path("protein-etl/data/demo_catalog/labels")
results = {}

for i in range(189, 206):
    n_path = LABELS_DIR / f"{i}_n.jpg"
    i_path = LABELS_DIR / f"{i}_i.jpg"
    
    n_text = []
    if n_path.exists():
        res = ocr(str(n_path))
        boxes = res[0] if isinstance(res, (list, tuple)) and len(res) > 0 and isinstance(res[0], list) else (res if isinstance(res, list) else [])
        n_text = [b[1] for b in boxes if isinstance(b, (list, tuple)) and len(b) > 1]
        
    i_text = []
    if i_path.exists():
        res = ocr(str(i_path))
        boxes = res[0] if isinstance(res, (list, tuple)) and len(res) > 0 and isinstance(res[0], list) else (res if isinstance(res, list) else [])
        i_text = [b[1] for b in boxes if isinstance(b, (list, tuple)) and len(b) > 1]

    results[i] = {
        "n_file": str(n_path.name) if n_path.exists() else None,
        "i_file": str(i_path.name) if i_path.exists() else None,
        "n_ocr": n_text,
        "i_ocr": i_text
    }

out_p = Path("protein-etl/data/demo_catalog/batch2_ocr_189_205.json")
out_p.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Extracted OCR for items 189-205, saved to {out_p}")
