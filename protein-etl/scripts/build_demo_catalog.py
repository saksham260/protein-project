"""Build the demo catalogue from label readings, supporting multi-variant products.

Inputs (protein-etl/data/demo_catalog/):
  picks.txt            store | handle | category | brand, one product per line (line number = reading "i")
  readings.jsonl       per-serving values read by hand from each product's nutrition-label photo
  store_snapshot.json  prices / variants / images from each brand's Shopify feed

Outputs: protein-etl/data/seed_products.json (for scripts/seed.py -> Supabase) and
protein-web/src/data/seedCatalog.json (enriched with metrics, red flags and tiers).

Run: python scripts/build_demo_catalog.py
"""
import json, sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "protein-etl"))
from src.db.supabase_client import SupabaseUploader  # noqa: E402
from src.links import SEARCH_URL_TEMPLATES, build_search_url  # noqa: E402
from src.models import ProductCreate, VariantCreate, NutritionPerPack, slugify  # noqa: E402
from src.parsers.manual import parse_raw_ingredient_deck  # noqa: E402

HERE = REPO / "protein-etl" / "data" / "demo_catalog"
NUTRIENT_KEYS = ["calories_kcal", "protein_g", "total_carbs_g", "total_fat_g", "saturated_fat_g", "trans_fat_g",
                 "cholesterol_mg", "dietary_fiber_g", "total_sugars_g", "added_sugars_g", "sodium_mg"]

catalogs = json.load(open(HERE / "store_snapshot.json", encoding="utf-8"))
tier_defs = json.load(open(REPO / "protein-etl/src/data/protein_sources.json", encoding="utf-8"))["tier_definitions"]

manual_entries_file = HERE / "manual_entries.jsonl"
manual_entries = {}
if manual_entries_file.exists():
    for line in manual_entries_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                obj = json.loads(line)
                manual_entries[obj["handle"]] = obj
            except Exception:
                pass


def find_product(store, prefix):
    if store == "manual" or prefix in manual_entries:
        p = manual_entries[prefix]
        return {
            "url": p.get("url") or "",
            "image_url": p.get("image_url"),
            "variants": p.get("variants", []),
        }
    ps = catalogs[store]
    p = ([x for x in ps if x["handle"] == prefix] or [x for x in ps if x["handle"].startswith(prefix)])[0]
    return {
        "url": p.get("url") or f"https://{store}/products/{p['handle']}",
        "image_url": p["images"][0]["src"] if p.get("images") else None,
        "variants": p["variants"],
    }


def prioritize_and_cap_variants(category_slug, variants, max_variants=12):
    if len(variants) <= 1:
        return variants, []
    
    # 1. Determine default variant (index 0) per F5:
    # Powders: plain variant closest to 1000g, in stock, not combo
    # Others: smallest available pack/weight, not combo
    def default_score(v):
        avail_penalty = 0 if getattr(v, "is_available", True) else 1000000
        combo_penalty = 0 if not getattr(v, "is_combo", False) else 500000
        if category_slug in ("protein-powders", "mass-gainers"):
            weight_diff = abs(v.net_weight_g - 1000)
            return avail_penalty + combo_penalty + weight_diff
        else:
            return avail_penalty + combo_penalty + v.net_weight_g

    sorted_for_default = sorted(variants, key=default_score)
    default_var = sorted_for_default[0]

    # 2. Prioritize remaining variants to satisfy cap (F3 / G1):
    remaining = [v for v in variants if v != default_var]
    
    def variant_priority(v):
        combo_score = 100 if getattr(v, "is_combo", False) else 0
        avail_score = 50 if not getattr(v, "is_available", True) else 0
        return (combo_score + avail_score, v.net_weight_g)

    remaining_sorted = sorted(remaining, key=variant_priority)
    kept = [default_var] + remaining_sorted[:max_variants - 1]
    dropped = remaining_sorted[max_variants - 1:]

    return kept, dropped


