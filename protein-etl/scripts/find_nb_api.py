import urllib.request, re, json

url = "https://nutrabay.com/product/nutrabay-gold-100-whey-protein-concentrate"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode("utf-8", errors="ignore")

scripts = re.findall(r'src="(/_next/static/[^"]+\.js)"', html)
print(f"Next.js scripts found: {len(scripts)}")

app_url = "https://nutrabay.com/_next/static/chunks/pages/_app-8d5f95867a9ba425.js"
with urllib.request.urlopen(urllib.request.Request(app_url, headers={"User-Agent": "Mozilla/5.0"})) as r:
    js = r.read().decode("utf-8", errors="ignore")

idx = js.find('s="https://nutrabay.com/api/product-details"')
if idx != -1:
    # search backwards for JSON.parse
    jp_idx = js.rfind("JSON.parse", 0, idx)
    print("Found JSON.parse at:", jp_idx)
    print(js[jp_idx:idx])




