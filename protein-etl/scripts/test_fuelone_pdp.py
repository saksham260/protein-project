"""Extract product data from Fuel One product pages."""
import httpx
from bs4 import BeautifulSoup
import json
import re

url = "https://www.fuelone.in/sv/fuel-one-whey-max-powder/SP-141763"
r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}, timeout=12)
print("Status:", r.status_code, "Length:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")
print("Title:", soup.title.string if soup.title else "No Title")

# Search for JSON blobs in script tags
for idx, s in enumerate(soup.find_all("script")):
    text = s.string or ""
    if any(k in text for k in ["SP-141763", "variants", "nutritionalInfo", "mrp", "finalPrice", "discountedPrice"]):
        print(f"Script {idx} has product keywords (len={len(text)}):")
        # try to extract json or key lines
        for line in text.splitlines():
            if any(k in line for k in ["title", "finalPrice", "mrp", "variant", "protein"]):
                print("  ", line.strip()[:120])
