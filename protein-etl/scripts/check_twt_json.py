import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0"}
def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)

status, body = fetch("https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate.json")
print("TWT .json status:", status)
if status == 200:
    data = json.loads(body)
    p = data.get("product", {})
    print("TWT is Shopify! Title:", p.get("title"))
    print("Variants:", len(p.get("variants", [])))
    for v in p.get("variants", []):
        print("  Variant:", v.get("title"), "Price:", v.get("price"), "Grams:", v.get("grams"))
    print("Images:", len(p.get("images", [])))
else:
    # Let's inspect the ld+json from the HTML
    status, html = fetch("https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate")
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    for idx, item in enumerate(ld):
        try:
            parsed = json.loads(item)
            print(f"LD {idx} type:", parsed.get("@type"))
            if parsed.get("@type") == "Product":
                print("  Product:", parsed.get("name"), parsed.get("offers"))
        except Exception as e:
            print(f"LD {idx} err:", e)
