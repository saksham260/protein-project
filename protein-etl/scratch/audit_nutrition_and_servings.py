import json
import math
from pathlib import Path
from collections import defaultdict
from dotenv import dotenv_values
from supabase import create_client

REPO = Path("c:/Users/Saksham/Documents/new-project")
DATA_DIR = REPO / "protein-etl" / "data" / "demo_catalog"

# Load local files
with open(REPO / "protein-etl/data/seed_products.json", "r", encoding="utf-8") as f:
    seed_products = json.load(f)

with open(REPO / "protein-web/src/data/seedCatalog.json", "r", encoding="utf-8") as f:
    seed_catalog = json.load(f)

picks = [l.split("|") for l in (DATA_DIR / "picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
readings = [json.loads(l) for l in (DATA_DIR / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

print(f"Loaded {len(seed_products)} seed products, {len(readings)} readings.")

# Category density ranges
DENSITY_RANGES = {
    "protein-powders": (50, 100),
    "protein-bars": (12, 45),
    "savory-snacks": (5, 45),
    "rtd-drinks": (4, 15),
    "protein-spreads": (15, 40),
    "breakfast-cereals": (15, 45),
    "dairy": (4, 35),
    "cookies-baked": (10, 45),
    "mass-gainers": (12, 45),
    "adult-nutrition": (10, 45),
    "staples": (12, 60),
}

# 1. Audit Seed Products
math_errors = []
sub_nutrient_errors = []
physical_limit_errors = []
serving_pack_errors = []
density_outliers = []
missing_fields = []

total_variants = 0

for p in seed_products:
    cat = p.get("category_slug", "")
    p_name = f"{p.get('brand_name', '')} - {p.get('name', '')} ({p.get('slug', '')})"
    
    for v in p.get("variants", []):
        total_variants += 1
        v_name = f"{p_name} [{v.get('variant_name', '')}]"
        
        serv = v.get("serving_size_g")
        net = v.get("net_weight_g")
        serv_label = v.get("serving_size_label")
        n = v.get("nutrition")
        
        # Check missing fields
        if serv is None or serv <= 0:
            missing_fields.append((v_name, f"Invalid serving_size_g: {serv}"))
        if net is None or net <= 0:
            missing_fields.append((v_name, f"Invalid net_weight_g: {net}"))
        if not n:
            missing_fields.append((v_name, "Missing nutrition dict"))
            continue
            
        kcal = n.get("calories_kcal", 0) or 0
        prot = n.get("protein_g", 0) or 0
        carbs = n.get("total_carbs_g", 0) or 0
        fat = n.get("total_fat_g", 0) or 0
        sat_fat = n.get("saturated_fat_g")
        trans_fat = n.get("trans_fat_g")
        fiber = n.get("dietary_fiber_g") or 0
        sugar = n.get("total_sugars_g")
        added_sugar = n.get("added_sugars_g")
        poly = n.get("non_glycemic_polyols_g") or 0
        
        # Physical limits
        if serv:
            if prot > serv * 1.02:
                physical_limit_errors.append((v_name, f"Protein ({prot}g) > Serving ({serv}g)"))
            if carbs > serv * 1.05:
                physical_limit_errors.append((v_name, f"Carbs ({carbs}g) > Serving ({serv}g)"))
            if fat > serv * 1.05:
                physical_limit_errors.append((v_name, f"Fat ({fat}g) > Serving ({serv}g)"))
            if cat not in ("rtd-drinks", "dairy") and (prot + carbs + fat) > serv * 1.08:
                physical_limit_errors.append((v_name, f"Macros ({prot+carbs+fat:.1f}g) > Serving ({serv}g)"))
                
        # Serving vs Net
        if serv and net:
            if serv > net * 1.02:
                serving_pack_errors.append((v_name, f"Serving ({serv}g) > Net Pack ({net}g)"))
                
        # Sub-nutrients
        if sat_fat is not None and sat_fat > fat + 0.1:
            sub_nutrient_errors.append((v_name, f"Sat Fat ({sat_fat}g) > Total Fat ({fat}g)"))
        if trans_fat is not None and trans_fat > fat + 0.1:
            sub_nutrient_errors.append((v_name, f"Trans Fat ({trans_fat}g) > Total Fat ({fat}g)"))
        if sugar is not None and sugar > carbs + 0.1:
            sub_nutrient_errors.append((v_name, f"Sugars ({sugar}g) > Total Carbs ({carbs}g)"))
        if added_sugar is not None and sugar is not None and added_sugar > sugar + 0.1:
            sub_nutrient_errors.append((v_name, f"Added Sugar ({added_sugar}g) > Total Sugars ({sugar}g)"))
            
        # Calorie math sanity
        # Standard Atwater: 4P + 4C + 9F (polyols ~2.4, insoluble fiber deduction)
        est_gross = 4 * prot + 4 * carbs + 9 * fat
        est_net = 4 * prot + 4 * max(0.0, carbs - fiber) + 9 * fat - (1.6 * poly)
        min_diff = min(abs(est_gross - kcal), abs(est_net - kcal))
        max_allowed_diff = max(35, 0.25 * kcal)  # allow up to 25% or 35 kcal due to Indian FSSAI rounding
        if min_diff > max_allowed_diff and kcal > 0:
            math_errors.append((v_name, f"Kcal declared: {kcal}, macro calc: {est_gross:.0f} (diff {min_diff:.0f})"))
            
        # Protein density
        if serv and serv > 0:
            density = (prot / serv) * 100
            low, high = DENSITY_RANGES.get(cat, (5, 95))
            if density < low - 5 or density > high + 5:
                density_outliers.append((v_name, f"Density {density:.1f}% outside {cat} range ({low}-{high}%)"))

print("\n" + "="*50)
print("CATALOG NUTRITION & SERVING SIZE AUDIT RESULTS")
print("="*50)
print(f"Total Products Checked: {len(seed_products)}")
print(f"Total Variants Checked: {total_variants}")
print(f"Missing / Invalid Fields:    {len(missing_fields)}")
print(f"Physical Limit Violations:   {len(physical_limit_errors)}")
print(f"Serving vs Pack Errors:      {len(serving_pack_errors)}")
print(f"Sub-Nutrient Inconsistencies:{len(sub_nutrient_errors)}")
print(f"Calorie Math Discrepancies:  {len(math_errors)}")
print(f"Protein Density Outliers:    {len(density_outliers)}")

if missing_fields:
    print("\n--- Missing Fields ---")
    for item in missing_fields[:10]:
        print(" ", item[0], "-->", item[1])

if physical_limit_errors:
    print("\n--- Physical Limit Violations ---")
    for item in physical_limit_errors[:10]:
        print(" ", item[0], "-->", item[1])

if serving_pack_errors:
    print("\n--- Serving vs Pack Errors ---")
    for item in serving_pack_errors[:10]:
        print(" ", item[0], "-->", item[1])

if sub_nutrient_errors:
    print("\n--- Sub-Nutrient Inconsistencies ---")
    for item in sub_nutrient_errors[:10]:
        print(" ", item[0], "-->", item[1])

if math_errors:
    print("\n--- Calorie Math Discrepancies ---")
    for item in math_errors[:10]:
        print(" ", item[0], "-->", item[1])

if density_outliers:
    print("\n--- Protein Density Outliers ---")
    for item in density_outliers:
        print(" ", item[0], "-->", item[1])
