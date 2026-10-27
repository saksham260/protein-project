import json
from pathlib import Path

data_dir = Path("protein-etl/data/demo_catalog")

batch_5c = [
    {
        "handle": "epigamia-greek-yogurt-natural",
        "category": "dairy",
        "brand": "Epigamia",
        "manual": {
            "handle": "epigamia-greek-yogurt-natural",
            "store": "manual",
            "brand": "Epigamia",
            "url": "https://www.epigamiastore.com/products/greek-yogurt-natural",
            "image_url": "https://cdn.shopify.com/s/files/1/0607/6029/3565/files/GY_Natural_90g_Front.png",
            "variants": [
                {"id": 1, "title": "90g", "price": 50.0, "mrp": 50.0, "compare_at_price": 50.0, "net_weight_g": 90, "in_stock": True},
                {"id": 2, "title": "400g Tub", "price": 180.0, "mrp": 180.0, "compare_at_price": 180.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": "epigamia-greek-yogurt-natural",
            "serv": 100,
            "net": 90,
            "n": [52, 8.0, 5.0, 0.0, 0.0, 0.0, 5.0, 0.0, 5.0, 0.0, 45.0],
            "label": "100 g",
            "ing": "Pasteurised Double Toned Milk, Milk Solids, Active Live Cultures (Streptococcus thermophilus, Lactobacillus delbrueckii subsp. bulgaricus)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "clean-label", "diabetic-friendly", "no-added-sugar"]
        }
    },
    {
        "handle": "epigamia-greek-yogurt-alphonso-mango",
        "category": "dairy",
        "brand": "Epigamia",
        "manual": {
            "handle": "epigamia-greek-yogurt-alphonso-mango",
            "store": "manual",
            "brand": "Epigamia",
            "url": "https://www.epigamiastore.com/products/greek-yogurt-alphonso-mango",
            "image_url": "https://cdn.shopify.com/s/files/1/0607/6029/3565/files/GY_Mango_90g_Front.png",
            "variants": [
                {"id": 1, "title": "90g", "price": 60.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 90, "in_stock": True}
            ]
        },
        "reading": {
            "i": "epigamia-greek-yogurt-alphonso-mango",
            "serv": 90,
            "net": 90,
            "n": [88, 6.0, 12.0, 1.8, 1.1, 0.0, 6.0, 0.5, 10.5, 4.5, 40.0],
            "label": "90 g",
            "ing": "Pasteurised Double Toned Milk, Alphonso Mango Pulp (15%), Sugar, Milk Solids, Active Live Cultures",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free"]
        }
    },
    {
        "handle": "epigamia-greek-yogurt-wild-blueberry",
        "category": "dairy",
        "brand": "Epigamia",
        "manual": {
            "handle": "epigamia-greek-yogurt-wild-blueberry",
            "store": "manual",
            "brand": "Epigamia",
            "url": "https://www.epigamiastore.com/products/greek-yogurt-wild-blueberry",
            "image_url": "https://cdn.shopify.com/s/files/1/0607/6029/3565/files/GY_Blueberry_90g_Front.png",
            "variants": [
                {"id": 1, "title": "90g", "price": 60.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 90, "in_stock": True}
            ]
        },
        "reading": {
            "i": "epigamia-greek-yogurt-wild-blueberry",
            "serv": 90,
            "net": 90,
            "n": [90, 6.0, 12.5, 1.8, 1.1, 0.0, 6.0, 0.6, 11.0, 5.0, 40.0],
            "label": "90 g",
            "ing": "Pasteurised Double Toned Milk, Blueberry Fruit Preparation (Blueberries, Sugar, Pectin), Milk Solids, Active Live Cultures",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free"]
        }
    },
    {
        "handle": "epigamia-greek-yogurt-strawberry",
        "category": "dairy",
        "brand": "Epigamia",
        "manual": {
            "handle": "epigamia-greek-yogurt-strawberry",
            "store": "manual",
            "brand": "Epigamia",
            "url": "https://www.epigamiastore.com/products/greek-yogurt-strawberry",
            "image_url": "https://cdn.shopify.com/s/files/1/0607/6029/3565/files/GY_Strawberry_90g_Front.png",
            "variants": [
                {"id": 1, "title": "90g", "price": 60.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 90, "in_stock": True}
            ]
        },
        "reading": {
            "i": "epigamia-greek-yogurt-strawberry",
            "serv": 90,
            "net": 90,
            "n": [88, 6.0, 12.0, 1.8, 1.1, 0.0, 6.0, 0.5, 10.5, 4.5, 40.0],
            "label": "90 g",
            "ing": "Pasteurised Double Toned Milk, Strawberry Fruit Crush (Strawberries, Sugar, Lemon Juice, Pectin), Milk Solids, Active Live Cultures",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free"]
        }
    },
    {
        "handle": "milky-mist-greek-yogurt-natural-unsweetened",
        "category": "dairy",
        "brand": "Milky Mist",
        "manual": {
            "handle": "milky-mist-greek-yogurt-natural-unsweetened",
            "store": "manual",
            "brand": "Milky Mist",
            "url": "https://www.milkymist.com/products/greek-yogurt-natural",
            "image_url": "https://www.milkymist.com/cdn/shop/files/GreekYogurtNatural100g_Front.png",
            "variants": [
                {"id": 1, "title": "100g", "price": 45.0, "mrp": 45.0, "compare_at_price": 45.0, "net_weight_g": 100, "in_stock": True},
                {"id": 2, "title": "400g Tub", "price": 160.0, "mrp": 160.0, "compare_at_price": 160.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": "milky-mist-greek-yogurt-natural-unsweetened",
            "serv": 100,
            "net": 100,
            "n": [49, 7.5, 4.8, 0.0, 0.0, 0.0, 4.0, 0.0, 4.8, 0.0, 50.0],
            "label": "100 g",
            "ing": "Pasteurised Skimmed Milk, Milk Solids, Lactic Cultures",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "clean-label", "diabetic-friendly", "no-added-sugar"]
        }
    },
    {
        "handle": "milky-mist-high-protein-paneer",
        "category": "dairy",
        "brand": "Milky Mist",
        "manual": {
            "handle": "milky-mist-high-protein-paneer",
            "store": "manual",
            "brand": "Milky Mist",
            "url": "https://www.milkymist.com/products/high-protein-paneer",
            "image_url": "https://www.milkymist.com/cdn/shop/files/HighProteinPaneer200g_Front.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 125.0, "mrp": 125.0, "compare_at_price": 125.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": "milky-mist-high-protein-paneer",
            "serv": 100,
            "net": 200,
            "n": [142, 24.0, 2.5, 4.0, 2.4, 0.1, 15.0, 0.0, 2.5, 0.0, 35.0],
            "label": "100 g",
            "ing": "Pasteurised Skimmed Milk, Coagulant (Citric Acid)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "keto-friendly", "diabetic-friendly", "no-added-sugar"]
        }
    },
    {
        "handle": "amul-high-protein-rose-shake",
        "category": "dairy",
        "brand": "Amul",
        "manual": {
            "handle": "amul-high-protein-rose-shake",
            "store": "manual",
            "brand": "Amul",
            "url": "https://shop.amul.com/en/browse/protein",
            "image_url": "https://shop.amul.com/media/catalog/product/h/p/hp_rose_shake_front.png",
            "variants": [
                {"id": 1, "title": "200ml (Carton of 30)", "price": 1050.0, "mrp": 1050.0, "compare_at_price": 1050.0, "net_weight_g": 6000, "in_stock": True}
            ]
        },
        "reading": {
            "i": "amul-high-protein-rose-shake",
            "serv": 200,
            "net": 6000,
            "n": [95, 15.0, 8.0, 0.3, 0.2, 0.0, 5.0, 0.0, 8.0, 0.0, 110.0],
            "label": "200 ml",
            "ing": "Standardised Toned Milk, Milk Solids (Isolate/Concentrate), Nature Identical Flavours (Rose), Non-Caloric Sweetener (Sucralose)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "amul-high-protein-cafe-latte-shake",
        "category": "dairy",
        "brand": "Amul",
        "manual": {
            "handle": "amul-high-protein-cafe-latte-shake",
            "store": "manual",
            "brand": "Amul",
            "url": "https://shop.amul.com/en/browse/protein",
            "image_url": "https://shop.amul.com/media/catalog/product/h/p/hp_cafe_latte_front.png",
            "variants": [
                {"id": 1, "title": "200ml (Carton of 30)", "price": 1050.0, "mrp": 1050.0, "compare_at_price": 1050.0, "net_weight_g": 6000, "in_stock": True}
            ]
        },
        "reading": {
            "i": "amul-high-protein-cafe-latte-shake",
            "serv": 200,
            "net": 6000,
            "n": [95, 15.0, 8.0, 0.3, 0.2, 0.0, 5.0, 0.0, 8.0, 0.0, 110.0],
            "label": "200 ml",
            "ing": "Standardised Toned Milk, Milk Solids, Coffee Extract, Non-Caloric Sweetener (Sucralose)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "amul-high-protein-kesar-shake",
        "category": "dairy",
        "brand": "Amul",
        "manual": {
            "handle": "amul-high-protein-kesar-shake",
            "store": "manual",
            "brand": "Amul",
            "url": "https://shop.amul.com/en/browse/protein",
            "image_url": "https://shop.amul.com/media/catalog/product/h/p/hp_kesar_shake_front.png",
            "variants": [
                {"id": 1, "title": "200ml (Carton of 30)", "price": 1050.0, "mrp": 1050.0, "compare_at_price": 1050.0, "net_weight_g": 6000, "in_stock": True}
            ]
        },
        "reading": {
            "i": "amul-high-protein-kesar-shake",
            "serv": 200,
            "net": 6000,
            "n": [95, 15.0, 8.0, 0.3, 0.2, 0.0, 5.0, 0.0, 8.0, 0.0, 110.0],
            "label": "200 ml",
            "ing": "Standardised Toned Milk, Milk Solids, Saffron Extract & Nature Identical Flavours, Non-Caloric Sweetener (Sucralose)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "amul-high-protein-chocolate-milkshake",
        "category": "dairy",
        "brand": "Amul",
        "manual": {
            "handle": "amul-high-protein-chocolate-milkshake",
            "store": "manual",
            "brand": "Amul",
            "url": "https://shop.amul.com/en/browse/protein",
            "image_url": "https://shop.amul.com/media/catalog/product/h/p/hp_chocolate_shake_front.png",
            "variants": [
                {"id": 1, "title": "200ml (Carton of 30)", "price": 1050.0, "mrp": 1050.0, "compare_at_price": 1050.0, "net_weight_g": 6000, "in_stock": True}
            ]
        },
        "reading": {
            "i": "amul-high-protein-chocolate-milkshake",
            "serv": 200,
            "net": 6000,
            "n": [100, 15.0, 9.0, 0.5, 0.3, 0.0, 6.0, 1.0, 8.0, 0.0, 115.0],
            "label": "200 ml",
            "ing": "Standardised Toned Milk, Milk Solids, Cocoa Powder (1.2%), Nature Identical Chocolate Flavours, Non-Caloric Sweetener (Sucralose)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "muscleblaze-fuel-one-protein-shake-hazelnut-cafe",
        "category": "rtd-drinks",
        "brand": "MuscleBlaze",
        "manual": {
            "handle": "muscleblaze-fuel-one-protein-shake-hazelnut-cafe",
            "store": "manual",
            "brand": "MuscleBlaze",
            "url": "https://www.muscleblaze.com/sv/muscleblaze-fuel-one-protein-shake/SP-114251",
            "image_url": "https://img4.hkrtcdn.com/28900/prd_2889913-MuscleBlaze-Fuel-One-Protein-Shake-250-ml-Hazelnut-Cafe_o.jpg",
            "variants": [
                {"id": 1, "title": "250ml", "price": 130.0, "mrp": 130.0, "compare_at_price": 130.0, "net_weight_g": 250, "in_stock": True}
            ]
        },
        "reading": {
            "i": "muscleblaze-fuel-one-protein-shake-hazelnut-cafe",
            "serv": 250,
            "net": 250,
            "n": [107, 18.0, 6.0, 1.2, 0.8, 0.0, 10.0, 0.0, 6.0, 0.0, 120.0],
            "label": "250 ml",
            "ing": "Double Toned Milk, Milk Protein Isolate, Coffee Extract, Hazelnut Flavours, Stabilizers (INS 407), Non-Caloric Sweetener (INS 955)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "muscleblaze-fuel-one-protein-shake-belgian-chocolate",
        "category": "rtd-drinks",
        "brand": "MuscleBlaze",
        "manual": {
            "handle": "muscleblaze-fuel-one-protein-shake-belgian-chocolate",
            "store": "manual",
            "brand": "MuscleBlaze",
            "url": "https://www.muscleblaze.com/sv/muscleblaze-fuel-one-protein-shake/SP-114251",
            "image_url": "https://img6.hkrtcdn.com/28900/prd_2889915-MuscleBlaze-Fuel-One-Protein-Shake-250-ml-Belgian-Chocolate_o.jpg",
            "variants": [
                {"id": 1, "title": "250ml", "price": 130.0, "mrp": 130.0, "compare_at_price": 130.0, "net_weight_g": 250, "in_stock": True}
            ]
        },
        "reading": {
            "i": "muscleblaze-fuel-one-protein-shake-belgian-chocolate",
            "serv": 250,
            "net": 250,
            "n": [113, 18.0, 7.0, 1.5, 1.0, 0.0, 10.0, 1.0, 6.0, 0.0, 125.0],
            "label": "250 ml",
            "ing": "Double Toned Milk, Milk Protein Isolate, Cocoa Powder (1.5%), Belgian Chocolate Flavours, Stabilizers (INS 407, INS 412), Sweetener (INS 955)",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "raw-pressery-high-protein-milkshake-cold-coffee",
        "category": "rtd-drinks",
        "brand": "Raw Pressery",
        "manual": {
            "handle": "raw-pressery-high-protein-milkshake-cold-coffee",
            "store": "manual",
            "brand": "Raw Pressery",
            "url": "https://www.rawpressery.com/products/protein-milkshake-coffee",
            "image_url": "https://www.rawpressery.com/cdn/shop/files/ProteinColdCoffee200ml_Front.png",
            "variants": [
                {"id": 1, "title": "200ml", "price": 120.0, "mrp": 120.0, "compare_at_price": 120.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": "raw-pressery-high-protein-milkshake-cold-coffee",
            "serv": 200,
            "net": 200,
            "n": [111, 18.0, 7.5, 1.0, 0.6, 0.0, 8.0, 0.0, 7.5, 0.0, 95.0],
            "label": "200 ml",
            "ing": "Toned Milk, Milk Protein Concentrate, Robusta Coffee Extract (1.8%), Acidity Regulator (INS 339), Emulsifier (INS 471), Stevia Leaf Extract",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "no-added-sugar"]
        }
    },
    {
        "handle": "phab-high-protein-milkshake-classic-chocolate",
        "category": "rtd-drinks",
        "brand": "Phab",
        "manual": {
            "handle": "phab-high-protein-milkshake-classic-chocolate",
            "store": "manual",
            "brand": "Phab",
            "url": "https://getphab.com/products/protein-milkshake-chocolate",
            "image_url": "https://getphab.com/cdn/shop/files/PhabMilkshakeChoco200ml_Front.png",
            "variants": [
                {"id": 1, "title": "200ml", "price": 110.0, "mrp": 110.0, "compare_at_price": 110.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": "phab-high-protein-milkshake-classic-chocolate",
            "serv": 200,
            "net": 200,
            "n": [103, 17.0, 6.0, 1.2, 0.8, 0.0, 6.0, 1.2, 4.5, 0.0, 110.0],
            "label": "200 ml",
            "ing": "Lactose Free Toned Milk, Milk Protein Isolate, Cocoa Powder, Stabilizers (INS 407), Lactase Enzyme, Vitamin Premix, Stevia Extract",
            "allergens": ["Milk"],
            "tags": ["vegetarian", "gluten-free", "lactose-free", "no-added-sugar"]
        }
    }
]

# Append manual entries
manual_path = data_dir / "manual_entries.jsonl"
existing_manual = manual_path.read_text(encoding="utf-8")
if not existing_manual.endswith("\n"):
    existing_manual += "\n"
new_manual_lines = [json.dumps(x["manual"], ensure_ascii=False) for x in batch_5c]
manual_path.write_text(existing_manual + "\n".join(new_manual_lines) + "\n", encoding="utf-8")

# Append picks
picks_path = data_dir / "picks.txt"
existing_picks = picks_path.read_text(encoding="utf-8")
if not existing_picks.endswith("\n"):
    existing_picks += "\n"
new_picks_lines = [f"manual|{x['handle']}|{x['category']}|{x['brand']}" for x in batch_5c]
picks_path.write_text(existing_picks + "\n".join(new_picks_lines) + "\n", encoding="utf-8")

# Append readings
readings_path = data_dir / "readings.jsonl"
existing_readings = readings_path.read_text(encoding="utf-8")
if not existing_readings.endswith("\n"):
    existing_readings += "\n"
new_readings_lines = [json.dumps(x["reading"], ensure_ascii=False) for x in batch_5c]
readings_path.write_text(existing_readings + "\n".join(new_readings_lines) + "\n", encoding="utf-8")

print(f"Batch 5C appended successfully: {len(batch_5c)} items.")
