import urllib.request, re, json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

try:
    req = urllib.request.Request("https://www.plixlife.com/sitemap.xml", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        xml = r.read().decode('utf-8')
        prods = [loc for loc in re.findall(r'<loc>(https://www.plixlife.com/product/[^<]+)</loc>', xml)]
        print(f"Total Plix products in sitemap: {len(prods)}")
        for p in prods:
            if any(k in p for k in ['protein', 'women', 'green', 'superfood']):
                print("  ", p)
except Exception as e:
    print("ERR:", e)
