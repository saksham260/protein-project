"""Audit candidate products across candidate stores for Batch 3 & 4."""
import json
import httpx
from pathlib import Path

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def audit_shopify_store(store_domain, keywords):
    url = f"https://{store_domain}/products.json?limit=250"
    try:
        r = httpx.get(url, headers=headers, timeout=12.0, follow_redirects=True)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}
        data = r.json()
        products = data.get("products", [])
        matched = []
        for p in products:
            title = p.get("title", "")
            handle = p.get("handle", "")
            desc = p.get("body_html", "")
            text = (title + " " + handle + " " + desc).lower()
            if any(k.lower() in text for k in keywords):
                matched.append({
                    "title": title,
                    "handle": handle,
                    "variants_count": len(p.get("variants", [])),
                    "variants": [
                        {
                            "title": v.get("title"),
                            "price": v.get("price"),
                            "compare_at_price": v.get("compare_at_price"),
                            "available": v.get("available"),
                            "grams": v.get("grams")
                        } for v in p.get("variants", [])[:5]
                    ],
                    "images_count": len(p.get("images", [])),
                    "sample_image": p.get("images", [{}])[0].get("src") if p.get("images") else None
                })
        return {"total": len(products), "matched": matched}
    except Exception as e:
        return {"error": str(e)}

results = {}

print("Auditing Pintola...")
results["pintola.in"] = audit_shopify_store("pintola.in", ["protein", "muesli", "peanut butter", "cake"])

print("Auditing Bagrry's...")
results["bagrrys.com"] = audit_shopify_store("bagrrys.com", ["protein", "muesli", "oats", "peanut butter"])

print("Auditing True Elements...")
results["true-elements.com"] = audit_shopify_store("true-elements.com", ["protein", "muesli", "oatmeal", "seed"])

print("Auditing Bigmuscles Nutrition...")
results["bigmusclesnutrition.com"] = audit_shopify_store("bigmusclesnutrition.com", ["gold whey", "real whey", "nitra whey", "isolate", "plant"])

Path("protein-etl/data/demo_catalog/audit_batch3_stores.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print("Finished store audits!\n")
for s, r in results.items():
    print(f"=== {s} (Total: {r.get('total')}, Matched: {len(r.get('matched', []))}) ===")
    for p in r.get('matched', [])[:10]:
        print(f"  - {p['title']} | handle: {p['handle']} | {p['variants_count']} variants")
