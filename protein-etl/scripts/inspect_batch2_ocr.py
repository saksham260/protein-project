import json, re
from pathlib import Path

data = json.load(open("protein-etl/data/demo_catalog/batch2_all_ocr.json", encoding="utf-8"))

for i in range(189, 219):
    item = data[str(i)]
    brand = item["brand"]
    handle = item["handle"]
    ocr_lines = item["n_ocr"]
    i_lines = item["i_ocr"]
    
    print(f"\n==================== [{i}] {brand}: {handle} ====================")
    # Print the lines that mention numbers or macros
    relevant = []
    for line in ocr_lines:
        lower = line.lower()
        if any(w in lower for w in ["energy", "kcal", "protein", "carbohydrate", "fat", "sugar", "sodium", "cholesterol", "fiber", "serve", "serving", "100g", "approx", "ingredients"]):
            relevant.append(line)
    
    print("\n".join(ocr_lines[:25]))
