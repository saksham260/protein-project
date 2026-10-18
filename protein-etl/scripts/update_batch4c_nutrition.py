"""Update corrected Batch 4C Fuel One nutrition in seed_products.json and seedCatalog.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED_PRODUCTS = ROOT / "protein-etl" / "data" / "seed_products.json"
SEED_CATALOG = ROOT / "protein-web" / "src" / "data" / "seedCatalog.json"

for file_path in [SEED_PRODUCTS, SEED_CATALOG]:
    with open(file_path, encoding="utf-8") as f:
        prods = json.load(f)
    
    updated = 0
    for p in prods:
        if p.get("brand_name") == "Fuel One":
            name = p.get("name")
            if name == "Whey Protein":
                v = p["variants"][0]
                v["nutrition"]["total_carbs_g"] = 6.16
                v["nutrition"]["total_sugars_g"] = 2.40
                updated += 1
                print(f"Updated Fuel One Whey Protein in {file_path.name}")
            elif name == "Impact Whey Protein":
                v = p["variants"][0]
                v["nutrition"]["total_carbs_g"] = 16.11
                v["nutrition"]["total_sugars_g"] = 11.00
                updated += 1
                print(f"Updated Fuel One Impact Whey Protein in {file_path.name}")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(prods, f, indent=2)

print("Successfully updated nutrition values.")
