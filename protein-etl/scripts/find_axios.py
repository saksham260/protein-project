import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

# Find axios( or axios.get( or axios.post(
pos = 0
matches = []
for m in re.finditer(r'axios\s*\(', js):
    p = m.start()
    matches.append(js[max(0, p-80):min(len(js), p+250)])

print(f"Found {len(matches)} axios calls:")
for m in matches[:5]:
    print("---")
    print(m)
