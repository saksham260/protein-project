"""Inspect Kapiva Next Data, Fuel One HTML, and XLR8 sitemap."""
import json
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent / "data" / "demo_catalog" / "scratch"

# 1. Kapiva Next Data
if (ROOT / "kapiva_next_data.json").exists():
    with open(ROOT / "kapiva_next_data.json", encoding="utf-8") as f:
        kd = json.load(f)
    print("=== Kapiva Next Data Keys ===")
    print("page:", kd.get("page"))
    props = kd.get("props", {}).get("pageProps", {})
    print("pageProps keys:", list(props.keys()))

# 2. Fuel One HTML
with open(ROOT / "fuelone_home.html", encoding="utf-8") as f:
    f_html = f.read()
soup = BeautifulSoup(f_html, "html.parser")
print("\n=== Fuel One HTML ===")
print("Scripts count:", len(soup.find_all("script")))
for s in soup.find_all("script")[:5]:
    src = s.get("src", "")
    if src:
        print("  script src:", src[:80])
    elif s.string:
        print("  inline script:", s.string.strip()[:100])

# 3. XLR8 Sitemap
print("\n=== XLR8 Sitemap ===")
try:
    r = httpx.get("https://xlr8sport.com/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    print("Sitemap status:", r.status_code)
    if r.status_code == 200:
        lines = [l.strip() for l in r.text.splitlines() if "<loc>" in l]
        print(f"Total locs: {len(lines)}")
        prod_locs = [l for l in lines if "/products/" in l]
        print(f"Product locs: {len(prod_locs)}")
        for pl in prod_locs[:10]:
            print(" ", pl)
except Exception as e:
    print("Sitemap error:", e)
