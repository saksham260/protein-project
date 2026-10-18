"""Extract full product data from Fuel One flight payloads."""
import httpx
from bs4 import BeautifulSoup
import json
import re

url = "https://www.fuelone.in/sv/fuel-one-whey-max-powder/SP-141763"
r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}, timeout=12)

soup = BeautifulSoup(r.text, "html.parser")
found_data = None

for s in soup.find_all("script"):
    text = s.string or ""
    if '"spName":' in text and '"results":' in text:
        # Extract the JSON payload inside self.__next_f.push
        m = re.search(r'\{"data":\{"results":\{.*?\}\}\}', text)
        if not m:
            # Match larger block
            idx = text.find('{"data":{"results":')
            if idx != -1:
                # Find matching closing brace
                brace_count = 0
                end_idx = idx
                for i in range(idx, len(text)):
                    if text[i] == '{':
                        brace_count += 1
                    elif text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                blob = text[idx:end_idx].replace('\\"', '"').replace('\\\\', '\\')
                try:
                    found_data = json.loads(blob)
                except Exception as e:
                    # try without replace
                    try:
                        found_data = json.loads(text[idx:end_idx])
                    except Exception:
                        pass
        else:
            try:
                found_data = json.loads(m.group(0))
            except Exception:
                pass

if found_data:
    res = found_data.get("data", {}).get("results", {})
    print("SUCCESS extracting Fuel One data!")
    print("spName:", res.get("spName"))
    print("brandName:", res.get("brandName"))
    print("Keys in results:", list(res.keys()))
    variants = res.get("variants", [])
    print("Variants count:", len(variants))
    for v in variants[:5]:
        print("  Variant:", v.get("variantName") or v.get("name"), "| Price:", v.get("finalPrice") or v.get("offerPrice"), "| MRP:", v.get("mrp"))
    images = res.get("media", []) or res.get("galleryImages", []) or res.get("images", [])
    print("Images count:", len(images))
else:
    print("Could not parse JSON cleanly, searching directly...")
    # Find image URLs and variant names directly
    imgs = re.findall(r'https://[^\s"]+?\.jpg|https://[^\s"]+?\.png', r.text)
    hk_imgs = [i for i in imgs if "hkrtcdn" in i]
    print(f"Found {len(hk_imgs)} HealthKart CDN images: {hk_imgs[:3]}")
