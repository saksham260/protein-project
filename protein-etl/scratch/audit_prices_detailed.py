import json

with open("protein-etl/data/demo_catalog/manual_entries.jsonl", "r", encoding="utf-8") as f:
    manual_entries = [json.loads(line) for line in f if line.strip()]

with open("protein-etl/data/demo_catalog/store_snapshot.json", "r", encoding="utf-8") as f:
    snapshot = json.load(f)

# Brand to store mapping
brand_to_stores = {
    "The Whole Truth": ["thewholetruthfoods.com"],
    "Cosmix": ["cosmix.in"],
    "Optimum Nutrition": ["optimumnutrition.co.in"],
    "OZiva": ["oziva.in"],
    "Pintola": ["pintola.in"],
    "MyFitness": ["myfitness.in"],
    "Max Protein": ["maxprotein.in"],
    "Phab": ["getphab.com"],
    "Open Secret": ["opensecret.in"],
    "Bigmuscles Nutrition": ["bigmusclesnutrition.com"],
    "Epigamia": ["epigamia.com", "epigamiastore.com"],
    "Eat Better Co": ["eatbetterco.com"]
}

matches = []

for m in manual_entries:
    brand = m.get("brand")
    stores = brand_to_stores.get(brand, [])
    if not stores:
        continue
        
    m_handle = m["handle"].lower()
    
    # Try finding in those stores
    best_sp = None
    for store in stores:
        for sp in snapshot.get(store, []):
            sp_handle = sp.get("handle", "").lower()
            sp_title = sp.get("title", "").lower()
            # check overlap
            words = [w for w in m_handle.replace(brand.lower().replace(" ", "-"), "").split("-") if len(w) > 3]
            match_count = sum(1 for w in words if w in sp_handle or w in sp_title)
            if match_count >= 2:
                best_sp = sp
                break
        if best_sp:
            break
            
    if best_sp:
        matches.append({
            "manual_handle": m["handle"],
            "brand": brand,
            "manual_vars": m.get("variants"),
            "snapshot_handle": best_sp.get("handle"),
            "snapshot_title": best_sp.get("title"),
            "snapshot_vars": best_sp.get("variants")
        })

print(f"Matched {len(matches)} manual products to real store snapshot products:")
for match in matches:
    print(f"\n--- [{match['brand']}] {match['manual_handle']} ---")
    print(f"Matched Store Product: {match['snapshot_title']} ({match['snapshot_handle']})")
    print(f"Manual variants:")
    for v in match['manual_vars']:
        print(f"   {v.get('title')}: Price INR {v.get('price')}, MRP INR {v.get('mrp')}")
    print(f"Real Snapshot variants:")
    for v in match['snapshot_vars']:
        print(f"   {v.get('title')}: Price INR {v.get('price')}, MRP INR {v.get('compare_at_price')}")

