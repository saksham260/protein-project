import json
import urllib.request
import urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

searches = [
    ('maxprotein.in', 'max-protein-7-grain-protein-cookie-choco-chips', 'choco chips cookie'),
    ('maxprotein.in', 'max-protein-7-grain-protein-cookie-oats-raisins', 'oats raisins cookie'),
    ('maxprotein.in', 'max-protein-7-grain-protein-cookie-nuts-seeds', 'nuts seeds cookie'),
    ('getphab.com', 'phab-high-protein-bar-strawberries-cream', 'strawberries cream bar'),
    ('eatbetterco.com', 'eat-better-co-high-protein-spicy-seed-trail-mix-nut-free', 'seed trail mix'),
    ('lofoods.fit', 'lo-foods-ultra-low-carb-keto-atta-3g-net-carbs', 'keto atta'),
    ('bigmusclesnutrition.com', 'bigmuscles-nutrition-real-mass-gainer', 'real mass gainer'),
    ('wellbeingnutrition.com', 'wellbeing-nutrition-superfood-plant-protein-french-vanilla', 'superfood plant protein vanilla')
]

results = {}

for domain, slug, q in searches:
    url = f"https://{domain}/search/suggest.json?q={urllib.parse.quote(q)}&resources[type]=product&resources[options][unavailable_products]=show"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            prods = data.get('resources', {}).get('results', {}).get('products', [])
            results[slug] = []
            for p in prods[:3]:
                results[slug].append({
                    'title': p.get('title'),
                    'handle': p.get('handle'),
                    'image': p.get('image'),
                    'url': f"https://{domain}/products/{p.get('handle')}"
                })
    except Exception as e:
        results[slug] = f"ERR: {e}"

with open('protein-etl/scratch/shopify_batch2_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Saved to protein-etl/scratch/shopify_batch2_results.json")
