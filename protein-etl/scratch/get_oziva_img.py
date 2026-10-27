import urllib.request, re, json

url = "https://www.oziva.in/products/oziva-protein-herbs-women-whey-protein-powder-with-ayurvedic-herbs-multivitamins-soy-free-gluten-free-no-preservatives"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8')

# Search for LD JSON or Shopify image URLs
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
for item in ld:
    try:
        p = json.loads(item)
        if p.get("@type") == "Product":
            print("Product Name:", p.get("name"))
            print("Product Image:", p.get("image"))
    except:
        pass

imgs = re.findall(r'https://cdn\.shopify\.com/s/files/1/2393/2199/[^\s"\'<>]+(?:png|jpg|jpeg|webp)', html)
imgs = list(dict.fromkeys(imgs))

for i in imgs:
    if any(k in i.lower() for k in ["choco", "phw", "women", "herbs"]):
        print("Candidate img:", i)
