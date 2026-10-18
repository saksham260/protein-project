"""Inspect nutrition tables found in batch4c_images."""
from pathlib import Path
from rapidocr import RapidOCR

engine = RapidOCR()
p = Path("protein-etl/data/demo_catalog/scratch/batch4c_images")

# Key test images
test_tags = [
    "kapiva_testofuel_0.jpg",
    "kapiva_testofuel_3.jpg",
    "kapiva_testofuel_4.jpg",
    "fuelone_fuel-one-whey-max_0.jpg",
    "fuelone_fuel-one-whey-max_2.jpg",
    "fuelone_fuel-one-iso-max_0.jpg",
    "fuelone_fuel-one-iso-max_2.jpg",
    "fuelone_fuel-one-whey-protein_0.jpg",
    "fuelone_fuel-one-whey-protein_2.jpg",
    "fuelone_fuel-one-impact-whey_0.jpg",
    "fuelone_fuel-one-impact-whey_2.jpg",
    "bolt_whey-protein-5l_1.jpg",
    "bolt_whey-protein-5l_2.jpg",
    "bolt_whey-protein-5l_9.jpg",
    "bolt_whey-protein-5l_10.jpg"
]

for tag in test_tags:
    img_file = p / tag
    if not img_file.exists():
        continue
    lines = engine(str(img_file)).txts or []
    nutr = [l for l in lines if any(k in l.lower() for k in ["protein", "energy", "calories", "carbohydrate", "fat", "serving", "sugar", "sodium"])]
    if len(nutr) >= 3:
        print(f"\n==================== {tag} ({len(lines)} lines) ====================")
        for i, l in enumerate(lines):
            if any(k in l.lower() for k in ["nutrition", "protein", "energy", "calories", "carbohydrate", "fat", "serving", "sugar", "sodium", "ingredients", "cholesterol"]):
                print(f"  {i:2d}: {l}")
