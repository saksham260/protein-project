import sys
sys.path.insert(0, "protein-etl/scratch")
from prepare_wave_1_data import WAVE_1_PRODUCTS

PACK_MATH_TOLERANCE = 0.25

print("Checking pack math drift for all Wave 1 products...")
issues = []
for p in WAVE_1_PRODUCTS:
    net = float(p["net"])
    serv = float(p["serv"])
    spp = max(1, round(net / serv))
    drift = abs(spp * serv - net) / net
    if drift > PACK_MATH_TOLERANCE:
        issues.append(f"FAIL {drift:.1%}: {p['name']} (net={net}, serv={serv}, spp={spp}, total={spp*serv})")
    elif drift > 0.15:
        print(f"WARN {drift:.1%}: {p['name']} (net={net}, serv={serv}, spp={spp}, total={spp*serv})")

if issues:
    print(f"Found {len(issues)} issues:")
    for iss in issues:
        print(" ", iss)
else:
    print("All products pass pack math tolerance!")
