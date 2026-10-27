import urllib.request, re, json

headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("https://www.muscleblaze.com/sitemap.xml", headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    xml = r.read().decode('utf-8')

urls = re.findall(r'<loc>(https://www.muscleblaze.com/sv/[^<]+)</loc>', xml)
print(f"Total MB product URLs in sitemap: {len(urls)}")

targets = [
    ("super-gainer-xxl", "Super Gainer XXL"),
    ("mass-gainer-pro", "Mass Gainer Pro"),
    ("micellar-casein", "100% Micellar Casein"),
    ("iso-zero", "Biozyme Iso-Zero"),
    ("protein-shake", "Fuel One Protein Shake"),
    ("oats", "High Protein Oats")
]

matched = {}
for u in urls:
    for key, name in targets:
        if key in u.lower():
            matched.setdefault(key, []).append(u)

for k, matches in matched.items():
    print(f"\nTarget: {k} -> {len(matches)} matches")
    for m in matches[:5]:
        print(" ", m)

with open('protein-etl/scratch/mb_sitemap_matches.json', 'w', encoding='utf-8') as f:
    json.dump(matched, f, indent=2)
