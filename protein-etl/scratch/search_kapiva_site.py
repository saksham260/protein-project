import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://kapiva.in/search.php?search_query=protein"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print("Search status 200, length:", len(html))
        prods = re.findall(r'href="(/[^"]*protein[^"]*)"', html, re.I)
        print("Product links found:", len(set(prods)))
        for p in set(prods):
            print("  Link:", p)
        imgs = list(set(re.findall(r'https://[^\s"\'<>]+\.(?:jpg|png|webp)', html)))
        print("Images found:", len(imgs))
        for img in imgs:
            if any(k in img.lower() for k in ['protein', 'women', 'dia', 'product']):
                print("  Img:", img)
except Exception as e:
    print("ERR:", e)
