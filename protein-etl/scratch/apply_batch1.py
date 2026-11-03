import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))
from src.models import slugify

load_dotenv(ROOT / "protein-etl" / ".env")
load_dotenv(ROOT / "protein-web" / ".env.local")

SUPABASE_URL = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_KEY)

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch1_imgs"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# 1. Upload all 24 WebP files in batch1_imgs to Supabase Storage 'product-images'
uploaded_urls = {}
for webp_file in sorted(IMG_DIR.glob("*.webp")):
    slug = webp_file.stem
    filename = webp_file.name
    data = webp_file.read_bytes()
    sb.storage.from_("product-images").upload(
        path=filename,
        file=data,
        file_options={"content-type": "image/webp", "upsert": "true"}
    )
    pub_url = f"{SUPABASE_URL}/storage/v1/object/public/product-images/{filename}"
    uploaded_urls[slug] = pub_url
    print(f"[UPLOADED] {filename} -> {pub_url}")

# Also include the already-uploaded Raw Pressery Cold Coffee
uploaded_urls["raw-pressery-high-protein-milkshake-cold-coffee"] = (
    f"{SUPABASE_URL}/storage/v1/object/public/product-images/raw-pressery-high-protein-milkshake-cold-coffee.webp"
)

# 2. Define the 6 duplicate line numbers (1-based) in picks.txt / readings.jsonl to remove
DUPLICATE_INDICES_TO_REMOVE = {
    537,  # the-whole-truth-soft-baked-cookie-double-dark-chocolate (dups the-whole-truth-protein-cookie-dark-chocolate)
    541,  # ritebite-max-protein-cookie-choco-almond (dups max-protein-7-grain-breakfast-protein-cookie-choco-almond)
    542,  # ritebite-max-protein-cookie-oats-raisins (dups max-protein-7-grain-protein-cookie-oats-raisins)
    543,  # ritebite-max-protein-cookie-nuts-seeds (dups max-protein-7-grain-protein-cookie-nuts-seeds)
    549,  # open-secret-unjunked-protein-cookies-peanut-butter (dups open-secret-peanut-butter-nutty-cookies)
    550,  # raw-pressery-high-protein-milkshake-cold-coffee (dups line 412 raw-pressery-high-protein-milkshake-cold-coffee)
}

