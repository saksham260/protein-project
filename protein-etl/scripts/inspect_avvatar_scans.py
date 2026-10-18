import json

data = json.load(open("protein-etl/data/demo_catalog/avvatar_ocr_scans.json", encoding="utf-8"))
summary = {}
for h, outputs in data.items():
    found_nut = []
    for item in outputs:
        txts = item.get("txts", [])
        joined = " ".join(txts).lower()
        if "energy" in joined and "protein" in joined:
            found_nut.append({"url": item.get("url"), "txts": txts})
    summary[h] = found_nut
    print(f"Avvatar {h}: found {len(found_nut)} nutrition panels")

with open("protein-etl/data/demo_catalog/avvatar_nut_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print("Saved avvatar_nut_summary.json")
