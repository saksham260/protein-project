import urllib.request
import json

replacements = {
    "avvatar-protein-wafer-bar": "https://www.avvatarindia.com/images/product_images/1754284949_WhatsApp%20Image%202025-07-25%20at%2012.08.28%20PM.jpeg",
    "cosmix-plant-protein-kerala-vanilla-bean": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/PackCover.webp?v=1790226033",
    "cosmix-plant-protein-malnad-arabica-coffee": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/PackCover_439f2c33-7821-4a6c-a6d1-696a102ee5ac.webp?v=1790226128",
    "cosmix-raw-plant-protein-unflavoured": "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/CopyofPackCover-2.webp?v=1790226211",
    "the-whole-truth-pure-whey-isolate-unflavoured": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691679839.png?w=600",
    "the-whole-truth-plant-protein-double-cocoa": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691566136.png?w=600",
    "the-whole-truth-plant-protein-pista-badaam": "https://media.thewholetruthfoods.com/public/backend-assets/image_1753691565681.png?w=600",
    "optimum-nutrition-gold-standard-100-whey-double-rich-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927065725_1_872e2270-f183-4b16-9679-60f0c2cab58e.jpg?v=1791372160",
    "optimum-nutrition-gold-standard-100-whey-vanilla-ice-cream": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/1118946_1_d0ed8e7b-35a6-41a2-aa0f-5efde2a95806.webp?v=1752258642",
    "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927065725_1_872e2270-f183-4b16-9679-60f0c2cab58e.jpg?v=1791372160",
    "isopure-low-carb-dutch-chocolate": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/089094025939_1_961fea67-9d69-4e39-b471-24a3eaa8b984.jpg?v=1784782190",
    "isopure-zero-carb-creamy-vanilla": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/089094025939_1_961fea67-9d69-4e39-b471-24a3eaa8b984.jpg?v=1784782190",
    "oziva-clean-whey-protein-concentrate": "https://cdn.shopify.com/s/files/1/2393/2199/files/Pack_of_1_f321c13c-955d-45b4-a6f9-144f9234cb38.png?v=1748857257",
    "oziva-organic-plant-protein": "https://cdn.shopify.com/s/files/1/2393/2199/products/OPPU_1_d1901b8a-5738-40af-8f91-7e93e753c9cf.jpg?v=1701175440",
    "pintola-high-protein-peanut-butter-dark-chocolate": "https://cdn.shopify.com/s/files/1/0538/2137/4655/files/HP_DC_Mockup.png?v=1780312471",
    "ritebite-daily-protein-bar-choco-berry": "https://cdn.shopify.com/s/files/1/0512/8827/7146/files/Mood-Shot_1.png?v=1787741576",
    "ritebite-daily-protein-bar-choco-almond": "https://cdn.shopify.com/s/files/1/0512/8827/7146/files/Max_Protein_Daily_Choco_Almond_Bar_2.png?v=1787739677",
    "myfitness-high-protein-peanut-butter-crispy-chocolate": "https://cdn.shopify.com/s/files/1/0440/7921/8842/files/chocolate-crispy-1773491327_9be99785-30ab-4b4b-accb-dd909c2b27c0.webp?v=1773500155",
    "phab-high-protein-milkshake-classic-chocolate": "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_03_44_51_PM_1.webp?v=1784610561",
    "open-secret-unjunked-high-protein-choco-almond-cookies": "https://cdn.shopify.com/s/files/1/0629/7252/6778/files/ChocoAlmondBoxof5Cookies.jpg?v=1783068673"
}

headers = {"User-Agent": "Mozilla/5.0"}

print(f"Testing {len(replacements)} verified candidate image URLs...")
all_ok = True
for key, url in replacements.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if resp.status == 200 and "image" in content_type:
                print(f"[OK 200] {key}")
            else:
                print(f"[WARN {resp.status}] {key}: content-type={content_type}")
                all_ok = False
    except Exception as e:
        print(f"[FAIL] {key}: {e}")
        all_ok = False

if all_ok:
    print("\nALL 20 verified candidate image URLs returned 200 OK image/* successfully!")
