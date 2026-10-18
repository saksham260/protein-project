import json, urllib.request, time
from pathlib import Path

SNAPSHOT_PATH = Path("protein-etl/data/demo_catalog/store_snapshot.json")
snapshot = json.load(open(SNAPSHOT_PATH, encoding="utf-8"))

PICKS_PATH = Path("protein-etl/data/demo_catalog/picks.txt")
picks = [l.split("|") for l in PICKS_PATH.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]

# Items 189 to 218 (index 188 to 217)
batch2_picks = picks[188:]
print(f"Updating snapshot for {len(batch2_picks)} Batch 2 products...")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Track existing handles per store in snapshot
for i, (store, handle, cat, brand) in enumerate(batch2_picks, 189):
    if store not in snapshot:
        snapshot[store] = []
    
    # Check if already present
    existing_handles = {p["handle"] for p in snapshot[store]}
    if handle in existing_handles:
        print(f"[{i}] {store} | {handle} already in snapshot")
        continue

    url = f"https://{store}/products/{handle}.json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            p = data.get("product")
            if p:
                snapshot[store].append(p)
                print(f"[{i}] Added {store} | {handle} ({p.get('title')[:35]})")
            else:
                print(f"[{i}] No product found in response for {handle}")
    except Exception as e:
        print(f"[{i}] Error fetching {store}/{handle}: {e}")
    time.sleep(0.3)

SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Snapshot updated successfully! Total stores: {len(snapshot)}")
