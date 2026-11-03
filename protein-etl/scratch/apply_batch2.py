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

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch2_images"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# Format:
# idx -> dict with source_stem, cat, brand, name, url, variant, price, mrp, net, serv, label, n, ing, allergens, tags, desc, protein_source, protein_tier
BATCH2_SPEC = {
    378: {
        "source_stem": "bsn-syntha-6-protein-powder-chocolate-milkshake",
        "cat": "protein-powders",
        "brand": "BSN",
        "name": "Syntha-6 Ultra Premium Protein Matrix Chocolate Milkshake",
        "url": "https://www.optimumnutrition.co.in/products/bsn-syntha-6-protein-powder-5-lbs-2-27-kg-chocolate-milkshake-ultra-premium-protein-matrix-whey-protein-micellar-casein-for-muscle-recovery",
        "variant": "2.27kg (5 lb) Tub",
        "price": 6399.0,
        "mrp": 7499.0,
        "net": 2270.0,
        "serv": 44.0,
        "label": "1 scoop (44g)",
        "n": [190.0, 22.0, 13.0, 5.5, 2.0, 0.0, 55.0, 5.0, 2.0, 0.0, 190.0],
        "ing": "Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate, Calcium Caseinate, Micellar Casein, Milk Protein Isolate, Egg Albumin, Glutamine Peptides), Cocoa Powder, Polydextrose, Sunflower Creamer, Natural & Artificial Flavors, Sucralose, Acesulfame Potassium",
        "allergens": ["Milk", "Egg", "Soy", "Gluten"],
        "tags": ["Vegetarian", "High-Fibre"],
        "desc": "Ultra-premium sustained-release protein powder combining whey protein concentrate, whey isolate, and slow-digesting micellar casein for 22g protein and 10g EAAs per serving.",
        "protein_source": "Whey & Micellar Casein Matrix",
        "protein_tier": "tier_1",
    },
    380: {
        "source_stem": "isopure-low-carb-whey-protein-isolate-cookies-cream",
        "cat": "protein-powders",
        "brand": "Isopure",
        "name": "Low Carb 100% Whey Protein Isolate Cookies & Cream",
        "url": "https://www.optimumnutrition.co.in/products/isopure-whey-protein-isolate-powder-with-vitamins-for-immune-support-cookies-cream-1-kg-1141367",
        "variant": "1kg Tub",
        "price": 4319.0,
        "mrp": 4799.0,
        "net": 1000.0,
        "serv": 31.0,
        "label": "1 scoop (31g)",
        "n": [110.0, 25.0, 2.0, 0.5, 0.2, 0.0, 10.0, 0.5, 0.0, 0.0, 240.0],
        "ing": "100% Whey Protein Isolate, Vitamin and Mineral Blend (Vitamin C, Vitamin E, Zinc Oxide, Vitamin A, Vitamin D3), Cocoa Powder, Natural & Artificial Flavors, Xanthan Gum, Sucralose, Soy Lecithin",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar", "Keto-Friendly", "Low-Carb"],
        "desc": "100% pure micro-filtered whey protein isolate in Cookies & Cream flavor delivering 25g protein with zero added sugar, lactose-free, and fortified with immune-supporting vitamins C, E & Zinc.",
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
    },
    388: {
        "source_stem": "nakpro-womens-whey-protein-isolate-malai-kulfi",
        "cat": "protein-powders",
        "brand": "Nakpro",
        "name": "Women's Whey Protein Isolate with Biotin & Herbal Extracts Malai Kulfi",
        "url": "https://nakpro.com/products/nakpro-womens-whey-protein",
        "variant": "1kg Pouch",
        "price": 2999.0,
        "mrp": 4600.0,
        "net": 1000.0,
        "serv": 33.0,
        "label": "1 scoop (33g)",
        "n": [126.0, 24.8, 3.2, 1.4, 0.8, 0.0, 15.0, 0.8, 0.5, 0.0, 85.0],
        "ing": "Whey Protein Isolate, Whey Protein Concentrate, Shatavari Extract, Ashwagandha Extract, Flaxseed Powder, Biotin, Iron, Folic Acid, Calcium, Vitamin D3, Natural Malai Kulfi Flavor, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Specialized women's whey protein isolate formulated with 24.8g protein per serving alongside Shatavari, Ashwagandha, Biotin, Iron, and Folic Acid for lean muscle, skin, and hormonal wellness.",
        "protein_source": "Whey Protein Isolate & Concentrate",
        "protein_tier": "tier_1",
    },
    390: {
        "source_stem": "as-it-is-atom-plant-protein-complex-cafe-latte",
        "cat": "protein-powders",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Plant Protein Complex Cafe Latte",
        "url": "https://asitisnutrition.com/products/atom-plant-protein-complex-i-clinically-tested-whey-protein-equivalent-i-26g-protein-i-ashwagandha-infused-vegan-protein",
        "variant": "1kg Pouch",
        "price": 1415.0,
        "mrp": 2129.0,
        "net": 1000.0,
        "serv": 36.0,
        "label": "1 scoop (36g)",
        "n": [134.0, 26.0, 4.2, 1.5, 0.4, 0.0, 0.0, 1.8, 0.0, 0.0, 180.0],
        "ing": "Pea Protein Isolate, Brown Rice Protein Isolate, L-Leucine, L-Lysine, L-Valine, L-Isoleucine, Ashwagandha Root Extract (300mg), Coffee Powder, DigeZyme Multi-Enzyme Complex, Sucralose",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Lactose-Free", "No Added Sugar"],
        "desc": "Clinically tested whey-equivalent vegan protein blend combining pea and brown rice protein with 300mg Ashwagandha and DigeZyme enzymes for 26g complete plant protein per serving.",
        "protein_source": "Pea & Brown Rice Protein Isolate",
        "protein_tier": "tier_2",
    },
    391: {
        "source_stem": "as-it-is-atom-pea-protein-isolate-caramelized-banana",
        "cat": "protein-powders",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Pea Protein Isolate Caramelized Banana",
        "url": "https://asitisnutrition.com/products/as-it-is-nutrition-atom-pea-protein-29g-protein-peak-muscle-gains-fast-recovery-easy-digest-vegan-smooth-delicious-1kg",
        "variant": "1kg Pouch",
        "price": 1163.0,
        "mrp": 1750.0,
        "net": 1000.0,
        "serv": 36.0,
        "label": "1 scoop (36g)",
        "n": [138.0, 29.0, 2.5, 1.2, 0.3, 0.0, 0.0, 1.2, 0.0, 0.0, 210.0],
        "ing": "Pea Protein Isolate, Natural Caramelized Banana Flavor, DigeZyme Multi-Enzyme Complex (Amylase, Protease, Lactase, Lipase, Cellulase), Stabilizer (Xanthan Gum), Sucralose",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Lactose-Free", "No Added Sugar"],
        "desc": "High-potency vegan pea protein isolate delivering 29g plant protein and 5.1g BCAAs per serving with DigeZyme digestive enzymes in a smooth Caramelized Banana flavor.",
        "protein_source": "Pea Protein Isolate",
        "protein_tier": "tier_2",
    },
    392: {
        "source_stem": "cosmix-no-nonsense-plant-protein-mahabaleshwar-strawberry",
        "cat": "protein-powders",
        "brand": "CosMix",
        "name": "No-Nonsense Plant Protein Mahabaleshwar Strawberry",
        "url": "https://cosmix.in/products/no-nonsense-plant-protein-mahabaleshwar-strawberry",
        "variant": "500g Pouch",
        "price": 1085.0,
        "mrp": 1550.0,
        "net": 500.0,
        "serv": 36.0,
        "label": "1 heaped scoop (36g)",
        "n": [136.0, 24.0, 6.5, 1.6, 0.4, 0.0, 0.0, 2.2, 1.2, 0.0, 165.0],
        "ing": "Organic Pea Protein Isolate, Organic Brown Rice Protein, Freeze-Dried Mahabaleshwar Strawberry Powder, Beetroot Powder, Monk Fruit Extract, Gut-Friendly Herbal Blend (Ginger, Fennel, Cumin, Fenugreek)",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Clean-Label", "No Added Sugar", "Stevia-Free"],
        "desc": "Clean-label organic pea and brown rice protein flavored with real freeze-dried Mahabaleshwar strawberries and sweetened with monk fruit, delivering 24g plant protein per serving.",
        "protein_source": "Organic Pea & Brown Rice Protein",
        "protein_tier": "tier_2",
    },
    393: {
        "source_stem": "plantigo-plant-based-protein-powder-brazilian-chocolate",
        "cat": "protein-powders",
        "brand": "Plantigo",
        "name": "Plant-Based Protein Powder Brazilian Chocolate",
        "url": "https://plantigo.in/products/plant-based-vegan-protein-powder-for-muscle-gain",
        "variant": "1kg Tub",
        "price": 1299.0,
        "mrp": 3199.0,
        "net": 1000.0,
        "serv": 40.0,
        "label": "1 scoop (40g)",
        "n": [148.0, 24.0, 8.0, 2.2, 0.5, 0.0, 0.0, 5.0, 0.5, 0.0, 175.0],
        "ing": "Pea Protein Isolate, Brown Rice Protein, Flaxseed Powder, Pumpkin Seed Protein, Brazilian Alkalized Cocoa Powder, Tart Cherry Extract, Bromelain, Papain, Stevia",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "High-Fibre", "No Added Sugar"],
        "desc": "4-source vegan protein superblend (pea, brown rice, flaxseed, pumpkin seed) delivering 24g protein, 4.4g BCAAs, and 5g dietary fiber per serving in rich Brazilian Chocolate flavor.",
        "protein_source": "Pea, Brown Rice, Flax & Pumpkin Seed Protein",
        "protein_tier": "tier_2",
    },
    436: {
        "source_stem": "yogabar-dark-chocolate-cranberry-muesli",
        "cat": "breakfast-cereals",
        "brand": "Yoga Bar",
        "name": "Super Muesli Dark Chocolate & Cranberry",
        "url": "https://www.yogabars.in/products/dark-chocolate-cranberry-muesli-450g",
        "variant": "450g Box",
        "price": 299.0,
        "mrp": 445.0,
        "net": 450.0,
        "serv": 50.0,
        "label": "1 bowl (50g)",
        "n": [204.0, 9.0, 28.5, 6.2, 1.5, 0.0, 0.0, 5.2, 6.5, 4.0, 25.0],
        "ing": "Whole Grains (Rolled Oats, Brown Rice Flakes, Ragi Flakes, Quinoa), Dried Cranberries, Dark Chocolate Chunks, Almonds, Pumpkin Seeds, Chia Seeds, Flax Seeds, Cocoa Powder, Unrefined Cane Sugar",
        "allergens": ["Tree Nuts", "Soy", "Gluten"],
        "tags": ["Vegetarian", "High-Fibre", "Whole-Grain"],
        "desc": "83% wholegrains, super seeds, nuts, and dried cranberries tossed in rich dark chocolate, delivering 6.5g plant protein and 5.2g fiber per 50g bowl.",
        "protein_source": "Whole Grains, Almonds, Pumpkin & Chia Seeds",
        "protein_tier": "tier_3",
    },
    457: {
        "source_stem": "optimum-nutrition-gold-standard-100-whey-alphonso-mango",
        "cat": "protein-powders",
        "brand": "Optimum Nutrition",
        "name": "Gold Standard 100% Whey Alphonso Mango",
        "url": "https://www.optimumnutrition.co.in/products/6072921",
        "variant": "907g (2 lb) Tub",
        "price": 3099.0,
        "mrp": 3899.0,
        "net": 907.0,
        "serv": 30.0,
        "label": "1 scoop (30g)",
        "n": [117.0, 24.0, 3.0, 1.2, 0.7, 0.0, 35.0, 0.0, 1.0, 0.0, 75.0],
        "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Hydrolyzed Whey Peptides), Alphonso Mango Powder, Sunflower Lecithin, Citric Acid, Sucralose, Acesulfame Potassium",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Informed-Choice", "No Added Sugar"],
        "desc": "Limited-edition Indian Alphonso Mango flavor of Optimum Nutrition Gold Standard 100% Whey, with whey protein isolate as the primary source and 24g protein + 5.5g BCAAs per serving.",
        "protein_source": "Whey Protein Isolate & Concentrate",
        "protein_tier": "tier_1",
    },
    459: {
        "source_stem": "optimum-nutrition-gold-standard-100-whey-unflavoured",
        "cat": "protein-powders",
        "brand": "Optimum Nutrition",
        "name": "Gold Standard 100% Whey Unflavoured",
        "url": "https://www.optimumnutrition.co.in/products/unflavored-optimum-nutrition-on-gold-standard-100-whey-protein-powder-2-lb-907-g",
        "variant": "907g (2 lb) Tub",
        "price": 3099.0,
        "mrp": 3699.0,
        "net": 907.0,
        "serv": 29.0,
        "label": "1 scoop (29g)",
        "n": [113.0, 24.0, 2.0, 1.0, 0.6, 0.0, 30.0, 0.0, 1.0, 0.0, 50.0],
        "ing": "Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Hydrolyzed Whey Peptides), Emulsifier (Sunflower Lecithin)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Clean-Label", "Unflavoured", "No Artificial Sweeteners", "Informed-Choice"],
        "desc": "Unflavoured, unsweetened Optimum Nutrition Gold Standard 100% Whey with zero artificial flavors or sweeteners—ideal for shakes, smoothies, and high-protein recipes.",
        "protein_source": "Whey Protein Isolate & Concentrate",
        "protein_tier": "tier_1",
    },
    463: {
        "source_stem": "labrada-iso-100-whey-protein-isolate-chocolate",
        "cat": "protein-powders",
        "brand": "Labrada",
        "name": "ISO 100% Whey Protein Isolate Chocolate",
        "url": "https://www.labradanutrition.in/products/iso-whey",
        "variant": "2kg Tub",
        "price": 6999.0,
        "mrp": 8499.0,
        "net": 2000.0,
        "serv": 30.0,
        "label": "1 scoop (30g)",
        "n": [114.0, 25.0, 2.0, 0.5, 0.3, 0.0, 5.0, 0.5, 0.0, 0.0, 95.0],
        "ing": "Cross-Flow Micro-Filtered Whey Protein Isolate, Alkalized Cocoa Powder, Natural & Artificial Chocolate Flavors, Cellulose Gum, Sucralose, Acesulfame Potassium, Soy Lecithin",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar"],
        "desc": "100% cross-flow micro-filtered whey protein isolate delivering 25g fast-absorbing protein per 30g scoop with zero sugar and lactose-free digestion.",
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
    },
    464: {
        "source_stem": "labrada-100-whey-protein-chocolate",
        "cat": "protein-powders",
        "brand": "Labrada",
        "name": "100% Whey Protein Chocolate",
        "url": "https://www.labradanutrition.in/products/100-whey",
        "variant": "500g Tub",
        "price": 1599.0,
        "mrp": 2199.0,
        "net": 500.0,
        "serv": 35.0,
        "label": "1 scoop (35g)",
        "n": [138.0, 24.0, 4.5, 2.2, 1.2, 0.0, 45.0, 1.0, 1.5, 0.0, 110.0],
        "ing": "Instantized Whey Protein Concentrate, Cocoa Powder, Natural & Artificial Flavors, Xanthan Gum, Salt, Sucralose, Acesulfame Potassium",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Instantized 100% whey protein concentrate delivering 24g protein, 5.4g BCAAs, and 4g glutamine per serving in rich chocolate flavor.",
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    466: {
        "source_stem": "labrada-turbo-whey-protein-chocolate",
        "cat": "protein-powders",
        "brand": "Labrada",
        "name": "Turbo Whey Protein Isolate & Concentrate Chocolate",
        "url": "https://www.labradanutrition.in/products/turbo-whey",
        "variant": "1.8kg Tub",
        "price": 4699.0,
        "mrp": 5999.0,
        "net": 1800.0,
        "serv": 44.0,
        "label": "1 scoop (44g)",
        "n": [168.0, 30.0, 6.0, 2.5, 1.5, 0.0, 45.0, 1.0, 2.0, 0.0, 130.0],
        "ing": "Whey Protein Isolate, Whey Protein Concentrate, Creatine Monohydrate (3g), Cocoa Powder, L-Glutamine, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "High-potency performance whey blend combining whey isolate and whey concentrate with 30g protein and 3g creatine monohydrate per serving for strength and muscle recovery.",
        "protein_source": "Whey Protein Isolate & Concentrate",
        "protein_tier": "tier_1",
    },
    467: {
        "source_stem": "labrada-classic-whey-protein-powder-chocolate",
        "cat": "protein-powders",
        "brand": "Labrada",
        "name": "Classic Whey Protein Powder Chocolate",
        "url": "https://www.labradanutrition.in/products/labrada-classic-whey-protein-powder-1-8kg-chocolate-24g-protein-53-servings",
        "variant": "1.8kg Tub",
        "price": 4299.0,
        "mrp": 5499.0,
        "net": 1800.0,
        "serv": 34.0,
        "label": "1 scoop (34g)",
        "n": [132.0, 24.0, 4.0, 2.0, 1.1, 0.0, 40.0, 0.8, 1.5, 0.0, 105.0],
        "ing": "Ultrafiltered Whey Protein Concentrate, Alkalized Cocoa Powder, Digestive Enzymes (Papain, Bromelain), Stabilizer (INS 415), Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Everyday ultrafiltered whey protein concentrate providing 24g protein and 53 servings per 1.8kg tub with added digestive enzymes.",
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    468: {
        "source_stem": "yogabar-ultimate-whey-isolate-yeast-protein-chocolate",
        "cat": "protein-powders",
        "brand": "Yoga Bar",
        "name": "Ultimate Whey Isolate with Fermented Yeast Protein Chocolate",
        "url": "https://www.yogabars.in/products/ultimate-whey-isolate-with-fermented-yeast-protein-chocolate-500gm",
        "variant": "500g Pouch",
        "price": 1699.0,
        "mrp": 2099.0,
        "net": 500.0,
        "serv": 36.0,
        "label": "1 scoop (36g)",
        "n": [134.0, 28.0, 3.2, 1.0, 0.4, 0.0, 5.0, 1.5, 0.0, 0.0, 95.0],
        "ing": "Whey Protein Isolate, Bio-Fermented Yeast Protein Isolate, Cocoa Powder, Probiotic Blend (1 Billion CFU Bacillus Coagulans), Digestive Enzymes, Monk Fruit Extract",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Clean-Label", "No Added Sugar"],
        "desc": "Dual-action 1.0 PDCAAS protein combining fast-absorbing whey protein isolate with sustainable bio-fermented yeast protein, delivering 28g protein, 6.5g BCAAs, and 1B CFU probiotics.",
        "protein_source": "Whey Protein Isolate & Fermented Yeast Protein",
        "protein_tier": "tier_1",
    },
    469: {
        "source_stem": "wellbeing-nutrition-biofermented-yeast-protein-dark-chocolate",
        "cat": "protein-powders",
        "brand": "Wellbeing Nutrition",
        "name": "Biofermented Yeast Protein Isolate Dark Chocolate",
        "url": "https://wellbeingnutrition.com/products/yeast-protein-powder-dark-chocolate-500g",
        "variant": "500g Pouch",
        "price": 1614.0,
        "mrp": 1899.0,
        "net": 500.0,
        "serv": 34.0,
        "label": "1 scoop (34g)",
        "n": [128.0, 24.0, 4.0, 1.6, 0.5, 0.0, 0.0, 2.2, 0.0, 0.0, 115.0],
        "ing": "Bio-Fermented Saccharomyces Cerevisiae Yeast Protein Isolate, Dark Cocoa Powder, Prebiotic Fiber, 2 Billion CFU Probiotics, Digestive Enzymes (Protease, Bromelain, Papain), Monk Fruit",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Lactose-Free", "Clean-Label", "No Added Sugar"],
        "desc": "Next-generation vegan biofermented yeast protein isolate with a PDCAAS 1.0 score matching whey, delivering 24g protein, 11.8g EAAs, 2B CFU probiotics, and 3 digestive enzymes in Dark Chocolate flavor.",
        "protein_source": "Biofermented Yeast Protein Isolate",
        "protein_tier": "tier_1",
    },
    529: {
        "source_stem": "as-it-is-atom-whey-protein-isolate-mango-delight",
        "cat": "protein-powders",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Whey Protein Isolate Mango Delight",
        "url": "https://asitisnutrition.com/products/atomwheyproteinisolate",
        "variant": "1kg Pouch",
        "price": 4382.0,
        "mrp": 5859.0,
        "net": 1000.0,
        "serv": 34.0,
        "label": "1 scoop (34g)",
        "n": [126.0, 29.0, 1.5, 0.4, 0.2, 0.0, 5.0, 0.4, 0.0, 0.0, 85.0],
        "ing": "Cross-Flow Micro-Filtered Whey Protein Isolate, Alphonso Mango Powder, DigeZyme Multi-Enzyme Complex, Stabilizer (Xanthan Gum), Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Low-Carb", "No Added Sugar"],
        "desc": "Ultra-pure cross-flow micro-filtered whey protein isolate delivering 29g protein, 6.8g BCAAs, and 13.7g EAAs per 34g serving with DigeZyme enzymes.",
        "protein_source": "Whey Protein Isolate",
        "protein_tier": "tier_1",
    },
}

