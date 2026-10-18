import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
req = urllib.request.Request("https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093", headers=headers)
html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
for item in ld:
    try:
        p = json.loads(item)
        t = p.get("@type")
        if t == "Product" or (isinstance(t, list) and "Product" in t):
            print("Name:", p.get("name"))
            print("Image:", p.get("image"))
            print("Offers:", p.get("offers"))
            print("Brand:", p.get("brand"))
            print("Description:", (p.get("description") or "")[:200])
    except Exception as e:
        print("Parse error:", e)
