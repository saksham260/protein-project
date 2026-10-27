import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0"}

try:
    req = urllib.request.Request("https://www.oziva.in/sitemap_products_1.xml", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        xml = r.read().decode('utf-8')
        prods = re.findall(r'<loc>(https://www.oziva.in/products/[^<]+)</loc>', xml)
        print(f"Total OZiva products in sitemap: {len(prods)}")
        for p in prods:
            if 'protein' in p.lower() and 'women' in p.lower():
                print("  ", p)
except Exception as e:
    print("ERR:", e)
