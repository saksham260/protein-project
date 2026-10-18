import json

data = json.load(open("protein-etl/data/demo_catalog/biozyme_found.json", encoding="utf-8"))
for idx, item in enumerate(data):
    txts = item.get("txts", [])
    print(f"Item {idx}: {len(txts)} lines. URL: {item['url']}")
    # print first 5 lines
    for line in txts[:5]:
        print("   ", repr(line))
