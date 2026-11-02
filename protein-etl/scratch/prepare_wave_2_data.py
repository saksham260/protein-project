"""Wave 2 Dataset: Mass Gainers & Gym Staples (+30 Products)

Categories:
- mass-gainers: 29 products
- protein-powders: 1 product (Animal 100% Whey Isolate)
"""

import json

WAVE_2_PRODUCTS = [
    # 1. Labrada Muscle Mass Gainer Chocolate
    {
        "pick": ["manual", "labrada-muscle-mass-gainer-chocolate", "mass-gainers", "Labrada"],
        "name": "Muscle Mass Gainer Chocolate",
        "desc": "High-calorie mass builder engineered for hardgainers, delivering 52g protein and 1265 kcal per serving.",
        "serv": 333.0, "net": 3000.0, "label": "333g (9 scoops)",
        "n": [1265.0, 52.0, 250.0, 6.0, 3.5, 0.0, 90.0, 5.0, 20.0, 0.0, 420.0],
        "ing": "Maltodextrin, Cross Flow Micro-Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Calcium Caseinate, Cocoa Powder, Natural & Artificial Flavours, Fibersol-2, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Milk Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.labrada.com/products/muscle-mass-gainer",
        "image_url": None,
        "price": 3499.0, "mrp": 4699.0,
        "variant_title": "3kg Tub"
    },
    # 2. Labrada Muscle Mass Gainer Vanilla
    {
        "pick": ["manual", "labrada-muscle-mass-gainer-vanilla", "mass-gainers", "Labrada"],
        "name": "Muscle Mass Gainer Vanilla",
        "desc": "Creamy vanilla mass builder packed with 52g high-biological-value protein and BCAAs for muscle growth.",
        "serv": 333.0, "net": 3000.0, "label": "333g (9 scoops)",
        "n": [1265.0, 52.0, 252.0, 5.5, 3.0, 0.0, 85.0, 4.0, 20.0, 0.0, 410.0],
        "ing": "Maltodextrin, Cross Flow Micro-Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Calcium Caseinate, Natural & Artificial Flavours, Fibersol-2, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Milk Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.labrada.com/products/muscle-mass-gainer",
        "image_url": None,
        "price": 3499.0, "mrp": 4699.0,
        "variant_title": "3kg Tub"
    },
    # 3. Labrada Muscle Mass Gainer Strawberry
    {
        "pick": ["manual", "labrada-muscle-mass-gainer-strawberry", "mass-gainers", "Labrada"],
        "name": "Muscle Mass Gainer Strawberry",
        "desc": "Refreshing strawberry mass gainer loaded with complex carbs, essential amino acids and digestive enzymes.",
        "serv": 333.0, "net": 3000.0, "label": "333g (9 scoops)",
        "n": [1265.0, 52.0, 252.0, 5.5, 3.0, 0.0, 85.0, 4.0, 20.0, 0.0, 410.0],
        "ing": "Maltodextrin, Cross Flow Micro-Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Calcium Caseinate, Natural & Artificial Flavours, Beetroot Powder (Colour), Fibersol-2, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Milk Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.labrada.com/products/muscle-mass-gainer",
        "image_url": None,
        "price": 3499.0, "mrp": 4699.0,
        "variant_title": "3kg Tub"
    },
    # 4. Labrada Muscle Mass Gainer Banana
    {
        "pick": ["manual", "labrada-muscle-mass-gainer-banana", "mass-gainers", "Labrada"],
        "name": "Muscle Mass Gainer Banana",
        "desc": "Smooth banana flavour mass gainer with sustained-release protein blend for anabolic muscle building.",
        "serv": 333.0, "net": 3000.0, "label": "333g (9 scoops)",
        "n": [1265.0, 52.0, 252.0, 5.5, 3.0, 0.0, 85.0, 4.0, 20.0, 0.0, 410.0],
        "ing": "Maltodextrin, Cross Flow Micro-Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Calcium Caseinate, Natural & Artificial Flavours, Fibersol-2, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Milk Protein Isolate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.labrada.com/products/muscle-mass-gainer",
        "image_url": None,
        "price": 3499.0, "mrp": 4699.0,
        "variant_title": "3kg Tub"
    },
    # 5. Dymatize Super Mass Gainer Gourmet Chocolate
    {
        "pick": ["manual", "dymatize-super-mass-gainer-gourmet-chocolate", "mass-gainers", "Dymatize"],
        "name": "Super Mass Gainer Gourmet Chocolate",
        "desc": "Powerhouse mass gainer formulated with 52g protein, 10.7g BCAAs and 1g creatine monohydrate per serving.",
        "serv": 333.0, "net": 2720.0, "label": "333g (2.5 scoops)",
        "n": [1280.0, 52.0, 252.0, 7.0, 3.5, 0.0, 135.0, 4.0, 22.0, 0.0, 500.0],
        "ing": "Dymatize Mass Gainer Blend (Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate, Whey Protein Hydrolysate, Micellar Casein), Maltodextrin, Cocoa Powder, Sunflower Creamer, Creatine Monohydrate, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.dymatize.com/super-mass-gainer",
        "image_url": None,
        "price": 4299.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Tub"
    },
    # 6. Dymatize Super Mass Gainer Rich Chocolate 12lb
    {
        "pick": ["manual", "dymatize-super-mass-gainer-rich-chocolate", "mass-gainers", "Dymatize"],
        "name": "Super Mass Gainer Rich Chocolate",
        "desc": "Mega-size 12 lb bag of Dymatize high-calorie gainer packed with fast and slow digesting muscle-building proteins.",
        "serv": 333.0, "net": 5440.0, "label": "333g (2.5 scoops)",
        "n": [1280.0, 52.0, 252.0, 7.0, 3.5, 0.0, 135.0, 4.0, 22.0, 0.0, 500.0],
        "ing": "Dymatize Mass Gainer Blend (Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate, Micellar Casein), Maltodextrin, Cocoa Powder, Creatine Monohydrate, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.dymatize.com/super-mass-gainer",
        "image_url": None,
        "price": 7699.0, "mrp": 9999.0,
        "variant_title": "5.44kg (12 lb) Bag"
    },
    # 7. Dymatize Super Mass Gainer Cookies & Cream
    {
        "pick": ["manual", "dymatize-super-mass-gainer-cookies-and-cream", "mass-gainers", "Dymatize"],
        "name": "Super Mass Gainer Cookies & Cream",
        "desc": "Decadent cookies and cream mass gainer featuring real cookie bits, 52g protein and complete vitamin support.",
        "serv": 333.0, "net": 2720.0, "label": "333g (2.5 scoops)",
        "n": [1280.0, 52.0, 254.0, 6.0, 3.0, 0.0, 130.0, 3.0, 23.0, 0.0, 520.0],
        "ing": "Dymatize Mass Gainer Blend (Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate), Maltodextrin, Cookie Bits, Sunflower Creamer, Creatine Monohydrate, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy", "Wheat"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.dymatize.com/super-mass-gainer",
        "image_url": None,
        "price": 4299.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Tub"
    },
    # 8. BSN True-Mass 1200 Chocolate Milkshake
    {
        "pick": ["manual", "bsn-true-mass-1200-chocolate-milkshake", "mass-gainers", "BSN"],
        "name": "True-Mass 1200 Chocolate Milkshake",
        "desc": "Ultra-premium super mass gainer designed for serious athletes seeking high-density clean calories and multi-stage protein.",
        "serv": 314.0, "net": 4710.0, "label": "314g (2 heaping scoops)",
        "n": [1230.0, 50.0, 222.0, 16.0, 5.0, 0.0, 150.0, 12.0, 18.0, 0.0, 530.0],
        "ing": "Complex Carbohydrate Blend (Maltodextrin, Rolled Oats), Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Milk Protein Isolate, Micellar Casein, Egg Albumin, Hydrolyzed Whey Protein), Cocoa, Medium Chain Triglycerides, Soy Lecithin, Sucralose",
        "allergens": ["Milk", "Egg", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Calcium Caseinate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.gobsn.com/en-us/Products/Weight-Gainers/TRUE-MASS-1200/p/true-mass-1200",
        "image_url": None,
        "price": 6499.0, "mrp": 8499.0,
        "variant_title": "4.71kg (10.38 lb) Bag"
    },
    # 9. BSN True-Mass 1200 Strawberry Milkshake
    {
        "pick": ["manual", "bsn-true-mass-1200-strawberry-milkshake", "mass-gainers", "BSN"],
        "name": "True-Mass 1200 Strawberry Milkshake",
        "desc": "Delicious strawberry milkshake mass gainer with whole oat flour, multi-source protein matrix and healthy fats.",
        "serv": 314.0, "net": 4710.0, "label": "314g (2 heaping scoops)",
        "n": [1230.0, 50.0, 224.0, 15.0, 4.5, 0.0, 145.0, 10.0, 19.0, 0.0, 510.0],
        "ing": "Complex Carbohydrate Blend (Maltodextrin, Rolled Oats), Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Milk Protein Isolate, Micellar Casein, Egg Albumin), Medium Chain Triglycerides, Natural & Artificial Flavours, Beet Juice Powder, Sucralose",
        "allergens": ["Milk", "Egg", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Calcium Caseinate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.gobsn.com/en-us/Products/Weight-Gainers/TRUE-MASS-1200/p/true-mass-1200",
        "image_url": None,
        "price": 6499.0, "mrp": 8499.0,
        "variant_title": "4.71kg (10.38 lb) Bag"
    },
    # 10. BSN True-Mass 1200 Vanilla Ice Cream
    {
        "pick": ["manual", "bsn-true-mass-1200-vanilla-ice-cream", "mass-gainers", "BSN"],
        "name": "True-Mass 1200 Vanilla Ice Cream",
        "desc": "Smooth vanilla ice cream flavoured mass gainer supporting intense workout recovery and lean size accumulation.",
        "serv": 314.0, "net": 4710.0, "label": "314g (2 heaping scoops)",
        "n": [1230.0, 50.0, 224.0, 15.0, 4.5, 0.0, 145.0, 10.0, 19.0, 0.0, 510.0],
        "ing": "Complex Carbohydrate Blend (Maltodextrin, Rolled Oats), Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Milk Protein Isolate, Micellar Casein, Egg Albumin), Medium Chain Triglycerides, Natural & Artificial Flavours, Sucralose",
        "allergens": ["Milk", "Egg", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Calcium Caseinate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.gobsn.com/en-us/Products/Weight-Gainers/TRUE-MASS-1200/p/true-mass-1200",
        "image_url": None,
        "price": 6499.0, "mrp": 8499.0,
        "variant_title": "4.71kg (10.38 lb) Bag"
    },
    # 11. Rule 1 R1 LBS Mass Gainer Chocolate Fudge
    {
        "pick": ["manual", "rule-1-r1-lbs-mass-gainer-chocolate-fudge", "mass-gainers", "Rule 1"],
        "name": "R1 LBS Mass Gainer Chocolate Fudge",
        "desc": "Hardcore weight gainer delivering a 5:1 carb-to-protein ratio, 40g whey protein and 1000+ quality calories.",
        "serv": 275.0, "net": 2750.0, "label": "275g (2 scoops)",
        "n": [1030.0, 40.0, 204.0, 6.0, 3.5, 0.0, 90.0, 4.0, 12.0, 0.0, 410.0],
        "ing": "Carbohydrate Blend (Maltodextrin, Organic Rice Bran, Pea Starch), Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate), Cocoa, Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Whey Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.ruleoneproteins.com/products/r1-lbs",
        "image_url": None,
        "price": 3999.0, "mrp": 5299.0,
        "variant_title": "2.75kg (6.06 lb) Tub"
    },
    # 12. Rule 1 R1 LBS Mass Gainer Vanilla Butter Cake
    {
        "pick": ["manual", "rule-1-r1-lbs-mass-gainer-vanilla-butter-cake", "mass-gainers", "Rule 1"],
        "name": "R1 LBS Mass Gainer Vanilla Butter Cake",
        "desc": "Rich bakery-inspired vanilla butter cake mass gainer with pure whey proteins, creatine and zero added creamers.",
        "serv": 275.0, "net": 2750.0, "label": "275g (2 scoops)",
        "n": [1030.0, 40.0, 205.0, 5.5, 3.0, 0.0, 85.0, 3.0, 13.0, 0.0, 400.0],
        "ing": "Carbohydrate Blend (Maltodextrin, Organic Rice Bran, Pea Starch), Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate), Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Whey Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.ruleoneproteins.com/products/r1-lbs",
        "image_url": None,
        "price": 3999.0, "mrp": 5299.0,
        "variant_title": "2.75kg (6.06 lb) Tub"
    },
    # 13. Rule 1 R1 LBS Mass Gainer Strawberries & Creme
    {
        "pick": ["manual", "rule-1-r1-lbs-mass-gainer-strawberries-and-creme", "mass-gainers", "Rule 1"],
        "name": "R1 LBS Mass Gainer Strawberries & Creme",
        "desc": "Fruity strawberries and cream weight gainer formulated for high-intensity athletes needing clean caloric surplus.",
        "serv": 275.0, "net": 2750.0, "label": "275g (2 scoops)",
        "n": [1030.0, 40.0, 205.0, 5.5, 3.0, 0.0, 85.0, 3.0, 13.0, 0.0, 400.0],
        "ing": "Carbohydrate Blend (Maltodextrin, Organic Rice Bran, Pea Starch), Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate), Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Beet Powder, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Whey Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.ruleoneproteins.com/products/r1-lbs",
        "image_url": None,
        "price": 3999.0, "mrp": 5299.0,
        "variant_title": "2.75kg (6.06 lb) Tub"
    },
    # 14. GNC Pro Performance Bulk 1340 Double Chocolate
    {
        "pick": ["manual", "gnc-pro-performance-bulk-1340-double-chocolate", "mass-gainers", "GNC India"],
        "name": "Pro Performance Bulk 1340 Double Chocolate",
        "desc": "High-potency mass gainer packing 1340 calories, 50g protein and 10g BCAAs per serving for maximum bulk.",
        "serv": 360.0, "net": 3240.0, "label": "360g (4 rounded scoops)",
        "n": [1340.0, 50.0, 277.0, 4.0, 2.0, 0.0, 95.0, 3.0, 20.0, 0.0, 540.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Whey Protein Isolate, Milk Protein Isolate, Egg Albumin), Cocoa, Creatine Monohydrate, Medium Chain Triglycerides, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Egg", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.guardian.in/products/gnc-pro-performance-bulk-1340",
        "image_url": None,
        "price": 3899.0, "mrp": 5499.0,
        "variant_title": "3.24kg (7.14 lb) Tub"
    },
    # 15. GNC Pro Performance Bulk 1340 Vanilla Ice Cream
    {
        "pick": ["manual", "gnc-pro-performance-bulk-1340-vanilla-ice-cream", "mass-gainers", "GNC India"],
        "name": "Pro Performance Bulk 1340 Vanilla Ice Cream",
        "desc": "Classic vanilla mass gainer delivering 50g anabolic protein, glutamine and complete micronutrients.",
        "serv": 360.0, "net": 3240.0, "label": "360g (4 rounded scoops)",
        "n": [1340.0, 50.0, 278.0, 3.5, 1.8, 0.0, 90.0, 2.0, 20.0, 0.0, 520.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Whey Protein Isolate, Milk Protein Isolate), Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.guardian.in/products/gnc-pro-performance-bulk-1340",
        "image_url": None,
        "price": 3899.0, "mrp": 5499.0,
        "variant_title": "3.24kg (7.14 lb) Tub"
    },
    # 16. GNC Pro Performance Bulk 1340 Strawberries and Cream
    {
        "pick": ["manual", "gnc-pro-performance-bulk-1340-strawberries-and-cream", "mass-gainers", "GNC India"],
        "name": "Pro Performance Bulk 1340 Strawberries and Cream",
        "desc": "Berry-sweet high calorie gainer designed to fuel intense training sessions and rapid muscular recovery.",
        "serv": 360.0, "net": 3240.0, "label": "360g (4 rounded scoops)",
        "n": [1340.0, 50.0, 278.0, 3.5, 1.8, 0.0, 90.0, 2.0, 20.0, 0.0, 520.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Whey Protein Isolate), Creatine Monohydrate, Medium Chain Triglycerides, Beetroot Extract, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.guardian.in/products/gnc-pro-performance-bulk-1340",
        "image_url": None,
        "price": 3899.0, "mrp": 5499.0,
        "variant_title": "3.24kg (7.14 lb) Tub"
    },
    # 17. MuscleTech Mass-Tech Elite Milk Chocolate
    {
        "pick": ["manual", "muscletech-mass-tech-elite-milk-chocolate", "mass-gainers", "MuscleTech"],
        "name": "Mass-Tech Elite Milk Chocolate",
        "desc": "Elite gainer featuring 63g multi-phase protein, ProHydrolase enzyme matrix and 10g HPLC-tested creatine.",
        "serv": 230.0, "net": 3180.0, "label": "230g (5 scoops)",
        "n": [860.0, 63.0, 132.0, 9.0, 5.0, 0.0, 170.0, 4.0, 10.0, 0.0, 580.0],
        "ing": "Multi-Phase Carb Complex (Maltodextrin, Oat Bran, Isomaltulose), Premium Whey Protein Matrix (Whey Protein Concentrate, Calcium Caseinate, Whey Protein Isolate, Hydrolyzed Whey Protein Isolate), Cocoa, Creatine Monohydrate, Medium Chain Triglycerides, ProHydrolase Enzymes, Sucralose",
        "allergens": ["Milk", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://muscletech.in/products/mass-tech-elite",
        "image_url": None,
        "price": 4699.0, "mrp": 6299.0,
        "variant_title": "3.18kg (7 lb) Tub"
    },
    # 18. MuscleTech Mass-Tech Elite Vanilla Cake
    {
        "pick": ["manual", "muscletech-mass-tech-elite-vanilla-cake", "mass-gainers", "MuscleTech"],
        "name": "Mass-Tech Elite Vanilla Cake",
        "desc": "Vanilla cake flavour elite gainer engineered to build dense muscle mass with 63g protein and 860 calories.",
        "serv": 230.0, "net": 3180.0, "label": "230g (5 scoops)",
        "n": [860.0, 63.0, 133.0, 8.5, 4.5, 0.0, 165.0, 3.0, 10.0, 0.0, 560.0],
        "ing": "Multi-Phase Carb Complex (Maltodextrin, Oat Bran, Isomaltulose), Premium Whey Protein Matrix (Whey Protein Concentrate, Calcium Caseinate, Whey Protein Isolate), Creatine Monohydrate, Natural & Artificial Flavors, ProHydrolase Enzymes, Sucralose",
        "allergens": ["Milk", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://muscletech.in/products/mass-tech-elite",
        "image_url": None,
        "price": 4699.0, "mrp": 6299.0,
        "variant_title": "3.18kg (7 lb) Tub"
    },
    # 19. Optimum Nutrition Serious Mass Vanilla
    {
        "pick": ["manual", "optimum-nutrition-serious-mass-vanilla", "mass-gainers", "Optimum Nutrition"],
        "name": "Serious Mass Weight Gainer Vanilla",
        "desc": "Gold standard weight gain formula offering 1250 calories and 50g protein to support high-intensity workout goals.",
        "serv": 334.0, "net": 2720.0, "label": "334g (2 heaping scoops)",
        "n": [1250.0, 50.0, 252.0, 4.5, 2.5, 0.0, 100.0, 4.0, 20.0, 0.0, 570.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Egg Albumin), Artificial Flavors, Mineral Blend, Creatine Monohydrate, L-Glutamine, Choline Bitartrate, Sucralose",
        "allergens": ["Milk", "Egg", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.optimumnutrition.co.in/serious-mass",
        "image_url": None,
        "price": 3299.0, "mrp": 3999.0,
        "variant_title": "2.72kg (6 lb) Tub"
    },
    # 20. Optimum Nutrition Serious Mass Banana
    {
        "pick": ["manual", "optimum-nutrition-serious-mass-banana", "mass-gainers", "Optimum Nutrition"],
        "name": "Serious Mass Weight Gainer Banana",
        "desc": "Creamy banana weight gainer delivering 50g blended protein, 250+ grams of carbs and 25 vitamins and minerals.",
        "serv": 334.0, "net": 2720.0, "label": "334g (2 heaping scoops)",
        "n": [1250.0, 50.0, 252.0, 4.5, 2.5, 0.0, 100.0, 4.0, 20.0, 0.0, 570.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Egg Albumin), Natural & Artificial Flavors, Mineral Blend, Creatine Monohydrate, L-Glutamine, Sucralose",
        "allergens": ["Milk", "Egg", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Calcium Caseinate",
        "protein_tier": "tier_2",
        "url": "https://www.optimumnutrition.co.in/serious-mass",
        "image_url": None,
        "price": 3299.0, "mrp": 3999.0,
        "variant_title": "2.72kg (6 lb) Tub"
    },
    # 21. Mutant Mass Extreme 2500 Triple Chocolate
    {
        "pick": ["manual", "mutant-mutant-mass-extreme-2500-triple-chocolate", "mass-gainers", "Mutant"],
        "name": "Mutant Mass Extreme 2500 Triple Chocolate",
        "desc": "Extreme calorie dense mass builder made with 100% pure whey protein and whole food carbo-blend.",
        "serv": 285.0, "net": 2720.0, "label": "285g (4 scoops)",
        "n": [1070.0, 30.0, 230.0, 3.0, 1.5, 0.0, 50.0, 5.0, 12.0, 0.0, 440.0],
        "ing": "Clean-Carb Blend (Maltodextrin, Waxy Maize Starch, Sweet Potato, Rolled Oats), 100% Pure Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate), Cocoa, MCT Oil, Sunflower Lecithin, Sucralose",
        "allergens": ["Milk", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Whey Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.iammutant.com/products/mutant-mass-extreme-2500",
        "image_url": None,
        "price": 4199.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Bag"
    },
    # 22. Mutant Mass Extreme 2500 Vanilla Ice Cream
    {
        "pick": ["manual", "mutant-mutant-mass-extreme-2500-vanilla-ice-cream", "mass-gainers", "Mutant"],
        "name": "Mutant Mass Extreme 2500 Vanilla Ice Cream",
        "desc": "Vanilla ice cream flavoured mutant mass gainer delivering 1070 clean calories per 4-scoop serving.",
        "serv": 285.0, "net": 2720.0, "label": "285g (4 scoops)",
        "n": [1070.0, 30.0, 231.0, 2.8, 1.4, 0.0, 45.0, 4.0, 12.0, 0.0, 420.0],
        "ing": "Clean-Carb Blend (Maltodextrin, Waxy Maize Starch, Sweet Potato, Rolled Oats), 100% Pure Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), MCT Oil, Natural Flavors, Sucralose",
        "allergens": ["Milk", "Soy", "Oats"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Whey Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://www.iammutant.com/products/mutant-mass-extreme-2500",
        "image_url": None,
        "price": 4199.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Bag"
    },
    # 23. Universal Nutrition Real Gains Chocolate Ice Cream
    {
        "pick": ["manual", "universal-nutrition-real-gains-chocolate", "mass-gainers", "Universal Nutrition"],
        "name": "Real Gains Weight Gainer Chocolate Ice Cream",
        "desc": "Hardcore lean mass formula crafted with fast and slow proteins, complex inulin fiber and healthy fats.",
        "serv": 155.0, "net": 3100.0, "label": "155g (3.5 scoops)",
        "n": [600.0, 52.0, 87.0, 5.0, 2.5, 0.0, 100.0, 4.0, 7.0, 0.0, 240.0],
        "ing": "Maltodextrin, Real Gains Protein Complex (Whey Protein Concentrate, Micellar Casein, Whey Protein Isolate), Dutch Processed Cocoa, Inulin, Flaxseed Powder, MCT Oil, Natural and Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Lean Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://www.universalnutrition.com/product/real-gains",
        "image_url": None,
        "price": 4499.0, "mrp": 5999.0,
        "variant_title": "3.1kg (6.85 lb) Tub"
    },
    # 24. Universal Nutrition Real Gains Banana
    {
        "pick": ["manual", "universal-nutrition-real-gains-banana", "mass-gainers", "Universal Nutrition"],
        "name": "Real Gains Weight Gainer Banana",
        "desc": "Clean calorie mass gainer delivering 52g protein and prebiotic inulin for gut-friendly muscle recovery.",
        "serv": 155.0, "net": 3100.0, "label": "155g (3.5 scoops)",
        "n": [600.0, 52.0, 87.0, 5.0, 2.5, 0.0, 100.0, 3.0, 7.0, 0.0, 230.0],
        "ing": "Maltodextrin, Real Gains Protein Complex (Whey Protein Concentrate, Micellar Casein, Whey Protein Isolate), Inulin, Flaxseed Powder, MCT Oil, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Lean Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://www.universalnutrition.com/product/real-gains",
        "image_url": None,
        "price": 4499.0, "mrp": 5999.0,
        "variant_title": "3.1kg (6.85 lb) Tub"
    },
    # 25. Animal 100% Whey Isolate Vanilla
    {
        "pick": ["manual", "animal-100-whey-isolate-vanilla", "protein-powders", "Animal"],
        "name": "100% Whey Isolate Vanilla",
        "desc": "Ultra-filtered cross-flow microfiltered pure whey isolate with 25g protein and under 1g fat per scoop.",
        "serv": 32.0, "net": 2270.0, "label": "32g (1 rounded scoop)",
        "n": [120.0, 25.0, 2.5, 1.0, 0.5, 0.0, 35.0, 0.0, 1.0, 0.0, 110.0],
        "ing": "Cross-Flow Microfiltered Whey Protein Isolate, Natural & Artificial Flavors, Cellulose Gum, Xanthan Gum, Sucralose, Acesulfame Potassium",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "No Added Sugar", "Clean Label"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://www.animalpak.com/products/animal-whey-isolate",
        "image_url": None,
        "price": 7499.0, "mrp": 8999.0,
        "variant_title": "2.27kg (5 lb) Tub"
    },
    # 26. Kevin Levrone LevroLegendary Mass Chocolate
    {
        "pick": ["manual", "kevin-levrone-levrolegendary-mass-chocolate", "mass-gainers", "Kevin Levrone"],
        "name": "LevroLegendary Mass Gainer Chocolate",
        "desc": "Signature series advanced mass gainer designed by IFBB legend Kevin Levrone with 42g protein per serving.",
        "serv": 200.0, "net": 3000.0, "label": "200g (4 scoops)",
        "n": [770.0, 42.0, 138.0, 4.5, 2.5, 0.0, 75.0, 2.0, 20.0, 0.0, 380.0],
        "ing": "Carbohydrate Complex (Maltodextrin, Glucose), Protein Complex (Milk Protein Concentrate, Whey Protein Concentrate Carbelac, Whey Protein Isolate Isolac, Hydrolysed Whey Protein Optipep), Cocoa, Thickener (Xanthan Gum), Flavourings",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Milk Protein Concentrate & Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://levrosupplements.com/products/levro-legendary-mass",
        "image_url": None,
        "price": 3499.0, "mrp": 4999.0,
        "variant_title": "3kg Tub"
    },
    # 27. Kevin Levrone Anabolic Mass Gainer Chocolate
    {
        "pick": ["manual", "kevin-levrone-anabolic-mass-gainer-chocolate", "mass-gainers", "Kevin Levrone"],
        "name": "Anabolic Mass Gainer Chocolate",
        "desc": "Powerful anabolic mass gainer enriched with creatine monohydrate, D-aspartic acid and fenugreek extract.",
        "serv": 120.0, "net": 3000.0, "label": "120g (2 scoops)",
        "n": [450.0, 36.0, 68.0, 3.5, 2.0, 0.0, 60.0, 2.0, 10.0, 0.0, 240.0],
        "ing": "Protein Complex (Whey Protein Concentrate, Whey Protein Isolate, Hydrolysed Whey Protein Concentrate, Micellar Casein), Carbohydrate Complex (Maltodextrin, Glucose), Creatine Monohydrate, DAA, Fenugreek Extract, Cocoa, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Mass Gainer", "Anabolic Matrix", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://levrosupplements.com/products/anabolic-mass",
        "image_url": None,
        "price": 3699.0, "mrp": 5299.0,
        "variant_title": "3kg Tub"
    },
    # 28. Ronnie Coleman King Mass XL Dark Chocolate
    {
        "pick": ["manual", "ronnie-coleman-king-mass-xl-dark-chocolate", "mass-gainers", "Ronnie Coleman"],
        "name": "King Mass XL Dark Chocolate",
        "desc": "Heavyweight mass builder engineered with 60g protein, 1000 calories and creatine to pack on royal size.",
        "serv": 250.0, "net": 2720.0, "label": "250g (4 scoops)",
        "n": [1000.0, 60.0, 178.0, 4.5, 2.0, 0.0, 80.0, 3.0, 25.0, 0.0, 340.0],
        "ing": "Coleman Sustained Delivery Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate, Milk Protein Isolate, Micellar Casein), Maltodextrin, Cocoa, Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Whey Protein Isolate & Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://ronniecoleman.net/products/king-mass-xl",
        "image_url": None,
        "price": 4199.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Bag"
    },
    # 29. Ronnie Coleman King Mass XL Vanilla
    {
        "pick": ["manual", "ronnie-coleman-king-mass-xl-vanilla", "mass-gainers", "Ronnie Coleman"],
        "name": "King Mass XL Vanilla",
        "desc": "Ultra-rich vanilla milkshake mass gainer supporting rapid post-workout glycogen synthesis and muscle repair.",
        "serv": 250.0, "net": 2720.0, "label": "250g (4 scoops)",
        "n": [1000.0, 60.0, 179.0, 4.0, 1.8, 0.0, 75.0, 2.0, 25.0, 0.0, 330.0],
        "ing": "Coleman Sustained Delivery Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate, Milk Protein Isolate, Micellar Casein), Maltodextrin, Creatine Monohydrate, Medium Chain Triglycerides, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "High Calorie", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate, Whey Protein Isolate & Micellar Casein",
        "protein_tier": "tier_2",
        "url": "https://ronniecoleman.net/products/king-mass-xl",
        "image_url": None,
        "price": 4199.0, "mrp": 5499.0,
        "variant_title": "2.72kg (6 lb) Bag"
    },
    # 30. Bigmuscles Nutrition Quick Mass Gainer Belgian Chocolate
    {
        "pick": ["manual", "bigmuscles-nutrition-quick-mass-gainer-belgian-chocolate", "mass-gainers", "Bigmuscles Nutrition"],
        "name": "Quick Mass Gainer Belgian Chocolate",
        "desc": "Fast-digesting muscle mass gainer with whey protein concentrate, complex carbs and digestive enzymes.",
        "serv": 150.0, "net": 3000.0, "label": "150g (3 scoops)",
        "n": [580.0, 45.0, 94.0, 2.5, 1.2, 0.0, 40.0, 3.0, 8.0, 0.0, 210.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Skimmed Milk Powder, Cocoa Powder, Starch, Dietary Fibre, Digestive Enzymes (Papain, Pepsin), Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Mass Gainer", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Skimmed Milk Powder",
        "protein_tier": "tier_2",
        "url": "https://bigmusclesnutrition.com/products/quick-mass",
        "image_url": None,
        "price": 1799.0, "mrp": 2499.0,
        "variant_title": "3kg Tub"
    }
]

print(f"Total Wave 2 products prepared: {len(WAVE_2_PRODUCTS)}")

# Pre-validate all math
KEYS = ["kcal", "protein", "carbs", "fat", "sat_fat", "trans_fat", "chol", "fiber", "sugar", "added_sugar", "sod"]
errors = []

for idx, p in enumerate(WAVE_2_PRODUCTS, 1):
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
    print("ALL 30 WAVE 2 PRODUCTS PASSED VALIDATION WITH 0 ERRORS!")
