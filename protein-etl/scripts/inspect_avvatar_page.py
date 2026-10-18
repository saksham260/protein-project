import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
req = urllib.request.Request("https://avvatarindia.com/product/100-performance-whey-belgain-chocolate-flavour-1-kg", headers=headers)
html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")

og_tags = dict(re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', html))
h1 = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.S)]

# Look for price patterns
prices = re.findall(r'class="[^"]*price[^"]*"[^>]*>(.*?)<', html, re.I)
clean_prices = [p.strip() for p in prices if p.strip()]

res = {
    "og": og_tags,
    "h1": h1,
    "prices": clean_prices[:10],
}
with open("protein-etl/data/demo_catalog/avvatar_sample.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)

print("Saved avvatar sample successfully.")
