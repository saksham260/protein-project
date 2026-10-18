import json, urllib.request, io
from pathlib import Path
from PIL import Image

HERE = Path("protein-etl/data/demo_catalog")
PICKS_PATH = HERE / "picks.txt"
READINGS_PATH = HERE / "readings.jsonl"
LABELS_DIR = HERE / "labels"
LABELS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Define the 31 picks lines
NEW_PICKS = [
    # Avvatar Performance Whey (6 variants)
    ("avvatarindia.com", "100-performance-whey-belgain-chocolate-flavour-1-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "100-performance-whey-belgain-chocolate-flavour-2-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "100-performance-whey-malai-kulfi-flavour-1-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "100-performance-whey-malai-kulfi-flavour-2-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "100-performance-whey-cold-coffee-flavour-2-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "100-performance-whey-unflavored-1-kg", "protein-powders", "Avvatar"),
    # Avvatar ISORICH (5 variants)
    ("avvatarindia.com", "isorich-protein-belgian-chocolate-flavour-1-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "isorich-protein-belgian-chocolate-flavour-2-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "isorich-protein-malai-kulfi-flavour-1-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "isorich-protein-malai-kulfi-flavour-2-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "isorich-protein-chocolate-hazelnut-flavour-1-kg", "protein-powders", "Avvatar"),
    # Avvatar Alpha Whey (4 variants)
    ("avvatarindia.com", "alpha-whey-belgian-chocolate-flavour-1-kg-2509104129-263", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "alpha-whey-belgian-chocolate-flavour-2-kg-2509104551-890", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "alpha-whey-malai-kulfi-flavour-1-kg", "protein-powders", "Avvatar"),
    ("avvatarindia.com", "alpha-whey-cold-coffee-flavour-1-kg", "protein-powders", "Avvatar"),
    # Avvatar Wafer Bar (2 variants)
    ("avvatarindia.com", "protein-wafer-bar-coffee-flavour-320g", "protein-bars", "Avvatar"),
    ("avvatarindia.com", "protein-wafer-bar-tiramisu-flavour-320g", "protein-bars", "Avvatar"),
    # MuscleBlaze (4 products)
    ("muscleblaze.com", "muscleblaze-biozyme-performance-whey", "protein-powders", "MuscleBlaze"),
    ("muscleblaze.com", "fuel-one-whey-protein", "protein-powders", "MuscleBlaze"),
    ("muscleblaze.com", "muscleblaze-100-clean-raw-whey-protein-concentrate", "protein-powders", "MuscleBlaze"),
    ("muscleblaze.com", "muscleblaze-hi-protein-bar-30g-protein", "protein-bars", "MuscleBlaze"),
    # Bigmuscles Nutrition (3 products)
    ("bigmusclesnutrition.com", "premium-gold-whey-protein-1", "protein-powders", "Bigmuscles Nutrition"),
    ("bigmusclesnutrition.com", "titan-whey", "protein-powders", "Bigmuscles Nutrition"),
    ("bigmusclesnutrition.com", "plant-protein-isolate-vegan-protein-powder-clean-recovery-pea-brown-rice-protein-copy", "protein-powders", "Bigmuscles Nutrition"),
    # The Whole Truth (6 picks -> 3 products)
    ("thewholetruthfoods.com", "unflavoured-30-g-pure-whey-protein-isolate", "protein-powders", "The Whole Truth"),
    ("thewholetruthfoods.com", "unflavored-26g-whey-protein-isolate-concentrate", "protein-powders", "The Whole Truth"),
    ("thewholetruthfoods.com", "light-cocoa-24g-whey-protein-isolate-concentrate", "protein-powders", "The Whole Truth"),
    ("thewholetruthfoods.com", "cold-coffee-24g-whey-protein-isolate-concentrate", "protein-powders", "The Whole Truth"),
    ("thewholetruthfoods.com", "double-cocoa-25g-plant-protein", "protein-powders", "The Whole Truth"),
    ("thewholetruthfoods.com", "pista-badaam-24g-plant-protein", "protein-powders", "The Whole Truth"),
]

# 2. Define the corresponding readings
NEW_READINGS = [
    # 219: Avvatar Performance Whey Belgian Choc 1kg
    {
        "i": 219, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Belgian Chocolate 1kg",
        "net": 1000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 4274, "mrp": 6649,
        "n": [137.0, 25.0, 4.5, 2.1, 1.3, 0.1, 5.6, 0.0, 0.0, 0.0, 174.0],
        "ing": "Whey Protein concentrate, Alkalized Cocoa Powder, lodized salt, Acesulfame potassium (INS 950), Sucralose (INS 955), Stabilizer (INS 413, INS 416), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 220: Avvatar Performance Whey Belgian Choc 2kg
    {
        "i": 220, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Belgian Chocolate 2kg",
        "net": 2000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 8397, "mrp": 12899,
        "n": [137.0, 25.0, 4.5, 2.1, 1.3, 0.1, 5.6, 0.0, 0.0, 0.0, 174.0],
        "ing": "Whey Protein concentrate, Alkalized Cocoa Powder, lodized salt, Acesulfame potassium (INS 950), Sucralose (INS 955), Stabilizer (INS 413, INS 416), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 221: Avvatar Performance Whey Malai Kulfi 1kg
    {
        "i": 221, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Malai Kulfi 1kg",
        "net": 1000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 4274, "mrp": 6649,
        "n": [141.0, 27.5, 3.8, 1.9, 1.2, 0.0, 5.0, 0.0, 0.0, 0.0, 68.0],
        "ing": "Whey Protein concentrate, Stabilizer (INS 413, INS 416), lodized salt, Acesulfame potassium (INS 950), Sucralose (INS 955), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 222: Avvatar Performance Whey Malai Kulfi 2kg
    {
        "i": 222, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Malai Kulfi 2kg",
        "net": 2000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 8397, "mrp": 12899,
        "n": [141.0, 27.5, 3.8, 1.9, 1.2, 0.0, 5.0, 0.0, 0.0, 0.0, 68.0],
        "ing": "Whey Protein concentrate, Stabilizer (INS 413, INS 416), lodized salt, Acesulfame potassium (INS 950), Sucralose (INS 955), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 223: Avvatar Performance Whey Cold Coffee 2kg
    {
        "i": 223, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Cold Coffee 2kg",
        "net": 2000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 8397, "mrp": 12899,
        "n": [138.0, 25.0, 4.2, 2.0, 1.2, 0.0, 5.2, 0.0, 0.0, 0.0, 85.0],
        "ing": "Whey Protein concentrate, Coffee Powder, lodized salt, Acesulfame potassium (INS 950), Sucralose (INS 955), Stabilizer (INS 413, INS 416), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 224: Avvatar Performance Whey Unflavoured 1kg
    {
        "i": 224, "g": "avvatar-performance-whey", "name": "100% Performance Whey Protein", "variant": "Raw Unflavoured 1kg",
        "net": 1000, "serv": 30, "label": "1 scoop (30g)", "price": 3899, "mrp": 6749,
        "n": [120.0, 24.0, 1.8, 1.8, 1.1, 0.0, 4.8, 0.0, 0.0, 0.0, 58.0],
        "ing": "Whey Protein Concentrate, Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 225: Avvatar ISORICH Belgian Choc 1kg
    {
        "i": 225, "g": "avvatar-isorich", "name": "ISORICH Whey Protein Isolate", "variant": "Belgian Chocolate 1kg",
        "net": 1000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 5600, "mrp": 10399,
        "n": [130.0, 29.0, 1.3, 1.0, 0.7, 0.0, 2.8, 0.0, 0.0, 0.0, 100.0],
        "ing": "Whey Protein Isolate, Cocoa Powder, lodized Salt, Acesulfame Potassium (INS 950), Sucralose (INS 955), Stabilizers (INS 415, INS 417), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 226: Avvatar ISORICH Belgian Choc 2kg
    {
        "i": 226, "g": "avvatar-isorich", "name": "ISORICH Whey Protein Isolate", "variant": "Belgian Chocolate 2kg",
        "net": 2000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 11200, "mrp": 19149,
        "n": [130.0, 29.0, 1.3, 1.0, 0.7, 0.0, 2.8, 0.0, 0.0, 0.0, 100.0],
        "ing": "Whey Protein Isolate, Cocoa Powder, lodized Salt, Acesulfame Potassium (INS 950), Sucralose (INS 955), Stabilizers (INS 415, INS 417), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 227: Avvatar ISORICH Malai Kulfi 1kg
    {
        "i": 227, "g": "avvatar-isorich", "name": "ISORICH Whey Protein Isolate", "variant": "Malai Kulfi 1kg",
        "net": 1000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 5600, "mrp": 10399,
        "n": [130.0, 29.0, 1.3, 1.0, 0.7, 0.0, 2.8, 0.0, 0.0, 0.0, 100.0],
        "ing": "Whey Protein Isolate, lodized Salt, Acesulfame Potassium (INS 950), Sucralose (INS 955), Stabilizers (INS 415, INS 417), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 228: Avvatar ISORICH Malai Kulfi 2kg
    {
        "i": 228, "g": "avvatar-isorich", "name": "ISORICH Whey Protein Isolate", "variant": "Malai Kulfi 2kg",
        "net": 2000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 11200, "mrp": 19149,
        "n": [130.0, 29.0, 1.3, 1.0, 0.7, 0.0, 2.8, 0.0, 0.0, 0.0, 100.0],
        "ing": "Whey Protein Isolate, lodized Salt, Acesulfame Potassium (INS 950), Sucralose (INS 955), Stabilizers (INS 415, INS 417), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 229: Avvatar ISORICH Chocolate Hazelnut 1kg
    {
        "i": 229, "g": "avvatar-isorich", "name": "ISORICH Whey Protein Isolate", "variant": "Chocolate Hazelnut 1kg",
        "net": 1000, "serv": 35, "label": "1 rounded scoop (35g)", "price": 5600, "mrp": 10399,
        "n": [130.0, 29.0, 1.3, 1.0, 0.7, 0.0, 2.8, 0.0, 0.0, 0.0, 100.0],
        "ing": "Whey Protein Isolate, Cocoa Powder, lodized Salt, Acesulfame Potassium (INS 950), Sucralose (INS 955), Stabilizers (INS 415, INS 417), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 230: Avvatar Alpha Whey Belgian Choc 1kg
    {
        "i": 230, "g": "avvatar-alpha-whey", "name": "Alpha Whey Protein", "variant": "Belgian Chocolate 1kg",
        "net": 1000, "serv": 40, "label": "1 rounded scoop (40g)", "price": 2999, "mrp": 4999,
        "n": [147.3, 25.0, 8.0, 1.7, 1.1, 0.05, 4.6, 0.0, 8.0, 0.0, 70.0],
        "ing": "Whey Protein Concentrate, Milk Protein Concentrate, Alkalized Cocoa Powder, Minerals and Vitamins Premix, Stabilizer (INS 413, INS 416), Acesulfame Potassium (INS 950), Sucralose (INS 955), lodized Salt, Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 231: Avvatar Alpha Whey Belgian Choc 2kg
    {
        "i": 231, "g": "avvatar-alpha-whey", "name": "Alpha Whey Protein", "variant": "Belgian Chocolate 2kg",
        "net": 2000, "serv": 40, "label": "1 rounded scoop (40g)", "price": 5777, "mrp": 9749,
        "n": [147.3, 25.0, 8.0, 1.7, 1.1, 0.05, 4.6, 0.0, 8.0, 0.0, 70.0],
        "ing": "Whey Protein Concentrate, Milk Protein Concentrate, Alkalized Cocoa Powder, Minerals and Vitamins Premix, Stabilizer (INS 413, INS 416), Acesulfame Potassium (INS 950), Sucralose (INS 955), lodized Salt, Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 232: Avvatar Alpha Whey Malai Kulfi 1kg
    {
        "i": 232, "g": "avvatar-alpha-whey", "name": "Alpha Whey Protein", "variant": "Malai Kulfi 1kg",
        "net": 1000, "serv": 40, "label": "1 rounded scoop (40g)", "price": 2999, "mrp": 4999,
        "n": [147.3, 25.0, 8.0, 1.7, 1.1, 0.05, 4.6, 0.0, 8.0, 0.0, 70.0],
        "ing": "Whey Protein Concentrate, Milk Protein Concentrate, Minerals and Vitamins Premix, Stabilizer (INS 413, INS 416), Acesulfame Potassium (INS 950), Sucralose (INS 955), lodized Salt, Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 233: Avvatar Alpha Whey Cold Coffee 1kg
    {
        "i": 233, "g": "avvatar-alpha-whey", "name": "Alpha Whey Protein", "variant": "Cold Coffee 1kg",
        "net": 1000, "serv": 40, "label": "1 rounded scoop (40g)", "price": 2999, "mrp": 4999,
        "n": [147.3, 25.0, 8.0, 1.7, 1.1, 0.05, 4.6, 0.0, 8.0, 0.0, 70.0],
        "ing": "Whey Protein Concentrate, Milk Protein Concentrate, Coffee Powder, Minerals and Vitamins Premix, Stabilizer (INS 413, INS 416), Acesulfame Potassium (INS 950), Sucralose (INS 955), lodized Salt, Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 234: Avvatar Wafer Bar Coffee
    {
        "i": 234, "g": "avvatar-wafer-bar", "name": "Protein Wafer Bar", "variant": "Coffee Flavour (Pack of 8)",
        "net": 320, "serv": 40, "label": "1 bar (40g)", "price": 792, "mrp": 792,
        "n": [173.0, 10.0, 14.0, 8.0, 5.0, 0.0, 4.0, 2.0, 0.0, 0.0, 34.0],
        "ing": "Milk Protein Concentrate, Whey Protein Isolate, Cocoa Butter, Wheat Flour, Coffee Extract, Erythritol, Sunflower Lecithin, Raising Agent (INS 500(ii)), Salt",
        "allergens": ["milk", "wheat"], "tags": ["Vegetarian", "No Added Sugar"]
    },
    # 235: Avvatar Wafer Bar Tiramisu
    {
        "i": 235, "g": "avvatar-wafer-bar", "name": "Protein Wafer Bar", "variant": "Tiramisu Flavour (Pack of 8)",
        "net": 336, "serv": 42, "label": "1 bar (42g)", "price": 792, "mrp": 792,
        "n": [173.0, 10.0, 14.0, 8.0, 5.0, 0.0, 4.0, 2.0, 0.0, 0.0, 34.0],
        "ing": "Milk Protein Concentrate, Whey Protein Isolate, Cocoa Butter, Wheat Flour, Cocoa Powder, Erythritol, Sunflower Lecithin, Raising Agent (INS 500(ii)), Salt",
        "allergens": ["milk", "wheat"], "tags": ["Vegetarian", "No Added Sugar"]
    },
    # 236: MuscleBlaze Biozyme Performance Whey
    {
        "i": 236, "name": "Biozyme Performance Whey", "variant": "Rich Chocolate 2kg",
        "net": 2000, "serv": 36, "label": "1 Scoop (36g)", "price": 4499, "mrp": 7399,
        "n": [144.08, 25.0, 6.51, 2.24, 1.13, 0.0, 29.87, 1.48, 0.56, 0.0, 148.87],
        "ing": "Whey Protein Concentrate, Cocoa Powder, Nature Identical Flavouring Substances, MB EnzymePro (Protease Enzymes), Sodium Chloride, Stabilizer (INS 415), Sweetener (INS 955), Sunflower Lecithin (INS 322)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 237: MuscleBlaze Fuel One Whey Protein
    {
        "i": 237, "name": "Fuel One Whey Protein", "variant": "Chocolate 1kg",
        "net": 1000, "serv": 39, "label": "1 Heaping Scoop (39g)", "price": 1899, "mrp": 2199,
        "n": [150.77, 24.0, 8.78, 2.11, 1.35, 0.0, 64.49, 0.0, 5.85, 0.0, 200.85],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Cocoa Powder, Nature Identical Flavouring Substances, Sodium Chloride, Emulsifier (INS 322(i)), Sweetener (INS 955)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 238: MuscleBlaze 100% Clean Raw Whey Protein Concentrate
    {
        "i": 238, "name": "100% Clean Raw Whey Protein Concentrate", "variant": "Unflavoured 1kg",
        "net": 1000, "serv": 30, "label": "1 Scoop (30g)", "price": 1799, "mrp": 2399,
        "n": [118.5, 24.0, 2.25, 1.5, 0.76, 0.0, 45.0, 0.0, 2.1, 0.0, 51.6],
        "ing": "Whey Protein Concentrate (Instantised with Sunflower Lecithin)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 239: MuscleBlaze Hi-Protein Bar 30g Protein
    {
        "i": 239, "name": "Hi-Protein Bar (30g Protein)", "variant": "Choco Almond (Pack of 6)",
        "net": 600, "serv": 100, "label": "1 Bar (100g)", "price": 791, "mrp": 900, "poly": 18.0,
        "n": [368.0, 30.0, 45.0, 9.0, 3.72, 0.0, 15.0, 6.5, 5.0, 0.0, 210.0],
        "ing": "Protein Blend (Whey Protein Concentrate, Soy Protein Isolate, Calcium Caseinate), Humectant (INS 422, INS 965(ii)), Almonds, Cocoa Butter, Cocoa Powder, Dark Chocolate Compound, Dietary Fiber (Fructooligosaccharides), Emulsifier (INS 322(i)), Preservative (INS 202)",
        "allergens": ["milk", "soy", "nuts"], "tags": ["Vegetarian", "No Added Sugar"]
    },
    # 240: Bigmuscles Premium Gold Whey Protein
    {
        "i": 240, "name": "Premium Gold Whey Protein", "variant": "Belgian Chocolate 1kg",
        "net": 1000, "serv": 37, "label": "1 Scoop (37g)", "price": 1999, "mrp": 3499,
        "n": [136.2, 25.0, 5.0, 1.8, 0.9, 0.0, 40.0, 0.0, 3.4, 0.0, 166.0],
        "ing": "Protein Blend [85%] [Whey Protein Isolate, Whey Protein Concentrate, Whey Powder], Cocoa Powder, Natural Flavour (Chocolate), Plant Based Sweetener (Stevia), Himalayan Salt, Bromelain (Digestive Enzyme)",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 241: Bigmuscles Titan Whey
    {
        "i": 241, "name": "Titan Whey", "variant": "Rich Chocolate 1kg",
        "net": 1000, "serv": 39, "label": "1 Scoop (39g)", "price": 1699, "mrp": 2999,
        "n": [141.1, 25.0, 6.0, 1.9, 0.9, 0.0, 40.0, 0.0, 3.4, 0.0, 168.0],
        "ing": "Protein Blend [Whey Protein Isolate, Whey Protein Concentrate], Cocoa Powder, Natural Flavour, Plant Based Stevia, Himalayan Salt, Bromelain [Digestive Enzyme]",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 242: Bigmuscles Plant Protein Isolate
    {
        "i": 242, "name": "Plant Protein Isolate", "variant": "Belgian Chocolate 1kg",
        "net": 1000, "serv": 37, "label": "1 Scoop (37g)", "price": 1799, "mrp": 3199,
        "n": [122.0, 25.0, 2.8, 1.2, 0.3, 0.0, 15.0, 0.0, 0.8, 0.0, 230.0],
        "ing": "Pea Protein Isolate, Brown Rice Protein Isolate, Cocoa Powder, Plant Based Stevia",
        "allergens": [], "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "No Added Sugar"]
    },
    # 243: The Whole Truth 100% Pure Whey Protein Isolate
    {
        "i": 243, "name": "100% Pure Whey Protein Isolate", "variant": "Unflavoured 1kg",
        "net": 1000, "serv": 33, "label": "1 scoop (33g)", "price": 7499, "mrp": 7499,
        "n": [123.9, 30.0, 0.8, 0.3, 0.2, 0.0, 2.0, 0.0, 0.0, 0.0, 45.0],
        "ing": "Instantised Whey Protein Isolate, Bromelain",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 244: The Whole Truth Whey Blend Unflavoured
    {
        "i": 244, "g": "twt-whey-blend", "name": "Whey Protein Blend (Isolate + Concentrate)", "variant": "Unflavoured 1kg",
        "net": 1000, "serv": 32, "label": "1 scoop (32g)", "price": 4999, "mrp": 4999,
        "n": [127.0, 26.0, 2.4, 1.5, 0.9, 0.0, 15.0, 0.0, 0.0, 0.0, 60.0],
        "ing": "Instantised Whey Protein Concentrate, Bromelain",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 245: The Whole Truth Whey Blend Light Cocoa
    {
        "i": 245, "g": "twt-whey-blend", "name": "Whey Protein Blend (Isolate + Concentrate)", "variant": "Light Cocoa 1kg",
        "net": 1000, "serv": 34, "label": "1 scoop (34g)", "price": 5499, "mrp": 5499,
        "n": [134.0, 24.0, 4.6, 1.8, 1.1, 0.0, 12.0, 0.8, 2.1, 0.0, 65.0],
        "ing": "Instantised Whey Protein Isolate, Whey Protein Concentrate, Cocoa, Milk Solids, Dates, Monk Fruit, Bromelain",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 246: The Whole Truth Whey Blend Cold Coffee
    {
        "i": 246, "g": "twt-whey-blend", "name": "Whey Protein Blend (Isolate + Concentrate)", "variant": "Cold Coffee 1kg",
        "net": 1000, "serv": 34, "label": "1 scoop (34g)", "price": 5499, "mrp": 5499,
        "n": [134.0, 24.0, 4.5, 1.8, 1.1, 0.0, 12.0, 0.8, 2.0, 0.0, 65.0],
        "ing": "Instantised Whey Protein Isolate, Whey Protein Concentrate, Coffee Powder, Milk Solids, Dates, Monk Fruit, Bromelain",
        "allergens": ["milk"], "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"]
    },
    # 247: The Whole Truth Plant Protein Double Cocoa
    {
        "i": 247, "g": "twt-plant-protein", "name": "100% Plant Protein Powder", "variant": "Double Cocoa 1kg",
        "net": 1000, "serv": 35, "label": "1 scoop (35g)", "price": 3499, "mrp": 3499,
        "n": [138.0, 25.0, 4.8, 2.1, 0.6, 0.0, 0.0, 1.2, 2.2, 0.0, 185.0],
        "ing": "Pea Protein Isolate, Brown Rice Protein Isolate, Cocoa, Dates, Monk Fruit, Bromelain",
        "allergens": [], "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "No Added Sugar"]
    },
    # 248: The Whole Truth Plant Protein Pista Badaam
    {
        "i": 248, "g": "twt-plant-protein", "name": "100% Plant Protein Powder", "variant": "Pista Badaam 1kg",
        "net": 1000, "serv": 35, "label": "1 scoop (35g)", "price": 3499, "mrp": 3499,
        "n": [142.0, 24.0, 4.5, 2.8, 0.7, 0.0, 0.0, 1.0, 2.0, 0.0, 190.0],
        "ing": "Pea Protein Isolate, Brown Rice Protein Isolate, Pistachios, Almonds, Dates, Monk Fruit, Curcumin, Bromelain",
        "allergens": ["nuts"], "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "No Added Sugar"]
    }
]

print(f"Total new picks: {len(NEW_PICKS)}")
print(f"Total new readings: {len(NEW_READINGS)}")
assert len(NEW_PICKS) == len(NEW_READINGS), "Count mismatch between picks and readings!"

# 3. Append to picks.txt
with open(PICKS_PATH, "a", encoding="utf-8") as f:
    f.write("\n# --- Batch 3A: Sports Nutrition Heavyweights ---\n")
    for store, handle, cat, brand in NEW_PICKS:
        f.write(f"{store}|{handle}|{cat}|{brand}\n")

# 4. Append to readings.jsonl
with open(READINGS_PATH, "a", encoding="utf-8") as f:
    for r in NEW_READINGS:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Successfully appended picks and readings.")
