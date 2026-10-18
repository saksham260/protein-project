"""Fetch and extract all Fuel One flagship products."""
import httpx
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"

urls = [
    ("fuel-one-whey-max", "https://www.fuelone.in/sv/fuel-one-whey-max-powder/SP-141763"),
    ("fuel-one-iso-max", "https://www.fuelone.in/sv/fuel-one-whey-iso-max/SP-122553"),
    ("fuel-one-whey-protein", "https://www.fuelone.in/sv/fuel-one-whey-protein/SP-125967"),
    ("fuel-one-impact-whey", "https://www.fuelone.in/sv/fuel-one-impact-whey-protein/SP-135075")
]

client = httpx.Client(follow_redirects=True, timeout=15, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})

all_fuelone = {}

for slug, url in urls:
    print(f"Fetching {slug}...")
    try:
        r = client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        chunks = []
        for s in soup.find_all("script"):
            t = s.string or ""
            if "self.__next_f.push" in t:
                m = re.search(r'self\.__next_f\.push\(\[(.*?)\}\]\)', t, re.DOTALL) or re.search(r'self\.__next_f\.push\(\[(.*)\]\)', t, re.DOTALL)
                if m:
                    try:
                        parsed = json.loads("[" + m.group(1) + "]")
                        if len(parsed) >= 2 and isinstance(parsed[1], str):
                            chunks.append(parsed[1])
                    except Exception:
                        pass
        full = "".join(chunks)
        idx = full.find('"results":')
        if idx != -1:
            b_start = full.rfind('{', 0, idx)
            cnt = 0
            b_end = b_start
            for i in range(b_start, len(full)):
                if full[i] == '{':
                    cnt += 1
                elif full[i] == '}':
                    cnt -= 1
                    if cnt == 0:
                        b_end = i + 1
                        break
            data = json.loads(full[b_start:b_end])
            res = data.get("results", {})
            print(f"  OK: {res.get('spName')} | offer: {res.get('offer_pr')} | mrp: {res.get('mrp')}")
            all_fuelone[slug] = res
        else:
            print("  No 'results' found")
    except Exception as e:
        print(f"  Error {slug}: {e}")

with open(ROOT / "fuelone_products.json", "w", encoding="utf-8") as f:
    json.dump(all_fuelone, f, indent=2)

print(f"Saved {len(all_fuelone)} Fuel One products to fuelone_products.json")