# 3. Define the 24 real verified product replacements/updates keyed by their current 1-based index `i` in picks.txt/readings.jsonl
# Format: i -> (store, handle, category, brand, manual_entry_dict, reading_dict)
BATCH1_RECORDS = {
    410: (
        "manual",
        "phab-high-protein-milkshake-vanilla-almond",
        "rtd-drinks",
        "Phab",
        {
            "handle": "phab-high-protein-milkshake-vanilla-almond",
            "store": "manual",
            "brand": "Phab",
            "title": "Phab High Protein Milkshake Vanilla Almond",
            "url": "https://www.getphab.com/products/vanilla-almond-18g-protein-milkshake",
            "image_url": uploaded_urls["phab-high-protein-milkshake-vanilla-almond"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 125.0, "mrp": 125.0, "compare_at_price": 125.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["phab-high-protein-milkshake-vanilla-almond"]}],
        },
        {
            "v": 0,
            "name": "High Protein Milkshake Vanilla Almond",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [146.0, 18.0, 14.0, 2.0, 1.2, 0.0, 10.0, 1.5, 9.0, 0.0, 110.0],
            "ing": "Double Toned Milk, Milk Protein Concentrate, Almond Paste, Natural Vanilla Extract, Stabilizer (INS 407), Sweetener (Sucralose), Vitamins & Minerals",
            "allergens": ["Milk", "Tree Nuts"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Ready-to-drink 18g protein milkshake blended with real vanilla and almond, zero added sugar, and gut-friendly prebiotic fiber.",
            "protein_source": "Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    448: (
        "manual",
        "lo-foods-protein-chef-keto-almond-cookies",
        "cookies-baked",
        "Lo! Foods",
        {
            "handle": "lo-foods-protein-chef-keto-almond-cookies",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Protein Chef Keto Almond Cookies",
            "url": "https://lofoods.fit/products/keto-cookies-almond",
            "image_url": uploaded_urls["lo-foods-protein-chef-keto-almond-cookies"],
            "variants": [{"id": 1, "title": "150g Pack", "price": 279.0, "mrp": 299.0, "compare_at_price": 299.0, "net_weight_g": 150.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-protein-chef-keto-almond-cookies"]}],
        },
        {
            "v": 0,
            "name": "Protein Chef Keto Almond Cookies",
            "variant": "150g Pack",
            "net": 150.0,
            "serv": 30.0,
            "label": "2 cookies (30g)",
            "n": [142.0, 6.0, 7.0, 10.0, 4.2, 0.0, 8.0, 3.0, 0.5, 0.0, 65.0],
            "ing": "Almond Flour, Wheat Protein Isolate, Sunflower Seeds, Flax Seeds, Butter, Erythritol, Baking Powder",
            "allergens": ["Milk", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "Keto-Friendly", "No Added Sugar", "Low-Carb"],
            "desc": "Ultra-low-carb keto almond cookies baked with superfood seeds and nuts, delivering 6g protein and 1g net carbs per cookie with no maida or added sugar.",
            "protein_source": "Almond & Wheat Protein Isolate",
            "protein_tier": "tier_3",
        },
    ),
    449: (
        "manual",
        "lo-foods-protein-chef-baked-bikaneri-bhujia",
        "savory-snacks",
        "Lo! Foods",
        {
            "handle": "lo-foods-protein-chef-baked-bikaneri-bhujia",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Protein Chef Baked Bikaneri Bhujia",
            "url": "https://lofoods.fit/products/baked-bhujia-authentic-bikaneri-flavor",
            "image_url": uploaded_urls["lo-foods-protein-chef-baked-bikaneri-bhujia"],
            "variants": [{"id": 1, "title": "100g Pack", "price": 139.0, "mrp": 149.0, "compare_at_price": 149.0, "net_weight_g": 100.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-protein-chef-baked-bikaneri-bhujia"]}],
        },
        {
            "v": 0,
            "name": "Protein Chef Baked Bikaneri Bhujia",
            "variant": "100g Pack",
            "net": 100.0,
            "serv": 30.0,
            "label": "1 serving (30g)",
            "n": [126.0, 6.5, 11.5, 6.0, 1.0, 0.0, 0.0, 3.5, 0.8, 0.0, 195.0],
            "ing": "Moth Dal Flour, Besan (Chickpea Flour), Defatted Soya Flour, High Oleic Sunflower Oil, Bikaneri Spices, Black Salt, Clove, Cinnamon",
            "allergens": ["Soy"],
            "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
            "desc": "100% baked (not fried) authentic Bikaneri bhujia crafted with moth dal, besan, and soy protein with zero palm oil.",
            "protein_source": "Chickpea, Moth Dal & Soy Protein",
            "protein_tier": "tier_3",
        },
    ),
    450: (
        "manual",
        "lo-foods-keto-south-indian-mixture-low-carb",
        "savory-snacks",
        "Lo! Foods",
        {
            "handle": "lo-foods-keto-south-indian-mixture-low-carb",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Keto South Indian Mixture (Low Carb)",
            "url": "https://lofoods.fit/products/keto-snack-south-indian-mixture-low-carb",
            "image_url": uploaded_urls["lo-foods-keto-south-indian-mixture-low-carb"],
            "variants": [{"id": 1, "title": "130g Pack", "price": 189.0, "mrp": 199.0, "compare_at_price": 199.0, "net_weight_g": 130.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-keto-south-indian-mixture-low-carb"]}],
        },
        {
            "v": 0,
            "name": "Keto South Indian Mixture (Low Carb)",
            "variant": "130g Pack",
            "net": 130.0,
            "serv": 30.0,
            "label": "1 serving (30g)",
            "n": [138.0, 7.5, 6.0, 9.5, 1.4, 0.0, 0.0, 4.0, 0.5, 0.0, 180.0],
            "ing": "Roasted Peanuts, Chickpea Flour, Isolated Soy Protein,Sunflower Seeds, Flax Seeds, Curry Leaves, Red Chilli, Rock Salt",
            "allergens": ["Peanuts", "Soy"],
            "tags": ["Vegetarian", "Vegan", "Keto-Friendly", "Low-Carb", "No Added Sugar"],
            "desc": "Low-carb keto South Indian savory mixture made with superfood seeds, roasted peanuts, and plant protein (only 2g net carbs per serving).",
            "protein_source": "Soy & Peanut Protein",
            "protein_tier": "tier_3",
        },
    ),
    451: (
        "manual",
        "eat-better-co-better-seed-mix-spiced-jaggery-nut-free",
        "savory-snacks",
        "Eat Better Co",
        {
            "handle": "eat-better-co-better-seed-mix-spiced-jaggery-nut-free",
            "store": "manual",
            "brand": "Eat Better Co",
            "title": "Eat Better Co Better Seed Mix Spiced Jaggery (Nut-Free)",
            "url": "https://eatbetterco.com/products/better-seed-mix-spiced-jaggery-100g",
            "image_url": uploaded_urls["eat-better-co-better-seed-mix-spiced-jaggery-nut-free"],
            "variants": [{"id": 1, "title": "100g Pouch", "price": 89.0, "mrp": 99.0, "compare_at_price": 99.0, "net_weight_g": 100.0, "in_stock": True, "image_url": uploaded_urls["eat-better-co-better-seed-mix-spiced-jaggery-nut-free"]}],
        },
        {
            "v": 0,
            "name": "Better Seed Mix Spiced Jaggery (Nut-Free)",
            "variant": "100g Pouch",
            "net": 100.0,
            "serv": 30.0,
            "label": "1 serving (30g)",
            "n": [163.0, 7.2, 8.5, 11.2, 1.8, 0.0, 0.0, 3.2, 3.0, 2.5, 45.0],
            "ing": "Pumpkin Seeds, Watermelon Seeds, Sunflower Seeds, Flax Seeds, Sesame Seeds, Jaggery, Dry Ginger Powder, Black Pepper",
            "allergens": ["Sesame"],
            "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Nut-Free", "Jain"],
            "desc": "Crunchy 5-seed roasted mix (pumpkin, watermelon, sunflower, flax, sesame) lightly glazed with spiced jaggery and dry ginger.",
            "protein_source": "Pumpkin, Watermelon & Sunflower Seeds",
            "protein_tier": "tier_3",
        },
    ),
    535: (
        "manual",
        "open-secret-special-choco-almond-nutty-brownie",
        "cookies-baked",
        "Open Secret",
        {
            "handle": "open-secret-special-choco-almond-nutty-brownie",
            "store": "manual",
            "brand": "Open Secret",
            "title": "Open Secret Special Choco Almond Nutty Brownie",
            "url": "https://opensecret.in/products/choco-almond-brownie-pack-of-4",
            "image_url": uploaded_urls["open-secret-special-choco-almond-nutty-brownie"],
            "variants": [{"id": 1, "title": "Pack of 4 (160g)", "price": 199.0, "mrp": 220.0, "compare_at_price": 220.0, "net_weight_g": 160.0, "in_stock": True, "image_url": uploaded_urls["open-secret-special-choco-almond-nutty-brownie"]}],
        },
        {
            "v": 0,
            "name": "Special Choco Almond Nutty Brownie",
            "variant": "Pack of 4 (160g)",
            "net": 160.0,
            "serv": 40.0,
            "label": "1 brownie (40g)",
            "n": [182.0, 5.2, 20.0, 9.0, 3.2, 0.0, 0.0, 3.0, 8.0, 0.0, 55.0],
            "ing": "Roasted Almonds, Cashews, Dark Cocoa Mass, Whey Protein Concentrate, Rolled Oats, Honey, Prebiotic Dietary Fiber",
            "allergens": ["Milk", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "No Maida", "No Palm Oil"],
            "desc": "Un-junked fudgy choco almond nutty brownie baked with roasted almonds, dark cocoa, and whey protein with zero maida and zero palm oil.",
            "protein_source": "Almonds & Whey Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    536: (
        "manual",
        "max-protein-7-grain-protein-cookie-coconut-delite",
        "cookies-baked",
        "Max Protein",
        {
            "handle": "max-protein-7-grain-protein-cookie-coconut-delite",
            "store": "manual",
            "brand": "Max Protein",
            "title": "Max Protein 7 Grain Protein Cookie Coconut Delite",
            "url": "https://maxprotein.in/products/max-protein-coconut-delite-cookie-pack-of-6",
            "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-coconut-delite"],
            "variants": [{"id": 1, "title": "Pack of 6 (330g)", "price": 299.0, "mrp": 360.0, "compare_at_price": 360.0, "net_weight_g": 330.0, "in_stock": True, "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-coconut-delite"]}],
        },
        {
            "v": 0,
            "name": "7 Grain Protein Cookie Coconut Delite",
            "variant": "Pack of 6 (330g)",
            "net": 330.0,
            "serv": 55.0,
            "label": "1 cookie (55g)",
            "n": [238.0, 10.0, 26.0, 10.5, 4.5, 0.0, 0.0, 4.0, 6.5, 0.0, 115.0],
            "ing": "7 Grain Blend (Oats, Ragi, Quinoa, Amaranth, Soya, Wheat, Chickpea), Whey Protein Concentrate, Desiccated Coconut, Almonds, Maltitol",
            "allergens": ["Milk", "Soy", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "High-Fibre", "No Added Sugar"],
            "desc": "Soft-baked 7-grain breakfast protein cookie with real desiccated coconut, packing 10g protein and 4g fiber per 55g cookie.",
            "protein_source": "Whey, Soy & 7-Grain Blend",
            "protein_tier": "tier_2",
        },
    ),
    538: (
        "manual",
        "max-protein-7-grain-protein-cookie-choco-coconut",
        "cookies-baked",
        "Max Protein",
        {
            "handle": "max-protein-7-grain-protein-cookie-choco-coconut",
            "store": "manual",
            "brand": "Max Protein",
            "title": "Max Protein 7 Grain Protein Cookie Choco Coconut",
            "url": "https://maxprotein.in/products/max-protein-choco-coconut-cookie-pack-of-6",
            "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-choco-coconut"],
            "variants": [{"id": 1, "title": "Pack of 6 (330g)", "price": 299.0, "mrp": 360.0, "compare_at_price": 360.0, "net_weight_g": 330.0, "in_stock": True, "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-choco-coconut"]}],
        },
        {
            "v": 0,
            "name": "7 Grain Protein Cookie Choco Coconut",
            "variant": "Pack of 6 (330g)",
            "net": 330.0,
            "serv": 55.0,
            "label": "1 cookie (55g)",
            "n": [242.0, 10.0, 26.5, 10.8, 4.8, 0.0, 0.0, 4.2, 6.8, 0.0, 120.0],
            "ing": "7 Grain Blend (Oats, Ragi, Quinoa, Amaranth, Soya, Wheat, Chickpea), Whey Protein Concentrate, Dark Choco Chips, Desiccated Coconut, Cocoa Solids",
            "allergens": ["Milk", "Soy", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "High-Fibre", "No Added Sugar"],
            "desc": "Rich chocolate and toasted coconut 7-grain breakfast cookie delivering 10g protein and 4.2g dietary fiber per cookie.",
            "protein_source": "Whey, Soy & 7-Grain Blend",
            "protein_tier": "tier_2",
        },
    ),
    539: (
        "manual",
        "max-protein-7-grain-protein-cookie-trail-mix",
        "cookies-baked",
        "Max Protein",
        {
            "handle": "max-protein-7-grain-protein-cookie-trail-mix",
            "store": "manual",
            "brand": "Max Protein",
            "title": "Max Protein 7 Grain Protein Cookie Trail Mix",
            "url": "https://maxprotein.in/products/max-protein-trail-mix-cookie",
            "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-trail-mix"],
            "variants": [{"id": 1, "title": "55g Cookie", "price": 55.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 55.0, "in_stock": True, "image_url": uploaded_urls["max-protein-7-grain-protein-cookie-trail-mix"]}],
        },
        {
            "v": 0,
            "name": "7 Grain Protein Cookie Trail Mix",
            "variant": "55g Cookie",
            "net": 55.0,
            "serv": 55.0,
            "label": "1 cookie (55g)",
            "n": [235.0, 10.0, 25.5, 10.2, 3.5, 0.0, 0.0, 4.5, 6.5, 0.0, 110.0],
            "ing": "7 Grain Blend (Oats, Ragi, Quinoa, Amaranth, Soya, Wheat, Chickpea), Whey Protein Concentrate, Cashews, Almonds, Cranberries, Black Raisins, Pumpkin Seeds",
            "allergens": ["Milk", "Soy", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "High-Fibre"],
            "desc": "Loaded trail mix 7-grain breakfast protein cookie studded with cashews, almonds, cranberries, raisins, and pumpkin seeds for 10g protein.",
            "protein_source": "Whey, Soy & 7-Grain Blend",
            "protein_tier": "tier_2",
        },
    ),
    540: (
        "manual",
        "max-protein-berry-bliss-crunchy-protein-cookies",
        "cookies-baked",
        "Max Protein",
        {
            "handle": "max-protein-berry-bliss-crunchy-protein-cookies",
            "store": "manual",
            "brand": "Max Protein",
            "title": "Max Protein Berry Bliss Crunchy Protein Cookies",
            "url": "https://maxprotein.in/products/berry-bliss-crunchy-cookies",
            "image_url": uploaded_urls["max-protein-berry-bliss-crunchy-protein-cookies"],
            "variants": [{"id": 1, "title": "60g Pack", "price": 55.0, "mrp": 60.0, "compare_at_price": 60.0, "net_weight_g": 60.0, "in_stock": True, "image_url": uploaded_urls["max-protein-berry-bliss-crunchy-protein-cookies"]}],
        },
        {
            "v": 0,
            "name": "Berry Bliss Crunchy Protein Cookies",
            "variant": "60g Pack",
            "net": 60.0,
            "serv": 60.0,
            "label": "1 pack (60g)",
            "n": [256.0, 10.0, 30.0, 10.5, 4.2, 0.0, 0.0, 4.0, 5.0, 0.0, 125.0],
            "ing": "Whole Wheat Flour, Milk Protein Concentrate, Soy Protein Isolate, Dried Blueberries, Cranberries, Rolled Oats, Maltitol",
            "allergens": ["Milk", "Soy", "Gluten"],
            "tags": ["Vegetarian", "No Added Sugar", "High-Fibre"],
            "desc": "Crunchy bite-sized berry protein cookies made with real dried blueberries and cranberries, delivering 10g protein per 60g pack.",
            "protein_source": "Milk & Soy Protein",
            "protein_tier": "tier_2",
        },
    ),
    544: (
        "manual",
        "lo-foods-gluten-free-ragi-oat-cookies",
        "cookies-baked",
        "Lo! Foods",
        {
            "handle": "lo-foods-gluten-free-ragi-oat-cookies",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Gluten Free Ragi Oat Cookies",
            "url": "https://lofoods.fit/products/gluten-free-raagi-cookies",
            "image_url": uploaded_urls["lo-foods-gluten-free-ragi-oat-cookies"],
            "variants": [{"id": 1, "title": "150g Box", "price": 179.0, "mrp": 199.0, "compare_at_price": 199.0, "net_weight_g": 150.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-gluten-free-ragi-oat-cookies"]}],
        },
        {
            "v": 0,
            "name": "Gluten Free Ragi Oat Cookies",
            "variant": "150g Box",
            "net": 150.0,
            "serv": 30.0,
            "label": "2 cookies (30g)",
            "n": [134.0, 4.5, 13.0, 7.0, 3.2, 0.0, 8.0, 3.2, 0.5, 0.0, 60.0],
            "ing": "Sprouted Ragi Flour, Gluten-Free Rolled Oats, Chickpea Protein, Almond Flour, Cardamom (Elaichi), Butter, Erythritol",
            "allergens": ["Milk", "Tree Nuts"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "High-Fibre"],
            "desc": "Gluten-free ragi and oat cookies flavored with aromatic cardamom (elaichi), baked with zero maida, zero palm oil, and no added sugar.",
            "protein_source": "Ragi, Oats & Almond",
            "protein_tier": "tier_3",
        },
    ),
    545: (
        "manual",
        "lo-foods-gluten-free-butter-millet-cookies",
        "cookies-baked",
        "Lo! Foods",
        {
            "handle": "lo-foods-gluten-free-butter-millet-cookies",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Gluten Free Butter Millet Cookies",
            "url": "https://lofoods.fit/products/gluten-free-butter-millet-cookies",
            "image_url": uploaded_urls["lo-foods-gluten-free-butter-millet-cookies"],
            "variants": [{"id": 1, "title": "150g Box", "price": 179.0, "mrp": 199.0, "compare_at_price": 199.0, "net_weight_g": 150.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-gluten-free-butter-millet-cookies"]}],
        },
        {
            "v": 0,
            "name": "Gluten Free Butter Millet Cookies",
            "variant": "150g Box",
            "net": 150.0,
            "serv": 30.0,
            "label": "2 cookies (30g)",
            "n": [140.0, 4.2, 14.5, 7.2, 3.8, 0.0, 10.0, 2.8, 4.0, 3.5, 65.0],
            "ing": "Jowar (Sorghum) Flour, Desiccated Coconut, Chickpea Flour, Pure Cow Butter, Organic Jaggery, Milk Solids",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "No Maida", "No Palm Oil"],
            "desc": "Traditional butter millet cookies crafted with jowar, coconut, and jaggery with zero maida and zero palm oil.",
            "protein_source": "Jowar & Chickpea Flour",
            "protein_tier": "tier_3",
        },
    ),
    546: (
        "manual",
        "lo-foods-gluten-free-cashew-pistachio-millet-cookies",
        "cookies-baked",
        "Lo! Foods",
        {
            "handle": "lo-foods-gluten-free-cashew-pistachio-millet-cookies",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Gluten Free Cashew Pistachio Millet Cookies",
            "url": "https://lofoods.fit/products/gluten-free-pista-cookies",
            "image_url": uploaded_urls["lo-foods-gluten-free-cashew-pistachio-millet-cookies"],
            "variants": [{"id": 1, "title": "150g Box", "price": 189.0, "mrp": 199.0, "compare_at_price": 199.0, "net_weight_g": 150.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-gluten-free-cashew-pistachio-millet-cookies"]}],
        },
        {
            "v": 0,
            "name": "Gluten Free Cashew Pistachio Millet Cookies",
            "variant": "150g Box",
            "net": 150.0,
            "serv": 30.0,
            "label": "2 cookies (30g)",
            "n": [143.0, 5.0, 12.5, 8.2, 3.5, 0.0, 8.0, 3.0, 0.5, 0.0, 60.0],
            "ing": "Jowar Flour, Roasted Cashews, Pistachios, Almond Flour, Chickpea Protein, Butter, Erythritol",
            "allergens": ["Milk", "Tree Nuts"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Gluten-free millet cookies studded with roasted cashews and pistachios, sweetened naturally without added sugar or maida.",
            "protein_source": "Cashews, Pistachios & Jowar",
            "protein_tier": "tier_3",
        },
    ),
    547: (
        "manual",
        "lo-foods-protein-chef-high-protein-no-maida-rusk",
        "cookies-baked",
        "Lo! Foods",
        {
            "handle": "lo-foods-protein-chef-high-protein-no-maida-rusk",
            "store": "manual",
            "brand": "Lo! Foods",
            "title": "Lo! Foods Protein Chef High Protein No Maida Rusk",
            "url": "https://lofoods.fit/products/zero-maida-high-protein-wheat-rusk",
            "image_url": uploaded_urls["lo-foods-protein-chef-high-protein-no-maida-rusk"],
            "variants": [{"id": 1, "title": "200g Pack", "price": 139.0, "mrp": 149.0, "compare_at_price": 149.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["lo-foods-protein-chef-high-protein-no-maida-rusk"]}],
        },
        {
            "v": 0,
            "name": "Protein Chef High Protein No Maida Rusk",
            "variant": "200g Pack",
            "net": 200.0,
            "serv": 40.0,
            "label": "3 rusks (40g)",
            "n": [158.0, 6.0, 22.0, 5.2, 1.5, 0.0, 0.0, 3.5, 4.0, 3.0, 95.0],
            "ing": "MP Sharbati Whole Wheat Flour, Vital Wheat Gluten, Soy Protein Isolate, High Oleic Sunflower Oil, Cardamom (Elaichi), Yeast",
            "allergens": ["Gluten", "Soy"],
            "tags": ["Vegetarian", "No Maida", "No Palm Oil", "High-Fibre"],
            "desc": "Crunchy double-baked elaichi toast rusk made from 100% MP Sharbati whole wheat and plant protein (20g protein per pack, zero maida, zero palm oil).",
            "protein_source": "Whole Wheat & Soy Protein",
            "protein_tier": "tier_3",
        },
    ),
    548: (
        "manual",
        "open-secret-white-choco-cashew-nutty-cookies",
        "cookies-baked",
        "Open Secret",
        {
            "handle": "open-secret-white-choco-cashew-nutty-cookies",
            "store": "manual",
            "brand": "Open Secret",
            "title": "Open Secret White Choco Cashew Nutty Cookies",
            "url": "https://opensecret.in/products/white-choco-cashew-story-box-x6-cookies",
            "image_url": uploaded_urls["open-secret-white-choco-cashew-nutty-cookies"],
            "variants": [{"id": 1, "title": "Box of 5 (125g)", "price": 149.0, "mrp": 150.0, "compare_at_price": 150.0, "net_weight_g": 125.0, "in_stock": True, "image_url": uploaded_urls["open-secret-white-choco-cashew-nutty-cookies"]}],
        },
        {
            "v": 0,
            "name": "White Choco Cashew Nutty Cookies",
            "variant": "Box of 5 (125g)",
            "net": 125.0,
            "serv": 25.0,
            "label": "1 cookie (25g)",
            "n": [126.0, 3.8, 11.5, 7.2, 2.5, 0.0, 5.0, 2.0, 4.5, 3.0, 45.0],
            "ing": "Roasted Cashews (42%), Rolled Oats, Whey Protein Concentrate, White Chocolate Chips, Butter, Prebiotic Dietary Fiber",
            "allergens": ["Milk", "Tree Nuts", "Gluten"],
            "tags": ["Vegetarian", "No Maida", "No Palm Oil"],
            "desc": "Gourmet nutty cookies loaded with over 40% roasted cashews, white chocolate chips, oats, and whey protein with zero maida.",
            "protein_source": "Cashews & Whey Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    551: (
        "manual",
        "raw-pressery-high-protein-milkshake-chocolate-mint",
        "rtd-drinks",
        "Raw Pressery",
        {
            "handle": "raw-pressery-high-protein-milkshake-chocolate-mint",
            "store": "manual",
            "brand": "Raw Pressery",
            "title": "Raw Pressery High Protein Milkshake Chocolate Mint",
            "url": "https://www.rawpressery.com/products/chocolate-mint",
            "image_url": uploaded_urls["raw-pressery-high-protein-milkshake-chocolate-mint"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 100.0, "mrp": 100.0, "compare_at_price": 100.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["raw-pressery-high-protein-milkshake-chocolate-mint"]}],
        },
        {
            "v": 0,
            "name": "High Protein Milkshake Chocolate Mint",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [134.0, 18.0, 12.0, 1.5, 1.0, 0.0, 12.0, 1.2, 8.5, 0.0, 110.0],
            "ing": "Skimmed Milk, Milk Protein Concentrate, Alkalized Cocoa Powder, Natural Peppermint Extract, Stevia, Lactase Enzyme",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar"],
            "desc": "Refreshing chocolate and mint ready-to-drink milkshake delivering 18g clean milk protein and 40% daily calcium with no added sugar.",
            "protein_source": "Skimmed Milk & Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    552: (
        "manual",
        "raw-pressery-high-protein-milkshake-banana-honey",
        "rtd-drinks",
        "Raw Pressery",
        {
            "handle": "raw-pressery-high-protein-milkshake-banana-honey",
            "store": "manual",
            "brand": "Raw Pressery",
            "title": "Raw Pressery High Protein Milkshake Banana Honey",
            "url": "https://www.rawpressery.com/products/banana-honey",
            "image_url": uploaded_urls["raw-pressery-high-protein-milkshake-banana-honey"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 100.0, "mrp": 100.0, "compare_at_price": 100.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["raw-pressery-high-protein-milkshake-banana-honey"]}],
        },
        {
            "v": 0,
            "name": "High Protein Milkshake Banana Honey",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [138.0, 18.0, 13.0, 1.5, 1.0, 0.0, 12.0, 1.5, 9.5, 0.0, 105.0],
            "ing": "Skimmed Milk, Milk Protein Concentrate, Banana Puree, Natural Honey, Prebiotic Fiber (Inulin), Stevia, Lactase Enzyme",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar"],
            "desc": "Creamy banana and honey protein milkshake packing 18g milk protein, prebiotic fiber, and 30% RDA calcium with no added refined sugar.",
            "protein_source": "Skimmed Milk & Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    553: (
        "manual",
        "phab-high-protein-milkshake-strawberries-cream",
        "rtd-drinks",
        "Phab",
        {
            "handle": "phab-high-protein-milkshake-strawberries-cream",
            "store": "manual",
            "brand": "Phab",
            "title": "Phab High Protein Milkshake Strawberries & Cream",
            "url": "https://www.getphab.com/products/cold-coffee-18g-protein-milkshake-copy",
            "image_url": uploaded_urls["phab-high-protein-milkshake-strawberries-cream"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 125.0, "mrp": 125.0, "compare_at_price": 125.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["phab-high-protein-milkshake-strawberries-cream"]}],
        },
        {
            "v": 0,
            "name": "High Protein Milkshake Strawberries & Cream",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [144.0, 18.0, 13.5, 2.0, 1.2, 0.0, 10.0, 1.5, 8.5, 0.0, 110.0],
            "ing": "Double Toned Milk, Milk Protein Concentrate, Strawberry Puree, Stabilizer (INS 407), Sweetener (Sucralose), Vitamins A & D",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Velvety strawberries and cream ready-to-drink protein shake delivering 18g complete milk protein with zero trans fat and zero added sugar.",
            "protein_source": "Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    554: (
        "manual",
        "phab-high-protein-milkshake-mango-magic",
        "rtd-drinks",
        "Phab",
        {
            "handle": "phab-high-protein-milkshake-mango-magic",
            "store": "manual",
            "brand": "Phab",
            "title": "Phab High Protein Milkshake Mango Magic",
            "url": "https://www.getphab.com/products/vanilla-almond-18g-protein-milkshake-copy",
            "image_url": uploaded_urls["phab-high-protein-milkshake-mango-magic"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 125.0, "mrp": 125.0, "compare_at_price": 125.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["phab-high-protein-milkshake-mango-magic"]}],
        },
        {
            "v": 0,
            "name": "High Protein Milkshake Mango Magic",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [146.0, 18.0, 14.0, 2.0, 1.2, 0.0, 10.0, 1.5, 9.0, 0.0, 110.0],
            "ing": "Double Toned Milk, Milk Protein Concentrate, Alphonso Mango Pulp, Prebiotic Fiber, Sweetener (Sucralose), Vitamins & Minerals",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Alphonso mango high-protein milkshake packing 18g milk protein per 200ml bottle with zero added sugar.",
            "protein_source": "Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    555: (
        "manual",
        "phab-protein-milkshake-coffee-tiramisu",
        "rtd-drinks",
        "Phab",
        {
            "handle": "phab-protein-milkshake-coffee-tiramisu",
            "store": "manual",
            "brand": "Phab",
            "title": "Phab Protein Milkshake Coffee Tiramisu",
            "url": "https://www.getphab.com/products/phab-10g-protein-milkshake-coffee-tiramisu-copy",
            "image_url": uploaded_urls["phab-protein-milkshake-coffee-tiramisu"],
            "variants": [{"id": 1, "title": "200ml Bottle", "price": 85.0, "mrp": 85.0, "compare_at_price": 85.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["phab-protein-milkshake-coffee-tiramisu"]}],
        },
        {
            "v": 0,
            "name": "Protein Milkshake Coffee Tiramisu",
            "variant": "200ml Bottle",
            "net": 200.0,
            "serv": 200.0,
            "label": "1 bottle (200ml)",
            "n": [118.0, 10.0, 15.0, 2.0, 1.2, 0.0, 8.0, 1.2, 8.5, 0.0, 95.0],
            "ing": "Toned Milk, Skimmed Milk Powder, Milk Protein Concentrate, Coffee Extract, Cocoa Solids, Natural Tiramisu Flavor, Stevia",
            "allergens": ["Milk"],
            "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
            "desc": "Everyday 10g protein coffee tiramisu milkshake crafted with real coffee extract, cocoa, and zero artificial sweeteners.",
            "protein_source": "Milk Protein Concentrate",
            "protein_tier": "tier_2",
        },
    ),
    556: (
        "manual",
        "farmley-roasted-foxnuts-tangy-tomato",
        "savory-snacks",
        "Farmley",
        {
            "handle": "farmley-roasted-foxnuts-tangy-tomato",
            "store": "manual",
            "brand": "Farmley",
            "title": "Farmley High Protein Roasted Makhana Tangy Tomato",
            "url": "https://www.farmley.com/products/tangy-tomato-pack-of-4-77g",
            "image_url": uploaded_urls["farmley-high-protein-roasted-makhana-tangy-tomato"],
            "variants": [{"id": 1, "title": "77g Jar", "price": 125.0, "mrp": 149.0, "compare_at_price": 149.0, "net_weight_g": 77.0, "in_stock": True, "image_url": uploaded_urls["farmley-high-protein-roasted-makhana-tangy-tomato"]}],
        },
        None,  # Keep existing verified reading for 556
    ),
    557: (
        "manual",
        "farmley-roasted-foxnuts-peri-peri",
        "savory-snacks",
        "Farmley",
        {
            "handle": "farmley-roasted-foxnuts-peri-peri",
            "store": "manual",
            "brand": "Farmley",
            "title": "Farmley High Protein Roasted Makhana Peri Peri",
            "url": "https://www.farmley.com/products/peri-peri-makhana-pack-of-4",
            "image_url": uploaded_urls["farmley-high-protein-roasted-makhana-peri-peri"],
            "variants": [{"id": 1, "title": "77g Jar", "price": 125.0, "mrp": 149.0, "compare_at_price": 149.0, "net_weight_g": 77.0, "in_stock": True, "image_url": uploaded_urls["farmley-high-protein-roasted-makhana-peri-peri"]}],
        },
        None,  # Keep existing verified reading for 557
    ),
    558: (
        "manual",
        "farmley-5-in-1-protein-rich-seed-mix",
        "savory-snacks",
        "Farmley",
        {
            "handle": "farmley-5-in-1-protein-rich-seed-mix",
            "store": "manual",
            "brand": "Farmley",
            "title": "Farmley 5-in-1 Protein Rich Seed Mix",
            "url": "https://www.farmley.com/products/5-in-1-protein-rich-seed-mix-jar",
            "image_url": uploaded_urls["farmley-5-in-1-protein-rich-seed-mix"],
            "variants": [{"id": 1, "title": "200g Pouch", "price": 199.0, "mrp": 249.0, "compare_at_price": 249.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["farmley-5-in-1-protein-rich-seed-mix"]}],
        },
        {
            "v": 0,
            "name": "5-in-1 Protein Rich Seed Mix",
            "variant": "200g Pouch",
            "net": 200.0,
            "serv": 30.0,
            "label": "1 serving (30g)",
            "n": [168.0, 7.5, 6.0, 12.6, 1.8, 0.0, 0.0, 3.6, 0.6, 0.0, 15.0],
            "ing": "Pumpkin Seeds, Watermelon Seeds, Sunflower Seeds, Flax Seeds, Chia Seeds",
            "allergens": [],
            "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Clean-Label", "No Added Sugar", "Nut-Free"],
            "desc": "Power-up 5-in-1 roasted superseed mix combining pumpkin, watermelon, sunflower, flax, and chia seeds for natural plant protein and omega-3s.",
            "protein_source": "Pumpkin, Watermelon, Sunflower, Flax & Chia Seeds",
            "protein_tier": "tier_3",
        },
    ),
    559: (
        "manual",
        "farmley-high-protein-roasted-pumpkin-seeds",
        "savory-snacks",
        "Farmley",
        {
            "handle": "farmley-high-protein-roasted-pumpkin-seeds",
            "store": "manual",
            "brand": "Farmley",
            "title": "Farmley High Protein Roasted Pumpkin Seeds",
            "url": "https://www.farmley.com/products/pumpkin-seeds",
            "image_url": uploaded_urls["farmley-high-protein-roasted-pumpkin-seeds"],
            "variants": [{"id": 1, "title": "200g Pouch", "price": 239.0, "mrp": 299.0, "compare_at_price": 299.0, "net_weight_g": 200.0, "in_stock": True, "image_url": uploaded_urls["farmley-high-protein-roasted-pumpkin-seeds"]}],
        },
        {
            "v": 0,
            "name": "High Protein Roasted Pumpkin Seeds",
            "variant": "200g Pouch",
            "net": 200.0,
            "serv": 30.0,
            "label": "1 serving (30g)",
            "n": [171.0, 9.0, 4.5, 13.0, 2.2, 0.0, 0.0, 2.5, 0.4, 0.0, 10.0],
            "ing": "100% Premium AAA-Grade Green Pumpkin Seeds (Pepitas)",
            "allergens": [],
            "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Clean-Label", "No Added Sugar", "Keto-Friendly", "Nut-Free"],
            "desc": "100% natural, nutrient-dense green pumpkin seeds delivering 30g protein per 100g (9g per 30g serving) along with magnesium and zinc.",
            "protein_source": "Pumpkin Seed Protein",
            "protein_tier": "tier_3",
        },
    ),
}

# Read current picks.txt and readings.jsonl
picks_lines = [l for l in (HERE / "picks.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
readings_objs = [json.loads(l) for l in (HERE / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

assert len(picks_lines) == len(readings_objs), f"Mismatch: {len(picks_lines)} vs {len(readings_objs)}"

old_slugs_to_delete_from_supabase = set()
new_picks = []
new_readings = []

for old_idx in range(1, len(picks_lines) + 1):
    old_pick = picks_lines[old_idx - 1]
    old_r = readings_objs[old_idx - 1]
    assert old_r["i"] == old_idx, f"Line {old_idx} has r['i']={old_r['i']}"

    old_store, old_prefix, old_cat, old_brand = old_pick.split("|")
    old_name = old_r["name"]
    if old_name.lower().startswith(old_brand.lower() + " "):
        old_name = old_name[len(old_brand) + 1:]
    old_slug = slugify(f"{old_brand}-{old_name}")

    if old_idx in DUPLICATE_INDICES_TO_REMOVE:
        # Don't delete raw-pressery-high-protein-milkshake-cold-coffee from Supabase since line 412 keeps it!
        if old_slug != "raw-pressery-high-protein-milkshake-cold-coffee":
            old_slugs_to_delete_from_supabase.add(old_slug)
        continue

    if old_idx in BATCH1_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH1_RECORDS[old_idx]
        new_pick_line = f"{store}|{handle}|{cat}|{brand}"
        if r_override is not None:
            updated_r = dict(r_override)
            updated_r["i"] = len(new_picks) + 1
            new_name = updated_r["name"]
            if new_name.lower().startswith(brand.lower() + " "):
                new_name = new_name[len(brand) + 1:]
            new_slug = slugify(f"{brand}-{new_name}")
            if new_slug != old_slug:
                old_slugs_to_delete_from_supabase.add(old_slug)
        else:
            updated_r = dict(old_r)
            updated_r["i"] = len(new_picks) + 1
        new_picks.append(new_pick_line)
        new_readings.append(updated_r)
    else:
        updated_r = dict(old_r)
        updated_r["i"] = len(new_picks) + 1
        new_picks.append(old_pick)
        new_readings.append(updated_r)

# Write updated picks.txt and readings.jsonl
(HERE / "picks.txt").write_text("\n".join(new_picks) + "\n", encoding="utf-8")
(HERE / "readings.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in new_readings) + "\n", encoding="utf-8")
print(f"Updated picks.txt and readings.jsonl: {len(picks_lines)} -> {len(new_picks)} lines")

# Update manual_entries.jsonl (deduplicated by handle, keeping line 41 for raw-pressery and applying BATCH1_RECORDS)
manual_map = {}
for line in (HERE / "manual_entries.jsonl").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    obj = json.loads(line)
    h = obj["handle"]
    # Don't let the duplicate null-image Raw Pressery overwrite the first one with image_url
    if h in manual_map and manual_map[h].get("image_url") and not obj.get("image_url"):
        continue
    manual_map[h] = obj

for _, (_, handle, _, _, manual_obj, _) in BATCH1_RECORDS.items():
    manual_map[handle] = manual_obj

(HERE / "manual_entries.jsonl").write_text(
    "\n".join(json.dumps(v, ensure_ascii=False) for v in manual_map.values()) + "\n",
    encoding="utf-8"
)
print(f"Updated manual_entries.jsonl ({len(manual_map)} unique manual handles)")
print(f"Old duplicate/synthetic slugs to remove from seedCatalog.json & live Supabase: {sorted(old_slugs_to_delete_from_supabase)}")

# Remove old_slugs_to_delete_from_supabase from seedCatalog.json BEFORE running build_demo_catalog.py
# so build_demo_catalog.py's preservation loop doesn't preserve retired synthetic slugs!
seed_web_path = ROOT / "protein-web" / "src" / "data" / "seedCatalog.json"
existing_seed = json.loads(seed_web_path.read_text(encoding="utf-8"))
cleaned_seed = []
seen_slugs = set()
for item in existing_seed:
    s = item.get("slug")
    if s in old_slugs_to_delete_from_supabase:
        continue
    if s in seen_slugs:
        continue
    seen_slugs.add(s)
    cleaned_seed.append(item)
seed_web_path.write_text(json.dumps(cleaned_seed, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Pre-cleaned seedCatalog.json: {len(existing_seed)} -> {len(cleaned_seed)} items")

# Save old_slugs_to_delete_from_supabase for the Supabase sync step
(ROOT / "protein-etl" / "scratch" / "batch1_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8"
)

