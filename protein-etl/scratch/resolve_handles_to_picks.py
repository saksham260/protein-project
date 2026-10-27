import json

# Load picks.txt
picks = []
with open('protein-etl/data/demo_catalog/picks.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split('|')
            picks.append(parts)

# Load manual_entries
manual = {}
with open('protein-etl/data/demo_catalog/manual_entries.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            obj = json.loads(line)
            manual[obj['handle']] = obj

# Load seed_products.json to get generated slug
with open('protein-etl/data/seed_products.json', 'r', encoding='utf-8') as f:
    seeds = json.load(f)

seed_by_slug = {p['slug']: p for p in seeds}

# Load the broken items from task-720
broken_slugs = [
    "nutrabay-pure-100-raw-whey-protein-concentrate",
    "nutrabay-gold-hydrolyzed-pea-protein-isolate",
    "nutrabay-gold-tri-blend-whey-protein",
    "nutrabay-gold-100-whey-protein-concentrate",
    "amul-high-protein-probiotic-dahi",
    "nutrabay-wellness-vegan-plant-protein-powder-with-superfoods",
    "amul-high-protein-milk",
    "bigmuscles-nutrition-real-mass-gainer",
    "wellbeing-nutrition-superfood-plant-protein-french-vanilla",
    "plix-women-plant-protein",
    "oziva-superfood-plant-protein-for-women",
    "epigamia-high-protein-greek-yogurt-natural-no-added-sugar",
    "epigamia-high-protein-greek-yogurt-alphonso-mango",
    "epigamia-high-protein-greek-yogurt-strawberry",
    "epigamia-high-protein-greek-yogurt-wild-blueberry",
    "ensure-original-complete-balanced-adult-nutrition",
    "ensure-diabetes-care-specialized-nutrition",
    "glucerna-specialized-diabetes-nutritional-drink",
    "ensure-plus-high-protein-recovery-drink",
    "milky-mist-high-protein-low-fat-paneer",
    "milky-mist-high-protein-greek-yogurt-natural-unsweetened",
    "gritzo-supermilk-for-young-athletes-boys-13-yrs",
    "gritzo-supermilk-for-young-athletes-girls-13-yrs",
    "urban-platter-organic-non-gmo-firm-tofu-block",
    "pediasure-complete-balanced-growth-nutrition-chocolate",
    "pediasure-complete-balanced-growth-nutrition-vanilla",
    "ultimate-nutrition-prostar-100-whey-protein-chocolate-creme",
    "ultimate-nutrition-iso-sensation-93-100-pure-whey-isolate-natural-chocolate",
    "muscletech-nitrotech-ripped-hybrid-whey-protein-french-vanilla"
]

print(f"Analyzing {len(broken_slugs)} broken slugs:")

for s in broken_slugs:
    p = seed_by_slug.get(s)
    # Find matching pick
    matching_pick = None
    for pick in picks:
        store, handle = pick[0], pick[1]
        if handle in s or s in handle or (p and p['name'].lower() in handle):
            matching_pick = pick
            break
    print(f"Slug: {s}")
    print(f"  Current image_url: {p.get('image_url') if p else 'NOT IN SEED'}")
    if matching_pick:
        print(f"  Matching pick: store={matching_pick[0]}, handle={matching_pick[1]}")
        m_obj = manual.get(matching_pick[1])
        if m_obj:
            print(f"  Manual entry image_url: {m_obj.get('image_url')}")
    print()
