"""Fetch and parse XLR8 products from Dukaan JSON-LD and HTML."""
import httpx
from bs4 import BeautifulSoup
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"

xlr8_urls = [
    ("xlr8-whey-protein-chocolate", "https://xlr8sport.com/products/whey-protein-with-24-g-protein-5-4-g-bcaa"),
    ("xlr8-whey-protein-cookies-cream", "https://xlr8sport.com/products/xlr8-whey-protein-with-24-g-protein-5-4-g-bcaa-cookies-and-cream"),
    ("xlr8-classic-whey-chocolate", "https://xlr8sport.com/products/xlr8-classic-whey-24-g-protein-5-5-bcaa-chocolate"),
    ("xlr8-whey-protein-sachets", "https://xlr8sport.com/products/xlr8-whey-protein-136gm-4-units-34gm-each")
]

client = httpx.Client(follow_redirects=True, timeout=15, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})

all_xlr8 = {}

for slug, url in xlr8_urls:
    print(f"Fetching {slug}...")
    try:
        r = client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        prod_schema = None
        for s in soup.find_all("script", type="application/ld+json"):
            if s.string:
                try:
                    data = json.loads(s.string, strict=False)
                    if data.get("@type") == "Product":
                        prod_schema = data
                        break
                except Exception:
                    pass
        
        # Also find images on the page
        imgs = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src and any(ext in src.lower() for ext in [".jpg", ".png", ".webp"]) and any(h in src.lower() for h in ["mydukaan", "xlr8", "cloudfront", "dukaan"]):
                imgs.append(src)

        if prod_schema:
            offers = prod_schema.get("offers", {})
            price = offers.get("price") if isinstance(offers, dict) else (offers[0].get("price") if isinstance(offers, list) else None)
            print(f"  OK: {prod_schema.get('name')[:40]} | Price: {price} | Images: {len(imgs)}")
            prod_schema["gallery_images"] = imgs
            all_xlr8[slug] = prod_schema
        else:
            print(f"  No schema found, found title: {soup.title.string if soup.title else ''}")
    except Exception as e:
        print(f"  Error {slug}: {e}")

with open(ROOT / "xlr8_products.json", "w", encoding="utf-8") as f:
    json.dump(all_xlr8, f, indent=2)

print(f"Saved {len(all_xlr8)} XLR8 products to xlr8_products.json")
