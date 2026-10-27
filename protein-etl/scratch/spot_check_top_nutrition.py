import json

targets = [
    'optimum-nutrition-serious-mass-gainer',
    'optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate',
    'dymatize-iso100-hydrolyzed-whey-protein-isolate-gourmet-chocolate',
    'muscleblaze-super-gainer-xxl',
    'muscleblaze-biozyme-iso-zero-low-carb',
    'nutrabay-pure-100-raw-whey-protein-concentrate',
    'the-whole-truth-pure-whey-isolate-unflavoured',
    'cosmix-plant-protein-kerala-vanilla-bean',
    'epigamia-high-protein-greek-yogurt-natural-no-added-sugar',
    'lo-foods-ultra-low-carb-keto-atta-3g-net-carbs'
]

with open('protein-etl/data/seed_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    if p['slug'] in targets:
        v = p['variants'][0]
        n = v['nutrition']
        print(f"=== {p['brand_name']} - {p['name']} ({p['slug']}) ===")
        print(f"  Serving Size: {v['serving_size_g']}g ({v.get('serving_size_label')})")
        print(f"  Net Weight: {v['net_weight_g']}g | MRP: Rs. {v['mrp_inr']}")
        print(f"  Energy: {n['calories_kcal']} kcal | Protein: {n['protein_g']}g")
        print(f"  Carbs: {n['total_carbs_g']}g (Sugar: {n['total_sugars_g']}g) | Fat: {n['total_fat_g']}g | Sodium: {n['sodium_mg']}mg")
        print(f"  Protein Density: {v['computed_metrics']['protein_density_pct']}%")
        print()
