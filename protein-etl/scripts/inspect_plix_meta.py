import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"

with open(scratch / "plix_sample_pdp.json", encoding="utf-8") as f:
    ppd = json.load(f)

p = ppd.get("product", {})
print("Thumbnail:", p.get("thumbnail"))
print("Thumbnail2x:", p.get("thumbnail2x"))
print("Images list:", p.get("images"))

metadata = p.get("metadata", [])
for item in metadata:
    k = item.get("key")
    v = item.get("value")
    if any(term in k.lower() for term in ["nutrition", "ingredient", "detail", "image", "know"]):
        print(f"\n--- Metadata: {k} ---")
        try:
            parsed = json.loads(v)
            print(json.dumps(parsed, indent=2)[:1000])
        except Exception:
            print(str(v)[:500])
