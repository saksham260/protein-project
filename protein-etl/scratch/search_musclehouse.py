import json
import urllib.request
import urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

queries = [
    ("dymatize-iso100-gourmet-chocolate", "dymatize iso 100 chocolate"),
    ("dymatize-iso100-birthday-cake", "dymatize iso 100 birthday cake"),
    ("dymatize-elite-whey", "dymatize elite whey"),
    ("labrada-mass-gainer", "labrada mass gainer")
]

for slug, q in queries:
    url = f"https://musclehouseindia.com/search/suggest.json?q={urllib.parse.quote(q)}&resources[type]=product&resources[options][unavailable_products]=show"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            prods = data.get('resources', {}).get('results', {}).get('products', [])
            print(f"\n=== Query: {q} (Slug: {slug}) -> Found {len(prods)} ===")
            for p in prods[:3]:
                print(f"  Title: {p.get('title')}")
                print(f"  Handle: {p.get('handle')}")
                print(f"  Image: {p.get('image')}")
    except Exception as e:
        print(f"Error for {slug}: {e}")
