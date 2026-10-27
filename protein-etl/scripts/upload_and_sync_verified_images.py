import os
import sys
import json
import urllib.request
import io
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from supabase import create_client

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

load_dotenv(ROOT / "protein-etl" / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase credentials in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Exact verified image sources
VERIFIED_SOURCES = {
    # Optimum Nutrition
    "optimum-nutrition-serious-mass-gainer": "https://cdn.shopify.com/s/files/1/0738/8649/9042/files/1110152_1_43efaf6f-3293-4107-ba6b-f12d32faae8d.webp?v=1752258610",
    
    # Epigamia
    "epigamia-high-protein-greek-yogurt-natural-no-added-sugar": "https://cdn.shopify.com/s/files/1/0331/1983/0148/files/GY85gNatural_29c6f064-d3bb-48e3-bc9d-039e3fc7fb03.png?v=1748432655",
    "epigamia-high-protein-greek-yogurt-alphonso-mango": "https://cdn.shopify.com/s/files/1/0331/1983/0148/files/GY_85g_Mango_62df4255-4c25-4953-9afa-d0113916f742.png?v=1762511723",
    "epigamia-high-protein-greek-yogurt-wild-blueberry": "https://cdn.shopify.com/s/files/1/0331/1983/0148/files/GY85gBlueberry_e3a10441-e97b-47da-ac81-1a1dded237f0.png?v=1748431697",
    "epigamia-high-protein-greek-yogurt-strawberry": "https://cdn.shopify.com/s/files/1/0331/1983/0148/files/GY85gStrawberry.png?v=1748242055",
    
    # Max Protein
    "max-protein-7-grain-protein-cookie-choco-chips": "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/1_ddbfc195-d4a2-48ab-ae4a-ec8952b8dbcc.jpg?v=1657296747",
    "max-protein-7-grain-protein-cookie-oats-raisins": "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/Mood-Shot_14852be1-e6ed-499e-bf77-4fe0da0e6990.png?v=1677666504",
    "max-protein-7-grain-protein-cookie-nuts-seeds": "https://cdn.shopify.com/s/files/1/0512/8827/7146/products/Mood-Shot_a69984f7-2c38-4f17-b7d9-b42555f8ebda.png?v=1677668100",
    
    # Phab
    "phab-high-protein-bar-strawberries-cream": "https://cdn.shopify.com/s/files/1/0563/1891/8790/files/Frame2087330035.webp?v=1784525047",
    
    # Lo! Foods
    "lo-foods-ultra-low-carb-keto-atta-3g-net-carbs": "https://cdn.shopify.com/s/files/1/0060/2551/1012/files/keto_ulc.png?v=1779358989",
    
    # Bigmuscles Nutrition
    "bigmuscles-nutrition-real-mass-gainer": "https://cdn.shopify.com/s/files/1/0291/3743/6771/files/Front_eae82c74-689a-42b6-9182-ef1e15517f6f.jpg?v=1753096698",
    
    # Wellbeing Nutrition
    "wellbeing-nutrition-superfood-plant-protein-french-vanilla": "https://cdn.shopify.com/s/files/1/0240/2942/9840/files/Vegan_Protein_22g_907g_3B_CFU_Probiotics_French_Vanilla_Caramel_1e241fff-bddc-4f0d-867e-0cb49650da8a.jpg?v=1752051770",
    
    # OZiva
    "oziva-protein-herbs-for-women": "https://cdn.shopify.com/s/files/1/2393/2199/files/Choco_D2C_800X800.jpg",
    
    # RAW Pressery
    "raw-pressery-high-protein-milkshake-cold-coffee": "https://cdn.shopify.com/s/files/1/0753/4349/5462/files/CopyofUntitled-1_0003_ColdCoffeeProtein01.jpg?v=1725615990",
    
    # Avvatar
    "avvatar-100-whey-isolate": "https://www.avvatarindia.com/images/product_images/1697618942_FOP.jpg",
    
    # Dymatize (via Muscle House India)
    "dymatize-iso100-hydrolyzed-whey-isolate": "https://cdn.shopify.com/s/files/1/0965/2420/6367/files/ISO100_5lb_India_GourChoc_D7L360001IN0101_1F_3_84de9c17-dc06-4042-97a6-46f2f92bd65c.png?v=1784791261",
    "dymatize-iso100-hydrolyzed-whey-protein-isolate-gourmet-chocolate": "https://cdn.shopify.com/s/files/1/0965/2420/6367/files/ISO100_5lb_India_GourChoc_D7L360001IN0101_1F_3_84de9c17-dc06-4042-97a6-46f2f92bd65c.png?v=1784791261",
    "dymatize-iso100-hydrolyzed-whey-protein-isolate-birthday-cake": "https://cdn.shopify.com/s/files/1/0965/2420/6367/files/Birthday_Cake_pebbles.jpg?v=1784797150",
    "dymatize-elite-100-whey-protein-rich-chocolate": "https://cdn.shopify.com/s/files/1/0965/2420/6367/files/EliteWhey_India_5lb_RichChoc_D7L280001IN0101_1D_1_d2625ed8-8fad-4574-87c5-d9fcbc5b20e7.png?v=1784793745",
    
    # MuscleBlaze
    "muscleblaze-super-gainer-xxl": "https://img4.hkrtcdn.com/37800/prd_3779993-MuscleBlaze-Super-Gainer-XXL-Weight-Gainer-6.6-lb-Chocolate_o.jpg",
    "muscleblaze-mass-gainer-pro": "https://img10.hkrtcdn.com/12116/prd_1211559-MuscleBlaze-Mass-Gainer-PRO-with-Creapure-6.6-lb-Chocolate_o.jpg",
    "muscleblaze-100-micellar-casein": "https://img10.hkrtcdn.com/39694/prd_3969389-MuscleBlaze-100-Micellar-Casein-2.2-lb-Chocolate_o.jpg",
    "muscleblaze-biozyme-iso-zero-low-carb": "https://img4.hkrtcdn.com/46798/prd_4679703-MuscleBlaze-Biozyme-IsoZero-Powder-Old-MRP-4.4-lb-Low-Carb-Tropical-Mango-IsoZero_o.jpg",
    "muscleblaze-high-protein-oats-dark-chocolate": "https://img8.hkrtcdn.com/42837/prd_4283617-MuscleBlaze-High-Protein-Oats-400-g-Dark-Chocolate_o.jpg",
    "muscleblaze-fuel-one-protein-shake-belgian-chocolate": "https://img9.hkrtcdn.com/20231/prd_2023068-MuscleBlaze-18g-Protein-Shake-No-Added-Sugar-1-PiecesPack-Chocolate_o.jpg",
    
    # Nutrabay
    "nutrabay-pure-100-raw-whey-protein-concentrate": "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1010-01-1789475113-200x200.webp",
    "nutrabay-gold-tri-blend-whey-protein": "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1014-12-400x400.webp",
    "nutrabay-gold-hydrolyzed-pea-protein-isolate": "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1102-02-1787736317-200x200.webp",
    "nutrabay-wellness-vegan-plant-protein-powder-with-superfoods": "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1054-03-1753299718-200x200.webp",
    "nutrabay-gold-100-whey-protein-concentrate": "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1064-03-1758998117-200x200.webp"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_and_optimize(source_url: str) -> bytes:
    req = urllib.request.Request(source_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw_bytes = resp.read()
    
    # Optimize to WebP
    try:
        im = Image.open(io.BytesIO(raw_bytes))
        im = im.convert("RGB")
        # Resize if overly large (> 1200px)
        if im.width > 1200 or im.height > 1200:
            im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=85)
        return buf.getvalue()
    except Exception as e:
        print(f"  [WARN] PIL conversion failed ({e}), uploading raw bytes")
        return raw_bytes

def main():
    print(f"=== Starting Upload of {len(VERIFIED_SOURCES)} Verified Product Images to Supabase Storage ===")
    
    uploaded_urls = {}
    for slug, src_url in VERIFIED_SOURCES.items():
        filename = f"{slug}.webp"
        print(f"\nProcessing: {slug}...")
        try:
            img_data = download_and_optimize(src_url)
            print(f"  Downloaded & optimized: {len(img_data)} bytes")
            
            # Upload to Supabase Storage
            res = supabase.storage.from_("product-images").upload(
                path=filename,
                file=img_data,
                file_options={"content-type": "image/webp", "upsert": "true"}
            )
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/product-images/{filename}"
            print(f"  [UPLOAD OK] -> {public_url}")
            uploaded_urls[slug] = public_url
        except Exception as e:
            print(f"  [ERROR] Failed to process {slug}: {e}")

    # 1. Update manual_entries.jsonl
    manual_path = ROOT / "protein-etl" / "data" / "demo_catalog" / "manual_entries.jsonl"
    updated_manual_lines = []
    with open(manual_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            handle = item.get("handle")
            if handle in uploaded_urls:
                item["image_url"] = uploaded_urls[handle]
            elif handle == "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate":
                item["image_url"] = None  # Remove duplicate Double Rich Chocolate image
            updated_manual_lines.append(json.dumps(item, ensure_ascii=False))

    with open(manual_path, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_manual_lines) + "\n")
    print(f"\nUpdated {manual_path} with new Supabase Storage URLs")

    # 2. Update store_snapshot.json if relevant
    snap_path = ROOT / "protein-etl" / "data" / "demo_catalog" / "store_snapshot.json"
    with open(snap_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    # For any matching handles in snapshot, update image_url
    for handle, purl in uploaded_urls.items():
        if handle in snapshot:
            snapshot[handle]["image_url"] = purl

    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"Updated {snap_path}")

    # 3. Save mapping for reference
    with open(ROOT / "protein-etl" / "scratch" / "uploaded_verified_images.json", "w", encoding="utf-8") as f:
        json.dump(uploaded_urls, f, indent=2)

if __name__ == "__main__":
    main()
