import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

# Find strings starting with /api or /ms/
api_urls = set(re.findall(r'["\'](/api/[^"\']+)["\']', js))
print(f"API URLs ({len(api_urls)}):")
for u in sorted(api_urls):
    print(" ", u)

ms_urls = set(re.findall(r'["\'](/ms/[^"\']+)["\']', js))
print(f"\nMS URLs ({len(ms_urls)}):")
for u in sorted(ms_urls)[:25]:
    print(" ", u)

# Check search endpoint or products endpoint
search_matches = set(re.findall(r'["\']([^"\']*(?:search|browse|category|product)[^"\']*)["\']', js))
filtered = [m for m in search_matches if "/" in m and len(m) < 60]
print(f"\nFiltered paths ({len(filtered)}):")
for m in sorted(filtered)[:25]:
    print(" ", m)
