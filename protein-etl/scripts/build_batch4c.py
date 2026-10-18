"""Inject Batch 4C products into store_snapshot.json, picks.txt, and readings.jsonl."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog"
SCRATCH = ROOT / "scratch"

# 1. Load existing files
with open(ROOT / "store_snapshot.json", encoding="utf-8") as f:
    snapshot = json.load(f)

picks_lines = [l.strip() for l in (ROOT / "picks.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.strip().startswith("#")]
readings_lines = [json.loads(l) for l in (ROOT / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

start_pick_idx = len(picks_lines)
print(f"Current filtered picks count: {len(picks_lines)} (next pick i = {start_pick_idx + 1})")
print(f"Current readings count: {len(readings_lines)}")

# Load scratch JSONs
with open(SCRATCH / "fuelone_products.json", encoding="utf-8") as f:
    fuelone_prods = json.load(f)

with open(SCRATCH / "kapiva_testofuel.json", encoding="utf-8") as f:
    kapiva_prod = json.load(f).get("product", {})

with open(SCRATCH / "bolt_products.json", encoding="utf-8") as f:
    bolt_prods = json.load(f)

with open(SCRATCH / "xlr8_products.json", encoding="utf-8") as f:
    xlr8_prods = json.load(f)

# 2. Define Batch 4C Products
BATCH_4C = [
    # ==================== FUEL ONE ====================
    {
        "store": "www.fuelone.in",
        "brand": "Fuel One",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "fuelone-whey-max",
        "product_name": "Whey Max Powder",
        "snapshot_entry": {
            "handle": "fuel-one-whey-max",
            "title": "Fuel One Whey Max Powder",
            "url": "https://www.fuelone.in/product/fuel-one-whey-max",
            "images": [{"src": "https://img10.hkrtcdn.com/43673/prd_4367229-Fuel-One-Whey-Max-OP-2.2-lb-Chocolate-Hazelnut_o.jpg"}],
            "variants": [
                {"title": "1 kg / Chocolate Hazelnut", "price": "2319.00", "compare_at_price": "2599.00", "sku": "FO-WMAX-1KG-CH", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "fuel-one-whey-max",
                "variant_name": "1 kg / Chocolate Hazelnut",
                "v_idx": 0,
                "net": 1000,
                "serv": 36.0,
                "label": "1 Scoop (36g)",
                "n": [147.48, 27.0, 4.82, 2.24, 1.46, 0.0, 48.70, 0.0, 2.10, 0.0, 168.34],
                "ing": "Protein Blend (Whey Protein Concentrate & Whey Protein Isolate), Proprietary Enzyme Blend (Amylase, Protease, Lactase, Lipase & Cellulase), Cocoa Powder, Nature-Identical Flavouring Substances, Salt, Sucralose (Sweetener) & Silicon Dioxide (Anticaking Agent)",
                "allergens": ["Milk", "Soy"],
                "tags": ["Vegetarian", "High Protein", "Enzyme Enriched"]
            }
        ]
    },
    {
        "store": "www.fuelone.in",
        "brand": "Fuel One",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "fuelone-iso-max",
        "product_name": "Whey Iso-Max",
        "snapshot_entry": {
            "handle": "fuel-one-iso-max",
            "title": "Fuel One Whey Iso-Max",
            "url": "https://www.fuelone.in/product/fuel-one-iso-max",
            "images": [{"src": "https://img6.hkrtcdn.com/45329/prd_4532865-Fuel-One-Whey-IsoMax-2.2-lb-Chocolate_o.jpg"}],
            "variants": [
                {"title": "1 kg / Chocolate", "price": "3899.00", "compare_at_price": "4999.00", "sku": "FO-ISOMAX-1KG-CH", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "fuel-one-iso-max",
                "variant_name": "1 kg / Chocolate",
                "v_idx": 0,
                "net": 1000,
                "serv": 35.0,
                "label": "1 Scoop (35g)",
                "n": [143.34, 28.0, 4.98, 1.10, 0.96, 0.0, 28.90, 0.0, 1.27, 0.0, 136.22],
                "ing": "Whey Protein Isolate, Cocoa Powder, Nature-Identical Flavouring Substances, Salt, Lecithin, Silicon Dioxide, Sucralose",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "Whey Isolate", "High Protein"]
            }
        ]
    },
    {
        "store": "www.fuelone.in",
        "brand": "Fuel One",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "fuelone-whey-protein",
        "product_name": "Whey Protein",
        "snapshot_entry": {
            "handle": "fuel-one-whey-protein",
            "title": "Fuel One Whey Protein",
            "url": "https://www.fuelone.in/product/fuel-one-whey-protein",
            "images": [{"src": "https://img4.hkrtcdn.com/32384/prd_3238333-Fuel-One-Whey-Protein-2.2-lb-Unflavoured_o.jpg"}],
            "variants": [
                {"title": "1 kg / Unflavoured", "price": "2199.00", "compare_at_price": "2299.00", "sku": "FO-WHEY-1KG-UN", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "fuel-one-whey-protein",
                "variant_name": "1 kg / Unflavoured",
                "v_idx": 0,
                "net": 1000,
                "serv": 35.0,
                "label": "1 Level Scoop (35g)",
                "n": [137.48, 24.0, 6.16, 1.82, 1.23, 0.0, 50.75, 0.0, 2.40, 0.0, 102.16],
                "ing": "Whey Protein Concentrate, Skimmed Milk Powder & Emulsifier (INS 322(i))",
                "allergens": ["Milk", "Soy"],
                "tags": ["Vegetarian", "Raw Whey", "High Protein"]
            }
        ]
    },
    {
        "store": "www.fuelone.in",
        "brand": "Fuel One",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "fuelone-impact-whey",
        "product_name": "Impact Whey Protein",
        "snapshot_entry": {
            "handle": "fuel-one-impact-whey",
            "title": "Fuel One Impact Whey Protein",
            "url": "https://www.fuelone.in/product/fuel-one-impact-whey",
            "images": [{"src": "https://img4.hkrtcdn.com/39209/prd_3920803-Fuel-One-Impact-Whey-Protein-2.2-lb-Chocolate_o.jpg"}],
            "variants": [
                {"title": "1 kg / Chocolate", "price": "1499.00", "compare_at_price": "2199.00", "sku": "FO-IMP-1KG-CH", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "fuel-one-impact-whey",
                "variant_name": "1 kg / Chocolate",
                "v_idx": 0,
                "net": 1000,
                "serv": 45.0,
                "label": "1 Scoop (45g)",
                "n": [172.10, 22.50, 16.11, 1.96, 1.06, 0.0, 39.54, 0.0, 11.00, 0.0, 257.94],
                "ing": "Whey Protein Blend (Whey Protein Concentrate, Whey Powder), Yeast Protein (extracted from Saccharomyces cerevisiae), Skimmed Milk Powder, Cocoa Powder, Nature-Identical Flavouring Substances, Lecithin, Sucralose",
                "allergens": ["Milk", "Soy"],
                "tags": ["Vegetarian", "High Protein"]
            }
        ]
    },

    # ==================== KAPIVA ====================
    {
        "store": "kapiva.in",
        "brand": "Kapiva",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "kapiva-testofuel-whey",
        "product_name": "Testofuel Shilajit Whey Protein",
        "snapshot_entry": {
            "handle": "testofuel-shilajit-whey-protein",
            "title": "Kapiva Testofuel Shilajit Whey Protein",
            "url": "https://kapiva.in/products/testofuel-shilajit-whey-protein",
            "images": [{"src": "https://cdn11.bigcommerce.com/s-5h8rqg02f8/images/stencil/original/products/1038/12701/Testofuel_10__94328.1772428457.jpg"}],
            "variants": [
                {"title": "1 kg / Belgian Chocolate", "price": "3999.00", "compare_at_price": "4149.00", "sku": "POW084", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "testofuel-shilajit-whey-protein",
                "variant_name": "1 kg / Belgian Chocolate",
                "v_idx": 0,
                "net": 1000,
                "serv": 35.0,
                "label": "1 Scoop (35g)",
                "n": [132.98, 25.0, 4.78, 1.54, 1.01, 0.0, 61.67, 0.0, 2.22, 0.0, 151.45],
                "ing": "Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), Shilajit Extract (Fulvic Acid >60%), Black Musli (Curculigo orchioides) Extract, Gokshura (Tribulus terrestris) Extract, DigeZyme Multi-Enzyme Complex, Cocoa Powder, Nature Identical Flavour, Sucralose",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "Ayurvedic Protein", "High Protein"]
            }
        ]
    },

    # ==================== BOLT NUTRITION ====================
    {
        "store": "boltnutritions.com",
        "brand": "Bolt Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "bolt-whey-5lb",
        "product_name": "Whey Protein Powder 5lb",
        "shopify_source": ("bolt_products.json", "whey-protein-5lb"),
        "variants": [
            {
                "handle": "whey-protein-5lb",
                "variant_name": "5 LBS / Piedmont Chocolate",
                "v_idx": 0,
                "net": 2270,
                "serv": 33.0,
                "label": "1 Level Scoop (33g)",
                "n": [136.4, 27.0, 2.3, 2.1, 1.3, 0.0, 77.0, 0.0, 0.0, 0.0, 5.8],
                "ing": "Whey Protein Concentrate (instantized with Sunflower Lecithin), Cocoa Powder, Nature-Identical Flavors, Digestive Enzymes, Sucralose",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein"]
            }
        ]
    },
    {
        "store": "boltnutritions.com",
        "brand": "Bolt Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "bolt-isolate-2lb",
        "product_name": "Whey Isolate Protein Powder 2lb",
        "shopify_source": ("bolt_products.json", "whey-isolate-protein-2lb"),
        "variants": [
            {
                "handle": "whey-isolate-protein-2lb",
                "variant_name": "2LB / Piedmont Chocolate",
                "v_idx": 1,
                "net": 907,
                "serv": 33.0,
                "label": "1 Level Scoop (33g)",
                "n": [123.0, 30.0, 0.5, 0.3, 0.1, 0.0, 5.0, 0.0, 0.0, 0.0, 50.0],
                "ing": "Whey Protein Isolate (USA-sourced), Phycocyanin (Spirulina Extract), Digestive Enzymes, Cocoa Powder, Nature-Identical Flavors, Sucralose",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "Whey Isolate", "High Protein"]
            }
        ]
    },
    {
        "store": "boltnutritions.com",
        "brand": "Bolt Nutrition",
        "category": "protein-powders",
        "is_vegan": True,
        "group": "bolt-fermented-yeast",
        "product_name": "Fermented Yeast Protein",
        "shopify_source": ("bolt_products.json", "bolt-fermented-yeast-protein"),
        "variants": [
            {
                "handle": "bolt-fermented-yeast-protein",
                "variant_name": "2 lb / Cafe Latte",
                "v_idx": 0,
                "net": 907,
                "serv": 33.0,
                "label": "1 Level Scoop (33g)",
                "n": [127.5, 23.1, 6.6, 0.9, 0.6, 0.0, 0.0, 0.0, 3.6, 0.0, 142.8],
                "ing": "Fermented Yeast Protein (Saccharomyces cerevisiae), Phycocyanin (Spirulina extract), Coffee Powder, Natural Flavors, Stevia Extract",
                "allergens": [],
                "tags": ["Vegan", "Fermented Protein", "Dairy Free", "Gluten Free"]
            }
        ]
    },
    {
        "store": "boltnutritions.com",
        "brand": "Bolt Nutrition",
        "category": "protein-powders",
        "is_vegan": True,
        "group": "bolt-biozyme-plant",
        "product_name": "Biozyme Plant Protein Powder",
        "shopify_source": ("bolt_products.json", "bolt-plant-protein"),
        "variants": [
            {
                "handle": "bolt-plant-protein",
                "variant_name": "500gm / Piedmont Chocolate",
                "v_idx": 0,
                "net": 500,
                "serv": 35.0,
                "label": "1 Level Scoop (35g)",
                "n": [129.0, 26.0, 2.8, 1.8, 0.6, 0.0, 0.0, 2.02, 0.0, 0.0, 43.0],
                "ing": "Plant Protein Blend (Pea Protein Isolate, Brown Rice Protein Isolate), Herbal Blend, Digestive Enzymes (Biozyme Technology), Cocoa Powder, Nature Identical Flavors, Sucralose",
                "allergens": [],
                "tags": ["Vegan", "Plant Protein", "Dairy Free", "Gluten Free"]
            }
        ]
    },
    {
        "store": "boltnutritions.com",
        "brand": "Bolt Nutrition",
        "category": "protein-bars",
        "is_vegan": False,
        "group": "bolt-protein-bar",
        "product_name": "Protein Bar 22g Protein Cookies & Cream",
        "shopify_source": ("bolt_products.json", "protein-bar-22g-protein-cookies-cream"),
        "variants": [
            {
                "handle": "protein-bar-22g-protein-cookies-cream",
                "variant_name": "5 Bars / Cookie & Cream",
                "v_idx": 0,
                "net": 315,
                "serv": 63.0,
                "label": "1 Bar (63g)",
                "n": [268.1, 22.0, 25.11, 9.5, 4.51, 0.0, 0.0, 4.03, 13.8, 0.0, 71.4],
                "ing": "Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Milk Protein), Prebiotic Dietary Fiber, Dark Chocolate Coating, Cookies Crumbs, Almonds, Glycerin, Soy Lecithin, Stevia",
                "allergens": ["Milk", "Soy", "Tree Nuts"],
                "tags": ["Vegetarian", "High Protein Bar"]
            }
        ]
    },

    # ==================== XLR8 SPORTS NUTRITION ====================
    {
        "store": "xlr8sport.com",
        "brand": "XLR8 Sports Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "xlr8-whey-4lbs",
        "product_name": "Whey Protein Powder 4 lbs",
        "snapshot_entry": {
            "handle": "xlr8-whey-protein-chocolate",
            "title": "XLR8 Whey Protein Powder 4 lbs",
            "url": "https://xlr8sport.com/products/whey-protein-with-24-g-protein-5-4-g-bcaa",
            "images": [{"src": "https://dukaan.b-cdn.net/700x700/webp/media/253c6f4c-d0b5-492c-8667-3e8aecc4b964.jpg"}],
            "variants": [
                {"title": "4 lbs / Milk Chocolate Fudge", "price": "6499.00", "compare_at_price": "6499.00", "sku": "50656688", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "xlr8-whey-protein-chocolate",
                "variant_name": "4 lbs / Milk Chocolate Fudge",
                "v_idx": 0,
                "net": 1814,
                "serv": 34.0,
                "label": "1 Scoop (34g)",
                "n": [140.0, 24.0, 4.0, 3.0, 0.2, 0.02, 4.8, 0.0, 0.5, 0.5, 51.0],
                "ing": "Whey Protein Concentrate 80 (86%), Chocolate Seasoning, Natural Cocoa Powder, Thickener (INS 460(i)), Sweetener (INS 955 & INS 960), Sodium Chloride",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein", "Lab Certified"]
            }
        ]
    },
    {
        "store": "xlr8sport.com",
        "brand": "XLR8 Sports Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "xlr8-whey-2lbs",
        "product_name": "Whey Protein Powder 2 lbs",
        "snapshot_entry": {
            "handle": "xlr8-whey-protein-cookies-cream",
            "title": "XLR8 Whey Protein Powder 2 lbs",
            "url": "https://xlr8sport.com/products/xlr8-whey-protein-with-24-g-protein-5-4-g-bcaa-cookies-and-cream",
            "images": [{"src": "https://dukaan.b-cdn.net/700x700/webp/media/8c2a3e7e-fd7d-4eda-96e7-6a0fc45e53ee.png"}],
            "variants": [
                {"title": "2 lbs / Cookies & Cream", "price": "3399.00", "compare_at_price": "3399.00", "sku": "50656573", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "xlr8-whey-protein-cookies-cream",
                "variant_name": "2 lbs / Cookies & Cream",
                "v_idx": 0,
                "net": 907,
                "serv": 34.0,
                "label": "1 Scoop (34g)",
                "n": [140.0, 24.0, 4.0, 3.0, 0.3, 0.02, 4.8, 0.0, 0.0, 0.0, 56.1],
                "ing": "Whey Protein Concentrate 80 (88%), Natural Cocoa Powder, Cookies Flavor, Thickener (INS 460(i)), Sweetener (INS 955 & INS 960), Sodium Chloride",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein"]
            }
        ]
    },
    {
        "store": "xlr8sport.com",
        "brand": "XLR8 Sports Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "xlr8-classic-whey",
        "product_name": "Classic Whey Protein Powder 1kg",
        "snapshot_entry": {
            "handle": "xlr8-classic-whey-chocolate",
            "title": "XLR8 Classic Whey Protein Powder 1kg",
            "url": "https://xlr8sport.com/products/xlr8-classic-whey-24-g-protein-5-5-bcaa-chocolate",
            "images": [{"src": "https://dukaan.b-cdn.net/700x700/webp/media/2e740955-bdac-4b4d-b478-83a1a4d328bd.jpeg"}],
            "variants": [
                {"title": "1 kg / Chocolate", "price": "1449.00", "compare_at_price": "1449.00", "sku": "61198295", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "xlr8-classic-whey-chocolate",
                "variant_name": "1 kg / Chocolate",
                "v_idx": 0,
                "net": 1000,
                "serv": 45.0,
                "label": "1 Scoop (45g)",
                "n": [166.0, 24.0, 13.0, 2.0, 0.1, 0.01, 8.1, 0.0, 0.0, 0.0, 150.1],
                "ing": "Whey Blend (Whey Protein Concentrate, Whey Powder), Peanut Protein, Milk Solids, Cocoa Powder, Color (INS 150c), Nature Identical Flavours",
                "allergens": ["Milk", "Peanut"],
                "tags": ["Vegetarian", "High Protein"]
            }
        ]
    },
    {
        "store": "xlr8sport.com",
        "brand": "XLR8 Sports Nutrition",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "xlr8-whey-sachets",
        "product_name": "Whey Protein Powder Pack of 4 Sachets",
        "snapshot_entry": {
            "handle": "xlr8-whey-protein-sachets",
            "title": "XLR8 Whey Protein Powder Pack of 4 Sachets",
            "url": "https://xlr8sport.com/products/xlr8-whey-protein-136gm-4-units-34gm-each",
            "images": [{"src": "https://dukaan.b-cdn.net/700x700/webp/media/95edf8ae-05e4-4562-9298-175f19eef9f4.jpg"}],
            "variants": [
                {"title": "Pack of 4 (136g)", "price": "660.00", "compare_at_price": "660.00", "sku": "58522902", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "xlr8-whey-protein-sachets",
                "variant_name": "Pack of 4 (136g)",
                "v_idx": 0,
                "net": 136,
                "serv": 34.0,
                "label": "1 Sachet (34g)",
                "n": [140.0, 24.0, 4.0, 3.0, 0.2, 0.02, 4.8, 0.0, 0.0, 0.0, 51.0],
                "ing": "Whey Protein Concentrate 80 (80%-89.4%), Milk Solids, Cocoa Powder / Natural Flavours, Thickener (INS 460(i)), Sweetener (INS 955, INS 960)",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein", "Travel Sachet"]
            }
        ]
    },
]

# 3. Update store_snapshot.json
for p in BATCH_4C:
    store = p["store"]
    if store not in snapshot:
        snapshot[store] = []
        print(f"Created new store entry in snapshot: {store}")
    
    if "snapshot_entry" in p:
        entry = p["snapshot_entry"]
        if not any(x["handle"] == entry["handle"] for x in snapshot[store]):
            snapshot[store].append(entry)
            print(f"Added snapshot entry {entry['handle']} to {store}")
    elif "shopify_source" in p:
        src_file, handle = p["shopify_source"]
        with open(SCRATCH / src_file, encoding="utf-8") as sf:
            items = json.load(sf)
        src = next((x for x in items if x.get("handle") == handle), None)
        if not src:
            print(f"WARNING: source handle {handle} not found in {src_file}")
            continue
        
        images = [{"src": img["src"]} for img in src.get("images", []) if "src" in img]
        variants = []
        for v in src.get("variants", []):
            variants.append({
                "title": v.get("title", "Default Title"),
                "price": str(v.get("price", "0.00")),
                "compare_at_price": str(v.get("compare_at_price", "")) if v.get("compare_at_price") else "",
                "sku": v.get("sku", ""),
                "available": v.get("available", True)
            })
        
        entry = {
            "handle": handle,
            "title": src.get("title", ""),
            "url": f"https://{store}/products/{handle}",
            "images": images[:5],
            "variants": variants
        }
        if not any(x["handle"] == entry["handle"] for x in snapshot[store]):
            snapshot[store].append(entry)
            print(f"Added shopify snapshot entry {handle} to {store} ({len(variants)} variants)")

# Save store_snapshot.json
with open(ROOT / "store_snapshot.json", "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2)
print("Updated store_snapshot.json successfully.")

# 4. Generate picks and readings
curr_pick_i = len(picks_lines) + 1
new_picks = []
new_readings = []

for p in BATCH_4C:
    store = p["store"]
    brand = p["brand"]
    category = p["category"]
    group = p["group"]
    prod_name = p["product_name"]
    is_vegan = p["is_vegan"]
    
    for v in p["variants"]:
        handle = v["handle"]
        pick_line = f"{store}|{handle}|{category}|{brand}"
        new_picks.append(pick_line)
        
        reading = {
            "i": curr_pick_i,
            "v": v["v_idx"],
            "g": group,
            "name": prod_name,
            "variant": v["variant_name"],
            "net": v["net"],
            "serv": v["serv"],
            "label": v.get("label", f"{v['serv']}g"),
            "n": v["n"],
            "ing": v["ing"],
            "allergens": v["allergens"],
            "tags": v["tags"],
            "is_vegan": is_vegan
        }
        new_readings.append(reading)
        curr_pick_i += 1

print(f"Adding {len(new_picks)} picks and {len(new_readings)} readings...")

# 5. Append to picks.txt and readings.jsonl
with open(ROOT / "picks.txt", "a", encoding="utf-8") as f:
    for pl in new_picks:
        f.write(pl + "\n")

with open(ROOT / "readings.jsonl", "a", encoding="utf-8") as f:
    for rd in new_readings:
        f.write(json.dumps(rd) + "\n")

print(f"Appended {len(new_picks)} items. New total picks = {len(picks_lines) + len(new_picks)}.")
