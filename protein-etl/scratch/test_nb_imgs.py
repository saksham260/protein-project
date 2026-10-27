import urllib.request, json

headers = {"User-Agent": "Mozilla/5.0"}

urls = [
    ("nutrabay-pure-100-raw-whey-protein-concentrate", "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1010-01-1789475113-200x200.webp"),
    ("nutrabay-gold-tri-blend-whey-protein", "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1014-12-400x400.webp"),
    ("nutrabay-gold-hydrolyzed-pea-protein-isolate", "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1102-02-1787736317-200x200.webp"),
    ("nutrabay-wellness-vegan-plant-protein-powder-with-superfoods", "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1054-03-1753299718-200x200.webp"),
    ("nutrabay-gold-vital-whey-protein", "https://cdn2.nutrabay.com/uploads/variant/images/thumbnail_image-NB-NUT-1064-03-1758998117-200x200.webp")
]

for slug, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"[OK] {slug} -> {r.status} {r.headers.get('content-type')} {len(r.read())} bytes")
    except Exception as e:
        print(f"[ERR] {slug} -> {e}")
