import urllib.request, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return 0, str(e)

# Test Avvatar
status, html = fetch("https://avvatarindia.com/product/100-performance-whey-belgain-chocolate-flavour-1-kg")
print(f"Avvatar Belgian Choc 1kg: status={status}, len={len(html)}")
if status == 200:
    # Find title, price, images, script tags
    title = re.findall(r'<title>(.*?)</title>', html, re.I)
    print("Title:", title)
    # Check for ld+json or next data or state
    ld_jsons = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    print(f"ld+json found: {len(ld_jsons)}")
    if ld_jsons:
        print("ld+json sample:", ld_jsons[0][:300])

# Test categories
status, html = fetch("https://avvatarindia.com/categories/isorich-protein")
print(f"Avvatar ISORICH cat: status={status}, len={len(html)}")
if status == 200:
    links = set(re.findall(r'href="([^"]*product/[^"]*)"', html))
    print("Product links in ISORICH cat:", links)

status, html = fetch("https://avvatarindia.com/categories/alpha-whey")
print(f"Avvatar Alpha Whey cat: status={status}, len={len(html)}")
if status == 200:
    links = set(re.findall(r'href="([^"]*product/[^"]*)"', html))
    print("Product links in Alpha Whey cat:", links)
