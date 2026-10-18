import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"

with open(scratch / "nb_api_detail.json", encoding="utf-8") as f:
    res = json.load(f)

p = res["data"]
print("Product keys:", list(p.keys()))
print("Name:", p.get("product_name") or p.get("name"))
print("Brand:", p.get("brand_name") or p.get("brand"))
print("Variants:", len(p.get("variants", [])))
for v in p.get("variants", []):
    print(f"  - id: {v.get('id')}, name: {v.get('name') or v.get('variant_name')}, price: {v.get('selling_price')}, mrp: {v.get('market_price')}, sku: {v.get('sku')}, in_stock: {v.get('is_in_stock')}")

print("\nNutrition / Ingredients:")
for k in ["nutrition", "nutritional_info", "supplement_facts", "nutrition_table", "nutrition_details", "ingredients", "directions", "gallery"]:
    if k in p:
        print(f"  {k}: {type(p[k])}")
        if isinstance(p[k], dict):
            print(f"    keys: {list(p[k].keys())[:10]}")
        elif isinstance(p[k], list):
            print(f"    len: {len(p[k])}")
        else:
            print(f"    value: {str(p[k])[:150]}")
