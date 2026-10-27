import json
from pathlib import Path

data_dir = Path("protein-etl/data/demo_catalog")

batch_5g = [
    {
        "handle": "optimum-nutrition-gold-standard-100-whey-double-rich-chocolate",
        "category": "protein-powders",
        "brand": "Optimum Nutrition",
        "manual": {
            "handle": "optimum-nutrition-gold-standard-100-whey-double-rich-chocolate",
            "store": "manual",
            "brand": "Optimum Nutrition",
            "url": "https://www.optimumnutrition.co.in/products/gold-standard-100-whey-protein",
            "image_url": "https://www.optimumnutrition.co.in/cdn/shop/files/ON_GS_100Whey_DRC_2lb_Front.png",
            "variants": [
                {"id": 1, "title": "2 lbs (907g)", "price": 3899.0, "mrp": 4399.0, "compare_at_price": 4399.0, "net_weight_g": 907, "in_stock": True},
                {"id": 2, "title": "5 lbs (2.27kg)", "price": 7899.0, "mrp": 8999.0, "compare_at_price": 8999.0, "net_weight_g": 2270, "in_stock": True}
            ]
        },
        "reading": {
            "i": 456,
            "v": 0,
            "name": "Gold Standard 100% Whey Double Rich Chocolate",
            "variant": "2 lbs (907g)",
            "net": 907,
            "serv": 30.4,
            "label": "1 rounded scoop (30.4g)",
            "n": [120.0, 24.0, 3.0, 1.5, 1.0, 0.0, 35.0, 1.0, 1.0, 0.0, 130.0],
            "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Hydrolyzed Whey Peptides), Cocoa Powder (Processed with Alkali), Natural and Artificial Flavors, Lecithin, Acesulfame Potassium, Aminogen, Lactase",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "The world's gold standard of whey protein. Formulated with primary whey protein isolates, 5.5g naturally occurring BCAAs, and 4g glutamine per serving. Authenticated with Glanbia India security seal.",
            "protein_source": "Whey Protein Isolate, Whey Protein Concentrate & Hydrolyzed Whey Peptides",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate",
        "category": "protein-powders",
        "brand": "Optimum Nutrition",
        "manual": {
            "handle": "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate",
            "store": "manual",
            "brand": "Optimum Nutrition",
            "url": "https://www.optimumnutrition.co.in/products/gold-standard-100-whey-protein",
            "image_url": "https://www.optimumnutrition.co.in/cdn/shop/files/ON_GS_100Whey_EMC_2lb_Front.png",
            "variants": [
                {"id": 1, "title": "2 lbs (907g)", "price": 3899.0, "mrp": 4399.0, "compare_at_price": 4399.0, "net_weight_g": 907, "in_stock": True}
            ]
        },
        "reading": {
            "i": 457,
            "v": 0,
            "name": "Gold Standard 100% Whey Extreme Milk Chocolate",
            "variant": "2 lbs (907g)",
            "net": 907,
            "serv": 32.0,
            "label": "1 rounded scoop (32g)",
            "n": [130.0, 24.0, 4.0, 1.5, 1.0, 0.0, 35.0, 1.0, 2.0, 0.0, 140.0],
            "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Whey Peptides), Cocoa (Processed with Alkali), Natural & Artificial Flavors, Sunflower Lecithin, Salt, Sucralose, Acesulfame Potassium",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Creamier milk-chocolate profile of the iconic Gold Standard Whey with instantized mixability and authentic verification code on neck band.",
            "protein_source": "Whey Protein Isolate, Whey Concentrate & Peptides",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "optimum-nutrition-gold-standard-100-whey-vanilla-ice-cream",
        "category": "protein-powders",
        "brand": "Optimum Nutrition",
        "manual": {
            "handle": "optimum-nutrition-gold-standard-100-whey-vanilla-ice-cream",
            "store": "manual",
            "brand": "Optimum Nutrition",
            "url": "https://www.optimumnutrition.co.in/products/gold-standard-100-whey-protein",
            "image_url": "https://www.optimumnutrition.co.in/cdn/shop/files/ON_GS_100Whey_Vanilla_2lb_Front.png",
            "variants": [
                {"id": 1, "title": "2 lbs (907g)", "price": 3899.0, "mrp": 4399.0, "compare_at_price": 4399.0, "net_weight_g": 907, "in_stock": True}
            ]
        },
        "reading": {
            "i": 458,
            "v": 0,
            "name": "Gold Standard 100% Whey Vanilla Ice Cream",
            "variant": "2 lbs (907g)",
            "net": 907,
            "serv": 31.0,
            "label": "1 rounded scoop (31g)",
            "n": [120.0, 24.0, 3.0, 1.5, 1.0, 0.0, 35.0, 0.0, 2.0, 0.0, 130.0],
            "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Whey Peptides), Natural and Artificial Flavors, Lecithin, Salt, Sucralose, Acesulfame Potassium, Aminogen, Lactase",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Silky smooth vanilla ice cream whey protein ideal for post-workout shakes and protein smoothies. Authenticated Glanbia distribution.",
            "protein_source": "Whey Protein Isolate, Whey Concentrate & Peptides",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "optimum-nutrition-gold-standard-100-plant-protein-chocolate",
        "category": "protein-powders",
        "brand": "Optimum Nutrition",
        "manual": {
            "handle": "optimum-nutrition-gold-standard-100-plant-protein-chocolate",
            "store": "manual",
            "brand": "Optimum Nutrition",
            "url": "https://www.optimumnutrition.co.in/products/gold-standard-100-plant-protein",
            "image_url": "https://www.optimumnutrition.co.in/cdn/shop/files/ON_GS_Plant_Choc_Front.png",
            "variants": [
                {"id": 1, "title": "1.5 lbs (684g)", "price": 3499.0, "mrp": 3999.0, "compare_at_price": 3999.0, "net_weight_g": 684, "in_stock": True}
            ]
        },
        "reading": {
            "i": 459,
            "v": 0,
            "name": "Gold Standard 100% Plant Protein Chocolate",
            "variant": "1.5 lbs (684g)",
            "net": 684,
            "serv": 36.0,
            "label": "1 scoop (36g)",
            "n": [140.0, 24.0, 6.0, 2.5, 0.5, 0.0, 0.0, 2.0, 1.0, 0.0, 210.0],
            "ing": "Plant Protein Blend (Organic Pea Protein, Organic Brown Rice Protein, Organic Sacha Inchi Protein), Organic Cocoa Powder, Natural Flavors, Stevia Leaf Extract, Vitamin B12, Organic Pomegranate Powder",
            "allergens": [],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "Gluten-Free", "No Added Sugar"],
            "desc": "USDA Organic certified vegan protein combining organic pea, brown rice, and sacha inchi. 24g complete plant protein with 4g naturally occurring BCAAs and 100% daily value of vitamin B12.",
            "protein_source": "Organic Pea, Brown Rice & Sacha Inchi Protein",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "dymatize-iso100-hydrolyzed-whey-isolate-gourmet-chocolate",
        "category": "protein-powders",
        "brand": "Dymatize",
        "manual": {
            "handle": "dymatize-iso100-hydrolyzed-whey-isolate-gourmet-chocolate",
            "store": "manual",
            "brand": "Dymatize",
            "url": "https://www.musclehouse.co.in/products/dymatize-iso-100",
            "image_url": "https://dymatize.com/cdn/shop/files/ISO100_GourmetChocolate_5lb_Front.png",
            "variants": [
                {"id": 1, "title": "5 lbs (2.3kg)", "price": 9499.0, "mrp": 10999.0, "compare_at_price": 10999.0, "net_weight_g": 2300, "in_stock": True}
            ]
        },
        "reading": {
            "i": 460,
            "v": 0,
            "name": "ISO100 Hydrolyzed Whey Protein Isolate Gourmet Chocolate",
            "variant": "5 lbs (2.3kg)",
            "net": 2300,
            "serv": 30.0,
            "label": "1 scoop (30g)",
            "n": [110.0, 25.0, 1.0, 0.5, 0.3, 0.0, 10.0, 0.5, 0.5, 0.0, 100.0],
            "ing": "Hydrolyzed Whey Protein Isolate, Whey Protein Isolate, Cocoa Powder (Processed with Alkali), Salt, Soy Lecithin, Natural and Artificial Flavor, Sucralose, Steviol Glycosides",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Clean Label"],
            "desc": "Multi-award winning hydrolyzed 100% whey protein isolate scientifically formulated for ultra-fast digestion and peak muscle recovery. Authenticated via Muscle House India security scratch code.",
            "protein_source": "Hydrolyzed Whey Protein Isolate & Whey Protein Isolate",
            "protein_tier": "tier_4"
        }
    },
    {
        "handle": "dymatize-iso100-hydrolyzed-whey-isolate-birthday-cake",
        "category": "protein-powders",
        "brand": "Dymatize",
        "manual": {
            "handle": "dymatize-iso100-hydrolyzed-whey-isolate-birthday-cake",
            "store": "manual",
            "brand": "Dymatize",
            "url": "https://www.musclehouse.co.in/products/dymatize-iso-100",
            "image_url": "https://dymatize.com/cdn/shop/files/ISO100_BirthdayCake_5lb_Front.png",
            "variants": [
                {"id": 1, "title": "5 lbs (2.3kg)", "price": 9499.0, "mrp": 10999.0, "compare_at_price": 10999.0, "net_weight_g": 2300, "in_stock": True}
            ]
        },
        "reading": {
            "i": 461,
            "v": 0,
            "name": "ISO100 Hydrolyzed Whey Protein Isolate Birthday Cake",
            "variant": "5 lbs (2.3kg)",
            "net": 2300,
            "serv": 30.0,
            "label": "1 scoop (30g)",
            "n": [110.0, 25.0, 1.5, 0.5, 0.2, 0.0, 10.0, 0.0, 0.5, 0.0, 110.0],
            "ing": "Hydrolyzed Whey Protein Isolate, Whey Protein Isolate, Natural and Artificial Flavors, Rainbow Sprinkles (Sugar, Corn Starch, Vegetable Oil), Salt, Sucralose, Steviol Glycosides",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Delightful birthday cake flavour featuring hydrolyzed whey isolate with real rainbow sprinkles. <1g sugar, <1g fat, zero bloating.",
            "protein_source": "Hydrolyzed Whey Protein Isolate",
            "protein_tier": "tier_4"
        }
    },
    {
        "handle": "dymatize-elite-100-whey-protein-rich-chocolate",
        "category": "protein-powders",
        "brand": "Dymatize",
        "manual": {
            "handle": "dymatize-elite-100-whey-protein-rich-chocolate",
            "store": "manual",
            "brand": "Dymatize",
            "url": "https://www.musclehouse.co.in/products/dymatize-elite-100-whey",
            "image_url": "https://dymatize.com/cdn/shop/files/EliteWhey_RichChocolate_5lb_Front.png",
            "variants": [
                {"id": 1, "title": "5 lbs (2.3kg)", "price": 7499.0, "mrp": 8499.0, "compare_at_price": 8499.0, "net_weight_g": 2300, "in_stock": True}
            ]
        },
        "reading": {
            "i": 462,
            "v": 0,
            "name": "Elite 100% Whey Protein Rich Chocolate",
            "variant": "5 lbs (2.3kg)",
            "net": 2300,
            "serv": 36.0,
            "label": "1 scoop (36g)",
            "n": [140.0, 25.0, 3.0, 2.5, 1.5, 0.0, 75.0, 1.0, 2.0, 0.0, 135.0],
            "ing": "Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Hydrolyzed Whey Protein Concentrate), Cocoa Powder, Polydextrose, Soy Lecithin, Potassium Chloride, Salt, Sucralose",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "100% pure whey protein blend delivering 25g fast-digesting protein and 5.5g BCAAs per scoop. Certified Informed-Choice tested for banned substances.",
            "protein_source": "Whey Protein Concentrate, Whey Isolate & Hydrolyzed Whey",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "muscletech-nitrotech-ripped-french-vanilla",
        "category": "protein-powders",
        "brand": "MuscleTech",
        "manual": {
            "handle": "muscletech-nitrotech-ripped-french-vanilla",
            "store": "manual",
            "brand": "MuscleTech",
            "url": "https://muscletech.in/products/nitro-tech-ripped",
            "image_url": "https://muscletech.in/cdn/shop/files/NitroTechRipped_Vanilla_4lb_Front.png",
            "variants": [
                {"id": 1, "title": "4 lbs (1.8kg)", "price": 5999.0, "mrp": 7499.0, "compare_at_price": 7499.0, "net_weight_g": 1800, "in_stock": True}
            ]
        },
        "reading": {
            "i": 463,
            "v": 0,
            "name": "NitroTech Ripped Hybrid Whey Protein French Vanilla",
            "variant": "4 lbs (1.8kg)",
            "net": 1800,
            "serv": 43.0,
            "label": "1 scoop (43g)",
            "n": [170.0, 30.0, 4.0, 3.0, 1.5, 0.0, 85.0, 1.0, 2.0, 0.0, 140.0],
            "ing": "Isolate Protein & Peptide Blend (Whey Peptides, Whey Protein Isolate, Whey Protein Isolate 97%), Natural & Artificial Flavors, Ripped Matrix (L-Carnitine L-Tartrate 500mg, CLA 250mg, Green Tea Extract 100mg, Rose Hip Extract), Sucralose",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Cutting-edge 7-in-1 hybrid formula delivering 30g pure whey peptides & isolate combined with a scientifically researched weight loss blend (L-Carnitine, CLA, Green Coffee).",
            "protein_source": "Whey Peptides & Whey Protein Isolate 97%",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "muscletech-nitrotech-100-whey-gold-double-rich-chocolate",
        "category": "protein-powders",
        "brand": "MuscleTech",
        "manual": {
            "handle": "muscletech-nitrotech-100-whey-gold-double-rich-chocolate",
            "store": "manual",
            "brand": "MuscleTech",
            "url": "https://muscletech.in/products/nitro-tech-100-whey-gold",
            "image_url": "https://muscletech.in/cdn/shop/files/NitroTech100WheyGold_Chocolate_5lb_Front.png",
            "variants": [
                {"id": 1, "title": "5 lbs (2.27kg)", "price": 6899.0, "mrp": 7999.0, "compare_at_price": 7999.0, "net_weight_g": 2270, "in_stock": True}
            ]
        },
        "reading": {
            "i": 464,
            "v": 0,
            "name": "NitroTech 100% Whey Gold Double Rich Chocolate",
            "variant": "5 lbs (2.27kg)",
            "net": 2270,
            "serv": 33.0,
            "label": "1 scoop (33g)",
            "n": [130.0, 24.0, 3.0, 2.0, 1.2, 0.0, 65.0, 0.5, 2.0, 0.0, 120.0],
            "ing": "Whey Protein Blend (Whey Peptides, Whey Protein Isolate, Whey Protein Concentrate), Cocoa (Processed with Alkali), Soy or Sunflower Lecithin, Salt, Natural & Artificial Flavors, Gum Blend, Sucralose",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Micro-filtered whey isolate and peptides engineered for rapid absorption, clean macronutrients, and superior mixability. Authenticated via Shri Balaji Overseas verification.",
            "protein_source": "Whey Peptides, Whey Protein Isolate & Whey Concentrate",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "muscletech-mass-tech-extreme-2000",
        "category": "mass-gainers",
        "brand": "MuscleTech",
        "manual": {
            "handle": "muscletech-mass-tech-extreme-2000",
            "store": "manual",
            "brand": "MuscleTech",
            "url": "https://muscletech.in/products/mass-tech-extreme-2000",
            "image_url": "https://muscletech.in/cdn/shop/files/MassTechExtreme2000_6lb_Front.png",
            "variants": [
                {"id": 1, "title": "6 lbs (2.72kg)", "price": 3699.0, "mrp": 4999.0, "compare_at_price": 4999.0, "net_weight_g": 2720, "in_stock": True}
            ]
        },
        "reading": {
            "i": 465,
            "v": 0,
            "name": "Mass Tech Extreme 2000 High Calorie Mass Gainer",
            "variant": "6 lbs (2.72kg)",
            "net": 2720,
            "serv": 285.0,
            "label": "3 heaping scoops (285g)",
            "n": [1070.0, 60.0, 200.0, 3.5, 2.0, 0.0, 165.0, 3.0, 12.0, 0.0, 480.0],
            "ing": "Multi-Phase Carb Complex (Maltodextrin, Oat Bran, Isomaltulose), Multi-Phase Protein System (Whey Protein Concentrate, Whey Protein Isolate 97%, Whey Protein Isolate, Hydrolyzed Whey Protein Isolate), Cocoa, Creatine Monohydrate (5g), Medium Chain Triglycerides, Natural Flavors, Vitamins & Minerals",
            "allergens": ["Milk", "Soy", "Oats"],
            "tags": ["Vegetarian", "No Added Sugar"],
            "desc": "Hardcore mass gainer designed for serious athletes and hardgainers. 60g multi-phase protein, 5g HPLC-tested creatine, and over 1,000 clean calories to drive extreme mass and strength.",
            "protein_source": "Whey Protein Concentrate & Isolate Multi-Phase System",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "myprotein-impact-whey-isolate-chocolate-smooth",
        "category": "protein-powders",
        "brand": "Myprotein",
        "manual": {
            "handle": "myprotein-impact-whey-isolate-chocolate-smooth",
            "store": "manual",
            "brand": "Myprotein",
            "url": "https://www.myprotein.co.in/sports-nutrition/impact-whey-isolate/10530911.html",
            "image_url": "https://static.thcdn.com/images/large/original//productimg/1600/1600/10530911-1374889507441865.jpg",
            "variants": [
                {"id": 1, "title": "1kg", "price": 3499.0, "mrp": 4299.0, "compare_at_price": 4299.0, "net_weight_g": 1000, "in_stock": True},
                {"id": 2, "title": "2.5kg", "price": 7499.0, "mrp": 8999.0, "compare_at_price": 8999.0, "net_weight_g": 2500, "in_stock": True}
            ]
        },
        "reading": {
            "i": 466,
            "v": 0,
            "name": "Impact Whey Isolate Chocolate Smooth",
            "variant": "1kg",
            "net": 1000,
            "serv": 25.0,
            "label": "1 scoop (25g)",
            "n": [96.0, 23.0, 0.6, 0.1, 0.1, 0.0, 2.0, 0.3, 0.6, 0.0, 50.0],
            "ing": "Whey Protein Isolate (Milk) (91%), Emulsifier (Soy/Sunflower Lecithin), Cocoa Powder, Flavouring, Sweetener (Sucralose)",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Clean Label"],
            "desc": "Labdoor Grade A certified 90%+ pure whey isolate. Exceptionally low in fat and carbohydrates with 23g ultra-pure protein per scoop.",
            "protein_source": "Cross-Flow Microfiltered Whey Protein Isolate",
            "protein_tier": "tier_4"
        }
    },
    {
        "handle": "myprotein-clear-whey-isolate-orange-mango",
        "category": "protein-powders",
        "brand": "Myprotein",
        "manual": {
            "handle": "myprotein-clear-whey-isolate-orange-mango",
            "store": "manual",
            "brand": "Myprotein",
            "url": "https://www.myprotein.co.in/sports-nutrition/clear-whey-isolate/12081395.html",
            "image_url": "https://static.thcdn.com/images/large/original//productimg/1600/1600/12081396-1994821817441890.jpg",
            "variants": [
                {"id": 1, "title": "500g", "price": 2999.0, "mrp": 3699.0, "compare_at_price": 3699.0, "net_weight_g": 500, "in_stock": True}
            ]
        },
        "reading": {
            "i": 467,
            "v": 0,
            "name": "Clear Whey Isolate Orange Mango",
            "variant": "500g",
            "net": 500,
            "serv": 25.0,
            "label": "1 scoop (25g)",
            "n": [87.0, 20.0, 0.7, 0.1, 0.0, 0.0, 2.0, 0.0, 0.5, 0.0, 40.0],
            "ing": "Hydrolysed Whey Protein Isolate (Milk) (90%), Natural Flavouring, Acidity Regulators (Citric Acid, Phosphoric Acid), Colour (Curcumin, Beetroot Red), Sweetener (Sucralose)",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Clean Label"],
            "desc": "Revolutionary juice-like protein shake. Made from hydrolyzed high-quality whey isolate that dissolves into a light, translucent, fruity refreshing drink with zero milky texture.",
            "protein_source": "Hydrolysed Whey Protein Isolate",
            "protein_tier": "tier_4"
        }
    },
    {
        "handle": "ultimate-nutrition-prostar-100-whey-chocolate-creme",
        "category": "protein-powders",
        "brand": "Ultimate Nutrition",
        "manual": {
            "handle": "ultimate-nutrition-prostar-100-whey-chocolate-creme",
            "store": "manual",
            "brand": "Ultimate Nutrition",
            "url": "https://paradigmsmt.com/products/prostar-100-whey-protein",
            "image_url": "https://ultimatenutrition.com/cdn/shop/products/Prostar_ChocolateCreme_5.28lb.png",
            "variants": [
                {"id": 1, "title": "5.28 lbs (2.39kg)", "price": 6299.0, "mrp": 7999.0, "compare_at_price": 7999.0, "net_weight_g": 2390, "in_stock": True}
            ]
        },
        "reading": {
            "i": 468,
            "v": 0,
            "name": "Prostar 100% Whey Protein Chocolate Creme",
            "variant": "5.28 lbs (2.39kg)",
            "net": 2390,
            "serv": 30.0,
            "label": "1 rounded scoop (30g)",
            "n": [120.0, 25.0, 2.0, 1.0, 0.5, 0.0, 20.0, 0.5, 1.0, 0.0, 70.0],
            "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Whey Peptides), Cocoa, Natural and Artificial Flavors, Sucralose, Acesulfame Potassium, Soy Lecithin",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Longstanding gym classic engineered with micro- and ultra-filtered whey isolates and concentrates. Delivers 25g protein per 30g serving with 6g naturally occurring BCAAs. Verified via Paradigm Sourcing India.",
            "protein_source": "Whey Protein Isolate, Whey Concentrate & Whey Peptides",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "ultimate-nutrition-iso-sensation-93-chocolate",
        "category": "protein-powders",
        "brand": "Ultimate Nutrition",
        "manual": {
            "handle": "ultimate-nutrition-iso-sensation-93-chocolate",
            "store": "manual",
            "brand": "Ultimate Nutrition",
            "url": "https://paradigmsmt.com/products/iso-sensation-93",
            "image_url": "https://ultimatenutrition.com/cdn/shop/products/ISOSensation93_Chocolate_5lb.png",
            "variants": [
                {"id": 1, "title": "5 lbs (2.27kg)", "price": 8499.0, "mrp": 9999.0, "compare_at_price": 9999.0, "net_weight_g": 2270, "in_stock": True}
            ]
        },
        "reading": {
            "i": 469,
            "v": 0,
            "name": "ISO Sensation 93 100% Pure Whey Isolate Natural Chocolate",
            "variant": "5 lbs (2.27kg)",
            "net": 2270,
            "serv": 32.0,
            "label": "1 scoop (32g)",
            "n": [130.0, 30.0, 1.0, 0.2, 0.1, 0.0, 2.0, 0.5, 0.5, 0.0, 50.0],
            "ing": "IsoChill (Double Cold-Temperature Processed Cross-Flow Full-Spectrum Premium Micro-Filtrated Whey Protein Isolate), Cocoa, Colostrum Complex, Glutamine Complex, SI Complex (Alpha Lipoic Acid, d-Pinitol, 4-Hydroxyisoleucine), D-Digest Complex, Sucralose",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Clean Label"],
            "desc": "Industry-leading 93% pure whey isolate processed with proprietary IsoChill low-temperature cross-flow technology. Fortified with colostrum and digestive enzymes for peak bio-absorption.",
            "protein_source": "IsoChill Cold-Processed Micro-Filtrated Whey Protein Isolate",
            "protein_tier": "tier_4"
        }
    }
]

# Append manual entries
manual_path = data_dir / "manual_entries.jsonl"
existing_manual = manual_path.read_text(encoding="utf-8")
if not existing_manual.endswith("\n"):
    existing_manual += "\n"
new_manual_lines = [json.dumps(x["manual"], ensure_ascii=False) for x in batch_5g]
manual_path.write_text(existing_manual + "\n".join(new_manual_lines) + "\n", encoding="utf-8")

# Append picks
picks_path = data_dir / "picks.txt"
existing_picks = picks_path.read_text(encoding="utf-8")
if not existing_picks.endswith("\n"):
    existing_picks += "\n"
new_picks_lines = [f"manual|{x['handle']}|{x['category']}|{x['brand']}" for x in batch_5g]
picks_path.write_text(existing_picks + "\n".join(new_picks_lines) + "\n", encoding="utf-8")

# Append readings
readings_path = data_dir / "readings.jsonl"
existing_readings = readings_path.read_text(encoding="utf-8")
if not existing_readings.endswith("\n"):
    existing_readings += "\n"
new_readings_lines = [json.dumps(x["reading"], ensure_ascii=False) for x in batch_5g]
readings_path.write_text(existing_readings + "\n".join(new_readings_lines) + "\n", encoding="utf-8")

print(f"Batch 5G appended successfully: {len(batch_5g)} items.")
