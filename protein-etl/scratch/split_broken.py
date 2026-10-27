import json

with open("protein-etl/scratch/browser_image_status.json", "r", encoding="utf-8") as f:
    data = json.load(f)

broken = data["broken"]
print(f"Total broken: {len(broken)}")

with open("protein-etl/data/demo_catalog/manual_entries.jsonl", "r", encoding="utf-8") as f:
    manual_handles = set(json.loads(line)["handle"] for line in f if line.strip())

in_manual = [b for b in broken if b["slug"] in manual_handles]
in_older = [b for b in broken if b["slug"] not in manual_handles]

print(f"Broken in manual_entries (Batches 5A-5G): {len(in_manual)}")
print(f"Broken in older catalog: {len(in_older)}")

print("\nOlder catalog broken products:")
for b in in_older:
    print(f"  [{b['brand']}] {b['name']} ({b['slug']}): {b['status']} -> {b['url']}")

