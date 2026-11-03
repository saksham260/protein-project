import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))
from src.models import slugify

load_dotenv(ROOT / "protein-etl" / ".env")
load_dotenv(ROOT / "protein-web" / ".env.local")

SUPABASE_URL = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_KEY)

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch4_webp"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# 11-element nutrition array n:
# [calories, protein, carbs, fat, sat_fat, trans_fat, cholesterol, fiber, total_sugar, added_sugar, sodium]
BATCH4_SPEC = {
    325: {
        "source_stem": "epigamia-turbo-high-protein-milk",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Turbo High Protein Milk Zero Fat",
        "url": "https://epigamia.com/products/turbo-high-protein-milk-v-zfwandheri",
        "variant": "250ml Bottle",
        "price": 125.0,
        "mrp": 125.0,
        "net": 250.0,
        "serv": 250.0,
        "label": "1 bottle (250ml)",
        "n": [165.0, 25.0, 12.0, 0.5, 0.3, 0.0, 8.0, 0.0, 11.0, 0.0, 140.0],
        "ing": "Filtered Skimmed Cow Milk, Milk Protein Concentrate, Lactase Enzyme",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar"],
        "desc": "Zero-fat, lactose-free ultra-filtered high-protein dairy milk delivering 25g natural milk protein per 250ml bottle with zero added sugar.",
        "protein_source": "Ultra-Filtered Milk Protein",
        "protein_tier": "tier_1",
    },
    326: {
        "source_stem": "epigamia-lactose-free-artisanal-curd",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Artisanal Lactose Free Curd with Probiotics",
        "url": "https://epigamia.com/products/lactose-free-curd",
        "variant": "400g Tub",
        "price": 100.0,
        "mrp": 100.0,
        "net": 400.0,
        "serv": 100.0,
        "label": "100g serving",
        "n": [64.0, 4.2, 4.5, 3.2, 2.0, 0.0, 10.0, 0.0, 4.2, 0.0, 48.0],
        "ing": "Pasteurized Cow Milk, Milk Solids, Lactase Enzyme, Active Probiotic Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free", "No Added Sugar"],
        "desc": "Creamy artisanal lactose-free probiotic curd crafted from pasteurized cow milk with live gut-friendly cultures and zero preservatives.",
        "protein_source": "Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    404: {
        "source_stem": "epigamia-natural-greek-yogurt-tub-400g",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Greek Yogurt Natural Partly Skimmed Tub",
        "url": "https://epigamia.com/products/epigamia-natural-greek-yogurt-400gm-v-zfwmanikonda",
        "variant": "400g Tub",
        "price": 250.0,
        "mrp": 250.0,
        "net": 400.0,
        "serv": 100.0,
        "label": "100g serving",
        "n": [80.0, 8.5, 4.8, 3.0, 1.9, 0.0, 10.0, 0.0, 4.5, 0.0, 52.0],
        "ing": "Pasteurized Partly Skimmed Cow Milk, Milk Solids, Permitted Starter Cultures (S. Thermophilus, L. Bulgaricus)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Thick, strained natural Greek yogurt in a 400g multi-serve tub providing 8.5g complete dairy protein per 100g serving with no added sugar.",
        "protein_source": "Strained Dairy Yogurt Protein",
        "protein_tier": "tier_1",
    },
    405: {
        "source_stem": "epigamia-turbo-high-protein-paneer",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Turbo Soft & Creamy High Protein Paneer",
        "url": "https://epigamia.com/products/turbo-50g-protein-paneer-v-zfwandheri",
        "variant": "200g Pack",
        "price": 250.0,
        "mrp": 250.0,
        "net": 200.0,
        "serv": 100.0,
        "label": "100g serving",
        "n": [182.0, 25.0, 3.5, 7.5, 4.8, 0.0, 22.0, 0.0, 2.0, 0.0, 35.0],
        "ing": "Pasteurized Toned Cow Milk, Milk Solids, Citric Acid",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Soft and creamy high-protein paneer packing 25g complete dairy protein per 100g (50g per 200g pack) with reduced fat and zero preservatives.",
        "protein_source": "Milk Casein & Whey Protein",
        "protein_tier": "tier_1",
    },
    470: {
        "source_stem": "epigamia-turbo-high-protein-yogurt-alphonso-mango",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Turbo High Protein Greek Yogurt Alphonso Mango",
        "url": "https://epigamia.com/products/turbo-15g-protein-yogurt-mango-v-zfwandheri",
        "variant": "140g Cup",
        "price": 125.0,
        "mrp": 125.0,
        "net": 140.0,
        "serv": 140.0,
        "label": "1 cup (140g)",
        "n": [110.0, 15.0, 11.2, 0.5, 0.3, 0.0, 5.0, 0.4, 8.5, 0.0, 60.0],
        "ing": "Pasteurized Skimmed Cow Milk, Milk Protein Concentrate, Alphonso Mango Pulp, Stevia Extract, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Zero-fat, zero-added-sugar high-protein Greek yogurt cup delivering 15g complete dairy protein per 140g cup with real Alphonso mango.",
        "protein_source": "Strained Greek Yogurt & Milk Protein",
        "protein_tier": "tier_1",
    },
    471: {
        "source_stem": "epigamia-zero-added-sugar-greek-yogurt-smoothie-blueberry",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Zero Added Sugar Greek Yogurt Smoothie Blueberry",
        "url": "https://epigamia.com/products/zero-added-sugar-greek-yogurt-smoothies-blueberry-v-zfwandheri",
        "variant": "180ml Bottle",
        "price": 100.0,
        "mrp": 100.0,
        "net": 180.0,
        "serv": 180.0,
        "label": "1 bottle (180ml)",
        "n": [113.0, 10.0, 12.5, 2.5, 1.6, 0.0, 10.0, 0.5, 9.0, 0.0, 65.0],
        "ing": "Greek Yogurt (Pasteurized Toned Milk, Milk Solids, Active Probiotic Cultures), Blueberry Puree, Steviol Glycosides",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Drinkable probiotic Greek yogurt smoothie providing 10g dairy protein per 180ml bottle with real blueberry puree and zero added sugar.",
        "protein_source": "Greek Yogurt Dairy Protein",
        "protein_tier": "tier_1",
    },
    472: {
        "source_stem": "epigamia-zero-added-sugar-greek-yogurt-smoothie-strawberry",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Zero Added Sugar Greek Yogurt Smoothie Strawberry",
        "url": "https://epigamia.com/products/zero-added-sugar-greek-yogurt-smoothies-strawberry-v-zfwandheri",
        "variant": "180ml Bottle",
        "price": 100.0,
        "mrp": 100.0,
        "net": 180.0,
        "serv": 180.0,
        "label": "1 bottle (180ml)",
        "n": [113.0, 10.0, 12.5, 2.5, 1.6, 0.0, 10.0, 0.5, 9.0, 0.0, 65.0],
        "ing": "Greek Yogurt (Pasteurized Toned Milk, Milk Solids, Active Probiotic Cultures), Strawberry Puree, Steviol Glycosides",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Drinkable probiotic Greek yogurt smoothie providing 10g dairy protein per 180ml bottle with real strawberry puree and zero added sugar.",
        "protein_source": "Greek Yogurt Dairy Protein",
        "protein_tier": "tier_1",
    },
    473: {
        "source_stem": "epigamia-zero-added-sugar-greek-yogurt-alphonso-mango",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Zero Added Sugar Greek Yogurt Alphonso Mango",
        "url": "https://epigamia.com/products/zero-added-sugar-greek-yogurt-mango-v-zfwandheri",
        "variant": "85g Cup",
        "price": 70.0,
        "mrp": 70.0,
        "net": 85.0,
        "serv": 85.0,
        "label": "1 cup (85g)",
        "n": [58.0, 5.0, 6.2, 1.5, 1.0, 0.0, 6.0, 0.2, 5.5, 0.0, 38.0],
        "ing": "Pasteurized Toned Cow Milk, Alphonso Mango Pulp, Milk Solids, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Single-serve 85g Greek yogurt cup with real Alphonso mango pulp, 5g protein, only 58 kcal, and zero added refined sugar.",
        "protein_source": "Strained Greek Yogurt Protein",
        "protein_tier": "tier_1",
    },
    474: {
        "source_stem": "epigamia-lactose-free-mishti-doi",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Lactose Free Mishti Doi Multipack",
        "url": "https://epigamia.com/products/lactose-free-mishti-doi-pack-of-4",
        "variant": "Pack of 4 (340g)",
        "price": 119.0,
        "mrp": 119.0,
        "net": 340.0,
        "serv": 85.0,
        "label": "1 cup (85g)",
        "n": [93.0, 3.8, 13.5, 2.6, 1.7, 0.0, 8.0, 0.0, 12.5, 8.0, 42.0],
        "ing": "Pasteurized Toned Milk, Jaggery, Sugar, Milk Solids, Lactase Enzyme, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "Lactose-Free"],
        "desc": "Lactose-free artisanal Bengali Mishti Doi sweetened with real jaggery and fermented with live probiotic cultures (pack of 4 x 85g cups).",
        "protein_source": "Cultured Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    475: {
        "source_stem": "epigamia-greek-yogurt-wild-raspberry",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Greek Yogurt Wild Raspberry",
        "url": "https://epigamia.com/products/greek-yogurt-wild-raspberry-85-gm-v-epigamia-v-zfwchennai",
        "variant": "85g Cup",
        "price": 60.0,
        "mrp": 60.0,
        "net": 85.0,
        "serv": 85.0,
        "label": "1 cup (85g)",
        "n": [85.0, 5.8, 11.0, 2.0, 1.3, 0.0, 7.0, 0.3, 9.5, 5.5, 40.0],
        "ing": "Pasteurized Toned Milk, Wild Raspberry Fruit Preparation (Raspberries, Sugar, Pectin), Milk Solids, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Thick strained Greek yogurt blended with wild raspberry fruit prep, delivering 5.8g dairy protein per 85g cup with zero preservatives.",
        "protein_source": "Strained Greek Yogurt Protein",
        "protein_tier": "tier_1",
    },
    476: {
        "source_stem": "epigamia-zero-added-sugar-greek-yogurt-mixed-berries-multipack",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Zero Added Sugar Greek Yogurt Mixed Berries Multipack",
        "url": "https://epigamia.com/products/zero-added-sugar-greek-yogurt-mixed-berries-pack-of-4-v-zfwkalyannagar",
        "variant": "Pack of 4 (340g)",
        "price": 280.0,
        "mrp": 280.0,
        "net": 340.0,
        "serv": 85.0,
        "label": "1 cup (85g)",
        "n": [68.0, 5.0, 8.0, 1.8, 1.1, 0.0, 6.0, 0.4, 6.0, 0.0, 38.0],
        "ing": "Pasteurized Toned Milk, Mixed Berries Compote (Strawberry, Blueberry, Raspberry), Milk Solids, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Multipack of 4 x 85g Zero Added Sugar Mixed Berries Greek Yogurt cups providing 5g protein and 68 kcal per cup.",
        "protein_source": "Strained Greek Yogurt Protein",
        "protein_tier": "tier_1",
    },
    477: {
        "source_stem": "epigamia-zero-added-sugar-greek-yogurt-strawberry-multipack",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Zero Added Sugar Greek Yogurt Strawberry Multipack",
        "url": "https://epigamia.com/products/zero-added-sugar-greek-yogurt-strawberry-pack-of-4-v-zfwkalyannagar",
        "variant": "Pack of 4 (340g)",
        "price": 280.0,
        "mrp": 280.0,
        "net": 340.0,
        "serv": 85.0,
        "label": "1 cup (85g)",
        "n": [61.0, 5.0, 6.8, 1.6, 1.0, 0.0, 6.0, 0.3, 5.5, 0.0, 38.0],
        "ing": "Pasteurized Toned Milk, Strawberry Pulp, Milk Solids, Active Lactic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Multipack of 4 x 85g Zero Added Sugar Strawberry Greek Yogurt cups providing 5g complete dairy protein and 61 kcal per cup.",
        "protein_source": "Strained Greek Yogurt Protein",
        "protein_tier": "tier_1",
    },
    478: {
        "source_stem": "epigamia-fruit-yogurt-strawberry",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Artisanal Fruit Yogurt Strawberry",
        "url": "https://epigamia.com/products/fruit-yogurt-strawberry-75-gms-v-kurla",
        "variant": "75g Cup",
        "price": 50.0,
        "mrp": 50.0,
        "net": 75.0,
        "serv": 75.0,
        "label": "1 cup (75g)",
        "n": [76.0, 3.5, 10.5, 2.2, 1.4, 0.0, 7.0, 0.2, 9.0, 5.0, 35.0],
        "ing": "Pasteurized Toned Milk, Strawberry Fruit Prep, Milk Solids, Sugar, Active Probiotic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Smooth probiotic fruit yogurt blended with real strawberries and live cultures in a 75g single-serve cup.",
        "protein_source": "Cultured Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    479: {
        "source_stem": "epigamia-fruit-yogurt-alphonso-mango",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Artisanal Fruit Yogurt Alphonso Mango",
        "url": "https://epigamia.com/products/fruit-yogurt-mango-75-gms-v-kurla",
        "variant": "75g Cup",
        "price": 50.0,
        "mrp": 50.0,
        "net": 75.0,
        "serv": 75.0,
        "label": "1 cup (75g)",
        "n": [77.0, 3.5, 10.8, 2.2, 1.4, 0.0, 7.0, 0.2, 9.2, 5.2, 35.0],
        "ing": "Pasteurized Toned Milk, Alphonso Mango Pulp, Milk Solids, Sugar, Active Probiotic Cultures",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Smooth probiotic fruit yogurt crafted with real Alphonso mango pulp and live gut-friendly cultures in a 75g cup.",
        "protein_source": "Cultured Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    480: {
        "source_stem": "epigamia-everyday-milkshake-chocolate",
        "cat": "dairy",
        "brand": "Epigamia",
        "name": "Everyday Milkshake Chocolate Fortified with Vitamin A & D",
        "url": "https://epigamia.com/products/milkshake-chocolate",
        "variant": "180ml Pack",
        "price": 38.0,
        "mrp": 40.0,
        "net": 180.0,
        "serv": 180.0,
        "label": "1 pack (180ml)",
        "n": [143.0, 6.2, 19.5, 4.5, 2.8, 0.0, 12.0, 0.5, 17.5, 10.5, 85.0],
        "ing": "Toned Milk, Sugar, Milk Solids, Cocoa Powder (1.2%), Stabilizer (INS 407), Vitamin A & D2",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Ready-to-drink chocolate dairy milkshake fortified with Vitamins A and D, offering 6.2g milk protein per 180ml Tetra Pak.",
        "protein_source": "Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    481: {
        "source_stem": "humpy-farms-a2-desi-cow-paneer",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "A2 Desi Cow Paneer Crafted Using Lemon Juice",
        "url": "https://www.humpyfarms.com/products/a2-desi-cow-paneer",
        "variant": "200g Pack",
        "price": 126.0,
        "mrp": 140.0,
        "net": 200.0,
        "serv": 100.0,
        "label": "100g serving",
        "n": [271.0, 19.5, 3.2, 20.0, 12.5, 0.0, 55.0, 0.0, 1.8, 0.0, 28.0],
        "ing": "100% Pure A2 Desi Cow Milk, Natural Lemon Juice (Free from Synthetic Acids)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Farm-fresh A2 Desi Cow Paneer coagulated naturally using lemon juice without synthetic acids, delivering 19.5g A2 protein per 100g.",
        "protein_source": "A2 Desi Cow Milk Casein & Whey",
        "protein_tier": "tier_1",
    },
    482: {
        "source_stem": "humpy-farms-a2-desi-cow-cheese-plain",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "A2 Desi Cow Cheese Plain Block",
        "url": "https://www.humpyfarms.com/products/a2-cheese-plain",
        "variant": "200g Block",
        "price": 220.0,
        "mrp": 250.0,
        "net": 200.0,
        "serv": 30.0,
        "label": "1 slice/cube (30g)",
        "n": [102.0, 7.2, 0.8, 7.8, 5.0, 0.0, 24.0, 0.0, 0.4, 0.0, 180.0],
        "ing": "Pasteurized A2 Desi Cow Milk, Vegetarian Microbial Rennet, Cheese Culture, Himalayan Pink Salt",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Artisanal plain cheese block made from A2 Desi Cow milk and vegetarian microbial rennet with 24% protein density (7.2g per 30g serving).",
        "protein_source": "A2 Desi Cow Cheese Protein",
        "protein_tier": "tier_1",
    },
    483: {
        "source_stem": "humpy-farms-a2-desi-cow-cheese-garlic",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "A2 Desi Cow Cheese Garlic Block",
        "url": "https://www.humpyfarms.com/products/a2-garlic-cheese",
        "variant": "200g Block",
        "price": 220.0,
        "mrp": 250.0,
        "net": 200.0,
        "serv": 30.0,
        "label": "1 slice/cube (30g)",
        "n": [101.0, 7.2, 1.0, 7.6, 4.9, 0.0, 24.0, 0.0, 0.4, 0.0, 185.0],
        "ing": "Pasteurized A2 Desi Cow Milk, Fresh Roasted Garlic, Vegetarian Microbial Rennet, Cheese Culture, Himalayan Pink Salt",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Artisanal garlic-infused cheese block crafted from A2 Desi Cow milk and microbial rennet, providing 7.2g complete protein per 30g serving.",
        "protein_source": "A2 Desi Cow Cheese Protein",
        "protein_tier": "tier_1",
    },
    484: {
        "source_stem": "humpy-farms-a2-desi-cow-milk-glass-bottle",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "Farm Fresh A2 Desi Cow Milk Glass Bottle",
        "url": "https://www.humpyfarms.com/products/a2-desi-cow-milk-glass-bottle",
        "variant": "1L Glass Bottle",
        "price": 102.0,
        "mrp": 110.0,
        "net": 1000.0,
        "serv": 250.0,
        "label": "1 glass (250ml)",
        "n": [168.0, 8.5, 12.0, 9.5, 6.0, 0.0, 28.0, 0.0, 11.5, 0.0, 110.0],
        "ing": "100% Farm Fresh Unhomogenized Grass-Fed A2 Desi Cow Milk",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Grass-fed, free-range A2 Desi Cow milk delivered in a reusable 1L glass bottle, offering 8.5g natural A2 beta-casein protein per 250ml glass.",
        "protein_source": "A2 Desi Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    485: {
        "source_stem": "humpy-farms-a2-desi-cow-milk-pouch",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "Pasteurized A2 Desi Cow Milk Pouch",
        "url": "https://www.humpyfarms.com/products/a2-desi-cow-milk-pouch",
        "variant": "1L Pouch",
        "price": 98.0,
        "mrp": 105.0,
        "net": 1000.0,
        "serv": 250.0,
        "label": "1 glass (250ml)",
        "n": [168.0, 8.5, 12.0, 9.5, 6.0, 0.0, 28.0, 0.0, 11.5, 0.0, 110.0],
        "ing": "100% Pasteurized Grass-Fed A2 Desi Cow Milk",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Pasteurized grass-fed A2 Desi Cow milk in a 1L pouch, free from antibiotics and growth hormones, with 8.5g A2 protein per 250ml serving.",
        "protein_source": "A2 Desi Cow Milk Protein",
        "protein_tier": "tier_1",
    },
    486: {
        "source_stem": "humpy-farms-desi-buffalo-milk-glass-bottle",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "Pasteurized Desi Buffalo Milk Glass Bottle",
        "url": "https://www.humpyfarms.com/products/a2-desi-buffalo-milk",
        "variant": "1L Glass Bottle",
        "price": 110.0,
        "mrp": 115.0,
        "net": 1000.0,
        "serv": 250.0,
        "label": "1 glass (250ml)",
        "n": [242.0, 10.5, 13.0, 16.5, 10.5, 0.0, 42.0, 0.0, 12.0, 0.0, 125.0],
        "ing": "100% Pasteurized Free-Range Desi Buffalo Milk",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Rich, creamy pasteurized Desi Buffalo milk in a 1L glass bottle providing 10.5g complete dairy protein and high calcium per 250ml glass.",
        "protein_source": "Desi Buffalo Milk Protein",
        "protein_tier": "tier_1",
    },
    487: {
        "source_stem": "humpy-farms-desi-buffalo-milk-pouch",
        "cat": "dairy",
        "brand": "Humpy Farms",
        "name": "Pasteurized Desi Buffalo Milk Pouch",
        "url": "https://www.humpyfarms.com/products/desi-cow-milk-pouch-copy",
        "variant": "1L Pouch",
        "price": 104.0,
        "mrp": 110.0,
        "net": 1000.0,
        "serv": 250.0,
        "label": "1 glass (250ml)",
        "n": [242.0, 10.5, 13.0, 16.5, 10.5, 0.0, 42.0, 0.0, 12.0, 0.0, 125.0],
        "ing": "100% Pasteurized Free-Range Desi Buffalo Milk",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Pasteurized free-range Desi Buffalo milk in a 1L pouch delivering 10.5g dairy protein per 250ml glass, ideal for thick homemade curd and paneer.",
        "protein_source": "Desi Buffalo Milk Protein",
        "protein_tier": "tier_1",
    },
}

