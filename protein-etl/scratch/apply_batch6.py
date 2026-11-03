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

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch6_webp"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# Duplicate lines in current 569-line picks.txt / readings.jsonl to remove:
DUPLICATE_INDICES_TO_REMOVE = {
    554,  # ensure-plus-high-protein-vanilla (duplicates i=415)
    555,  # ensure-diabetes-care-vanilla (duplicates i=416)
}

# 11-element nutrition array n:
# [calories, protein, carbs, fat, sat_fat, trans_fat, cholesterol, fiber, total_sugar, added_sugar, sodium]
# Note: adult-nutrition density range in verify_demo_catalog.py is (10, 45)%
BATCH6_SPEC = {
    414: {
        "source_stem": "pentasure-daily-nutrition-vanilla-400g",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Balanced Daily Nutritional Supplement Vanilla (400g)",
        "url": "https://pentasurenutrition.com/products/nutritional-drink-daily-nutrition-new-pentasure-400gm",
        "variant": "400g Tin",
        "price": 796.0,
        "mrp": 890.0,
        "net": 400.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [216.0, 11.0, 29.5, 6.0, 1.2, 0.0, 5.0, 1.8, 3.0, 0.0, 115.0],
        "ing": "Skimmed Milk Powder, Soy Protein Isolate, Whey Protein Concentrate, Maltodextrin, High Oleic Sunflower Oil, MCT Oil, Inulin (Prebiotic Fiber), 28 Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Complete and balanced daily adult nutritional drink delivering 11g tri-protein blend, MCTs, prebiotic fiber, and 28 essential vitamins and minerals per 50g serving.",
        "protein_source": "Whey, Milk & Soy Protein Blend",
        "protein_tier": "tier_1",
    },
    415: {
        "source_stem": "pentasure-daily-nutrition-vanilla-1kg",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Balanced Daily Nutritional Supplement Vanilla (1kg)",
        "url": "https://pentasurenutrition.com/products/nutritional-drink-daily-nutrition-new-pentasure-1-kg",
        "variant": "1kg Tin",
        "price": 1887.0,
        "mrp": 2120.0,
        "net": 1000.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [216.0, 11.0, 29.5, 6.0, 1.2, 0.0, 5.0, 1.8, 3.0, 0.0, 115.0],
        "ing": "Skimmed Milk Powder, Soy Protein Isolate, Whey Protein Concentrate, Maltodextrin, High Oleic Sunflower Oil, MCT Oil, Inulin (Prebiotic Fiber), 28 Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Economical 1kg tin of PentaSure Balanced Daily Nutritional Supplement providing 11g high-quality protein and 28 micronutrients per 50g serving for adult recovery and immunity.",
        "protein_source": "Whey, Milk & Soy Protein Blend",
        "protein_tier": "tier_1",
    },
    416: {
        "source_stem": "pentasure-nutrone-healthy-ageing-kesar-badam",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Nutrone Healthy Aging Nutrition Kesar Badam",
        "url": "https://pentasurenutrition.com/products/nutrone-healthy-ageing",
        "variant": "300g Jar",
        "price": 559.0,
        "mrp": 650.0,
        "net": 300.0,
        "serv": 30.0,
        "label": "2 scoops (30g)",
        "n": [112.0, 9.5, 15.0, 1.6, 0.4, 0.0, 4.0, 2.2, 1.2, 0.0, 65.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Isolated Soy Protein, Almond Powder, Saffron Extract, Dietary Fiber, Calcium, Vitamin D3, Vitamin B12, Coenzyme Q10",
        "allergens": ["Milk", "Soy", "Tree Nuts"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Specialized senior and healthy-aging nutrition in Kesar Badam flavor fortified with 9.5g protein per 30g serving, Calcium, Vitamin D3, and CoQ10 for bone and muscle strength.",
        "protein_source": "Whey, Milk & Soy Protein Blend",
        "protein_tier": "tier_1",
    },
    417: {
        "source_stem": "pentasure-nutrone-men-saffron",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Nutrone Men Daily Strength & Immunity Nutrition Saffron",
        "url": "https://pentasurenutrition.com/products/nutrone-men",
        "variant": "300g Jar",
        "price": 566.0,
        "mrp": 650.0,
        "net": 300.0,
        "serv": 30.0,
        "label": "2 scoops (30g)",
        "n": [114.0, 10.2, 14.5, 1.6, 0.4, 0.0, 4.0, 2.0, 1.2, 0.0, 68.0],
        "ing": "Whey Protein Concentrate, Soy Protein Isolate, Skimmed Milk Powder, Ashwagandha Extract, Saffron, L-Carnitine, Zinc, Magnesium, B-Complex Vitamins",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Daily men's nutritional shake in Saffron flavor delivering 10.2g protein per 30g serving alongside Ashwagandha, Zinc, Magnesium, and essential vitamins for stamina and muscle maintenance.",
        "protein_source": "Whey & Soy Protein Blend",
        "protein_tier": "tier_1",
    },
    418: {
        "source_stem": "pentasure-nutrone-women-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Nutrone Women Daily Strength & Immunity Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/nutrone-women",
        "variant": "300g Jar",
        "price": 566.0,
        "mrp": 650.0,
        "net": 300.0,
        "serv": 30.0,
        "label": "2 scoops (30g)",
        "n": [112.0, 9.8, 14.8, 1.5, 0.4, 0.0, 4.0, 2.2, 1.4, 0.0, 65.0],
        "ing": "Whey Protein Concentrate, Soy Protein Isolate, Skimmed Milk Powder, Cocoa Powder, Ferric Pyrophosphate (Iron), Folic Acid, Calcium Citrate, Vitamin D3, Biotin, Vitamin B12",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Daily women's nutritional drink in Chocolate flavor formulated with 9.8g protein per 30g serving plus bioavailable Iron, Folic Acid, Calcium, Vitamin D3, and Biotin.",
        "protein_source": "Whey & Soy Protein Blend",
        "protein_tier": "tier_1",
    },
    419: {
        "source_stem": "pentasure-pediagold-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Vanilla",
        "url": "https://pentasurenutrition.com/products/pediagold-vanilla",
        "variant": "400g Tin",
        "price": 747.0,
        "mrp": 840.0,
        "net": 400.0,
        "serv": 45.0,
        "label": "3 scoops (45g)",
        "n": [198.0, 6.5, 29.0, 6.2, 1.5, 0.0, 6.0, 1.5, 4.5, 0.0, 85.0],
        "ing": "Skimmed Milk Powder, Whey Protein Concentrate, Maltodextrin, Vegetable Oils, FOS Prebiotic Fiber, DHA, Colostrum, 35 Vital Vitamins & Minerals",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Sucrose-free pediatric growth nutrition for children aged 2-14 years in Vanilla flavor, providing 6.5g dairy protein, DHA, Colostrum, and 35 vital nutrients per 45g serving.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_1",
    },
    423: {
        "source_stem": "pentasure-pediagold-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Chocolate",
        "url": "https://pentasurenutrition.com/products/pediagold-chocolate",
        "variant": "400g Tin",
        "price": 747.0,
        "mrp": 840.0,
        "net": 400.0,
        "serv": 45.0,
        "label": "3 scoops (45g)",
        "n": [198.0, 6.5, 29.0, 6.2, 1.5, 0.0, 6.0, 1.6, 4.5, 0.0, 88.0],
        "ing": "Skimmed Milk Powder, Whey Protein Concentrate, Maltodextrin, Alkalized Cocoa Powder, Vegetable Oils, FOS Prebiotic Fiber, DHA, Colostrum, 35 Vital Vitamins & Minerals",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Sucrose-free pediatric growth nutrition in Chocolate flavor for children aged 2-14 years, enriched with 6.5g dairy protein, DHA, and 35 essential micronutrients per 45g serving.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_1",
    },
    424: {
        "source_stem": "pentasure-pediagold-mango",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Mango",
        "url": "https://pentasurenutrition.com/products/pediagold-mango",
        "variant": "400g Tin",
        "price": 747.0,
        "mrp": 840.0,
        "net": 400.0,
        "serv": 45.0,
        "label": "3 scoops (45g)",
        "n": [198.0, 6.5, 29.0, 6.2, 1.5, 0.0, 6.0, 1.5, 4.5, 0.0, 85.0],
        "ing": "Skimmed Milk Powder, Whey Protein Concentrate, Maltodextrin, Natural Mango Flavor, Vegetable Oils, FOS Prebiotic Fiber, DHA, Colostrum, 35 Vital Vitamins & Minerals",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Mango-flavored sucrose-free complete pediatric nutrition drink for growing children aged 2-14 years with 6.5g protein, DHA, and 35 vitamins and minerals per 45g serving.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_1",
    },
    425: {
        "source_stem": "pentasure-pediagold-plus-peptide-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "PediaGold Plus 100% Peptide Diet for Kids Vanilla",
        "url": "https://pentasurenutrition.com/products/pediagold-plus",
        "variant": "400g Tin",
        "price": 1411.0,
        "mrp": 1590.0,
        "net": 400.0,
        "serv": 45.0,
        "label": "3 scoops (45g)",
        "n": [202.0, 7.2, 28.5, 6.6, 2.2, 0.0, 8.0, 1.2, 3.0, 0.0, 90.0],
        "ing": "Hydrolyzed Whey Peptides (100% Peptide Protein), Medium Chain Triglycerides (MCT), Maltodextrin, DHA, Prebiotic FOS, L-Glutamine, Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Specialized 100% hydrolyzed whey peptide diet for children with malabsorption or recovery needs, delivering 7.2g pre-digested protein and MCTs per 45g serving.",
        "protein_source": "100% Hydrolyzed Whey Peptides",
        "protein_tier": "tier_1",
    },
    426: {
        "source_stem": "nakpro-gen-z-teen-protein-chocolate",
        "cat": "adult-nutrition",
        "brand": "Nakpro",
        "name": "Gen-Z Protein Powder for Teenagers Double Rich Chocolate",
        "url": "https://nakpro.com/products/gen-z-teen-protein-powder",
        "variant": "400g Jar",
        "price": 799.0,
        "mrp": 1099.0,
        "net": 400.0,
        "serv": 36.0,
        "label": "1 scoop (36g)",
        "n": [136.0, 15.0, 15.5, 1.5, 0.8, 0.0, 22.0, 1.2, 2.0, 0.0, 75.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Maltodextrin, Alkalized Cocoa Powder, Ashwagandha, Brahmi, DHA, 26 Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Formulated specifically for growing teenagers with 15g whey & milk protein, DHA, Brahmi, Calcium, and 26 essential vitamins and minerals per 36g scoop.",
        "protein_source": "Whey Protein Concentrate & Milk Solids",
        "protein_tier": "tier_1",
    },
    427: {
        "source_stem": "nakpro-gen-nxt-protein-shake-mix-chocolate",
        "cat": "adult-nutrition",
        "brand": "Nakpro",
        "name": "GEN-NXT Protein Shake Mix with DHA Double Rich Chocolate",
        "url": "https://nakpro.com/products/nakpro-gen-nxt-protein-shake-mix-with-protein-dha-vitamins-minerals",
        "variant": "400g Jar",
        "price": 799.0,
        "mrp": 1099.0,
        "net": 400.0,
        "serv": 35.0,
        "label": "1 scoop (35g)",
        "n": [132.0, 14.0, 15.5, 1.5, 0.8, 0.0, 20.0, 1.2, 2.0, 0.0, 72.0],
        "ing": "Whey Protein Concentrate, Milk Solids, Oats Flour, Cocoa Powder, Algal DHA, Prebiotic Fiber, Vitamin D3, Calcium, Iron, Zinc, Sucralose",
        "allergens": ["Milk", "Gluten"],
        "tags": ["Vegetarian", "No Added Sugar"],
        "desc": "Daily nutritional protein shake mix delivering 14g protein, algal DHA for cognitive support, and essential micronutrients per 35g serving in Double Rich Chocolate.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_1",
    },
    550: {
        "source_stem": "pentasure-hp-whey-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "HP High Protein Clinical Whey Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-hp-whey-protein-chocolate-flavour-400gm",
        "variant": "400g Tin",
        "price": 1317.0,
        "mrp": 1480.0,
        "net": 400.0,
        "serv": 30.0,
        "label": "2 scoops (30g)",
        "n": [114.0, 12.6, 13.5, 1.0, 0.4, 0.0, 8.0, 1.2, 1.0, 0.0, 62.0],
        "ing": "100% Whey Protein Concentrate, Maltodextrin, Cocoa Powder, Alpha Lipoic Acid, Taurine, L-Carnitine, Inositol, 28 Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Clinical high-protein 100% whey nutritional supplement in Chocolate flavor providing 12.6g whey protein (42% protein density) per 30g serving for post-surgical and muscle recovery.",
        "protein_source": "100% Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    551: {
        "source_stem": "pentasure-2-0-high-protein-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "2.0 High Protein High Calorie Clinical Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/weight-gain-powder-weight-gainer-protein-pentasure-2-0-400g",
        "variant": "400g Tin",
        "price": 1828.0,
        "mrp": 2050.0,
        "net": 400.0,
        "serv": 54.0,
        "label": "4 scoops (54g)",
        "n": [254.0, 13.0, 26.0, 10.8, 3.5, 0.0, 12.0, 1.5, 2.5, 0.0, 110.0],
        "ing": "Whey Protein Concentrate, Calcium Caseinate, Medium Chain Triglycerides (MCT Oil), High Oleic Vegetable Oils, Maltodextrin, L-Carnitine, Taurine, Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Calorically dense (2 kcal/ml) high-protein clinical formula in Vanilla flavor delivering 254 kcal, 13g whey & casein protein, and MCTs per 54g serving for cachexia and critical recovery.",
        "protein_source": "Whey Protein & Calcium Caseinate",
        "protein_tier": "tier_1",
    },
    552: {
        "source_stem": "pentasure-2-0-high-protein-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "2.0 High Protein High Calorie Clinical Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-2-0-high-protein-high-calorie-weight-gainer-chocolate-flavour-400gm",
        "variant": "400g Tin",
        "price": 1626.0,
        "mrp": 1850.0,
        "net": 400.0,
        "serv": 54.0,
        "label": "4 scoops (54g)",
        "n": [254.0, 13.0, 26.0, 10.8, 3.5, 0.0, 12.0, 1.6, 2.5, 0.0, 112.0],
        "ing": "Whey Protein Concentrate, Calcium Caseinate, Medium Chain Triglycerides (MCT Oil), Cocoa Powder, High Oleic Vegetable Oils, Maltodextrin, L-Carnitine, Taurine, Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "High-calorie (2 kcal/ml), high-protein clinical nutrition in Chocolate flavor providing 254 kcal and 13g protein with MCTs per 54g serving for lean mass restoration.",
        "protein_source": "Whey Protein & Calcium Caseinate",
        "protein_tier": "tier_1",
    },
    553: {
        "source_stem": "pentasure-critipep-whey-peptide-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Critipep 100% Whey Peptide Critical Care Nutrition Creamy Vanilla",
        "url": "https://pentasurenutrition.com/products/100-whey-peptide-pentasure-critipep",
        "variant": "400g Tin",
        "price": 1742.0,
        "mrp": 1950.0,
        "net": 400.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [222.0, 10.5, 29.0, 7.2, 3.8, 0.0, 10.0, 1.0, 2.0, 0.0, 105.0],
        "ing": "100% Enzymatically Hydrolyzed Whey Peptides, Medium Chain Triglycerides (70% of Fat as MCT), Maltodextrin, L-Glutamine, Taurine, L-Carnitine, 28 Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Semi-elemental critical care formula with 100% hydrolyzed whey peptides and 70% MCT fat, providing 10.5g rapidly absorbed protein per 50g serving for GI-compromised patients.",
        "protein_source": "100% Hydrolyzed Whey Peptides",
        "protein_tier": "tier_1",
    },
    556: {
        "source_stem": "pentasure-dm-diabetes-care-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "DM Diabetes Care High Protein Low GI Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-dm-diabetes-care-nutrition-drink-chocolate-flavor-400-gm",
        "variant": "400g Tin",
        "price": 1159.0,
        "mrp": 1300.0,
        "net": 400.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [212.0, 11.5, 24.0, 7.8, 1.2, 0.0, 6.0, 5.5, 1.0, 0.0, 110.0],
        "ing": "3P Protein Matrix (Whey Protein Concentrate, Calcium Caseinate, Soy Protein Isolate), Isomaltulose (Low-GI Carbohydrate), Cocoa Powder, Soluble Corn Fiber, MUFA-Rich Sunflower Oil, Alpha Lipoic Acid, Taurine, Inositol, Chromium Picolinate",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Low-GI"],
        "desc": "Zero-maltodextrin, zero-sucrose diabetic nutrition in Chocolate flavor featuring a 3P Protein Matrix (11.5g protein per 50g), slow-release Isomaltulose, and 5.5g fiber for glycemic control.",
        "protein_source": "Whey, Casein & Soy 3P Matrix",
        "protein_tier": "tier_1",
    },
    557: {
        "source_stem": "pentasure-hepatic-liver-care-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Hepatic Liver Care Nutrition with BCAA & MCT Vanilla",
        "url": "https://pentasurenutrition.com/products/pentasure-hepatic-nutrition-for-liver-care",
        "variant": "400g Tin",
        "price": 1172.0,
        "mrp": 1320.0,
        "net": 400.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [208.0, 9.5, 33.0, 4.2, 2.5, 0.0, 4.0, 1.5, 2.0, 0.0, 55.0],
        "ing": "Branched-Chain Amino Acids (L-Leucine, L-Isoleucine, L-Valine), Whey Protein Isolate, Soy Protein Isolate, Medium Chain Triglycerides (MCT), Maltodextrin, Essential Vitamins & Trace Minerals",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Specialized hepatic nutrition enriched with high Branched-Chain Amino Acids (BCAAs) and MCTs, delivering 9.5g protein per 50g serving to support protein synthesis in chronic liver care.",
        "protein_source": "BCAA-Enriched Whey & Soy Isolate",
        "protein_tier": "tier_1",
    },
    558: {
        "source_stem": "threptin-protein-powder-chocolate",
        "cat": "adult-nutrition",
        "brand": "Threptin",
        "name": "Micromix High Protein Casein Supplement Powder Chocolate",
        "url": "https://threptin.com/products/threptin-protein-powder-chocolate",
        "variant": "200g Tin",
        "price": 417.0,
        "mrp": 450.0,
        "net": 200.0,
        "serv": 30.0,
        "label": "2 tablespoons (30g)",
        "n": [112.0, 9.0, 16.5, 1.0, 0.5, 0.0, 6.0, 0.6, 4.5, 3.0, 80.0],
        "ing": "Casein (Milk Protein), Maltodextrin, Sucrose, Cocoa Powder, Minerals (Calcium, Iron, Zinc, Phosphorus), Vitamins (B1, B2, B6, B12, Niacinamide, Folic Acid, Vitamin D)",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "High-biological-value casein protein supplement powder in Chocolate flavor delivering 9g slow-digesting dairy protein and B-complex vitamins per 30g serving for daily adult recovery.",
        "protein_source": "Milk Casein Protein",
        "protein_tier": "tier_1",
    },
    559: {
        "source_stem": "pentasure-obesigo-meal-replacement-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Vanilla",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-vanilla",
        "variant": "350g Box (7 x 50g Sachets)",
        "price": 1143.0,
        "mrp": 1295.0,
        "net": 350.0,
        "serv": 50.0,
        "label": "1 sachet (50g)",
        "n": [192.0, 16.5, 22.0, 4.2, 0.8, 0.0, 8.0, 6.0, 1.5, 0.0, 125.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Pea Protein Isolate, Polydextrose & Oat Fiber, Garcinia Cambogia Extract, Green Tea Extract, L-Carnitine, 27 Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Calorie-controlled medical meal replacement shake in Vanilla flavor delivering 16.5g protein, 6g satiety fiber, L-Carnitine, and only 192 kcal per 50g sachet.",
        "protein_source": "Whey, Milk & Pea Protein Blend",
        "protein_tier": "tier_1",
    },
    560: {
        "source_stem": "pentasure-obesigo-meal-replacement-chocolate",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Chocolate",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-chocolate",
        "variant": "350g Box (7 x 50g Sachets)",
        "price": 1040.0,
        "mrp": 1295.0,
        "net": 350.0,
        "serv": 50.0,
        "label": "1 sachet (50g)",
        "n": [192.0, 16.5, 22.0, 4.2, 0.8, 0.0, 8.0, 6.2, 1.5, 0.0, 128.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Pea Protein Isolate, Alkalized Cocoa Powder, Polydextrose & Oat Fiber, Garcinia Cambogia Extract, Green Tea Extract, L-Carnitine, 27 Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Calorie-controlled Chocolate meal replacement shake packing 16.5g protein, 6.2g fiber, L-Carnitine, and 27 micronutrients in 192 kcal per 50g sachet.",
        "protein_source": "Whey, Milk & Pea Protein Blend",
        "protein_tier": "tier_1",
    },
    561: {
        "source_stem": "pentasure-obesigo-meal-replacement-mango",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Mango",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-mango",
        "variant": "350g Box (7 x 50g Sachets)",
        "price": 1040.0,
        "mrp": 1295.0,
        "net": 350.0,
        "serv": 50.0,
        "label": "1 sachet (50g)",
        "n": [192.0, 16.5, 22.0, 4.2, 0.8, 0.0, 8.0, 6.0, 1.5, 0.0, 125.0],
        "ing": "Whey Protein Concentrate, Skimmed Milk Powder, Pea Protein Isolate, Natural Mango Powder, Polydextrose & Oat Fiber, Garcinia Cambogia Extract, Green Tea Extract, L-Carnitine, 27 Vitamins & Minerals",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Mango-flavored low-calorie meal replacement shake formulated with 16.5g protein, 6g soluble fiber, L-Carnitine, and 27 vitamins and minerals per 50g sachet.",
        "protein_source": "Whey, Milk & Pea Protein Blend",
        "protein_tier": "tier_1",
    },
    562: {
        "source_stem": "threptin-protein-powder-vanilla",
        "cat": "adult-nutrition",
        "brand": "Threptin",
        "name": "Micromix High Protein Casein Supplement Powder Vanilla",
        "url": "https://threptin.com/products/threptin-protein-powder-vanilla",
        "variant": "200g Tin",
        "price": 417.0,
        "mrp": 450.0,
        "net": 200.0,
        "serv": 30.0,
        "label": "2 tablespoons (30g)",
        "n": [112.0, 9.0, 16.5, 1.0, 0.5, 0.0, 6.0, 0.5, 4.5, 3.0, 80.0],
        "ing": "Casein (Milk Protein), Maltodextrin, Sucrose, Minerals (Calcium, Iron, Zinc, Phosphorus), Vitamins (B1, B2, B6, B12, Niacinamide, Folic Acid, Vitamin D), Vanilla Flavor",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "High-biological-value casein protein supplement powder in Vanilla flavor delivering 9g slow-digesting dairy protein and B-complex vitamins per 30g serving for convalescence.",
        "protein_source": "Milk Casein Protein",
        "protein_tier": "tier_1",
    },
    563: {
        "source_stem": "threptin-high-protein-diskettes-vanilla",
        "cat": "adult-nutrition",
        "brand": "Threptin",
        "name": "High Protein Casein Diskettes Vanilla",
        "url": "https://threptin.com/products/threptin-protein-diskettes-vanilla",
        "variant": "275g Tin",
        "price": 453.5,
        "mrp": 485.0,
        "net": 275.0,
        "serv": 30.0,
        "label": "6 diskettes (30g)",
        "n": [128.0, 9.0, 14.5, 3.8, 2.2, 0.0, 12.0, 0.4, 5.5, 4.5, 95.0],
        "ing": "Casein (Milk Protein 30%), Sucrose, Refined Wheat Flour, Hydrogenated Vegetable Fat, Sodium Bicarbonate, B-Complex Vitamins (Thiamine, Riboflavin, Nicotinamide), Vanilla Flavor",
        "allergens": ["Milk", "Wheat", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "Iconic ready-to-eat Vanilla casein protein diskettes providing 9g first-class milk casein protein (30% protein density) and B-vitamins per 30g serving.",
        "protein_source": "Milk Casein Protein",
        "protein_tier": "tier_1",
    },
    564: {
        "source_stem": "threptin-high-protein-diskettes-chocolate",
        "cat": "adult-nutrition",
        "brand": "Threptin",
        "name": "High Protein Casein Diskettes Chocolate",
        "url": "https://threptin.com/products/threptin-protein-diskettes-chocolate",
        "variant": "275g Tin",
        "price": 453.5,
        "mrp": 485.0,
        "net": 275.0,
        "serv": 30.0,
        "label": "6 diskettes (30g)",
        "n": [128.0, 9.0, 14.5, 3.8, 2.2, 0.0, 12.0, 0.6, 5.5, 4.5, 95.0],
        "ing": "Casein (Milk Protein 30%), Sucrose, Refined Wheat Flour, Cocoa Powder, Vegetable Fat, Sodium Bicarbonate, B-Complex Vitamins (B1, B2, B3)",
        "allergens": ["Milk", "Wheat", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "Ready-to-eat Chocolate high-protein diskettes packing 9g slow-release casein dairy protein per 30g serving for convenient mid-meal medical nutrition.",
        "protein_source": "Milk Casein Protein",
        "protein_tier": "tier_1",
    },
    565: {
        "source_stem": "threptin-lite-diskettes-sugar-free",
        "cat": "adult-nutrition",
        "brand": "Threptin",
        "name": "Lite Sugar-Free High Protein Diskettes Vanilla",
        "url": "https://threptin.com/products/threptin-lite-diskettes",
        "variant": "275g Tin",
        "price": 478.0,
        "mrp": 510.0,
        "net": 275.0,
        "serv": 30.0,
        "label": "6 diskettes (30g)",
        "n": [118.0, 9.0, 13.0, 3.4, 1.9, 0.0, 10.0, 1.2, 0.5, 0.0, 90.0],
        "ing": "Casein (Milk Protein 30%), Whole Wheat Flour, Maltitol, Polydextrose, Edible Vegetable Oil, Soy Protein Isolate, Dietary Fiber, Antioxidants, Sucralose, B-Vitamins",
        "allergens": ["Milk", "Wheat", "Gluten", "Soy"],
        "tags": ["Vegetarian", "No Added Sugar", "Low-GI"],
        "desc": "Sucrose-free diabetic-friendly high-protein casein diskettes delivering 9g protein per 30g serving with zero added sugar and added dietary fiber.",
        "protein_source": "Casein & Soy Protein",
        "protein_tier": "tier_1",
    },
    566: {
        "source_stem": "pentasure-hp-whey-banana-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "HP High Protein Clinical Whey Nutrition Banana Vanilla",
        "url": "https://pentasurenutrition.com/products/whey-protein-powder-best-whey-protein-in-india-pentasure-hp-400gm",
        "variant": "400g Tin",
        "price": 1318.0,
        "mrp": 1480.0,
        "net": 400.0,
        "serv": 30.0,
        "label": "2 scoops (30g)",
        "n": [114.0, 12.6, 13.5, 1.0, 0.4, 0.0, 8.0, 1.0, 1.0, 0.0, 60.0],
        "ing": "100% Whey Protein Concentrate, Maltodextrin, Alpha Lipoic Acid, Taurine, L-Carnitine, Inositol, 28 Vitamins & Minerals, Banana Vanilla Flavor, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Clinical high-protein 100% whey supplement in Banana Vanilla flavor providing 12.6g protein (42% density), Alpha Lipoic Acid, and 28 micronutrients per 30g serving.",
        "protein_source": "100% Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    567: {
        "source_stem": "pentasure-dm-diabetes-care-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "DM Diabetes Care High Protein Low GI Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/pentasure-dm-diabetes-care-nutrition-drink-vanilla-flavor-400-gm",
        "variant": "400g Tin",
        "price": 1126.0,
        "mrp": 1265.0,
        "net": 400.0,
        "serv": 50.0,
        "label": "4 scoops (50g)",
        "n": [212.0, 11.5, 24.0, 7.8, 1.2, 0.0, 6.0, 5.5, 1.0, 0.0, 110.0],
        "ing": "3P Protein Matrix (Whey Protein Concentrate, Calcium Caseinate, Soy Protein Isolate), Isomaltulose (Low-GI Carbohydrate), Soluble Fiber, High-MUFA Sunflower Oil, Alpha Lipoic Acid, Taurine, Inositol, Chromium",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Low-GI"],
        "desc": "Clinically formulated Vanilla diabetic nutrition shake with 11.5g 3P Protein, low-GI Isomaltulose, 5.5g fiber, and Alpha Lipoic Acid per 50g serving for blood glucose management.",
        "protein_source": "Whey, Casein & Soy 3P Matrix",
        "protein_tier": "tier_1",
    },
    568: {
        "source_stem": "pentasure-renal-pre-dialysis-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "Renal Pre-Dialysis Kidney Care Nutrition Creamy Vanilla",
        "url": "https://pentasurenutrition.com/products/renal-powder-renal-care-pentasure-renal",
        "variant": "400g Tin",
        "price": 1148.0,
        "mrp": 1290.0,
        "net": 400.0,
        "serv": 45.0,
        "label": "4 scoops (45g)",
        "n": [204.0, 5.0, 29.0, 7.5, 1.5, 0.0, 5.0, 1.5, 1.5, 0.0, 45.0],
        "ing": "High Biological Value Whey Protein Concentrate, Maltodextrin, High Oleic Sunflower Oil, Medium Chain Triglycerides (MCT), L-Carnitine, Taurine, Low-Electrolyte Renal Vitamin & Mineral Blend",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Specialized pre-dialysis renal care nutrition with controlled protein (5.0g per 45g serving = 11.1% density) and restricted potassium, phosphorus, and sodium.",
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    569: {
        "source_stem": "pentasure-dls-dialysis-care-vanilla",
        "cat": "adult-nutrition",
        "brand": "PentaSure",
        "name": "DLS Dialysis Care High Protein Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/dialysis-powder-dialysis-supplement-pentasure-dls",
        "variant": "400g Tin",
        "price": 1385.0,
        "mrp": 1550.0,
        "net": 400.0,
        "serv": 54.0,
        "label": "4 scoops (54g)",
        "n": [248.0, 12.5, 27.5, 9.8, 2.2, 0.0, 10.0, 1.5, 1.5, 0.0, 60.0],
        "ing": "Whey Protein Concentrate, Calcium Caseinate, High Oleic Sunflower Oil, Medium Chain Triglycerides (MCT), Maltodextrin, L-Carnitine, Taurine, Low-Phosphorus & Low-Potassium Vitamin-Mineral Premix",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "High-protein, low-electrolyte clinical nutrition specifically designed for dialysis patients, delivering 12.5g high-biological-value dairy protein and 248 kcal per 54g serving.",
        "protein_source": "Whey Protein & Calcium Caseinate",
        "protein_tier": "tier_1",
    },
}

uploaded_urls = {}
BATCH6_RECORDS = {}

for idx, spec in BATCH6_SPEC.items():
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
    BATCH6_RECORDS[idx] = ("manual", target_slug, spec["cat"], brand, manual_obj, reading_obj)

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

    if old_idx in BATCH6_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH6_RECORDS[old_idx]
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

for _, (_, handle, _, _, manual_obj, _) in BATCH6_RECORDS.items():
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

(ROOT / "protein-etl" / "scratch" / "batch6_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8",
)
(ROOT / "protein-etl" / "scratch" / "batch6_active_slugs.json").write_text(
    json.dumps(sorted(uploaded_urls.keys()), indent=2),
    encoding="utf-8",
)
