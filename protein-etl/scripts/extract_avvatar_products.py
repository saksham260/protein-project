import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

avvatar_handles = [
    # Performance Whey
    "100-performance-whey-belgain-chocolate-flavour-1-kg",
    "100-performance-whey-belgain-chocolate-flavour-2-kg",
    "100-performance-whey-malai-kulfi-flavour-1-kg",
    "100-performance-whey-malai-kulfi-flavour-2-kg",
    "100-performance-whey-cold-coffee-flavour-1-kg",
    "100-performance-whey-cold-coffee-flavour-2-kg",
    "100-performance-whey-caramel-creme-flavour-1-kg",
    "100-performance-whey-unflavored-1-kg",
    # ISORICH
    "isorich-protein-belgian-chocolate-flavour-1-kg",
    "isorich-protein-belgian-chocolate-flavour-2-kg",
    "isorich-protein-malai-kulfi-flavour-1-kg",
    "isorich-protein-malai-kulfi-flavour-2-kg",
    "isorich-protein-chocolate-hazelnut-flavour-1-kg",
    # Alpha Whey
    "alpha-whey-belgian-chocolate-flavour-1-kg-2509104129-263",
    "alpha-whey-belgian-chocolate-flavour-2-kg-2509104551-890",
    "alpha-whey-malai-kulfi-flavour-1-kg",
    "alpha-whey-malai-kulfi-flavour-2-kg",
    "alpha-whey-cold-coffee-flavour-1-kg",
    # Wafer Bar
    "protein-wafer-bar-coffee-flavour-320g",
    "protein-wafer-bar-tiramisu-flavour-320g"
]

avvatar_extracted = {}

for handle in avvatar_handles:
    url = f"https://www.avvatarindia.com/product/{handle}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
        
        # Title
        h1_matches = re.findall(r'<h1 class="product-title">(.*?)</h1>', html, re.S)
        title = h1_matches[-1].strip() if h1_matches else handle.replace("-", " ").title()
        
        # Prices
        mrp_m = re.search(r'MRP:\s*<span class="old-price">₹\s*([\d,]+)</span>', html)
        mrp = mrp_m.group(1).replace(",", "") if mrp_m else "0"
        
        offer_m = re.search(r'Offer Price:\s*<span class="new-price">₹\s*([\d,]+)</span>', html)
        offer_price = offer_m.group(1).replace(",", "") if offer_m else mrp
        
        # Images
        imgs = re.findall(r'<img\b[^>]*src="([^"]+)"[^>]*>', html)
        media_imgs = []
        seen = set()
        for img in imgs:
            full_url = img if img.startswith("http") else f"https://www.avvatarindia.com{img}"
            if any(k in full_url.lower() for k in ["product_images", "nutrition_images"]):
                if full_url not in seen:
                    media_imgs.append({"src": full_url})
                    seen.add(full_url)
        
        avvatar_extracted[handle] = {
            "handle": handle,
            "title": title,
            "url": url,
            "variants": [
                {
                    "title": title,
                    "price": offer_price,
                    "compare_at_price": mrp if float(mrp) > float(offer_price) else offer_price,
                    "sku": handle,
                    "available": True
                }
            ],
            "images": media_imgs
        }
        print(f"[OK] Avvatar {handle}: {title} | Rs {offer_price} (MRP {mrp}) | {len(media_imgs)} imgs")
    except Exception as e:
        print(f"[ERR] Avvatar {handle}: {e}")

with open("protein-etl/data/demo_catalog/avvatar_extracted.json", "w", encoding="utf-8") as f:
    json.dump(avvatar_extracted, f, indent=2, ensure_ascii=False)
