import json
from pathlib import Path

data = json.load(open("protein-etl/data/demo_catalog/batch2_all_ocr.json", encoding="utf-8"))

out_p = Path("protein-etl/data/demo_catalog/batch2_details_dump.txt")
with open(out_p, "w", encoding="utf-8") as out:
    for i in range(189, 219):
        item = data[str(i)]
        brand = item["brand"]
        handle = item["handle"]
        all_lines = item["n_ocr"] + item["i_ocr"]
        
        out.write(f"\n==================== [{i}] {brand}: {handle} ====================\n")
        ing_text = []
        capture = False
        for l in all_lines:
            if "ingredient" in l.lower():
                capture = True
            if capture:
                ing_text.append(l)
                if len(ing_text) >= 12 or any(term in l.lower() for term in ["allergen", "contains permitted", "manufactured in", "fssai"]):
                    break
        out.write("INGREDIENTS:\n")
        out.write(" ".join(ing_text) if ing_text else "NOT FOUND IN OCR")
        out.write("\n\nNUTRITION SAMPLE:\n")
        out.write(" | ".join(all_lines[:25]) + "\n")

print(f"Written UTF-8 details to {out_p}")
