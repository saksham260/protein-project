"""Read-only: list products that now have no image, and check whether any of them had a WORKING image before Entry 34."""
import json
from collections import defaultdict

cur = json.load(open("protein-etl/scratch/browser_image_status.json", encoding="utf-8"))["broken"]  # latest run (all MISSING)
first = json.load(open("protein-etl/scratch/http_check_results.json", encoding="utf-8"))           # first urllib run (pre-change)
ok_before = {r["product"]["slug"]: r["url"] for r in first["ok_http"]}

null_slugs = {b["slug"] for b in cur}
regressed = [(s, ok_before[s]) for s in null_slugs if s in ok_before]
print(f"Products with no image now: {len(null_slugs)}")
print(f"Of these, had a 200-OK image BEFORE Entry 34 (possible regressions): {len(regressed)}")
for s, u in sorted(regressed):
    print(f"  REGRESSED {s} -> {u}")

by_brand = defaultdict(list)
for b in cur:
    by_brand[b["brand"]].append(f"{b['name']} [{b['category']}]")
print("\nBy brand:")
for br in sorted(by_brand, key=lambda k: -len(by_brand[k])):
    print(f"{br} ({len(by_brand[br])}): " + " | ".join(by_brand[br]))
