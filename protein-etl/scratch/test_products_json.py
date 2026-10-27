import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

stores = {
    'Ketofy': 'https://www.ketofy.in/products.json?limit=5',
    'OZiva': 'https://www.oziva.in/products.json?limit=5',
    'Kapiva': 'https://kapiva.in/products.json?limit=5',
    'Plix': 'https://www.plixlife.com/products.json?limit=5',
    'Urban Platter': 'https://urbanplatter.in/products.json?limit=5',
    'Milky Mist': 'https://shop.milkymist.com/products.json?limit=5',
    'MuscleTech': 'https://muscletech.in/products.json?limit=5'
}

for name, url in stores.items():
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            prods = data.get('products', [])
            print(f"{name:15} -> OK ({len(prods)} products in products.json)")
    except Exception as e:
        print(f"{name:15} -> ERR: {e}")
