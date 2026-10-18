import urllib.request, re, json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

req = urllib.request.Request("https://www.plixlife.com/", headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="ignore")

product_links = set(re.findall(r'href=["\'](/products/[^"\']+)["\']', html))
print(f"Product links found on homepage: {len(product_links)}")
for l in sorted(product_links)[:15]:
    print("  -", l)

m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    print("Plix __NEXT_DATA__ found!")
    pageProps = data.get("props", {}).get("pageProps", {})
    print("pageProps keys:", list(pageProps.keys()))
    with open("protein-etl/data/demo_catalog/scratch/plix_home_next_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved to scratch/plix_home_next_data.json")
else:
    print("__NEXT_DATA__ not found!")