uploaded_urls = {}
BATCH2_RECORDS = {}

for idx, spec in BATCH2_SPEC.items():
    brand = spec["brand"]
    name = spec["name"]
    target_slug = slugify(f"{brand}-{name}")
    src_webp = IMG_DIR / f"{spec['source_stem']}.webp"
    assert src_webp.exists(), f"Missing {src_webp}"

    dest_filename = f"{target_slug}.webp"
    data = src_webp.read_bytes()
    sb.storage.from_("product-images").upload(
        path=dest_filename,
        file=data,
        file_options={"content-type": "image/webp", "upsert": "true"},
    )
    pub_url = f"{SUPABASE_URL}/storage/v1/object/public/product-images/{dest_filename}"
    uploaded_urls[target_slug] = pub_url
    print(f"[UPLOADED] {dest_filename} -> {pub_url}")

    manual_obj = {
        "handle": target_slug,
        "store": "manual",
        "brand": brand,
        "title": f"{brand} {name}",
        "url": spec["url"],
        "image_url": pub_url,
        "variants": [
            {
                "id": 1,
                "title": spec["variant"],
                "price": spec["price"],
                "mrp": spec["mrp"],
                "compare_at_price": spec["mrp"],
                "net_weight_g": spec["net"],
                "in_stock": True,
                "image_url": pub_url,
            }
        ],
    }
    reading_obj = {
        "v": 0,
        "name": name,
        "variant": spec["variant"],
        "net": spec["net"],
        "serv": spec["serv"],
        "label": spec["label"],
        "n": spec["n"],
        "ing": spec["ing"],
        "allergens": spec["allergens"],
        "tags": spec["tags"],
        "desc": spec["desc"],
        "protein_source": spec["protein_source"],
        "protein_tier": spec["protein_tier"],
    }
    BATCH2_RECORDS[idx] = ("manual", target_slug, spec["cat"], brand, manual_obj, reading_obj)

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

    if old_idx in BATCH2_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH2_RECORDS[old_idx]
        new_pick_line = f"{store}|{handle}|{cat}|{brand}"
        updated_r = dict(r_override)
        updated_r["i"] = len(new_picks) + 1
        if handle != old_slug:
            old_slugs_to_delete_from_supabase.add(old_slug)
        new_picks.append(new_pick_line)
        new_readings.append(updated_r)
    else:
        updated_r = dict(old_r)
        updated_r["i"] = len(new_picks) + 1
        new_picks.append(old_pick)
        new_readings.append(updated_r)

