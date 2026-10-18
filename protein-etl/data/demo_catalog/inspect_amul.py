import httpx, re

headers = {"User-Agent": "Mozilla/5.0"}
r = httpx.get("https://shop.amul.com/en/browse/protein", headers=headers, timeout=10.0)
hrefs = re.findall(r'href=["\']([^"\']+)["\']', r.text)
print("Total hrefs on page:", len(hrefs))
for h in sorted(set(hrefs)):
    if any(k in h.lower() for k in ["protein", "paneer", "whey", "buttermilk", "lassi", "shake"]):
        print(" ", h)
