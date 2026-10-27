import json
from pathlib import Path

data_dir = Path("protein-etl/data/demo_catalog")

batch_5d = [
    {
        "handle": "ensure-original-complete-nutrition-vanilla",
        "category": "adult-nutrition",
        "brand": "Ensure",
        "manual": {
            "handle": "ensure-original-complete-nutrition-vanilla",
            "store": "manual",
            "brand": "Ensure",
            "url": "https://www.abbottnutrition.in/ensure-adult-nutrition",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/e/n/ensure_vanilla_400g_front.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 720.0, "mrp": 720.0, "compare_at_price": 720.0, "net_weight_g": 400, "in_stock": True},
                {"id": 2, "title": "Vanilla 1kg Refill", "price": 1550.0, "mrp": 1550.0, "compare_at_price": 1550.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 414,
            "v": 0,
            "name": "Ensure Original Complete Balanced Adult Nutrition",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 50,
            "label": "50 g (approx. 3 scoops)",
            "n": [210.0, 9.0, 29.0, 6.5, 1.5, 0.0, 5.0, 2.5, 14.0, 8.0, 180.0],
            "ing": "Maltodextrin, Sucrose, Edible Vegetable Oil (High Oleic Sunflower Oil, Soy Oil), Calcium Caseinate, Whey Protein Concentrate, Soy Protein Isolate, Fructooligosaccharides (FOS), Minerals, Vitamins, Taurine, L-Carnitine",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Clinically proven complete balanced nutrition scientifically formulated with 32 vital nutrients, high-quality triple protein blend, calcium, and vitamin D for adult strength and active mobility.",
            "protein_source": "Calcium Caseinate, Whey Protein Concentrate & Soy Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ensure-plus-high-protein-vanilla",
        "category": "adult-nutrition",
        "brand": "Ensure",
        "manual": {
            "handle": "ensure-plus-high-protein-vanilla",
            "store": "manual",
            "brand": "Ensure",
            "url": "https://www.abbottnutrition.in/ensure-plus",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/e/n/ensure_plus_vanilla_400g_front.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 780.0, "mrp": 780.0, "compare_at_price": 780.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 415,
            "v": 0,
            "name": "Ensure Plus High Protein Recovery Drink",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 50,
            "label": "50 g (approx. 3 scoops)",
            "n": [215.0, 12.5, 27.0, 6.2, 1.4, 0.0, 6.0, 2.0, 12.0, 6.0, 190.0],
            "ing": "Maltodextrin, Sodium & Calcium Caseinates, Sucrose, Edible Vegetable Oils (High Oleic Sunflower, Canola), Whey Protein Concentrate, Minerals, FOS, Vitamins",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Therapeutic high-protein adult clinical nutrition powder designed for recovery, muscle preservation, and enhanced nutritional intake during convalescence.",
            "protein_source": "Milk Caseinates & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ensure-diabetes-care-vanilla",
        "category": "adult-nutrition",
        "brand": "Ensure",
        "manual": {
            "handle": "ensure-diabetes-care-vanilla",
            "store": "manual",
            "brand": "Ensure",
            "url": "https://www.abbottnutrition.in/ensure-diabetes-care",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/e/n/ensure_diabetes_care_vanilla_400g.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 790.0, "mrp": 790.0, "compare_at_price": 790.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 416,
            "v": 0,
            "name": "Ensure Diabetes Care Specialized Nutrition",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 50,
            "label": "50 g (approx. 3 scoops)",
            "n": [188.0, 9.2, 23.5, 6.0, 1.2, 0.0, 4.0, 5.0, 0.0, 0.0, 165.0],
            "ing": "Maltodextrin, Calcium Caseinate, Edible Vegetable Oils (High Oleic Sunflower Oil, Soy Oil), Fructose, Fructooligosaccharides (FOS), Resistant Dextrin (Fibersol), Soy Polysaccharide, Minerals, Vitamins, Myo-Inositol",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "No Added Sugar", "High-Fibre"],
            "desc": "Scientifically designed diabetes-specific nutritional supplement with low glycemic index (GI), dual-fibre blend (Fibersol & FOS), and complex carbohydrates to manage steady blood sugar release.",
            "protein_source": "Calcium Caseinate & Soy Protein",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "glucerna-specialized-diabetes-care-vanilla",
        "category": "adult-nutrition",
        "brand": "Glucerna",
        "manual": {
            "handle": "glucerna-specialized-diabetes-care-vanilla",
            "store": "manual",
            "brand": "Glucerna",
            "url": "https://www.abbottnutrition.in/glucerna",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/g/l/glucerna_vanilla_400g_front.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 840.0, "mrp": 840.0, "compare_at_price": 840.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 417,
            "v": 0,
            "name": "Glucerna Specialized Diabetes Nutritional Drink",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 52,
            "label": "52 g (approx. 5 scoops)",
            "n": [220.0, 10.0, 26.5, 8.0, 1.5, 0.0, 5.0, 3.8, 0.0, 0.0, 195.0],
            "ing": "Maltodextrin, Vegetable Oils (Canola, High Oleic Sunflower), Calcium Caseinate, Soy Protein Isolate, Sucromalt, Glycerin, Minerals, FOS, Resistant Starch, Vitamins, Inositol",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "No Added Sugar"],
            "desc": "Clinically proven meal replacement for diabetes management featuring Triple Care slow-release carbohydrate blend, monounsaturated fatty acids, and essential micronutrients.",
            "protein_source": "Calcium Caseinate & Soy Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "pediasure-complete-growth-chocolate",
        "category": "adult-nutrition",
        "brand": "PediaSure",
        "manual": {
            "handle": "pediasure-complete-growth-chocolate",
            "store": "manual",
            "brand": "PediaSure",
            "url": "https://www.abbottnutrition.in/pediasure-kids-nutrition",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/p/e/pediasure_chocolate_400g_front.png",
            "variants": [
                {"id": 1, "title": "Chocolate 400g", "price": 690.0, "mrp": 690.0, "compare_at_price": 690.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 418,
            "v": 0,
            "name": "PediaSure Complete Balanced Growth Nutrition Chocolate",
            "variant": "Chocolate 400g",
            "net": 400,
            "serv": 45,
            "label": "45 g (approx. 5 scoops)",
            "n": [200.0, 7.0, 27.5, 7.0, 1.8, 0.0, 6.0, 1.8, 16.0, 9.0, 135.0],
            "ing": "Skimmed Milk Powder, Sucrose, Edible Vegetable Oil (Soy Oil, High Oleic Sunflower Oil), Maltodextrin, Cocoa Powder, Fructooligosaccharides (FOS), Minerals, Vitamins, Arginine, Vitamin K2, DHA",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Complete and balanced pediatric nutrition scientifically formulated with 37 vital nutrients, Arginine, Vitamin K2, and DHA to support visible growth and immunity in children.",
            "protein_source": "Skimmed Milk & Whey Protein",
            "protein_tier": "tier_1"
        }
    },
    {
        "handle": "pediasure-complete-growth-vanilla",
        "category": "adult-nutrition",
        "brand": "PediaSure",
        "manual": {
            "handle": "pediasure-complete-growth-vanilla",
            "store": "manual",
            "brand": "PediaSure",
            "url": "https://www.abbottnutrition.in/pediasure-kids-nutrition",
            "image_url": "https://www.abbottnutrition.in/media/catalog/product/p/e/pediasure_vanilla_400g_front.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 690.0, "mrp": 690.0, "compare_at_price": 690.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 419,
            "v": 0,
            "name": "PediaSure Complete Balanced Growth Nutrition Vanilla",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 45,
            "label": "45 g (approx. 5 scoops)",
            "n": [200.0, 7.0, 27.5, 7.0, 1.8, 0.0, 6.0, 1.8, 16.0, 9.0, 135.0],
            "ing": "Skimmed Milk Powder, Sucrose, Edible Vegetable Oil (Soy Oil, High Oleic Sunflower Oil), Maltodextrin, Fructooligosaccharides (FOS), Minerals, Vitamins, Arginine, Vitamin K2, DHA",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Delicious vanilla pediatric nutrition drink with essential macro and micronutrients clinically shown to support height and weight gain in picky eaters.",
            "protein_source": "Skimmed Milk & Whey Protein",
            "protein_tier": "tier_1"
        }
    },
    {
        "handle": "protinex-original-hydrolysed-protein",
        "category": "adult-nutrition",
        "brand": "Protinex",
        "manual": {
            "handle": "protinex-original-hydrolysed-protein",
            "store": "manual",
            "brand": "Protinex",
            "url": "https://www.protinex.com/products/protinex-original",
            "image_url": "https://www.protinex.com/images/products/protinex_original_400g.png",
            "variants": [
                {"id": 1, "title": "Original 400g", "price": 640.0, "mrp": 640.0, "compare_at_price": 640.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 420,
            "v": 0,
            "name": "Protinex Original Hydrolysed Protein",
            "variant": "Original 400g",
            "net": 400,
            "serv": 35,
            "label": "35 g (approx. 2-3 heaped tbsp)",
            "n": [125.0, 11.9, 18.0, 0.5, 0.2, 0.0, 2.0, 1.5, 9.0, 5.0, 140.0],
            "ing": "Peanut Protein Hydrolysate (56%), Sucrose, Malt Extract, Minerals, Vitamins",
            "allergens": ["Peanuts", "Barley"],
            "tags": ["Vegetarian"],
            "desc": "India's iconic heritage health supplement with 34% hydrolysed protein for rapid digestion and 25 immuno-nutrients to build physical strength and stamina.",
            "protein_source": "Peanut Protein Hydrolysate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "protinex-tasty-chocolate",
        "category": "adult-nutrition",
        "brand": "Protinex",
        "manual": {
            "handle": "protinex-tasty-chocolate",
            "store": "manual",
            "brand": "Protinex",
            "url": "https://www.protinex.com/products/protinex-tasty-chocolate",
            "image_url": "https://www.protinex.com/images/products/protinex_tasty_chocolate_400g.png",
            "variants": [
                {"id": 1, "title": "Chocolate 400g", "price": 640.0, "mrp": 640.0, "compare_at_price": 640.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 421,
            "v": 0,
            "name": "Protinex Tasty Chocolate Adult Protein",
            "variant": "Chocolate 400g",
            "net": 400,
            "serv": 35,
            "label": "35 g (approx. 2-3 heaped tbsp)",
            "n": [128.0, 10.5, 19.5, 0.8, 0.3, 0.0, 2.0, 1.8, 11.0, 7.0, 130.0],
            "ing": "Soy Protein Isolate (45%), Sucrose, Cocoa Powder (10%), Skimmed Milk Powder, Minerals, Vitamins",
            "allergens": ["Soy", "Milk"],
            "tags": ["Vegetarian"],
            "desc": "Rich chocolate adult nutritional drink delivering 30% protein with zero trans-fats and high iron, calcium, and B-vitamins for daily vitality.",
            "protein_source": "Soy Protein Isolate & Skimmed Milk",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "protinex-diabetes-care-vanilla",
        "category": "adult-nutrition",
        "brand": "Protinex",
        "manual": {
            "handle": "protinex-diabetes-care-vanilla",
            "store": "manual",
            "brand": "Protinex",
            "url": "https://www.protinex.com/products/protinex-diabetes-care",
            "image_url": "https://www.protinex.com/images/products/protinex_diabetes_care_400g.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 710.0, "mrp": 710.0, "compare_at_price": 710.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 422,
            "v": 0,
            "name": "Protinex Diabetes Care Vanilla",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 35,
            "label": "35 g (approx. 2-3 heaped tbsp)",
            "n": [122.0, 10.5, 18.0, 0.8, 0.3, 0.0, 2.0, 4.2, 0.0, 0.0, 120.0],
            "ing": "Soy Protein Isolate, Dietary Fibre (Polydextrose, Inulin), Maltodextrin, Minerals, Vitamins, Nature Identical Vanilla Flavour, Sucralose",
            "allergens": ["Soy"],
            "tags": ["Vegetarian", "Diabetic-Friendly", "No Added Sugar", "High-Fibre"],
            "desc": "Specially formulated nutritional powder for individuals with diabetes with 30% protein, low GI, zero added sucrose, and high dietary fibre.",
            "protein_source": "Soy Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "complan-royale-chocolate-nutrition-drink",
        "category": "adult-nutrition",
        "brand": "Complan",
        "manual": {
            "handle": "complan-royale-chocolate-nutrition-drink",
            "store": "manual",
            "brand": "Complan",
            "url": "https://complan.in/products/complan-royale-chocolate",
            "image_url": "https://complan.in/media/catalog/product/c/o/complan_royale_chocolate_500g.png",
            "variants": [
                {"id": 1, "title": "Chocolate 500g", "price": 360.0, "mrp": 360.0, "compare_at_price": 360.0, "net_weight_g": 500, "in_stock": True}
            ]
        },
        "reading": {
            "i": 423,
            "v": 0,
            "name": "Complan Royale Chocolate Nutrition Drink",
            "variant": "Chocolate 500g",
            "net": 500,
            "serv": 33,
            "label": "33 g (approx. 2 heaped tbsp)",
            "n": [135.0, 6.0, 22.0, 2.5, 1.2, 0.0, 4.0, 1.0, 14.0, 8.0, 95.0],
            "ing": "Milk Solids (54.8%), Sugar, Peanut Oil, Cocoa Solids (4.5%), Minerals, Vitamins, Taurine, Inositol",
            "allergens": ["Milk", "Peanuts"],
            "tags": ["Vegetarian"],
            "desc": "Nutritional milk drink containing 100% first class milk protein and 34 vital nutrients clinically shown to support 2X faster growth in children.",
            "protein_source": "Milk Solids & Whey",
            "protein_tier": "tier_1"
        }
    },
    {
        "handle": "horlicks-protein-plus-chocolate",
        "category": "adult-nutrition",
        "brand": "Horlicks",
        "manual": {
            "handle": "horlicks-protein-plus-chocolate",
            "store": "manual",
            "brand": "Horlicks",
            "url": "https://horlicks.in/products/horlicks-protein-plus",
            "image_url": "https://horlicks.in/media/catalog/product/h/o/horlicks_protein_plus_chocolate_400g.png",
            "variants": [
                {"id": 1, "title": "Chocolate 400g", "price": 580.0, "mrp": 580.0, "compare_at_price": 580.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 424,
            "v": 0,
            "name": "Horlicks Protein Plus Chocolate Drink",
            "variant": "Chocolate 400g",
            "net": 400,
            "serv": 30,
            "label": "30 g (approx. 3 heaped tsp)",
            "n": [112.0, 10.2, 15.0, 1.2, 0.5, 0.0, 3.0, 1.5, 7.0, 3.5, 110.0],
            "ing": "Triple Protein Blend (Whey Protein Concentrate, Soy Protein Isolate, Calcium Caseinate), Sugar, Cocoa Solids, Minerals, Vitamins",
            "allergens": ["Milk", "Soy"],
            "tags": ["Vegetarian"],
            "desc": "Scientifically designed adult nutrition beverage offering 34% protein through a triple protein blend (Whey, Soy, Casein) to fight fatigue and support muscle health.",
            "protein_source": "Whey Protein Concentrate, Soy Protein Isolate & Calcium Caseinate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "horlicks-protein-plus-vanilla",
        "category": "adult-nutrition",
        "brand": "Horlicks",
        "manual": {
            "handle": "horlicks-protein-plus-vanilla",
            "store": "manual",
            "brand": "Horlicks",
            "url": "https://horlicks.in/products/horlicks-protein-plus",
            "image_url": "https://horlicks.in/media/catalog/product/h/o/horlicks_protein_plus_vanilla_400g.png",
            "variants": [
                {"id": 1, "title": "Vanilla 400g", "price": 580.0, "mrp": 580.0, "compare_at_price": 580.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 425,
            "v": 0,
            "name": "Horlicks Protein Plus Vanilla Drink",
            "variant": "Vanilla 400g",
            "net": 400,
            "serv": 30,
            "label": "30 g (approx. 3 heaped tsp)",
            "n": [112.0, 10.2, 15.0, 1.2, 0.5, 0.0, 3.0, 1.5, 7.0, 3.5, 110.0],
            "ing": "Triple Protein Blend (Whey Protein Concentrate, Soy Protein Isolate, Calcium Caseinate), Sugar, Malt Extract, Minerals, Vitamins",
            "allergens": ["Milk", "Soy", "Barley"],
            "tags": ["Vegetarian"],
            "desc": "Specially formulated triple protein health drink for adults aged 30+ to maintain strength, bone density, and muscle mass.",
            "protein_source": "Whey Protein Concentrate, Soy Protein Isolate & Calcium Caseinate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "gritzo-supermilk-young-athletes-boys-13",
        "category": "adult-nutrition",
        "brand": "Gritzo",
        "manual": {
            "handle": "gritzo-supermilk-young-athletes-boys-13",
            "store": "manual",
            "brand": "Gritzo",
            "url": "https://gritzo.com/products/gritzo-supermilk-young-athletes-boys-13-years",
            "image_url": "https://img8.hkrtcdn.com/15200/prd_1519927-Gritzo-SuperMilk-Young-Athletes-13-years-Boys-400-g-Double-Chocolate_o.jpg",
            "variants": [
                {"id": 1, "title": "Double Chocolate 400g", "price": 799.0, "mrp": 999.0, "compare_at_price": 999.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 426,
            "v": 0,
            "name": "Gritzo SuperMilk for Young Athletes (Boys 13+ yrs)",
            "variant": "Double Chocolate 400g",
            "net": 400,
            "serv": 33,
            "label": "33 g (approx. 2 scoops)",
            "n": [125.0, 13.0, 14.5, 1.6, 0.8, 0.0, 10.0, 2.0, 0.0, 0.0, 90.0],
            "ing": "Milk Protein Blend (Whey Protein Concentrate, Skimmed Milk Powder), Oats Flour, Cocoa Powder, Fructooligosaccharides, Minerals, Vitamins, Ashwagandha, DHA, Curcumin",
            "allergens": ["Milk", "Oats"],
            "tags": ["Vegetarian", "Clean Label", "No Added Sugar"],
            "desc": "Clean athletic nutrition for teenage boys offering 13g clean whey protein per scoop, unrefined carbohydrates from oats, 21 vitamins and minerals, and zero artificial sweeteners.",
            "protein_source": "Whey Protein Concentrate & Skimmed Milk",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "gritzo-supermilk-young-athletes-girls-13",
        "category": "adult-nutrition",
        "brand": "Gritzo",
        "manual": {
            "handle": "gritzo-supermilk-young-athletes-girls-13",
            "store": "manual",
            "brand": "Gritzo",
            "url": "https://gritzo.com/products/gritzo-supermilk-young-athletes-girls-13-years",
            "image_url": "https://img2.hkrtcdn.com/15200/prd_1519931-Gritzo-SuperMilk-Young-Athletes-13-years-Girls-400-g-Natural-Chocolate_o.jpg",
            "variants": [
                {"id": 1, "title": "Natural Chocolate 400g", "price": 799.0, "mrp": 999.0, "compare_at_price": 999.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 427,
            "v": 0,
            "name": "Gritzo SuperMilk for Young Athletes (Girls 13+ yrs)",
            "variant": "Natural Chocolate 400g",
            "net": 400,
            "serv": 33,
            "label": "33 g (approx. 2 scoops)",
            "n": [125.0, 13.0, 14.5, 1.6, 0.8, 0.0, 10.0, 2.0, 0.0, 0.0, 90.0],
            "ing": "Milk Protein Blend (Whey Protein Concentrate, Skimmed Milk Powder), Oats Flour, Cocoa Powder, Fructooligosaccharides, Iron, Calcium, Vitamins, Cranberry Extract, Shatavari, DHA",
            "allergens": ["Milk", "Oats"],
            "tags": ["Vegetarian", "Clean Label", "No Added Sugar"],
            "desc": "Specially formulated personalized athletic nutrition for teenage girls packed with 13g whey protein, bioavailable iron, calcium, vitamin D3, and cranberry extract.",
            "protein_source": "Whey Protein Concentrate & Skimmed Milk",
            "protein_tier": "tier_2"
        }
    }
]

# Append manual entries
manual_path = data_dir / "manual_entries.jsonl"
existing_manual = manual_path.read_text(encoding="utf-8")
if not existing_manual.endswith("\n"):
    existing_manual += "\n"
new_manual_lines = [json.dumps(x["manual"], ensure_ascii=False) for x in batch_5d]
manual_path.write_text(existing_manual + "\n".join(new_manual_lines) + "\n", encoding="utf-8")

# Append picks
picks_path = data_dir / "picks.txt"
existing_picks = picks_path.read_text(encoding="utf-8")
if not existing_picks.endswith("\n"):
    existing_picks += "\n"
new_picks_lines = [f"manual|{x['handle']}|{x['category']}|{x['brand']}" for x in batch_5d]
picks_path.write_text(existing_picks + "\n".join(new_picks_lines) + "\n", encoding="utf-8")

# Append readings
readings_path = data_dir / "readings.jsonl"
existing_readings = readings_path.read_text(encoding="utf-8")
if not existing_readings.endswith("\n"):
    existing_readings += "\n"
new_readings_lines = [json.dumps(x["reading"], ensure_ascii=False) for x in batch_5d]
readings_path.write_text(existing_readings + "\n".join(new_readings_lines) + "\n", encoding="utf-8")

print(f"Batch 5D appended successfully: {len(batch_5d)} items.")
