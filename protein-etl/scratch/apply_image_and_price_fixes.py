import json
import urllib.request
from pathlib import Path

# 1. Verified Working Image Replacements (All tested and confirmed 200 OK image/*)
VERIFIED_IMAGE_MAP = {
    # Avvatar (percent-encoded URL)
    "avvatar-protein-wafer-bar": "https://www.avvatarindia.com/images/product_images/1754284949_WhatsApp%20Image%202025-07-25%20at%2012.08.28%20PM.jpeg",
    
    # Cosmix (Official Shopify CDN)
    "cosmix-plant-protein-kerala-vanilla-bean": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/PackCover.webp?v=1790226033",
    "cosmix-plant-protein-malnad-arabica-coffee": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/PackCover_439f2c33-7821-4a6c-a6d1-696a102ee5ac.webp?v=1790226128",
    "cosmix-raw-plant-protein-unflavoured": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/CopyofPackCover-2.webp?v=1790226211",
    
    # The Whole Truth (Official CDN)
    "the-whole-truth-pure-whey-isolate-unflavoured": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691679839.png?w=600",
    "the-whole-truth-plant-protein-double-cocoa": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691566136.png?w=600",
    "the-whole-truth-plant-protein-pista-badaam": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691565681.png?w=600",
    
    # Optimum Nutrition (Official ON India Shopify CDN)
    "optimum-nutrition-gold-standard-100-whey-double-rich-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927065725_1_872e2270-f183-4b16-9679-60f0c2cab58e.jpg?v=1791372160",
    "optimum-nutrition-gold-standard-100-whey-vanilla-ice-cream": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/1118946_1_d0ed8e7b-35a6-41a2-aa0f-5efde2a95806.webp?v=1752258642",
    "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927065725_1_872e2270-f183-4b16-9679-60f0c2cab58e.jpg?v=1791372160",
    "isopure-low-carb-dutch-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/089094025939_1_961fea67-9d69-4e39-b471-24a3eaa8b984.jpg?v=1784782190",
    "isopure-zero-carb-creamy-vanilla": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/089094025939_1_961fea67-9d69-4e39-b471-24a3eaa8b984.jpg?v=1784782190",
    
    # OZiva (Official Shopify CDN)
    "oziva-clean-whey-protein-concentrate": "https://cdn.shopify.com/s/files/1/2393/2199/files/Pack_of_1_f321c13c-955d-45b4-a6f9-144f9234cb38.png?v=1748857257",
    "oziva-organic-plant-protein": "https://cdn.shopify.com/s/files/1/2393/2199/products/OPPU_1_d1901b8a-5738-40af-8f91-7e93e753c9cf.jpg?v=1701175440",
    
    # Pintola (Official Shopify CDN)
    "pintola-high-protein-peanut-butter-dark-chocolate": "https://cdn.shopify.com/s/files/1/0538/2137/4655/files/HP_DC_Mockup.png?v=1780312471",
    
    # Max Protein / RiteBite (Official Shopify CDN)
    "ritebite-daily-protein-bar-choco-berry": "https://cdn.shopify.com/s/files/1/0512/8827/7146/files/Mood-Shot_1.png?v=1787741576",
    "ritebite-daily-protein-bar-choco-almond": "https://cdn.shopify.com/s/files/1/0512/8827/7146/files/Max_Protein_Daily_Choco_Almond_Bar_2.png?v=1787739677",
    
    # MyFitness (Official Shopify CDN)
    "myfitness-high-protein-peanut-butter-crispy-chocolate": "https://cdn.shopify.com/s/files/1/0440/7921/8842/files/chocolate-crispy-1773491327_9be99785-30ab-4b4b-accb-dd909c2b27c0.webp?v=1773500155",
    
    # Phab (Official Shopify CDN)
    "phab-high-protein-milkshake-classic-chocolate": "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_03_44_51_PM_1.webp?v=1784610561",
    
    # Open Secret (Official Shopify CDN)
    "open-secret-unjunked-high-protein-choco-almond-cookies": "https://cdn.shopify.com/s/files/1/0629/7252/6778/files/ChocoAlmondBoxof5Cookies.jpg?v=1783068673"
}

