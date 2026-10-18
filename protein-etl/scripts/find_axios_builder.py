import urllib.request
import re

url = "https://shop.amul.com/global/assets/mystore/js/mystore_vue-4c271a2f755.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    js = r.read().decode("utf-8", errors="ignore")

p = js.find("axios(o.url,d)")
if p != -1:
    print(js[max(0, p-1200):p+100])
