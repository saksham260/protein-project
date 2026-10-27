import json

with open("protein-etl/data/demo_catalog/store_snapshot.json", "r", encoding="utf-8") as f:
    snapshot = json.load(f)

stores_to_check = [
    "oziva.in",
    "thewholetruthfoods.com",
    "optimumnutrition.co.in",
    "bigmusclesnutrition.com",
    "avvatarindia.com",
    "muscleblaze.com",
    "pintola.in",
    "cosmix.in",
    "myfitness.in",
    "getphab.com",
    "maxprotein.in",
    "eatbetterco.com",
    "opensecret.in"
]

for s in stores_to_check:
    prods = snapshot.get(s, [])
    print(f"\n=== Store: {s} ({len(prods)} products) ===")
    for p in prods[:8]:
        img = p.get("images", [{}])[0].get("src") if p.get("images") else None
        print(f"  - handle: {p.get('handle')}")
        print(f"    title: {p.get('title')}")
        print(f"    image: {img}")
        vars = [(v.get("title"), v.get("price"), v.get("compare_at_price")) for v in p.get("variants", [])[:2]]
        print(f"    variants: {vars}")
