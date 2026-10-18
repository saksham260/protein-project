import json
from pathlib import Path
from rapidocr import RapidOCR

ocr = RapidOCR()
LABELS_DIR = Path("protein-etl/data/demo_catalog/labels").resolve()
PICKS_PATH = Path("protein-etl/data/demo_catalog/picks.txt").resolve()
picks = [l.split("|") for l in PICKS_PATH.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]

results = {}

for i in range(189, 219):
    store, handle, cat, brand = picks[i - 1]
    n_path = LABELS_DIR / f"{i}_n.jpg"
    i_path = LABELS_DIR / f"{i}_i.jpg"
    
    n_txts = []
    if n_path.exists():
        res = ocr(str(n_path))
        if hasattr(res, "txts") and res.txts:
            n_txts = list(res.txts)
            
    i_txts = []
    if i_path.exists():
        res = ocr(str(i_path))
        if hasattr(res, "txts") and res.txts:
            i_txts = list(res.txts)
            
    results[i] = {
        "brand": brand,
        "handle": handle,
        "category": cat,
        "n_ocr": n_txts,
        "i_ocr": i_txts
    }
    print(f"[{i}] {brand:<15} {handle:<40} | N lines: {len(n_txts)} | I lines: {len(i_txts)}")

out_path = Path("protein-etl/data/demo_catalog/batch2_all_ocr.json").resolve()
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nAll OCR dumped to {out_path}")
