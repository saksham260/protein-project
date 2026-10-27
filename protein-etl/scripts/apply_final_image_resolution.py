import json
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client

ROOT = Path(__file__).resolve().parents[2]

# 1. Exact verified handles to Supabase Storage URLs
EXACT_VERIFIED_STORAGE = {
    # Optimum Nutrition
    "optimum-nutrition-serious-mass": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/optimum-nutrition-serious-mass-gainer.webp",
    
    # Epigamia
    "epigamia-greek-yogurt-natural": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/epigamia-high-protein-greek-yogurt-natural-no-added-sugar.webp",
    "epigamia-greek-yogurt-alphonso-mango": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/epigamia-high-protein-greek-yogurt-alphonso-mango.webp",
    "epigamia-greek-yogurt-wild-blueberry": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/epigamia-high-protein-greek-yogurt-wild-blueberry.webp",
    "epigamia-greek-yogurt-strawberry": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/epigamia-high-protein-greek-yogurt-strawberry.webp",
    
    # Max Protein
    "max-protein-7-grain-protein-cookie-choco-chips": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/max-protein-7-grain-protein-cookie-choco-chips.webp",
    "max-protein-7-grain-protein-cookie-oats-raisins": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/max-protein-7-grain-protein-cookie-oats-raisins.webp",
    "max-protein-7-grain-protein-cookie-nuts-seeds": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/max-protein-7-grain-protein-cookie-nuts-seeds.webp",
    
    # Phab
    "phab-high-protein-bar-strawberries-cream": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/phab-high-protein-bar-strawberries-cream.webp",
    
    # Lo! Foods
    "lo-foods-ultra-low-carb-keto-atta": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/lo-foods-ultra-low-carb-keto-atta-3g-net-carbs.webp",
    
    # Bigmuscles Nutrition
    "bigmuscles-real-mass-gainer": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/bigmuscles-nutrition-real-mass-gainer.webp",
    
    # Wellbeing Nutrition
    "wellbeing-nutrition-superfood-plant-protein-vanilla": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/wellbeing-nutrition-superfood-plant-protein-french-vanilla.webp",
    
    # OZiva
    "oziva-protein-herbs-for-women": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/oziva-protein-herbs-for-women.webp",
    
    # RAW Pressery
    "raw-pressery-high-protein-milkshake-cold-coffee": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/raw-pressery-high-protein-milkshake-cold-coffee.webp",
    
    # Avvatar
    "avvatar-100-whey-isolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/avvatar-100-whey-isolate.webp",
    
    # Dymatize (via Muscle House India)
    "dymatize-iso100-hydrolyzed-whey-isolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/dymatize-iso100-hydrolyzed-whey-isolate.webp",
    "dymatize-iso100-hydrolyzed-whey-isolate-gourmet-chocolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/dymatize-iso100-hydrolyzed-whey-protein-isolate-gourmet-chocolate.webp",
    "dymatize-iso100-hydrolyzed-whey-isolate-birthday-cake": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/dymatize-iso100-hydrolyzed-whey-protein-isolate-birthday-cake.webp",
    "dymatize-elite-100-whey-protein-rich-chocolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/dymatize-elite-100-whey-protein-rich-chocolate.webp",
    
    # MuscleBlaze
    "muscleblaze-super-gainer-xxl": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-super-gainer-xxl.webp",
    "muscleblaze-mass-gainer-pro": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-mass-gainer-pro.webp",
    "muscleblaze-100-micellar-casein": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-100-micellar-casein.webp",
    "muscleblaze-biozyme-iso-zero": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-biozyme-iso-zero-low-carb.webp",
    "muscleblaze-high-protein-oats-dark-chocolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-high-protein-oats-dark-chocolate.webp",
    "muscleblaze-fuel-one-protein-shake-belgian-chocolate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/muscleblaze-fuel-one-protein-shake-belgian-chocolate.webp",
}

