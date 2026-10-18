import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")

html = fetch("https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate")
print("TWT HTML length:", len(html))

next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
if next_data:
    print("Found __NEXT_DATA__! Parsing JSON...")
    data = json.loads(next_data[0])
    page_props = data.get("props", {}).get("pageProps", {})
    print("Keys in pageProps:", list(page_props.keys()))
    prod = page_props.get("product") or page_props.get("initialData") or page_props.get("data")
    if prod:
        print("Product keys:", list(prod.keys()) if isinstance(prod, dict) else type(prod))
        if isinstance(prod, dict):
            print("Title:", prod.get("title") or prod.get("name"))
            print("Variants:", len(prod.get("variants", [])))
            for v in prod.get("variants", [])[:4]:
                print("  Var:", v.get("title") or v.get("name"), v.get("price"), v.get("weight"))
else:
    print("No __NEXT_DATA__, checking for script/json...")
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    print("ld+json count:", len(ld))
