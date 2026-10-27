from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")

client = create_client(url, key)

print("Checking Supabase Storage buckets...")
try:
    buckets = client.storage.list_buckets()
    print("Existing buckets:", [b.name for b in buckets])
    
    bucket_names = [b.name for b in buckets]
    if "product-images" not in bucket_names:
        print("Creating 'product-images' public bucket...")
        res = client.storage.create_bucket("product-images", options={"public": True})
        print("Bucket creation response:", res)
    else:
        print("'product-images' bucket already exists.")
except Exception as e:
    print("Storage check error:", e)
