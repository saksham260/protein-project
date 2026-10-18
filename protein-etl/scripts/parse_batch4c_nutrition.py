"""Parse and inspect Batch 4C OCR nutrition labels."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"
with open(ROOT / "batch4c_ocr.json", encoding="utf-8") as f:
    ocr_data = json.load(f)

# Group keys by product prefix
products = {
    "kapiva_testofuel": ["kapiva_testofuel_4", "kapiva_testofuel_5"],
    "fuelone_whey_max": ["fuelone_fuel-one-whey-max_1", "fuelone_fuel-one-whey-max_2"],
    "fuelone_iso_max": ["fuelone_fuel-one-iso-max_3", "fuelone_fuel-one-iso-max_4"],
    "fuelone_whey_protein": ["fuelone_fuel-one-whey-protein_4", "fuelone_fuel-one-whey-protein_8"],
    "fuelone_impact_whey": ["fuelone_fuel-one-impact-whey_5", "fuelone_fuel-one-impact-whey_9"],
    "bolt_whey_5lb": ["bolt_whey-protein-5l_8", "bolt_whey-protein-5l_15"],
    "bolt_whey_isolate_2lb": ["bolt_whey-isolate-pr_5", "bolt_whey-isolate-pr_13"],
    "bolt_fermented_yeast": ["bolt_bolt-fermented-_4", "bolt_bolt-fermented-_11"],
    "bolt_plant_protein": ["bolt_bolt-plant-prot_5", "bolt_bolt-plant-prot_12"],
    "bolt_protein_bar": ["bolt_protein-bar-22g_0", "bolt_protein-bar-22g_6"],
    "xlr8_whey_4lbs": ["xlr8_xlr8-whey-protein-chocolate_3", "xlr8_xlr8-whey-protein-chocolate_7"],
    "xlr8_whey_2lbs": ["xlr8_xlr8-whey-protein-cookies-cream_2", "xlr8_xlr8-whey-protein-cookies-cream_3"],
    "xlr8_classic_whey": ["xlr8_xlr8-classic-whey-chocolate_2", "xlr8_xlr8-classic-whey-chocolate_3"],
    "xlr8_sachets": ["xlr8_xlr8-whey-protein-sachets_3", "xlr8_xlr8-whey-protein-sachets_4"],
}

for prod, tags in products.items():
    print(f"\n=======================================================")
    print(f"PRODUCT: {prod}")
    print(f"=======================================================")
    for tag in tags:
        lines = ocr_data.get(tag, [])
        print(f"--- TAG: {tag} ({len(lines)} lines) ---")
        for idx, line in enumerate(lines):
            # Print lines mentioning nutrition terms or ingredients
            if any(k in line.lower() for k in [
                "serving", "energy", "calories", "kcal", "protein", "carbohydrate", 
                "sugar", "fat", "saturated", "trans", "cholesterol", "sodium", 
                "fiber", "dietary", "ingredients", "contains", "blend", "isolate", "concentrate"
            ]):
                print(f"  [{idx:02d}] {line}")
