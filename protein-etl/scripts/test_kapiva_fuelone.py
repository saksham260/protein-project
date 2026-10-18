"""Inspect Kapiva and Fuel One structure."""
import json
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"

# 1. Kapiva inspection
with open(ROOT / "kapiva_next_data.json", encoding="utf-8") as f:
    kd = json.load(f)

page_props = kd.get("props", {}).get("pageProps", {})
data = page_props.get("data", {})
print("Kapiva pageProps.data keys:", list(data.keys()) if isinstance(data, dict) else type(data))

# Also test Kapiva collection page: e.g. /collections/nutrition or /collections/proteins
client = httpx.Client(follow_redirects=True, timeout=12, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})
for path in ["/collections/protein", "/collections/nutrition", "/collections/all"]:
    try:
        r = client.get(f"https://kapiva.in{path}")
        print(f"Kapiva {path} -> {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        nd = soup.find("script", id="__NEXT_DATA__")
        if nd:
            col_data = json.load(open(ROOT / "sample.json", "w", encoding="utf-8")) if False else json.loads(nd.string)
            print(f"  __NEXT_DATA__ page: {col_data.get('page')}")
            col_props = col_data.get("props", {}).get("pageProps", {})
            print(f"  col_props keys: {list(col_props.keys())}")
    except Exception as e:
        print(f"Kapiva {path} error: {e}")

# 2. Fuel One inspection
# Fuel One is Next.js app hosted on HealthKart CDN (static1.hkrtcdn.com/fuelone)
# Let's inspect fuelone_home.html for links, api calls, or Next.js state
with open(ROOT / "fuelone_home.html", encoding="utf-8") as f:
    f_html = f.read()

soup_f = BeautifulSoup(f_html, "html.parser")
nd_f = soup_f.find("script", id="__NEXT_DATA__")
if nd_f:
    print("\nFuel One has __NEXT_DATA__!")
else:
    print("\nFuel One has NO __NEXT_DATA__ (likely App Router)")
    # Check for self.__next_f.push scripts
    next_f = [s.string for s in soup_f.find_all("script") if s.string and "self.__next_f.push" in s.string]
    print(f"Fuel One App Router self.__next_f scripts: {len(next_f)}")

# Let's check sitemap on www.fuelone.in
try:
    r = client.get("https://www.fuelone.in/sitemap.xml")
    print(f"\nFuel One sitemap.xml -> {r.status_code}")
    if r.status_code == 200:
        locs = [l.strip() for l in r.text.splitlines() if "<loc>" in l]
        print(f"Total locs: {len(locs)}")
        for l in locs[:10]:
            print(" ", l)
except Exception as e:
    print("Fuel One sitemap error:", e)
