import json
from pathlib import Path

REPO = Path("c:/Users/Saksham/Documents/new-project")
with open(REPO / "protein-web/src/data/seedCatalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Auditing enriched catalog ({len(catalog)} products)...")

pack_math_issues = []
allergen_stats = {}
dietary_tag_stats = {}
red_flag_stats = {}
zero_ingredients = []

total_v = 0
for p in catalog:
    for v in p.get("variants", []):
        total_v += 1
        name = f"{p.get('name')} [{v.get('variant_name')}]"
        
        # Servings math
        serv_g = v.get("serving_size_g") or 0
        net_g = v.get("net_weight_g") or 0
        spp = v.get("servings_per_pack")
        if spp and serv_g and net_g:
            expected_net = spp * serv_g
            diff_pct = abs(expected_net - net_g) / net_g
            if diff_pct > 0.15:  # allow 15% tolerance for scoops/pack sizes
                pack_math_issues.append((name, f"spp({spp}) * serv({serv_g}g) = {expected_net}g vs net({net_g}g)"))
                
        # Ingredients
        ing = v.get("ingredient_list") or []
        if not ing:
            zero_ingredients.append(name)
            
        # Tags
        for t in v.get("dietary_tags") or []:
            dietary_tag_stats[t] = dietary_tag_stats.get(t, 0) + 1
            
        # Allergens
        for a in v.get("allergens") or []:
            allergen_stats[a] = allergen_stats.get(a, 0) + 1
            
        # Red flags
        for rf in v.get("red_flags") or []:
            rf_id = rf.get("flag_id") or rf.get("name")
            red_flag_stats[rf_id] = red_flag_stats.get(rf_id, 0) + 1

print("\n=== Catalog Enrichment & Integrity Summary ===")
print(f"Total Enriched Variants:     {total_v}")
print(f"Pack Math Inconsistencies:   {len(pack_math_issues)}")
print(f"Variants with 0 Ingredients: {len(zero_ingredients)}")
print(f"Unique Dietary Tags:         {len(dietary_tag_stats)} (Top: {sorted(dietary_tag_stats.items(), key=lambda x: -x[1])[:5]})")
print(f"Unique Allergens Tracked:    {len(allergen_stats)} (Top: {sorted(allergen_stats.items(), key=lambda x: -x[1])[:5]})")
print(f"Red Flags Detected:          {len(red_flag_stats)} (Counts: {red_flag_stats})")

if pack_math_issues:
    print("\nPack Math Issues (sample):")
    for item in pack_math_issues[:5]:
        print(" ", item[0], item[1])
