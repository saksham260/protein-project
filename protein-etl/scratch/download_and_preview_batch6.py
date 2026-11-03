import io
import json
import os
import sys
import urllib.request
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = "protein-etl/scratch/batch6_webp"
os.makedirs(OUT_DIR, exist_ok=True)

BATCH6_ITEMS = [
    {
        "i": 414,
        "source_stem": "pentasure-daily-nutrition-vanilla-400g",
        "brand": "PentaSure",
        "name": "Balanced Daily Nutritional Supplement Vanilla (400g)",
        "url": "https://pentasurenutrition.com/products/nutritional-drink-daily-nutrition-new-pentasure-400gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/key_features_e24d6826-2c3c-47e5-bcbf-260ef5e12f0f.jpg?v=1777960225",
    },
    {
        "i": 415,
        "source_stem": "pentasure-daily-nutrition-vanilla-1kg",
        "brand": "PentaSure",
        "name": "Balanced Daily Nutritional Supplement Vanilla (1kg)",
        "url": "https://pentasurenutrition.com/products/nutritional-drink-daily-nutrition-new-pentasure-1-kg",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/key_features_2.jpg?v=1777960741",
    },
    {
        "i": 416,
        "source_stem": "pentasure-nutrone-healthy-ageing-kesar-badam",
        "brand": "PentaSure",
        "name": "Nutrone Healthy Aging Nutrition Kesar Badam",
        "url": "https://pentasurenutrition.com/products/nutrone-healthy-ageing",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_d88a1cf1-59e6-45de-a589-696f8f1c11bf.jpg?v=1756972404",
    },
    {
        "i": 417,
        "source_stem": "pentasure-nutrone-men-saffron",
        "brand": "PentaSure",
        "name": "Nutrone Men Daily Strength & Immunity Nutrition Saffron",
        "url": "https://pentasurenutrition.com/products/nutrone-men",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/1_e664f567-64bc-40b1-bbde-f8e323266f73.jpg?v=1756972405",
    },
    {
        "i": 418,
        "source_stem": "pentasure-nutrone-women-chocolate",
        "brand": "PentaSure",
        "name": "Nutrone Women Daily Strength & Immunity Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/nutrone-women",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/1_7335f63f-887b-4e2c-bb3e-b451a96f9bc4.jpg?v=1756972405",
    },
    {
        "i": 419,
        "source_stem": "pentasure-pediagold-vanilla",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Vanilla",
        "url": "https://pentasurenutrition.com/products/pediagold-vanilla",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/4_786c814e-ac3c-4809-b1da-627008b1daec.jpg?v=1756972405",
    },
    {
        "i": 423,
        "source_stem": "pentasure-pediagold-chocolate",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Chocolate",
        "url": "https://pentasurenutrition.com/products/pediagold-chocolate",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/4_0ef71061-559b-46a1-a6f9-48018cfa0f8b.jpg?v=1777959557",
    },
    {
        "i": 424,
        "source_stem": "pentasure-pediagold-mango",
        "brand": "PentaSure",
        "name": "PediaGold Complete Growth Nutrition for Kids Mango",
        "url": "https://pentasurenutrition.com/products/pediagold-mango",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/4_43e5cd36-3592-4187-80d2-e61c44d800de.jpg?v=1756972405",
    },
    {
        "i": 425,
        "source_stem": "pentasure-pediagold-plus-peptide-vanilla",
        "brand": "PentaSure",
        "name": "PediaGold Plus 100% Peptide Diet for Kids Vanilla",
        "url": "https://pentasurenutrition.com/products/pediagold-plus",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_d45d02a4-f6ff-4a63-b38f-d7a1025c6640.jpg?v=1756972405",
    },
    {
        "i": 426,
        "source_stem": "nakpro-gen-z-teen-protein-chocolate",
        "brand": "Nakpro",
        "name": "Gen-Z Protein Powder for Teenagers Double Rich Chocolate",
        "url": "https://nakpro.com/products/gen-z-teen-protein-powder",
        "src_img": "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/gen-z_protein.png?v=1746926919",
    },
    {
        "i": 427,
        "source_stem": "nakpro-gen-nxt-protein-shake-mix-chocolate",
        "brand": "Nakpro",
        "name": "GEN-NXT Protein Shake Mix with DHA Double Rich Chocolate",
        "url": "https://nakpro.com/products/nakpro-gen-nxt-protein-shake-mix-with-protein-dha-vitamins-minerals",
        "src_img": "https://cdn.shopify.com/s/files/1/0237/4497/0832/files/01_4fef7041-6cb8-489c-9586-5b4200044624.jpg?v=1780309224",
    },
    {
        "i": 550,
        "source_stem": "pentasure-hp-whey-chocolate",
        "brand": "PentaSure",
        "name": "HP High Protein Clinical Whey Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-hp-whey-protein-chocolate-flavour-400gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/10_57e7f4bc-3740-4f9f-b5af-b6b2c8e41c04.jpg?v=1777364059",
    },
    {
        "i": 551,
        "source_stem": "pentasure-2-0-high-protein-vanilla",
        "brand": "PentaSure",
        "name": "2.0 High Protein High Calorie Clinical Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/weight-gain-powder-weight-gainer-protein-pentasure-2-0-400g",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/11_826ca926-6570-4819-835c-41ad1d3ecb18.jpg?v=1777363259",
    },
    {
        "i": 552,
        "source_stem": "pentasure-2-0-high-protein-chocolate",
        "brand": "PentaSure",
        "name": "2.0 High Protein High Calorie Clinical Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-2-0-high-protein-high-calorie-weight-gainer-chocolate-flavour-400gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/10_733b7b18-6ea5-4e27-b8af-ab8d85b12508.jpg?v=1777364125",
    },
    {
        "i": 553,
        "source_stem": "pentasure-critipep-whey-peptide-vanilla",
        "brand": "PentaSure",
        "name": "Critipep 100% Whey Peptide Critical Care Nutrition Creamy Vanilla",
        "url": "https://pentasurenutrition.com/products/100-whey-peptide-pentasure-critipep",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_77ba6171-3e15-436e-9d22-3efb75a55260.jpg?v=1756972407",
    },
    {
        "i": 556,
        "source_stem": "pentasure-dm-diabetes-care-chocolate",
        "brand": "PentaSure",
        "name": "DM Diabetes Care High Protein Low GI Nutrition Chocolate",
        "url": "https://pentasurenutrition.com/products/pentasure-dm-diabetes-care-nutrition-drink-chocolate-flavor-400-gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/key_features_7a64bd57-f12d-4d6e-97d5-02c2d5cace09.jpg?v=1777363907",
    },
    {
        "i": 557,
        "source_stem": "pentasure-hepatic-liver-care-vanilla",
        "brand": "PentaSure",
        "name": "Hepatic Liver Care Nutrition with BCAA & MCT Vanilla",
        "url": "https://pentasurenutrition.com/products/pentasure-hepatic-nutrition-for-liver-care",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_8fab0295-6ef9-48be-aa32-100e4c84d94a.jpg?v=1756972407",
    },
    {
        "i": 558,
        "source_stem": "threptin-protein-powder-chocolate",
        "brand": "Threptin",
        "name": "Micromix High Protein Casein Supplement Powder Chocolate",
        "url": "https://threptin.com/products/threptin-protein-powder-chocolate",
        "src_img": "https://cdn.shopify.com/s/files/1/0797/3814/2754/files/threptinPowderFront_2_1.png?v=1764758291",
    },
    {
        "i": 559,
        "source_stem": "pentasure-obesigo-meal-replacement-vanilla",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Vanilla",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-vanilla",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/6_5c892bcf-b083-458c-9b77-0a57ae5e661a.jpg?v=1756972405",
    },
    {
        "i": 560,
        "source_stem": "pentasure-obesigo-meal-replacement-chocolate",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Chocolate",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-chocolate",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/6_1293086b-bafd-486c-9cc0-de161b32d83c.jpg?v=1756972405",
    },
    {
        "i": 561,
        "source_stem": "pentasure-obesigo-meal-replacement-mango",
        "brand": "PentaSure",
        "name": "Obesigo High Protein Meal Replacement Shake Mango",
        "url": "https://pentasurenutrition.com/products/obesigo-weight-loss-mango",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/6_10745d16-562a-4a5b-aa4a-a6bcd876f11b.jpg?v=1756972405",
    },
    {
        "i": 562,
        "source_stem": "threptin-protein-powder-vanilla",
        "brand": "Threptin",
        "name": "Micromix High Protein Casein Supplement Powder Vanilla",
        "url": "https://threptin.com/products/threptin-protein-powder-vanilla",
        "src_img": "https://cdn.shopify.com/s/files/1/0797/3814/2754/files/threptinPowderFront.png?v=1764054935",
    },
    {
        "i": 563,
        "source_stem": "threptin-high-protein-diskettes-vanilla",
        "brand": "Threptin",
        "name": "High Protein Casein Diskettes Vanilla",
        "url": "https://threptin.com/products/threptin-protein-diskettes-vanilla",
        "src_img": "https://cdn.shopify.com/s/files/1/0797/3814/2754/files/Rectangle56_1.png?v=1764758378",
    },
    {
        "i": 564,
        "source_stem": "threptin-high-protein-diskettes-chocolate",
        "brand": "Threptin",
        "name": "High Protein Casein Diskettes Chocolate",
        "url": "https://threptin.com/products/threptin-protein-diskettes-chocolate",
        "src_img": "https://cdn.shopify.com/s/files/1/0797/3814/2754/files/Rectangle_19_5.png?v=1764054257",
    },
    {
        "i": 565,
        "source_stem": "threptin-lite-diskettes-sugar-free",
        "brand": "Threptin",
        "name": "Lite Sugar-Free High Protein Diskettes Vanilla",
        "url": "https://threptin.com/products/threptin-lite-diskettes",
        "src_img": "https://cdn.shopify.com/s/files/1/0797/3814/2754/files/Rectangle37.png?v=1764055098",
    },
    {
        "i": 566,
        "source_stem": "pentasure-hp-whey-banana-vanilla",
        "brand": "PentaSure",
        "name": "HP High Protein Clinical Whey Nutrition Banana Vanilla",
        "url": "https://pentasurenutrition.com/products/whey-protein-powder-best-whey-protein-in-india-pentasure-hp-400gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/11_5d0cb500-400f-44f1-b937-f091f4a29789.jpg?v=1777961294",
    },
    {
        "i": 567,
        "source_stem": "pentasure-dm-diabetes-care-vanilla",
        "brand": "PentaSure",
        "name": "DM Diabetes Care High Protein Low GI Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/pentasure-dm-diabetes-care-nutrition-drink-vanilla-flavor-400-gm",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/8_77e77dac-d9a5-40c0-bddb-fdaa58b5ef7d.jpg?v=1777363667",
    },
    {
        "i": 568,
        "source_stem": "pentasure-renal-pre-dialysis-vanilla",
        "brand": "PentaSure",
        "name": "Renal Pre-Dialysis Kidney Care Nutrition Creamy Vanilla",
        "url": "https://pentasurenutrition.com/products/renal-powder-renal-care-pentasure-renal",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_81940781-5c91-48a3-86ea-a9707bbb1839.jpg?v=1756972406",
    },
    {
        "i": 569,
        "source_stem": "pentasure-dls-dialysis-care-vanilla",
        "brand": "PentaSure",
        "name": "DLS Dialysis Care High Protein Nutrition Vanilla",
        "url": "https://pentasurenutrition.com/products/dialysis-powder-dialysis-supplement-pentasure-dls",
        "src_img": "https://cdn.shopify.com/s/files/1/0879/7418/3228/files/3_e8dd4cf6-5687-46bd-bf6e-212a6f13d0f7.jpg?v=1756972406",
    },
]

def main():
    thumbs = []
    for idx, item in enumerate(BATCH6_ITEMS, 1):
        stem = item["source_stem"]
        url = item["src_img"]
        out_path = os.path.join(OUT_DIR, f"{stem}.webp")
        print(f"[{idx}/{len(BATCH6_ITEMS)}] Downloading {stem} <- {url}")
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

    sheet_path = "protein-etl/scratch/batch6_contact_sheet.jpg"
    sheet.save(sheet_path, "JPEG", quality=88)
    print(f"Saved contact sheet to {sheet_path}")

if __name__ == "__main__":
    main()
