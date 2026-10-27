import urllib.request, re, json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

urls = [
    ("myprotein-impact-whey-isolate-chocolate-smooth", "https://www.myprotein.co.in/sports-nutrition/impact-whey-isolate/10530911.html"),
    ("myprotein-clear-whey-isolate-orange-mango", "https://www.myprotein.co.in/sports-nutrition/clear-whey-isolate/12081395.html")
]

for slug, url in urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https://[^\s"\'<>]*thcdn\.com/images/[^\s"\'<>]+\.(?:jpg|png|webp)', html)
            imgs = list(dict.fromkeys(imgs))
            print(f"Product images on {slug}: {len(imgs)}")
            for img in imgs[:5]:
                print(" ", img)
    except Exception as e:
        print(f"ERR for {slug}: {e}")
