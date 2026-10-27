import json

with open("protein-etl/data/demo_catalog/store_snapshot.json", "r", encoding="utf-8") as f:
    snapshot = json.load(f)

with open("protein-etl/scratch/products_displaying_emoji.json", "r", encoding="utf-8") as f:
    broken_prods = json.load(f)

print(f"Checking {len(broken_prods)} broken products against store_snapshot.json...")

matches_found = 0
for bp in broken_prods:
    slug = bp["slug"]
    name = bp["name"].lower()
    brand = bp["brand"].lower()
    
    found = False
    for store, prods in snapshot.items():
        for p in prods:
            p_handle = p.get("handle", "").lower()
            p_title = p.get("title", "").lower()
            if p_handle in slug or slug in p_handle or (name[:15] in p_title):
                images = p.get("images", [])
                img_src = images[0].get("src") if images else None
                print(f"[FOUND] {bp['name']} ({bp['brand']}) in store '{store}'")
                print(f"   Handle: {p_handle} | Title: {p_title}")
                print(f"   Image: {img_src}")
                matches_found += 1
                found = True
                break
        if found:
            break

print(f"\nTotal matches found in existing snapshot: {matches_found}")
