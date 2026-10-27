import json

with open("protein-etl/scratch/http_check_results.json", "r", encoding="utf-8") as f:
    http_data = json.load(f)

with open("protein-etl/scratch/image_audit_summary.json", "r", encoding="utf-8") as f:
    summary_data = json.load(f)

broken_in_allowed = http_data["broken_in_allowed"]
broken_in_unallowed = http_data["broken_in_unallowed"]
ok_http = http_data["ok_http"]

# Products that fail to display image on website:
# Group A: Hostname is not permitted in next.config.ts (Next.js automatically blocks them, onError fires -> emoji)
# Group B: Hostname is allowed in next.config.ts, but image returns 404/403/broken (browser fetch fails, onError fires -> emoji)

failed_products = {}

# Group A: unallowed hostname
for item in summary_data["unallowed_hostname"]:
    pid = item["id"]
    failed_products[pid] = {
        "id": pid,
        "name": item["name"],
        "slug": item["slug"],
        "brand": item["brand"],
        "category": item["category"],
        "image_url": item["image_url"],
        "reason_code": "UNALLOWED_HOSTNAME",
        "detail": f"Domain '{item.get('hostname')}' is not in next.config.ts remotePatterns"
    }

# Group B: allowed hostname but broken HTTP
for item in broken_in_allowed:
    p = item["product"]
    pid = p["id"]
    if pid not in failed_products:
        failed_products[pid] = {
            "id": pid,
            "name": p["name"],
            "slug": p["slug"],
            "brand": p["brand"],
            "category": p["category"],
            "image_url": p["image_url"],
            "reason_code": "BROKEN_HTTP",
            "detail": f"HTTP {item['http_status']} ({item.get('error')})"
        }

print(f"Total products failing to display image: {len(failed_products)}")

# Also let's see how many of Group A are ALSO broken URLs
unallowed_and_broken = 0
for item in broken_in_unallowed:
    pid = item["product"]["id"]
    if pid in failed_products:
        unallowed_and_broken += 1
        failed_products[pid]["http_status"] = item["http_status"]

# Categorize and sort by brand and name
failed_list = list(failed_products.values())
failed_list.sort(key=lambda x: (x["brand"], x["name"]))

with open("protein-etl/scratch/products_displaying_emoji.json", "w", encoding="utf-8") as f:
    json.dump(failed_list, f, indent=2)

print("\nBreakdown by Reason:")
print(f"- Domain not in next.config.ts: {len(summary_data['unallowed_hostname'])} (of which {unallowed_and_broken} are also 404/broken)")
print(f"- Allowed domain but HTTP 403/404/error: {len(broken_in_allowed)}")
print(f"- Total unique products displaying emoji: {len(failed_list)}")

print("\nBreakdown by Category:")
from collections import Counter
cat_counts = Counter(p["category"] for p in failed_list)
for cat, cnt in cat_counts.most_common():
    print(f"  {cat}: {cnt}")

print("\nBreakdown by Brand:")
brand_counts = Counter(p["brand"] for p in failed_list)
for br, cnt in brand_counts.most_common():
    print(f"  {br}: {cnt}")

