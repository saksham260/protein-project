import json

with open("protein-etl/data/demo_catalog/store_snapshot.json", "r", encoding="utf-8") as f:
    snapshot = json.load(f)

for store in ["kapiva.in", "plixlife.com", "bigmusclesnutrition.com", "epigamia.com", "cosmix.in"]:
    prods = snapshot.get(store, [])
    print(f"\n=================== {store} ({len(prods)} products) ===================")
    for p in prods:
        img = p.get("images", [{}])[0].get("src") if p.get("images") else None
        print(f"handle: {p.get('handle')}")
        print(f"  title: {p.get('title')}")
        print(f"  image: {img}")
        vars = [(v.get("title"), v.get("price"), v.get("compare_at_price")) for v in p.get("variants", [])[:2]]
        print(f"  vars: {vars}")