(HERE / "picks.txt").write_text("\n".join(new_picks) + "\n", encoding="utf-8")
(HERE / "readings.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in new_readings) + "\n", encoding="utf-8")
print(f"Updated picks.txt and readings.jsonl: {len(picks_lines)} -> {len(new_picks)} lines")

manual_map = {}
for line in (HERE / "manual_entries.jsonl").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    obj = json.loads(line)
    manual_map[obj["handle"]] = obj

for _, (_, handle, _, _, manual_obj, _) in BATCH2_RECORDS.items():
    manual_map[handle] = manual_obj

(HERE / "manual_entries.jsonl").write_text(
    "\n".join(json.dumps(v, ensure_ascii=False) for v in manual_map.values()) + "\n",
    encoding="utf-8",
)
print(f"Updated manual_entries.jsonl ({len(manual_map)} unique manual handles)")
print(f"Old slugs to remove from seedCatalog.json & live Supabase: {sorted(old_slugs_to_delete_from_supabase)}")

seed_web_path = ROOT / "protein-web" / "src" / "data" / "seedCatalog.json"
existing_seed = json.loads(seed_web_path.read_text(encoding="utf-8"))
cleaned_seed = [item for item in existing_seed if item.get("slug") not in old_slugs_to_delete_from_supabase]
seed_web_path.write_text(json.dumps(cleaned_seed, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Pre-cleaned seedCatalog.json: {len(existing_seed)} -> {len(cleaned_seed)} items")

(ROOT / "protein-etl" / "scratch" / "batch2_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8",
)
(ROOT / "protein-etl" / "scratch" / "batch2_active_slugs.json").write_text(
    json.dumps(sorted(uploaded_urls.keys()), indent=2),
    encoding="utf-8",
)
