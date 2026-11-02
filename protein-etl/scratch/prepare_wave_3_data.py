"""Wave 3 Dataset: Functional Bakery, Cookies & RTD Drinks (+25 Products)

Categories:
- cookies-baked: 15 products
- rtd-drinks: 6 products
- savory-snacks: 4 products
"""

import json

WAVE_3_PRODUCTS = [
    # --- COOKIES & BAKED (15 Products) ---
    # 1. The Whole Truth Protein Brownie Fudgy Dark Chocolate
    {
        "pick": ["manual", "the-whole-truth-protein-brownie-fudgy-dark-chocolate", "cookies-baked", "The Whole Truth"],
        "name": "Protein Brownie Fudgy Dark Chocolate",
        "desc": "Rich fudgy bakery brownie packed with 12g whey protein isolate, dates, almonds and zero refined sugar.",
        "serv": 55.0, "net": 55.0, "label": "55g (1 brownie)",
        "n": [209.0, 12.0, 20.0, 9.0, 4.5, 0.0, 10.0, 4.0, 9.0, 0.0, 75.0],
        "ing": "Dates, Whey Protein Isolate, Dark Chocolate (Cocoa Solids, Cocoa Butter), Almonds, Cashews, Cocoa Powder",
        "allergens": ["Milk", "Almonds", "Cashews"],
        "tags": ["Vegetarian", "Gluten-Free", "Clean Label", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://thewholetruthfoods.com/products/protein-brownie-fudgy-dark-chocolate",
        "image_url": None,
        "price": 120.0, "mrp": 130.0,
        "variant_title": "55g Brownie"
    },
    # 2. The Whole Truth Protein Brownie Hazelnut Chocolate
    {
        "pick": ["manual", "the-whole-truth-protein-brownie-hazelnut-chocolate", "cookies-baked", "The Whole Truth"],
        "name": "Protein Brownie Hazelnut Chocolate",
        "desc": "Decadent hazelnut chocolate brownie delivering 12g protein from pure whey isolate and roasted hazelnuts.",
        "serv": 55.0, "net": 55.0, "label": "55g (1 brownie)",
        "n": [212.0, 12.0, 19.5, 9.5, 4.0, 0.0, 10.0, 4.0, 8.5, 0.0, 70.0],
        "ing": "Dates, Whey Protein Isolate, Roasted Hazelnuts, Dark Chocolate (Cocoa Solids, Cocoa Butter), Almonds, Cocoa Powder",
        "allergens": ["Milk", "Hazelnuts", "Almonds"],
        "tags": ["Vegetarian", "Gluten-Free", "Clean Label", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://thewholetruthfoods.com/products/protein-brownie-hazelnut-chocolate",
        "image_url": None,
        "price": 130.0, "mrp": 140.0,
        "variant_title": "55g Brownie"
    },
    # 3. The Whole Truth Soft Baked Protein Cookie Double Dark Chocolate
    {
        "pick": ["manual", "the-whole-truth-soft-baked-cookie-double-dark-chocolate", "cookies-baked", "The Whole Truth"],
        "name": "Soft Baked Protein Cookie Double Dark Chocolate",
        "desc": "Soft chewy double chocolate cookie delivering 10g protein made exclusively from oats, whey isolate and cocoa butter.",
        "serv": 50.0, "net": 50.0, "label": "50g (1 cookie)",
        "n": [196.0, 10.0, 21.0, 8.0, 3.5, 0.0, 5.0, 4.5, 8.0, 0.0, 80.0],
        "ing": "Oat Flour, Whey Protein Isolate, Dark Chocolate Chips, Dates, Butter, Cocoa Powder, Sea Salt",
        "allergens": ["Milk", "Oats"],
        "tags": ["Vegetarian", "Clean Label", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://thewholetruthfoods.com/products/protein-cookie-double-chocolate",
        "image_url": None,
        "price": 99.0, "mrp": 110.0,
        "variant_title": "50g Cookie"
    },
    # 4. The Whole Truth Soft Baked Protein Cookie Peanut Butter Chunk
    {
        "pick": ["manual", "the-whole-truth-soft-baked-cookie-peanut-butter-chunk", "cookies-baked", "The Whole Truth"],
        "name": "Soft Baked Protein Cookie Peanut Butter Chunk",
        "desc": "Nutty protein cookie packed with roasted peanut chunks and whey protein isolate for 11g clean protein.",
        "serv": 50.0, "net": 50.0, "label": "50g (1 cookie)",
        "n": [201.0, 11.0, 19.0, 9.0, 3.0, 0.0, 5.0, 4.0, 7.0, 0.0, 85.0],
        "ing": "Peanut Butter, Oat Flour, Whey Protein Isolate, Dates, Roasted Peanut Chunks, Butter, Sea Salt",
        "allergens": ["Milk", "Peanuts", "Oats"],
        "tags": ["Vegetarian", "Clean Label", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Isolate & Peanut Butter",
        "protein_tier": "tier_1",
        "url": "https://thewholetruthfoods.com/products/protein-cookie-peanut-butter",
        "image_url": None,
        "price": 99.0, "mrp": 110.0,
        "variant_title": "50g Cookie"
    },
    # 5. Phab High Protein Brownie Fudgy Chocolate
    {
        "pick": ["manual", "phab-high-protein-brownie-fudgy-chocolate", "cookies-baked", "Phab"],
        "name": "High Protein Brownie Fudgy Chocolate",
        "desc": "Guilt-free chocolate fudge brownie providing 10g balanced protein and zero added sugar for active sweet tooths.",
        "serv": 50.0, "net": 50.0, "label": "50g (1 brownie)",
        "n": [191.0, 10.0, 22.0, 7.0, 3.5, 0.0, 10.0, 3.0, 6.0, 0.0, 90.0],
        "ing": "Protein Blend (Whey Protein Concentrate, Milk Protein Isolate), Cocoa Butter, Dietary Fiber, Dark Compound, Cocoa Powder, Stevia",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "High Protein", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://getphab.com/products/protein-brownie-chocolate",
        "image_url": None,
        "price": 99.0, "mrp": 115.0,
        "variant_title": "50g Brownie"
    },
    # 6. Phab High Protein Brownie Walnut Chocolate
    {
        "pick": ["manual", "phab-high-protein-brownie-walnut-chocolate", "cookies-baked", "Phab"],
        "name": "High Protein Brownie Walnut Chocolate",
        "desc": "Crispy walnut loaded chocolate brownie delivering 10g protein and gut-healthy prebiotic fiber.",
        "serv": 50.0, "net": 50.0, "label": "50g (1 brownie)",
        "n": [196.0, 10.0, 21.0, 8.0, 3.2, 0.0, 10.0, 3.5, 6.0, 0.0, 85.0],
        "ing": "Protein Blend (Whey Protein Concentrate, Milk Protein Isolate), Walnuts, Cocoa Butter, Dietary Fiber, Dark Compound, Cocoa Powder, Stevia",
        "allergens": ["Milk", "Walnuts"],
        "tags": ["Vegetarian", "High Protein", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Milk Protein Isolate",
        "protein_tier": "tier_2",
        "url": "https://getphab.com/products/protein-brownie-walnut",
        "image_url": None,
        "price": 105.0, "mrp": 120.0,
        "variant_title": "50g Brownie"
    },
    # 7. RiteBite Max Protein Cookie 7 Grain Choco Almond
    {
        "pick": ["manual", "ritebite-max-protein-cookie-choco-almond", "cookies-baked", "RiteBite Max Protein"],
        "name": "7 Grain Breakfast Protein Cookie Choco Almond",
        "desc": "Nutrient-dense breakfast cookie fortified with 7 grains, roasted almonds and 10g dual-source protein.",
        "serv": 55.0, "net": 55.0, "label": "55g (1 cookie)",
        "n": [220.0, 10.0, 26.0, 8.5, 3.8, 0.0, 10.0, 4.0, 9.0, 4.0, 110.0],
        "ing": "Protein Blend (Soy Protein Concentrate, Whey Protein Concentrate), 7 Grain Flour Blend (Oats, Ragi, Bajra, Jowar, Wheat, Quinoa, Corn), Roasted Almonds, Dark Choco Chips, Honey",
        "allergens": ["Milk", "Soy", "Almonds", "Wheat", "Oats"],
        "tags": ["Vegetarian", "High Protein", "High-Fibre"],
        "is_vegan": False,
        "protein_source": "Soy Protein Concentrate & Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://maxprotein.in/products/max-protein-choco-almond-cookie",
        "image_url": None,
        "price": 55.0, "mrp": 60.0,
        "variant_title": "55g Cookie"
    },
    # 8. RiteBite Max Protein Cookie 7 Grain Oats & Raisins
    {
        "pick": ["manual", "ritebite-max-protein-cookie-oats-raisins", "cookies-baked", "RiteBite Max Protein"],
        "name": "7 Grain Breakfast Protein Cookie Oats & Raisins",
        "desc": "Traditional morning cookie loaded with rolled oats, juicy black raisins and 10g sustained protein.",
        "serv": 55.0, "net": 55.0, "label": "55g (1 cookie)",
        "n": [215.0, 10.0, 27.0, 7.5, 3.2, 0.0, 10.0, 4.5, 8.5, 3.5, 105.0],
        "ing": "Protein Blend (Soy Protein Concentrate, Whey Protein Concentrate), 7 Grain Flour Blend (Oats, Ragi, Bajra, Jowar, Wheat, Quinoa), Black Raisins, Honey, Cinnamon",
        "allergens": ["Milk", "Soy", "Wheat", "Oats"],
        "tags": ["Vegetarian", "High Protein", "High-Fibre"],
        "is_vegan": False,
        "protein_source": "Soy Protein Concentrate & Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://maxprotein.in/products/max-protein-oats-raisins-cookie",
        "image_url": None,
        "price": 55.0, "mrp": 60.0,
        "variant_title": "55g Cookie"
    },
    # 9. RiteBite Max Protein Cookie 7 Grain Nuts & Seeds
    {
        "pick": ["manual", "ritebite-max-protein-cookie-nuts-seeds", "cookies-baked", "RiteBite Max Protein"],
        "name": "7 Grain Breakfast Protein Cookie Nuts & Seeds",
        "desc": "Crunchy breakfast protein cookie packed with flax seeds, chia seeds, watermelon seeds and 10g protein.",
        "serv": 55.0, "net": 55.0, "label": "55g (1 cookie)",
        "n": [221.0, 10.0, 25.0, 9.0, 3.5, 0.0, 10.0, 4.0, 8.0, 3.5, 110.0],
        "ing": "Protein Blend (Soy Protein Concentrate, Whey Protein Concentrate), 7 Grain Flour Blend, Seed Blend (Flax, Chia, Watermelon, Pumpkin), Honey, Butter",
        "allergens": ["Milk", "Soy", "Wheat", "Oats"],
        "tags": ["Vegetarian", "High Protein", "High-Fibre"],
        "is_vegan": False,
        "protein_source": "Soy Protein Concentrate & Whey Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://maxprotein.in/products/max-protein-nuts-seeds-cookie",
        "image_url": None,
        "price": 55.0, "mrp": 60.0,
        "variant_title": "55g Cookie"
    },
    # 10. Ketofy High Protein Keto Cookies Almond Fudge
    {
        "pick": ["manual", "ketofy-high-protein-keto-cookies-almond-fudge", "cookies-baked", "Ketofy"],
        "name": "High Protein Keto Cookies Almond Fudge",
        "desc": "Ultra low carb almond flour keto cookies delivering 10.5g protein per serving and zero maltitol.",
        "serv": 50.0, "net": 200.0, "label": "50g (approx. 4 cookies)",
        "n": [235.0, 10.5, 11.0, 16.5, 5.5, 0.0, 0.0, 5.5, 1.5, 0.0, 95.0],
        "ing": "Almond Flour, Isolated Soy Protein, Cocoa Butter, Cocoa Powder, Erythritol, Butter, Vanilla Extract, Stevia",
        "allergens": ["Almonds", "Soy", "Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Almond Flour & Isolated Soy Protein",
        "protein_tier": "tier_3",
        "url": "https://www.ketofy.in/products/keto-cookies-almond-fudge",
        "image_url": None,
        "price": 299.0, "mrp": 349.0,
        "variant_title": "200g Box"
    },
    # 11. Ketofy High Protein Keto Cookies Coconut Crunch
    {
        "pick": ["manual", "ketofy-high-protein-keto-cookies-coconut-crunch", "cookies-baked", "Ketofy"],
        "name": "High Protein Keto Cookies Coconut Crunch",
        "desc": "Crispy shredded coconut keto cookies rich in healthy medium-chain fats and 10g clean protein.",
        "serv": 50.0, "net": 200.0, "label": "50g (approx. 4 cookies)",
        "n": [239.0, 10.0, 11.5, 17.0, 8.0, 0.0, 0.0, 5.0, 1.5, 0.0, 90.0],
        "ing": "Desiccated Coconut, Almond Flour, Isolated Soy Protein, Erythritol, Butter, Sea Salt, Stevia",
        "allergens": ["Almonds", "Soy", "Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Almond Flour & Isolated Soy Protein",
        "protein_tier": "tier_3",
        "url": "https://www.ketofy.in/products/keto-cookies-coconut",
        "image_url": None,
        "price": 299.0, "mrp": 349.0,
        "variant_title": "200g Box"
    },
    # 12. Lo! Foods High Protein Low Carb Chocolate Cookies
    {
        "pick": ["manual", "lo-foods-high-protein-low-carb-chocolate-cookies", "cookies-baked", "Lo! Foods"],
        "name": "High Protein Low Carb Chocolate Cookies",
        "desc": "Keto-compliant low carb chocolate cookies crafted with seed flours and whey delivering 8.5g protein.",
        "serv": 40.0, "net": 120.0, "label": "40g (approx. 3 cookies)",
        "n": [181.0, 8.5, 12.0, 11.0, 4.5, 0.0, 0.0, 4.5, 2.0, 0.0, 75.0],
        "ing": "Seed & Nut Flour Blend (Sunflower, Flax, Almond), Defatted Soy Flour, Whey Protein Concentrate, Cocoa, Butter, Erythritol, Stevia",
        "allergens": ["Milk", "Soy", "Almonds"],
        "tags": ["Vegetarian", "Low Carb", "Keto-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Defatted Soy Flour, Whey Concentrate & Seed Flour Blend",
        "protein_tier": "tier_3",
        "url": "https://lofoods.fit/products/low-carb-chocolate-cookies",
        "image_url": None,
        "price": 175.0, "mrp": 199.0,
        "variant_title": "120g Box"
    },
    # 13. Lo! Foods High Protein Low Carb Coconut Cookies
    {
        "pick": ["manual", "lo-foods-high-protein-low-carb-coconut-cookies", "cookies-baked", "Lo! Foods"],
        "name": "High Protein Low Carb Coconut Cookies",
        "desc": "Tropical coconut cookies baked with clean seed flours and whey protein for sustained keto energy.",
        "serv": 40.0, "net": 120.0, "label": "40g (approx. 3 cookies)",
        "n": [184.0, 8.5, 11.5, 11.5, 6.0, 0.0, 0.0, 4.5, 2.0, 0.0, 70.0],
        "ing": "Desiccated Coconut, Seed & Nut Flour Blend, Defatted Soy Flour, Whey Protein Concentrate, Butter, Erythritol, Stevia",
        "allergens": ["Milk", "Soy", "Almonds"],
        "tags": ["Vegetarian", "Low Carb", "Keto-Friendly", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Defatted Soy Flour, Whey Concentrate & Seed Flour Blend",
        "protein_tier": "tier_3",
        "url": "https://lofoods.fit/products/low-carb-coconut-cookies",
        "image_url": None,
        "price": 175.0, "mrp": 199.0,
        "variant_title": "120g Box"
    },
    # 14. Open Secret Unjunked High Protein Choco Sea Salt Cookies
    {
        "pick": ["manual", "open-secret-unjunked-protein-cookies-choco-sea-salt", "cookies-baked", "Open Secret"],
        "name": "Unjunked High Protein Choco Sea Salt Cookies",
        "desc": "Signature unjunked cookies with rich cocoa, sea salt crunch and 8g whey protein without palm oil.",
        "serv": 45.0, "net": 180.0, "label": "45g (approx. 3 cookies)",
        "n": [192.0, 8.0, 22.0, 8.0, 3.5, 0.0, 5.0, 3.5, 6.5, 0.0, 120.0],
        "ing": "Oats, Whey Protein Concentrate, Roasted Almonds, Cocoa Powder, Brown Sugar, Butter, Sea Salt",
        "allergens": ["Milk", "Almonds", "Oats"],
        "tags": ["Vegetarian", "Clean Label", "No Palm Oil"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Almonds",
        "protein_tier": "tier_2",
        "url": "https://opensecret.in/products/choco-sea-salt-cookies",
        "image_url": None,
        "price": 199.0, "mrp": 240.0,
        "variant_title": "180g Box"
    },
    # 15. Open Secret Unjunked High Protein Peanut Butter Cookies
    {
        "pick": ["manual", "open-secret-unjunked-protein-cookies-peanut-butter", "cookies-baked", "Open Secret"],
        "name": "Unjunked High Protein Peanut Butter Cookies",
        "desc": "Golden baked peanut butter cookies made with natural whole peanuts and whey protein.",
        "serv": 45.0, "net": 180.0, "label": "45g (approx. 3 cookies)",
        "n": [195.0, 8.5, 21.0, 8.5, 3.0, 0.0, 5.0, 3.5, 6.0, 0.0, 115.0],
        "ing": "Peanut Butter, Oats, Whey Protein Concentrate, Roasted Peanuts, Jaggery, Butter, Sea Salt",
        "allergens": ["Milk", "Peanuts", "Oats"],
        "tags": ["Vegetarian", "Clean Label", "No Palm Oil"],
        "is_vegan": False,
        "protein_source": "Whey Protein Concentrate & Peanut Butter",
        "protein_tier": "tier_2",
        "url": "https://opensecret.in/products/peanut-butter-cookies",
        "image_url": None,
        "price": 199.0, "mrp": 240.0,
        "variant_title": "180g Box"
    },

    # --- RTD DRINKS (6 Products) ---
    # 16. Raw Pressery High Protein Milkshake Cold Coffee
    {
        "pick": ["manual", "raw-pressery-high-protein-milkshake-cold-coffee", "rtd-drinks", "Raw Pressery"],
        "name": "High Protein Milkshake Cold Coffee",
        "desc": "Brewed Arabica cold coffee milkshake packing 18g milk protein per bottle with zero added sugar.",
        "serv": 200.0, "net": 200.0, "label": "200ml (1 bottle)",
        "n": [134.0, 18.0, 12.0, 1.5, 1.0, 0.0, 15.0, 0.0, 10.0, 0.0, 110.0],
        "ing": "Ultrafiltered Skimmed Milk, Milk Protein Concentrate, Coffee Extract, Cocoa Powder, Stevia, Lactase Enzyme",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Lactose-Free", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Ultrafiltered Skimmed Milk & Milk Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://www.rawpressery.com/products/protein-milkshake-cold-coffee",
        "image_url": None,
        "price": 120.0, "mrp": 130.0,
        "variant_title": "200ml Bottle"
    },
    # 17. Raw Pressery High Protein Milkshake Choco Hazelnut
    {
        "pick": ["manual", "raw-pressery-high-protein-milkshake-choco-hazelnut", "rtd-drinks", "Raw Pressery"],
        "name": "High Protein Milkshake Choco Hazelnut",
        "desc": "Decadent chocolate hazelnut protein shake delivering 18g pure dairy protein without any artificial colours.",
        "serv": 200.0, "net": 200.0, "label": "200ml (1 bottle)",
        "n": [142.0, 18.0, 13.0, 2.0, 1.2, 0.0, 15.0, 0.5, 11.0, 0.0, 120.0],
        "ing": "Ultrafiltered Skimmed Milk, Milk Protein Concentrate, Cocoa Solids, Natural Hazelnut Flavour, Stevia, Lactase Enzyme",
        "allergens": ["Milk", "Hazelnuts"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Lactose-Free", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Ultrafiltered Skimmed Milk & Milk Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://www.rawpressery.com/products/protein-milkshake-choco-hazelnut",
        "image_url": None,
        "price": 120.0, "mrp": 130.0,
        "variant_title": "200ml Bottle"
    },
    # 18. Raw Pressery High Protein Milkshake Vanilla Almond
    {
        "pick": ["manual", "raw-pressery-high-protein-milkshake-vanilla-almond", "rtd-drinks", "Raw Pressery"],
        "name": "High Protein Milkshake Vanilla Almond",
        "desc": "Smooth vanilla almond ready-to-drink shake enriched with 18g protein for easy on-the-go recovery.",
        "serv": 200.0, "net": 200.0, "label": "200ml (1 bottle)",
        "n": [138.0, 18.0, 12.5, 1.8, 1.0, 0.0, 15.0, 0.0, 10.5, 0.0, 115.0],
        "ing": "Ultrafiltered Skimmed Milk, Milk Protein Concentrate, Natural Vanilla Flavour, Natural Almond Extract, Stevia, Lactase Enzyme",
        "allergens": ["Milk", "Almonds"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "Lactose-Free", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Ultrafiltered Skimmed Milk & Milk Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://www.rawpressery.com/products/protein-milkshake-vanilla-almond",
        "image_url": None,
        "price": 120.0, "mrp": 130.0,
        "variant_title": "200ml Bottle"
    },
    # 19. Myprotein Clear Whey RTD Orange Mango
    {
        "pick": ["manual", "myprotein-clear-whey-rtd-orange-mango", "rtd-drinks", "Myprotein"],
        "name": "Clear Whey Isolate RTD Orange Mango",
        "desc": "Translucent fruity ready-to-drink shake providing 20g pure hydrolyzed whey isolate with zero milky texture.",
        "serv": 500.0, "net": 500.0, "label": "500ml (1 bottle)",
        "n": [91.0, 20.0, 2.5, 0.1, 0.0, 0.0, 5.0, 0.0, 1.0, 0.0, 45.0],
        "ing": "Water, Hydrolysed Whey Protein Isolate (Milk) (4.5%), Acidity Regulators (Citric Acid, Phosphoric Acid), Natural Flavouring, Sweetener (Sucralose)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Fat-Free", "No Added Sugar", "Clean Label"],
        "is_vegan": False,
        "protein_source": "Hydrolysed Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://www.myprotein.co.in/sports-nutrition/clear-whey-rtd/12655458.html",
        "image_url": None,
        "price": 299.0, "mrp": 350.0,
        "variant_title": "500ml Bottle"
    },
    # 20. Myprotein Clear Whey RTD Mixed Berry
    {
        "pick": ["manual", "myprotein-clear-whey-rtd-mixed-berry", "rtd-drinks", "Myprotein"],
        "name": "Clear Whey Isolate RTD Mixed Berry",
        "desc": "Light juice-style protein drink with 20g hydrolyzed isolate protein, zero fat and zero sugar.",
        "serv": 500.0, "net": 500.0, "label": "500ml (1 bottle)",
        "n": [91.0, 20.0, 2.5, 0.1, 0.0, 0.0, 5.0, 0.0, 1.0, 0.0, 45.0],
        "ing": "Water, Hydrolysed Whey Protein Isolate (Milk) (4.5%), Acidity Regulators (Citric Acid, Malic Acid), Natural Colouring (Beetroot Red), Natural Flavouring, Sweetener (Sucralose)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Fat-Free", "No Added Sugar", "Clean Label"],
        "is_vegan": False,
        "protein_source": "Hydrolysed Whey Protein Isolate",
        "protein_tier": "tier_1",
        "url": "https://www.myprotein.co.in/sports-nutrition/clear-whey-rtd/12655458.html",
        "image_url": None,
        "price": 299.0, "mrp": 350.0,
        "variant_title": "500ml Bottle"
    },
    # 21. Myprotein Protein Shake RTD Chocolate
    {
        "pick": ["manual", "myprotein-protein-shake-rtd-chocolate", "rtd-drinks", "Myprotein"],
        "name": "Protein Shake RTD Chocolate",
        "desc": "Creamy on-the-go chocolate milkshake packing 25g pure milk protein and low fat.",
        "serv": 330.0, "net": 330.0, "label": "330ml (1 carton)",
        "n": [174.0, 25.0, 15.0, 1.5, 0.8, 0.0, 20.0, 1.0, 14.0, 0.0, 180.0],
        "ing": "Skimmed Milk (75%), Water, Milk Protein Concentrate (8%), Fat Reduced Cocoa Powder, Flavouring, Stabiliser (Carrageenan), Sweetener (Sucralose)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "High Protein", "No Added Sugar"],
        "is_vegan": False,
        "protein_source": "Skimmed Milk & Milk Protein Concentrate",
        "protein_tier": "tier_2",
        "url": "https://www.myprotein.co.in/sports-nutrition/protein-shake-rtd/10530514.html",
        "image_url": None,
        "price": 249.0, "mrp": 299.0,
        "variant_title": "330ml Carton"
    },

    # --- SAVORY SNACKS (4 Products) ---
    # 22. Farmley High Protein Roasted Foxnuts Tangy Tomato
    {
        "pick": ["manual", "farmley-roasted-foxnuts-tangy-tomato", "savory-snacks", "Farmley"],
        "name": "High Protein Roasted Makhana Tangy Tomato",
        "desc": "Slow roasted crunchy phool makhana seasoned with zesty sun-ripe tomatoes, delivering clean fiber and plant protein.",
        "serv": 35.0, "net": 70.0, "label": "35g (approx. 1 bowl)",
        "n": [151.0, 5.5, 22.0, 4.5, 1.5, 0.0, 0.0, 3.5, 2.0, 0.0, 190.0],
        "ing": "Foxnuts (Makhana) (70%), Olive Oil, Tangy Tomato Seasoning (Tomato Powder, Chilli, Black Salt, Cumin), Roasted Lentil Protein Flour",
        "allergens": [],
        "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Clean Label", "No Added Sugar"],
        "is_vegan": True,
        "protein_source": "Pulse & Millet Flours",
        "protein_tier": "tier_3",
        "url": "https://farmley.com/products/roasted-makhana-tangy-tomato",
        "image_url": None,
        "price": 99.0, "mrp": 110.0,
        "variant_title": "70g Pouch"
    },
    # 23. Farmley High Protein Roasted Foxnuts Peri Peri
    {
        "pick": ["manual", "farmley-roasted-foxnuts-peri-peri", "savory-snacks", "Farmley"],
        "name": "High Protein Roasted Makhana Peri Peri",
        "desc": "Spicy roasted foxnuts infused with authentic African birds eye peri-peri seasoning and roasted plant proteins.",
        "serv": 35.0, "net": 70.0, "label": "35g (approx. 1 bowl)",
        "n": [151.0, 5.5, 22.0, 4.5, 1.5, 0.0, 0.0, 3.5, 1.5, 0.0, 210.0],
        "ing": "Foxnuts (Makhana) (70%), Olive Oil, Peri Peri Seasoning (Garlic, Onion, Red Chilli, Pepper, Oregano), Roasted Lentil Protein Flour",
        "allergens": [],
        "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Clean Label", "No Added Sugar"],
        "is_vegan": True,
        "protein_source": "Pulse & Millet Flours",
        "protein_tier": "tier_3",
        "url": "https://farmley.com/products/roasted-makhana-peri-peri",
        "image_url": None,
        "price": 99.0, "mrp": 110.0,
        "variant_title": "70g Pouch"
    },
    # 24. Farmley Roasted 7-in-1 Super Seeds Protein Mix
    {
        "pick": ["manual", "farmley-roasted-7-in-1-super-seeds-mix", "savory-snacks", "Farmley"],
        "name": "Roasted 7-in-1 Super Seeds Protein Mix",
        "desc": "Nutrient-packed roasted blend of pumpkin, chia, flax, watermelon, sesame, sunflower seeds with 25% protein.",
        "serv": 30.0, "net": 150.0, "label": "30g (approx. 2 tbsp)",
        "n": [160.0, 7.5, 5.5, 12.0, 2.2, 0.0, 0.0, 4.5, 0.8, 0.0, 60.0],
        "ing": "Roasted Pumpkin Seeds, Chia Seeds, Watermelon Seeds, Flax Seeds, Sesame Seeds, Sunflower Seeds, Rock Salt",
        "allergens": ["Sesame"],
        "tags": ["Vegan", "Vegetarian", "Gluten-Free", "Keto-Friendly", "Diabetic-Friendly", "High-Fibre", "No Added Sugar", "Clean Label"],
        "is_vegan": True,
        "protein_source": "Pumpkin Seed Protein",
        "protein_tier": "tier_3",
        "url": "https://farmley.com/products/7-in-1-seeds-mix",
        "image_url": None,
        "price": 175.0, "mrp": 199.0,
        "variant_title": "150g Jar"
    },
    # 25. Farmley High Protein Roasted Soy Nuts Salt & Pepper
    {
        "pick": ["manual", "farmley-roasted-soy-nuts-salt-pepper", "savory-snacks", "Farmley"],
        "name": "High Protein Roasted Soy Nuts Salt & Pepper",
        "desc": "Crunchy roasted non-GMO soybeans providing 40g plant protein per 100g with classic sea salt and cracked pepper.",
        "serv": 40.0, "net": 160.0, "label": "40g (approx. 1/4 cup)",
        "n": [162.0, 16.0, 11.0, 6.0, 1.0, 0.0, 0.0, 6.0, 2.0, 0.0, 180.0],
        "ing": "Roasted Soybeans (Non-GMO), Cold Pressed Edible Oil, Black Pepper, Himalayan Pink Salt",
        "allergens": ["Soy"],
        "tags": ["Vegan", "Vegetarian", "Gluten-Free", "High Protein", "Clean Label", "No Added Sugar"],
        "is_vegan": True,
        "protein_source": "Soy Protein Isolate",
        "protein_tier": "tier_3",
        "url": "https://farmley.com/products/roasted-soya-nuts",
        "image_url": None,
        "price": 149.0, "mrp": 175.0,
        "variant_title": "160g Pouch"
    }
]

print(f"Total Wave 3 products prepared: {len(WAVE_3_PRODUCTS)}")

# Pre-validate all math
KEYS = ["kcal", "protein", "carbs", "fat", "sat_fat", "trans_fat", "chol", "fiber", "sugar", "added_sugar", "sod"]
errors = []

for idx, p in enumerate(WAVE_3_PRODUCTS, 1):
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
    if p["pick"][2] not in ("rtd-drinks", "dairy") and (n["protein"] + n["carbs"] + n["fat"]) > serv * 1.05:
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
    print("ALL 25 WAVE 3 PRODUCTS PASSED VALIDATION WITH 0 ERRORS!")
