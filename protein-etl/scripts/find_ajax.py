import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

# Look for fetch or api calls around product loading
matches = [m.start() for m in re.finditer(r'product_id|get_product|fetch_product|\.alias', js)]
print(f"Found {len(matches)} matches")

# Let's search for how HTTP requests are sent in mystore_vue
ajax_matches = [m.start() for m in re.finditer(r'\$\.ajax|axios|fetch\(', js)]
print(f"AJAX matches: {len(ajax_matches)}")
for idx in ajax_matches[:10]:
    start = max(0, idx - 50)
    end = min(len(js), idx + 250)
    print("--- AJAX ---")
    print(js[start:end])
