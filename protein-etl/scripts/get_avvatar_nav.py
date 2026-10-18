import urllib.request, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
req = urllib.request.Request("https://avvatarindia.com/", headers=headers)
html = urllib.request.urlopen(req).read().decode("utf-8")
cat_links = set(re.findall(r'href="([^"]*(?:categories|product)[^"]*)"', html))
for l in sorted(cat_links):
    if not l.startswith("$"):
        print("Avvatar Link:", l)
