"""Regenerate consistent picks.txt and readings.jsonl from seed_products.json and store_snapshot.json."""

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "protein-etl" / "data" / "demo_catalog"
SEED_FILE = ROOT / "protein-etl" / "data" / "seed_products.json"

NUTRIENT_KEYS = [
    "calories_kcal", "protein_g", "total_carbs_g", "total_fat_g", 
    "saturated_fat_g", "trans_fat_g", "cholesterol_mg", "dietary_fiber_g", 
    "total_sugars_g", "added_sugars_g", "sodium_mg"
]

def main():
    with open(SEED_FILE, encoding="utf-8") as f:
        products = json.load(f)
    
    with open(DATA_DIR / "store_snapshot.json", encoding="utf-8") as f:
        snapshot = json.load(f)
    
    # Build handle-to-store lookup from snapshot
    handle_to_store = {}
    for store, items in snapshot.items():
        for item in items:
            handle_to_store[item["handle"]] = store
    
    picks_lines = []
    readings = []
    
    curr_i = 1
    for p in products:
        brand = p["brand_name"]
        cat = p["category_slug"]
        prod_name = p["name"]
        is_vegan = p.get("is_vegan", False)
        group_key = p.get("slug")
        
        for v_idx, v in enumerate(p["variants"]):
            # Determine store and handle from redirect links or snapshot
            store = None
            handle = None
            
            d2c_link = next((l["url"] for l in v.get("redirect_links", []) if l.get("platform") == "d2c"), None)
            if d2c_link:
                parsed = urlparse(d2c_link)
                store = parsed.netloc
                # Extract handle from path /products/<handle> or /product/<handle>
                parts = parsed.path.strip("/").split("/")
                if len(parts) >= 2 and parts[-2] in ["products", "product"]:
                    handle = parts[-1]
            
            if not handle or not store:
                # Fallback to finding by title/handle in snapshot
                found = False
                for s, items in snapshot.items():
                    for item in items:
                        if item.get("title", "").strip().lower() == prod_name.strip().lower() or item.get("handle") in (p.get("slug", ""), v.get("slug", "")):
                            store = s
                            handle = item["handle"]
                            found = True
                            break
                    if found:
                        break
            
            if not store:
                store = "unknown.com"
            if not handle:
                handle = v.get("slug") or p.get("slug")
            
            # Add to snapshot if missing so build_demo_catalog doesn't fail
            if store not in snapshot:
                snapshot[store] = []
            if not any(x["handle"] == handle for x in snapshot[store]):
                snapshot[store].append({
                    "handle": handle,
                    "title": f"{brand} {prod_name}",
                    "url": d2c_link or f"https://{store}/products/{handle}",
                    "images": [{"src": v.get("image_url") or p.get("image_url")}],
                    "variants": [{
                        "title": v.get("variant_name"),
                        "price": str(v.get("mrp_inr", 0.0)),
                        "compare_at_price": str(v.get("mrp_inr", 0.0)),
                        "sku": v.get("sku") or "",
                        "available": v.get("is_available", True)
                    }]
                })
            
            pick_line = f"{store}|{handle}|{cat}|{brand}"
            picks_lines.append(pick_line)
            
            # Extract 11 nutrients
            nut = v.get("nutrition", {})
            n_vals = [nut.get(k, 0.0) for k in NUTRIENT_KEYS]
            
            d2c_price = next(
                (l.get("platform_price_inr") for l in v.get("redirect_links", [])
                 if l.get("platform") == "d2c" and l.get("platform_price_inr")),
                None
            )
            price_val = float(d2c_price) if d2c_price is not None else float(v.get("mrp_inr", 0.0))
            mrp_val = float(v.get("mrp_inr", price_val))

            prof = v.get("protein_profile") or {}
            
            reading = {
                "i": curr_i,
                "v": v_idx,
                "g": group_key,
                "name": prod_name,
                "variant": v.get("variant_name"),
                "net": float(v.get("net_weight_g", 0.0)),
                "serv": float(v.get("serving_size_g", 0.0)),
                "label": v.get("serving_size_label") or f"{v.get('serving_size_g')}g",
                "price": price_val,
                "mrp": mrp_val,
                "n": n_vals,
                "ing": ", ".join(v.get("ingredient_list", [])) if isinstance(v.get("ingredient_list"), list) else str(v.get("ingredient_list", "")),
                "allergens": v.get("allergens", []),
                "tags": v.get("dietary_tags", []),
                "is_vegan": is_vegan,
                "protein_tier": prof.get("protein_tier"),
                "protein_source": prof.get("primary_protein_source"),
            }
            if nut.get("non_glycemic_polyols_g"):
                reading["poly"] = float(nut["non_glycemic_polyols_g"])
                
            readings.append(reading)
            curr_i += 1

    print(f"Generated {len(picks_lines)} pick lines and {len(readings)} reading lines.")
    
    # Save files
    with open(DATA_DIR / "picks.txt", "w", encoding="utf-8") as f:
        for pl in picks_lines:
            f.write(pl + "\n")
            
    with open(DATA_DIR / "readings.jsonl", "w", encoding="utf-8") as f:
        for rd in readings:
            f.write(json.dumps(rd) + "\n")
            
    with open(DATA_DIR / "store_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
        
    print("Saved picks.txt, readings.jsonl, and store_snapshot.json successfully.")

if __name__ == "__main__":
    main()
