import json
from pathlib import Path

HERE = Path("protein-etl/data/demo_catalog")
report = json.loads(Path("protein-etl/scratch/missing_images_report.json").read_text(encoding="utf-8"))
missing_slugs = {p["slug"] for p in report["missing_products"]}

seed = json.loads(Path("protein-web/src/data/seedCatalog.json").read_text(encoding="utf-8"))
imaged_products = [p for p in seed if p.get("image_url")]

# Check exact/near duplicates already in seedCatalog.json with working images
exact_duplicates = [
    ("raw-pressery-high-protein-milkshake-cold-coffee", "raw-pressery-high-protein-milkshake-cold-coffee (line 412 in picks.txt, image already in Supabase Storage)"),
    ("ritebite-max-protein-7-grain-breakfast-protein-cookie-choco-almond", "max-protein-7-grain-breakfast-protein-cookie-choco-almond (already in catalog with image)"),
    ("ritebite-max-protein-7-grain-breakfast-protein-cookie-nuts-seeds", "max-protein-7-grain-protein-cookie-nuts-seeds (already in catalog with image in Supabase Storage)"),
    ("ritebite-max-protein-7-grain-breakfast-protein-cookie-oats-raisins", "max-protein-7-grain-protein-cookie-oats-raisins (already in catalog with image in Supabase Storage)"),
    ("open-secret-unjunked-high-protein-peanut-butter-cookies", "open-secret-peanut-butter-nutty-cookies (already in catalog with image)"),
    ("the-whole-truth-soft-baked-protein-cookie-double-dark-chocolate", "the-whole-truth-protein-cookie-dark-chocolate (already in catalog with image)"),
    ("aashirvaad-proactive-high-protein-atta", "aashirvaad-proactive-high-protein-multigrain-atta (duplicate product added in Wave 1 vs Batch 5)"),
    ("fortune-soya-chunks-protein-rich", "fortune-soya-chunks-99-fat-free (duplicate product added in Wave 1 vs Batch 5)"),
    ("ensure-plus-high-protein-vanilla", "ensure-plus-high-protein-recovery-drink (duplicate product added in Wave 4 vs Batch 5)"),
    ("ensure-diabetes-care-vanilla", "ensure-diabetes-care-specialized-nutrition (duplicate product added in Wave 4 vs Batch 5)"),
    ("labrada-muscle-mass-gainer-chocolate", "labrada-muscle-mass-gainer (duplicate product added in Wave 2 vs baseline)"),
]

print(f"Identified {len(exact_duplicates)} duplicate/overlapping SKUs created during Waves 1-4.")

