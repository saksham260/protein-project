import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
seed = json.load(open(REPO / "protein-etl/data/seed_products.json", encoding="utf-8"))
web = json.load(open(REPO / "protein-web/src/data/seedCatalog.json", encoding="utf-8"))
picks = [l.split("|") for l in (REPO / "protein-etl/data/demo_catalog/picks.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
manual_path = REPO / "protein-etl/data/demo_catalog/manual_entries.jsonl"
manual = [json.loads(l) for l in manual_path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]

print(f"seed_products: {len(seed)} | seedCatalog: {len(web)} | picks: {len(picks)} | manual entries: {len(manual)}")

cat_count = Counter(p["category_slug"] for p in seed)
brand_prod = Counter(p["brand_name"] for p in seed)
brand_cats = defaultdict(Counter)
cat_brands = defaultdict(set)
vegan = Counter()
var_count = 0
img_null = Counter()
price_by_cat = defaultdict(list)
cpg_by_cat = defaultdict(list)
tags = Counter()
sources = Counter()
for p in seed:
    c = p["category_slug"]
    brand_cats[p["brand_name"]][c] += 1
    cat_brands[c].add(p["brand_name"])
    if p.get("is_vegan"):
        vegan[c] += 1
    if not p.get("image_url"):
        img_null[c] += 1
    for v in p.get("variants", []):
        var_count += 1
        price_by_cat[c].append(v.get("mrp_inr") or 0)
        m = v.get("computed_metrics") or {}
        if m.get("cost_per_g_protein"):
            cpg_by_cat[c].append(m["cost_per_g_protein"])
        for t in v.get("dietary_tags") or []:
            tags[t.lower()] += 1
        pp = v.get("protein_profile") or {}
        if pp.get("primary_protein_source"):
            sources[pp["primary_protein_source"]] += 1

print(f"variants: {var_count} | brands: {len(brand_prod)}\n")
print("=== CATEGORIES ===")
for c, n in cat_count.most_common():
    prices = sorted(price_by_cat[c]); cpg = sorted(cpg_by_cat[c])
    med = prices[len(prices)//2] if prices else 0
    cmed = cpg[len(cpg)//2] if cpg else 0
    print(f"{c:20s} products={n:3d} brands={len(cat_brands[c]):2d} vegan={vegan[c]:3d} no_img={img_null[c]:2d} median_mrp={med:7.0f} median_cpg={cmed:5.2f}")

print("\n=== BRANDS (products | categories) ===")
for b, n in brand_prod.most_common():
    print(f"{b:32s} {n:3d} | " + ", ".join(f"{c}:{k}" for c, k in brand_cats[b].most_common()))

print("\n=== SINGLE-PRODUCT BRANDS ===")
print([b for b, n in brand_prod.items() if n == 1])

print("\n=== PROTEIN SOURCES ===")
for s, n in sources.most_common(25):
    print(f"  {s}: {n}")

print("\n=== TOP DIETARY TAGS ===")
for t, n in tags.most_common(25):
    print(f"  {t}: {n}")

print("\n=== PICK SOURCES (store domains) ===")
for s, n in Counter(p[0] for p in picks).most_common():
    print(f"  {s}: {n}")
