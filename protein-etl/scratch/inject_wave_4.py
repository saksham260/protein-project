"""Inject Wave 4 (20 Clinical & Adult Nutrition Products) into the catalog.
This script:
1. Reads WAVE_4_PRODUCTS from prepare_wave_4_data.py
2. Appends lines to picks.txt, readings.jsonl, and manual_entries.jsonl
3. Verifies line counts and alignment
"""

import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
DATA_DIR = REPO / "protein-etl" / "data" / "demo_catalog"

# Import WAVE_4_PRODUCTS
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_wave_4_data import WAVE_4_PRODUCTS

def run_injection():
    picks_file = DATA_DIR / "picks.txt"
    readings_file = DATA_DIR / "readings.jsonl"
    manual_file = DATA_DIR / "manual_entries.jsonl"

    picks_lines = [l for l in picks_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    readings_lines = [l for l in readings_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    manual_lines = [l for l in manual_file.read_text(encoding="utf-8").splitlines() if l.strip()]

    print(f"Current baseline: picks={len(picks_lines)}, readings={len(readings_lines)}, manual_entries={len(manual_lines)}")
    assert len(picks_lines) == len(readings_lines), f"Mismatch: picks {len(picks_lines)} != readings {len(readings_lines)}"
    
    start_idx = len(picks_lines) + 1  # 560
    print(f"Injection starting at reading index: {start_idx}")

    new_picks = []
    new_readings = []
    new_manuals = []

    for offset, p in enumerate(WAVE_4_PRODUCTS):
        idx = start_idx + offset
        store, handle, category, brand = p["pick"]

        # 1. Pick line
        pick_line = f"{store}|{handle}|{category}|{brand}"
        new_picks.append(pick_line)

        # 2. Reading JSON
        reading_obj = {
            "i": idx,
            "v": 0,
            "name": p["name"],
            "variant": p["variant_title"],
            "net": float(p["net"]),
            "serv": float(p["serv"]),
            "label": p["label"],
            "n": p["n"],
            "ing": p["ing"],
            "allergens": p["allergens"],
            "tags": p["tags"],
            "desc": p["desc"],
            "protein_source": p["protein_source"],
            "protein_tier": p["protein_tier"],
        }
        if p.get("is_vegan"):
            reading_obj["is_vegan"] = True
        new_readings.append(json.dumps(reading_obj, ensure_ascii=False))

        # 3. Manual entry JSON
        manual_obj = {
            "handle": handle,
            "store": store,
            "brand": brand,
            "title": f"{brand} {p['name']}",
            "url": p["url"],
            "image_url": p["image_url"],
            "variants": [
                {
                    "id": 1,
                    "title": p["variant_title"],
                    "price": float(p["price"]),
                    "mrp": float(p["mrp"]),
                    "compare_at_price": float(p["mrp"]),
                    "net_weight_g": float(p["net"]),
                    "in_stock": True,
                    "image_url": p["image_url"],
                }
            ],
        }
        new_manuals.append(json.dumps(manual_obj, ensure_ascii=False))

    # Append to files
    all_picks = picks_lines + new_picks
    all_readings = readings_lines + new_readings
    all_manuals = manual_lines + new_manuals

    picks_file.write_text("\n".join(all_picks) + "\n", encoding="utf-8")
    readings_file.write_text("\n".join(all_readings) + "\n", encoding="utf-8")
    manual_file.write_text("\n".join(all_manuals) + "\n", encoding="utf-8")

    print(f"Successfully appended {len(WAVE_4_PRODUCTS)} products.")
    print(f"New counts: picks={len(all_picks)}, readings={len(all_readings)}, manual_entries={len(all_manuals)}")

if __name__ == "__main__":
    run_injection()
