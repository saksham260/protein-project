import urllib.request, json, urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"}

# Nutrabay search API or sitemap
q = "Gold 100% Whey Protein Concentrate"
url = f"https://nutrabay.com/api/search/search-products?search_term={urllib.parse.quote(q)}"

try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
        print("Search API Response keys:", list(d.keys()))
        prods = d.get('data', {}).get('products', []) or d.get('products', [])
        print(f"Found {len(prods)} products:")
        for p in prods[:5]:
            print(" ", p.get('name'), "| PID:", p.get('product_id'), "| img:", p.get('featured_image') or p.get('thumbnail'))
except Exception as e:
    print("ERR:", e)
