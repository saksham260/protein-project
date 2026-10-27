import urllib.request, re

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.avvatarindia.com/sitemap.xml"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        xml = r.read().decode('utf-8')
        prods = re.findall(r'<loc>(https://www.avvatarindia.com/product/[^<]+)</loc>', xml)
        print(f"Total Avvatar product URLs: {len(prods)}")
        for p in prods:
            if 'mass' in p.lower() or 'gainer' in p.lower() or 'isolate' in p.lower() or 'isorich' in p.lower():
                print(" ", p)
except Exception as e:
    print("ERR:", e)
