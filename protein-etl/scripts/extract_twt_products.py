import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

twt_handles = [
    "unflavoured-30-g-pure-whey-protein-isolate",
    "unflavored-26g-whey-protein-isolate-concentrate",
    "light-cocoa-24g-whey-protein-isolate-concentrate",
    "cold-coffee-24g-whey-protein-isolate-concentrate",
    "double-cocoa-25g-plant-protein",
    "pista-badaam-24g-plant-protein"
]

twt_extracted = {}

for handle in twt_handles:
    url = f"https://thewholetruthfoods.com/products/{handle}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8")
        ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        prod_obj = None
        for item in ld:
            try:
                p = json.loads(item)
                if p.get("@type") == "Product":
                    prod_obj = p
                    break
            except:
                pass
        
        if prod_obj:
            title = prod_obj.get("name")
            img_data = prod_obj.get("image")
            img_url = ""
            if isinstance(img_data, dict):
                img_url = img_data.get("url") or img_data.get("image") or ""
            elif isinstance(img_data, list) and img_data:
                img_url = img_data[0].get("url") if isinstance(img_data[0], dict) else str(img_data[0])
            elif isinstance(img_data, str):
                img_url = img_data

            # Look for all image URLs in the page that match media.thewholetruthfoods.com
            all_media_imgs = re.findall(r'(https://media\.thewholetruthfoods\.com/public/backend-assets/[^"\'\s>]+)', html)
            unique_imgs = []
            seen = set()
            if img_url:
                unique_imgs.append({"src": img_url})
                seen.add(img_url.split("?")[0])
            for m in all_media_imgs:
                clean_m = m.split("?")[0]
                if clean_m not in seen and not any(k in clean_m.lower() for k in ["logo", "icon", "banner", "review"]):
                    unique_imgs.append({"src": m})
                    seen.add(clean_m)

            variants = []
            offers = prod_obj.get("offers", [])
            for off in offers:
                var_name = off.get("name", "Default")
                var_price = str(off.get("price"))
                variants.append({
                    "title": var_name,
                    "price": var_price,
                    "compare_at_price": var_price,
                    "sku": off.get("sku"),
                    "available": "InStock" in off.get("availability", "")
                })

            twt_extracted[handle] = {
                "handle": handle,
                "title": title,
                "variants": variants,
                "images": unique_imgs
            }
            print(f"[OK] TWT {handle}: {title} | {len(variants)} vars | {len(unique_imgs)} imgs")
    except Exception as e:
        print(f"[ERR] TWT {handle}: {e}")

with open("protein-etl/data/demo_catalog/twt_extracted.json", "w", encoding="utf-8") as f:
    json.dump(twt_extracted, f, indent=2, ensure_ascii=False)
