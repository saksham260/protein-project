import urllib.request, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"

url = "https://www.plixlife.com/product/plant-protein-powder"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="ignore")

m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if m:
    d = json.loads(m.group(1))
    ppd = d.get("props", {}).get("pageProps", {}).get("productPageData", {})
    print("productPageData keys:", list(ppd.keys()))
    with open(scratch / "plix_sample_pdp.json", "w", encoding="utf-8") as f:
        json.dump(ppd, f, indent=2, ensure_ascii=False)
    
    p = ppd.get("product", {})
    print("Product name:", p.get("name"))
    print("Product slug:", p.get("slug"))
    print("All keys:", list(p.keys()))
    variants = p.get("variants", [])
    print(f"Variants ({len(variants)}):")
    for v in variants:
        v_name = v.get("name")
        v_sku = v.get("sku")
        v_pricing = v.get("pricing", {})
        price = v_pricing.get("price", {}).get("gross", {}).get("amount")
        mrp = v_pricing.get("priceUndiscounted", {}).get("gross", {}).get("amount")
        print(f"  Variant: {v_name} | SKU: {v_sku} | Price: {price} | MRP: {mrp}")

    media = p.get("media", [])
    print(f"Media images ({len(media)}):")
    for m in media:
        print("  -", m.get("url"))
    
    # Check metadata
    print("Metadata keys/items:")
    for item in p.get("metadata", []):
        print(f"  {item.get('key')}: {str(item.get('value'))[:100]}...")
