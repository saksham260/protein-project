import urllib.request, json, urllib.parse

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': 'application/json'}

searches = [
    ('itcstore.in', 'aashirvaad-proactive-high-protein-multigrain-atta', 'proactive atta'),
    ('itcstore.in', 'aashirvaad-proactive-high-protein-multigrain-atta-alt', 'aashirvaad proactive'),
    ('rawpressery.com', 'raw-pressery-high-protein-milkshake-cold-coffee', 'protein coffee milkshake'),
    ('rawpressery.com', 'raw-pressery-high-protein-milkshake-cold-coffee-alt', 'cold coffee protein'),
    ('urbanplatter.in', 'urban-platter-organic-non-gmo-firm-tofu-block', 'organic tofu')
]

for domain, slug, q in searches:
    url = f"https://{domain}/search/suggest.json?q={urllib.parse.quote(q)}&resources[type]=product&resources[options][unavailable_products]=show"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
            prods = d.get('resources', {}).get('results', {}).get('products', [])
            print(f"\n{slug} on {domain} (q={q}) -> found {len(prods)}")
            for p in prods[:2]:
                print(f"  {p.get('title')} | {p.get('image')}")
    except Exception as e:
        print(f"\n{slug} on {domain} ERR: {e}")
