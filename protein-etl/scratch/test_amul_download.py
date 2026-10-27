import urllib.request

urls = [
    ('amul-high-protein-milk', 'https://shop.amul.com/s/62fa94df8c13af2e242eba16/671b30a3caec6f032c8154ed/amul-high-protein-milk.png'),
    ('amul-high-protein-probiotic-dahi', 'https://shop.amul.com/s/62fa94df8c13af2e242eba16/671b30a3caec6f032c8154ed/amul-high-protein-dahi.png')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://shop.amul.com/'
}

for slug, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
            print(f"[OK] {slug} -> Status: {r.status}, Content-Type: {r.headers.get('content-type')}, Size: {len(data)}")
    except Exception as e:
        print(f"[ERR] {slug} -> {e}")
