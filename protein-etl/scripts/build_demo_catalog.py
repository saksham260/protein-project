"""Build the 100-product demo catalogue from label readings.

Inputs (protein-etl/data/demo_catalog/):
  picks.txt            store | handle | category | brand, one product per line (line number = reading "i")
  readings.jsonl       per-serving values read by hand from each product's nutrition-label photo
  store_snapshot.json  prices / variants / images from each brand's Shopify feed (snapshot 2026-10-06)

Outputs: protein-etl/data/seed_products.json (for scripts/seed.py -> Supabase) and
protein-web/src/data/seedCatalog.json (enriched with metrics, red flags and tiers; used when Supabase is not set up).

Run: python scripts/build_demo_catalog.py
"""
import json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "protein-etl"))
from src.db.supabase_client import SupabaseUploader  # noqa: E402
from src.links import SEARCH_URL_TEMPLATES, build_search_url  # noqa: E402
from src.models import ProductCreate  # noqa: E402
from src.parsers.manual import parse_raw_ingredient_deck  # noqa: E402

HERE = REPO / "protein-etl" / "data" / "demo_catalog"
NUTRIENT_KEYS = ["calories_kcal", "protein_g", "total_carbs_g", "total_fat_g", "saturated_fat_g", "trans_fat_g",
                 "cholesterol_mg", "dietary_fiber_g", "total_sugars_g", "added_sugars_g", "sodium_mg"]

catalogs = json.load(open(HERE / "store_snapshot.json", encoding="utf-8"))


def find_product(store, prefix):
    ps = catalogs[store]
    p = ([x for x in ps if x["handle"] == prefix] or [x for x in ps if x["handle"].startswith(prefix)])[0]
    return {
        "url": f"https://{store}/products/{p['handle']}",
        "image_url": p["images"][0]["src"] if p.get("images") else None,
        "variants": p["variants"],
    }
picks = [l.split("|") for l in (HERE / "picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
readings = [json.loads(l) for l in (HERE / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

products, kept_readings, problems = [], [], []
for r in readings:
    store, prefix, category, brand = picks[r["i"] - 1]
    rec = find_product(store, prefix)
    v = rec["variants"][r.get("v", 0)]
    price = float(v["price"])
    compare = float(v["compare_at_price"]) if v.get("compare_at_price") else 0.0
    mrp = r.get("mrp") or (compare if compare > price else price)
    nutrition = {k: float(x) for k, x in zip(NUTRIENT_KEYS, r["n"]) if x is not None}
    if r.get("poly"):
        nutrition["non_glycemic_polyols_g"] = float(r["poly"])
    ingredients = parse_raw_ingredient_deck(r["ing"]) if r.get("ing") else []
    name = r["name"]
    if name.lower().startswith(brand.lower() + " "):
        name = name[len(brand) + 1:]
    links = [{"platform": "d2c", "url": rec["url"], "platform_price_inr": price}]
    links += [{"platform": p, "url": build_search_url(p, f"{brand} {name}")} for p in SEARCH_URL_TEMPLATES]
    try:
        product = ProductCreate(
            name=name,
            brand_name=brand,
            category_slug=category,
            description=r.get("desc"),
            image_url=rec["image_url"],
            variants=[{
                "variant_name": r.get("variant") or name,
                "sku": v.get("sku") or None,
                "mrp_inr": mrp,
                "net_weight_g": r["net"],
                "serving_size_g": r["serv"],
                "serving_size_label": r.get("label"),
                "nutrition": nutrition,
                "ingredient_list": ingredients,
                "ingredient_deck_raw": [{"name": x, "position": k + 1} for k, x in enumerate(ingredients)],
                "allergens": r.get("allergens", []),
                "dietary_tags": r.get("tags", []),
                "image_url": rec["image_url"],
                "redirect_links": links,
            }],
        )
    except Exception as e:
        problems.append(f"{r['i']} {name}: {e}")
        continue
    # Sanity: label energy should roughly match 4P + 4C + 9F
    est = 4 * nutrition["protein_g"] + 4 * nutrition["total_carbs_g"] + 9 * nutrition["total_fat_g"]
    if est and abs(est - nutrition["calories_kcal"]) > max(25, 0.2 * nutrition["calories_kcal"]):
        problems.append(f"{r['i']} {name}: energy {nutrition['calories_kcal']} vs macros {est:.0f} (check)")
    if nutrition["protein_g"] > r["serv"]:
        problems.append(f"{r['i']} {name}: protein > serving size")
    products.append(product)
    kept_readings.append(r)

raw = [p.model_dump(mode="json", exclude_none=True) for p in products]
uploader = SupabaseUploader(dry_run=True)
tier_defs = json.load(open(REPO / "protein-etl/src/data/protein_sources.json", encoding="utf-8"))["tier_definitions"]
enriched = []
for p, r in zip(products, kept_readings):
    p = uploader.process_and_enrich_product(p)
    # No ingredient list on the label photos: use the protein source stated on the pack front / same product line.
    if r.get("protein_tier") and not p.variants[0].ingredient_list:
        p.variants[0].protein_profile.primary_protein_source = r["protein_source"]
        p.variants[0].protein_profile.protein_tier = tier_defs[r["protein_tier"]]["label"]
    enriched.append(p.model_dump(mode="json"))

(REPO / "protein-etl/data/seed_products.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
(REPO / "protein-web/src/data/seedCatalog.json").write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding="utf-8")

from collections import Counter
print("products:", len(products), dict(Counter(p.category_slug for p in products)))
print("brands:", len({p.brand_name for p in products}))
for p in problems:
    print("PROBLEM", p)
