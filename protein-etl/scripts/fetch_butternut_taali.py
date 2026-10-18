import urllib.request
import json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')
ROOT.mkdir(parents=True, exist_ok=True)

# 1. Fetch Butternut Co products
print("Fetching The Butternut Company products...")
url_bn = "https://www.thebutternutcompany.com/products.json?limit=250"
req_bn = urllib.request.Request(url_bn, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_bn, timeout=12) as r:
    bn_data = json.loads(r.read())
bn_products = bn_data.get("products", [])
print(f"Found {len(bn_products)} products for The Butternut Company")
with open(ROOT / "butternut_products.json", "w", encoding="utf-8") as f:
    json.dump(bn_products, f, indent=2)

# 2. Fetch Taali Foods products
print("\nFetching Taali Foods products...")
url_taali = "https://taalifoods.in/products.json?limit=250"
req_taali = urllib.request.Request(url_taali, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_taali, timeout=12) as r:
    taali_data = json.loads(r.read())
taali_products = taali_data.get("products", [])
print(f"Found {len(taali_products)} products for Taali Foods")
with open(ROOT / "taalifoods_products.json", "w", encoding="utf-8") as f:
    json.dump(taali_products, f, indent=2)

print("\nSaved both product feeds to scratch!")
