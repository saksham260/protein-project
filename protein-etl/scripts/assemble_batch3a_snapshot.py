import json
from pathlib import Path

HERE = Path("protein-etl/data/demo_catalog")
SNAPSHOT_PATH = HERE / "store_snapshot.json"
PICKS_PATH = HERE / "picks.txt"
READINGS_PATH = HERE / "readings.jsonl"

snapshot = json.load(open(SNAPSHOT_PATH, encoding="utf-8"))

# Load extracted store snapshots
bm_extracted = json.load(open(HERE / "bm_extracted.json", encoding="utf-8"))
twt_extracted = json.load(open(HERE / "twt_extracted.json", encoding="utf-8"))
av_extracted = json.load(open(HERE / "avvatar_extracted.json", encoding="utf-8"))
mb_extracted = json.load(open(HERE / "mb_extracted.json", encoding="utf-8"))

# Fix MB Fuel one URL in mb_extracted
mb_extracted["fuel-one-whey-protein"] = {
    "handle": "fuel-one-whey-protein",
    "title": "MuscleBlaze Fuel One Whey Protein (Chocolate)",
    "url": "https://www.muscleblaze.com/sv/fuel-one-whey-protein/SP-72739",
    "variants": [{"title": "Chocolate 1kg", "price": "1899", "compare_at_price": "2199", "sku": "fuel-one-1kg", "available": True}],
    "images": [{"src": "https://img8.hkrtcdn.com/28330/prd_2832957-MB-Fuel-One-Whey-Protein-2.2-lb-Chocolate_o.jpg"}]
}
mb_extracted["muscleblaze-biozyme-performance-whey"]["variants"] = [
    {"title": "Rich Chocolate 2kg", "price": "4499", "compare_at_price": "7399", "sku": "biozyme-2kg", "available": True}
]
mb_extracted["muscleblaze-100-clean-raw-whey-protein-concentrate"]["variants"] = [
    {"title": "Unflavoured 1kg", "price": "1799", "compare_at_price": "2399", "sku": "raw-whey-1kg", "available": True}
]
mb_extracted["muscleblaze-hi-protein-bar-30g-protein"]["variants"] = [
    {"title": "Choco Almond Pack of 6", "price": "791", "compare_at_price": "900", "sku": "mb-bar-6", "available": True}
]

# Ensure store keys exist in snapshot
snapshot["bigmusclesnutrition.com"] = list(bm_extracted.values())
snapshot["thewholetruthfoods.com"] = list(twt_extracted.values())
snapshot["avvatarindia.com"] = list(av_extracted.values())
snapshot["muscleblaze.com"] = list(mb_extracted.values())

SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated store_snapshot.json with Bigmuscles ({len(bm_extracted)}), TWT ({len(twt_extracted)}), Avvatar ({len(av_extracted)}), MB ({len(mb_extracted)}).")
