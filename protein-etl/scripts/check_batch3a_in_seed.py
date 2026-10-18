import json

catalog = json.load(open("protein-web/src/data/seedCatalog.json", encoding="utf-8"))
print(f"Total products in seedCatalog: {len(catalog)}")
print("\n--- Products matching Avvatar, Bigmuscles, MuscleBlaze, The Whole Truth ---")
for p in catalog:
    brand = p["brand_name"]
    if brand in ["Avvatar", "Bigmuscles Nutrition", "MuscleBlaze", "The Whole Truth"]:
        name = p["name"]
        vars_count = len(p["variants"])
        def_var = p["variants"][0]
        var_name = def_var.get("variant_name") or def_var.get("name")
        mrp = def_var.get("mrp_inr", 0)
        d2c_price = next((l.get("platform_price_inr") for l in def_var.get("redirect_links", []) if l["platform"] == "d2c"), mrp)
        d2c_link = next((l["url"] for l in def_var.get("redirect_links", []) if l["platform"] == "d2c"), "No D2C")
        print(f"[{brand:<22}] {name[:40]:<40} | {vars_count:2d} vars | Def: {var_name:<25} | Rs {d2c_price:5.0f} | D2C: {d2c_link[:45]}")