# 2. Verified Real Store Pricing & Variants to Update
VERIFIED_PRICE_UPDATES = {
    "the-whole-truth-plant-protein-double-cocoa": [
        {"id": 1, "title": "500g", "price": 1425.0, "mrp": 1425.0, "compare_at_price": 1425.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg", "price": 2650.0, "mrp": 2650.0, "compare_at_price": 2650.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "the-whole-truth-plant-protein-pista-badaam": [
        {"id": 1, "title": "500g", "price": 1575.0, "mrp": 1575.0, "compare_at_price": 1575.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg", "price": 2950.0, "mrp": 2950.0, "compare_at_price": 2950.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "the-whole-truth-pure-whey-isolate-unflavoured": [
        {"id": 1, "title": "500g", "price": 3849.0, "mrp": 3849.0, "compare_at_price": 3849.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg", "price": 7499.0, "mrp": 7499.0, "compare_at_price": 7499.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "cosmix-raw-plant-protein-unflavoured": [
        {"id": 1, "title": "500g Pouch", "price": 1286.0, "mrp": 1513.0, "compare_at_price": 1513.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg Pouch", "price": 2099.0, "mrp": 2714.0, "compare_at_price": 2714.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "cosmix-plant-protein-kerala-vanilla-bean": [
        {"id": 1, "title": "500g", "price": 1362.0, "mrp": 1602.0, "compare_at_price": 1602.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg", "price": 2270.0, "mrp": 2892.0, "compare_at_price": 2892.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "cosmix-plant-protein-malnad-arabica-coffee": [
        {"id": 1, "title": "500g", "price": 1362.0, "mrp": 1602.0, "compare_at_price": 1602.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg", "price": 2270.0, "mrp": 2892.0, "compare_at_price": 2892.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "pintola-high-protein-peanut-butter-dark-chocolate": [
        {"id": 1, "title": "510g (Crunchy)", "price": 349.0, "mrp": 355.0, "compare_at_price": 355.0, "net_weight_g": 510, "in_stock": True},
        {"id": 2, "title": "1kg (Crunchy)", "price": 659.0, "mrp": 665.0, "compare_at_price": 665.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "myfitness-high-protein-peanut-butter-crispy-chocolate": [
        {"id": 1, "title": "510g", "price": 275.0, "mrp": 319.0, "compare_at_price": 319.0, "net_weight_g": 510, "in_stock": True},
        {"id": 2, "title": "1.25kg", "price": 499.0, "mrp": 669.0, "compare_at_price": 669.0, "net_weight_g": 1250, "in_stock": True}
    ],
    "optimum-nutrition-gold-standard-100-whey-double-rich-chocolate": [
        {"id": 1, "title": "2 lbs (907g)", "price": 4629.0, "mrp": 5079.0, "compare_at_price": 5079.0, "net_weight_g": 907, "in_stock": True}
    ],
    "optimum-nutrition-gold-standard-100-whey-vanilla-ice-cream": [
        {"id": 1, "title": "1 lb (454g)", "price": 2499.0, "mrp": 3449.0, "compare_at_price": 3449.0, "net_weight_g": 454, "in_stock": True}
    ],
    "oziva-clean-whey-protein-concentrate": [
        {"id": 1, "title": "1kg (Starter Pack)", "price": 3699.0, "mrp": 3899.0, "compare_at_price": 3899.0, "net_weight_g": 1000, "in_stock": True}
    ],
    "oziva-organic-plant-protein": [
        {"id": 1, "title": "500g (Starter Pack)", "price": 1299.0, "mrp": 1329.0, "compare_at_price": 1329.0, "net_weight_g": 500, "in_stock": True},
        {"id": 2, "title": "1kg (Result Pack)", "price": 2199.0, "mrp": 2499.0, "compare_at_price": 2499.0, "net_weight_g": 1000, "in_stock": True}
    ]
}

# Load broken products to know which ones need image_url set to null (clean fallback emoji)
with open("protein-etl/scratch/browser_image_status.json", "r", encoding="utf-8") as f:
    broken_list = json.load(f)["broken"]

broken_slugs = set(b["slug"] for b in broken_list)

# 3. Read and update manual_entries.jsonl
manual_file = Path("protein-etl/data/demo_catalog/manual_entries.jsonl")
lines = [l.strip() for l in manual_file.read_text(encoding="utf-8").splitlines() if l.strip()]

updated_lines = []
updated_images_count = 0
cleared_images_count = 0
updated_prices_count = 0

for line in lines:
    item = json.loads(line)
    handle = item.get("handle")
    
    # A. Image updates
    if handle in VERIFIED_IMAGE_MAP:
        item["image_url"] = VERIFIED_IMAGE_MAP[handle]
        updated_images_count += 1
    elif handle in broken_slugs or any(handle.startswith(b) or b.startswith(handle) for b in broken_slugs):
        # Per Decision 2: Set to null to keep clean emoji fallback without broken HTTP errors
        item["image_url"] = None
        cleared_images_count += 1
        
    # B. Price updates
    if handle in VERIFIED_PRICE_UPDATES:
        item["variants"] = VERIFIED_PRICE_UPDATES[handle]
        updated_prices_count += 1
        
    updated_lines.append(json.dumps(item))

manual_file.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
print(f"manual_entries.jsonl updated:")
print(f"  - Verified Images added: {updated_images_count}")
print(f"  - Unverified/broken images set to null (clean emoji): {cleared_images_count}")
print(f"  - Verified real store pricing updated: {updated_prices_count}")

# 4. Also update store_snapshot.json for Avvatar Wafer Bar
snapshot_file = Path("protein-etl/data/demo_catalog/store_snapshot.json")
snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
avvatar_prods = snapshot.get("avvatarindia.com", [])
for p in avvatar_prods:
    if p.get("handle") == "protein-wafer-bar-coffee-flavour-320g":
        for img in p.get("images", []):
            if "WhatsApp Image" in img.get("src", ""):
                img["src"] = img["src"].replace(" ", "%20")
                print("Updated Avvatar wafer bar image in store_snapshot.json with percent-encoding")
snapshot_file.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

print("\nFiles updated successfully!")
