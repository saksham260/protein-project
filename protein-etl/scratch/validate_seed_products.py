import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "protein-etl"))

from src.models import ProductCreate

items = json.load(open(ROOT / "protein-etl/data/seed_products.json", encoding="utf-8"))
print("Total items in seed_products.json:", len(items))

valid = 0
errors = 0
for i, item in enumerate(items):
    try:
        p = ProductCreate(**item)
        valid += 1
    except Exception as e:
        print(f"Error on item {i} ({item.get('slug')}): {e}")
        errors += 1

print(f"Validation complete: {valid} valid, {errors} errors")
