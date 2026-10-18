from src.db.supabase_client import SupabaseUploader

uploader = SupabaseUploader()
if uploader.client:
    cats = uploader.client.table("categories").select("slug, name, display_order").execute().data
    print("Categories in Supabase:")
    for c in cats:
        print(f"  slug={c['slug']}, name={c['name']}, order={c['display_order']}")
