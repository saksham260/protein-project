import json

with open("protein-etl/data/demo_catalog/manual_entries.jsonl", "r", encoding="utf-8") as f:
    manual_entries = [json.loads(line) for line in f if line.strip()]

with open("protein-etl/data/demo_catalog/store_snapshot.json", "r", encoding="utf-8") as f:
    snapshot = json.load(f)

print(f"Comparing {len(manual_entries)} manual entries with store_snapshot...")

discrepancies = []

for m in manual_entries:
    m_handle = m["handle"]
    # Look for matching products in snapshot
    matched_snapshot_prod = None
    for store, prods in snapshot.items():
        for sp in prods:
            if sp.get("handle") == m_handle:
                matched_snapshot_prod = sp
                break
        if matched_snapshot_prod:
            break
            
    if matched_snapshot_prod:
        sp_vars = matched_snapshot_prod.get("variants", [])
        m_vars = m.get("variants", [])
        
        diff = {
            "handle": m_handle,
            "brand": m.get("brand"),
            "manual_vars": m_vars,
            "real_snapshot_vars": [(v.get("title"), v.get("price"), v.get("compare_at_price")) for v in sp_vars]
        }
        discrepancies.append(diff)

print(f"Total exact handle matches in store_snapshot: {len(discrepancies)}")
for d in discrepancies[:10]:
    print(f"\nProduct: {d['brand']} - {d['handle']}")
    print(f"  Manual: {d['manual_vars']}")
    print(f"  Real Snapshot: {d['real_snapshot_vars']}")

