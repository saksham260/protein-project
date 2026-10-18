import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

pos = js.find("_httpDefaults")
if pos != -1:
    print(js[max(0, pos-100):min(len(js), pos+300)])

pos2 = js.find("token")
while pos2 != -1:
    snippet = js[max(0, pos2-50):min(len(js), pos2+150)]
    if "header" in snippet.lower() or "auth" in snippet.lower() or "bearer" in snippet.lower():
        print("Found token header snippet:")
        print(snippet)
    pos2 = js.find("token", pos2+6)
