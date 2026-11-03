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

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch5_webp"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# Duplicate lines in current 571-line picks.txt / readings.jsonl to remove:
DUPLICATE_INDICES_TO_REMOVE = {
    494,  # aashirvaad-proactive-high-protein-atta (duplicates i=432)
    503,  # fortune-soya-chunks-protein-rich (duplicates i=428)
}

# 11-element nutrition array n:
# [calories, protein, carbs, fat, sat_fat, trans_fat, cholesterol, fiber, total_sugar, added_sugar, sodium]
BATCH5_SPEC = {
    428: {
        "source_stem": "as-it-is-atom-roti-protein",
        "cat": "staples",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Roti Protein Unflavoured Chapati Mix",
        "url": "https://asitisnutrition.com/products/as-it-is-atom-roti-protein-1kg-make-roti-s-protein-rich-easy-to-use-25g-protein-per-serving",
        "variant": "500g Pouch",
        "price": 577.0,
        "mrp": 799.0,
        "net": 500.0,
        "serv": 50.0,
        "label": "1 scoop / mix (50g)",
        "n": [178.0, 25.0, 14.0, 2.4, 0.4, 0.0, 0.0, 4.5, 0.5, 0.0, 120.0],
        "ing": "Isolated Soy Protein, Pea Protein Isolate, Chickpea Flour, Wheat Gluten, Dietary Fibre, Digestive Enzymes",
        "allergens": ["Soy", "Gluten", "Wheat"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Unflavoured high-protein chapati dough fortifier delivering 25g plant protein per 50g serving to turn everyday rotis into protein-rich meals.",
        "protein_source": "Soy & Pea Protein Isolate Blend",
        "protein_tier": "tier_2",
    },
    429: {
        "source_stem": "lo-foods-low-carb-high-protein-atta",
        "cat": "staples",
        "brand": "Lo! Foods",
        "name": "Lo Carb High Protein Atta Flour",
        "url": "https://lofoods.fit/products/low-carb-high-protein-atta",
        "variant": "1kg Pouch",
        "price": 374.0,
        "mrp": 449.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [336.0, 28.0, 42.0, 6.2, 1.0, 0.0, 0.0, 18.0, 1.5, 0.0, 45.0],
        "ing": "Superfood Seeds & Nuts Blend (Sunflower, Flax, Melon, Pumpkin, Peanuts), Isolated Wheat & Soy Protein, Whole Wheat Flour, Oat Fibre",
        "allergens": ["Wheat", "Gluten", "Soy", "Peanuts"],
        "tags": ["Vegetarian", "No Added Sugar", "Low-GI"],
        "desc": "Low-carb, high-protein everyday chapati flour enriched with superfood seeds and isolated plant proteins, offering 28g protein and 18g fiber per 100g.",
        "protein_source": "Wheat, Soy & Seed Protein Blend",
        "protein_tier": "tier_2",
    },
    430: {
        "source_stem": "lo-foods-gluten-free-multi-millet-atta",
        "cat": "staples",
        "brand": "Lo! Foods",
        "name": "Protein Chef Gluten Free Multi-Millet Atta",
        "url": "https://lofoods.fit/products/gluten-free-multi-millet-atta",
        "variant": "1kg Pouch",
        "price": 224.0,
        "mrp": 249.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [348.0, 12.8, 66.0, 3.6, 0.6, 0.0, 0.0, 10.5, 1.0, 0.0, 22.0],
        "ing": "Jowar (Sorghum) Flour, Ragi (Finger Millet) Flour, Bajra (Pearl Millet) Flour, Chickpea (Besan) Flour, Amaranth Flour, Psyllium Husk",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
        "desc": "100% gluten-free multi-millet chapati flour combining Jowar, Ragi, Bajra, Amaranth, and Chickpea flour for 12.8g protein and 10.5g fiber per 100g.",
        "protein_source": "Multi-Millet & Chickpea Protein",
        "protein_tier": "tier_3",
    },
    431: {
        "source_stem": "anveshan-high-protein-atta",
        "cat": "staples",
        "brand": "Anveshan",
        "name": "High Protein Stone-Ground Atta",
        "url": "https://www.anveshan.farm/products/high-protein-atta",
        "variant": "1kg Pouch",
        "price": 400.0,
        "mrp": 420.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [356.0, 21.5, 58.0, 4.2, 0.7, 0.0, 0.0, 11.2, 1.2, 0.0, 18.0],
        "ing": "Stone-Ground Khapli (Emmer) Wheat, Roasted Chana Sattu, Defatted Soy Flour, Flaxseeds, Methi Seeds, Moringa Leaf Powder",
        "allergens": ["Wheat", "Gluten", "Soy"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Traditional stone-ground high-protein atta crafted from ancient Khapli wheat, roasted Chana Sattu, flaxseeds, and moringa, delivering 21.5g protein per 100g.",
        "protein_source": "Khapli Wheat, Chana Sattu & Soy Blend",
        "protein_tier": "tier_2",
    },
    432: {
        "source_stem": "anveshan-khapli-multigrain-atta",
        "cat": "staples",
        "brand": "Anveshan",
        "name": "Khapli Multigrain Stone-Ground Atta",
        "url": "https://www.anveshan.farm/products/khapli-multigrain-atta",
        "variant": "2kg Pouch",
        "price": 198.0,
        "mrp": 240.0,
        "net": 2000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [346.0, 14.5, 65.0, 3.2, 0.5, 0.0, 0.0, 10.8, 1.4, 0.0, 15.0],
        "ing": "Khapli (Emmer) Wheat (60%), Chana Dal, Jowar, Bajra, Ragi, Jau (Barley), Amaranth (Rajgira)",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar", "Low-GI"],
        "desc": "Slow stone-ground multigrain flour combining low-GI Khapli Emmer wheat with Chana Dal, Jowar, Ragi, and Barley for 14.5g protein per 100g.",
        "protein_source": "Khapli Emmer Wheat & Pulse Protein",
        "protein_tier": "tier_3",
    },
    434: {
        "source_stem": "humpy-farms-organic-besan",
        "cat": "staples",
        "brand": "Humpy Farms",
        "name": "Organic Stone-Ground Besan Chickpea Flour",
        "url": "https://www.humpyfarms.com/products/organic-besan",
        "variant": "1kg Pouch",
        "price": 203.0,
        "mrp": 225.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [372.0, 22.0, 58.0, 5.8, 0.7, 0.0, 0.0, 10.8, 2.5, 0.0, 32.0],
        "ing": "100% Certified Organic Unpolished Chana Dal (Bengal Gram) Stone-Ground Flour",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
        "desc": "Certified organic stone-ground Besan milled from unpolished Bengal gram (Chana Dal), naturally rich in 22g plant protein and 10.8g dietary fiber per 100g.",
        "protein_source": "Chickpea (Bengal Gram) Protein",
        "protein_tier": "tier_2",
    },
    435: {
        "source_stem": "pintola-organic-quinoa",
        "cat": "staples",
        "brand": "Pintola",
        "name": "Organic High Protein & Fibre Quinoa",
        "url": "https://pintola.in/products/pintola-organic-quinoa-high-in-protein-fibre-minerals-cholesterol-free-gluten-free-aids-weight-management",
        "variant": "500g Pouch",
        "price": 165.0,
        "mrp": 210.0,
        "net": 500.0,
        "serv": 100.0,
        "label": "100g dry grain",
        "n": [368.0, 14.1, 64.2, 6.1, 0.7, 0.0, 0.0, 7.0, 0.9, 0.0, 5.0],
        "ing": "100% Certified Organic White Quinoa Seeds",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
        "desc": "100% organic, gluten-free white quinoa grain containing all 9 essential amino acids with 14.1g complete plant protein and 7g fiber per 100g.",
        "protein_source": "Complete Quinoa Grain Protein",
        "protein_tier": "tier_2",
    },
    488: {
        "source_stem": "wickedgud-multigrain-fusilli-pasta",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Multigrain Fusilli Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-fusilli-pasta-pack-of-4",
        "variant": "Pack of 4 (1.6kg)",
        "price": 642.0,
        "mrp": 700.0,
        "net": 1600.0,
        "serv": 100.0,
        "label": "100g dry pasta",
        "n": [352.0, 14.2, 68.0, 2.5, 0.4, 0.0, 0.0, 8.5, 1.8, 0.0, 14.0],
        "ing": "Whole Wheat Semolina, Chickpea Flour, Red Lentil Flour, Jowar Flour, Oats Flour",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Zero-maida multigrain fusilli pasta crafted from whole wheat, chickpea, lentil, and millet flours, delivering 14.2g protein and 8.5g fiber per 100g.",
        "protein_source": "Chickpea, Lentil & Durum Wheat Protein",
        "protein_tier": "tier_2",
    },
    489: {
        "source_stem": "wickedgud-multigrain-penne-pasta",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Multigrain Penne Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-penne-pasta-pack-of-4",
        "variant": "Pack of 4 (1.6kg)",
        "price": 642.0,
        "mrp": 700.0,
        "net": 1600.0,
        "serv": 100.0,
        "label": "100g dry pasta",
        "n": [352.0, 14.2, 68.0, 2.5, 0.4, 0.0, 0.0, 8.5, 1.8, 0.0, 14.0],
        "ing": "Whole Wheat Semolina, Chickpea Flour, Red Lentil Flour, Jowar Flour, Oats Flour",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Zero-maida multigrain penne pasta made with chickpea, red lentil, oats, and whole wheat, providing 14.2g plant protein and 8.5g fiber per 100g.",
        "protein_source": "Chickpea, Lentil & Durum Wheat Protein",
        "protein_tier": "tier_2",
    },
    490: {
        "source_stem": "wickedgud-nourishing-instant-noodles-schezwan",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Nourishing Instant Noodles Schezwan Zero Maida",
        "url": "https://www.wickedgud.com/products/nourishing-instant-noodles-schezwan-pack-of-10",
        "variant": "Pack of 10 (690g)",
        "price": 438.0,
        "mrp": 450.0,
        "net": 690.0,
        "serv": 100.0,
        "label": "100g noodles",
        "n": [375.0, 12.5, 66.0, 6.8, 1.2, 0.0, 0.0, 6.2, 2.0, 1.0, 580.0],
        "ing": "Whole Wheat Atta, Oats Flour, Chana Dal Flour, Jowar Flour, Steaming & Air-Drying Matrix, Schezwan Spice Mix (Chilli, Garlic, Ginger, Onion, Spices)",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan"],
        "desc": "Steamed and baked (not fried) zero-maida, zero-palm-oil Schezwan instant noodles made with whole wheat, oats, and chana dal providing 12.5g protein per 100g.",
        "protein_source": "Whole Wheat, Oats & Chana Dal Protein",
        "protein_tier": "tier_3",
    },
    491: {
        "source_stem": "wickedgud-nourishing-instant-noodles-masala",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Nourishing Instant Noodles Masala Zero Maida",
        "url": "https://www.wickedgud.com/products/nourishing-instant-noodles-masala-pack-of-10",
        "variant": "Pack of 10 (690g)",
        "price": 438.0,
        "mrp": 450.0,
        "net": 690.0,
        "serv": 100.0,
        "label": "100g noodles",
        "n": [372.0, 12.5, 65.5, 6.5, 1.1, 0.0, 0.0, 6.4, 1.8, 0.8, 560.0],
        "ing": "Whole Wheat Atta, Oats Flour, Chana Dal Flour, Jowar Flour, Desi Masala Spice Mix (Turmeric, Coriander, Cumin, Black Pepper, Garlic, Onion)",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan"],
        "desc": "Zero-maida, zero-palm-oil Masala instant noodles crafted with whole wheat, oats, and chana dal flour using convection air-drying for 12.5g protein per 100g.",
        "protein_source": "Whole Wheat, Oats & Chana Dal Protein",
        "protein_tier": "tier_3",
    },
    492: {
        "source_stem": "wickedgud-multigrain-spaghetti-pasta",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Multigrain Spaghetti Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-spaghetti-pasta-pack-of-4",
        "variant": "Pack of 4 (1.6kg)",
        "price": 730.0,
        "mrp": 780.0,
        "net": 1600.0,
        "serv": 100.0,
        "label": "100g dry pasta",
        "n": [350.0, 14.0, 68.2, 2.4, 0.4, 0.0, 0.0, 8.2, 1.8, 0.0, 14.0],
        "ing": "Durum Whole Wheat Semolina, Chickpea Flour, Red Lentil Flour, Jowar Flour, Oats Flour",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "High-protein, high-fibre zero-maida multigrain spaghetti pasta blended with chickpea and lentil flours for 14g protein per 100g serving.",
        "protein_source": "Chickpea, Lentil & Durum Wheat Protein",
        "protein_tier": "tier_2",
    },
    493: {
        "source_stem": "wickedgud-multigrain-macaroni-pasta",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Multigrain Macaroni Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-macaroni-pasta-pack-of-4",
        "variant": "Pack of 4 (1.6kg)",
        "price": 642.0,
        "mrp": 700.0,
        "net": 1600.0,
        "serv": 100.0,
        "label": "100g dry pasta",
        "n": [352.0, 14.2, 68.0, 2.5, 0.4, 0.0, 0.0, 8.5, 1.8, 0.0, 14.0],
        "ing": "Whole Wheat Semolina, Chickpea Flour, Red Lentil Flour, Jowar Flour, Oats Flour",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Zero-maida multigrain elbow macaroni pasta fortified with chickpea, lentil, and millet flours, delivering 14.2g protein and 8.5g dietary fiber per 100g.",
        "protein_source": "Chickpea, Lentil & Durum Wheat Protein",
        "protein_tier": "tier_2",
    },
    495: {
        "source_stem": "wickedgud-whole-wheat-wraps-rolls",
        "cat": "staples",
        "brand": "WickedGud",
        "name": "Whole Wheat Wraps & Rolls Zero Maida",
        "url": "https://www.wickedgud.com/products/whole-wheat-wraps-rolls",
        "variant": "Pack of 6 Wraps (300g)",
        "price": 180.0,
        "mrp": 199.0,
        "net": 300.0,
        "serv": 100.0,
        "label": "2 wraps (100g)",
        "n": [298.0, 12.5, 52.0, 4.5, 0.6, 0.0, 0.0, 7.5, 1.2, 0.0, 310.0],
        "ing": "100% Whole Wheat Atta, Chickpea Protein Flour, Cold-Pressed Sunflower Oil, Himalayan Pink Salt",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Soft, ready-to-cook 100% whole wheat wraps with zero maida and added chickpea flour, providing 12.5g protein and 7.5g fiber per 100g.",
        "protein_source": "Whole Wheat & Chickpea Protein",
        "protein_tier": "tier_3",
    },
    496: {
        "source_stem": "twf-whole-wheat-bread-flour",
        "cat": "staples",
        "brand": "TWF Flours",
        "name": "Whole Wheat Bread Flour Unbleached Stone-Milled",
        "url": "https://twfflours.com/products/twf-whole-wheat-bread-flour",
        "variant": "1kg Bag",
        "price": 149.0,
        "mrp": 175.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [345.0, 13.8, 67.5, 2.2, 0.4, 0.0, 0.0, 9.8, 1.0, 0.0, 8.0],
        "ing": "100% Single-Origin High-Protein Hard Spring Whole Wheat (Unbleached, Bromate-Free)",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Precision-milled, unbleached high-protein whole wheat bread flour with 13.8g natural wheat protein per 100g for artisanal sourdough and whole-grain loaves.",
        "protein_source": "Hard Spring Wheat Protein",
        "protein_tier": "tier_3",
    },
    497: {
        "source_stem": "twf-high-fibre-maida",
        "cat": "staples",
        "brand": "TWF Flours",
        "name": "High Fibre Maida Unbleached Craft Flour",
        "url": "https://twfflours.com/products/twf-high-fibre-maida",
        "variant": "1kg Bag",
        "price": 149.0,
        "mrp": 175.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [348.0, 13.2, 69.0, 1.8, 0.3, 0.0, 0.0, 7.5, 0.8, 0.0, 6.0],
        "ing": "Unbleached High-Extraction Hard Wheat Endosperm & Aleurone Layer Flour (Zero Chemical Bleaching Agents)",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Unbleached high-extraction craft flour retaining the nutrient-rich wheat aleurone layer for 13.2g protein and 3x more dietary fiber than regular maida.",
        "protein_source": "High-Extraction Wheat Protein",
        "protein_tier": "tier_3",
    },
    498: {
        "source_stem": "twf-multigrain-flour",
        "cat": "staples",
        "brand": "TWF Flours",
        "name": "Multigrain Stone-Milled Craft Flour",
        "url": "https://twfflours.com/products/twf-multigrain-flour",
        "variant": "1kg Bag",
        "price": 149.0,
        "mrp": 175.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry flour",
        "n": [344.0, 14.5, 64.0, 3.3, 0.5, 0.0, 0.0, 11.0, 1.2, 0.0, 12.0],
        "ing": "Sharabati & Khapli Whole Wheat, Roasted Chana Dal, Rolled Oats, Ragi, Jowar, Flaxseeds",
        "allergens": ["Wheat", "Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar"],
        "desc": "Freshly stone-milled multigrain chapati flour combining heirloom wheat, roasted chana dal, oats, ragi, and flaxseeds for 14.5g protein and 11g fiber per 100g.",
        "protein_source": "Heirloom Wheat, Chana Dal & Seed Protein",
        "protein_tier": "tier_3",
    },
    499: {
        "source_stem": "jiwa-30-degree-peanut-flour",
        "cat": "staples",
        "brand": "Jiwa",
        "name": "30 Degree Cold-Pressed High Protein Peanut Flour",
        "url": "https://jiwa.in/products/30-degree-peanut-flour",
        "variant": "200g Pouch",
        "price": 149.0,
        "mrp": 175.0,
        "net": 200.0,
        "serv": 100.0,
        "label": "100g flour",
        "n": [386.0, 50.0, 20.0, 11.8, 1.8, 0.0, 0.0, 11.5, 4.0, 0.0, 18.0],
        "ing": "100% Cold-Pressed Defatted Roasted Groundnuts (Peanuts) Milled at 30°C",
        "allergens": ["Peanuts"],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar", "Keto-Friendly"],
        "desc": "Cold-pressed, partially defatted peanut flour milled at 30°C to preserve nutrients, packing 50g plant protein (50% protein density) and 11.5g fiber per 100g.",
        "protein_source": "Cold-Pressed Peanut Protein",
        "protein_tier": "tier_2",
    },
    500: {
        "source_stem": "jiwa-30-degree-jau-sattu-powder",
        "cat": "staples",
        "brand": "Jiwa",
        "name": "30 Degree Jau & Chana Sattu Powder",
        "url": "https://jiwa.in/products/30-degree-jau-sattu-powder",
        "variant": "750g Pouch",
        "price": 175.0,
        "mrp": 195.0,
        "net": 750.0,
        "serv": 100.0,
        "label": "100g powder",
        "n": [358.0, 20.6, 60.0, 4.0, 0.6, 0.0, 0.0, 12.0, 1.5, 0.0, 20.0],
        "ing": "Sand-Roasted Bengal Gram (Chana Sattu) & Roasted Barley (Jau) Cold-Milled at 30°C",
        "allergens": ["Gluten"],
        "tags": ["Vegetarian", "Vegan", "No Added Sugar", "Low-GI"],
        "desc": "Traditional cooling Jau and Chana Sattu powder cold-milled at 30°C, delivering 20.6g plant protein and 12g dietary fiber per 100g for savory drinks and parathas.",
        "protein_source": "Roasted Bengal Gram & Barley Protein",
        "protein_tier": "tier_2",
    },
    501: {
        "source_stem": "humpy-farms-organic-chana-dal",
        "cat": "staples",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Chana Dal",
        "url": "https://www.humpyfarms.com/products/organic-chana-dal",
        "variant": "1kg Pouch",
        "price": 169.0,
        "mrp": 190.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry dal",
        "n": [364.0, 21.5, 58.0, 5.2, 0.7, 0.0, 0.0, 11.5, 2.2, 0.0, 26.0],
        "ing": "100% Certified Organic Unpolished Split Bengal Gram (Chana Dal)",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar", "Low-GI"],
        "desc": "Certified organic unpolished Chana Dal free from artificial oil/water polishing, providing 21.5g protein and 11.5g low-GI dietary fiber per 100g.",
        "protein_source": "Bengal Gram (Chana Dal) Protein",
        "protein_tier": "tier_2",
    },
    502: {
        "source_stem": "humpy-farms-organic-moong-dal",
        "cat": "staples",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Yellow Moong Dal",
        "url": "https://www.humpyfarms.com/products/organic-moong-dal",
        "variant": "1kg Pouch",
        "price": 247.0,
        "mrp": 270.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry dal",
        "n": [348.0, 24.0, 59.5, 1.5, 0.3, 0.0, 0.0, 8.2, 1.8, 0.0, 18.0],
        "ing": "100% Certified Organic Unpolished Split Yellow Mung Beans (Moong Dal)",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
        "desc": "Easy-to-digest organic unpolished yellow Moong Dal naturally packing 24g plant protein per 100g with only 1.5g fat.",
        "protein_source": "Mung Bean (Moong Dal) Protein",
        "protein_tier": "tier_2",
    },
    504: {
        "source_stem": "humpy-farms-organic-toor-dal",
        "cat": "staples",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Arhar Toor Dal",
        "url": "https://www.humpyfarms.com/products/organic-toor-dal",
        "variant": "1kg Pouch",
        "price": 236.0,
        "mrp": 260.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "100g dry dal",
        "n": [343.0, 22.3, 57.6, 1.7, 0.3, 0.0, 0.0, 9.5, 2.0, 0.0, 22.0],
        "ing": "100% Certified Organic Unpolished Split Pigeon Peas (Arhar / Toor Dal)",
        "allergens": [],
        "tags": ["Vegetarian", "Vegan", "Gluten-Free", "No Added Sugar"],
        "desc": "Farm-fresh organic unpolished Arhar Toor Dal rich in folic acid, iron, and 22.3g plant protein per 100g.",
        "protein_source": "Pigeon Pea (Toor Dal) Protein",
        "protein_tier": "tier_2",
    },
}

uploaded_urls = {}
BATCH5_RECORDS = {}

for idx, spec in BATCH5_SPEC.items():
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
    BATCH5_RECORDS[idx] = ("manual", target_slug, spec["cat"], brand, manual_obj, reading_obj)

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
        old_slugs_to_delete_from_supabase.add(old_slug)
        continue

    if old_idx in BATCH5_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH5_RECORDS[old_idx]
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

for _, (_, handle, _, _, manual_obj, _) in BATCH5_RECORDS.items():
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

(ROOT / "protein-etl" / "scratch" / "batch5_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8",
)
(ROOT / "protein-etl" / "scratch" / "batch5_active_slugs.json").write_text(
    json.dumps(sorted(uploaded_urls.keys()), indent=2),
    encoding="utf-8",
)
