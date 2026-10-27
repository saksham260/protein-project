import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
try:
    req = urllib.request.Request("https://www.muscleblaze.com/sitemap.xml", headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        xml = r.read().decode('utf-8')
        print("MB sitemap length:", len(xml))
        print("MB sitemap snippet:", xml[:500])
except Exception as e:
    print("ERR:", e)
