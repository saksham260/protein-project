"""Script to recover the exact picks.txt and readings.jsonl before checkout."""
import json
from pathlib import Path

LOG_PATH = Path(r"C:\Users\Saksham\.gemini\antigravity-ide\brain\1fa62d0a-8ca6-47bb-b9cc-7dcd95ac81a8\.system_generated\logs\transcript_full.jsonl")

# Search for the step where build_batch4b.py was run or where readings were appended
found_steps = []
with open(LOG_PATH, encoding="utf-8") as f:
    for line in f:
        if "build_batch4b" in line or "build_batch4a" in line or "batch3" in line:
            obj = json.loads(line)
            idx = obj.get("step_index")
            s = json.dumps(obj)
            if "Appended" in s and "picks" in s:
                found_steps.append((idx, s[:200]))

print(f"Found {len(found_steps)} append steps:")
for idx, s in found_steps[-10:]:
    print(idx, s)
