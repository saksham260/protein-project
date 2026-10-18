import json, re

html = open("protein-etl/scripts/inspect_avvatar_page.py").read()
# Let's inspect the cached response or fetch and save the html
import urllib.request
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("https://avvatarindia.com/product/100-performance-whey-belgain-chocolate-flavour-1-kg", headers=headers)
raw_html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")

# Find images
imgs = re.findall(r'<img\b[^>]*src="([^"]+)"[^>]*>', raw_html)
prod_imgs = [img for img in imgs if "product" in img.lower() or "parag" in img.lower() or "upload" in img.lower() or "media" in img.lower()]

# Find details block around the H1
idx = raw_html.find("Avvatar Performance Whey | 1 Kg | Belgian Chocolate Flavour")
snippet = raw_html[max(0, idx-500):idx+2000] if idx != -1 else ""

res = {
    "prod_imgs": prod_imgs[:10],
    "all_imgs": [img for img in imgs if not img.endswith(".svg") and not "icon" in img.lower()][:15],
    "snippet": snippet
}
with open("protein-etl/data/demo_catalog/avvatar_detail.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("Saved detail. Snippet len:", len(snippet), "Prod imgs:", len(prod_imgs))
