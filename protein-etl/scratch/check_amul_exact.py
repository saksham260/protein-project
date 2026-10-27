import urllib.request, re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

urls = [
    "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-30",
    "https://shop.amul.com/en/product/amul-high-protein-dahi-400-g-or-pack-of-2"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            print(f"=== {u} ===")
            imgs = re.findall(r'https://shop\.amul\.com/s/[^"\'\s>]+\.png', html)
            for i in set(imgs):
                if 'logo' not in i and 'favicon' not in i:
                    print("  ", i)
    except Exception as e:
        print("ERR:", e)
