"""Inspect architecture of fuelone.in, kapiva.in, and xlr8sport.com."""
import httpx
from bs4 import BeautifulSoup
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"

# 1. Save Bolt Nutrition feed
print("Saving Bolt Nutrition products...")
r = httpx.get("https://boltnutritions.com/products.json?limit=250", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
if r.status_code == 200:
    data = r.json().get("products", [])
    print(f"Bolt Nutrition: {len(data)} products saved.")
    with open(ROOT / "bolt_products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

client = httpx.Client(follow_redirects=True, timeout=12, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})

for domain, name in [("www.fuelone.in", "fuelone"), ("kapiva.in", "kapiva"), ("xlr8sport.com", "xlr8")]:
    print(f"\nAnalyzing {domain} ({name})...")
    resp = client.get(f"https://{domain}")
    print(f"Status: {resp.status_code}")
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Check Next.js __NEXT_DATA__
    next_data = soup.find("script", id="__NEXT_DATA__")
    if next_data:
        print(f"  -> Found __NEXT_DATA__ (Next.js application!)")
        with open(ROOT / f"{name}_next_data.json", "w", encoding="utf-8") as f:
            f.write(next_data.string)
    
    # Check Shopify hints
    if "cdn.shopify.com" in resp.text:
        print("  -> Contains Shopify CDN assets")
    
    # Check WooCommerce / WordPress
    if "wp-content" in resp.text:
        print("  -> Contains WordPress / WooCommerce assets")

    # Find sample product links
    product_links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if any(k in href for k in ["/product", "/products/", "/item/"]):
            product_links.add(href)
    print(f"  -> Sample product links ({len(product_links)}): {list(product_links)[:5]}")

    with open(ROOT / f"{name}_home.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
