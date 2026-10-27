import os
import json
import urllib.request
from pathlib import Path
from dotenv import dotenv_values
from urllib.parse import urlparse

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
            domain_part = pat[2:]
            if hostname == domain_part or hostname.endswith("." + domain_part):
                return True
        elif hostname == pat:
            return True
    return False

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")

from supabase import create_client
client = create_client(url, key)

res = client.table("products").select("id, name, slug, image_url, category_id, brands(name), product_variants(id, variant_name, slug, image_url)").execute()
products = res.data

results = {
    "null_or_empty": [],
    "unallowed_hostname": [],
    "http_error": [],
    "valid_images": []
}

for p in products:
    brand_name = p.get("brands", {}).get("name") if p.get("brands") else "Unknown"
    p_img = p.get("image_url")
    variants = p.get("product_variants") or []
    var_imgs = [v.get("image_url") for v in variants if v.get("image_url")]
    effective_img = var_imgs[0] if var_imgs else p_img
    
    prod_info = {
        "id": p["id"],
        "name": p["name"],
        "slug": p["slug"],
        "brand": brand_name,
        "category": p.get("category_id"),
        "image_url": effective_img
    }
    
    if not effective_img or not effective_img.strip():
        results["null_or_empty"].append(prod_info)
    elif not is_domain_allowed(urlparse(effective_img).hostname):
        prod_info["hostname"] = urlparse(effective_img).hostname
        results["unallowed_hostname"].append(prod_info)
    else:
        results["valid_images"].append(prod_info)

with open("protein-etl/scratch/image_audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Total Products in Supabase: {len(products)}")
print(f"1. NULL or Empty image_url: {len(results['null_or_empty'])}")
print(f"2. Unallowed Hostname in next.config.ts: {len(results['unallowed_hostname'])}")
print(f"3. Initially Valid Image Configuration: {len(results['valid_images'])}")

# Check distinct unallowed hostnames
unallowed_hosts = set(p["hostname"] for p in results["unallowed_hostname"])
print(f"\nUnique Unallowed Hostnames ({len(unallowed_hosts)}):")
for h in sorted(unallowed_hosts):
    count = sum(1 for p in results["unallowed_hostname"] if p["hostname"] == h)
    print(f"  - {h}: {count} products")

