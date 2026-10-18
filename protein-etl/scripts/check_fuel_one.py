import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.muscleblaze.com/sv/fuel-one-whey-protein/SP-72739"
req = urllib.request.Request(url, headers=headers)
try:
    html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    for item in ld:
        try:
            p = json.loads(item)
            if p.get("@type") == "Product" or (isinstance(p.get("@type"), list) and "Product" in p.get("@type")):
                print("Found Fuel One product:", p.get("name"), "Price:", p.get("offers", {}).get("price"))
        except:
            pass
except Exception as e:
    print("Err:", e)
