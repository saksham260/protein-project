import urllib.request, json, re, xml.etree.ElementTree as ET

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return 0, str(e)

print("--- 1. Bigmuscles Nutrition ---")
status, text = fetch("https://bigmusclesnutrition.com/products.json?limit=250")
if status == 200:
    bm_data = json.loads(text)
    bm_products = bm_data.get("products", [])
    print(f"Total BM products: {len(bm_products)}")
    for p in bm_products:
        title = p.get("title", "")
        handle = p.get("handle", "")
        if any(k in title.lower() for k in ["premium gold", "titan", "plant"]):
            v_titles = [v.get("title") for v in p.get("variants", [])]
            prices = [v.get("price") for v in p.get("variants", [])]
            print(f"  BM Match: {title} | handle: {handle} | vars: {v_titles[:4]} | prices: {prices[:4]}")

print("\n--- 2. The Whole Truth ---")
status, text = fetch("https://thewholetruthfoods.com/sitemap.xml")
if status == 200:
    root = ET.fromstring(text)
    twt_urls = [elem.text for elem in root.iter() if elem.text and "thewholetruthfoods.com/products/" in elem.text]
    print(f"Total TWT product URLs in sitemap: {len(twt_urls)}")
    for u in twt_urls:
        if any(k in u for k in ["whey", "plant", "isolate"]):
            print(f"  TWT Match: {u}")

print("\n--- 3. MuscleBlaze ---")
status, text = fetch("https://www.muscleblaze.com/sitemap.xml")
if status == 200:
    try:
        root = ET.fromstring(text)
        mb_urls = [elem.text for elem in root.iter() if elem.text and ("muscleblaze.com" in elem.text)]
        print(f"Total MB URLs: {len(mb_urls)}")
        for u in mb_urls:
            if any(k in u.lower() for k in ["biozyme", "fuel-one", "raw-whey", "protein-bar"]):
                print(f"  MB Match: {u}")
    except Exception as e:
        print("XML parse err:", e)

print("\n--- 4. Avvatar Categories ---")
for cat in ["performance-whey", "alpha-whey", "isorich-protein"]:
    status, html = fetch(f"https://avvatarindia.com/categories/{cat}")
    if status == 200:
        links = set(re.findall(r'href="([^"]*product/[^"]*)"', html))
        valid = [l for l in links if not l.startswith("$")]
        print(f"  Avvatar {cat}: {len(valid)} products found. Sample: {valid[:3]}")
