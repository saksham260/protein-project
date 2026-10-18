import httpx, re

headers = {"User-Agent": "Mozilla/5.0"}
r = httpx.get("https://www.avvatarindia.com/", headers=headers, timeout=10.0, follow_redirects=True)
all_links = set(re.findall(r'href=["\']([^"\']+)["\']', r.text))
product_links = [l for l in all_links if any(k in l.lower() for k in ["whey", "isorich", "alpha", "product", "protein"])]
print("Total Avvatar product-like links:", len(product_links))
for l in sorted(product_links)[:25]:
    print(" ", l)
