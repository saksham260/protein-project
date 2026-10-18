import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("https://avvatarindia.com/categories/performance-whey", headers=headers)
html = urllib.request.urlopen(req).read().decode("utf-8")
links = set(re.findall(r'href="([^"]*product/[^"]*)"', html))
for l in sorted(links):
    if not l.startswith("$"):
        print("Performance Whey:", l)
