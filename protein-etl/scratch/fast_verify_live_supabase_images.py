import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")
client = create_client(url, key)

print("Fetching all live products from Supabase...")
res = client.table("products").select("id, slug, name, image_url").execute()
products = res.data
total = len(products)
print(f"Loaded {total} products from live Supabase.")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def check_prod(p):
    img = p.get("image_url")
    if not img:
        return ("null", p['slug'], None, None)
    try:
        req = urllib.request.Request(img, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as r:
            if r.status == 200:
                return ("ok", p['slug'], img, None)
            else:
                return ("broken", p['slug'], img, f"HTTP {r.status}")
    except Exception as e:
        return ("broken", p['slug'], img, str(e))

with ThreadPoolExecutor(max_workers=25) as executor:
    results = list(executor.map(check_prod, products))

ok_list = [r for r in results if r[0] == "ok"]
null_list = [r for r in results if r[0] == "null"]
broken_list = [r for r in results if r[0] == "broken"]

print("\n=== Live Supabase Image Audit Summary ===")
print(f"Total Products:         {total}")
print(f"Verified Working (200): {len(ok_list)}")
print(f"Clean Emoji Fallbacks:  {len(null_list)}")
print(f"Broken HTTP Assets:     {len(broken_list)}")

if broken_list:
    print("\nBroken items:")
    for _, slug, img, err in broken_list:
        print(f"  {slug}: {err} | {img}")
