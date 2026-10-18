import json

data = json.load(open("protein-etl/data/demo_catalog/avvatar_nut_summary.json", encoding="utf-8"))
with open("protein-etl/data/demo_catalog/avvatar_parsed_labels.txt", "w", encoding="utf-8") as out:
    for h, panels in data.items():
        out.write(f"\n=========================================\n")
        out.write(f"HANDLE: {h}\n")
        out.write(f"=========================================\n")
        for p_idx, p in enumerate(panels):
            out.write(f"\n--- Panel {p_idx} (URL: {p['url']}) ---\n")
            for line in p.get("txts", []):
                out.write(line + "\n")

print("Saved avvatar_parsed_labels.txt")
