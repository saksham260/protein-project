import os
import urllib.request
from PIL import Image, ImageDraw

os.makedirs("protein-etl/scratch/batch2_images", exist_ok=True)

# (index_1based, new_handle, label, img_url)
BATCH2_ITEMS = [
    (378, "bsn-syntha-6-protein-powder-chocolate-milkshake", "BSN Syntha-6 Protein Chocolate Milkshake", "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/Red_BSN_Syntha-6_Protein_Set.png?v=1792066574"),
    (380, "isopure-low-carb-whey-protein-isolate-cookies-cream", "Isopure Whey Isolate Cookies & Cream", "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/089094025847_1_afc28725-ee74-4a09-ba85-f5c7af5e2f78.jpg?v=1784783583"),
    (388, "nakpro-womens-whey-protein-isolate-malai-kulfi", "Nakpro Women's Whey Protein Isolate", "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/01_malaikulfi_169f4c83-0f5f-4ab5-a86a-d9d31561bab3.jpg?v=1777272000"),
    (390, "as-it-is-atom-plant-protein-complex-cafe-latte", "AS-IT-IS ATOM Plant Protein Complex", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOMPlantProteinComplex1kgcommonpouchdesignCafeProductFrontImage_1.jpg?v=1782985650"),
    (391, "as-it-is-atom-pea-protein-isolate-caramelized-banana", "AS-IT-IS ATOM Pea Protein Caramelized Banana", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_PEA_PROTEIN_1KG_Caramelized_Banana_PRODUCT_FRONT_IMAGE.png?v=1776768832"),
    (392, "cosmix-no-nonsense-plant-protein-mahabaleshwar-strawberry", "CosMix Plant Protein Strawberry", "https://cdn.shopify.com/s/files/1/0281/7507/3373/files/ConvertOut-Resized-StrawberryCatalogueCover.jpg?v=1762523304"),
    (393, "plantigo-plant-based-protein-powder-brazilian-chocolate", "Plantigo Plant Protein Brazilian Chocolate", "https://cdn.shopify.com/s/files/1/0653/9604/8086/files/Plant_Protein_Brazilian_Chocolate.jpg?v=1761727563"),
    (436, "yogabar-dark-chocolate-cranberry-muesli", "Yoga Bar Dark Chocolate Cranberry Muesli", "https://cdn.shopify.com/s/files/1/0267/5245/files/yogabar-super-muesli-dark-chocolate-cranberry.jpg?v=1780750682"),
    (457, "optimum-nutrition-gold-standard-100-whey-alphonso-mango", "ON Gold Standard 100% Whey Alphonso Mango", "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927069648_1_9927f6fb-c9b4-4da2-b8e3-26c0d934c151.webp?v=1752258590"),
    (459, "optimum-nutrition-gold-standard-100-whey-unflavoured", "ON Gold Standard 100% Whey Unflavoured", "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/748927072457_1_0ac342c8-c0e1-48f9-b9b8-857e132a4e3e.jpg?v=1782188875"),
    (463, "labrada-iso-100-whey-protein-isolate-chocolate", "Labrada ISO 100% Whey Protein Isolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/products/ISO-Whey-Choc-2K-Front.jpg?v=1755172810"),
    (464, "labrada-100-whey-protein-chocolate", "Labrada 100% Whey Protein Chocolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/files/100whey500GChoR1_1.jpg?v=1761389437"),
    (466, "labrada-turbo-whey-protein-chocolate", "Labrada Turbo Whey Protein Chocolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/files/LabradaTurbowheychoclate1.8kgview1.jpg?v=1693813131"),
    (467, "labrada-classic-whey-protein-powder-chocolate", "Labrada Classic Whey Protein Chocolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/files/WHEYPROTEIN_1_8KG_CHOCOLATE_R1.png?v=1784012835"),
    (468, "yogabar-ultimate-whey-isolate-yeast-protein-chocolate", "Yoga Bar Ultimate Whey Isolate Chocolate", "https://cdn.shopify.com/s/files/1/0267/5245/files/whey-isolate-yeast-protein-chocolate-flavour-pack.jpg?v=1784804941"),
    (469, "wellbeing-nutrition-biofermented-yeast-protein-dark-chocolate", "Wellbeing Nutrition Yeast Protein Dark Choc", "https://cdn.shopify.com/s/files/1/0240/2942/9840/files/Yeast_Protein_2_FOP_04b7b319-5acb-4ec8-b343-8ee8f073e4b8.jpg?v=1793022944"),
    (529, "as-it-is-atom-whey-protein-isolate-mango-delight", "AS-IT-IS ATOM Whey Isolate Mango Delight", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_Whey_Protein_Isolate_Product_Front_Image.jpg?v=1776771464"),
]

thumbs = []
for idx, handle, label, url in BATCH2_ITEMS:
    webp_path = f"protein-etl/scratch/batch2_images/{handle}.webp"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw_path = f"protein-etl/scratch/batch2_images/{handle}.raw"
    with urllib.request.urlopen(req, timeout=20) as resp:
        with open(raw_path, "wb") as f:
            f.write(resp.read())
    im = Image.open(raw_path)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im_rgba = im.convert("RGBA")
        bg.paste(im_rgba, mask=im_rgba.split()[3])
        im = bg
    else:
        im = im.convert("RGB")
    im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    im.save(webp_path, "WEBP", quality=85)
    os.remove(raw_path)
    print(f"Downloaded & converted: {handle}.webp ({im.size})")
    thumbs.append((idx, handle, label, webp_path))

cols = 4
rows = (len(thumbs) + cols - 1) // cols
cell_w, cell_h = 360, 400
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
draw = ImageDraw.Draw(sheet)

for i, (idx, handle, label, path) in enumerate(thumbs):
    r, c = divmod(i, cols)
    x0, y0 = c * cell_w, r * cell_h
    im = Image.open(path)
    im.thumbnail((320, 320), Image.Resampling.LANCZOS)
    sheet.paste(im, (x0 + (cell_w - im.width) // 2, y0 + 10))
    draw.text((x0 + 10, y0 + 340), f"[{idx}] {label[:38]}", fill=(0, 0, 0))
    draw.text((x0 + 10, y0 + 365), handle[:42], fill=(80, 80, 80))

sheet_path = "protein-etl/scratch/batch2_contact_sheet.jpg"
sheet.save(sheet_path, "JPEG", quality=88)
print(f"Saved contact sheet: {sheet_path}")

