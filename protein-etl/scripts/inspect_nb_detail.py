import urllib.request, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scratch = ROOT / "protein-etl" / "data" / "demo_catalog" / "scratch"

url = "https://nutrabay.com/product/nutrabay-gold-100-whey-protein-concentrate"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="ignore")

m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    pageProps = data.get("props", {}).get("pageProps", {})
    print("pageProps keys:", list(pageProps.keys()))
    with open(scratch / "nb_page_props.json", "w", encoding="utf-8") as f:
        json.dump(pageProps, f, indent=2, ensure_ascii=False)
    print("Saved pageProps to scratch/nb_page_props.json")
else:
    print("NEXT_DATA not found")
