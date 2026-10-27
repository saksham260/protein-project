import json
import urllib.request
import urllib.parse

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = "https://eatbetterco.com/products.json?limit=250"
req = urllib.request.Request(url, headers=HEADERS)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        prods = data.get('products', [])
        print(f"Total Eat Better Co products: {len(prods)}")
        for p in prods:
            title = p.get('title', '')
            if 'seed' in title.lower() or 'trail' in title.lower() or 'spicy' in title.lower():
                print(f"  {title} | handle: {p.get('handle')}")
                if p.get('images'):
                    print(f"    img: {p['images'][0].get('src')}")
except Exception as e:
    print("ERR:", e)
