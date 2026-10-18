from src.db.supabase_client import SupabaseUploader

uploader = SupabaseUploader()
if uploader.client:
    res = uploader.client.table("categories").upsert({
        "name": "Dairy",
        "slug": "dairy",
        "description": "High-protein paneer, fresh curd, and everyday dairy staples.",
        "icon": "🧀",
        "display_order": 7
    }, on_conflict="slug").execute()
    print("Dairy category upserted:", res.data)

    # Re-check categories
    cats = uploader.client.table("categories").select("slug, name, display_order").execute().data
    print("\nUpdated categories in Supabase:")
    for c in cats:
        print(f"  slug={c['slug']}, name={c['name']}, order={c['display_order']}")