uploaded_urls = {}
BATCH4_RECORDS = {}

for idx, spec in BATCH4_SPEC.items():
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
    BATCH4_RECORDS[idx] = ("manual", target_slug, spec["cat"], brand, manual_obj, reading_obj)

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

    if old_idx in BATCH4_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH4_RECORDS[old_idx]
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
    if obj["handle"] in old_slugs_to_delete_from_supabase:
        continue
    manual_map[obj["handle"]] = obj

for _, (_, handle, _, _, manual_obj, _) in BATCH4_RECORDS.items():
    manual_map[handle] = manual_obj

(HERE / "manual_entries.jsonl").write_text(
    "\n".join(json.dumps(v, ensure_ascii=False) for v in manual_map.values()) + "\n",
    encoding="utf-8",
)
print(f"Updated manual_entries.jsonl ({len(manual_map)} unique manual handles)")

# Remove empty-image amul-high-protein-milk and amul-high-protein-dahi from store_snapshot.json
snap_path = HERE / "store_snapshot.json"
snap = json.loads(snap_path.read_text(encoding="utf-8"))
if "shop.amul.com" in snap:
    snap["shop.amul.com"] = [
        p for p in snap["shop.amul.com"]
        if p.get("handle") not in ("amul-high-protein-milk", "amul-high-protein-dahi")
    ]
snap_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Old slugs to remove from seedCatalog.json & live Supabase: {sorted(old_slugs_to_delete_from_supabase)}")

seed_web_path = ROOT / "protein-web" / "src" / "data" / "seedCatalog.json"
existing_seed = json.loads(seed_web_path.read_text(encoding="utf-8"))
cleaned_seed = [item for item in existing_seed if item.get("slug") not in old_slugs_to_delete_from_supabase]
seed_web_path.write_text(json.dumps(cleaned_seed, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Pre-cleaned seedCatalog.json: {len(existing_seed)} -> {len(cleaned_seed)} items")

(ROOT / "protein-etl" / "scratch" / "batch4_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8",
)
(ROOT / "protein-etl" / "scratch" / "batch4_active_slugs.json").write_text(
    json.dumps(sorted(uploaded_urls.keys()), indent=2),
    encoding="utf-8",
)
