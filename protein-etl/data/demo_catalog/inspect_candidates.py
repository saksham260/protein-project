import httpx

headers = {"User-Agent": "Mozilla/5.0"}

def inspect_store(domain, terms):
    r = httpx.get(f"https://{domain}/products.json?limit=250", headers=headers, timeout=12.0)
    prods = r.json().get("products", [])
    print(f"\n==================== {domain} ({len(prods)} products) ====================")
    for p in prods:
        t = p["title"]
        h = p["handle"]
        if any(term.lower() in t.lower() for term in terms):
            vars_info = [f"{v['title']} (INR {v['price']})" for v in p.get("variants", [])[:3]]
            print(f"- {t}")
            print(f"  handle: {h}")
            print(f"  variants: {vars_info}")

inspect_store("pintola.in", ["peanut butter", "muesli", "protein", "rice cake"])
inspect_store("bagrrys.com", ["protein", "muesli", "peanut butter", "oats"])
inspect_store("bigmusclesnutrition.com", ["whey", "protein", "isolate"])
