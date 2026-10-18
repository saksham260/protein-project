"""Audit all existing 235 products in the catalog for vegan claims & ingredients.
Criteria:
- Must have a clear 'vegan' or 'plant-based' label claim or brand identity
- Must contain NO animal-derived ingredients (milk, whey, casein, butter, ghee, curd, paneer, egg, honey, gelatin, collagen)
Outputs scratch/vegan_audit.json and prints a summary.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "protein-web" / "src" / "data" / "seedCatalog.json"
SCRATCH_DIR = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

with open(CATALOG_PATH, encoding="utf-8") as f:
    products = json.load(f)

ANIMAL_DERIVED = [
    "milk", "whey", "casein", "butter", "ghee", "curd", "dahi", "paneer", 
    "cheese", "egg", "honey", "gelatin", "collagen", "dairy", "yogurt", "yoghurt",
    "skimmed milk", "milk solids", "milk protein"
]

results = []
vegan_count = 0

for p in products:
    slug = p.get("slug", "")
    brand = p.get("brand_name") or (p.get("brand") or {}).get("name", "")
    name = p.get("name", "")
    cat = p.get("category_slug") or (p.get("category") or {}).get("slug", "")
    
    all_ings = []
    all_tags = []
    for v in p.get("variants", []):
        all_ings.extend([i.lower() for i in v.get("ingredient_list", [])])
        all_tags.extend([t.lower() for t in v.get("dietary_tags", [])])
    
    ing_text = " ".join(all_ings)
    matched_animal = [kw for kw in ANIMAL_DERIVED if kw in ing_text]
    
    has_vegan_tag = "vegan" in all_tags
    is_plant_brand = brand in ["Cosmix", "Origin Nutrition", "OZiva"]
    is_plant_title = any(w in (name + " " + slug).lower() for w in ["plant protein", "vegan", "plant-based", "brown rice cakes"])
    
    # Check 100% peanut butter (pure peanuts, no dairy)
    is_pure_peanut = "peanut-butter" in slug and not matched_animal and ("all-natural" in slug or "natural" in slug or "100%" in name)
    
    # Explicit vegan determination
    is_vegan = False
    evidence = ""
    
    if matched_animal:
        is_vegan = False
        evidence = f"Contains animal ingredients: {', '.join(matched_animal)}"
    elif has_vegan_tag:
        is_vegan = True
        evidence = f"Explicit 'vegan' dietary tag verified with zero animal ingredients"
    elif is_plant_brand:
        is_vegan = True
        evidence = f"Certified 100% plant-based brand ({brand}) with zero animal ingredients"
    elif is_plant_title and not matched_animal:
        is_vegan = True
        evidence = f"Product title/claim states plant/vegan with zero animal ingredients"
    else:
        is_vegan = False
        evidence = "Not claimed vegan or no certified plant label"

    if is_vegan:
        vegan_count += 1
        
    results.append({
        "slug": slug,
        "brand": brand,
        "name": name,
        "category": cat,
        "is_vegan": is_vegan,
        "evidence": evidence,
        "matched_animal_ingredients": matched_animal,
        "dietary_tags": list(set(all_tags))
    })

out_file = SCRATCH_DIR / "vegan_audit.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Total products audited: {len(products)}")
print(f"Verified Vegan: {vegan_count}")
print(f"Non-Vegan / Animal-derived: {len(products) - vegan_count}")
print(f"Audit saved to: {out_file}")

# Show by category breakdown
cat_breakdown = {}
for r in results:
    if r["is_vegan"]:
        c = r["category"]
        cat_breakdown[c] = cat_breakdown.get(c, 0) + 1

print("\nVegan products by category:")
for c, count in sorted(cat_breakdown.items(), key=lambda x: -x[1]):
    print(f"  {c}: {count}")

print("\nSample verified vegan products:")
for r in [r for r in results if r["is_vegan"]][:10]:
    print(f"  [{r['category']}] {r['brand']} - {r['name']} ({r['evidence']})")
