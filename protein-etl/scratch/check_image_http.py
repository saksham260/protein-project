import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

with open("protein-etl/scratch/image_audit_summary.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Combine unallowed and valid to check their actual HTTP reachable status
all_to_check = []
for p in data["unallowed_hostname"]:
    all_to_check.append((p, "unallowed_hostname"))
for p in data["valid_images"]:
    all_to_check.append((p, "allowed_hostname"))

print(f"Checking HTTP reachability for {len(all_to_check)} product image URLs...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_url(item):
    p, status_group = item
    img_url = p["image_url"]
    
    if img_url.startswith("/"):
        # Local relative image
        local_path = "protein-web/public" + img_url
        import os
        exists = os.path.exists(local_path)
        return {
            "product": p,
            "status_group": status_group,
            "url": img_url,
            "http_status": 200 if exists else 404,
            "error": None if exists else "Local file missing"
        }
        
    req = urllib.request.Request(img_url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            return {
                "product": p,
                "status_group": status_group,
                "url": img_url,
                "http_status": response.status,
                "error": None
            }
    except urllib.error.HTTPError as e:
        # Some servers disallow HEAD, try GET with Range or small stream
        if e.code in (403, 405):
            req_get = urllib.request.Request(img_url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(req_get, timeout=6) as response_get:
                    return {
                        "product": p,
                        "status_group": status_group,
                        "url": img_url,
                        "http_status": response_get.status,
                        "error": None
                    }
            except Exception as e_get:
                return {
                    "product": p,
                    "status_group": status_group,
                    "url": img_url,
                    "http_status": getattr(e_get, 'code', None),
                    "error": str(e_get)
                }
        return {
            "product": p,
            "status_group": status_group,
            "url": img_url,
            "http_status": e.code,
            "error": str(e)
        }
    except Exception as e:
        return {
            "product": p,
            "status_group": status_group,
            "url": img_url,
            "http_status": None,
            "error": str(e)
        }

results_by_url = []
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(check_url, item) for item in all_to_check]
    for future in as_completed(futures):
        results_by_url.append(future.result())

broken_http = [r for r in results_by_url if r["http_status"] != 200]
ok_http = [r for r in results_by_url if r["http_status"] == 200]

print(f"\n--- HTTP Check Results ---")
print(f"Total checked: {len(results_by_url)}")
print(f"200 OK: {len(ok_http)}")
print(f"HTTP Errors / Broken: {len(broken_http)}")

broken_in_allowed = [r for r in broken_http if r["status_group"] == "allowed_hostname"]
broken_in_unallowed = [r for r in broken_http if r["status_group"] == "unallowed_hostname"]

print(f"Broken among ALLOWED hostnames: {len(broken_in_allowed)}")
print(f"Broken among UNALLOWED hostnames: {len(broken_in_unallowed)}")

with open("protein-etl/scratch/http_check_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "broken_in_allowed": broken_in_allowed,
        "broken_in_unallowed": broken_in_unallowed,
        "ok_http": ok_http
    }, f, indent=2)

print("\nSample broken among allowed:")
for r in broken_in_allowed[:10]:
    print(f"  [{r['product']['brand']}] {r['product']['name']} ({r['http_status']}): {r['url']}")

print("\nSample broken among unallowed:")
for r in broken_in_unallowed[:10]:
    print(f"  [{r['product']['brand']}] {r['product']['name']} ({r['http_status']}): {r['url']}")
