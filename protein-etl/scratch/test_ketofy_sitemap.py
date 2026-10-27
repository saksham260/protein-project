import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
try:
    req = urllib.request.Request("https://www.ketofy.in/sitemap.xml", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        xml = r.read().decode('utf-8')
        print("Ketofy sitemap length:", len(xml))
        print("Ketofy sitemap head:", xml[:500])
except Exception as e:
    print("ERR:", e)
