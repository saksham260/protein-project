import urllib.request, re

url = "https://nutrabay.com/_next/static/chunks/pages/product/%5BproductTitle%5D-4132547d43301834.js"
with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})) as r:
    js = r.read().decode("utf-8", errors="ignore")

# Search for strings containing endpoints or actions
strings = re.findall(r'"([^"\\]{4,80})"', js)
candidates = [s for s in strings if any(k in s for k in ["product", "parent", "detail", "variant", "inventory", "price", "nutrition"])]
print("Relevant string constants in PDP chunk:")
for c in sorted(set(candidates))[:30]:
    print(" -", c)
