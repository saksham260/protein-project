import urllib.request, json, xml.etree.ElementTree as ET

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=12) as r:
        return r.read().decode("utf-8", errors="ignore")

# 1. Bigmuscles
data = json.loads(fetch("https://bigmusclesnutrition.com/products.json?limit=250"))
for p in data.get("products", []):
    t = p.get("title", "")
    h = p.get("handle", "")
    if any(k in t.lower() for k in ["premium gold", "titan", "plant protein isolate", "real whey", "raw"]):
        print(f"BM: {t} -> {h}")

# 2. TWT
text = fetch("https://thewholetruthfoods.com/sitemap.xml")
root = ET.fromstring(text)
for elem in root.iter():
    if elem.text and "thewholetruthfoods.com/products/" in elem.text:
        u = elem.text
        if any(k in u for k in ["whey", "plant"]):
            print(f"TWT: {u}")
