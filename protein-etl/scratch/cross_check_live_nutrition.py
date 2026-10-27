import json
from dotenv import dotenv_values
from supabase import create_client

cfg = dotenv_values('protein-etl/.env')
client = create_client(cfg.get('SUPABASE_URL'), cfg.get('SUPABASE_SERVICE_KEY'))

with open('protein-etl/data/seed_products.json', 'r', encoding='utf-8') as f:
    local_prods = json.load(f)

# Fetch all live variants
res = client.table('product_variants').select('id, slug, variant_name, serving_size_g, net_weight_g, calories_kcal, protein_g, total_carbs_g, total_fat_g, mrp_inr').execute()
live_vars = {v['slug']: v for v in res.data}

mismatches = []
matched_count = 0
unmatched_local = []

for p in local_prods:
    p_slug = p['slug']
    for v in p.get('variants', []):
        combined_slug = f"{p_slug}-{v.get('slug')}"
        lv = live_vars.get(combined_slug)
        if not lv:
            lv = live_vars.get(v.get('slug'))
        if not lv:
            unmatched_local.append(combined_slug)
            continue
            
        matched_count += 1
        n = v.get('nutrition', {})
        diffs = []
        for field, l_val, lv_val in [
            ('serving_size_g', v.get('serving_size_g'), lv.get('serving_size_g')),
            ('net_weight_g', v.get('net_weight_g'), lv.get('net_weight_g')),
            ('protein_g', n.get('protein_g'), lv.get('protein_g')),
            ('calories_kcal', n.get('calories_kcal'), lv.get('calories_kcal')),
            ('total_carbs_g', n.get('total_carbs_g'), lv.get('total_carbs_g')),
            ('total_fat_g', n.get('total_fat_g'), lv.get('total_fat_g')),
            ('mrp_inr', v.get('mrp_inr'), lv.get('mrp_inr'))
        ]:
            if l_val is not None and lv_val is not None:
                if abs(float(l_val) - float(lv_val)) > 0.1:
                    diffs.append(f'{field}: local={l_val} vs live={lv_val}')
        if diffs:
            mismatches.append((combined_slug, diffs))

print(f'Matched variants: {matched_count}')
print(f'Unmatched local: {len(unmatched_local)}')
print(f'Mismatches found: {len(mismatches)}')
if mismatches:
    for slug, diffs in mismatches[:15]:
        print(f'  {slug}:')
        for d in diffs:
            print(f'    {d}')
