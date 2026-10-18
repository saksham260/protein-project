import json

data = json.load(open("protein-etl/data/demo_catalog/avvatar_ocr_scans.json", encoding="utf-8"))
with open("protein-etl/data/demo_catalog/avvatar_tables_clean.txt", "w", encoding="utf-8") as out:
    for h, scans in data.items():
        for scan in scans:
            txts = scan.get("txts", [])
            joined = " ".join(txts).lower()
            if any(k in scan.get("url", "").lower() for k in ["bc.jpeg", "mk.jpeg", "cc.jpeg", "table", "nutrition"]) or ("energy" in joined and "protein" in joined):
                out.write(f"\n=== {h} | {scan['url']} ===\n")
                for line in txts:
                    out.write(line + "\n")

print("Saved avvatar_tables_clean.txt")
