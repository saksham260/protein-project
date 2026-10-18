import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
req = urllib.request.Request("https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093", headers=headers)
html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
print("MB HTML length:", len(html))
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
print("MB ld+json count:", len(ld))
for item in ld:
    try:
        p = json.loads(item)
        if isinstance(p, dict):
            print("Type:", p.get("@type"))
            if p.get("@type") == "Product":
                print("  Name:", p.get("name"))
                print("  Image:", p.get("image"))
                print("  Offers:", p.get("offers"))
    except Exception as e:
        print("Parse error:", e)
