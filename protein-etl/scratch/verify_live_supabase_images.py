import urllib.request
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
null_imgs = []
valid_imgs = []
broken_imgs = []

headers = {"User-Agent": "Mozilla/5.0"}

print(f"Auditing {total} live products...")

for p in products:
    img = p.get("image_url")
    if not img:
        null_imgs.append(p)
        continue
    
    try:
        req = urllib.request.Request(img, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            if r.status == 200:
                valid_imgs.append(p)
            else:
                broken_imgs.append((p, f"HTTP {r.status}"))
    except Exception as e:
        broken_imgs.append((p, str(e)))

print("\n=== Live Supabase Image Audit Summary ===")
print(f"Total Products:         {total}")
print(f"Verified Working (200): {len(valid_imgs)}")
print(f"Clean Emoji Fallbacks:  {len(null_imgs)}")
print(f"Broken HTTP Assets:     {len(broken_imgs)}")

if broken_imgs:
    print("\nBroken items:")
    for p, err in broken_imgs:
        print(f"  {p['slug']}: {err} | {p['image_url']}")
