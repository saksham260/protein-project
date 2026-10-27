import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
url = "https://muscletech.in"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print("Status:", r.status, "Length:", len(html))
        # Look for search suggest or products
        imgs = re.findall(r'https://cdn\.shopify\.com/s/files/[^\s"\'<>]+\.(?:jpg|png|webp)', html)
        print("Shopify images found:", len(imgs))
        for img in set(imgs)[:5]:
            print(" ", img)
except Exception as e:
    print("ERR:", e)
