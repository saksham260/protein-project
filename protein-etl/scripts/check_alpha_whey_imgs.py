import urllib.request, re, json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.avvatarindia.com/product/alpha-whey-belgian-chocolate-flavour-1-kg-2509104129-263"
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode("utf-8")
imgs = re.findall(r'(/images/nutrition_images/[^"\'\s>]+)', html)
for img in sorted(set(imgs)):
    print("Alpha Whey Nut Img:", img)
