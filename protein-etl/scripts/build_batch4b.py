"""Inject Batch 4B products into store_snapshot.json, picks.txt, and readings.jsonl."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog"
SCRATCH = ROOT / "scratch"

# 1. Load existing files
with open(ROOT / "store_snapshot.json", encoding="utf-8") as f:
    snapshot = json.load(f)

picks_lines = [l.strip() for l in (ROOT / "picks.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
readings_lines = [json.loads(l) for l in (ROOT / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

start_pick_idx = len(picks_lines)  # next 0-based index
print(f"Current picks count: {len(picks_lines)} (next pick i = {start_pick_idx + 1})")
print(f"Current readings count: {len(readings_lines)}")

# 2. Define Batch 4B Products
BATCH_4B = [
    # --- AMUL ADDITIONS ---
    {
        "store": "shop.amul.com",
        "brand": "Amul",
        "category": "dairy",
        "is_vegan": False,
        "group": "amul-hp-milk",
        "product_name": "High Protein Milk",
        "snapshot_entry": {
            "handle": "amul-high-protein-milk",
            "title": "Amul High Protein Milk",
            "url": "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-30",
            "images": [{"src": "https://shop.amul.com/s/62fa94df8c13af2e242eba16/671b30a3caec6f032c8154ed/amul-high-protein-milk.png"}],
            "variants": [
                {"title": "Pack of 30 (250ml)", "price": "750.00", "compare_at_price": "750.00", "sku": "HPMILK_30", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "amul-high-protein-milk",
                "variant_name": "Pack of 30 (250ml)",
                "v_idx": 0,
                "net": 7500,
                "serv": 250.0,
                "n": [225.0, 35.0, 20.0, 0.5, 0.2, 0.0, 5.0, 0.0, 20.0, 0.0, 84.0],
                "ing": "Pasteurised Skimmed Milk, Milk Solids, Beta-Galactosidase, Probiotic Bacterial Culture",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein", "Lactose Free"]
            }
        ]
    },
    {
        "store": "shop.amul.com",
        "brand": "Amul",
        "category": "dairy",
        "is_vegan": False,
        "group": "amul-hp-dahi",
        "product_name": "High Protein Probiotic Dahi",
        "snapshot_entry": {
            "handle": "amul-high-protein-dahi",
            "title": "Amul High Protein Probiotic Dahi",
            "url": "https://shop.amul.com/en/product/amul-high-protein-dahi-400g",
            "images": [{"src": "https://shop.amul.com/s/62fa94df8c13af2e242eba16/671b30a3caec6f032c8154ed/amul-high-protein-dahi.png"}],
            "variants": [
                {"title": "400g Tub", "price": "70.00", "compare_at_price": "70.00", "sku": "HPDAHI_400", "available": True}
            ]
        },
        "variants": [
            {
                "handle": "amul-high-protein-dahi",
                "variant_name": "400g Tub",
                "v_idx": 0,
                "net": 400,
                "serv": 200.0,
                "n": [136.0, 12.6, 20.0, 0.2, 0.1, 0.0, 4.0, 0.0, 20.0, 0.0, 168.0],
                "ing": "Pasteurised Skimmed Milk, Milk Solids, Active Probiotic Culture",
                "allergens": ["Milk"],
                "tags": ["Vegetarian", "High Protein", "Probiotic"]
            }
        ]
    },

    # --- OPEN SECRET ---
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "protein-powders",
        "is_vegan": False,
        "group": "os-dailywhey",
        "product_name": "DailyWHEY+ Blend of Whey + Plant Protein",
        "shopify_source": ("opensecret_products.json", "daily-whey-blend-of-whey-plant-protein-1kg"),
        "variants": [
            {
                "handle": "daily-whey-blend-of-whey-plant-protein-1kg",
                "variant_name": "Chocolate 1kg",
                "v_idx": 0,
                "net": 1000,
                "serv": 35.0,
                "n": [131.0, 24.2, 6.3, 1.0, 0.4, 0.0, 24.7, 2.2, 0.7, 0.0, 69.6],
                "ing": "Whey Protein Concentrate, Pea Protein Isolate, Cocoa Solids, Natural Digestive Blend (Ginger Powder, Fennel Powder, Cinnamon Extract, Fenugreek Extract), Monk Fruit Extract, Steviol Glycosides (INS 960), Himalayan Pink Salt, Stabiliser (Cellulose Gum, Xanthan Gum, Carrageenan)",
                "allergens": ["Milk", "Soy"],
                "tags": ["Vegetarian", "No Added Sugar", "Digestive Enzymes"]
            }
        ]
    },
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "cookies-baked",
        "is_vegan": False,
        "group": "os-rusk-elaichi",
        "product_name": "High Protein Rusk Elaichi",
        "shopify_source": ("opensecret_products.json", "open-secret-high-protein-rusk-elaichi-80g"),
        "variants": [
            {
                "handle": "open-secret-high-protein-rusk-elaichi-80g",
                "variant_name": "Elaichi 80g",
                "v_idx": 0,
                "net": 80,
                "serv": 20.0,
                "n": [79.0, 2.4, 12.2, 2.4, 0.5, 0.0, 0.6, 1.2, 4.4, 4.0, 16.0],
                "ing": "Cereal products (64.7%) [Whole Wheat Atta (58.8%), Suji (5.9%)], Sugar, Rice Bran Oil, Pea Protein Concentrate, Milk Powder, Yeast, Salt, Gluten, Bread Improver, Saunf, Elaichi Powder, Rosemary Extract",
                "allergens": ["Wheat", "Milk"],
                "tags": ["Vegetarian", "High Protein"]
            }
        ]
    },
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "cookies-baked",
        "is_vegan": False,
        "group": "os-choco-almond-cookies",
        "product_name": "Choco Almond Nutty Cookies",
        "shopify_source": ("opensecret_products.json", "choco-almond-story-box-x5-nutty-cookies"),
        "variants": [
            {
                "handle": "choco-almond-story-box-x5-nutty-cookies",
                "variant_name": "Story Box 5 Cookies (62.5g)",
                "v_idx": 0,
                "net": 62.5,
                "serv": 12.5,
                "n": [52.13, 1.39, 5.25, 3.03, 1.12, 0.0, 0.0, 2.91, 2.33, 1.40, 16.38],
                "ing": "Almonds (26%), Dark Compounds (25%) [Sugar, Edible Vegetable Fat (Hydrogenated), Cocoa Solids, Emulsifiers (INS 491, 322)], Peanuts (22%), Honey, Rice Crispies (5%) (Rice Flour, Sugar, Maize Starch, Malt Extract, Salt, Calcium Carbonate), Oligofructose, Sugar, Sunflower Oil, Liquid Glucose, Cocoa Powder, Antioxidants (INS 322), Edible Common Salt, Cocoa Butter",
                "allergens": ["Nuts", "Soy"],
                "tags": ["Vegetarian"]
            }
        ]
    },
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "cookies-baked",
        "is_vegan": False,
        "group": "os-peanut-butter-cookies",
        "product_name": "Peanut Butter Nutty Cookies",
        "shopify_source": ("opensecret_products.json", "peanut-butter-story-box-x6-nutty-cookies"),
        "variants": [
            {
                "handle": "peanut-butter-story-box-x6-nutty-cookies",
                "variant_name": "Story Box 5 Cookies (62.5g)",
                "v_idx": 0,
                "net": 62.5,
                "serv": 12.5,
                "n": [61.0, 1.39, 7.48, 2.86, 1.21, 0.0, 0.0, 0.53, 1.50, 1.26, 21.83],
                "ing": "Milk Compounds (25%) [Sugar, Edible Vegetable Fat (Hydrogenated), Milk Solids, Cocoa Solids, Emulsifier (INS 322)], Peanuts (18.5%), Honey, Oats (15%), Liquid Glucose, Peanut Butter (10%) [Roasted Peanuts, Sugar, Stabilizer (INS 471), Peanut Oil, Iodized Salt], Rice Crispies, Sugar, Maize Starch, Malt Extract, Salt, Calcium Carbonate, Antioxidants (INS 322), Edible Common Salt, Cocoa Butter",
                "allergens": ["Nuts", "Milk", "Soy"],
                "tags": ["Vegetarian"]
            }
        ]
    },
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "breakfast-cereals",
        "is_vegan": True,
        "group": "os-protein-oats",
        "product_name": "High Protein Breakfast Oats",
        "shopify_source": ("opensecret_products.json", "open-secret-high-protein-healthy-breakfast-oats"),
        "variants": [
            {
                "handle": "open-secret-high-protein-healthy-breakfast-oats",
                "variant_name": "Chocolate 1kg",
                "v_idx": 0,
                "net": 1000,
                "serv": 40.0,
                "n": [163.1, 8.9, 25.6, 2.8, 0.5, 0.0, 0.0, 4.3, 6.3, 4.3, 134.4],
                "ing": "Rolled Oats (51%), Oligofructose, Soy Protein, Edible Vegetable Oil (Sunflower Oil), Cocoa Powder, Almonds, Pumpkin Seeds, Black Raisins, Himalayan Pink Salt",
                "allergens": ["Oats", "Soy", "Almonds"],
                "tags": ["Vegan", "Vegetarian", "High Protein"]
            }
        ]
    },
    {
        "store": "opensecret.in",
        "brand": "Open Secret",
        "category": "savory-snacks",
        "is_vegan": True,
        "group": "os-ragi-chips",
        "product_name": "Ragi Chips Chatpata",
        "shopify_source": ("opensecret_products.json", "open-secret-ragi-chips-chatpata-30g"),
        "variants": [
            {
                "handle": "open-secret-ragi-chips-chatpata-30g",
                "variant_name": "Chatpata 30g",
                "v_idx": 0,
                "net": 30,
                "serv": 30.0,
                "n": [164.0, 1.9, 18.0, 10.0, 4.8, 0.0, 0.0, 2.3, 1.9, 0.0, 92.0],
                "ing": "Cracker (Oats Flour, Corn Flour, Rice Flour, Sunflower Oil, Chilly Oil, Sugar, Jowar Flour, Gluten, Sea Salt, Nachni Flour, Bajra Flour, Urad Flour), Sunflower Oil, Seasoning (Chilli, Black Pepper, Oregano, Parsley, Iodized Salt, Garlic, Onion, Sugar, Tamarind Powder, Acidity Regulator E330)",
                "allergens": ["Oats", "Gluten"],
                "tags": ["Vegan", "Vegetarian", "Baked Snacks"]
            }
        ]
    },

    # --- THE BUTTERNUT COMPANY ---
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": False,
        "group": "bn-protein-pb-unsweetened",
        "product_name": "High Protein Peanut Butter (Unsweetened)",
        "shopify_source": ("butternut_products.json", "the-butternut-co-protein-peanut-butter-unsweetened-1000000061059"),
        "variants": [
            {
                "handle": "the-butternut-co-protein-peanut-butter-unsweetened-1000000061059",
                "variant_name": "Crunchy 925g",
                "v_idx": 0,
                "net": 925,
                "serv": 30.0,
                "n": [184.0, 11.0, 5.0, 14.0, 2.0, 0.0, 0.0, 3.0, 1.0, 0.0, 6.0],
                "ing": "Peanuts, Whey Protein Isolate",
                "allergens": ["Peanuts", "Milk"],
                "tags": ["Vegetarian", "No Added Sugar", "High Protein"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": False,
        "group": "bn-protein-pb-choc-fudge",
        "product_name": "High Protein Peanut Butter (Chocolate Fudge)",
        "shopify_source": ("butternut_products.json", "the-butternut-co-protein-peanut-butter-chocolate-procfudge_925g"),
        "variants": [
            {
                "handle": "the-butternut-co-protein-peanut-butter-chocolate-procfudge_925g",
                "variant_name": "Chocolate Fudge 925g",
                "v_idx": 0,
                "net": 925,
                "serv": 30.0,
                "n": [172.0, 10.0, 5.0, 11.0, 1.0, 0.0, 0.0, 2.0, 3.0, 0.0, 72.0],
                "ing": "Peanuts, Whey Protein Isolate, Jaggery, Cocoa Solids, Sea Salt",
                "allergens": ["Peanuts", "Milk"],
                "tags": ["Vegetarian", "High Protein", "No Refined Sugar"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": True,
        "group": "bn-natural-pb",
        "product_name": "Natural Peanut Butter (100% Peanuts)",
        "shopify_source": ("butternut_products.json", "the-butternut-co-natural-peanut-butter-crunchy-1kg-pbcrunchy"),
        "variants": [
            {
                "handle": "the-butternut-co-natural-peanut-butter-crunchy-1kg-pbcrunchy",
                "variant_name": "Crunchy 1kg",
                "v_idx": 0,
                "net": 1000,
                "serv": 15.0,
                "n": [96.0, 5.0, 2.0, 8.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0],
                "ing": "Dry Roasted Peanuts (100%)",
                "allergens": ["Peanuts"],
                "tags": ["Vegan", "Vegetarian", "No Added Sugar", "100% Natural"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": True,
        "group": "bn-natural-almond-butter",
        "product_name": "Natural Almond Butter (100% Almonds)",
        "shopify_source": ("butternut_products.json", "the-butternut-co-natural-almond-butter-creamy-1kg-abcreamy"),
        "variants": [
            {
                "handle": "the-butternut-co-natural-almond-butter-creamy-1kg-abcreamy",
                "variant_name": "Creamy 1kg",
                "v_idx": 0,
                "net": 1000,
                "serv": 15.0,
                "n": [96.0, 4.0, 3.0, 8.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0],
                "ing": "Dry Roasted Almonds (100%)",
                "allergens": ["Almonds"],
                "tags": ["Vegan", "Vegetarian", "No Added Sugar", "100% Natural"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": False,
        "group": "bn-protein-hazelnut",
        "product_name": "Protein Chocolate Hazelnut Spread",
        "shopify_source": ("butternut_products.json", "the-butternut-co-protein-chocolate-hazelnut-spread-prochazlnut_925g"),
        "variants": [
            {
                "handle": "the-butternut-co-protein-chocolate-hazelnut-spread-prochazlnut_925g",
                "variant_name": "Chocolate Hazelnut 925g",
                "v_idx": 0,
                "net": 925,
                "serv": 30.0,
                "n": [177.0, 8.0, 8.0, 13.0, 2.0, 0.0, 0.0, 1.0, 3.0, 0.0, 23.0],
                "ing": "Almonds, Hazelnuts, Whey Protein Isolate, Coconut Sugar, Cocoa Solids, Sea Salt",
                "allergens": ["Almonds", "Hazelnuts", "Milk"],
                "tags": ["Vegetarian", "High Protein", "No Refined Sugar"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-bars",
        "is_vegan": True,
        "group": "bn-energy-balls",
        "product_name": "Energy Balls Almond Butter & Oats",
        "shopify_source": ("butternut_products.json", "the-butternut-co-energy-balls-almond-butter-oats-ebabo211"),
        "variants": [
            {
                "handle": "the-butternut-co-energy-balls-almond-butter-oats-ebabo211",
                "variant_name": "Pack of 6 (288g)",
                "v_idx": 0,
                "net": 288,
                "serv": 24.0,
                "n": [91.0, 4.0, 20.0, 2.0, 0.2, 0.0, 0.0, 2.0, 9.0, 0.0, 10.0],
                "ing": "Dates, Cashews, Rolled Oats, Almond Butter, Raisins, Rice Flour",
                "allergens": ["Cashews", "Oats", "Almonds"],
                "tags": ["Vegan", "Vegetarian", "Clean Label", "No Added Sugar"]
            }
        ]
    },
    {
        "store": "thebutternutcompany.com",
        "brand": "The Butternut Company",
        "category": "protein-spreads",
        "is_vegan": False,
        "group": "bn-coffee-caramel-pb",
        "product_name": "Coffee Caramel Peanut Butter",
        "shopify_source": ("butternut_products.json", "the-butternut-co-coffee-caramel-peanut-butter-1000000013459"),
        "variants": [
            {
                "handle": "the-butternut-co-coffee-caramel-peanut-butter-1000000013459",
                "variant_name": "Crunchy 340g",
                "v_idx": 0,
                "net": 340,
                "serv": 15.0,
                "n": [91.0, 4.0, 3.0, 7.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 27.0],
                "ing": "Peanuts, Jaggery, Milk Solids, Coffee Powder, Sunflower Oil, Natural Cacao Nibs, Cocoa Butter, Salt",
                "allergens": ["Peanuts", "Milk"],
                "tags": ["Vegetarian", "Gluten Free"]
            }
        ]
    },

    # --- TAALI FOODS ---
    {
        "store": "taalifoods.in",
        "brand": "Taali Foods",
        "category": "savory-snacks",
        "is_vegan": True,
        "group": "taali-puffs-masala",
        "product_name": "Protein Puffs Masala Mania",
        "shopify_source": ("taalifoods_products.json", "masala-mania-pack-of-6"),
        "variants": [
            {
                "handle": "masala-mania-pack-of-6",
                "variant_name": "Pack of 6 (360g)",
                "v_idx": 0,
                "net": 360,
                "serv": 28.0,
                "n": [145.0, 5.0, 20.0, 5.0, 1.0, 0.0, 0.0, 2.0, 1.0, 1.0, 221.0],
                "ing": "Protein Puff Blend 73% (Rice, Corn, Soy Protein Isolate, Chickpeas, Lentil, Sorghum), Masala Seasoning 12% (Spices & Condiments (Onion, Chilli, Coriander, Garlic, Cumin), Corn Starch, Iodised Salt, Sugar, Black Salt, Dehydrated Mango Powder, Yeast Extract, Acidity Regulator (INS 330)), Edible Vegetable Oil (Rice Bran Oil / Cottonseed Oil)",
                "allergens": ["Soy"],
                "tags": ["Vegan", "Vegetarian", "Roasted Not Fried", "Gluten Free"]
            }
        ]
    },
    {
        "store": "taalifoods.in",
        "brand": "Taali Foods",
        "category": "savory-snacks",
        "is_vegan": True,
        "group": "taali-puffs-korean",
        "product_name": "Protein Puffs Korean Style",
        "shopify_source": ("taalifoods_products.json", "taali-korean-style-protein-puffs-pack-of-6-korean-puff"),
        "variants": [
            {
                "handle": "taali-korean-style-protein-puffs-pack-of-6-korean-puff",
                "variant_name": "Pack of 6 (360g)",
                "v_idx": 0,
                "net": 360,
                "serv": 28.0,
                "n": [145.0, 5.0, 20.0, 5.0, 1.0, 0.0, 0.0, 2.0, 1.0, 1.0, 221.0],
                "ing": "Protein Puff Blend 74% (Rice, Corn, Soy Protein Isolate, Chickpeas, Lentil, Sorghum), Korean Seasoning (Iodised Salt, Dehydrated Garlic Powder, Sugar, Spices & Condiments (Chilli, Ginger), Dehydrated Onion Powder, Maltodextrin, Fermented Soya Sauce Powder, Hydrolysed Vegetable Protein, Acidity Regulators (INS 330, INS 296), Yeast Extract), Edible Vegetable Oil",
                "allergens": ["Soy"],
                "tags": ["Vegan", "Vegetarian", "Roasted Not Fried", "Gluten Free"]
            }
        ]
    },
    {
        "store": "taalifoods.in",
        "brand": "Taali Foods",
        "category": "savory-snacks",
        "is_vegan": True,
        "group": "taali-makhana-pudina",
        "product_name": "Roasted Makhana Crunch (Pudina Pop)",
        "shopify_source": ("taalifoods_products.json", "pudina-pop-60gm-x-3"),
        "variants": [
            {
                "handle": "pudina-pop-60gm-x-3",
                "variant_name": "Pack of 3 (180g)",
                "v_idx": 0,
                "net": 180,
                "serv": 22.0,
                "n": [97.0, 2.0, 15.0, 3.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 196.0],
                "ing": "Makhana (Popped Water Lily Seeds) (75%), Pudina Seasoning (9%) (Spices & Condiments (Chilli, Coriander, Dry Mango, Cumin, Turmeric, Dried Ginger, Long Pepper, Fenugreek, Mace, Nutmeg), Iodised salt, Black salt, Sugar, Mint Leaves (7%), Acidity Regulator (INS 330)), Edible Vegetable Oil (Olive Oil)",
                "allergens": [],
                "tags": ["Vegan", "Vegetarian", "Roasted Snacks", "Superfood"]
            }
        ]
    },
    {
        "store": "taalifoods.in",
        "brand": "Taali Foods",
        "category": "savory-snacks",
        "is_vegan": True,
        "group": "taali-peanuts-korean",
        "product_name": "Roasted Peanuts Korean Style",
        "shopify_source": ("taalifoods_products.json", "taali-roasted-peanuts-korean-style-pack-of-4"),
        "variants": [
            {
                "handle": "taali-roasted-peanuts-korean-style-pack-of-4",
                "variant_name": "Pack of 4 (560g)",
                "v_idx": 0,
                "net": 560,
                "serv": 35.0,
                "n": [228.0, 8.0, 7.0, 19.0, 4.0, 0.0, 0.0, 1.0, 1.0, 0.0, 231.0],
                "ing": "Peanuts (92%), Korean Style Seasoning (5%) (Iodised Salt, Dehydrated Garlic Powder, Sugar, Spices & Condiments (Chilli, Ginger), Dehydrated Onion Powder, Maltodextrin, Vinegar Powder, Fermented Soya Sauce Powder, Hydrolysed Vegetable Protein, Acidity Regulators (INS 330, INS 296), Yeast Extract), Edible Vegetable Oil (Rice Bran Oil / Cottonseed Oil)",
                "allergens": ["Peanuts", "Soy"],
                "tags": ["Vegan", "Vegetarian", "High Protein", "Roasted"]
            }
        ]
    }
]

# 3. Update store_snapshot.json
for p in BATCH_4B:
    store = p["store"]
    if store not in snapshot:
        snapshot[store] = []
    
    if "snapshot_entry" in p:
        entry = p["snapshot_entry"]
        # Check if already in snapshot
        if not any(x["handle"] == entry["handle"] for x in snapshot[store]):
            snapshot[store].append(entry)
            print(f"Added manual snapshot entry {entry['handle']} to {store}")
    elif "shopify_source" in p:
        json_file, handle = p["shopify_source"]
        with open(SCRATCH / json_file, encoding="utf-8") as f:
            src_prods = json.load(f)
        src = next((x for x in src_prods if x.get("handle") == handle), None)
        if not src:
            raise ValueError(f"Handle {handle} not found in {json_file}")
        
        # Build clean snapshot entry
        images = [{"src": img["src"]} for img in src.get("images", []) if img.get("src")]
        variants = []
        for v in src.get("variants", []):
            price = str(v.get("price", "0.00"))
            compare = str(v.get("compare_at_price") or price)
            variants.append({
                "title": v.get("title", "Default Title"),
                "price": price,
                "compare_at_price": compare,
                "sku": v.get("sku") or "",
                "available": bool(v.get("available", True))
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

for p in BATCH_4B:
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