# Handles to strictly nullify (Waiting List -> clean emoji fallback)
WAITING_LIST_HANDLES = {
    # Abbott
    "ensure-original-complete-nutrition-vanilla",
    "ensure-plus-high-protein-vanilla",
    "ensure-diabetes-care-vanilla",
    "glucerna-specialized-diabetes-care-vanilla",
    "pediasure-complete-growth-chocolate",
    "pediasure-complete-growth-vanilla",
    # Gritzo
    "gritzo-supermilk-young-athletes-boys-13",
    "gritzo-supermilk-young-athletes-girls-13",
    # Milky Mist
    "milky-mist-high-protein-paneer",
    "milky-mist-greek-yogurt-natural-unsweetened",
    # Urban Platter
    "urban-platter-organic-firm-tofu",
    # Ultimate Nutrition
    "ultimate-nutrition-prostar-100-whey-chocolate-creme",
    "ultimate-nutrition-iso-sensation-93-chocolate",
    # MuscleTech
    "muscletech-nitrotech-ripped-french-vanilla",
    "muscletech-nitrotech-100-whey-gold-double-rich-chocolate",
    "muscletech-mass-tech-extreme-2000",
    # Myprotein
    "myprotein-impact-whey-isolate-chocolate-smooth",
    "myprotein-clear-whey-isolate-orange-mango",
    # Labrada
    "labrada-muscle-mass-gainer",
    # Avvatar Mass Gainer
    "avvatar-high-protein-mass-gainer",
    # Amul
    "amul-high-protein-milk",
    "amul-high-protein-probiotic-dahi",
    # Optimum Nutrition unverified flavors / Step 0 fix
    "optimum-nutrition-gold-standard-100-whey-extreme-milk-chocolate",
    "optimum-nutrition-gold-standard-100-casein",
    "optimum-nutrition-platinum-hydrowhey",
    "optimum-nutrition-gold-standard-100-plant-protein-chocolate",
    # Plix
    "plix-womens-plant-protein",
    "plix-daily-superfood-green-protein",
    # OZiva
    "oziva-superfood-plant-protein-women",
    # Kapiva
    "kapiva-ayurvedic-protein-for-women",
    "kapiva-dia-free-plant-protein",
    # Ketofy
    "ketofy-high-protein-keto-flour-atta",
    "ketofy-chocolate-keto-cookies",
    "ketofy-high-protein-keto-bhujia-sev",
    "ketofy-high-protein-keto-nachos-peri-peri",
    # Eat Better Co
    "eat-better-co-high-protein-spicy-seed-trail-mix",
    # MuscleBlaze Hazelnut
    "muscleblaze-fuel-one-protein-shake-hazelnut-cafe",
    # Complan & Horlicks
    "complan-royale-chocolate-nutrition-drink",
    "horlicks-protein-plus-chocolate",
    "horlicks-protein-plus-vanilla",
    # Soya & Atta
    "fortune-soya-chunks",
    "nutrela-soya-chunks",
    "nutrela-soya-mini-chunks",
    "nutrela-soya-granules",
    "aashirvaad-proactive-high-protein-multigrain-atta"
}

def main():
    print("=== Applying Final Image Resolution to ETL Sources ===")
    
    # 1. Update manual_entries.jsonl
    manual_path = ROOT / "protein-etl" / "data" / "demo_catalog" / "manual_entries.jsonl"
    updated_manual = []
    
    with open(manual_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            handle = item.get("handle")
            
            if handle in EXACT_VERIFIED_STORAGE:
                item["image_url"] = EXACT_VERIFIED_STORAGE[handle]
                for v in item.get("variants", []):
                    v["image_url"] = EXACT_VERIFIED_STORAGE[handle]
            elif handle in WAITING_LIST_HANDLES:
                item["image_url"] = None
                for v in item.get("variants", []):
                    v["image_url"] = None
            
            updated_manual.append(json.dumps(item, ensure_ascii=False))
            
    with open(manual_path, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_manual) + "\n")
    print(f"Updated {manual_path}")

    # 2. Update store_snapshot.json
    snap_path = ROOT / "protein-etl" / "data" / "demo_catalog" / "store_snapshot.json"
    with open(snap_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
        
    # Update Nutrabay in store_snapshot
    nb_url_map = {
        "nutrabay-whey-protein-concentrate": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/nutrabay-pure-100-raw-whey-protein-concentrate.webp",
        "nutrabay-gold-tri-blend-whey-protein": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/nutrabay-gold-tri-blend-whey-protein.webp",
        "nutrabay-gold-hydrolyzed-pea-protein": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/nutrabay-gold-hydrolyzed-pea-protein-isolate.webp",
        "nutrabay-wellness-vegan-plant-protein-powder-superfoods": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/nutrabay-wellness-vegan-plant-protein-powder-with-superfoods.webp",
        "nutrabay-gold-vital-whey-protein-for-beginners": "https://xggxmlfilnufcacmeiwc.supabase.co/storage/v1/object/public/product-images/nutrabay-gold-100-whey-protein-concentrate.webp"
    }

    # If snapshot has nutrabay.com or top-level handles:
    for k, v in snapshot.items():
        if isinstance(v, dict):
            for nb_h, purl in nb_url_map.items():
                if nb_h in k:
                    v["image_url"] = purl
        elif isinstance(v, list):
            for prod in v:
                h = prod.get("handle", "")
                for nb_h, purl in nb_url_map.items():
                    if nb_h == h or nb_h in h:
                        prod["image_url"] = purl
                        if "images" in prod and prod["images"]:
                            prod["images"][0]["src"] = purl

    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"Updated {snap_path}")

if __name__ == "__main__":
    main()
