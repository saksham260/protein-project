import json
from pathlib import Path

data_dir = Path("protein-etl/data/demo_catalog")

batch_5e = [
    {
        "handle": "fortune-soya-chunks",
        "category": "staples",
        "brand": "Fortune",
        "manual": {
            "handle": "fortune-soya-chunks",
            "store": "manual",
            "brand": "Fortune",
            "url": "https://www.fortunefoods.com/products/fortune-soya-chunks",
            "image_url": "https://www.fortunefoods.com/sites/default/files/2021-06/soya-chunk-200g.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 50.0, "mrp": 50.0, "compare_at_price": 50.0, "net_weight_g": 200, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 220.0, "mrp": 220.0, "compare_at_price": 220.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 428,
            "v": 0,
            "name": "Fortune Soya Chunks (99% Fat Free)",
            "variant": "200g",
            "net": 200,
            "serv": 100,
            "label": "100 g (uncooked)",
            "n": [345.0, 52.0, 33.0, 0.5, 0.1, 0.0, 0.0, 13.0, 0.0, 0.0, 20.0],
            "ing": "Defatted Soya Flour (100%)",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar", "Gluten-Free"],
            "desc": "99% fat-free defatted soya chunks delivering an unmatched 52g of plant protein per 100g. A highly economical, versatile, and complete vegetarian protein kitchen staple.",
            "protein_source": "100% Defatted Soya Flour",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "nutrela-soya-chunks",
        "category": "staples",
        "brand": "Nutrela",
        "manual": {
            "handle": "nutrela-soya-chunks",
            "store": "manual",
            "brand": "Nutrela",
            "url": "https://www.nutrelanutrition.com/product/nutrela-soya-chunks",
            "image_url": "https://patanjaliayurved.net/media/images/product/soya_chunks_200g.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 55.0, "mrp": 55.0, "compare_at_price": 55.0, "net_weight_g": 200, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 240.0, "mrp": 240.0, "compare_at_price": 240.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 429,
            "v": 0,
            "name": "Nutrela Soya Chunks Classic",
            "variant": "200g",
            "net": 200,
            "serv": 100,
            "label": "100 g (uncooked)",
            "n": [345.0, 52.0, 33.0, 0.5, 0.1, 0.0, 0.0, 13.0, 0.0, 0.0, 20.0],
            "ing": "Defatted Soya Flour (100%)",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar", "Gluten-Free"],
            "desc": "India's original household soya chunks packed with 52g protein per 100g, 15 times more protein than milk, providing essential amino acids for plant-based nutrition.",
            "protein_source": "100% Defatted Soya Flour",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "nutrela-soya-mini-chunks",
        "category": "staples",
        "brand": "Nutrela",
        "manual": {
            "handle": "nutrela-soya-mini-chunks",
            "store": "manual",
            "brand": "Nutrela",
            "url": "https://www.nutrelanutrition.com/product/nutrela-soya-mini-chunks",
            "image_url": "https://patanjaliayurved.net/media/images/product/soya_mini_chunks_200g.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 55.0, "mrp": 55.0, "compare_at_price": 55.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": 430,
            "v": 0,
            "name": "Nutrela Soya Mini Chunks",
            "variant": "200g",
            "net": 200,
            "serv": 100,
            "label": "100 g (uncooked)",
            "n": [345.0, 52.0, 33.0, 0.5, 0.1, 0.0, 0.0, 13.0, 0.0, 0.0, 20.0],
            "ing": "Defatted Soya Flour (100%)",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar", "Gluten-Free"],
            "desc": "Bite-sized mini soya chunks that cook quickly in curries, biryanis, and pulavs while absorbing spices effortlessly. 52g high bioavailable plant protein.",
            "protein_source": "100% Defatted Soya Flour",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "nutrela-soya-granules",
        "category": "staples",
        "brand": "Nutrela",
        "manual": {
            "handle": "nutrela-soya-granules",
            "store": "manual",
            "brand": "Nutrela",
            "url": "https://www.nutrelanutrition.com/product/nutrela-soya-granules",
            "image_url": "https://patanjaliayurved.net/media/images/product/soya_granules_200g.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 55.0, "mrp": 55.0, "compare_at_price": 55.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": 431,
            "v": 0,
            "name": "Nutrela Soya Granules",
            "variant": "200g",
            "net": 200,
            "serv": 100,
            "label": "100 g (uncooked)",
            "n": [345.0, 52.0, 33.0, 0.5, 0.1, 0.0, 0.0, 13.0, 0.0, 0.0, 20.0],
            "ing": "Defatted Soya Flour (100%)",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar", "Gluten-Free"],
            "desc": "Finely textured soya granules ideal for vegetarian bhurji, keema curries, cutlets, and paratha stuffing. High protein, zero cholesterol, low fat.",
            "protein_source": "100% Defatted Soya Flour",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "aashirvaad-proactive-high-protein-multigrain-atta",
        "category": "staples",
        "brand": "Aashirvaad",
        "manual": {
            "handle": "aashirvaad-proactive-high-protein-multigrain-atta",
            "store": "manual",
            "brand": "Aashirvaad",
            "url": "https://itcstore.in/products/aashirvaad-proactive-high-protein-multigrain-atta",
            "image_url": "https://itcstore.in/cdn/shop/files/aashirvaad_proactive_atta_1kg.png",
            "variants": [
                {"id": 1, "title": "1kg", "price": 110.0, "mrp": 110.0, "compare_at_price": 110.0, "net_weight_g": 1000, "in_stock": True},
                {"id": 2, "title": "5kg", "price": 480.0, "mrp": 480.0, "compare_at_price": 480.0, "net_weight_g": 5000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 432,
            "v": 0,
            "name": "Aashirvaad ProActive High Protein Multigrain Atta",
            "variant": "1kg",
            "net": 1000,
            "serv": 100,
            "label": "100 g (approx. 3 rotis)",
            "n": [366.0, 15.0, 70.0, 2.9, 0.5, 0.0, 0.0, 10.5, 2.5, 0.0, 15.0],
            "ing": "Whole Wheat Flour (85%), Defatted Roasted Soya Flour (10%), Oat Flour, Psyllium Husk (Isabgol)",
            "allergens": ["Wheat", "Soy", "Oats"],
            "tags": ["Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar"],
            "desc": "Nutrient-dense multigrain flour enriched with defatted soya and oats, delivering 15g protein and 10.5g dietary fibre per 100g for soft, wholesome high-protein rotis.",
            "protein_source": "Whole Wheat & Defatted Roasted Soya Flour",
            "protein_tier": "tier_1"
        }
    },
    {
        "handle": "lo-foods-ultra-low-carb-keto-atta",
        "category": "staples",
        "brand": "Lo! Foods",
        "manual": {
            "handle": "lo-foods-ultra-low-carb-keto-atta",
            "store": "manual",
            "brand": "Lo! Foods",
            "url": "https://lofoods.fit/products/ultra-low-carb-keto-atta",
            "image_url": "https://lofoods.fit/cdn/shop/products/Keto_Atta_1kg_Front.png",
            "variants": [
                {"id": 1, "title": "1kg", "price": 399.0, "mrp": 499.0, "compare_at_price": 499.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 433,
            "v": 0,
            "name": "Ultra Low Carb Keto Atta (3g Net Carbs)",
            "variant": "1kg",
            "net": 1000,
            "serv": 100,
            "label": "100 g (approx. 3 rotis)",
            "n": [380.0, 30.0, 18.0, 20.0, 2.5, 0.0, 0.0, 15.0, 1.0, 0.0, 45.0],
            "ing": "Defatted Soya Flour, Isolated Wheat Protein, Almond Flour, Flaxseed Meal, Pumpkin Seed Powder, Sunflower Seed Powder, Psyllium Husk",
            "allergens": ["Soy", "Wheat", "Almonds"],
            "tags": ["Vegetarian", "Keto-Friendly", "Diabetic-Friendly", "High-Fibre", "No Added Sugar"],
            "desc": "Engineered specifically for keto and low-carb lifestyles. Contains only 3g net carbs and a massive 30g protein per 100g, puffing like regular wheat rotis without any aftertaste.",
            "protein_source": "Defatted Soya, Isolated Wheat Protein & Seed Flours",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "ketofy-high-protein-keto-flour-atta",
        "category": "staples",
        "brand": "Ketofy",
        "manual": {
            "handle": "ketofy-high-protein-keto-flour-atta",
            "store": "manual",
            "brand": "Ketofy",
            "url": "https://ketofy.in/products/ketofy-keto-flour",
            "image_url": "https://ketofy.in/cdn/shop/products/ketofy_keto_flour_1kg.png",
            "variants": [
                {"id": 1, "title": "1kg", "price": 499.0, "mrp": 599.0, "compare_at_price": 599.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 434,
            "v": 0,
            "name": "Ketofy High Protein Keto Flour / Atta",
            "variant": "1kg",
            "net": 1000,
            "serv": 100,
            "label": "100 g",
            "n": [410.0, 36.0, 16.0, 22.0, 3.0, 0.0, 0.0, 12.0, 1.5, 0.0, 50.0],
            "ing": "Almond Flour, Peanut Flour, Flax Seed Meal, Watermelon Seed Flour, Psyllium Husk, Isolated Soy Protein",
            "allergens": ["Almonds", "Peanuts", "Soy"],
            "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "High-Fibre", "No Added Sugar"],
            "desc": "Ultra low-carb gluten-free keto flour made from nutrient-rich almonds and super seeds. Delivers 36g protein per 100g with ultra-low glycemic response.",
            "protein_source": "Almond, Peanut, Seed Flours & Soy Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "urban-platter-organic-firm-tofu",
        "category": "staples",
        "brand": "Urban Platter",
        "manual": {
            "handle": "urban-platter-organic-firm-tofu",
            "store": "manual",
            "brand": "Urban Platter",
            "url": "https://urbanplatter.in/products/urban-platter-organic-firm-tofu-200g",
            "image_url": "https://urbanplatter.in/cdn/shop/products/urban_platter_organic_firm_tofu_200g.png",
            "variants": [
                {"id": 1, "title": "200g", "price": 120.0, "mrp": 120.0, "compare_at_price": 120.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": 435,
            "v": 0,
            "name": "Organic Non-GMO Firm Tofu Block",
            "variant": "200g",
            "net": 200,
            "serv": 100,
            "label": "100 g",
            "n": [135.0, 16.0, 3.0, 6.5, 1.0, 0.0, 0.0, 2.0, 0.5, 0.0, 15.0],
            "ing": "Organic Certified Non-GMO Soybeans, Water, Coagulant (Calcium Sulphate, Nigari)",
            "allergens": ["Soy"],
            "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Clean Label", "Diabetic-Friendly", "Keto-Friendly", "No Added Sugar"],
            "desc": "Fresh vacuum-packed certified organic firm tofu made from whole non-GMO soybeans. 16g complete plant protein per 100g, firm texture that grills and sautés without crumbling.",
            "protein_source": "Whole Organic Non-GMO Soybeans",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "healthkart-high-protein-muesli-dark-chocolate",
        "category": "breakfast-cereals",
        "brand": "HealthKart",
        "manual": {
            "handle": "healthkart-high-protein-muesli-dark-chocolate",
            "store": "manual",
            "brand": "HealthKart",
            "url": "https://www.healthkart.com/sv/healthkart-high-protein-muesli/SP-88321",
            "image_url": "https://img4.hkrtcdn.com/20200/prd_2019943-HealthKart-HK-Vitals-High-Protein-Muesli-400-g-Dark-Chocolate-Cranberry_o.jpg",
            "variants": [
                {"id": 1, "title": "400g", "price": 399.0, "mrp": 499.0, "compare_at_price": 499.0, "net_weight_g": 400, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 849.0, "mrp": 999.0, "compare_at_price": 999.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 436,
            "v": 0,
            "name": "High Protein Muesli Dark Chocolate & Cranberry",
            "variant": "400g",
            "net": 400,
            "serv": 50,
            "label": "50 g (approx. 1/2 cup)",
            "n": [205.0, 11.0, 27.5, 5.5, 1.2, 0.0, 2.0, 4.5, 6.0, 3.0, 60.0],
            "ing": "Multigrain Flakes (Rolled Oats, Wheat Flakes, Quinoa Flakes), Whey Protein Concentrate, Roasted Almonds, Dried Cranberries, Chia Seeds, Cocoa Solids, Jaggery",
            "allergens": ["Milk", "Wheat", "Almonds", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Crunchy multigrain muesli fortified with premium whey protein concentrate and roasted almonds. Delivers 22g protein per 100g for a powerful morning boost.",
            "protein_source": "Whey Protein Concentrate & Rolled Oats",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "muscleblaze-high-protein-oats-dark-chocolate",
        "category": "breakfast-cereals",
        "brand": "MuscleBlaze",
        "manual": {
            "handle": "muscleblaze-high-protein-oats-dark-chocolate",
            "store": "manual",
            "brand": "MuscleBlaze",
            "url": "https://www.muscleblaze.com/sv/muscleblaze-high-protein-oats/SP-109823",
            "image_url": "https://img2.hkrtcdn.com/28400/prd_2839931-MuscleBlaze-High-Protein-Oats-400-g-Dark-Chocolate_o.jpg",
            "variants": [
                {"id": 1, "title": "400g", "price": 299.0, "mrp": 399.0, "compare_at_price": 399.0, "net_weight_g": 400, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 649.0, "mrp": 799.0, "compare_at_price": 799.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 437,
            "v": 0,
            "name": "High Protein Oats Dark Chocolate",
            "variant": "400g",
            "net": 400,
            "serv": 50,
            "label": "50 g (approx. 1/2 cup)",
            "n": [198.0, 11.0, 28.0, 4.5, 1.0, 0.0, 3.0, 5.0, 4.0, 2.0, 55.0],
            "ing": "Rolled Oats (78%), Whey Protein Concentrate, Cocoa Powder, Chia Seeds, Roasted Pumpkin Seeds, Nature Identical Dark Chocolate Flavour, Sucralose",
            "allergens": ["Milk", "Oats"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Creamy instant rolled oats infused with whey protein concentrate and super seeds. Delivers 22g protein and rich dietary fibre per 100g to fuel long workouts.",
            "protein_source": "Whey Protein Concentrate & Whole Rolled Oats",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "the-whole-truth-dark-chocolate-high-protein-muesli",
        "category": "breakfast-cereals",
        "brand": "The Whole Truth",
        "manual": {
            "handle": "the-whole-truth-dark-chocolate-high-protein-muesli",
            "store": "manual",
            "brand": "The Whole Truth",
            "url": "https://thewholetruthfoods.com/products/dark-chocolate-protein-muesli",
            "image_url": "https://thewholetruthfoods.com/cdn/shop/products/dark_chocolate_protein_muesli_400g.jpg",
            "variants": [
                {"id": 1, "title": "400g", "price": 450.0, "mrp": 499.0, "compare_at_price": 499.0, "net_weight_g": 400, "in_stock": True}
            ]
        },
        "reading": {
            "i": 438,
            "v": 0,
            "name": "Dark Chocolate High Protein Muesli",
            "variant": "400g",
            "net": 400,
            "serv": 50,
            "label": "50 g",
            "n": [215.0, 10.5, 26.0, 7.5, 1.8, 0.0, 0.0, 4.8, 7.0, 0.0, 40.0],
            "ing": "Rolled Oats (45%), Whey Protein Isolate, Dates, Raw Cacao Powder (10%), Roasted Almonds, Chia Seeds, Flax Seeds",
            "allergens": ["Milk", "Oats", "Almonds"],
            "tags": ["Vegetarian", "Clean Label", "High-Fibre", "No Added Sugar"],
            "desc": "100% clean-label protein muesli made with whole rolled oats, whey isolate, and dark raw cacao. Sweetened exclusively with dates — 0 refined sugar, 0 artificial sweeteners.",
            "protein_source": "Whey Protein Isolate & Whole Oats",
            "protein_tier": "tier_3"
        }
    },
    {
        "handle": "pintola-high-protein-peanut-butter-dark-chocolate",
        "category": "protein-spreads",
        "brand": "Pintola",
        "manual": {
            "handle": "pintola-high-protein-peanut-butter-dark-chocolate",
            "store": "manual",
            "brand": "Pintola",
            "url": "https://pintola.in/products/high-protein-peanut-butter-dark-chocolate",
            "image_url": "https://pintola.in/cdn/shop/files/HP_PB_DarkChoc_510g.png",
            "variants": [
                {"id": 1, "title": "510g", "price": 499.0, "mrp": 499.0, "compare_at_price": 499.0, "net_weight_g": 510, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 899.0, "mrp": 899.0, "compare_at_price": 899.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 439,
            "v": 0,
            "name": "High Protein Peanut Butter Dark Chocolate (Crunchy)",
            "variant": "510g",
            "net": 510,
            "serv": 32,
            "label": "32 g (approx. 2 tbsp)",
            "n": [195.0, 10.5, 6.5, 14.0, 2.8, 0.0, 2.0, 2.5, 3.0, 1.5, 65.0],
            "ing": "Roasted Peanuts (80%), Whey Protein Isolate, Cocoa Powder, Brown Sugar, Stabilizer (INS 471)",
            "allergens": ["Peanuts", "Milk"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Premium slow-roasted peanut butter enriched with imported whey protein isolate and dark cocoa. Delivers 33g protein per 100g with a delicious crunchy texture.",
            "protein_source": "Roasted Peanuts & Whey Protein Isolate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "myfitness-high-protein-peanut-butter-crispy-chocolate",
        "category": "protein-spreads",
        "brand": "MyFitness",
        "manual": {
            "handle": "myfitness-high-protein-peanut-butter-crispy-chocolate",
            "store": "manual",
            "brand": "MyFitness",
            "url": "https://myfitness.in/products/high-protein-peanut-butter-crispy",
            "image_url": "https://myfitness.in/cdn/shop/files/Myfitness_Crispy_HP_510g.png",
            "variants": [
                {"id": 1, "title": "510g", "price": 549.0, "mrp": 549.0, "compare_at_price": 549.0, "net_weight_g": 510, "in_stock": True},
                {"id": 2, "title": "1kg", "price": 999.0, "mrp": 999.0, "compare_at_price": 999.0, "net_weight_g": 1000, "in_stock": True}
            ]
        },
        "reading": {
            "i": 440,
            "v": 0,
            "name": "High Protein Peanut Butter Crispy Dark Chocolate",
            "variant": "510g",
            "net": 510,
            "serv": 32,
            "label": "32 g (approx. 2 tbsp)",
            "n": [194.0, 10.2, 7.0, 13.8, 2.6, 0.0, 2.0, 2.4, 3.2, 1.6, 60.0],
            "ing": "Roasted Peanuts (78%), Whey Protein Concentrate, Cocoa Mass, Extruded Rice Crispies, Brown Sugar, Salt",
            "allergens": ["Peanuts", "Milk"],
            "tags": ["Vegetarian", "Gluten-Free"],
            "desc": "Iconic high-protein peanut butter infused with whey protein and crispy rice puffs for an irresistible crunch. Delivers 32g protein per 100g.",
            "protein_source": "Roasted Peanuts & Whey Protein Concentrate",
            "protein_tier": "tier_2"
        }
    },
    {
        "handle": "amul-fresh-malai-paneer-block",
        "category": "dairy",
        "brand": "Amul",
        "manual": {
            "handle": "amul-fresh-malai-paneer-block",
            "store": "manual",
            "brand": "Amul",
            "url": "https://shop.amul.com/en/browse/dairy",
            "image_url": "https://shop.amul.com/media/catalog/product/p/a/paneer_200g_front.png",
            "variants": [
                {"id": 1, "title": "200g Block", "price": 95.0, "mrp": 95.0, "compare_at_price": 95.0, "net_weight_g": 200, "in_stock": True}
            ]
        },
        "reading": {
            "i": 441,
            "v": 0,
            "name": "Fresh Malai Paneer Block",
            "variant": "200g Block",
            "net": 200,
            "serv": 100,
            "label": "100 g",
            "n": [289.0, 18.0, 4.0, 22.0, 14.0, 0.5, 60.0, 0.0, 4.0, 0.0, 40.0],
            "ing": "Pasteurised Milk, Coagulant (Citric Acid)",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "No Added Sugar"],
            "desc": "India's beloved pure dairy paneer made from fresh cow and buffalo milk. Rich in calcium and casein protein, yielding 18g protein per 100g block for traditional vegetarian dishes.",
            "protein_source": "Pure Milk Casein Curd",
            "protein_tier": "tier_2"
        }
    }
]

# Append manual entries
manual_path = data_dir / "manual_entries.jsonl"
existing_manual = manual_path.read_text(encoding="utf-8")
if not existing_manual.endswith("\n"):
    existing_manual += "\n"
new_manual_lines = [json.dumps(x["manual"], ensure_ascii=False) for x in batch_5e]
manual_path.write_text(existing_manual + "\n".join(new_manual_lines) + "\n", encoding="utf-8")

# Append picks
picks_path = data_dir / "picks.txt"
existing_picks = picks_path.read_text(encoding="utf-8")
if not existing_picks.endswith("\n"):
    existing_picks += "\n"
new_picks_lines = [f"manual|{x['handle']}|{x['category']}|{x['brand']}" for x in batch_5e]
picks_path.write_text(existing_picks + "\n".join(new_picks_lines) + "\n", encoding="utf-8")

# Append readings
readings_path = data_dir / "readings.jsonl"
existing_readings = readings_path.read_text(encoding="utf-8")
if not existing_readings.endswith("\n"):
    existing_readings += "\n"
new_readings_lines = [json.dumps(x["reading"], ensure_ascii=False) for x in batch_5e]
readings_path.write_text(existing_readings + "\n".join(new_readings_lines) + "\n", encoding="utf-8")

print(f"Batch 5E appended successfully: {len(batch_5e)} items.")
