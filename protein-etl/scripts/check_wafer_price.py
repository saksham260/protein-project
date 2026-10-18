import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.avvatarindia.com/product/protein-wafer-bar-coffee-flavour-320g"
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode("utf-8")
m = re.findall(r'price-box.*?</div>', html, re.S)
with open("protein-etl/data/demo_catalog/wafer_price.txt", "w", encoding="utf-8") as f:
    for x in m:
        f.write(x + "\n")
print("Saved wafer_price.txt")
