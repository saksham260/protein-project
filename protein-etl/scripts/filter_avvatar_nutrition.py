import json

data = json.load(open("protein-etl/data/demo_catalog/avvatar_ocr_scans.json", encoding="utf-8"))
with open("protein-etl/data/demo_catalog/avvatar_specific_panels.txt", "w", encoding="utf-8") as out:
    for h, scans in data.items():
        for scan in scans:
            url = scan.get("url", "")
            if "nutrition_images" in url:
                out.write(f"\n=== {h} | {url} ===\n")
                for line in scan.get("txts", []):
                    out.write(line + "\n")

print("Saved avvatar_specific_panels.txt")
