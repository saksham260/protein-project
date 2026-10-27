import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
urls = [
    "https://www.milkymist.com/greek-yogurt",
    "https://www.milkymist.com/paneer",
    "https://www.milkymist.com/products"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', html)
            print(f"[OK] {u} -> found {len(imgs)} images")
            for img in set(imgs):
                if any(k in img.lower() for k in ['paneer', 'protein', 'curd', 'dahi']):
                    print("  ", img)
    except Exception as e:
        print(f"[ERR] {u}: {e}")
