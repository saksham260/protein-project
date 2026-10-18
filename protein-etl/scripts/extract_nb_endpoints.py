import urllib.request, re

scripts = [
    "/_next/static/chunks/pages/_app-8d5f95867a9ba425.js",
    "/_next/static/chunks/394-acab6f68132cd051.js",
    "/_next/static/chunks/586-214e559ab59c721a.js",
    "/_next/static/chunks/2344-2e77a4c2a08f8984.js",
    "/_next/static/chunks/pages/product/%5BproductTitle%5D-4132547d43301834.js"
]

for s in scripts:
    s_url = "https://nutrabay.com" + s
    try:
        with urllib.request.urlopen(urllib.request.Request(s_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=10) as r:
            js = r.read().decode("utf-8", errors="ignore")
            # Look for baseURL, api.nutrabay.com, or endpoints
            base_urls = set(re.findall(r'https?://[a-zA-Z0-9.-]+\.nutrabay\.com', js))
            api_paths = set(re.findall(r'/(?:api|v[0-9]|catalog|product)[a-zA-Z0-9/_-]*', js))
            print(f"=== {s} ===")
            if base_urls:
                print("  base_urls:", base_urls)
            interesting_paths = [p for p in api_paths if any(k in p for k in ["parent", "detail", "item", "variant", "product"])]
            if interesting_paths:
                print("  paths:", interesting_paths[:10])
    except Exception as e:
        print(s, "failed:", e)
