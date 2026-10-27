import json
import urllib.request
import urllib.parse
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

SHOPIFY_DOMAINS = {
    'Ketofy': 'www.ketofy.in',
    'Max Protein': 'maxprotein.in',
    'OZiva': 'www.oziva.in',
    'Kapiva': 'kapiva.in',
    'Plix': 'www.plixlife.com',
    'Phab': 'getphab.com',
    'Eat Better Co': 'eatbetterco.com',
    'Urban Platter': 'urbanplatter.in',
    'Lo! Foods': 'lofoods.fit',
    'Bigmuscles Nutrition': 'bigmusclesnutrition.com',
    'Wellbeing Nutrition': 'wellbeingnutrition.com',
    'Milky Mist': 'shop.milkymist.com',
    'Epigamia': 'epigamia.com',
    'Optimum Nutrition': 'www.optimumnutrition.co.in'
}

def search_shopify_store(domain, query):
    encoded_q = urllib.parse.quote(query)
    url = f"https://{domain}/search/suggest.json?q={encoded_q}&resources[type]=product&resources[options][unavailable_products]=show"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            prods = data.get('resources', {}).get('results', {}).get('products', [])
            return prods
    except Exception as e:
        # Fallback to products.json search
        return f"ERR: {e}"

def test_domains():
    results = {}
    for brand, domain in SHOPIFY_DOMAINS.items():
        res = search_shopify_store(domain, 'protein')
        if isinstance(res, list):
            results[brand] = f"OK ({len(res)} prods returned)"
        else:
            results[brand] = res
    return results

if __name__ == '__main__':
    res = test_domains()
    for b, status in res.items():
        print(f"{b:20} -> {status}")
