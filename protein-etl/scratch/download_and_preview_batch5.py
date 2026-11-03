import io
import json
import os
import sys
import urllib.request
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = "protein-etl/scratch/batch5_webp"
os.makedirs(OUT_DIR, exist_ok=True)

BATCH5_ITEMS = [
    {
        "i": 428,
        "source_stem": "as-it-is-atom-roti-protein",
        "brand": "AS-IT-IS Nutrition",
        "name": "ATOM Roti Protein Unflavoured Chapati Mix",
        "url": "https://asitisnutrition.com/products/as-it-is-atom-roti-protein-1kg-make-roti-s-protein-rich-easy-to-use-25g-protein-per-serving",
        "src_img": "https://cdn.shopify.com/s/files/1/0005/5335/3267/files/ATOM_Roti_Protein_500g_Product_Front_Image_11zon.jpg?v=1766470513",
    },
    {
        "i": 429,
        "source_stem": "lo-foods-low-carb-high-protein-atta",
        "brand": "Lo! Foods",
        "name": "Lo Carb High Protein Atta Flour",
        "url": "https://lofoods.fit/products/low-carb-high-protein-atta",
        "src_img": "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/fop-1kg.png?v=1785395514",
    },
    {
        "i": 430,
        "source_stem": "lo-foods-gluten-free-multi-millet-atta",
        "brand": "Lo! Foods",
        "name": "Protein Chef Gluten Free Multi-Millet Atta",
        "url": "https://lofoods.fit/products/gluten-free-multi-millet-atta",
        "src_img": "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/gf_millet_atta1.png?v=1779359225",
    },
    {
        "i": 431,
        "source_stem": "anveshan-high-protein-atta",
        "brand": "Anveshan",
        "name": "High Protein Stone-Ground Atta",
        "url": "https://www.anveshan.farm/products/high-protein-atta",
        "src_img": "https://cdn.shopify.com/s/files/1/0270/3346/9006/files/Khapli_version_main_version_2.0Front.webp?v=1782470555",
    },
    {
        "i": 432,
        "source_stem": "anveshan-khapli-multigrain-atta",
        "brand": "Anveshan",
        "name": "Khapli Multigrain Stone-Ground Atta",
        "url": "https://www.anveshan.farm/products/khapli-multigrain-atta",
        "src_img": "https://cdn.shopify.com/s/files/1/0270/3346/9006/files/Frontcopy1.06.16PM1.08.54PM.webp?v=1775561230",
    },
    {
        "i": 434,
        "source_stem": "humpy-farms-organic-besan",
        "brand": "Humpy Farms",
        "name": "Organic Stone-Ground Besan Chickpea Flour",
        "url": "https://www.humpyfarms.com/products/organic-besan",
        "src_img": "https://cdn.shopify.com/s/files/1/0777/5843/1515/files/Flours-08.jpg?v=1740494801",
    },
    {
        "i": 435,
        "source_stem": "pintola-organic-quinoa",
        "brand": "Pintola",
        "name": "Organic High Protein & Fibre Quinoa",
        "url": "https://pintola.in/products/pintola-organic-quinoa-high-in-protein-fibre-minerals-cholesterol-free-gluten-free-aids-weight-management",
        "src_img": "https://cdn.shopify.com/s/files/1/0538/2137/4655/files/2_49e0e469-5e8f-4844-b14e-833bf01bf0c2.png?v=1780055687",
    },
    {
        "i": 488,
        "source_stem": "wickedgud-multigrain-fusilli-pasta",
        "brand": "WickedGud",
        "name": "Multigrain Fusilli Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-fusilli-pasta-pack-of-4",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/Fusilli_Pack_of_4.jpg?v=1752902256",
    },
    {
        "i": 489,
        "source_stem": "wickedgud-multigrain-penne-pasta",
        "brand": "WickedGud",
        "name": "Multigrain Penne Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-penne-pasta-pack-of-4",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/WickedGudMultigrainPennePastapackof4.png?v=1752736055",
    },
    {
        "i": 490,
        "source_stem": "wickedgud-nourishing-instant-noodles-schezwan",
        "brand": "WickedGud",
        "name": "Nourishing Instant Noodles Schezwan Zero Maida",
        "url": "https://www.wickedgud.com/products/nourishing-instant-noodles-schezwan-pack-of-10",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/WickedGudSchezwanInstantNoodlesPackof10.png?v=1752737738",
    },
    {
        "i": 491,
        "source_stem": "wickedgud-nourishing-instant-noodles-masala",
        "brand": "WickedGud",
        "name": "Nourishing Instant Noodles Masala Zero Maida",
        "url": "https://www.wickedgud.com/products/nourishing-instant-noodles-masala-pack-of-10",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/WickedGudMasalaInstantNoodlesPackof10.png?v=1752735750",
    },
    {
        "i": 492,
        "source_stem": "wickedgud-multigrain-spaghetti-pasta",
        "brand": "WickedGud",
        "name": "Multigrain Spaghetti Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-spaghetti-pasta-pack-of-4",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/WickedGudMultigrainSpaghettiPastapackof4.png?v=1752736690",
    },
    {
        "i": 493,
        "source_stem": "wickedgud-multigrain-macaroni-pasta",
        "brand": "WickedGud",
        "name": "Multigrain Macaroni Pasta High Protein & Fibre",
        "url": "https://www.wickedgud.com/products/multigrain-macaroni-pasta-pack-of-4",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/Macaroni_Pack_of_4.jpg?v=1752902203",
    },
    {
        "i": 495,
        "source_stem": "wickedgud-whole-wheat-wraps-rolls",
        "brand": "WickedGud",
        "name": "Whole Wheat Wraps & Rolls Zero Maida",
        "url": "https://www.wickedgud.com/products/whole-wheat-wraps-rolls",
        "src_img": "https://cdn.shopify.com/s/files/1/0582/7795/3694/files/FOP_703d5982-338e-42e0-925b-43a73f380554.png?v=1778137304",
    },
    {
        "i": 496,
        "source_stem": "twf-whole-wheat-bread-flour",
        "brand": "TWF Flours",
        "name": "Whole Wheat Bread Flour Unbleached Stone-Milled",
        "url": "https://twfflours.com/products/twf-whole-wheat-bread-flour",
        "src_img": "https://cdn.shopify.com/s/files/1/0746/0641/2095/files/WWBGS1.jpg?v=1788932729",
    },
    {
        "i": 497,
        "source_stem": "twf-high-fibre-maida",
        "brand": "TWF Flours",
        "name": "High Fibre Maida Unbleached Craft Flour",
        "url": "https://twfflours.com/products/twf-high-fibre-maida",
        "src_img": "https://cdn.shopify.com/s/files/1/0746/0641/2095/files/1KgHFM.jpg?v=1787638287",
    },
    {
        "i": 498,
        "source_stem": "twf-multigrain-flour",
        "brand": "TWF Flours",
        "name": "Multigrain Stone-Milled Craft Flour",
        "url": "https://twfflours.com/products/twf-multigrain-flour",
        "src_img": "https://cdn.shopify.com/s/files/1/0746/0641/2095/files/MultigrainFlour1.jpg?v=1785145079",
    },
    {
        "i": 499,
        "source_stem": "jiwa-30-degree-peanut-flour",
        "brand": "Jiwa",
        "name": "30 Degree Cold-Pressed High Protein Peanut Flour",
        "url": "https://jiwa.in/products/30-degree-peanut-flour",
        "src_img": "https://cdn.shopify.com/s/files/1/0516/7244/9178/files/YUc_JIWA_PROSHO_25Dpeanutflour200g_front_20Aug26.jpg?v=1789649724",
    },
    {
        "i": 500,
        "source_stem": "jiwa-30-degree-jau-sattu-powder",
        "brand": "Jiwa",
        "name": "30 Degree Jau & Chana Sattu Powder",
        "url": "https://jiwa.in/products/30-degree-jau-sattu-powder",
        "src_img": "https://cdn.shopify.com/s/files/1/0516/7244/9178/files/YUc_JIWAproshot25_Barleyjausattupowder_30june26.jpg?v=1783341966",
    },
    {
        "i": 501,
        "source_stem": "humpy-farms-organic-chana-dal",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Chana Dal",
        "url": "https://www.humpyfarms.com/products/organic-chana-dal",
        "src_img": "https://cdn.shopify.com/s/files/1/0777/5843/1515/files/Dals-02.jpg?v=1716275002",
    },
    {
        "i": 502,
        "source_stem": "humpy-farms-organic-moong-dal",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Yellow Moong Dal",
        "url": "https://www.humpyfarms.com/products/organic-moong-dal",
        "src_img": "https://cdn.shopify.com/s/files/1/0777/5843/1515/files/Dals-17.jpg?v=1716275306",
    },
    {
        "i": 504,
        "source_stem": "humpy-farms-organic-toor-dal",
        "brand": "Humpy Farms",
        "name": "Organic Unpolished Arhar Toor Dal",
        "url": "https://www.humpyfarms.com/products/organic-toor-dal",
        "src_img": "https://cdn.shopify.com/s/files/1/0777/5843/1515/files/Dals-24.jpg?v=1716275737",
    },
]

