import urllib.request

url = "https://shop.amul.com/ms/store/amul/auto/6731f68069aefe00369e525b/themeinfo.js?version=ms176132367_bootstrap4vuejs1792150818689"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    t_js = r.read().decode("utf-8", errors="ignore")

pos = 0
while True:
    p = t_js.find("atlas_search", pos)
    if p == -1:
        break
    print(f"=== atlas_search at {p} ===")
    print(t_js[max(0, p-100):min(len(t_js), p+300)])
    pos = p + 12
    if pos > 1000000:
        break
