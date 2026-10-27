import urllib.request, re

import ssl

ctx = ssl._create_unverified_context()
headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.abbottnutrition.in"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print("Status:", r.status, "Length:", len(html))
        imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|png|webp)', html)
        print("Total images:", len(set(imgs)))
        for i in set(imgs):
            print("  ", i)
except Exception as e:
    print("ERR:", e)
