import urllib.request
import re
import json
from pathlib import Path

ROOT = Path('protein-etl/data/demo_catalog/scratch')
ROOT.mkdir(parents=True, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    'https://shop.amul.com/en/browse/protein',
    'https://shop.amul.com/en/browse/milk',
    'https://shop.amul.com/en/browse/dahi-and-yoghurt'
]

all_links = set()

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8', errors='ignore')
        print(f'{url}: length {len(html)}')
        
        # Check __NEXT_DATA__
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        if m:
            d = json.loads(m.group(1))
            props = d.get('props', {}).get('pageProps', {})
            print('  __NEXT_DATA__ found! Keys:', list(props.keys()))
            prods = props.get('products') or props.get('initialData', {}).get('products') or []
            print(f'  Products in NEXT_DATA: {len(prods)}')
            for p in prods:
                name = p.get('name') or p.get('title')
                slug = p.get('slug') or p.get('handle')
                print(f'    - {name} ({slug})')
        
        links = re.findall(r'href=["\'](/en/product/[^"\']+)["\']', html)
        for l in links:
            all_links.add(l)
    except Exception as e:
        print(f'{url} failed: {e}')

print(f'\nTotal unique product links: {len(all_links)}')
for l in sorted(all_links):
    if any(k in l.lower() for k in ['protein', 'milk', 'dahi', 'curd', 'shake', 'lassi']):
        print(' ', l)
