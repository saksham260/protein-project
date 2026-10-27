import urllib.request
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

test_urls = [
    "https://www.oziva.in/products/clean-whey-concentrate-27g-protein-100-cold-processed.json",
    "https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate.json",
    "https://pintola.in/products/high-protein-peanut-butter-dark-chocolate.json",
    "https://myfitness.in/products/high-protein-peanut-butter-crispy.json",
    "https://ketofy.in/products/ketofy-keto-flour.json",
    "https://eatbetterco.com/products/high-protein-spicy-seed-mix.json",
]

for url in test_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.load(resp)
            prod = data.get("product", {})
            title = prod.get("title")
            img = prod.get("image", {}).get("src") if prod.get("image") else (prod.get("images", [{}])[0].get("src") if prod.get("images") else None)
            variants = prod.get("variants", [])
            v_info = [(v.get("title"), v.get("price"), v.get("compare_at_price")) for v in variants[:2]]
            print(f"[SUCCESS] {url.split('/')[2]}: '{title}'")
            print(f"   Image: {img}")
            print(f"   Variants: {v_info}")
    except Exception as e:
        print(f"[FAILED] {url}: {e}")
