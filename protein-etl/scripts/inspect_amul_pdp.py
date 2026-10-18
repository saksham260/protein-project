import urllib.request
import re
import json

test_urls = [
    "https://shop.amul.com/en/product/amul-high-protein-milk",
    "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-30",
    "https://shop.amul.com/en/product/amul-high-protein-dahi",
    "https://shop.amul.com/en/product/amul-high-protein-dahi-400-g-or-pack-of-2",
    "https://shop.amul.com/en/product/amul-high-protein-curd",
    "https://shop.amul.com/en/product/amul-high-protein-paneer-400-g-or-pack-of-2"
]

for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
        print(f"=== {url} -> HTTP {r.status}, length: {len(html)} ===")
        m_title = re.findall(r'<meta property="og:title" content="([^"]+)"', html)
        if m_title:
            print("  og:title:", m_title[0])
        m_desc = re.findall(r'<meta property="og:description" content="([^"]+)"', html)
        if m_desc:
            print("  og:description:", m_desc[0][:150])
        m_img = re.findall(r'<meta property="og:image" content="([^"]+)"', html)
        if m_img:
            print("  og:image:", m_img[0])
    except Exception as e:
        print(f"{url} -> {e}")
