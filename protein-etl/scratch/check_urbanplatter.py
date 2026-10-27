import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://urbanplatter.in/search?q=firm+tofu"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print("Status 200, length:", len(html))
        imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|png|webp)', html)
        for i in set(imgs):
            if 'tofu' in i.lower():
                print("  ", i)
except Exception as e:
    print("ERR:", e)
