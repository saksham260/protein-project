import urllib.request, json, re, urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}

mb_items = [
    ("muscleblaze-super-gainer-xxl", "super gainer xxl"),
    ("muscleblaze-mass-gainer-pro", "mass gainer pro"),
    ("muscleblaze-100-micellar-casein", "100% micellar casein"),
    ("muscleblaze-biozyme-iso-zero-low-carb", "biozyme iso zero"),
    ("muscleblaze-fuel-one-protein-shake-hazelnut-cafe", "fuel one protein shake hazelnut"),
    ("muscleblaze-fuel-one-protein-shake-belgian-chocolate", "fuel one protein shake chocolate"),
    ("muscleblaze-high-protein-oats-dark-chocolate", "high protein oats dark chocolate"),
    ("gritzo-supermilk-for-young-athletes-boys-13-yrs", "gritzo supermilk boys 13"),
    ("gritzo-supermilk-for-young-athletes-girls-13-yrs", "gritzo supermilk girls 13"),
    ("healthkart-high-protein-muesli-dark-chocolate-cranberry", "healthkart protein muesli dark chocolate")
]

for slug, q in mb_items:
    # Try searching Healthkart API or MuscleBlaze
    url = f"https://www.healthkart.com/search?q={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            # Look for product JSON or image links
            imgs = list(dict.fromkeys(re.findall(r'(https://img\d*\.hkrtcdn\.com/[^"\'\s>]+)', html)))
            filtered = [i for i in imgs if any(k in i.lower() for k in ["prd_", "secprd", "product"]) and not any(k in i.lower() for k in ["banner", "icon", "logo", "review", "sprite"])]
            print(f"\n{slug} (q={q}) -> found {len(filtered)} images")
            for img in filtered[:2]:
                print("  ", img)
    except Exception as e:
        print(f"\n{slug} ERR: {e}")
