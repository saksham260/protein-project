import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

# Find occurrences of '/product/'
matches = [m.start() for m in re.finditer(r'/product/', js)]
print(f"Found {len(matches)} occurrences of /product/")
for idx in matches[:5]:
    start = max(0, idx - 100)
    end = min(len(js), idx + 200)
    print("---")
    print(js[start:end])
