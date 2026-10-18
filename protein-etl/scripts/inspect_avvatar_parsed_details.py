import json

data = json.load(open("protein-etl/data/demo_catalog/avvatar_all_parsed.json", encoding="utf-8"))
with open("protein-etl/data/demo_catalog/avvatar_parsed_details.txt", "w", encoding="utf-8") as out:
    for h, panels in data.items():
        out.write(f"\n=====================================\n{h}\n=====================================\n")
        for ptype, pdata in panels.items():
            out.write(f"--- TYPE: {ptype} (URL: {pdata['url']}) ---\n")
            for line in pdata.get("txts", []):
                out.write(f"  {line}\n")

print("Saved avvatar_parsed_details.txt")
