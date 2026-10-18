import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

mb_items = [
    ("muscleblaze-biozyme-performance-whey", "https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093"),
    ("mb-fuel-one-whey-protein-powder", "https://www.muscleblaze.com/sv/mb-fuel-one-whey-protein-powder/SP-130407"),
    ("muscleblaze-100-clean-raw-whey-protein-concentrate", "https://www.muscleblaze.com/sv/muscleblaze-100-clean-raw-whey-protein-concentrate/SP-40454"),
    ("muscleblaze-hi-protein-bar-30g-protein", "https://www.muscleblaze.com/sv/muscleblaze-hi-protein-bar-30g-protein/SP-44769"),
]

mb_extracted = {}

for handle, url in mb_items:
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        prod = None
        for item in ld:
            try:
                p = json.loads(item)
                t = p.get("@type")
                if t == "Product" or (isinstance(t, list) and "Product" in t):
                    prod = p
                    break
            except:
                pass
        
        name = prod.get("name") if prod else handle
        img = prod.get("image") if prod else None
        offer = prod.get("offers", {}) if prod else {}
        price = str(offer.get("price", "0"))
        
        # Check for multiple variant options in the HTML or script
        # Check if there is variant data in HTML
        # Look for images on hkrtcdn.com
        hk_imgs = list(dict.fromkeys(re.findall(r'(https://img\d*\.hkrtcdn\.com/[^"\'\s>]+)', html)))
        filtered_imgs = [i for i in hk_imgs if any(k in i.lower() for k in ["prd_", "product", "secprd"]) and not any(k in i.lower() for k in ["banner", "icon", "logo", "review", "sprite"])]
        
        imgs_list = [{"src": img}] if img else []
        for i in filtered_imgs:
            if not any(x["src"] == i for x in imgs_list):
                imgs_list.append({"src": i})

        mb_extracted[handle] = {
            "handle": handle,
            "title": name,
            "url": url,
            "variants": [
                {
                    "title": name,
                    "price": price,
                    "compare_at_price": price,
                    "sku": handle,
                    "available": "InStock" in offer.get("availability", "")
                }
            ],
            "images": imgs_list
        }
        print(f"[OK] MB {handle}: {name[:40]} | Rs {price} | {len(imgs_list)} imgs")
    except Exception as e:
        print(f"[ERR] MB {handle}: {e}")

with open("protein-etl/data/demo_catalog/mb_extracted.json", "w", encoding="utf-8") as f:
    json.dump(mb_extracted, f, indent=2, ensure_ascii=False)