def main():
    thumbs = []
    for idx, item in enumerate(BATCH5_ITEMS, 1):
        stem = item["source_stem"]
        url = item["src_img"]
        out_path = os.path.join(OUT_DIR, f"{stem}.webp")
        print(f"[{idx}/{len(BATCH5_ITEMS)}] Downloading {stem} <- {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=20).read()
        im = Image.open(io.BytesIO(raw))
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            rgba = im.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[3])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        im.save(out_path, "WEBP", quality=85)
        thumbs.append((item, im.copy()))

    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    cell_w, cell_h = 340, 380
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (248, 250, 252))
    draw = ImageDraw.Draw(sheet)

    for idx, (item, im) in enumerate(thumbs):
        r = idx // cols
        c = idx % cols
        x0 = c * cell_w
        y0 = r * cell_h
        draw.rectangle([x0 + 4, y0 + 4, x0 + cell_w - 4, y0 + cell_h - 4], fill=(255, 255, 255), outline=(203, 213, 225))
        im_thumb = im.copy()
        im_thumb.thumbnail((300, 280), Image.Resampling.LANCZOS)
        ix = x0 + (cell_w - im_thumb.width) // 2
        iy = y0 + 10 + (280 - im_thumb.height) // 2
        sheet.paste(im_thumb, (ix, iy))
        label1 = f"#{idx+1} (i={item['i']}) {item['brand']}"
        label2 = item["name"][:42]
        label3 = item["name"][42:84]
        draw.text((x0 + 10, y0 + 300), label1, fill=(15, 23, 42))
        draw.text((x0 + 10, y0 + 320), label2, fill=(51, 65, 85))
        if label3:
            draw.text((x0 + 10, y0 + 340), label3, fill=(100, 116, 139))

    sheet_path = "protein-etl/scratch/batch5_contact_sheet.jpg"
    sheet.save(sheet_path, "JPEG", quality=88)
    print(f"Saved contact sheet to {sheet_path}")

if __name__ == "__main__":
    main()

