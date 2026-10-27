import urllib.request, re, json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

urls = [
    "https://www.plixlife.com/product/womens-protein-super-foods",
    "https://www.plixlife.com/product/women-protein",
    "https://www.plixlife.com/product/daily-superfood-green-protein",
    "https://www.plixlife.com/product/supergreens-powder"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
            if m:
                d = json.loads(m.group(1))
                pp = d.get("props", {}).get("pageProps", {})
                ppd = pp.get("productPageData")
                print(f"[FOUND] {url}")
                print(f"  ppd type: {type(ppd)}")
                if isinstance(ppd, dict):
                    print(f"  ppd keys: {list(ppd.keys())}")
                    if "product" in ppd and ppd["product"]:
                        print(f"  product: {ppd['product'].get('name')}")
                        for m_item in ppd['product'].get('media', []):
                            print(f"    img: {m_item.get('url')}")
    except Exception as e:
        print(f"[ERR] {url}: {e}")
