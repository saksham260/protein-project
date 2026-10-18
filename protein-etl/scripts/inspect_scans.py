import json

data = json.load(open("protein-etl/data/demo_catalog/batch3a_ocr_scans.json", encoding="utf-8"))
print("MB Scans:")
for k, v in data.get("mb", {}).items():
    print(f"  {k}: score={v.get('score')} | url={v.get('url')}")
    print("  Lines:", v.get("txts", [])[:8])

print("\nTWT Scans:")
for k, v in data.get("twt", {}).items():
    print(f"  {k}: score={v.get('score')} | url={v.get('url')}")
    print("  Lines:", v.get("txts", [])[:8])
