import re

with open("protein-etl/data/demo_catalog/scratch/amul_storeinfo.js", encoding="utf-8") as f:
    text = f.read()

# Look for store settings in storeinfo.js
pos = text.find("settings")
while pos != -1:
    snippet = text[pos:pos+200]
    if "key" in snippet.lower() or "search" in snippet.lower():
        print("Found snippet:", snippet)
    pos = text.find("settings", pos+8)

# Check themeinfo.js as well
import urllib.request
url = "https://shop.amul.com/ms/store/amul/auto/6731f68069aefe00369e525b/themeinfo.js?version=ms176132367_bootstrap4vuejs1792150818689"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        t_js = r.read().decode("utf-8", errors="ignore")
    print("themeinfo length:", len(t_js))
    pos2 = t_js.find("expertrec")
    if pos2 != -1:
        print("Found in themeinfo:", t_js[max(0, pos2-50):pos2+100])
except Exception as e:
    print("themeinfo error:", e)
