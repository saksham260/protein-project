import urllib.request
import json
from pathlib import Path

# Search Nutrabay API for brand: Nutrabay
# Let's try multiple endpoints or categories
urls = [
    'https://nutrabay.com/api/search/product-list?brand=nutrabay&page=1&per_page=50',
    'https://nutrabay.com/api/search/product-list?q=nutrabay+protein&page=1&per_page=50',
    'https://nutrabay.com/api/category/products?category=proteins&brand=nutrabay&page=1&per_page=50'
]

ROOT = Path('protein-etl/data/demo_catalog/scratch')
ROOT.mkdir(parents=True, exist_ok=True)

for url in urls:
    print('Testing URL:', url)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            products = data.get('data', {}).get('products', []) or data.get('data', {}).get('items', [])
            print(f'-> Found {len(products)} products')
            if products:
                with open(ROOT / 'nb_brand_products.json', 'w', encoding='utf-8') as f:
                    json.dump(products, f, indent=2)
                for p in products[:10]:
                    pid = p.get('id') or p.get('product_id')
                    name = p.get('name') or p.get('title')
                    price = p.get('selling_price') or p.get('price')
                    print(f'   [{pid}] {name} - Rs. {price}')
                break
    except Exception as e:
        print('  Failed:', e)
