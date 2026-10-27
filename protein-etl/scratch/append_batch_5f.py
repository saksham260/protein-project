import json
from pathlib import Path

data_dir = Path("protein-etl/data/demo_catalog")

batch_5f = [
    {
        "handle": "max-protein-7-grain-protein-cookie-choco-chips",
        "category": "cookies-baked",
        "brand": "Max Protein",
        "manual": {
            "handle": "max-protein-7-grain-protein-cookie-choco-chips",
            "store": "manual",
            "brand": "Max Protein",
            "url": "https://ritebite.com/products/max-protein-7-grain-cookie-choco-chips",
            "image_url": "https://ritebite.com/cdn/shop/files/7GrainCookieChocoChips55g_Front.png",
            "variants": [
                {"id": 1, "title": "55g Cookie", "price": 50.0, "mrp": 50.0, "compare_at_price": 50.0, "net_weight_g": 55, "in_stock": True}
            ]
        },
        "reading": {
            "i": 442,
            "v": 0,
            "name": "7 Grain Protein Cookie Choco Chips",
            "variant": "55g Cookie",
            "net": 55,
            "serv": 55,
            "label": "55 g (1 cookie)",
            "n": [245.0, 10.0, 28.0, 10.5, 3.5, 0.0, 0.0, 5.0, 8.5, 5.0, 95.0],
            "ing": "Protein Blend (Soy Protein Isolate, Whey Protein Concentrate), 7 Grain Flour Blend (Oats, Ragi, Quinoa, Corn, Wheat, Bengal Gram, Amaranth), Dark Chocolate Chips (12%), Rice Bran Oil, Prebiotic Fibre (FOS), Jaggery",
            "allergens": ["Milk", "Soy", "Wheat", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Guilt-free baked protein cookie packed with 10g protein and 7 wholesome ancient grains. Crafted with no maida and no palm oil for clean everyday snacking.",
            "protein_source": "Soy Protein Isolate & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "max-protein-7-grain-protein-cookie-oats-raisins",
        "category": "cookies-baked",
        "brand": "Max Protein",
        "manual": {
            "handle": "max-protein-7-grain-protein-cookie-oats-raisins",
            "store": "manual",
            "brand": "Max Protein",
            "url": "https://ritebite.com/products/max-protein-7-grain-cookie-oats-raisins",
            "image_url": "https://ritebite.com/cdn/shop/files/7GrainCookieOatsRaisins55g_Front.png",
            "variants": [
                {"id": 1, "title": "55g Cookie", "price": 50.0, "mrp": 50.0, "compare_at_price": 50.0, "net_weight_g": 55, "in_stock": True}
            ]
        },
        "reading": {
            "i": 443,
            "v": 0,
            "name": "7 Grain Protein Cookie Oats & Raisins",
            "variant": "55g Cookie",
            "net": 55,
            "serv": 55,
            "label": "55 g (1 cookie)",
            "n": [240.0, 10.0, 29.0, 9.5, 3.0, 0.0, 0.0, 5.5, 9.0, 4.5, 90.0],
            "ing": "Protein Blend (Soy Protein Isolate, Whey Protein Concentrate), 7 Grain Flour (Oats, Ragi, Quinoa, Corn, Wheat, Bengal Gram, Amaranth), Rolled Oats, Black Raisins, Rice Bran Oil, Prebiotic Fibre (FOS), Cinnamon",
            "allergens": ["Milk", "Soy", "Wheat", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Wholesome baked cookie combining chewy rolled oats, plump raisins, and 10g high quality dairy & soy protein. 100% vegetarian with zero trans fats.",
            "protein_source": "Soy Protein Isolate & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "max-protein-7-grain-protein-cookie-nuts-seeds",
        "category": "cookies-baked",
        "brand": "Max Protein",
        "manual": {
            "handle": "max-protein-7-grain-protein-cookie-nuts-seeds",
            "store": "manual",
            "brand": "Max Protein",
            "url": "https://ritebite.com/products/max-protein-7-grain-cookie-nuts-seeds",
            "image_url": "https://ritebite.com/cdn/shop/files/7GrainCookieNutsSeeds55g_Front.png",
            "variants": [
                {"id": 1, "title": "55g Cookie", "price": 50.0, "mrp": 50.0, "compare_at_price": 50.0, "net_weight_g": 55, "in_stock": True}
            ]
        },
        "reading": {
            "i": 444,
            "v": 0,
            "name": "7 Grain Protein Cookie Nuts & Seeds",
            "variant": "55g Cookie",
            "net": 55,
            "serv": 55,
            "label": "55 g (1 cookie)",
            "n": [248.0, 10.0, 27.0, 11.0, 3.2, 0.0, 0.0, 5.2, 7.5, 4.0, 90.0],
            "ing": "Protein Blend (Soy Protein Isolate, Whey Protein Concentrate), 7 Grain Flour, Roasted Almonds, Pumpkin Seeds, Watermelon Seeds, Chia Seeds, Rice Bran Oil, Prebiotic Fibre (FOS)",
            "allergens": ["Milk", "Soy", "Wheat", "Almonds", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Crunchy power cookie loaded with roasted California almonds, pumpkin seeds, and chia seeds. 10g protein and gut-friendly prebiotic fibre.",
            "protein_source": "Soy Protein Isolate & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "the-whole-truth-protein-cookie-dark-chocolate",
        "category": "cookies-baked",
        "brand": "The Whole Truth",
        "manual": {
            "handle": "the-whole-truth-protein-cookie-dark-chocolate",
            "store": "manual",
            "brand": "The Whole Truth",
            "url": "https://thewholetruthfoods.com/products/protein-cookie-dark-chocolate",
            "image_url": "https://thewholetruthfoods.com/cdn/shop/products/protein_cookie_dark_chocolate_50g.jpg",
            "variants": [
                {"id": 1, "title": "50g Cookie", "price": 80.0, "mrp": 80.0, "compare_at_price": 80.0, "net_weight_g": 50, "in_stock": True}
            ]
        },
        "reading": {
            "i": 445,
            "v": 0,
            "name": "Protein Cookie Dark Chocolate",
            "variant": "50g Cookie",
            "net": 50,
            "serv": 50,
            "label": "50 g (1 cookie)",
            "n": [218.0, 10.0, 23.0, 9.5, 2.2, 0.0, 2.0, 4.5, 9.0, 0.0, 40.0],
            "ing": "Whey Protein Concentrate, Dates, Rolled Oats, Raw Cacao Powder (12%), Almond Butter, Cocoa Butter, Pink Himalayan Salt",
            "allergens": ["Milk", "Oats", "Almonds"],
            "tags": ["Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar"],
            "desc": "100% clean-label baked protein cookie with only 7 real pantry ingredients. Sweetened exclusively with whole dates — zero refined sugar, zero artificial sweeteners, zero maida.",
            "protein_source": "Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "the-whole-truth-protein-cookie-cranberry-almond",
        "category": "cookies-baked",
        "brand": "The Whole Truth",
        "manual": {
            "handle": "the-whole-truth-protein-cookie-cranberry-almond",
            "store": "manual",
            "brand": "The Whole Truth",
            "url": "https://thewholetruthfoods.com/products/protein-cookie-cranberry-almond",
            "image_url": "https://thewholetruthfoods.com/cdn/shop/products/protein_cookie_cranberry_almond_50g.jpg",
            "variants": [
                {"id": 1, "title": "50g Cookie", "price": 80.0, "mrp": 80.0, "compare_at_price": 80.0, "net_weight_g": 50, "in_stock": True}
            ]
        },
        "reading": {
            "i": 446,
            "v": 0,
            "name": "Protein Cookie Cranberry & Almond",
            "variant": "50g Cookie",
            "net": 50,
            "serv": 50,
            "label": "50 g (1 cookie)",
            "n": [215.0, 10.0, 23.5, 9.0, 1.8, 0.0, 2.0, 4.2, 10.0, 0.0, 35.0],
            "ing": "Whey Protein Concentrate, Dates, Rolled Oats, Roasted Almonds (15%), Dried Cranberries, Almond Butter, Vanilla Extract, Pink Himalayan Salt",
            "allergens": ["Milk", "Oats", "Almonds"],
            "tags": ["Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar"],
            "desc": "Clean baked cookie made with whole roasted almonds, tangy cranberries, and grass-fed whey protein. Naturally sweetened with whole dates.",
            "protein_source": "Whey Protein Concentrate & Almonds",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "open-secret-unjunked-high-protein-choco-almond-cookies",
        "category": "cookies-baked",
        "brand": "Open Secret",
        "manual": {
            "handle": "open-secret-unjunked-high-protein-choco-almond-cookies",
            "store": "manual",
            "brand": "Open Secret",
            "url": "https://opensecret.in/products/unjunked-protein-cookies-choco-almond",
            "image_url": "https://opensecret.in/cdn/shop/files/OpenSecret_ChocoAlmond_60g.png",
            "variants": [
                {"id": 1, "title": "60g Pack", "price": 60.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 60, "in_stock": True}
            ]
        },
        "reading": {
            "i": 447,
            "v": 0,
            "name": "Unjunked High Protein Choco Almond Cookies",
            "variant": "60g Pack",
            "net": 60,
            "serv": 60,
            "label": "60 g (approx. 4 cookies)",
            "n": [285.0, 12.0, 26.0, 14.5, 3.5, 0.0, 0.0, 4.8, 7.0, 4.0, 75.0],
            "ing": "Nuts (Almonds & Peanuts 45%), Protein Blend (Pea Protein Isolate, Whey Protein), Cocoa Solids, Jaggery, Rice Flour, Butter",
            "allergens": ["Almonds", "Peanuts", "Milk"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Unjunked nutty cookies crafted with 45% real nuts and 12g protein per pack. Zero maida, zero artificial preservatives, zero refined white sugar.",
            "protein_source": "Almonds, Peanuts, Pea Protein & Whey Protein",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ketofy-chocolate-keto-cookies",
        "category": "cookies-baked",
        "brand": "Ketofy",
        "manual": {
            "handle": "ketofy-chocolate-keto-cookies",
            "store": "manual",
            "brand": "Ketofy",
            "url": "https://ketofy.in/products/ketofy-chocolate-cookies",
            "image_url": "https://ketofy.in/cdn/shop/products/Keto_Chocolate_Cookies_200g.png",
            "variants": [
                {"id": 1, "title": "200g Box", "price": 299.0, "mrp": 349.0, "compare_at_price": 349.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": 448,
            "v": 0,
            "name": "Ketofy Chocolate Keto Cookies (Ultra Low Carb)",
            "variant": "200g Box",
            "net": 200,
            "serv": 20,
            "label": "20 g (approx. 2 cookies)",
            "n": [85.0, 4.0, 3.2, 6.2, 1.5, 0.0, 0.0, 2.4, 0.2, 0.0, 25.0],
            "ing": "Almond Flour, Isolated Soy Protein, Cocoa Powder, Watermelon Seed Flour, Flax Seed Meal, Erythritol, Butter, Vanilla Extract, Stevia",
            "allergens": ["Almonds", "Soy", "Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "No Added Sugar"],
            "desc": "Rich chocolate keto cookies delivering only 0.8g net carbs and 4g protein per serving. Sweetened naturally with erythritol and stevia for ketogenic diets.",
            "protein_source": "Almond Flour & Soy Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ketofy-high-protein-keto-bhujia-sev",
        "category": "savory-snacks",
        "brand": "Ketofy",
        "manual": {
            "handle": "ketofy-high-protein-keto-bhujia-sev",
            "store": "manual",
            "brand": "Ketofy",
            "url": "https://ketofy.in/products/ketofy-keto-bhujia",
            "image_url": "https://ketofy.in/cdn/shop/products/Keto_Bhujia_150g.png",
            "variants": [
                {"id": 1, "title": "150g", "price": 199.0, "mrp": 249.0, "compare_at_price": 249.0, "net_weight_g": 150, "in_stock": True}
            ]
        },
        "reading": {
            "i": 449,
            "v": 0,
            "name": "High Protein Keto Bhujia / Sev",
            "variant": "150g",
            "net": 150,
            "serv": 50,
            "label": "50 g",
            "n": [240.0, 14.0, 7.0, 17.0, 2.5, 0.0, 0.0, 5.5, 0.5, 0.0, 180.0],
            "ing": "Defatted Soya Flour, Isolated Wheat Protein, Almond Flour, Cold Pressed Groundnut Oil, Ajwain, Black Pepper, Himalayan Pink Salt, Hing, Spices",
            "allergens": ["Soy", "Wheat", "Almonds", "Peanuts"],
            "tags": ["Vegetarian", "Keto-Friendly", "Diabetic-Friendly", "High-Fibre", "No Added Sugar"],
            "desc": "Crispy, traditional Indian spicy bhujia redesigned for keto. Packed with 28% protein and only 3g net carbs per 100g, crafted with cold-pressed oils and zero potato starch.",
            "protein_source": "Defatted Soya, Isolated Wheat Protein & Almonds",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ketofy-high-protein-keto-nachos-peri-peri",
        "category": "savory-snacks",
        "brand": "Ketofy",
        "manual": {
            "handle": "ketofy-high-protein-keto-nachos-peri-peri",
            "store": "manual",
            "brand": "Ketofy",
            "url": "https://ketofy.in/products/ketofy-keto-nachos-peri-peri",
            "image_url": "https://ketofy.in/cdn/shop/products/Keto_Nachos_PeriPeri_100g.png",
            "variants": [
                {"id": 1, "title": "100g", "price": 149.0, "mrp": 179.0, "compare_at_price": 179.0, "net_weight_g": 100, "in_stock": True}
            ]
        },
        "reading": {
            "i": 450,
            "v": 0,
            "name": "High Protein Keto Nachos Peri Peri",
            "variant": "100g",
            "net": 100,
            "serv": 50,
            "label": "50 g",
            "n": [232.0, 12.5, 8.5, 16.5, 2.2, 0.0, 0.0, 5.0, 1.0, 0.0, 210.0],
            "ing": "Almond Flour, Flaxseed Meal, Chia Seeds, Psyllium Husk, Isolated Soy Protein, Cold Pressed Sunflower Oil, Peri Peri Seasoning (Chilli, Garlic, Onion, Salt)",
            "allergens": ["Almonds", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "High-Fibre", "No Added Sugar"],
            "desc": "Crunchy triangle tortilla nachos made from almonds and super seeds with a zesty peri-peri kick. 25% protein and low glycemic index.",
            "protein_source": "Almond Flour & Soy Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "eat-better-co-high-protein-spicy-seed-trail-mix",
        "category": "savory-snacks",
        "brand": "Eat Better Co",
        "manual": {
            "handle": "eat-better-co-high-protein-spicy-seed-trail-mix",
            "store": "manual",
            "brand": "Eat Better Co",
            "url": "https://eatbetterco.com/products/high-protein-spicy-seed-mix",
            "image_url": "https://eatbetterco.com/cdn/shop/products/Spicy_Seed_Mix_160g.png",
            "variants": [
                {"id": 1, "title": "160g Pouch", "price": 180.0, "mrp": 199.0, "compare_at_price": 199.0, "net_weight_g": 160, "in_stock": True}
            ]
        },
        "reading": {
            "i": 451,
            "v": 0,
            "name": "High Protein Spicy Seed Trail Mix (Nut-Free)",
            "variant": "160g Pouch",
            "net": 160,
            "serv": 40,
            "label": "40 g (approx. 2 tbsp)",
            "n": [192.0, 9.6, 8.0, 13.5, 2.2, 0.0, 0.0, 4.0, 0.8, 0.0, 110.0],
            "ing": "Roasted Pumpkin Seeds, Roasted Watermelon Seeds, Roasted Sunflower Seeds, Roasted Flax Seeds, Roasted Soy Crisps, Spices & Condiments (Cumin, Red Chilli, Dry Mango, Black Pepper), Himalayan Pink Salt",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "Gluten-Free", "Nut-Free", "Jain", "High-Fibre", "No Added Sugar"],
            "desc": "100% nut-free, allergy-friendly roasted seed snack providing 24g protein per 100g. Perfectly spiced for Indian palates, vegan, and compliant with strict Jain dietary rules (no root vegetables).",
            "protein_source": "Pumpkin Seeds, Sunflower Seeds & Soy Crisps",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ritebite-daily-protein-bar-choco-berry",
        "category": "protein-bars",
        "brand": "RiteBite",
        "manual": {
            "handle": "ritebite-daily-protein-bar-choco-berry",
            "store": "manual",
            "brand": "RiteBite",
            "url": "https://ritebite.com/products/daily-protein-bar-choco-berry",
            "image_url": "https://ritebite.com/cdn/shop/files/DailyBarChocoBerry50g_Front.png",
            "variants": [
                {"id": 1, "title": "50g Bar", "price": 70.0, "mrp": 70.0, "compare_at_price": 70.0, "net_weight_g": 50, "in_stock": True}
            ]
        },
        "reading": {
            "i": 452,
            "v": 0,
            "name": "Daily Protein Bar Choco Berry",
            "variant": "50g Bar",
            "net": 50,
            "serv": 50,
            "label": "50 g (1 bar)",
            "n": [185.0, 10.0, 23.0, 5.5, 2.2, 0.0, 0.0, 5.0, 7.0, 4.0, 75.0],
            "ing": "Protein Blend (Soy Protein Nuggets, Whey Protein Concentrate, Calcium Caseinate), Dark Compound, Dietary Fibre (FOS), Dried Cranberries, Strawberries, Oats, Honey, 21 Vitamins & Minerals",
            "allergens": ["Milk", "Soy", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Everyday pocket snack delivering 10g protein, 21 essential vitamins & minerals, and electrolyte balance with the sweet-tart goodness of real berries.",
            "protein_source": "Soy Protein Nuggets, Whey Protein Concentrate & Calcium Caseinate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ritebite-daily-protein-bar-choco-almond",
        "category": "protein-bars",
        "brand": "RiteBite",
        "manual": {
            "handle": "ritebite-daily-protein-bar-choco-almond",
            "store": "manual",
            "brand": "RiteBite",
            "url": "https://ritebite.com/products/daily-protein-bar-choco-almond",
            "image_url": "https://ritebite.com/cdn/shop/files/DailyBarChocoAlmond50g_Front.png",
            "variants": [
                {"id": 1, "title": "50g Bar", "price": 70.0, "mrp": 70.0, "compare_at_price": 70.0, "net_weight_g": 50, "in_stock": True}
            ]
        },
        "reading": {
            "i": 453,
            "v": 0,
            "name": "Daily Protein Bar Choco Almond",
            "variant": "50g Bar",
            "net": 50,
            "serv": 50,
            "label": "50 g (1 bar)",
            "n": [188.0, 10.0, 22.5, 6.0, 2.4, 0.0, 0.0, 5.0, 6.5, 3.5, 75.0],
            "ing": "Protein Blend (Soy Protein Nuggets, Whey Protein Concentrate), Roasted California Almonds (12%), Dark Chocolate Coating, Dietary Fibre, Rolled Oats, Honey, Vitamins & Minerals",
            "allergens": ["Milk", "Soy", "Almonds", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Satisfying snack bar packed with roasted crunchy almonds, chocolate chips, and 10g balanced protein for afternoon hunger.",
            "protein_source": "Soy Protein Nuggets & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "phab-high-protein-bar-strawberries-cream",
        "category": "protein-bars",
        "brand": "Phab",
        "manual": {
            "handle": "phab-high-protein-bar-strawberries-cream",
            "store": "manual",
            "brand": "Phab",
            "url": "https://getphab.com/products/high-protein-bar-strawberries-cream",
            "image_url": "https://getphab.com/cdn/shop/files/PhabBarStrawberries60g_Front.png",
            "variants": [
                {"id": 1, "title": "60g Bar", "price": 120.0, "mrp": 140.0, "compare_at_price": 140.0, "net_weight_g": 60, "in_stock": True}
            ]
        },
        "reading": {
            "i": 454,
            "v": 0,
            "name": "High Protein Bar Strawberries & Cream",
            "variant": "60g Bar",
            "net": 60,
            "serv": 60,
            "label": "60 g (1 bar)",
            "n": [215.0, 21.0, 15.0, 7.0, 2.8, 0.0, 5.0, 6.5, 1.5, 0.0, 95.0],
            "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Calcium Caseinate), Dietary Fibre (Oligofructose), White Chocolate Drizzle, Dried Strawberries, Glycerin, Stevia",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "High-Fibre", "No Added Sugar"],
            "desc": "Heavy-hitting 21g protein bar crafted with pure whey isolate and real strawberry fruit. Zero added sugar, gluten-free, with prebiotic digestive fibre.",
            "protein_source": "Whey Protein Isolate & Calcium Caseinate",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "cosmix-raw-plant-protein-unflavoured",
        "category": "protein-powders",
        "brand": "Cosmix",
        "manual": {
            "handle": "cosmix-raw-plant-protein-unflavoured",
            "store": "manual",
            "brand": "Cosmix",
            "url": "https://cosmix.in/products/no-nonsense-plant-protein-raw-unflavoured",
            "image_url": "https://cosmix.in/cdn/shop/files/cosmix_raw_unflavoured_500g.png",
            "variants": [
                {"id": 1, "title": "500g Pouch", "price": 1399.0, "mrp": 1599.0, "compare_at_price": 1599.0, "net_weight_g": 500, "in_stock": True}
            ]
        },
        "reading": {
            "i": 455,
            "v": 0,
            "name": "Raw Plant Protein Unflavoured (Single-Ingredient)",
            "variant": "500g Pouch",
            "net": 500,
            "serv": 35,
            "label": "35 g (1 scoop)",
            "n": [136.0, 28.0, 2.5, 1.5, 0.3, 0.0, 0.0, 1.8, 0.0, 0.0, 85.0],
            "ing": "Organic Fermented Yellow Pea Protein Isolate (70%), Organic Sprouted Brown Rice Protein (30%)",
            "allergens": [],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "Gluten-Free", "Nut-Free", "Soy-Free", "Jain", "Diabetic-Friendly", "No Added Sugar"],
            "desc": "Zero-additive raw hypoallergenic plant protein powder. 28g protein per scoop with complete amino acid profile, naturally easy on sensitive guts and free of all major allergens.",
            "protein_source": "Organic Yellow Pea & Sprouted Brown Rice Isolate",
            "protein_tier": "tier_3"
        }
    }
]

# Append manual entries
manual_path = data_dir / "manual_entries.jsonl"
existing_manual = manual_path.read_text(encoding="utf-8")
if not existing_manual.endswith("\n"):
    existing_manual += "\n"
new_manual_lines = [json.dumps(x["manual"], ensure_ascii=False) for x in batch_5f]
manual_path.write_text(existing_manual + "\n".join(new_manual_lines) + "\n", encoding="utf-8")

# Append picks
picks_path = data_dir / "picks.txt"
existing_picks = picks_path.read_text(encoding="utf-8")
if not existing_picks.endswith("\n"):
    existing_picks += "\n"
new_picks_lines = [f"manual|{x['handle']}|{x['category']}|{x['brand']}" for x in batch_5f]
picks_path.write_text(existing_picks + "\n".join(new_picks_lines) + "\n", encoding="utf-8")

# Append readings
readings_path = data_dir / "readings.jsonl"
existing_readings = readings_path.read_text(encoding="utf-8")
if not existing_readings.endswith("\n"):
    existing_readings += "\n"
new_readings_lines = [json.dumps(x["reading"], ensure_ascii=False) for x in batch_5f]
readings_path.write_text(existing_readings + "\n".join(new_readings_lines) + "\n", encoding="utf-8")

print(f"Batch 5F appended successfully: {len(batch_5f)} items.")
