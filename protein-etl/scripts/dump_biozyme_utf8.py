import json

data = json.load(open("protein-etl/data/demo_catalog/biozyme_found.json", encoding="utf-8"))
with open("protein-etl/data/demo_catalog/biozyme_dump.txt", "w", encoding="utf-8") as f:
    for idx, item in enumerate(data):
        f.write(f"\n=== ITEM {idx}: {item['url']} ===\n")
        for line in item.get("txts", []):
            f.write(line + "\n")

print("Dumped all biozyme items to biozyme_dump.txt")
