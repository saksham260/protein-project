import io
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

BATCH1_IMAGES = [
    ("raw-pressery-high-protein-milkshake-chocolate-mint", "Raw Pressery Choco Mint 200ml", "https://cdn.shopify.com/s/files/1/0753/4349/5462/files/CopyofUntitled-1_0008_ChocoMintProtein01_430x_16833b36-21e5-4890-904b-c2ce927fbd63.jpg?v=1725617361"),
    ("raw-pressery-high-protein-milkshake-banana-honey", "Raw Pressery Banana Honey 200ml", "https://cdn.shopify.com/s/files/1/0753/4349/5462/files/CopyofUntitled-1_0013_BananaProtein01.jpg?v=1725616943"),
    ("phab-high-protein-milkshake-vanilla-almond", "Phab 18g Shake Vanilla Almond", "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_08_50_38_AM_1.webp?v=1784610560"),
    ("phab-high-protein-milkshake-strawberries-cream", "Phab 18g Shake Strawberries Cream", "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_08_53_33_AM_1.webp?v=1784610561"),
    ("phab-high-protein-milkshake-mango-magic", "Phab 18g Shake Mango Magic", "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_08_42_24_AM_1.webp?v=1784611012"),
    ("phab-protein-milkshake-coffee-tiramisu", "Phab 10g Shake Coffee Tiramisu", "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/ChatGPT_Image_Jul_13_2026_08_57_59_AM_1.webp?v=1784611421"),
    ("eat-better-co-better-seed-mix-spiced-jaggery-nut-free", "Eat Better Seed Mix Spiced Jaggery", "https://cdn.shopify.com/s/files/1/0272/5606/2025/files/dE55RUc29rVvxQ_A3awmmD0TelzU-of1SsPD41ftLFg.jpg?v=1777895153"),
    ("farmley-high-protein-roasted-makhana-tangy-tomato", "Farmley Makhana Tangy Tomato", "https://cdn.shopify.com/s/files/1/0597/7754/8453/files/feb26JARmakhanathumnail-07.jpg?v=1770126162"),
    ("farmley-high-protein-roasted-makhana-peri-peri", "Farmley Makhana Peri Peri", "https://cdn.shopify.com/s/files/1/0597/7754/8453/files/feb26_JAR_makhana_thumnail-11_1.jpg?v=1770201465"),
    ("farmley-5-in-1-protein-rich-seed-mix", "Farmley 5-in-1 Seed Mix", "https://cdn.shopify.com/s/files/1/0597/7754/8453/files/61YRcvEHu8L._SL1042.jpg?v=1792410085"),
    ("farmley-high-protein-roasted-pumpkin-seeds", "Farmley Pumpkin Seeds", "https://cdn.shopify.com/s/files/1/0597/7754/8453/files/Pumpkin_seeds.png?v=1769602006"),
    ("lo-foods-protein-chef-baked-bikaneri-bhujia", "Lo! Foods Baked Bikaneri Bhujia", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/baked_bhujia.png?v=1739943708"),
    ("lo-foods-keto-south-indian-mixture-low-carb", "Lo! Foods Keto South Indian Mixture", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/blinkit_28.png?v=1780037498"),
    ("lo-foods-protein-chef-keto-almond-cookies", "Lo! Foods Keto Almond Cookies", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/keto_almond_cookie.png?v=1779359023"),
    ("lo-foods-gluten-free-ragi-oat-cookies", "Lo! Foods Ragi Oat Cookies", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/ragi_cookie.png?v=1779359578"),
    ("lo-foods-gluten-free-butter-millet-cookies", "Lo! Foods Butter Millet Cookies", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/butter_millet_cookie.png?v=1779359315"),
    ("lo-foods-gluten-free-cashew-pistachio-millet-cookies", "Lo! Foods Cashew Pista Cookies", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/pista_cookie_b77f9556-7f09-4e28-9f86-770f94970a30.png?v=1779359183"),
    ("lo-foods-protein-chef-high-protein-no-maida-rusk", "Lo! Foods High Protein Rusk", "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/1_97.png?v=1787730322"),
    ("open-secret-white-choco-cashew-nutty-cookies", "Open Secret White Choco Cashew Cookie", "https://cdn.shopify.com/s/files/1/0629/7252/6778/files/1.FOP_208905e2-8b5c-4036-b31f-a8eec95f56a0.jpg?v=1782563830"),
    ("open-secret-special-choco-almond-nutty-brownie", "Open Secret Choco Almond Brownie", "https://cdn.shopify.com/s/files/1/0629/7252/6778/files/ChocoAlmondNuttyBrownie-4packs.jpg?v=1695814927"),
    ("max-protein-7-grain-protein-cookie-coconut-delite", "Max Protein Coconut Delite Cookie", "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/1_0937c0d4-14c8-4d7b-8449-3822702c812d.jpg?v=1657297086"),
    ("max-protein-7-grain-protein-cookie-choco-coconut", "Max Protein Choco Coconut Cookie", "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/1_f4c793d6-0ab9-47a2-833f-aedd4b04233a.jpg?v=1657296948"),
    ("max-protein-7-grain-protein-cookie-trail-mix", "Max Protein Trail Mix Cookie", "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/mood-shot_c4c6f50e-af30-48a3-9eeb-808bcaed8527.png?v=1677666654"),
    ("max-protein-berry-bliss-crunchy-protein-cookies", "Max Protein Berry Bliss Cookie", "https://cdn.shopify.com/s/files/1/0512/8827/7146/files/CrunchyCookief.png?v=1786620862"),
]

OUT_DIR = Path("protein-etl/scratch/batch1_imgs")
OUT_DIR.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

cols = 4
rows = 6
cell_w, cell_h = 300, 340
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
draw = ImageDraw.Draw(sheet)

for idx, (slug, label, url) in enumerate(BATCH1_IMAGES):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    webp_path = OUT_DIR / f"{slug}.webp"
    im_save = im.copy()
    if im_save.width > 1200 or im_save.height > 1200:
        im_save.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    im_save.save(webp_path, format="WEBP", quality=85)
    print(f"[{idx+1:2d}/24] Saved {webp_path.name} ({im.width}x{im.height})")

    thumb = im.copy()
    thumb.thumbnail((280, 280), Image.Resampling.LANCZOS)
    c = idx % cols
    r_idx = idx // cols
    x0 = c * cell_w + (cell_w - thumb.width) // 2
    y0 = r_idx * cell_h + 10
    sheet.paste(thumb, (x0, y0))
    draw.text((c * cell_w + 10, r_idx * cell_h + 295), f"{idx+1}. {label[:34]}", fill=(0, 0, 0))

sheet_path = Path("protein-etl/scratch/batch1_contact_sheet.jpg")
sheet.save(sheet_path, format="JPEG", quality=85)
print(f"Saved contact sheet to {sheet_path}")

