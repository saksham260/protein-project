import os
from pathlib import Path
from dotenv import dotenv_values

cfg = dotenv_values("protein-etl/.env")
url = cfg.get("SUPABASE_URL")
key = cfg.get("SUPABASE_SERVICE_KEY")

from supabase import create_client
client = create_client(url, key)
res_p = client.table("products").select("id", count="exact").execute()
res_b = client.table("brands").select("id", count="exact").execute()
res_v = client.table("product_variants").select("id", count="exact").execute()
res_c = client.table("categories").select("slug, name").execute()
print(f"Supabase Products Count: {res_p.count}")
print(f"Supabase Brands Count: {res_b.count}")
print(f"Supabase Variants Count: {res_v.count}")
print(f"Categories in Supabase: {[c['slug'] for c in res_c.data]}")
