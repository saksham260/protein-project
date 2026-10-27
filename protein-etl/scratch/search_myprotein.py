import urllib.request, re, json, urllib.parse

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

queries = [
    ("myprotein-impact-whey-isolate-chocolate-smooth", "impact whey isolate"),
    ("myprotein-clear-whey-isolate-orange-mango", "clear whey isolate")
]

for slug, q in queries:
    url = f"https://www.myprotein.co.in/elysium.search?search={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            # Look for product URLs and s1.thcdn.com or static.thcdn.com images
            imgs = re.findall(r'https://[^\s"\'<>]*(?:thcdn\.com|myprotein)[^\s"\'<>]+\.(?:jpg|png|webp)', html)
            imgs = list(dict.fromkeys(imgs))
            print(f"\n{slug} -> Found {len(imgs)} images")
            for img in imgs[:5]:
                print("  ", img)
    except Exception as e:
        print(f"ERR for {slug}: {e}")
