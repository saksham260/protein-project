"""Wave 4 Dataset: Clinical & Adult Nutrition Depth (+20 Products)

Category: adult-nutrition
"""

import json

WAVE_4_PRODUCTS = [
    # 1. Nestle Health Science Resource High Protein Vanilla
    {
        "pick": ["manual", "nestle-health-science-resource-high-protein-vanilla", "adult-nutrition", "Nestle Health Science"],
        "name": "Resource High Protein Vanilla",
        "desc": "High quality clinical whey protein formula with 45% protein to support muscle preservation and recovery in adults.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [177.0, 22.5, 20.0, 0.8, 0.4, 0.0, 15.0, 2.0, 9.0, 0.0, 180.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Inulin, Natural & Nature Identical Vanilla Flavour, Vitamins & Minerals Blend, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Skimmed Milk Powder",
        "protein_tier": "tier_2",
        "url": "https://www.nestlehealthscience.in/brands/resource/resource-high-protein",
        "image_url": None,
        "price": 1049.0, "mrp": 1199.0,
        "variant_title": "400g Tin"
    },
    # 2. Nestle Health Science Resource High Protein Chocolate
    {
        "pick": ["manual", "nestle-health-science-resource-high-protein-chocolate", "adult-nutrition", "Nestle Health Science"],
        "name": "Resource High Protein Chocolate",
        "desc": "Rich chocolate flavoured adult clinical nutrition providing 22.5g dual milk protein per serving.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [179.0, 22.5, 19.5, 1.2, 0.6, 0.0, 15.0, 2.5, 8.5, 0.0, 190.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Cocoa Powder, Inulin, Vitamins & Minerals Blend, Nature Identical Chocolate Flavour, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Skimmed Milk Powder",
        "protein_tier": "tier_2",
        "url": "https://www.nestlehealthscience.in/brands/resource/resource-high-protein",
        "image_url": None,
        "price": 1049.0, "mrp": 1199.0,
        "variant_title": "400g Tin"
    },
    # 3. Nestle Health Science Peptamen Complete Peptide-Based Nutrition
    {
        "pick": ["manual", "nestle-health-science-peptamen-peptide-nutrition", "adult-nutrition", "Nestle Health Science"],
        "name": "Peptamen Complete Peptide-Based Nutrition",
        "desc": "Specialized peptide-based formula with 100% enzymatically hydrolyzed whey protein and 70% MCT oil for impaired GI function.",
        "serv": 50.0, "net": 400.0, "label": "50g (7 scoops)",
        "n": [201.0, 8.0, 27.5, 6.5, 4.5, 0.0, 10.0, 0.0, 5.5, 0.0, 200.0],
        "ing": "Maltodextrin, Enzymatically Hydrolyzed Whey Protein, Medium Chain Triglycerides (MCT Oil), Corn Starch, Soybean Oil, Vitamins & Minerals, Soy Lecithin",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Clinical Nutrition", "Peptide-Based"],
        "is_vegan": False,
        "protein_source": "Whey Protein Hydrolysate",
        "protein_tier": "tier_1",
        "url": "https://www.nestlehealthscience.in/brands/peptamen",
        "image_url": None,
        "price": 1899.0, "mrp": 2199.0,
        "variant_title": "400g Tin"
    },
    # 4. Nestle Health Science Resource Diabetic Vanilla
    {
        "pick": ["manual", "nestle-health-science-resource-diabetic-vanilla", "adult-nutrition", "Nestle Health Science"],
        "name": "Resource Diabetic Clinical Nutrition Vanilla",
        "desc": "Low glycemic index complete clinical formula with whey protein and prebiotic fibers designed for diabetic management.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [204.0, 11.0, 23.0, 7.5, 1.5, 0.0, 5.0, 4.5, 1.5, 0.0, 170.0],
        "ing": "Tapioca Dextrin, Whey Protein Concentrate, High Oleic Sunflower Oil, Low Erucic Rapeseed Oil, Inulin, FOS, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://www.nestlehealthscience.in/brands/resource/resource-diabetic",
        "image_url": None,
        "price": 949.0, "mrp": 1099.0,
        "variant_title": "400g Tin"
    },
    # 5. Ensure Plus High Protein Vanilla
    {
        "pick": ["manual", "ensure-plus-high-protein-vanilla", "adult-nutrition", "Ensure"],
        "name": "Ensure Plus High Protein Vanilla",
        "desc": "Scientifically formulated adult nutrition with 30% dual-source protein, HMB and 28 essential vitamins and minerals.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [198.0, 15.0, 25.5, 4.0, 1.2, 0.0, 10.0, 2.5, 8.0, 0.0, 190.0],
        "ing": "Maltodextrin, Milk Protein Concentrate, Soy Protein Isolate, High Oleic Sunflower Oil, FOS, Calcium HMB, Vitamins & Minerals, Vanilla Flavor",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Adult Nutrition"],
        "is_vegan": False,
        "protein_source": "Milk Protein Concentrate & Soy Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://ensureindia.in/ensure-plus",
        "image_url": None,
        "price": 799.0, "mrp": 899.0,
        "variant_title": "400g Tin"
    },
    # 6. Ensure Diabetes Care Vanilla
    {
        "pick": ["manual", "ensure-diabetes-care-vanilla", "adult-nutrition", "Ensure"],
        "name": "Ensure Diabetes Care Vanilla",
        "desc": "Diabetes-specific balanced nutritional drink with slow-release energy system and high-quality milk protein.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [203.0, 11.5, 24.5, 6.5, 1.0, 0.0, 5.0, 4.0, 1.5, 0.0, 160.0],
        "ing": "Maltodextrin, Calcium Caseinate, High Oleic Sunflower Oil, FOS, Soy Protein Isolate, Inositol, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Adult Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Calcium Caseinate & Soy Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://ensureindia.in/diabetes-care",
        "image_url": None,
        "price": 820.0, "mrp": 925.0,
        "variant_title": "400g Tin"
    },
    # 7. Ensure Diabetes Care Chocolate
    {
        "pick": ["manual", "ensure-diabetes-care-chocolate", "adult-nutrition", "Ensure"],
        "name": "Ensure Diabetes Care Chocolate",
        "desc": "Heart-healthy and low-GI chocolate nutritional supplement designed to manage blood glucose and energy levels.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [203.0, 11.5, 24.0, 6.8, 1.2, 0.0, 5.0, 4.5, 1.5, 0.0, 170.0],
        "ing": "Maltodextrin, Calcium Caseinate, High Oleic Sunflower Oil, Cocoa Powder, FOS, Soy Protein Isolate, Inositol, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Adult Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Calcium Caseinate & Soy Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://ensureindia.in/diabetes-care",
        "image_url": None,
        "price": 820.0, "mrp": 925.0,
        "variant_title": "400g Tin"
    },
    # 8. Celevida Diabetic Nutrition Kesar Elaichi
    {
        "pick": ["manual", "celevida-diabetic-nutrition-kesar-elaichi", "adult-nutrition", "Celevida"],
        "name": "Diabetic Nutrition Drink Kesar Elaichi",
        "desc": "Scientifically designed high protein, high fiber, low carb nutritional supplement with traditional saffron cardamom flavour.",
        "serv": 25.0, "net": 400.0, "label": "25g (1 sachet / 2 scoops)",
        "n": [92.0, 7.0, 11.5, 2.0, 0.5, 0.0, 0.0, 3.0, 0.8, 0.0, 80.0],
        "ing": "Defatted Soya Flour, Gram Flour, FOS, Soy Protein Isolate, Vitamins & Minerals, Saffron & Cardamom Extract, Sucralose",
        "allergens": ["Soy"],
        "tags": ["Vegetarian", "High-Fibre", "Diabetic-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Soy Protein Isolate & Defatted Soya Flour",
        "protein_tier": "tier_3",
        "url": "https://www.celevida.com/products/kesar-elaichi",
        "image_url": None,
        "price": 720.0, "mrp": 820.0,
        "variant_title": "400g Tin"
    },
    # 9. Celevida Diabetic Nutrition Green Mango
    {
        "pick": ["manual", "celevida-diabetic-nutrition-green-mango", "adult-nutrition", "Celevida"],
        "name": "Diabetic Nutrition Drink Green Mango",
        "desc": "Tangy raw mango flavoured clinical nutrition drink delivering 28% plant protein and dietary fibre.",
        "serv": 25.0, "net": 400.0, "label": "25g (1 sachet / 2 scoops)",
        "n": [92.0, 7.0, 11.5, 2.0, 0.5, 0.0, 0.0, 3.0, 0.8, 0.0, 85.0],
        "ing": "Defatted Soya Flour, Gram Flour, FOS, Soy Protein Isolate, Raw Mango Extract, Vitamins & Minerals, Sucralose",
        "allergens": ["Soy"],
        "tags": ["Vegetarian", "High-Fibre", "Diabetic-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Soy Protein Isolate & Defatted Soya Flour",
        "protein_tier": "tier_3",
        "url": "https://www.celevida.com/products/green-mango",
        "image_url": None,
        "price": 720.0, "mrp": 820.0,
        "variant_title": "400g Tin"
    },
    # 10. Celevida Diabetic Nutrition Chocolate
    {
        "pick": ["manual", "celevida-diabetic-nutrition-chocolate", "adult-nutrition", "Celevida"],
        "name": "Diabetic Nutrition Drink Chocolate",
        "desc": "Low glycemic clinical chocolate formula proven to help manage blood sugar spikes and maintain satiety.",
        "serv": 25.0, "net": 400.0, "label": "25g (1 sachet / 2 scoops)",
        "n": [93.0, 7.0, 11.2, 2.2, 0.6, 0.0, 0.0, 3.0, 0.8, 0.0, 85.0],
        "ing": "Defatted Soya Flour, Cocoa Powder, Gram Flour, FOS, Soy Protein Isolate, Vitamins & Minerals, Sucralose",
        "allergens": ["Soy"],
        "tags": ["Vegetarian", "High-Fibre", "Diabetic-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Soy Protein Isolate & Defatted Soya Flour",
        "protein_tier": "tier_3",
        "url": "https://www.celevida.com/products/chocolate",
        "image_url": None,
        "price": 720.0, "mrp": 820.0,
        "variant_title": "400g Tin"
    },
    # 11. Prohance HP High Protein Vanilla
    {
        "pick": ["manual", "prohance-hp-high-protein-vanilla", "adult-nutrition", "Prohance"],
        "name": "Prohance HP High Protein Vanilla",
        "desc": "High protein nutritional powder with 45% whey protein concentrate, prebiotic fiber and antioxidant micronutrients.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [181.0, 22.5, 21.0, 0.8, 0.4, 0.0, 15.0, 2.0, 4.5, 0.0, 180.0],
        "ing": "Whey Protein Concentrate, Maltodextrin, Inulin, FOS, Vitamins & Minerals, Vanilla Flavor, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://prohance.in/products/prohance-hp",
        "image_url": None,
        "price": 999.0, "mrp": 1150.0,
        "variant_title": "400g Tin"
    },
    # 12. Prohance-D Diabetic Care Chocolate
    {
        "pick": ["manual", "prohance-d-diabetic-care-chocolate", "adult-nutrition", "Prohance"],
        "name": "Prohance-D Diabetic Care Chocolate",
        "desc": "Specially formulated sugar-free diabetic nutrition beverage loaded with whey isolate and slow carbs.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [203.0, 10.5, 25.0, 6.8, 1.2, 0.0, 5.0, 4.5, 1.5, 0.0, 170.0],
        "ing": "Maltodextrin, Whey Protein Isolate, Calcium Caseinate, High Oleic Sunflower Oil, Cocoa, FOS, Inositol, Chromium Picolinate, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://prohance.in/products/prohance-d",
        "image_url": None,
        "price": 799.0, "mrp": 920.0,
        "variant_title": "400g Tin"
    },
    # 13. Prohance-D Diabetic Care Vanilla
    {
        "pick": ["manual", "prohance-d-diabetic-care-vanilla", "adult-nutrition", "Prohance"],
        "name": "Prohance-D Diabetic Care Vanilla",
        "desc": "Vanilla diabetic clinical formula providing heart healthy fats, inositol and sustained energy release.",
        "serv": 50.0, "net": 400.0, "label": "50g (6 scoops)",
        "n": [203.0, 10.5, 25.5, 6.5, 1.0, 0.0, 5.0, 4.5, 1.5, 0.0, 160.0],
        "ing": "Maltodextrin, Whey Protein Isolate, Calcium Caseinate, High Oleic Sunflower Oil, FOS, Inositol, Chromium Picolinate, Vanilla Flavour, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://prohance.in/products/prohance-d",
        "image_url": None,
        "price": 799.0, "mrp": 920.0,
        "variant_title": "400g Tin"
    },
    # 14. Threptin High Protein Diskettes Vanilla
    {
        "pick": ["manual", "threptin-high-protein-diskettes-vanilla", "adult-nutrition", "Threptin"],
        "name": "High Protein Diskettes Vanilla",
        "desc": "Classic doctor-prescribed solid protein biscuit snack providing 30% high-biological-value casein protein.",
        "serv": 25.0, "net": 275.0, "label": "25g (approx. 5 diskettes)",
        "n": [112.0, 7.5, 12.5, 3.5, 1.5, 0.0, 5.0, 0.5, 6.0, 4.0, 90.0],
        "ing": "Casein, Wheat Flour, Sugar, Hydrogenated Vegetable Oil, Butter, Vitamins & Minerals, Natural Vanilla Flavour",
        "allergens": ["Milk", "Wheat"],
        "tags": ["Vegetarian", "High Protein", "Clinical Nutrition"],
        "is_vegan": False,
        "protein_source": "Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://raptakos.com/threptin-diskettes",
        "image_url": None,
        "price": 410.0, "mrp": 460.0,
        "variant_title": "275g Tin"
    },
    # 15. Threptin High Protein Diskettes Chocolate
    {
        "pick": ["manual", "threptin-high-protein-diskettes-chocolate", "adult-nutrition", "Threptin"],
        "name": "High Protein Diskettes Chocolate",
        "desc": "Chocolate flavoured protein diskettes delivering 7.5g casein protein per serving for post-illness strength building.",
        "serv": 25.0, "net": 275.0, "label": "25g (approx. 5 diskettes)",
        "n": [112.0, 7.5, 12.0, 3.8, 1.8, 0.0, 5.0, 0.8, 6.0, 4.0, 95.0],
        "ing": "Casein, Wheat Flour, Cocoa Powder, Sugar, Hydrogenated Vegetable Oil, Butter, Vitamins & Minerals, Flavour",
        "allergens": ["Milk", "Wheat"],
        "tags": ["Vegetarian", "High Protein", "Clinical Nutrition"],
        "is_vegan": False,
        "protein_source": "Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://raptakos.com/threptin-diskettes",
        "image_url": None,
        "price": 410.0, "mrp": 460.0,
        "variant_title": "275g Tin"
    },
    # 16. Threptin Threptin Lite Diskettes (Sugar-Free)
    {
        "pick": ["manual", "threptin-lite-diskettes-sugar-free", "adult-nutrition", "Threptin"],
        "name": "Threptin Lite Diskettes (Sugar-Free)",
        "desc": "Sugar-free version of Threptin diskettes sweetened with sucralose, providing 30% casein protein for diabetics.",
        "serv": 25.0, "net": 275.0, "label": "25g (approx. 5 diskettes)",
        "n": [111.0, 7.5, 13.0, 3.2, 1.2, 0.0, 5.0, 1.5, 0.5, 0.0, 85.0],
        "ing": "Casein, Wheat Flour, Polydextrose, Edible Vegetable Oil, Butter, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Wheat"],
        "tags": ["Vegetarian", "High Protein", "Diabetic-Friendly", "No Added Sugar", "Clinical Nutrition"],
        "is_vegan": False,
        "protein_source": "Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://raptakos.com/threptin-lite",
        "image_url": None,
        "price": 460.0, "mrp": 520.0,
        "variant_title": "275g Tin"
    },
    # 17. Pentasure HP 100% Whey Protein Banana Vanilla
    {
        "pick": ["manual", "pentasure-hp-100-whey-protein-banana-vanilla", "adult-nutrition", "Pentasure"],
        "name": "Pentasure HP 100% Whey Protein Banana Vanilla",
        "desc": "High biological value 100% whey protein clinical supplement with 43% protein to counter catabolism and sarcopenia.",
        "serv": 50.0, "net": 400.0, "label": "50g (4 scoops)",
        "n": [188.0, 21.5, 22.0, 1.5, 0.8, 0.0, 15.0, 2.0, 4.0, 0.0, 180.0],
        "ing": "Whey Protein Concentrate, Maltodextrin, Inulin, Vitamins & Minerals Blend, Banana & Vanilla Flavour, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://pentasure.com/products/pentasure-hp",
        "image_url": None,
        "price": 1099.0, "mrp": 1250.0,
        "variant_title": "400g Tin"
    },
    # 18. Pentasure DM Diabetes Care Vanilla
    {
        "pick": ["manual", "pentasure-dm-diabetes-care-vanilla", "adult-nutrition", "Pentasure"],
        "name": "Pentasure DM Diabetes Care Vanilla",
        "desc": "Complete diabetic medical formula enriched with taurine, carnitine and inositol to support glucose homeostasis.",
        "serv": 50.0, "net": 400.0, "label": "50g (4 scoops)",
        "n": [205.0, 11.0, 24.5, 7.0, 1.5, 0.0, 5.0, 4.0, 1.0, 0.0, 160.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, High Oleic Sunflower Oil, FOS, Inositol, Taurine, L-Carnitine, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Diabetic-Friendly", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Soy Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://pentasure.com/products/pentasure-dm",
        "image_url": None,
        "price": 850.0, "mrp": 980.0,
        "variant_title": "400g Tin"
    },
    # 19. Pentasure Renal Vanilla
    {
        "pick": ["manual", "pentasure-renal-vanilla", "adult-nutrition", "Pentasure"],
        "name": "Pentasure Renal Nutritional Supplement Vanilla",
        "desc": "Specialized kidney health formula with low electrolytes (sodium, potassium, phosphorus) and high calorie density.",
        "serv": 50.0, "net": 400.0, "label": "50g (4 scoops)",
        "n": [209.0, 9.5, 28.0, 6.5, 1.5, 0.0, 5.0, 2.0, 2.0, 0.0, 75.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, MCT Oil, Low Erucic Rapeseed Oil, FOS, Low Electrolyte Mineral Premix, Vitamins, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Clinical Nutrition", "Low Electrolyte", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://pentasure.com/products/pentasure-renal",
        "image_url": None,
        "price": 1199.0, "mrp": 1390.0,
        "variant_title": "400g Tin"
    },
    # 20. Fresenius Kabi Fresubin HP High Protein Vanilla
    {
        "pick": ["manual", "fresenius-kabi-fresubin-hp-high-protein-vanilla", "adult-nutrition", "Fresenius Kabi"],
        "name": "Fresubin HP High Protein Vanilla",
        "desc": "European clinical nutrition standard formula offering 42% balanced whey and casein proteins for patient recovery.",
        "serv": 50.0, "net": 400.0, "label": "50g (5 scoops)",
        "n": [192.0, 21.0, 22.5, 2.0, 1.0, 0.0, 15.0, 2.0, 3.5, 0.0, 170.0],
        "ing": "Whey Protein Concentrate, Calcium Caseinate, Maltodextrin, Inulin, Sunflower Oil, Vitamins & Minerals, Vanilla Flavor, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Clinical Nutrition", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.fresenius-kabi.com/in/products/fresubin-hp",
        "image_url": None,
        "price": 1050.0, "mrp": 1200.0,
        "variant_title": "400g Tin"
    }
]

print(f"Total Wave 4 products prepared: {len(WAVE_4_PRODUCTS)}")

# Pre-validate all math
KEYS = ["kcal", "protein", "carbs", "fat", "sat_fat", "trans_fat", "chol", "fiber", "sugar", "added_sugar", "sod"]
errors = []

for idx, p in enumerate(WAVE_4_PRODUCTS, 1):
    n = dict(zip(KEYS, p["n"]))
    serv = p["serv"]
    net = p["net"]
    
    # 1. Atwater check
    est = 4 * n["protein"] + 4 * n["carbs"] + 9 * n["fat"]
    diff = abs(est - n["kcal"])
    if diff > max(25, 0.2 * n["kcal"]):
        errors.append(f"{p['name']}: calories {n['kcal']} vs est {est:.1f} (diff={diff:.1f})")
        
    # 2. Physical limits
    if n["protein"] > serv:
        errors.append(f"{p['name']}: protein > serv ({n['protein']} > {serv})")
    if (n["protein"] + n["carbs"] + n["fat"]) > serv * 1.05:
        errors.append(f"{p['name']}: macros > serv ({n['protein']+n['carbs']+n['fat']} > {serv})")
        
    # 3. Sub-nutrients
    if n["sat_fat"] > n["fat"] + 0.05:
        errors.append(f"{p['name']}: sat_fat > fat ({n['sat_fat']} > {n['fat']})")
    if n["sugar"] > n["carbs"] + 0.05:
        errors.append(f"{p['name']}: sugar > carbs ({n['sugar']} > {n['carbs']})")
    if n["added_sugar"] > n["sugar"] + 0.05:
        errors.append(f"{p['name']}: added_sugar > sugar ({n['added_sugar']} > {n['sugar']})")

    # 4. Pack math drift
    spp = max(1, round(net / serv))
    drift = abs(spp * serv - net) / net
    if drift > 0.25:
        errors.append(f"{p['name']}: pack drift {drift:.1%} exceeds 25% (net={net}, serv={serv})")

print(f"Pre-validation complete. Errors found: {len(errors)}")
if errors:
    for e in errors:
        print("  ERROR:", e)
else:
    print("ALL 20 WAVE 4 PRODUCTS PASSED VALIDATION WITH 0 ERRORS!")