picks = [l.split("|") for l in (HERE / "picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
readings = [json.loads(l) for l in (HERE / "readings.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

# Group readings by group key `g` (or use unique id if not grouped)
grouped_readings = defaultdict(list)
for r in readings:
    group_key = r.get("g") or f"single-{r['i']}"
    grouped_readings[group_key].append(r)

products, problems = [], []

for group_key, r_list in grouped_readings.items():
    primary_r = r_list[0]
    store, prefix, category, brand = picks[primary_r["i"] - 1]
    rec = find_product(store, prefix)
    
    name = primary_r["name"]
    if name.lower().startswith(brand.lower() + " "):
        name = name[len(brand) + 1:]
        
    product_variants = []
    
    for r in r_list:
        r_store, r_prefix, _, _ = picks[r["i"] - 1]
        r_rec = find_product(r_store, r_prefix)
        v = r_rec["variants"][r.get("v", 0)]
        price = float(r["price"]) if "price" in r else float(v["price"])
        compare = float(v["compare_at_price"]) if v.get("compare_at_price") else 0.0
        mrp = float(r["mrp"]) if "mrp" in r else (compare if compare > price else price)
        
        nutrition_dict = {k: float(x) for k, x in zip(NUTRIENT_KEYS, r["n"]) if x is not None}
        if r.get("poly"):
            nutrition_dict["non_glycemic_polyols_g"] = float(r["poly"])
            
        ingredients = parse_raw_ingredient_deck(r["ing"]) if r.get("ing") else []
        
        links = [{"platform": "d2c", "url": r_rec["url"], "platform_price_inr": price}]
        var_display_name = r.get("variant") or name
        if brand == "Amul" and "blueberry" not in r_rec.get("handle", "").lower():
            pass  # User rule: Amul products except blueberry shake are only purchasable on Amul store
        else:
            links += [{"platform": p, "url": build_search_url(p, f"{brand} {name} {var_display_name}")} for p in SEARCH_URL_TEMPLATES]
        
        # Check energy sanity per reading
        # Check energy sanity per reading (considering potential fiber/polyol deduction)
        fiber = nutrition_dict.get("dietary_fiber_g", 0) or 0
        poly = float(r.get("poly", 0) or 0)
        est_gross = 4 * nutrition_dict["protein_g"] + 4 * nutrition_dict["total_carbs_g"] + 9 * nutrition_dict["total_fat_g"]
        est_zero_fiber = 4 * nutrition_dict["protein_g"] + 4 * max(0, nutrition_dict["total_carbs_g"] - fiber - poly) + 9 * nutrition_dict["total_fat_g"]
        diff = min(abs(est_gross - nutrition_dict["calories_kcal"]), abs(est_zero_fiber - nutrition_dict["calories_kcal"]))
        if diff > max(25, 0.2 * nutrition_dict["calories_kcal"]):
            problems.append(f"{r['i']} {name} ({var_display_name}): energy {nutrition_dict['calories_kcal']} vs macros {est_gross:.0f} (check)")
        if nutrition_dict["protein_g"] > r["serv"]:
            problems.append(f"{r['i']} {name}: protein > serving size")

        is_avail = True if v.get("available") is None else bool(v.get("available"))
        is_combo = bool(r.get("combo", False))

        tier_key = r.get("protein_tier") or primary_r.get("protein_tier")
        source_key = r.get("protein_source") or primary_r.get("protein_source")
        initial_profile = None
        if tier_key and tier_key in tier_defs:
            initial_profile = {
                "primary_protein_source": source_key,
                "protein_tier": tier_defs[tier_key]["label"],
                "has_added_free_form_aminos": False,
            }
        
        try:
            variant_obj = VariantCreate(
                variant_name=var_display_name,
                sku=v.get("sku") or None,
                mrp_inr=mrp,
                net_weight_g=float(r["net"]),
                serving_size_g=float(r["serv"]),
                serving_size_label=r.get("label"),
                nutrition=NutritionPerPack(**nutrition_dict),
                ingredient_list=ingredients,
                ingredient_deck_raw=[{"name": x, "position": k + 1} for k, x in enumerate(ingredients)],
                allergens=r.get("allergens", []),
                dietary_tags=r.get("tags", []),
                protein_profile=initial_profile,
                image_url=r_rec["image_url"],
                redirect_links=links,
                is_combo=is_combo,
                is_available=is_avail,
            )
            product_variants.append((variant_obj, r))
        except Exception as e:
            problems.append(f"{r['i']} variant {var_display_name}: {e}")

    if not product_variants:
        continue
        
    all_var_objs = [v_pair[0] for v_pair in product_variants]
    kept_vars, dropped_vars = prioritize_and_cap_variants(category, all_var_objs, max_variants=12)
    
    if dropped_vars:
        print(f"[DROPPED {len(dropped_vars)} VARIANTS] {brand} {name}: {[v.variant_name for v in dropped_vars]}")

    audit_lookup = {}
    audit_file = HERE / "scratch" / "vegan_audit.json"
    if audit_file.exists():
        try:
            for item in json.loads(audit_file.read_text(encoding="utf-8")):
                audit_lookup[item["slug"]] = item["is_vegan"]
        except Exception:
            pass

    is_vegan = bool(primary_r.get("is_vegan") or primary_r.get("vegan") or primary_r.get("vegan_claim"))
    if not is_vegan and all("vegan" in [t.lower() for t in v_pair[0].dietary_tags] for v_pair in product_variants):
        is_vegan = True
    temp_slug = slugify(f"{brand}-{name}")
    if temp_slug in audit_lookup:
        is_vegan = audit_lookup[temp_slug]

    try:
        product = ProductCreate(
            name=name,
            brand_name=brand,
            category_slug=category,
            description=primary_r.get("desc"),
            image_url=rec["image_url"],
            is_vegan=is_vegan,
            variants=kept_vars,
        )
        products.append((product, primary_r))
    except Exception as e:
        problems.append(f"Product {name}: {e}")

# Process and enrich
uploader = SupabaseUploader(dry_run=True)
tier_defs = json.load(open(REPO / "protein-etl/src/data/protein_sources.json", encoding="utf-8"))["tier_definitions"]
enriched = []

for prod, primary_r in products:
    enriched_prod = uploader.process_and_enrich_product(prod)
    enriched_prod.is_vegan = prod.is_vegan
    for v, orig_v in zip(enriched_prod.variants, prod.variants):
        v.is_combo = orig_v.is_combo
        v.is_available = orig_v.is_available
        # Enrich protein source if not set or unclassified
        if primary_r.get("protein_tier") and (not v.ingredient_list or v.protein_profile.protein_tier in (None, "", "Unknown / Unclassified")):
            v.protein_profile.primary_protein_source = primary_r["protein_source"]
            v.protein_profile.protein_tier = tier_defs[primary_r["protein_tier"]]["label"]
    enriched.append(enriched_prod)

# Check baseline products that are in Supabase / seedCatalog.json to preserve full dataset
existing_catalog = json.load(open(REPO / "protein-web/src/data/seedCatalog.json", encoding="utf-8"))
built_slugs = {p.slug for p, _ in products}

audit_lookup = {}
audit_file = HERE / "scratch" / "vegan_audit.json"
if audit_file.exists():
    try:
        for item in json.loads(audit_file.read_text(encoding="utf-8")):
            audit_lookup[item["slug"]] = item["is_vegan"]
    except Exception:
        pass

preserved_count = 0
preserved_raw = []
for ex in existing_catalog:
    # If not rebuilt by this run, preserve it
    if ex["slug"] not in built_slugs:
        # Wrap into ProductWithVariants shape
        brand_name = ex.get("brand_name") or (ex.get("brand") or {}).get("name")
        cat_slug = ex.get("category_slug") or (ex.get("category") or {}).get("slug")
        if ex.get("slug") == "yoga-bar-high-protein-oats-crisps" or "oats-crisp" in ex.get("slug", ""):
            cat_slug = "breakfast-cereals"
            ex["category_slug"] = "breakfast-cereals"
            if "category" in ex and isinstance(ex["category"], dict):
                ex["category"]["slug"] = "breakfast-cereals"
                ex["category"]["name"] = "Breakfast Cereals"
                ex["category"]["icon"] = "🥣"

        if "amul-high-protein-buttermilk" in ex.get("slug", "") or "amul-high-protein-lassi" in ex.get("slug", "") or "amul-high-protein-milkshake" in ex.get("slug", ""):
            cat_slug = "dairy"
            ex["category_slug"] = "dairy"
            if "category" in ex and isinstance(ex["category"], dict):
                ex["category"]["slug"] = "dairy"
                ex["category"]["name"] = "Dairy"
                ex["category"]["icon"] = "🧀"

        is_ex_vegan = audit_lookup.get(ex.get("slug", ""), ex.get("is_vegan", False))
        ex["is_vegan"] = is_ex_vegan
        
        # Build raw and enriched format
        ex_raw = {
            "name": ex["name"],
            "brand_name": brand_name,
            "category_slug": cat_slug,
            "slug": ex["slug"],
            "description": ex.get("description"),
            "image_url": ex.get("image_url"),
            "is_vegan": is_ex_vegan,
            "variants": ex.get("variants", [])
        }
        preserved_raw.append(ex_raw)
        enriched.append(ex) # Keep existing enriched representation
        preserved_count += 1

print(f"Catalog Build Complete: Rebuilt {len(products)} products, preserved {preserved_count} baseline products.")
print(f"Total catalog products: {len(enriched)}")

# Save outputs
raw_output = [p.model_dump(mode="json", exclude_none=True) for p, _ in products] + preserved_raw
(REPO / "protein-etl/data/seed_products.json").write_text(json.dumps(raw_output, indent=2, ensure_ascii=False), encoding="utf-8")

# For seedCatalog.json, output list of dictionaries
web_catalog_output = []
for item in enriched:
    if hasattr(item, "model_dump"):
        web_catalog_output.append(item.model_dump(mode="json"))
    else:
        web_catalog_output.append(item)

(REPO / "protein-web/src/data/seedCatalog.json").write_text(json.dumps(web_catalog_output, indent=2, ensure_ascii=False), encoding="utf-8")

from collections import Counter
print("Brands in new build:", len({p.brand_name for p, _ in products}))
print("Categories in catalog:", dict(Counter(
    p.category_slug if hasattr(p, 'category_slug') else (p.get('category_slug') or (p.get('category') or {}).get('slug'))
    for p in web_catalog_output
)))

for p in problems:
    print("PROBLEM", p)
