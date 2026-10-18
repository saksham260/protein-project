import json, urllib.request, time
from pathlib import Path

BATCH2_PICKS = [
    ("getphab.com", "phab-21g-protein-bar-chocolate-brownie", "protein-bars", "Phab"),
    ("getphab.com", "phab-21g-protein-bar-mocha-nut-fudge", "protein-bars", "Phab"),
    ("getphab.com", "lemon-pie-10g-protein-millet-wafer-bar", "protein-bars", "Phab"),
    ("getphab.com", "cookies-cream-protein-millet-wafer", "protein-bars", "Phab"),
    ("getphab.com", "phab-18g-protein-milkshake-cold-coffee", "rtd-drinks", "Phab"),
    ("getphab.com", "cold-coffee-18g-protein-milkshake-copy", "rtd-drinks", "Phab"),
    ("getphab.com", "mango-magic-18g-protein-milkshake-copy", "rtd-drinks", "Phab"),
    ("cosmix.in", "no-nonsense-plant-protein-pro-classic-unflavoured", "protein-powders", "Cosmix"),
    ("cosmix.in", "no-nonsense-plant-protein-pro-kerala-vanilla-bean", "protein-powders", "Cosmix"),
    ("cosmix.in", "no-nonsense-plant-protein-pro-malnad-arabica-coffee", "protein-powders", "Cosmix"),
    ("cosmix.in", "choco-peanut-protein-bar", "protein-bars", "Cosmix"),
    ("cosmix.in", "no-nonsense-fermented-yeast-protein-peanut-butter-fudge", "protein-powders", "Cosmix"),
    ("yogabars.in", "unsweetened-peanut-butter-400g", "protein-spreads", "Yoga Bar"),
    ("yogabars.in", "proclean-whey-protein-concentrate-1kg", "protein-powders", "Yoga Bar"),
    ("yogabars.in", "proclean-plant-protein-coffee", "protein-powders", "Yoga Bar"),
    ("yogabars.in", "power-up-coffee-20g-protein-bar-pack-of-5", "protein-bars", "Yoga Bar"),
    ("yogabars.in", "26g-protein-shake-double-chocolate", "rtd-drinks", "Yoga Bar"),
    ("in.fastandup.com", "plant-protein-alphonso-mango-25-servings", "protein-powders", "Fast&Up"),
    ("in.fastandup.com", "plant-protein-cookies-cream-1kg-free-spillproof-shaker", "protein-powders", "Fast&Up"),
    ("in.fastandup.com", "yeast-protein-unflavoured-1kg", "protein-powders", "Fast&Up"),
    ("in.fastandup.com", "yeast-protein-coffee-1kg", "protein-powders", "Fast&Up"),
    ("asitisnutrition.com", "as-it-is-atom-nxt-protein", "protein-powders", "AS-IT-IS Nutrition"),
    ("asitisnutrition.com", "as-it-is-one-fermented-yeast-protein-unflavoured-unsweetened", "protein-powders", "AS-IT-IS Nutrition"),
    ("asitisnutrition.com", "atom-whey-protein", "protein-powders", "AS-IT-IS Nutrition"),
    ("asitisnutrition.com", "atom-whey-assorted-36-gms-pack-of-6", "protein-powders", "AS-IT-IS Nutrition"),
    ("alpino.store", "super-bar-chocolate-40g", "protein-bars", "Alpino"),
    ("alpino.store", "super-bar-cookies-n-cream", "protein-bars", "Alpino"),
    ("alpino.store", "supernatural-peanut-protein-powder-cold-coffee-protein", "protein-powders", "Alpino"),
    ("alpino.store", "alpino-chocolate-peanut-butter-smooth", "protein-spreads", "Alpino"),
    ("alpino.store", "high-protein-dark-chocolate-peanut-butter-crunch", "protein-spreads", "Alpino"),
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
results = []

for store, handle, cat, brand in BATCH2_PICKS:
    url = f"https://{store}/products/{handle}.json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            p = data.get("product", {})
            v_count = len(p.get("variants", []))
            img_count = len(p.get("images", []))
            first_v = p.get("variants", [{}])[0]
            price = first_v.get("price")
            results.append({
                "store": store,
                "handle": handle,
                "status": "OK",
                "title": p.get("title"),
                "variants_count": v_count,
                "images_count": img_count,
                "first_price": price,
                "variants": [{"title": v.get("title"), "price": v.get("price"), "compare_at_price": v.get("compare_at_price"), "grams": v.get("grams"), "available": v.get("available")} for v in p.get("variants", [])],
                "images": [img.get("src") for img in p.get("images", [])]
            })
            print(f"[OK] {brand:<15} {handle:<50} | {p.get('title')[:40]} | {v_count} vars | {img_count} imgs | Rs {price}")
    except Exception as e:
        results.append({
            "store": store,
            "handle": handle,
            "status": f"ERR: {e}"
        })
        print(f"[FAIL] {brand:<15} {handle:<50} | {e}")
    time.sleep(0.4)

out_path = Path("protein-etl/data/demo_catalog/batch2_preflight.json")
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved {len(results)} results to {out_path}")
