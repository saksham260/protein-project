import re

with open('protein-etl/scratch/amul_live_storedata.js', 'r', encoding='utf-8', errors='ignore') as f:
    txt = f.read()

matches = re.findall(r'"([^"]*protein[^"]*)"', txt, re.I)
print(f"Protein strings found: {len(matches)}")
for m in matches[:10]:
    print(" ", m)

imgs = re.findall(r'"([^"]*\.(?:png|jpg|webp))"', txt, re.I)
print(f"Images found: {len(imgs)}")
for img in imgs:
    if 'protein' in img.lower() or 'milk' in img.lower() or 'dahi' in img.lower():
        print(" ", img)
