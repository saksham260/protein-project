import json, re

with open('protein-etl/data/demo_catalog/scratch/kapiva_next_data.json', 'r', encoding='utf-8') as f:
    kd = json.load(f)

# Search all keys and objects in kd for protein
kd_str = json.dumps(kd)
print("Length of kd_str:", len(kd_str))
imgs = re.findall(r'https://[^\s"\'<>]+\.(?:jpg|png|webp)', kd_str)
print(f"Total image URLs found in kapiva_next_data: {len(imgs)}")
for img in set(imgs):
    if any(k in img.lower() for k in ['protein', 'women', 'dia', 'shake']):
        print("  ", img)
