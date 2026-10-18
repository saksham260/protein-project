import json

data = json.load(open("protein-etl/data/demo_catalog/biozyme_found.json", encoding="utf-8"))
print(f"Total panels found: {len(data)}")
for idx, item in enumerate(data):
    txts = item.get("txts", [])
    joined = " ".join(txts)
    if "serving size" in joined.lower() or "servings per" in joined.lower() or "energy" in joined.lower():
        print(f"\n--- Item {idx}: {item['url']} ---")
        for line in txts[:15]:
            print(" ", repr(line))
