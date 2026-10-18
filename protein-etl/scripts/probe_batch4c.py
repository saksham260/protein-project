"""Probe storefronts for Batch 4C: Fuel One, Kapiva, Bolt Nutrition, XLR8."""
import urllib.request
import json
import ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"
ROOT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

domains = ["fuelone.in", "kapiva.in", "boltnutrition.com", "xlr8sportsnutrition.com"]

for d in domains:
    url = f"https://{d}/products.json?limit=250"
    print(f"Checking {d}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            prods = data.get("products", [])
            print(f"  -> SUCCESS! Found {len(prods)} products on Shopify /products.json")
            prefix = d.split(".")[0]
            with open(ROOT / f"{prefix}_products.json", "w", encoding="utf-8") as out:
                json.dump(prods, out, indent=2)
    except Exception as e:
        print(f"  -> FAILED {url}: {e}")
