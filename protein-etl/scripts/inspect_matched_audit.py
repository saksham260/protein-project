import json

audit = json.load(open("protein-etl/data/demo_catalog/audit_batch3_stores.json", encoding="utf-8"))

for store in ["pintola.in", "bagrrys.com", "true-elements.com"]:
    data = audit.get(store, {})
    matched = data.get("matched", [])
    print(f"\n=====================================\n{store} (Total: {data.get('total')}, Matched: {len(matched)})\n=====================================")
    for p in matched[:15]:
        t = p.get("title", "")
        h = p.get("handle", "")
        vars_info = [(v.get("title"), v.get("price")) for v in p.get("variants", [])[:3]]
        print(f"  {h:<50} | {t[:40]:<40} | vars: {vars_info}")
