"""Extract Next.js flight payload cleanly from Fuel One."""
import httpx
from bs4 import BeautifulSoup
import json
import re

url = "https://www.fuelone.in/sv/fuel-one-whey-max-powder/SP-141763"
r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}, timeout=12)

soup = BeautifulSoup(r.text, "html.parser")
combined_chunks = []

for s in soup.find_all("script"):
    text = s.string or ""
    if "self.__next_f.push" in text:
        # Match array inside self.__next_f.push(...)
        m = re.search(r'self\.__next_f\.push\(\[(.*?)\}\]\)', text, re.DOTALL)
        if not m:
            m = re.search(r'self\.__next_f\.push\(\[(.*)\]\)', text, re.DOTALL)
        if m:
            try:
                # Wrap in brackets to make valid JSON: [ <content> ]
                raw_json = "[" + m.group(1) + "]"
                parsed = json.loads(raw_json)
                if len(parsed) >= 2 and isinstance(parsed[1], str):
                    combined_chunks.append(parsed[1])
            except Exception:
                pass

full_str = "".join(combined_chunks)
print(f"Total decoded flight payload length: {len(full_str)}")

# Search for "results": in full_str
idx = full_str.find('"results":')
if idx != -1:
    print("Found 'results': at position", idx)
    # Search for { before "results"
    brace_start = full_str.rfind('{', 0, idx)
    # Find matching brace
    count = 0
    end = brace_start
    for i in range(brace_start, len(full_str)):
        if full_str[i] == '{':
            count += 1
        elif full_str[i] == '}':
            count -= 1
            if count == 0:
                end = i + 1
                break
    try:
        data = json.loads(full_str[brace_start:end])
        res = data.get("results", {})
        print("SUCCESS! Product:", res.get("spName"))
        print("Variants:", len(res.get("variants", [])))
        for v in res.get("variants", []):
            print(" ", v.get("variantName"), "| Price:", v.get("offerPrice"), "| MRP:", v.get("mrp"))
        with open("protein-etl/data/demo_catalog/scratch/fuelone_whey_max.json", "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print("Saved fuelone_whey_max.json successfully!")
    except Exception as e:
        print("JSON parse error:", e)
