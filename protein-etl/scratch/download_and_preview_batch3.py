import os
import urllib.request
from PIL import Image, ImageDraw

os.makedirs("protein-etl/scratch/batch3_images", exist_ok=True)

# (index_1based, source_stem, label, img_url)
BATCH3_ITEMS = [
    (375, "bigmuscles-mass-forge-rich-chocolate", "Bigmuscles Mass Forge Rich Chocolate", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Mass-forge-chocolate_jpg.jpg?v=1791797610"),
    (377, "labrada-muscle-mass-gainer", "Labrada Muscle Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/products/MMGainer-Choc-Front.jpg?v=1747812953"),
    (465, "bigmuscles-mass-forge-malai-kulfi", "Bigmuscles Mass Forge Malai Kulfi", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Mass-Forge_jpg.jpg?v=1791797610"),
    (506, "labrada-muscle-mass-gainer-vanilla", "Labrada Muscle Mass Gainer Vanilla", "https://cdn.shopify.com/s/files/1/0573/1464/0039/products/MMGainer-Van-Front.jpg?v=1747812953"),
    (507, "labrada-muscle-mass-gainer-mocha", "Labrada Muscle Mass Gainer Mocha", "https://cdn.shopify.com/s/files/1/0573/1464/0039/products/Gainer-Mocha-1K-Front.jpg?v=1747812953"),
    (508, "labrada-super-mass-gainer-chocolate-ice-cream", "Labrada Super Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0573/1464/0039/files/mass_Gainer_R1.jpg?v=1751094131"),
    (509, "labrada-super-mass-gainer-malai-kulfi", "Labrada Super Mass Gainer Malai Kulfi", "https://cdn.shopify.com/s/files/1/0573/1464/0039/files/Super_Mass_Gainer_malai_Kufli_F1.jpg?v=1751094131"),
    (511, "bigmuscles-smart-gainer-chocolate-eclair", "Bigmuscles Smart Gainer Choc Eclair", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Chocolate-Eclir-Front.jpg?v=1741691946"),
    (512, "bigmuscles-smart-gainer-cookies-cream", "Bigmuscles Smart Gainer Cookies Cream", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Cookie-and-cream-Fornt.jpg?v=1741691946"),
    (513, "bigmuscles-smart-gainer-malai-kulfi", "Bigmuscles Smart Gainer Malai Kulfi", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Malai-Kulfi-Front.jpg?v=1741691946"),
    (514, "bigmuscles-xtreme-muscle-fusion-chocolate-eclair", "Bigmuscles Xtreme Muscle Fusion Choc", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Chocolate-Eclir-Front_fff5d30a-1f61-4cd7-bf80-75133786a219.jpg?v=1741696633"),
    (515, "bigmuscles-xtreme-muscle-fusion-cookies-cream", "Bigmuscles Xtreme Muscle Fusion Cookies", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Cookie-and-cream-Fornt_c856277d-cd4f-4327-bc50-553b1660b8bb.jpg?v=1741696633"),
    (516, "bigmuscles-xtreme-muscle-fusion-malai-kulfi", "Bigmuscles Xtreme Muscle Fusion Kulfi", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Malai-Kulfi-Front_fd8d451e-7647-47b0-a3ae-b2dc45694913.jpg?v=1741696633"),
    (517, "bigmuscles-body-fuel-hardcore-chocolate-eclair", "Bigmuscles Body Fuel Hardcore Choc", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Bodyfuel_1kg.jpg?v=1735546948"),
    (518, "gnc-pro-performance-weight-gainer-double-chocolate", "GNC Pro Performance Weight Gainer Choc", "https://cdn.shopify.com/s/files/1/0623/9010/8391/files/ch3kg_2_6a1bd1db-6df9-424f-9012-e9d79f6bbf3b.png?v=1775471003"),
    (519, "gnc-pro-performance-weight-gainer-vanilla-ice-cream", "GNC Pro Performance Weight Gainer Van", "https://cdn.shopify.com/s/files/1/0623/9010/8391/files/Weight-Gainer-Vanilla-2Kg-3_d6a66597-b514-4774-b324-688a43af248a.jpg?v=1767166747"),
    (520, "gnc-amp-amplified-mass-xxx-chocolate", "GNC AMP Amplified Mass XXX Chocolate", "https://cdn.shopify.com/s/files/1/0623/9010/8391/files/99-161-940Mass-XXX-2Kg-Chocolate_L-Leucine-100g-Front.jpg?v=1792673049"),
    (521, "bigmuscles-xtreme-weight-gainer-malt-chocolate", "Bigmuscles Xtreme Weight Gainer Choc", "https://cdn.shopify.com/s/files/1/0291/3743/6771/products/1_4e714947-9552-4c7a-9ca0-8b5f9c9ce5b1.jpg?v=1628498464"),
    (522, "bigmuscles-lean-gain-malt-chocolate", "Bigmuscles Lean Gain Malt Chocolate", "https://cdn.shopify.com/s/files/1/0291/3743/6771/products/1_b462be8a-2fc8-4461-90b1-e2fdaa8a0be4.jpg?v=1628498787"),
    (523, "optimum-nutrition-serious-mass-weight-gainer-vanilla", "ON Serious Mass Weight Gainer Vanilla", "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/1110151_1_ac0525c5-9758-439c-9593-a2f38ce11694.webp?v=1752258616"),
    (524, "gnc-amp-amplified-mass-xxx-vanilla", "GNC AMP Amplified Mass XXX Vanilla", "https://cdn.shopify.com/s/files/1/0623/9010/8391/files/99-180-940Mass-XXX-2Kg-Vanilla_L-Leucine-100g-Front.jpg?v=1792673049"),
    (525, "bigmuscles-mamoth-gainer-belgian-chocolate", "Bigmuscles Mamoth Gainer Belgian Choc", "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/B0CDX2SKXH.MAIN.jpg?v=1701839147"),
    (526, "as-it-is-atom-mass-gainer-double-rich-chocolate", "AS-IT-IS ATOM Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_MASS_GAINER_1KG_COMMON_POUCH_DOUBLE_RICH_CHOCOLATE.jpg?v=1786012441"),
    (527, "as-it-is-atom-mass-gainer-mango-fusion", "AS-IT-IS ATOM Mass Gainer Mango Fusion", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_MASS_GAINER_1KG_COMMON_POUCH_MANGO.jpg?v=1786012868"),
    (528, "as-it-is-atom-weight-gainer-double-rich-chocolate", "AS-IT-IS ATOM Weight Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_PWR_WEIGHT_GAINER_DOUBLE_RICH_CHOCOLATE_PRODUCT_FRONT_IMAGE_1.jpg?v=1784633317"),
    (530, "as-it-is-atom-weight-gainer-kesar-elaichi", "AS-IT-IS ATOM Weight Gainer Kesar Elaichi", "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_PWR_WEIGHT_GAINER_KESAR_ELAICHI_PRODUCT_FRONT_IMAGE.jpg?v=1784633433"),
    (531, "nakpro-perform-mass-gainer-double-rich-chocolate", "Nakpro Perform Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/01_doublerichchocolate_5e410d20-11f9-432a-87e4-d4301a15f684.jpg?v=1777286037"),
    (532, "nakpro-gold-mass-gainer-coffee", "Nakpro Gold Mass Gainer Coffee", "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/01_coffee_7fd5a4cc-445d-4a23-9f3d-72d3aa7a3d1e.jpg?v=1777027586"),
    (533, "nakpro-mr-fit-mass-gainer-chocolate", "Nakpro Mr. Fit Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/01_chocolate_08927c8d-16c9-4c6c-ba1b-ce6701c1f7ca.jpg?v=1777292842"),
    (534, "bigmuscles-quick-mass-gainer-malt-chocolate", "Bigmuscles Quick Mass Gainer Chocolate", "https://cdn.shopify.com/s/files/1/0291/3743/6771/products/QucikMass_01.png?v=1677223756"),
]

thumbs = []
for idx, handle, label, url in BATCH3_ITEMS:
    webp_path = f"protein-etl/scratch/batch3_images/{handle}.webp"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw_path = f"protein-etl/scratch/batch3_images/{handle}.raw"
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

cols = 5
rows = (len(thumbs) + cols - 1) // cols
cell_w, cell_h = 340, 380
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
draw = ImageDraw.Draw(sheet)

for i, (idx, handle, label, path) in enumerate(thumbs):
    r, c = divmod(i, cols)
    x0, y0 = c * cell_w, r * cell_h
    im = Image.open(path)
    im.thumbnail((300, 300), Image.Resampling.LANCZOS)
    sheet.paste(im, (x0 + (cell_w - im.width) // 2, y0 + 10))
    draw.text((x0 + 8, y0 + 320), f"[{idx}] {label[:36]}", fill=(0, 0, 0))
    draw.text((x0 + 8, y0 + 345), handle[:40], fill=(80, 80, 80))

sheet_path = "protein-etl/scratch/batch3_contact_sheet.jpg"
sheet.save(sheet_path, "JPEG", quality=88)
print(f"Saved contact sheet: {sheet_path}")

