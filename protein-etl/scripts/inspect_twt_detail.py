import urllib.request, json, re
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=12).read().decode("utf-8")

# Let's inspect TWT HTML for nutrition / macro tables
twt_urls = [
    "https://thewholetruthfoods.com/products/unflavoured-30-g-pure-whey-protein-isolate",
    "https://thewholetruthfoods.com/products/unflavored-26g-whey-protein-isolate-concentrate",
    "https://thewholetruthfoods.com/products/light-cocoa-24g-whey-protein-isolate-concentrate",
    "https://thewholetruthfoods.com/products/double-cocoa-25g-plant-protein"
]

twt_data = {}
for u in twt_urls:
    h = u.split("/")[-1]
    html = fetch(u)
    # Search for all image tags
    imgs = list(set(re.findall(r'(https://media\.thewholetruthfoods\.com/public/backend-assets/[^"\'\s>]+)', html)))
    # Search for nutrition facts in HTML
    nut_m = re.findall(r'(\d+(?:\.\d+)?\s*(?:g|kcal|mg|mcg))', html)
    twt_data[h] = {
        "images": imgs,
        "sample_nut": nut_m[:20]
    }
    print(f"TWT {h}: {len(imgs)} backend images")

with open("protein-etl/data/demo_catalog/twt_detail_scans.json", "w", encoding="utf-8") as f:
    json.dump(twt_data, f, indent=2, ensure_ascii=False)
