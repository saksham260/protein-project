import os
import json
from pathlib import Path
from dotenv import dotenv_values
from urllib.parse import urlparse
import fnmatch

# Allowed remote patterns from next.config.ts
ALLOWED_PATTERNS = [
    "*.supabase.co",
    "*.amazon.com",
    "*.amazon.in",
    "images.unsplash.com",
    "cdn.shopify.com",
    "shop.amul.com",
    "epigamiastore.com",
    "media.thewholetruthfoods.com",
    "cdn.grofers.com",
    "*.flixcart.com",
    "*.bbassets.com",
    "*.bigcommerce.com",
    "*.nutrabay.com",
    "*.b-cdn.net",
    "*.hkrtcdn.com",
    "*.farziengineer.co",
    "*.avvatarindia.com",
]

def is_domain_allowed(hostname):
    if not hostname:
        return False
    for pat in ALLOWED_PATTERNS:
        if pat.startswith("*."):
            # Matches subdomains and root
            domain_part = pat[2:]
            if hostname == domain_part or hostname.endswith("." + domain_part):
                return True
        elif hostname == pat:
            return True
    return False

# 1. Check live Supabase
cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")

from supabase import create_client
client = create_client(url, key)

# Get all products with variants
print("Fetching products from Supabase...")
all_products = []
offset = 0
limit = 500
res = client.table("products").select("id, name, slug, image_url, category_id, brands(name), product_variants(id, variant_name, slug, image_url)").execute()
products = res.data

print(f"Total products in Supabase: {len(products)}")

missing_or_null_image = []
unallowed_domain = []
all_image_urls = set()

for p in products:
    brand_name = p.get("brands", {}).get("name") if p.get("brands") else "Unknown"
    p_img = p.get("image_url")
    variants = p.get("product_variants") or []
    
    # In ProductCard: variant?.image_url || product.image_url
    # Let's check default variant and variant image_urls
    var_imgs = [v.get("image_url") for v in variants if v.get("image_url")]
    
    # Effective primary image
    effective_img = var_imgs[0] if var_imgs else p_img
    
    if not effective_img or effective_img.strip() == "":
        missing_or_null_image.append({
            "name": p["name"],
            "slug": p["slug"],
            "brand": brand_name,
            "category": p.get("category_id"),
            "reason": "image_url is null or empty in Supabase"
        })
    else:
        all_image_urls.add((p["slug"], p["name"], brand_name, p.get("category_id"), effective_img))
        if effective_img.startswith("http"):
            parsed = urlparse(effective_img)
            if not is_domain_allowed(parsed.hostname):
                unallowed_domain.append({
                    "name": p["name"],
                    "slug": p["slug"],
                    "brand": brand_name,
                    "category": p.get("category_id"),
                    "image_url": effective_img,
                    "hostname": parsed.hostname
                })

print(f"\n--- Products with NULL / Empty Image in Supabase ({len(missing_or_null_image)}) ---")
for item in missing_or_null_image:
    print(f"- [{item['brand']}] {item['name']} ({item['slug']}) - Category: {item['category']}")

print(f"\n--- Products with Unallowed Hostname in next.config.ts ({len(unallowed_domain)}) ---")
for item in unallowed_domain:
    print(f"- [{item['brand']}] {item['name']} ({item['slug']}) -> {item['hostname']} ({item['image_url']})")

# Also check seedCatalog.json
print("\nChecking seedCatalog.json...")
seed_path = Path("protein-web/src/data/seedCatalog.json")
if seed_path.exists():
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_data = json.load(f)
    print(f"Total products in seedCatalog.json: {len(seed_data)}")
    seed_missing = []
    seed_unallowed = []
    for sp in seed_data:
        p_img = sp.get("image_url")
        vars = sp.get("variants") or []
        v_imgs = [v.get("image_url") for v in vars if v.get("image_url")]
        eff_img = v_imgs[0] if v_imgs else p_img
        if not eff_img or eff_img.strip() == "":
            seed_missing.append(sp["name"])
        elif eff_img.startswith("http"):
            parsed = urlparse(eff_img)
            if not is_domain_allowed(parsed.hostname):
                seed_unallowed.append((sp["name"], parsed.hostname, eff_img))
    print(f"seedCatalog null images: {len(seed_missing)}")
    print(f"seedCatalog unallowed domains: {len(seed_unallowed)}")
    for name, host, img in seed_unallowed[:10]:
        print(f"  - {name} -> {host}")

