import json

audit = json.load(open("protein-etl/data/demo_catalog/audit_batch3_stores.json", encoding="utf-8"))

for store in ["pintola.in", "bagrrys.com", "true-elements.com"]:
    prods = audit.get(store, [])
    print(f"\n=====================================\n{store} ({len(prods)} products)\n=====================================")
    for p in prods:
        t = p.get("title", "")
        h = p.get("handle", "")
        if any(k in t.lower() for k in ["protein", "muesli", "oats", "butter", "cake"]):
            vars_info = [(v.get("title"), v.get("price")) for v in p.get("variants", [])[:3]]
            print(f"  {h:<45} | {t[:40]:<40} | vars: {vars_info}")
