import os
import urllib.request
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('protein-etl/.env')
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_KEY')
supabase = create_client(url, key)

img_url = "https://img4.hkrtcdn.com/37800/prd_3779993-MuscleBlaze-Super-Gainer-XXL-Weight-Gainer-6.6-lb-Chocolate_o.jpg"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(img_url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as r:
    data = r.read()

filename = "test-mb-super-gainer-xxl.jpg"
print(f"Downloaded {len(data)} bytes from HK CDN. Uploading to Supabase Storage...")

# Upload to Supabase Storage bucket 'product-images'
res = supabase.storage.from_("product-images").upload(
    path=filename,
    file=data,
    file_options={"content-type": "image/jpeg", "upsert": "true"}
)
print("Upload result:", res)

# Check public URL
public_url = f"{url}/storage/v1/object/public/product-images/{filename}"
print("Public URL:", public_url)

# Test downloading public URL
req_pub = urllib.request.Request(public_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_pub, timeout=10) as r_pub:
    print(f"Public URL verified! Status: {r_pub.status}, Content-Type: {r_pub.headers.get('content-type')}, Size: {len(r_pub.read())} bytes")
