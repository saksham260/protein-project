import re, json

with open('protein-etl/data/demo_catalog/scratch/amul_storedata.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("Length of amul_storedata.js:", len(text))

# Search for products with protein or milk or dahi
matches = re.findall(r'(\{[^{}]*"name"\s*:\s*"[^"]*(?:protein|dahi|milk)[^"]*"[^{}]*\})', text, re.I)
print(f"Found {len(matches)} product objects")

for m in matches[:10]:
    try:
        # Extract name, slug, image
        name = re.findall(r'"name"\s*:\s*"([^"]+)"', m)
        slug = re.findall(r'"slug"\s*:\s*"([^"]+)"', m)
        img = re.findall(r'"image"\s*:\s*"([^"]+)"', m) or re.findall(r'"thumbnail"\s*:\s*"([^"]+)"', m) or re.findall(r'https://[^"]+\.(?:jpg|png|webp)', m)
        print(f"Name: {name} | Slug: {slug} | Img: {img}")
    except Exception as e:
        pass
