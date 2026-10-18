import urllib.request, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"
scratch.mkdir(parents=True, exist_ok=True)

url = "https://nutrabay.com/brand/nutrabay/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="ignore")

m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    print("__NEXT_DATA__ found successfully!")
    with open(scratch / "nutrabay_next_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    pageProps = data.get("props", {}).get("pageProps", {})
    initialState = pageProps.get("initialState", {})
    print("initialState keys:", list(initialState.keys()))
    
    plp = initialState.get("productListingPage", {})
    pbl = plp.get("ProductBrandListing", {})
    print("ProductBrandListing keys:", list(pbl.keys()))
    data_dict = pbl.get("data", {})
    products = data_dict.get("products", []) or pbl.get("products", [])
    print(f"Products in ProductBrandListing: {len(products)}")
    for p in products:
        name = p.get("name") or p.get("title")
        slug = p.get("slug")
        price = p.get("price")
        mrp = p.get("marketPrice") or p.get("mrp")
        category = p.get("categoryName") or p.get("category")
        print(f"  - {name} (slug: {slug}, price: {price}, mrp: {mrp}, cat: {category})")
else:
    print("__NEXT_DATA__ not found in HTML!")
