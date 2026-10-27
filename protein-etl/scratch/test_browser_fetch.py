import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

browser_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "http://localhost:3000/",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}

with open("protein-etl/scratch/image_audit_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

# Load all products from Supabase
from dotenv import dotenv_values
from supabase import create_client
cfg = dotenv_values("protein-etl/.env")
client = create_client(cfg.get("SUPABASE_URL"), cfg.get("SUPABASE_SERVICE_KEY"))

cats = {c["id"]: c["name"] for c in client.table("categories").select("id, name").execute().data}
res = client.table("products").select("id, name, slug, image_url, category_id, brands(name), product_variants(id, variant_name, slug, image_url)").execute()

products = res.data
print(f"Total products in Supabase: {len(products)}")

def test_product_image(p):
    brand = p.get("brands", {}).get("name") if p.get("brands") else "Unknown"
    category = cats.get(p.get("category_id"), p.get("category_id"))
    variants = p.get("product_variants") or []
    var_imgs = [v.get("image_url") for v in variants if v.get("image_url")]
    img_url = var_imgs[0] if var_imgs else p.get("image_url")
    
    if not img_url or not img_url.strip():
        return {
            "id": p["id"],
            "slug": p["slug"],
            "name": p["name"],
            "brand": brand,
            "category": category,
            "url": None,
            "status": "MISSING",
            "http_code": None,
            "error": "No image URL"
        }
        
    if img_url.startswith("/"):
        # Local public image
        import os
        exists = os.path.exists("protein-web/public" + img_url)
        return {
            "id": p["id"],
            "slug": p["slug"],
            "name": p["name"],
            "brand": brand,
            "category": category,
            "url": img_url,
            "status": "OK" if exists else "BROKEN_LOCAL",
            "http_code": 200 if exists else 404,
            "error": None if exists else "Local file missing"
        }
        
    try:
        req = urllib.request.Request(img_url, headers=browser_headers, method="GET")
        with urllib.request.urlopen(req, timeout=8) as resp:
            content_type = resp.headers.get("Content-Type", "")
            return {
                "id": p["id"],
                "slug": p["slug"],
                "name": p["name"],
                "brand": brand,
                "category": category,
                "url": img_url,
                "status": "OK" if ("image" in content_type or resp.status == 200) else "NOT_IMAGE",
                "http_code": resp.status,
                "error": None
            }
    except urllib.error.HTTPError as e:
        return {
            "id": p["id"],
            "slug": p["slug"],
            "name": p["name"],
            "brand": brand,
            "category": category,
            "url": img_url,
            "status": f"HTTP_{e.code}",
            "http_code": e.code,
            "error": str(e)
        }
    except Exception as e:
        return {
            "id": p["id"],
            "slug": p["slug"],
            "name": p["name"],
            "brand": brand,
            "category": category,
            "url": img_url,
            "status": "NETWORK_ERROR",
            "http_code": None,
            "error": str(e)
        }

results = []
with ThreadPoolExecutor(max_workers=25) as executor:
    futures = [executor.submit(test_product_image, p) for p in products]
    for future in as_completed(futures):
        results.append(future.result())

broken = [r for r in results if r["status"] != "OK"]
working = [r for r in results if r["status"] == "OK"]

print(f"\n--- Browser-Simulation Results ---")
print(f"Total checked: {len(results)}")
print(f"Working Images (200 OK): {len(working)}")
print(f"Broken Images (Displaying Emoji): {len(broken)}")

with open("protein-etl/scratch/browser_image_status.json", "w", encoding="utf-8") as f:
    json.dump({
        "broken_count": len(broken),
        "working_count": len(working),
        "broken": broken
    }, f, indent=2)

from collections import Counter
status_counts = Counter(r["status"] for r in broken)
print("\nBroken Image Breakdown by Status:")
for st, cnt in status_counts.most_common():
    print(f"  {st}: {cnt}")

