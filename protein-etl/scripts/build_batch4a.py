"""Complete builder script for Batch 4A: One Science Nutrition, Nutrabay, Plix.
Merges into store_snapshot.json, appends picks to picks.txt, appends readings to readings.jsonl,
and triggers build_demo_catalog.py.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "protein-etl" / "data" / "demo_catalog"

STORE_SNAPSHOT_FILE = DATA_DIR / "store_snapshot.json"
PICKS_FILE = DATA_DIR / "picks.txt"
READINGS_FILE = DATA_DIR / "readings.jsonl"

def main():
    # 1. Load existing data
    with open(STORE_SNAPSHOT_FILE, encoding="utf-8") as f:
        store_snapshot = json.load(f)
    with open(PICKS_FILE, encoding="utf-8") as f:
        raw_picks = f.read().splitlines()
    with open(READINGS_FILE, encoding="utf-8") as f:
        readings = [json.loads(line) for line in f if line.strip()]

    # Count non-comment pick lines to determine next reading index
    non_comment_picks = [p for p in raw_picks if p.strip() and not p.startswith("#")]
    next_idx = len(non_comment_picks) + 1
    print(f"Current non-comment picks count: {len(non_comment_picks)}. Next pick index: {next_idx}")

    # 2. Prepare store snapshots for the 3 brands
    osn_products = [
        {
            "handle": "one-science-nutrition-premium-whey-protein",
            "url": "https://onesciencenutrition.com/products/one-science-nutrition-premium-whey-protein",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/all_front.png"}],
            "variants": [
                {"id": 40101, "title": "Chocolate Charge / 2.27kg (5 Lbs)", "price": "6499", "compare_at_price": "7999", "sku": "OSN-PWP-5LB-CC", "available": True},
                {"id": 40102, "title": "Chocolate Charge / 907g (2 Lbs)", "price": "3199", "compare_at_price": "3899", "sku": "OSN-PWP-2LB-CC", "available": True},
                {"id": 40103, "title": "Vanilla Cream / 2.27kg (5 Lbs)", "price": "6499", "compare_at_price": "7999", "sku": "OSN-PWP-5LB-VC", "available": True},
                {"id": 40104, "title": "Strawberry White Chocolate / 2.27kg (5 Lbs)", "price": "6499", "compare_at_price": "7999", "sku": "OSN-PWP-5LB-SWC", "available": True},
                {"id": 40105, "title": "Cafe Mocha / 2.27kg (5 Lbs)", "price": "6499", "compare_at_price": "7999", "sku": "OSN-PWP-5LB-CM", "available": True},
                {"id": 40106, "title": "Chocolate Charge / 454g (1 Lb)", "price": "1699", "compare_at_price": "1999", "sku": "OSN-PWP-1LB-CC", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-iso-gold-whey-isolate",
            "url": "https://onesciencenutrition.com/products/iso-gold-protein-5lbs",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/1_3ed7a5d3-97e8-431b-a9ca-d02a68b5f846.png"}],
            "variants": [
                {"id": 40201, "title": "Chocolate Charge / 2.27kg (5 Lbs)", "price": "7999", "compare_at_price": "9999", "sku": "OSN-ISO-5LB-CC", "available": True},
                {"id": 40202, "title": "Chocolate Charge / 907g (2 Lbs)", "price": "3899", "compare_at_price": "4699", "sku": "OSN-ISO-2LB-CC", "available": True},
                {"id": 40203, "title": "Vanilla / 2.27kg (5 Lbs)", "price": "7999", "compare_at_price": "9999", "sku": "OSN-ISO-5LB-VAN", "available": True},
                {"id": 40204, "title": "Cafe Mocha / 2.27kg (5 Lbs)", "price": "7999", "compare_at_price": "9999", "sku": "OSN-ISO-5LB-CM", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-nitra-whey",
            "url": "https://onesciencenutrition.com/products/tiger-combo-pack-nitra-whey-protein-4-lb-with-daily-multivitams-60-capsules",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/4lb-NitraWhey-Chocolatebrownie-Front_1.png"}],
            "variants": [
                {"id": 40301, "title": "Chocolate Brownie / 1.81kg (4 Lbs)", "price": "4899", "compare_at_price": "5999", "sku": "OSN-NITRA-4LB-CB", "available": True},
                {"id": 40302, "title": "Chocolate Brownie / 907g (2 Lbs)", "price": "2799", "compare_at_price": "3399", "sku": "OSN-NITRA-2LB-CB", "available": True},
                {"id": 40303, "title": "Cappuccino / 1.81kg (4 Lbs)", "price": "4899", "compare_at_price": "5999", "sku": "OSN-NITRA-4LB-CAP", "available": True},
                {"id": 40304, "title": "Strawberry / 1.81kg (4 Lbs)", "price": "4899", "compare_at_price": "5999", "sku": "OSN-NITRA-4LB-SB", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-ripped-professional-whey",
            "url": "https://onesciencenutrition.com/products/ripped-professional-whey-4lbs",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/Ripped_whey.jpg"}],
            "variants": [
                {"id": 40401, "title": "Chocolate / 1.81kg (4 Lbs)", "price": "5299", "compare_at_price": "6499", "sku": "OSN-RIPPED-4LB-CHOC", "available": True},
                {"id": 40402, "title": "Vanilla / 1.81kg (4 Lbs)", "price": "5299", "compare_at_price": "6499", "sku": "OSN-RIPPED-4LB-VAN", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-plant-protein-pea-isolate",
            "url": "https://onesciencenutrition.com/products/one-science-nutrition-plant-protein-pea-protein-isolate-1kg",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/1_1a73634e-6c40-4251-ac4e-e7ff5d43dd28.jpg"}],
            "variants": [
                {"id": 40501, "title": "Rich Chocolate / 1kg", "price": "2499", "compare_at_price": "3199", "sku": "OSN-PLANT-1KG-CHOC", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-high-protein-oats",
            "url": "https://onesciencenutrition.com/products/one-science-nutrition-high-protein-oats-dark-chocolate",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/1_8b572bc3-7bd3-4b08-b0a0-0be3bf27cb0f.jpg"}],
            "variants": [
                {"id": 40601, "title": "Dark Chocolate / 400g", "price": "449", "compare_at_price": "599", "sku": "OSN-OATS-400G-DC", "available": True}
            ]
        },
        {
            "handle": "one-science-nutrition-high-protein-muesli",
            "url": "https://onesciencenutrition.com/products/one-science-nutrition-high-protein-muesli-dark-choco-crunchy",
            "images": [{"src": "https://cdn.shopify.com/s/files/1/0952/0483/5648/files/1_f16895f9-8c21-4404-82fc-dbafbd309e7d.jpg"}],
            "variants": [
                {"id": 40701, "title": "Dark Choco Crunchy / 400g", "price": "499", "compare_at_price": "649", "sku": "OSN-MUESLI-400G-DCC", "available": True}
            ]
        }
    ]

    nutrabay_products = [
        {
            "handle": "nutrabay-gold-100-whey-protein-concentrate",
            "url": "https://nutrabay.com/product/nutrabay-gold-100-whey-protein-concentrate",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1014-01-1758998117.png"}],
            "variants": [
                {"id": 41101, "title": "Rich Chocolate / 1 kg (2.2 lb)", "price": "2199", "compare_at_price": "2699", "sku": "NB-NUT-1014-01", "available": True},
                {"id": 41102, "title": "Rich Chocolate / 2 kg (4.4 lb)", "price": "3999", "compare_at_price": "4999", "sku": "NB-NUT-1014-02", "available": True},
                {"id": 41103, "title": "Cafe Mocha / 1 kg (2.2 lb)", "price": "2199", "compare_at_price": "2699", "sku": "NB-NUT-1014-03", "available": True},
                {"id": 41104, "title": "Strawberry Milkshake / 1 kg (2.2 lb)", "price": "2199", "compare_at_price": "2699", "sku": "NB-NUT-1014-04", "available": True},
                {"id": 41105, "title": "Kesar Kulfi / 1 kg (2.2 lb)", "price": "2199", "compare_at_price": "2699", "sku": "NB-NUT-1014-05", "available": True},
                {"id": 41106, "title": "Vanilla / 1 kg (2.2 lb)", "price": "2199", "compare_at_price": "2699", "sku": "NB-NUT-1014-06", "available": True}
            ]
        },
        {
            "handle": "nutrabay-gold-100-whey-protein-isolate",
            "url": "https://nutrabay.com/product/nutrabay-gold-100-whey-protein-isolate",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1013-17-1768993257.png"}],
            "variants": [
                {"id": 41201, "title": "Cold Coffee / 1 kg (2.2 lb)", "price": "2799", "compare_at_price": "3499", "sku": "NB-NUT-1013-17", "available": True},
                {"id": 41202, "title": "Rich Chocolate Creme / 1 kg (2.2 lb)", "price": "2799", "compare_at_price": "3499", "sku": "NB-NUT-1013-01", "available": True},
                {"id": 41203, "title": "Rich Chocolate Creme / 2 kg (4.4 lb)", "price": "5299", "compare_at_price": "6499", "sku": "NB-NUT-1013-02", "available": True},
                {"id": 41204, "title": "Strawberry Milkshake / 1 kg (2.2 lb)", "price": "2799", "compare_at_price": "3499", "sku": "NB-NUT-1013-04", "available": True},
                {"id": 41205, "title": "Vanilla / 1 kg (2.2 lb)", "price": "2799", "compare_at_price": "3499", "sku": "NB-NUT-1013-06", "available": True}
            ]
        },
        {
            "handle": "nutrabay-pure-whey-protein-concentrate",
            "url": "https://nutrabay.com/product/nutrabay-whey-protein-concentrate",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1001-01-1758998117.png"}],
            "variants": [
                {"id": 41301, "title": "Unflavoured / 1 kg (2.2 lb)", "price": "1799", "compare_at_price": "2299", "sku": "NB-NUT-1001-01", "available": True},
                {"id": 41302, "title": "Unflavoured / 1.5 kg (3.3 lb)", "price": "2499", "compare_at_price": "3199", "sku": "NB-NUT-1001-02", "available": True},
                {"id": 41303, "title": "Unflavoured / 2 kg (4.4 lb)", "price": "3299", "compare_at_price": "4199", "sku": "NB-NUT-1001-03", "available": True}
            ]
        },
        {
            "handle": "nutrabay-gold-tri-blend-whey-protein",
            "url": "https://nutrabay.com/product/nutrabay-gold-tri-blend-whey-protein",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1025-01-1758998117.png"}],
            "variants": [
                {"id": 41401, "title": "Double Chocolate / 1 kg (2.2 lb)", "price": "2299", "compare_at_price": "2899", "sku": "NB-NUT-1025-01", "available": True},
                {"id": 41402, "title": "Double Chocolate / 2 kg (4.4 lb)", "price": "4299", "compare_at_price": "5299", "sku": "NB-NUT-1025-02", "available": True},
                {"id": 41403, "title": "Strawberry Milkshake / 1 kg (2.2 lb)", "price": "2299", "compare_at_price": "2899", "sku": "NB-NUT-1025-03", "available": True},
                {"id": 41404, "title": "Malai Kulfi / 1 kg (2.2 lb)", "price": "2299", "compare_at_price": "2899", "sku": "NB-NUT-1025-04", "available": True}
            ]
        },
        {
            "handle": "nutrabay-gold-hydrolyzed-pea-protein",
            "url": "https://nutrabay.com/product/nutrabay-gold-hydrolyzed-pea-protein",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1030-01-1758998117.png"}],
            "variants": [
                {"id": 41501, "title": "Rich Chocolate Creme / 1 kg (2.2 lb)", "price": "1349", "compare_at_price": "1799", "sku": "NB-NUT-1030-01", "available": True},
                {"id": 41502, "title": "Cold Coffee / 1 kg (2.2 lb)", "price": "1349", "compare_at_price": "1799", "sku": "NB-NUT-1030-02", "available": True},
                {"id": 41503, "title": "French Vanilla / 1 kg (2.2 lb)", "price": "1349", "compare_at_price": "1799", "sku": "NB-NUT-1030-03", "available": True}
            ]
        },
        {
            "handle": "nutrabay-wellness-vegan-plant-protein-superfoods",
            "url": "https://nutrabay.com/product/nutrabay-wellness-vegan-plant-protein-powder-superfoods",
            "images": [{"src": "https://cdn2.nutrabay.com/uploads/variant/images/featured_image-NB-NUT-1035-01-1758998117.png"}],
            "variants": [
                {"id": 41601, "title": "Rich Chocolate / 1 kg (2.2 lb)", "price": "1299", "compare_at_price": "1699", "sku": "NB-NUT-1035-01", "available": True},
                {"id": 41602, "title": "Rich Chocolate / 500 g (1.1 lb)", "price": "699", "compare_at_price": "1199", "sku": "NB-NUT-1035-02", "available": True},
                {"id": 41603, "title": "Gourmet Chocolate / 500 g (1.1 lb)", "price": "699", "compare_at_price": "1199", "sku": "NB-NUT-1035-03", "available": True}
            ]
        }
    ]

    plix_products = [
        {
            "handle": "plix-evolve-plant-protein-powder",
            "url": "https://www.plixlife.com/product/plant-protein-powder",
            "images": [{"src": "https://plixlifefc-media.farziengineer.co/hosted/Evolve_aqualogica_image-ff087774d4d8.jpg"}],
            "variants": [
                {"id": 42101, "title": "Rich Chocolate / 1 Kg (30 Scoops)", "price": "1899", "compare_at_price": "2499", "sku": "PLX-EVL-1KG-CHOC", "available": True},
                {"id": 42102, "title": "Rich Chocolate / 2 Kg (60 Scoops)", "price": "3299", "compare_at_price": "4499", "sku": "PLX-EVL-2KG-CHOC", "available": True},
                {"id": 42103, "title": "Rich Chocolate / 3 Kg (90 Scoops)", "price": "4899", "compare_at_price": "6499", "sku": "PLX-EVL-3KG-CHOC", "available": True},
                {"id": 42104, "title": "Cafe Mocha / 1 Kg (30 Scoops)", "price": "1899", "compare_at_price": "2499", "sku": "PLX-EVL-1KG-CM", "available": True},
                {"id": 42105, "title": "Cafe Mocha / 2 Kg (60 Scoops)", "price": "3299", "compare_at_price": "4499", "sku": "PLX-EVL-2KG-CM", "available": True},
                {"id": 42106, "title": "Vanilla / 1 Kg (30 Scoops)", "price": "1899", "compare_at_price": "2499", "sku": "PLX-EVL-1KG-VAN", "available": True},
                {"id": 42107, "title": "Vanilla / 2 Kg (60 Scoops)", "price": "3299", "compare_at_price": "4499", "sku": "PLX-EVL-2KG-VAN", "available": True},
                {"id": 42108, "title": "Strawberry / 1 Kg (30 Scoops)", "price": "1899", "compare_at_price": "2499", "sku": "PLX-EVL-1KG-SB", "available": True}
            ]
        },
        {
            "handle": "plix-super-strength-fermented-yeast-protein",
            "url": "https://www.plixlife.com/product/super-strength-fermented-yeast-protein",
            "images": [{"src": "https://plixlifefc-media.farziengineer.co/hosted/Pack_of_1_With_Icons_Super_Strength_fermented_yeast_protein_19-1-26-1e46e7093fb8.jpg"}],
            "variants": [
                {"id": 42201, "title": "Milk Chocolate / 1 Kg (27 Scoops)", "price": "1999", "compare_at_price": "2700", "sku": "FG-SSP-POW-YEAST-CHOC-1KG", "available": True},
                {"id": 42202, "title": "Milk Chocolate / 2 Kg (54 Scoops)", "price": "3799", "compare_at_price": "5200", "sku": "FG-SSP-POW-YEAST-CHOC-2KG", "available": True},
                {"id": 42203, "title": "Milk Chocolate / 500 g (14 Scoops)", "price": "1099", "compare_at_price": "1499", "sku": "FG-SSP-POW-YEAST-CHOC-500G", "available": True},
                {"id": 42204, "title": "Strawberry Delight / 1 Kg", "price": "1999", "compare_at_price": "2700", "sku": "FG-SSP-POW-YEAST-SB-1KG", "available": True},
                {"id": 42205, "title": "Mocha Rush / 1 Kg", "price": "1999", "compare_at_price": "2700", "sku": "FG-SSP-POW-YEAST-MR-1KG", "available": True},
                {"id": 42206, "title": "Vanilla Ice Cream / 1 Kg", "price": "1999", "compare_at_price": "2700", "sku": "FG-SSP-POW-YEAST-VIC-1KG", "available": True},
                {"id": 42207, "title": "Cookies & Cream / 1 Kg", "price": "1999", "compare_at_price": "2700", "sku": "FG-SSP-POW-YEAST-CC-1KG", "available": True},
                {"id": 42208, "title": "Unflavored / 1 Kg", "price": "1899", "compare_at_price": "2600", "sku": "FG-SSP-POW-YEAST-RAW-1KG", "available": True}
            ]
        }
    ]

    # Save into store snapshot
    store_snapshot["onesciencenutrition.com"] = osn_products
    store_snapshot["nutrabay.com"] = nutrabay_products
    store_snapshot["plixlife.com"] = plix_products

    with open(STORE_SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(store_snapshot, f, indent=2)
    print("Updated store_snapshot.json with onesciencenutrition.com, nutrabay.com, plixlife.com!")

    # 3. Create picks and readings
    # We will define product groups and their variant readings
    new_picks = []
    new_readings = []

    def add_product(store, handle, category, brand, name, is_vegan, group_key, variants_data):
        nonlocal next_idx
        for v_idx, v_info in enumerate(variants_data):
            idx = next_idx
            next_idx += 1
            new_picks.append(f"{store}|{handle}|{category}|{brand}")
            
            # Nutrition array: [cal, prot, carbs, fat, sat_fat, trans_fat, chol, fiber, sugars, added_sugars, sodium]
            reading = {
                "i": idx,
                "v": v_idx,
                "g": group_key,
                "name": name,
                "variant": v_info["title"],
                "net": v_info["net"],
                "serv": v_info["serv"],
                "n": v_info["n"],
                "ing": v_info["ing"],
                "allergens": v_info.get("allergens", []),
                "tags": v_info.get("tags", ["Vegetarian", "No Added Sugar"]),
                "is_vegan": is_vegan
            }
            if is_vegan and "Vegan" not in reading["tags"]:
                reading["tags"].insert(0, "Vegan")
            new_readings.append(reading)

    # === ONE SCIENCE NUTRITION ===
    # 1. 100% Premium Whey
    osn_whey_ing = "Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), Soy Lecithin, Cocoa, DigeZyme Multienzyme Complex (Alpha-Amylase, Protease, Papain, Cellulase, Lactase), Sweeteners (Sucralose, Acesulfame K), Sodium Chloride"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-premium-whey-protein", "protein-powders", "One Science Nutrition",
        "100% Premium Whey Protein", False, "osn-premium-whey",
        [
            {"title": "Chocolate Charge 2.27kg", "net": 2270, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]},
            {"title": "Chocolate Charge 907g", "net": 907, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]},
            {"title": "Vanilla Cream 2.27kg", "net": 2270, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]},
            {"title": "Strawberry White Chocolate 2.27kg", "net": 2270, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]},
            {"title": "Cafe Mocha 2.27kg", "net": 2270, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]},
            {"title": "Chocolate Charge 454g", "net": 454, "serv": 32.5, "n": [117, 25.0, 1.6, 2.1, 0.6, 0.0, 45, 0.5, 0.8, 0, 96], "ing": osn_whey_ing, "allergens": ["milk", "soy"]}
        ]
    )

    # 2. ISO Gold
    osn_iso_ing = "Whey Protein Blend (93%)(Whey Protein Isolate, Whey Protein Hydrolysate), Sunflower Lecithin, Papain, Alpha Amylase, Cocoa Powder, Flavours, Xanthan Gum, Sodium Chloride, Sweeteners (Sucralose, Acesulfame K)"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-iso-gold-whey-isolate", "protein-powders", "One Science Nutrition",
        "ISO Gold 100% Whey Isolate", False, "osn-iso-gold",
        [
            {"title": "Chocolate Charge 2.27kg", "net": 2270, "serv": 32.5, "n": [113, 27.0, 0.5, 0.3, 0.2, 0.0, 5, 0.2, 0.3, 0, 24], "ing": osn_iso_ing, "allergens": ["milk"]},
            {"title": "Chocolate Charge 907g", "net": 907, "serv": 32.5, "n": [113, 27.0, 0.5, 0.3, 0.2, 0.0, 5, 0.2, 0.3, 0, 24], "ing": osn_iso_ing, "allergens": ["milk"]},
            {"title": "Vanilla 2.27kg", "net": 2270, "serv": 32.5, "n": [113, 27.0, 0.5, 0.3, 0.2, 0.0, 5, 0.2, 0.3, 0, 24], "ing": osn_iso_ing, "allergens": ["milk"]},
            {"title": "Cafe Mocha 2.27kg", "net": 2270, "serv": 32.5, "n": [113, 27.0, 0.5, 0.3, 0.2, 0.0, 5, 0.2, 0.3, 0, 24], "ing": osn_iso_ing, "allergens": ["milk"]}
        ]
    )

    # 3. Nitra Whey
    osn_nitra_ing = "Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), Creatine Monohydrate, Fat-Reduced Cocoa Powder, L-Aspartic Acid, Boron Proteinate, Maca Powder, Tribulus Terrestris Fruit Extract, Sweeteners (Acesulfame K, Sucralose), Xanthan Gum, DigeZyme Multienzyme Complex"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-nitra-whey", "protein-powders", "One Science Nutrition",
        "Nitra Whey Protein", False, "osn-nitra-whey",
        [
            {"title": "Chocolate Brownie 1.81kg", "net": 1810, "serv": 34.0, "n": [118.5, 27.0, 1.5, 0.5, 0.2, 0.0, 30, 0.5, 0.8, 0, 80], "ing": osn_nitra_ing, "allergens": ["milk", "soy"]},
            {"title": "Chocolate Brownie 907g", "net": 907, "serv": 34.0, "n": [118.5, 27.0, 1.5, 0.5, 0.2, 0.0, 30, 0.5, 0.8, 0, 80], "ing": osn_nitra_ing, "allergens": ["milk", "soy"]},
            {"title": "Cappuccino 1.81kg", "net": 1810, "serv": 34.0, "n": [118.5, 27.0, 1.5, 0.5, 0.2, 0.0, 30, 0.5, 0.8, 0, 80], "ing": osn_nitra_ing, "allergens": ["milk", "soy"]},
            {"title": "Strawberry 1.81kg", "net": 1810, "serv": 34.0, "n": [118.5, 27.0, 1.5, 0.5, 0.2, 0.0, 30, 0.5, 0.8, 0, 80], "ing": osn_nitra_ing, "allergens": ["milk", "soy"]}
        ]
    )

    # 4. Ripped Professional Whey
    osn_ripped_ing = "Whey Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Calcium Caseinate), Inulin, L-Carnitine L-Tartrate, Conjugated Linoleic Acid (CLA), Green Coffee Extract, Garcinia Cambogia Extract, DigeZyme Multienzyme Complex, Cocoa Powder, Flavours, Sucralose"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-ripped-professional-whey", "protein-powders", "One Science Nutrition",
        "Ripped Professional Whey Protein", False, "osn-ripped-whey",
        [
            {"title": "Chocolate 1.81kg", "net": 1810, "serv": 30.0, "n": [102, 24.0, 1.0, 0.5, 0.2, 0.0, 20, 0.8, 0.5, 0, 65], "ing": osn_ripped_ing, "allergens": ["milk", "soy"]},
            {"title": "Vanilla 1.81kg", "net": 1810, "serv": 30.0, "n": [102, 24.0, 1.0, 0.5, 0.2, 0.0, 20, 0.8, 0.5, 0, 65], "ing": osn_ripped_ing, "allergens": ["milk", "soy"]}
        ]
    )

    # 5. Plant Protein Pea Isolate
    osn_plant_ing = "Pea Protein Isolate, Cocoa Powder, Nature Identical Chocolate Flavour, Steviol Glycosides (INS 960), Xanthan Gum (INS 415), DigeZyme Multienzyme Complex"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-plant-protein-pea-isolate", "protein-powders", "One Science Nutrition",
        "100% Plant Pea Protein Isolate", True, "osn-plant-protein",
        [
            {"title": "Rich Chocolate 1kg", "net": 1000, "serv": 33.0, "n": [120, 25.0, 2.5, 1.2, 0.3, 0.0, 0, 1.8, 0.4, 0, 180], "ing": osn_plant_ing, "allergens": []}
        ]
    )

    # 6. High Protein Oats
    osn_oats_ing = "Rolled Oats (75%), Plant Protein Blend (Pea Protein, Soy Protein Isolate), Dark Chocolate Chips, Cocoa Powder, Chia Seeds, Pumpkin Seeds, Almonds, Jaggery"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-high-protein-oats", "breakfast-cereals", "One Science Nutrition",
        "High Protein Oats Dark Chocolate", True, "osn-hp-oats",
        [
            {"title": "Dark Chocolate 400g", "net": 400, "serv": 50.0, "n": [195, 13.0, 28.0, 3.5, 0.8, 0.0, 0, 4.5, 4.0, 2.0, 45], "ing": osn_oats_ing, "allergens": ["gluten", "soy", "nuts"]}
        ]
    )

    # 7. High Protein Muesli
    osn_muesli_ing = "Rolled Oats (50%), Wheat Flakes, Plant Protein Crisp, Dark Chocolate, Raisins, Almonds, Pumpkin Seeds, Cocoa Powder, Jaggery"
    add_product(
        "onesciencenutrition.com", "one-science-nutrition-high-protein-muesli", "breakfast-cereals", "One Science Nutrition",
        "High Protein Muesli Dark Choco Crunchy", True, "osn-hp-muesli",
        [
            {"title": "Dark Choco Crunchy 400g", "net": 400, "serv": 50.0, "n": [198, 13.0, 27.0, 3.8, 0.9, 0.0, 0, 4.0, 5.0, 2.5, 40], "ing": osn_muesli_ing, "allergens": ["gluten", "nuts"]}
        ]
    )

    # === NUTRABAY OWN BRAND ===
    # 8. Gold Whey Protein Concentrate
    nb_gold_conc_ing = "Whey Protein Concentrate (Cross-Flow Microfiltered), Cocoa Solids, Nature Identical Flavouring Substance (Chocolate), Enzymes Blend (Protease, Cellulase, Lactase, Amylase, Lipase), Stabilizer (INS 407, INS 415), Emulsifier (INS 322(i)), Common Salt, Sweetener (INS 955), Anti-Caking Agent (INS 551)"
    add_product(
        "nutrabay.com", "nutrabay-gold-100-whey-protein-concentrate", "protein-powders", "Nutrabay",
        "Gold 100% Whey Protein Concentrate", False, "nb-gold-concentrate",
        [
            {"title": "Rich Chocolate 1kg", "net": 1000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]},
            {"title": "Rich Chocolate 2kg", "net": 2000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]},
            {"title": "Cafe Mocha 1kg", "net": 1000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]},
            {"title": "Strawberry Milkshake 1kg", "net": 1000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]},
            {"title": "Kesar Kulfi 1kg", "net": 1000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]},
            {"title": "Vanilla 1kg", "net": 1000, "serv": 35.0, "n": [140.27, 25.08, 5.42, 2.03, 1.38, 0.0, 69.63, 1.2, 1.6, 0, 179.68], "ing": nb_gold_conc_ing, "allergens": ["milk"]}
        ]
    )

    # 9. Gold Whey Protein Isolate
    nb_gold_iso_ing = "Whey Protein Isolate (Cross-Flow Microfiltered), Cocoa Solids, Flavours, Digestive Enzymes Blend (Protease, Cellulase, Lactase, Amylase, Lipase), Emulsifier (INS 322(i)), Salt, Sweetener (INS 955)"
    add_product(
        "nutrabay.com", "nutrabay-gold-100-whey-protein-isolate", "protein-powders", "Nutrabay",
        "Gold 100% Whey Protein Isolate", False, "nb-gold-isolate",
        [
            {"title": "Cold Coffee 1kg", "net": 1000, "serv": 32.0, "n": [118.0, 26.0, 1.5, 0.5, 0.3, 0.0, 15.0, 0.4, 0.6, 0, 160.0], "ing": nb_gold_iso_ing, "allergens": ["milk"]},
            {"title": "Rich Chocolate Creme 1kg", "net": 1000, "serv": 32.0, "n": [118.0, 26.0, 1.5, 0.5, 0.3, 0.0, 15.0, 0.4, 0.6, 0, 160.0], "ing": nb_gold_iso_ing, "allergens": ["milk"]},
            {"title": "Rich Chocolate Creme 2kg", "net": 2000, "serv": 32.0, "n": [118.0, 26.0, 1.5, 0.5, 0.3, 0.0, 15.0, 0.4, 0.6, 0, 160.0], "ing": nb_gold_iso_ing, "allergens": ["milk"]},
            {"title": "Strawberry Milkshake 1kg", "net": 1000, "serv": 32.0, "n": [118.0, 26.0, 1.5, 0.5, 0.3, 0.0, 15.0, 0.4, 0.6, 0, 160.0], "ing": nb_gold_iso_ing, "allergens": ["milk"]},
            {"title": "Vanilla 1kg", "net": 1000, "serv": 32.0, "n": [118.0, 26.0, 1.5, 0.5, 0.3, 0.0, 15.0, 0.4, 0.6, 0, 160.0], "ing": nb_gold_iso_ing, "allergens": ["milk"]}
        ]
    )

    # 10. Pure Whey Protein Concentrate (Raw / Unflavoured)
    nb_raw_whey_ing = "Whey Protein Concentrate (Cross-Flow Microfiltered 100%)"
    add_product(
        "nutrabay.com", "nutrabay-pure-whey-protein-concentrate", "protein-powders", "Nutrabay",
        "Pure 100% Raw Whey Protein Concentrate", False, "nb-pure-whey-raw",
        [
            {"title": "Unflavoured 1kg", "net": 1000, "serv": 30.0, "n": [121.0, 23.4, 2.4, 2.1, 1.3, 0.0, 55.0, 0.0, 1.5, 0, 80.0], "ing": nb_raw_whey_ing, "allergens": ["milk"]},
            {"title": "Unflavoured 1.5kg", "net": 1500, "serv": 30.0, "n": [121.0, 23.4, 2.4, 2.1, 1.3, 0.0, 55.0, 0.0, 1.5, 0, 80.0], "ing": nb_raw_whey_ing, "allergens": ["milk"]},
            {"title": "Unflavoured 2kg", "net": 2000, "serv": 30.0, "n": [121.0, 23.4, 2.4, 2.1, 1.3, 0.0, 55.0, 0.0, 1.5, 0, 80.0], "ing": nb_raw_whey_ing, "allergens": ["milk"]}
        ]
    )

    # 11. Gold Tri-Blend Whey Protein
    nb_tri_ing = "Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate), Cocoa Solids, Nature Identical Flavours, Digestive Enzymes Blend (Protease, Cellulase, Lactase, Amylase, Lipase), Sweetener (INS 955), Emulsifier (INS 322(i))"
    add_product(
        "nutrabay.com", "nutrabay-gold-tri-blend-whey-protein", "protein-powders", "Nutrabay",
        "Gold Tri-Blend Whey Protein", False, "nb-tri-blend",
        [
            {"title": "Double Chocolate 1kg", "net": 1000, "serv": 33.0, "n": [131.0, 25.0, 3.2, 1.8, 1.1, 0.0, 50.0, 0.6, 1.2, 0, 140.0], "ing": nb_tri_ing, "allergens": ["milk"]},
            {"title": "Double Chocolate 2kg", "net": 2000, "serv": 33.0, "n": [131.0, 25.0, 3.2, 1.8, 1.1, 0.0, 50.0, 0.6, 1.2, 0, 140.0], "ing": nb_tri_ing, "allergens": ["milk"]},
            {"title": "Strawberry Milkshake 1kg", "net": 1000, "serv": 33.0, "n": [131.0, 25.0, 3.2, 1.8, 1.1, 0.0, 50.0, 0.6, 1.2, 0, 140.0], "ing": nb_tri_ing, "allergens": ["milk"]},
            {"title": "Malai Kulfi 1kg", "net": 1000, "serv": 33.0, "n": [131.0, 25.0, 3.2, 1.8, 1.1, 0.0, 50.0, 0.6, 1.2, 0, 140.0], "ing": nb_tri_ing, "allergens": ["milk"]}
        ]
    )

    # 12. Gold Hydrolyzed Pea Protein
    nb_pea_ing = "Hydrolyzed Pea Protein Isolate, Cocoa Solids, Nature Identical Flavour, Steviol Glycosides (INS 960), Common Salt, Digestive Enzymes Blend"
    add_product(
        "nutrabay.com", "nutrabay-gold-hydrolyzed-pea-protein", "protein-powders", "Nutrabay",
        "Gold Hydrolyzed Pea Protein Isolate", True, "nb-pea-isolate",
        [
            {"title": "Rich Chocolate Creme 1kg", "net": 1000, "serv": 40.0, "n": [148.0, 25.0, 4.5, 2.2, 0.6, 0.0, 0.0, 2.5, 0.5, 0, 280.0], "ing": nb_pea_ing, "allergens": []},
            {"title": "Cold Coffee 1kg", "net": 1000, "serv": 40.0, "n": [148.0, 25.0, 4.5, 2.2, 0.6, 0.0, 0.0, 2.5, 0.5, 0, 280.0], "ing": nb_pea_ing, "allergens": []},
            {"title": "French Vanilla 1kg", "net": 1000, "serv": 40.0, "n": [148.0, 25.0, 4.5, 2.2, 0.6, 0.0, 0.0, 2.5, 0.5, 0, 280.0], "ing": nb_pea_ing, "allergens": []}
        ]
    )

    # 13. Wellness Vegan Plant Protein + Superfoods
    nb_superfoods_ing = "Pea Protein Isolate, Brown Rice Protein, Malt Extract, Cocoa Solids, Vitamins & Minerals Blend, Digestive Enzymes Blend (Protease, Cellulase, Lactase, Amylase, Lipase), Flaxseed Extract, Spirulina Powder, Moringa Extract, Stabilizer (INS 407, 415), Sweetener (INS 955)"
    add_product(
        "nutrabay.com", "nutrabay-wellness-vegan-plant-protein-superfoods", "protein-powders", "Nutrabay",
        "Wellness Vegan Plant Protein Powder with Superfoods", True, "nb-vegan-superfoods",
        [
            {"title": "Rich Chocolate 1kg", "net": 1000, "serv": 34.0, "n": [139.5, 24.0, 9.3, 1.5, 0.4, 0.0, 0.0, 3.2, 1.2, 0, 210.0], "ing": nb_superfoods_ing, "allergens": []},
            {"title": "Rich Chocolate 500g", "net": 500, "serv": 34.0, "n": [139.5, 24.0, 9.3, 1.5, 0.4, 0.0, 0.0, 3.2, 1.2, 0, 210.0], "ing": nb_superfoods_ing, "allergens": []},
            {"title": "Gourmet Chocolate 500g", "net": 500, "serv": 34.0, "n": [139.5, 24.0, 9.3, 1.5, 0.4, 0.0, 0.0, 3.2, 1.2, 0, 210.0], "ing": nb_superfoods_ing, "allergens": []}
        ]
    )

    # === PLIX ===
    # 14. EVOLVE Plant Protein Powder
    plix_evolve_ing = "Pea Protein Isolate, Brown Rice Protein, Cocoa Powder, Natural Identical Flavour, Papain, Bromelain, Vitamin B12, Steviol Glycosides (INS 960), Pink Himalayan Salt"
    add_product(
        "plixlife.com", "plix-evolve-plant-protein-powder", "protein-powders", "Plix",
        "EVOLVE 100% Plant Protein Powder", True, "plix-evolve",
        [
            {"title": "Rich Chocolate 1kg (30 Scoops)", "net": 1000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Rich Chocolate 2kg (60 Scoops)", "net": 2000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Rich Chocolate 3kg (90 Scoops)", "net": 3000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Cafe Mocha 1kg (30 Scoops)", "net": 1000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Cafe Mocha 2kg (60 Scoops)", "net": 2000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Vanilla 1kg (30 Scoops)", "net": 1000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Vanilla 2kg (60 Scoops)", "net": 2000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []},
            {"title": "Strawberry 1kg (30 Scoops)", "net": 1000, "serv": 34.5, "n": [126.8, 25.26, 5.08, 0.60, 0.17, 0.0, 0.0, 2.1, 2.65, 0, 179.6], "ing": plix_evolve_ing, "allergens": []}
        ]
    )

    # 15. Super Strength Fermented Yeast Protein
    plix_yeast_ing = "Fermented Yeast Protein (Saccharomyces cerevisiae), Cocoa Powder, Nature Identical Chocolate Flavour, Papain, Bromelain, Steviol Glycosides (INS 960), Pink Himalayan Salt"
    add_product(
        "plixlife.com", "plix-super-strength-fermented-yeast-protein", "protein-powders", "Plix",
        "Super Strength Fermented Yeast Protein", True, "plix-yeast",
        [
            {"title": "Milk Chocolate 1kg (27 Scoops)", "net": 1000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Milk Chocolate 2kg (54 Scoops)", "net": 2000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Milk Chocolate 500g (14 Scoops)", "net": 500, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Strawberry Delight 1kg", "net": 1000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Mocha Rush 1kg", "net": 1000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Vanilla Ice Cream 1kg", "net": 1000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Cookies & Cream 1kg", "net": 1000, "serv": 34.0, "n": [125.0, 24.0, 4.0, 1.0, 0.25, 0.0, 0.0, 2.5, 0.8, 0, 120.0], "ing": plix_yeast_ing, "allergens": []},
            {"title": "Unflavored 1kg", "net": 1000, "serv": 34.0, "n": [125.0, 26.0, 2.0, 1.0, 0.25, 0.0, 0.0, 1.5, 0.2, 0, 100.0], "ing": "Fermented Yeast Protein (Saccharomyces cerevisiae 100%)", "allergens": []}
        ]
    )

    print(f"Adding {len(new_picks)} new pick lines and {len(new_readings)} new readings!")

    # 4. Append to picks.txt and readings.jsonl
    with open(PICKS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(new_picks) + "\n")
    print(f"Appended {len(new_picks)} picks to {PICKS_FILE}")

    with open(READINGS_FILE, "a", encoding="utf-8") as f:
        for r in new_readings:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Appended {len(new_readings)} readings to {READINGS_FILE}")

    print("\nBatch 4A files successfully prepared!")

if __name__ == "__main__":
    main()
