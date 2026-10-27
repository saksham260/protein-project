import urllib.request, re, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

# Check if there is an Amul API endpoint for products
api_urls = [
    "https://shop.amul.com/api/v1/categories/protein/products",
    "https://shop.amul.com/api/products?category=protein",
    "https://shop.amul.com/en/browse/protein"
]

for url in api_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https://shop\.amul\.com/s/[^"\'\s>]+\.png', content)
            print(f"{url} -> {r.status}, found {len(imgs)} images")
            for i in set(imgs):
                print("  ", i)
    except Exception as e:
        print(f"{url} -> {e}")
