import json

# Check BM images
bm = json.load(open("protein-etl/data/demo_catalog/bm_extracted.json", encoding="utf-8"))
for h, p in bm.items():
    print(f"BM {h}:")
    for img in p["images"][:6]:
        print("  ", img["src"])

# Check TWT images
twt = json.load(open("protein-etl/data/demo_catalog/twt_extracted.json", encoding="utf-8"))
for h, p in twt.items():
    print(f"TWT {h}:")
    for img in p["images"]:
        print("  ", img["src"])

# Check Avvatar images
av = json.load(open("protein-etl/data/demo_catalog/avvatar_extracted.json", encoding="utf-8"))
for h, p in list(av.items())[:4]:
    print(f"Avvatar {h}:")
    for img in p["images"][:4]:
        print("  ", img["src"])
