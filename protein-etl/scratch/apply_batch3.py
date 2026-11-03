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

IMG_DIR = ROOT / "protein-etl" / "scratch" / "batch3_images"
HERE = ROOT / "protein-etl" / "data" / "demo_catalog"

# Duplicate gainer lines to remove (1-based index in current picks.txt/readings.jsonl)
DUPLICATE_INDICES_TO_REMOVE = {
    505,  # labrada-muscle-mass-gainer-chocolate (duplicates i=377 labrada-muscle-mass-gainer)
    510,  # dymatize-super-mass-gainer-rich-chocolate (duplicates i=509)
}

BATCH3_SPEC = {
    375: {
        "source_stem": "bigmuscles-mass-forge-rich-chocolate",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Mass Forge High Calorie Mass Gainer Rich Chocolate",
        "url": "https://bigmusclesnutrition.com/products/mass-forge",
        "variant": "2.7kg Tub",
        "price": 3999.0,
        "mrp": 3999.0,
        "net": 2700.0,
        "serv": 200.0,
        "label": "2 scoops (200g)",
        "n": [810.0, 30.0, 150.0, 10.0, 3.5, 0.0, 35.0, 4.0, 12.0, 8.0, 210.0],
        "ing": "Complex Carbohydrate Matrix (Maltodextrin, Waxy Maize), Protein Blend (Whey Protein Concentrate, Milk Protein Concentrate), Alkalized Cocoa Powder, Creatine Monohydrate, L-Glutamine, Digestive Enzymes, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie muscle mass gainer delivering 810 kcal, 30g protein, and 150g carbohydrates per 200g serving in Rich Chocolate flavor.",
        "protein_source": "Whey & Milk Protein Concentrate",
        "protein_tier": "tier_2",
    },
    377: {
        "source_stem": "labrada-muscle-mass-gainer",
        "cat": "mass-gainers",
        "brand": "Labrada",
        "name": "Muscle Mass Gainer Chocolate",
        "url": "https://www.labradanutrition.in/products/best-muscle-mass-gainer",
        "variant": "3kg (6.6 lb) Pouch",
        "price": 3499.0,
        "mrp": 4699.0,
        "net": 3000.0,
        "serv": 333.0,
        "label": "9 scoops (333g)",
        "n": [1244.0, 52.0, 250.0, 4.0, 2.0, 0.0, 65.0, 5.0, 15.0, 10.0, 420.0],
        "ing": "Maltodextrin, Cross-Flow Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate, Cocoa Powder, Creatine Monohydrate, L-Glutamine, Vitamin & Mineral Blend, Sucralose, Acesulfame Potassium",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "High-calorie bodybuilding shake fortified with 52g protein, 250g carbs, 1244 kcal, creatine monohydrate, and L-glutamine per full 333g serving.",
        "protein_source": "Whey & Milk Protein Isolate/Concentrate",
        "protein_tier": "tier_1",
    },
    465: {
        "source_stem": "bigmuscles-mass-forge-malai-kulfi",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Mass Forge High Calorie Mass Gainer Cookie & Creme",
        "url": "https://bigmusclesnutrition.com/products/mass-forge",
        "variant": "2.7kg Tub",
        "price": 3999.0,
        "mrp": 3999.0,
        "net": 2700.0,
        "serv": 200.0,
        "label": "2 scoops (200g)",
        "n": [810.0, 30.0, 150.0, 10.0, 3.5, 0.0, 35.0, 4.0, 12.0, 8.0, 210.0],
        "ing": "Complex Carbohydrate Matrix (Maltodextrin, Waxy Maize), Protein Blend (Whey Protein Concentrate, Milk Protein Concentrate), Cookie Crumb Pieces, Creatine Monohydrate, L-Glutamine, Digestive Enzymes, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie muscle mass gainer delivering 810 kcal, 30g protein, and 150g carbohydrates per 200g serving in Cookie & Creme flavor.",
        "protein_source": "Whey & Milk Protein Concentrate",
        "protein_tier": "tier_2",
    },
    506: {
        "source_stem": "labrada-muscle-mass-gainer-vanilla",
        "cat": "mass-gainers",
        "brand": "Labrada",
        "name": "Muscle Mass Gainer Vanilla",
        "url": "https://www.labradanutrition.in/products/best-muscle-mass-gainer",
        "variant": "3kg (6.6 lb) Pouch",
        "price": 3499.0,
        "mrp": 4699.0,
        "net": 3000.0,
        "serv": 333.0,
        "label": "9 scoops (333g)",
        "n": [1235.0, 52.0, 250.0, 3.0, 1.5, 0.0, 60.0, 3.0, 14.0, 9.0, 390.0],
        "ing": "Maltodextrin, Cross-Flow Ultrafiltered Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate, Natural & Artificial Vanilla Flavor, Creatine Monohydrate, L-Glutamine, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "All-in-one high-calorie Vanilla mass gainer delivering 1235 kcal, 52g protein, 250g carbohydrates, creatine, and L-glutamine with no dextrose or sucrose.",
        "protein_source": "Whey & Milk Protein Isolate/Concentrate",
        "protein_tier": "tier_1",
    },
    507: {
        "source_stem": "labrada-muscle-mass-gainer-mocha",
        "cat": "mass-gainers",
        "brand": "Labrada",
        "name": "Muscle Mass Gainer Mocha",
        "url": "https://www.labradanutrition.in/products/best-muscle-mass-gainer",
        "variant": "1kg (2.2 lb) Tub",
        "price": 1349.0,
        "mrp": 1799.0,
        "net": 1000.0,
        "serv": 333.0,
        "label": "9 scoops (333g)",
        "n": [1272.0, 53.0, 257.0, 3.5, 1.8, 0.0, 60.0, 4.0, 15.0, 10.0, 410.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Milk Protein Isolate, Whey Protein Isolate, Coffee & Cocoa Solids, Creatine Monohydrate, L-Glutamine, Vitamin & Mineral Blend, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Rich Café Mocha high-calorie muscle mass gainer packing 1272 kcal, 53g protein, and 257g complex carbs per full serving.",
        "protein_source": "Whey & Milk Protein Isolate/Concentrate",
        "protein_tier": "tier_1",
    },
    508: {
        "source_stem": "labrada-super-mass-gainer-chocolate-ice-cream",
        "cat": "mass-gainers",
        "brand": "Labrada",
        "name": "Super Mass Gainer Chocolate Ice Cream",
        "url": "https://www.labradanutrition.in/products/super-mass-gainer",
        "variant": "1kg (2.2 lb) Tub",
        "price": 999.0,
        "mrp": 1699.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [376.0, 15.0, 74.0, 2.2, 1.2, 0.0, 25.0, 2.0, 6.0, 4.0, 140.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Skimmed Milk Powder, Alkalized Cocoa Powder, Creatine Monohydrate, Digestive Enzymes, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Balanced 1:5 protein-to-carbohydrate mass gainer in Chocolate Ice Cream flavor providing 15g protein and 74g carbs per 100g serving.",
        "protein_source": "Whey Protein Concentrate & Milk Solids",
        "protein_tier": "tier_2",
    },
    509: {
        "source_stem": "labrada-super-mass-gainer-malai-kulfi",
        "cat": "mass-gainers",
        "brand": "Labrada",
        "name": "Super Mass Gainer Malai Kulfi",
        "url": "https://www.labradanutrition.in/products/super-mass-gainer",
        "variant": "1kg (2.2 lb) Tub",
        "price": 999.0,
        "mrp": 1699.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [378.0, 15.0, 75.0, 2.0, 1.0, 0.0, 25.0, 1.5, 6.0, 4.0, 135.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Skimmed Milk Powder, Cardamom & Saffron (Malai Kulfi) Flavor, Creatine Monohydrate, Digestive Enzymes, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Indian Malai Kulfi flavored mass gainer delivering 15g protein, 75g complex carbs, and digestive enzymes per 100g serving.",
        "protein_source": "Whey Protein Concentrate & Milk Solids",
        "protein_tier": "tier_2",
    },
    511: {
        "source_stem": "bigmuscles-smart-gainer-chocolate-eclair",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Smart Gainer Chocolate Eclair",
        "url": "https://bigmusclesnutrition.com/products/smart-gainer",
        "variant": "1kg Tub",
        "price": 1149.0,
        "mrp": 1149.0,
        "net": 1000.0,
        "serv": 200.0,
        "label": "3 scoops (200g)",
        "n": [748.0, 30.0, 150.0, 3.0, 1.5, 0.0, 25.0, 3.5, 10.0, 6.0, 180.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, Creatine Monohydrate (3g), Cocoa Powder, Chocolate Eclair Flavor, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian"],
        "desc": "High-protein carb & creatine blend delivering 30g protein, 150g carbs, and 3g creatine per 200g serving in Chocolate Eclair flavor.",
        "protein_source": "Whey Protein Concentrate & Soy Isolate",
        "protein_tier": "tier_2",
    },
    512: {
        "source_stem": "bigmuscles-smart-gainer-cookies-cream",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Smart Gainer Cookie & Cream",
        "url": "https://bigmusclesnutrition.com/products/smart-gainer",
        "variant": "1kg Tub",
        "price": 1149.0,
        "mrp": 1149.0,
        "net": 1000.0,
        "serv": 200.0,
        "label": "3 scoops (200g)",
        "n": [748.0, 30.0, 150.0, 3.0, 1.5, 0.0, 25.0, 3.0, 10.0, 6.0, 180.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, Creatine Monohydrate (3g), Cookie Crumbs, Natural & Artificial Flavors, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "Smart Gainer mass-building formula packing 30g protein, 150g carbohydrates, and 3g creatine per 200g serving in Cookie & Cream flavor.",
        "protein_source": "Whey Protein Concentrate & Soy Isolate",
        "protein_tier": "tier_2",
    },
    513: {
        "source_stem": "bigmuscles-smart-gainer-malai-kulfi",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Smart Gainer Malai Kulfi",
        "url": "https://bigmusclesnutrition.com/products/smart-gainer",
        "variant": "1kg Tub",
        "price": 1149.0,
        "mrp": 1149.0,
        "net": 1000.0,
        "serv": 200.0,
        "label": "3 scoops (200g)",
        "n": [748.0, 30.0, 150.0, 3.0, 1.5, 0.0, 25.0, 3.0, 10.0, 6.0, 175.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, Creatine Monohydrate (3g), Cardamom & Pistachio Flavor, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie Malai Kulfi mass gainer delivering 30g protein, 150g complex carbs, and 3g creatine per 200g serving.",
        "protein_source": "Whey Protein Concentrate & Soy Isolate",
        "protein_tier": "tier_2",
    },
    514: {
        "source_stem": "bigmuscles-xtreme-muscle-fusion-chocolate-eclair",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Xtreme Muscle Fusion Chocolate Eclair",
        "url": "https://bigmusclesnutrition.com/products/xtreme-muscle-fusion",
        "variant": "1kg Tub",
        "price": 1649.0,
        "mrp": 1649.0,
        "net": 1000.0,
        "serv": 150.0,
        "label": "3 scoops (150g)",
        "n": [565.0, 50.0, 84.0, 3.2, 1.5, 0.0, 35.0, 3.0, 0.0, 0.0, 195.0],
        "ing": "Whey Protein Concentrate, Milk Protein Isolate, Complex Carbohydrates, Creatine Monohydrate (3g), Cocoa Solids, Chocolate Eclair Flavor, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "No Added Sugar"],
        "desc": "High-protein lean mass fusion formula delivering 50g protein, 3g creatine, and zero added sugar per 150g serving in Chocolate Eclair flavor.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_2",
    },
    515: {
        "source_stem": "bigmuscles-xtreme-muscle-fusion-cookies-cream",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Xtreme Muscle Fusion Cookie & Cream",
        "url": "https://bigmusclesnutrition.com/products/xtreme-muscle-fusion",
        "variant": "1kg Tub",
        "price": 1649.0,
        "mrp": 1649.0,
        "net": 1000.0,
        "serv": 150.0,
        "label": "3 scoops (150g)",
        "n": [565.0, 50.0, 84.0, 3.2, 1.5, 0.0, 35.0, 2.5, 0.0, 0.0, 190.0],
        "ing": "Whey Protein Concentrate, Milk Protein Isolate, Complex Carbohydrates, Creatine Monohydrate (3g), Cookie Crumb Pieces, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian", "No Added Sugar"],
        "desc": "Lean mass gainer matrix packing 50g protein, 3g creatine, and zero added sugar per 150g serving in Cookie & Cream flavor.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_2",
    },
    516: {
        "source_stem": "bigmuscles-xtreme-muscle-fusion-malai-kulfi",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Xtreme Muscle Fusion Malai Kulfi",
        "url": "https://bigmusclesnutrition.com/products/xtreme-muscle-fusion",
        "variant": "1kg Tub",
        "price": 1649.0,
        "mrp": 1649.0,
        "net": 1000.0,
        "serv": 150.0,
        "label": "3 scoops (150g)",
        "n": [565.0, 50.0, 84.0, 3.2, 1.5, 0.0, 35.0, 2.5, 0.0, 0.0, 185.0],
        "ing": "Whey Protein Concentrate, Milk Protein Isolate, Complex Carbohydrates, Creatine Monohydrate (3g), Cardamom & Saffron Flavor, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "No Added Sugar"],
        "desc": "High-protein lean mass builder providing 50g protein and 3g creatine with zero added sugar in Malai Kulfi flavor.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_2",
    },
    517: {
        "source_stem": "bigmuscles-body-fuel-hardcore-chocolate-eclair",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Body Fuel Hardcore Mass Gainer Chocolate Eclair",
        "url": "https://bigmusclesnutrition.com/products/body-fuel-hardcore-2",
        "variant": "1kg Tub",
        "price": 1449.0,
        "mrp": 1449.0,
        "net": 1000.0,
        "serv": 200.0,
        "label": "3 scoops (200g)",
        "n": [748.0, 40.0, 140.0, 3.0, 1.5, 0.0, 25.0, 3.5, 8.0, 5.0, 195.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Calcium Caseinate, Soy Protein Isolate, Creatine Monohydrate (3g), Cocoa Powder, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian"],
        "desc": "Hardcore muscle-building mass gainer delivering 40g multi-source protein, 140g carbs, and 3g creatine per 200g serving.",
        "protein_source": "Whey, Casein & Soy Protein",
        "protein_tier": "tier_2",
    },
    518: {
        "source_stem": "gnc-pro-performance-weight-gainer-double-chocolate",
        "cat": "mass-gainers",
        "brand": "GNC India",
        "name": "Pro Performance Weight Gainer Double Chocolate",
        "url": "https://www.guardian.in/products/gnc-pro-performance-weight-gainer-3kg-double-chocolate-1",
        "variant": "3kg Tub",
        "price": 1799.0,
        "mrp": 3399.0,
        "net": 3000.0,
        "serv": 150.0,
        "label": "3 scoops (150g)",
        "n": [560.0, 25.0, 110.0, 2.2, 1.0, 0.0, 20.0, 3.0, 9.0, 5.0, 180.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Milk Protein Concentrate, Calcium Caseinate, Cocoa Powder, Medium Chain Triglycerides (MCT), BCAAs, Digestive Enzymes, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "GNC Pro Performance Weight Gainer in Double Chocolate flavor fortified with 25g protein, 110g complex carbs, BCAAs, and digestive enzymes per 150g powder serving.",
        "protein_source": "Whey, Milk & Casein Protein",
        "protein_tier": "tier_2",
    },
    519: {
        "source_stem": "gnc-pro-performance-weight-gainer-vanilla-ice-cream",
        "cat": "mass-gainers",
        "brand": "GNC India",
        "name": "Pro Performance Weight Gainer Vanilla Ice Cream",
        "url": "https://www.guardian.in/products/gnc-pro-performance-weight-gainer-6",
        "variant": "2kg Pouch",
        "price": 1499.0,
        "mrp": 2299.0,
        "net": 2000.0,
        "serv": 150.0,
        "label": "3 scoops (150g)",
        "n": [556.0, 25.0, 110.0, 1.8, 0.9, 0.0, 20.0, 2.5, 8.5, 5.0, 175.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Milk Protein Concentrate, Calcium Caseinate, Natural & Artificial Vanilla Ice Cream Flavor, MCTs, BCAAs, Digestive Enzymes, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "GNC Pro Performance Weight Gainer in Vanilla Ice Cream flavor delivering 25g protein, 110g carbohydrates, and digestive enzymes per 150g serving.",
        "protein_source": "Whey, Milk & Casein Protein",
        "protein_tier": "tier_2",
    },
    520: {
        "source_stem": "gnc-amp-amplified-mass-xxx-chocolate",
        "cat": "mass-gainers",
        "brand": "GNC India",
        "name": "AMP Amplified Mass XXX Chocolate",
        "url": "https://www.guardian.in/products/gnc-amp-amplified-mass-xxx-l-leucine-100g",
        "variant": "2kg Tub",
        "price": 4798.0,
        "mrp": 6298.0,
        "net": 2000.0,
        "serv": 205.0,
        "label": "4 scoops (205g)",
        "n": [748.0, 50.0, 125.0, 5.5, 2.5, 0.0, 45.0, 4.0, 8.0, 4.0, 240.0],
        "ing": "Maltodextrin, Whey Protein Isolate, Whey Protein Concentrate, Micellar Casein, Creatine Monohydrate (3g), Micronized L-Leucine, L-Glutamine, Alkalized Cocoa Powder, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Advanced muscle performance mass gainer delivering 50g fast/medium/slow release protein, 125g carbs, 748 kcal, and 3g creatine per 205g serving.",
        "protein_source": "Whey Isolate, Concentrate & Micellar Casein",
        "protein_tier": "tier_1",
    },
    521: {
        "source_stem": "bigmuscles-xtreme-weight-gainer-malt-chocolate",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Xtreme Weight Gainer Cookie & Cream",
        "url": "https://bigmusclesnutrition.com/products/xtreme-weight-gainer",
        "variant": "1kg (2.2 lb) Tub",
        "price": 1299.0,
        "mrp": 1299.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [382.0, 16.0, 74.0, 2.5, 1.2, 0.0, 15.0, 2.5, 8.0, 5.0, 140.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, Skimmed Milk Powder, Cookie Crumbs, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie weight gainer formula delivering 16g protein and 74g carbohydrates per 100g serving with 22 essential vitamins and minerals.",
        "protein_source": "Whey, Soy & Milk Protein",
        "protein_tier": "tier_2",
    },
    522: {
        "source_stem": "bigmuscles-lean-gain-malt-chocolate",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Lean Gain Cookie & Cream",
        "url": "https://bigmusclesnutrition.com/products/lean-gain",
        "variant": "1kg (2.2 lb) Tub",
        "price": 1449.0,
        "mrp": 1449.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [376.0, 24.0, 64.0, 2.6, 1.2, 0.0, 20.0, 3.0, 6.0, 3.0, 150.0],
        "ing": "Complex Carbohydrates, Whey Protein Concentrate, Milk Protein Isolate, Cookie Crumb Pieces, L-Glutamine, BCAAs, Digestive Enzymes, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "Lean muscle gainer designed with a balanced 24g protein to 64g carbohydrate ratio per 100g serving to support clean muscle mass without excess fat.",
        "protein_source": "Whey & Milk Protein",
        "protein_tier": "tier_2",
    },
    523: {
        "source_stem": "optimum-nutrition-serious-mass-weight-gainer-vanilla",
        "cat": "mass-gainers",
        "brand": "Optimum Nutrition",
        "name": "Serious Mass Weight Gainer Vanilla",
        "url": "https://www.optimumnutrition.co.in/products/serious-mass-vanilla-1110151",
        "variant": "3kg (6.6 lb) Tub",
        "price": 3749.0,
        "mrp": 4399.0,
        "net": 3000.0,
        "serv": 334.0,
        "label": "2 heaped scoops (334g)",
        "n": [1249.0, 50.0, 254.0, 4.2, 2.5, 0.0, 80.0, 2.5, 20.0, 0.0, 410.0],
        "ing": "Maltodextrin, Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Egg Whites, Sweet Dairy Whey), Creatine Monohydrate (3g), L-Glutamine, Choline, Inositol, 25 Vitamins & Essential Minerals, Natural & Artificial Vanilla Flavor, Sucralose",
        "allergens": ["Milk", "Egg", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free", "Informed-Choice"],
        "desc": "Optimum Nutrition's ultimate high-calorie Vanilla weight gain formula delivering 1,249 kcal, 50g blended protein, 254g carbohydrates, 3g creatine, and 25 vitamins & minerals per serving.",
        "protein_source": "Whey, Casein & Egg White Protein",
        "protein_tier": "tier_1",
    },
    524: {
        "source_stem": "gnc-amp-amplified-mass-xxx-vanilla",
        "cat": "mass-gainers",
        "brand": "GNC India",
        "name": "AMP Amplified Mass XXX Vanilla",
        "url": "https://www.guardian.in/products/gnc-amp-amplified-mass-xxx-l-leucine-100g",
        "variant": "2kg Tub",
        "price": 4798.0,
        "mrp": 6198.0,
        "net": 2000.0,
        "serv": 205.0,
        "label": "4 scoops (205g)",
        "n": [745.0, 50.0, 125.0, 5.0, 2.2, 0.0, 45.0, 3.5, 8.0, 4.0, 235.0],
        "ing": "Maltodextrin, Whey Protein Isolate, Whey Protein Concentrate, Micellar Casein, Creatine Monohydrate (3g), Micronized L-Leucine, L-Glutamine, Natural & Artificial Vanilla Flavor, Sucralose",
        "allergens": ["Milk", "Soy"],
        "tags": ["Vegetarian", "Gluten-Free"],
        "desc": "Clinical-strength Vanilla mass gainer delivering 50g multi-phase protein, 125g carbs, 745 kcal, and 3g creatine monohydrate per 205g serving.",
        "protein_source": "Whey Isolate, Concentrate & Micellar Casein",
        "protein_tier": "tier_1",
    },
    525: {
        "source_stem": "bigmuscles-mamoth-gainer-belgian-chocolate",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Mamoth Gainer Belgian Chocolate",
        "url": "https://bigmusclesnutrition.com/products/mamoth-gainer",
        "variant": "1kg Tub",
        "price": 1549.0,
        "mrp": 1549.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [378.0, 18.0, 70.0, 2.8, 1.4, 0.0, 20.0, 3.0, 6.0, 3.0, 145.0],
        "ing": "Complex Carbohydrate Blend (Maltodextrin, Oat Flour), Whey Protein Concentrate, Milk Protein Concentrate, Creatine Monohydrate (3g), Belgian Cocoa Powder, BCAAs (4.5g), Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie Belgian Chocolate mass gainer fortified with 18g protein, 70g carbs, 3g creatine, and 4.5g BCAAs per 100g serving.",
        "protein_source": "Whey & Milk Protein Concentrate",
        "protein_tier": "tier_2",
    },
    526: {
        "source_stem": "as-it-is-atom-mass-gainer-double-rich-chocolate",
        "cat": "mass-gainers",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Mass Gainer Double Rich Chocolate",
        "url": "https://asitisnutrition.com/products/atom-mass-gainer",
        "variant": "1kg Pouch",
        "price": 677.0,
        "mrp": 985.0,
        "net": 1000.0,
        "serv": 79.0,
        "label": "2 scoops (79g)",
        "n": [315.0, 12.0, 60.0, 3.0, 1.5, 0.0, 15.0, 2.5, 0.0, 0.0, 110.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Whey Protein Isolate, Alkalized Cocoa Powder, Ashwagandha Extract, L-Glutamine, BCAAs, DigeZyme Multi-Enzyme Complex, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Labdoor/heavy-metal tested mass gainer delivering 315 kcal, 12g whey protein, and 60g complex carbs per 79g single serving with Ashwagandha, L-Glutamine, and DigeZyme enzymes.",
        "protein_source": "Whey Protein Concentrate & Isolate",
        "protein_tier": "tier_1",
    },
    527: {
        "source_stem": "as-it-is-atom-mass-gainer-mango-fusion",
        "cat": "mass-gainers",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Mass Gainer Mango Fusion",
        "url": "https://asitisnutrition.com/products/atom-mass-gainer",
        "variant": "1kg Pouch",
        "price": 677.0,
        "mrp": 985.0,
        "net": 1000.0,
        "serv": 79.0,
        "label": "2 scoops (79g)",
        "n": [315.0, 12.0, 60.0, 3.0, 1.5, 0.0, 15.0, 2.0, 0.0, 0.0, 105.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Whey Protein Isolate, Mango Fruit Powder, Ashwagandha Extract, L-Glutamine, BCAAs, DigeZyme Multi-Enzyme Complex, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Refreshing Mango Fusion mass gainer providing 315 kcal, 12g pure whey protein, and 60g complex carbs per 79g serving alongside Ashwagandha and DigeZyme enzymes.",
        "protein_source": "Whey Protein Concentrate & Isolate",
        "protein_tier": "tier_1",
    },
    528: {
        "source_stem": "as-it-is-atom-weight-gainer-double-rich-chocolate",
        "cat": "mass-gainers",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Weight Gainer Double Rich Chocolate",
        "url": "https://asitisnutrition.com/products/atom-weight-gainer",
        "variant": "1kg Pouch",
        "price": 611.0,
        "mrp": 889.0,
        "net": 1000.0,
        "serv": 75.0,
        "label": "2 scoops (75g)",
        "n": [283.0, 8.8, 61.0, 0.5, 0.2, 0.0, 5.0, 1.5, 0.0, 0.0, 95.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Alkalized Cocoa Powder, DigeZyme Multi-Enzyme Complex, Vitamin & Mineral Premix, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Low-Fat"],
        "desc": "High-carb weight gainer in Double Rich Chocolate flavor packing 283 kcal, 61g carbohydrates, and 8.8g protein per 75g serving with DigeZyme enzymes and zero added sugar.",
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    530: {
        "source_stem": "as-it-is-atom-weight-gainer-kesar-elaichi",
        "cat": "mass-gainers",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Weight Gainer Kesar Elaichi",
        "url": "https://asitisnutrition.com/products/atom-weight-gainer",
        "variant": "1kg Pouch",
        "price": 611.0,
        "mrp": 889.0,
        "net": 1000.0,
        "serv": 75.0,
        "label": "2 scoops (75g)",
        "n": [283.0, 8.8, 61.0, 0.5, 0.2, 0.0, 5.0, 1.2, 0.0, 0.0, 90.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Saffron (Kesar) & Cardamom (Elaichi) Extracts, DigeZyme Multi-Enzyme Complex, Vitamin & Mineral Premix, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar", "Low-Fat"],
        "desc": "Traditional Kesar Elaichi flavored weight gainer delivering 283 kcal, 61g carbs, and 8.8g whey protein per 75g serving with digestive enzymes.",
        "protein_source": "Whey Protein Concentrate",
        "protein_tier": "tier_1",
    },
    531: {
        "source_stem": "nakpro-perform-mass-gainer-double-rich-chocolate",
        "cat": "mass-gainers",
        "brand": "Nakpro",
        "name": "Perform Mass Gainer Double Rich Chocolate",
        "url": "https://nakpro.com/products/nakpro-perform-mass-gainers",
        "variant": "1kg Pouch",
        "price": 599.0,
        "mrp": 1290.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "3 scoops (100g)",
        "n": [384.0, 15.0, 76.0, 2.2, 1.2, 0.0, 20.0, 2.0, 0.0, 0.0, 120.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Milk Solids, Cocoa Powder, Creatine Monohydrate, MCT Powder, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Value mass gainer delivering 384 kcal, 15g protein, and 76g carbohydrates per 100g serving with 27 added vitamins and minerals in Double Rich Chocolate flavor.",
        "protein_source": "Whey Protein Concentrate & Milk Solids",
        "protein_tier": "tier_2",
    },
    532: {
        "source_stem": "nakpro-gold-mass-gainer-coffee",
        "cat": "mass-gainers",
        "brand": "Nakpro",
        "name": "Gold Mass Gainer Coffee",
        "url": "https://nakpro.com/products/nakpro-gold-mass-gainer",
        "variant": "1kg Pouch",
        "price": 699.0,
        "mrp": 1400.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "3 scoops (100g)",
        "n": [378.0, 21.0, 68.0, 2.5, 1.4, 0.0, 25.0, 2.2, 0.0, 0.0, 125.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Whey Protein Isolate, Coffee Powder, L-Glutamine, Creatine Monohydrate, Digestive Enzymes, Vitamins & Minerals, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "High-protein Coffee mass gainer packing 21g whey protein, 68g complex carbs, and 378 kcal per 100g serving with digestive enzymes and micronutrients.",
        "protein_source": "Whey Protein Concentrate & Isolate",
        "protein_tier": "tier_1",
    },
    533: {
        "source_stem": "nakpro-mr-fit-mass-gainer-chocolate",
        "cat": "mass-gainers",
        "brand": "Nakpro",
        "name": "Mr. Fit Super Fast Mass Gainer Chocolate",
        "url": "https://nakpro.com/products/nakpro-mr-fit-super-fast-mass-gainer",
        "variant": "1kg Pouch",
        "price": 499.0,
        "mrp": 1160.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "3 scoops (100g)",
        "n": [368.0, 20.0, 66.0, 2.6, 1.4, 0.0, 20.0, 2.0, 0.0, 0.0, 130.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Skimmed Milk Powder, Alkalized Cocoa Powder, Vitamins & Minerals, Digestive Enzymes, Sucralose",
        "allergens": ["Milk"],
        "tags": ["Vegetarian", "Gluten-Free", "No Added Sugar"],
        "desc": "Fast-absorbing Chocolate mass gainer delivering 20g protein and 66g carbohydrates per 100g serving fortified with vitamins, minerals, and digestive enzymes.",
        "protein_source": "Whey Protein Concentrate & Skimmed Milk",
        "protein_tier": "tier_2",
    },
    534: {
        "source_stem": "bigmuscles-quick-mass-gainer-malt-chocolate",
        "cat": "mass-gainers",
        "brand": "Bigmuscles Nutrition",
        "name": "Quick Mass Gainer Malt Chocolate",
        "url": "https://bigmusclesnutrition.com/products/quick-mass-gainer",
        "variant": "1kg (2.2 lb) Tub",
        "price": 949.0,
        "mrp": 949.0,
        "net": 1000.0,
        "serv": 100.0,
        "label": "2 scoops (100g)",
        "n": [380.0, 15.0, 74.0, 2.6, 1.2, 0.0, 15.0, 2.5, 8.0, 5.0, 140.0],
        "ing": "Maltodextrin, Whey Protein Concentrate, Soy Protein Isolate, Dairy Whey Powder, Malt Extract, Cocoa Solids, Sucralose",
        "allergens": ["Milk", "Soy", "Gluten"],
        "tags": ["Vegetarian"],
        "desc": "High-calorie Malt Chocolate weight gainer formulated with 15g protein and 74g carbohydrates per 100g serving for rapid calorie surplus.",
        "protein_source": "Whey & Soy Protein",
        "protein_tier": "tier_2",
    },
}

uploaded_urls = {}
BATCH3_RECORDS = {}

for idx, spec in BATCH3_SPEC.items():
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
    BATCH3_RECORDS[idx] = ("manual", target_slug, spec["cat"], brand, manual_obj, reading_obj)

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

    if old_idx in BATCH3_RECORDS:
        store, handle, cat, brand, manual_obj, r_override = BATCH3_RECORDS[old_idx]
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

for _, (_, handle, _, _, manual_obj, _) in BATCH3_RECORDS.items():
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

(ROOT / "protein-etl" / "scratch" / "batch3_retired_slugs.json").write_text(
    json.dumps(sorted(old_slugs_to_delete_from_supabase), indent=2),
    encoding="utf-8",
)
(ROOT / "protein-etl" / "scratch" / "batch3_active_slugs.json").write_text(
    json.dumps(sorted(uploaded_urls.keys()), indent=2),
    encoding="utf-8",
)

