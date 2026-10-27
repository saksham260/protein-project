import urllib.request, json, re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

urls = {
    "muscleblaze-super-gainer-xxl": "https://www.muscleblaze.com/sv/muscleblaze-super-gainer-xxl-weight-gainer/SP-42633",
    "muscleblaze-mass-gainer-pro": "https://www.muscleblaze.com/sv/muscleblaze-mass-gainer-pro-with-creapure/SP-38414",
    "muscleblaze-100-micellar-casein": "https://www.muscleblaze.com/sv/muscleblaze-100-micellar-casein/SP-38554",
    "muscleblaze-biozyme-iso-zero-low-carb": "https://www.muscleblaze.com/sv/muscleblaze-biozyme-iso-zero/SP-101666",
    "muscleblaze-high-protein-oats-dark-chocolate": "https://www.muscleblaze.com/sv/muscleblaze-high-protein-oats/SP-98284",
    "muscleblaze-fuel-one-protein-shake": "https://www.muscleblaze.com/sv/muscleblaze-18g-protein-shake-no-added-sugar/SP-97258"
}

results = {}

for slug, url in urls.items():
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
        ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        prod = None
        for item in ld:
            try:
                p = json.loads(item)
                t = p.get("@type")
                if t == "Product" or (isinstance(t, list) and "Product" in t):
                    prod = p
                    break
            except:
                pass
        
        main_img = prod.get("image") if prod else None
        hk_imgs = list(dict.fromkeys(re.findall(r'(https://img\d*\.hkrtcdn\.com/[^"\'\s>]+)', html)))
        filtered_imgs = [i for i in hk_imgs if any(k in i.lower() for k in ["prd_", "product", "secprd"]) and not any(k in i.lower() for k in ["banner", "icon", "logo", "review", "sprite"])]
        
        results[slug] = {
            "name": prod.get("name") if prod else None,
            "main_img": main_img,
            "filtered_imgs": filtered_imgs[:5]
        }
        print(f"\n[OK] {slug} -> Name: {results[slug]['name']}")
        print(f"  Main Img: {main_img}")
        for img in filtered_imgs[:2]:
            print(f"  HK Img:   {img}")
    except Exception as e:
        print(f"\n[ERR] {slug}: {e}")

with open('protein-etl/scratch/mb_exact_images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
