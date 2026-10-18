import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate", headers=headers)
html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
for item in ld:
    try:
        p = json.loads(item)
        if p.get("@type") == "Product":
            print("Product name:", p.get("name"))
            print("Images:", p.get("image"))
            print("Offers count:", len(p.get("offers", [])))
            for off in p.get("offers", []):
                print("  Offer:", off.get("name"), off.get("price"), off.get("sku"), off.get("availability"))
    except:
        pass
